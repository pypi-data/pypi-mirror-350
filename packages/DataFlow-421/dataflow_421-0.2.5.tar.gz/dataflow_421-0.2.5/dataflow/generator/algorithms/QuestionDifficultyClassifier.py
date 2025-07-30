import json
import os
import pandas as pd
from dataflow.generator.utils import APIGenerator_aisuite, APIGenerator_request
from dataflow.generator.utils.Prompts import QuestionDifficultyPrompt
import re
from dataflow.utils.registry import GENERATOR_REGISTRY
from dataflow.utils.utils import get_logger
from dataflow.data import MyScaleStorage, DatabaseConfig

@GENERATOR_REGISTRY.register()
class QuestionDifficultyClassifier():
    def __init__(self, args):
        """
        Initialize the QuestionCategoryClassifier with the provided configuration.
        """
        self.config = args
        self.prompts = QuestionDifficultyPrompt()
        use_db = args.get("use_db", False) or os.environ.get("USE_DB", "").lower() == "true"
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
            self.input_file = args.get("input_file")
            self.output_file = args.get("output_file")
        self.input_key = self.config.get("input_key", "data")
        self.read_key = self.config.get("read_key", "question")  # default key for question input
        self.output_key = self.config.get("output_key", "classification_result")  # default output key
        self.logger = get_logger()
        self.read_min_score = self.config.get('read_min_score', 0.9)
        self.read_max_score = self.config.get('read_max_score', 2.0)
        self.eval_stage = self.config.get('eval_stage',1)
        
        # Ensure input_file and output_file are provided
        if not self.storage and (not self.input_file or not self.output_file):
            raise ValueError("Both input_file and output_file must be specified in the config.")

        # Initialize the model
        self.model = self.__init_model__()
    
    def __init_model__(self):
        """
        Initialize the model generator based on the configuration.
        """
        generator_type = self.config.get("generator_type", "local").lower()
        
        if generator_type == "aisuite":
            return APIGenerator_aisuite(self.config)
        elif generator_type == "request":
            return APIGenerator_request(self.config)
        else:
            raise ValueError(f"Invalid generator type: {generator_type}")

    def _reformat_prompt(self, dataframe):
        """
        Reformat the prompts in the dataframe to generate questions.
        """
        # Check if read_key is in the dataframe
        if self.read_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"read_key: {self.read_key} not found in the dataframe. Available keys: {key_list}")

        formatted_prompts = []
        for i, text in enumerate(dataframe[self.read_key]):
            if text is not None:
                used_prompt = self.prompts.question_synthesis_prompt(text)
            else:
                used_prompt = None
            formatted_prompts.append(used_prompt.strip())

        return formatted_prompts

    def _load_input(self):
        if hasattr(self, 'storage'):
            value_list = self.storage.read_code_json(
                [self.input_key], stage=self.eval_stage, syn='syn_q', format='SFT_Single', maxmin_scores=[{'max_score': self.read_max_score, 'min_score': self.read_min_score}]
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
            output_rows = [
                {
                    "id": row.get("id"),
                    "difficulty_score": row.get("question_difficulty")
                }
                for row in output_rows
            ]
            self.storage.write_eval(output_rows, algo_name="QuestionDifficultyClassifier", score_key="difficulty_score")
        else:
            output_dir = os.path.dirname(self.output_file)
            os.makedirs(output_dir, exist_ok=True)
            dataframe.to_json(save_path, orient="records", lines=True)

    def run(self):
        # read input file : accept jsonl file only
        # dataframe = pd.read_json(self.input_file,lines=True)
        dataframe = self._load_input()
        # model = self.__init_model__()
        formatted_prompts = self._reformat_prompt(dataframe)
        responses = self.model.generate_text_from_input(formatted_prompts)

        rating_scores = []
        for response in responses:
            match = re.search(r'Rating:\s*([\d.]+)', response)
            score = float(match.group(1)) if match else -1
            rating_scores.append(score)

        #if self.output_key in dataframe.columns:
        #    key_list = dataframe.columns.tolist()
        #    raise ValueError(f"Found {self.output_text_key} in the dataframe, which leads to overwriting the existing column, please check the output_text_key: {key_list}")
        
        dataframe[self.output_key] = rating_scores
        
        
            # Save DataFrame to the output file
        # dataframe.to_json(self.output_file, orient="records", lines=True, force_ascii=False)
        self._write_output(self.output_file, dataframe, None)