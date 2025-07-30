import sys
from dataflow.generator.utils.Prompts import AnswerGeneratorPrompt
# from dataflow.generator.utils.LocalModelGenerator import LocalModelGenerator
from dataflow.generator.utils.APIGenerator_aisuite import APIGenerator_aisuite
from dataflow.generator.utils.APIGenerator_request import APIGenerator_request
from collections import defaultdict, Counter
# from dataflow.generator.algorithms.AnswerExtraction_qwenmatheval import AnswerExtraction_qwenmatheval
import yaml
import logging
import pandas as pd
from dataflow.utils.registry import GENERATOR_REGISTRY
from dataflow.utils.utils import get_logger, get_generator
import os
from dataflow.data import MyScaleStorage, DatabaseConfig
sys.path.append("..")
sys.path.append(".")
sys.path.append("../..")

@GENERATOR_REGISTRY.register()
class PseudoAnswerGenerator:
    '''
    Pseudo Answer Generator is a class that generates answers for given questions, then choose the most frequent answer.
    '''
    def __init__(self,config: dict):
        self.config = config
        self.prompt = AnswerGeneratorPrompt()
        use_db = config.get("use_db", False) or os.environ.get("USE_DB", "").lower() == "true"
        if use_db:
            db_config = DatabaseConfig(
                host=os.environ.get('MYSCALE_HOST', 'localhost'),
                port=int(os.environ.get('MYSCALE_PORT', '9000')),
                db_name=os.environ.get('MYSCALE_DATABASE', 'dataflow'),
                table_name=os.environ.get('MYSCALE_TABLE_NAME', ''),
                username=os.environ.get('MYSCALE_USER', ''),
                password=os.environ.get('MYSCALE_PASSWORD', '')
            )
            self.storage = MyScaleStorage(db_config)
            self.input_file = None
            self.output_file = None
        else:
            self.input_file = config.get("input_file")
            self.output_file= config.get("output_file")
        # self.input_file = self.config["input_file"]
        # self.output_file = self.config["output_file"]
        self.input_key = self.config["input_key"]
        self.read_key = self.config["read_key"]
        self.output_key_answer = self.config["output_key_answer"]
        self.output_key_answer_value = self.config["output_key_answer_value"]
        self.output_key_solutions = self.config["output_key_solutions"]
        self.output_key_correct_solution_example = self.config["output_key_correct_solution_example"]
        self.max_times = self.config["max_times"]
        self.model_generator = self.__init_model__()
        self.extractor = get_generator('AnswerExtraction_qwenmatheval', self.config) 
        self.logger = get_logger()
        self.read_min_score: list = self.config.get('read_min_score', [])
        self.read_max_score: list = self.config.get('read_max_score', [])
        self.eval_stage = self.config.get('eval_stage', 4)

    def __init_model__(self):
        if self.config["generator_type"] == "aisuite":
            return APIGenerator_aisuite(self.config)
        elif self.config["generator_type"] == "request":
            return APIGenerator_request(self.config)
        else:
            raise ValueError(f"Invalid generator type: {self.config['generator_type']}")
    
    def _load_input(self):
        if hasattr(self, 'storage'):
            value_list = self.storage.read_code_json(
                [self.input_key], stage=self.eval_stage, syn='syn_q', format='SFT_Single',  maxmin_scores=[dict(zip(['min_score', 'max_score'], list(_))) for _ in list(zip(self.read_min_score, self.read_max_score))]
            )
            return pd.DataFrame([
                {**item['data'], 'id': str(item['id'])}
                for item in value_list
            ])
        else:
            return pd.read_json(self.input_file, lines=True)

    def _write_output(self, save_path, dataframe, extractions):
        if hasattr(self, 'storage'):
            output_rows = dataframe.where(pd.notnull(dataframe), None).to_dict(orient="records")
            # output_rows = [
            #     {
            #         "id": row.get("id"),
            #         self.output_key_answer: row.get(self.output_key_answer),
            #         self.output_key_answer_value: row.get(self.output_key_answer_value),
            #         self.output_key_solutions: row.get(self.output_key_solutions),
            #         self.output_key_correct_solution_example: row.get(self.output_key_correct_solution_example),
            #     }
            #     for row in output_rows
            # ]
            self.storage.write_data(output_rows, format="SFT_Single", Synthetic="syn_qa")
        else:
            dataframe.to_json(save_path, orient="records", lines=True)

    def run(self):
        # read input file : accept jsonl file only
        self.logger.info(f"Reading input file: {self.input_file}")
        # dataframe = pd.read_json(self.input_file,lines=True)
        dataframe = self._load_input()
        input_data_number = dataframe.shape[0]
        # check if input_prompt_key are in the dataframe
        if self.read_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"read_key: {self.read_key} not found in the dataframe, please check the read_key: {key_list}")
        # check if output_text_key are in the dataframe
        if self.output_key_answer in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key_answer} in the dataframe, which leads to overwriting the existing column, please check the output_key: {key_list}")
        if self.output_key_solutions in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key_solutions} in the dataframe, which leads to overwriting the existing column, please check the output_key: {key_list}")
        if self.output_key_correct_solution_example in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key_correct_solution_example} in the dataframe, which leads to overwriting the existing column, please check the output_key: {key_list}")
        if self.output_key_answer_value in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key_answer_value} in the dataframe, which leads to overwriting the existing column, please check the output_key: {key_list}")
        # generate text
        user_prompts = dataframe[self.read_key].tolist()
        answer_dict = defaultdict(list)
        solution_dict = defaultdict(list)
        self.logger.info(f"Generating answers for {len(user_prompts)} questions")
        for i in range(self.max_times):
            self.logger.info(f"Generating: {i+1} times")
            solutions = self.model_generator.generate_text_from_input(user_prompts)
            answers = [self.extractor.answer_extractor.extract_answer(solution, self.extractor.data_name) for solution in solutions]
            for idx, answer in enumerate(answers):
                answer_dict[idx].append(answer)
                solution_dict[idx].append((answer, solutions[idx]))
        self.logger.info(f"Generating final answers")
        dataframe[self.output_key_answer] = dataframe.get(self.output_key_answer, None) 
        dataframe[self.output_key_solutions] = dataframe.get(self.output_key_solutions, None) 
        dataframe[self.output_key_correct_solution_example] = dataframe.get(self.output_key_correct_solution_example, None) 
        for key, value in answer_dict.items():
            count = Counter(value)
            final_answer = count.most_common(1)[0][0]
            dataframe.at[int(key),self.output_key_answer] = value
            dataframe.at[int(key),self.output_key_solutions] = final_answer
            correct_contents = [content for ans, content in solution_dict[key] if ans == final_answer]
            dataframe.at[int(key), self.output_key_solutions] = correct_contents
            correct_solution_example = correct_contents[0] if correct_contents else None
            dataframe.at[int(key), self.output_key_correct_solution_example] = correct_solution_example
            dataframe.at[int(key), self.output_key_answer_value] = final_answer
        # 过滤掉没有答案的行
        dataframe = dataframe[dataframe[self.output_key_answer_value].notna()]
        dataframe = dataframe[dataframe[self.output_key_correct_solution_example].notna()]
        self.logger.info(f"Data number {input_data_number} -> {dataframe.shape[0]}")
        # dataframe.to_json(self.output_file,orient="records",lines=True)

        self._write_output(self.output_file, dataframe, None)