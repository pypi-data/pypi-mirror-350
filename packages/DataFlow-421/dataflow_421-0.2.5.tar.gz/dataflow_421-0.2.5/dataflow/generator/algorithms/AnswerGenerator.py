from dataflow.generator.utils.Prompts import AnswerGeneratorPrompt
# from dataflow.generator.utils.LocalModelGenerator import LocalModelGenerator
from dataflow.generator.utils.APIGenerator_aisuite import APIGenerator_aisuite
from dataflow.generator.utils.APIGenerator_request import APIGenerator_request
import yaml
import logging
import pandas as pd
from dataflow.utils.registry import GENERATOR_REGISTRY
from dataflow.utils.utils import get_logger
from dataflow.data import MyScaleStorage, DatabaseConfig
import os

@GENERATOR_REGISTRY.register()
class AnswerGenerator:
    '''
    Answer Generator is a class that generates answers for given questions.
    '''
    def __init__(self, config: dict):
        self.config = config
        self.prompt = AnswerGeneratorPrompt()
        self.model_generator = self.__init_model__()
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
            self.input_file = self.config['input_file']
            self.output_file = self.config['output_file']
        # self.input_file = self.config.get("input_file")
        # self.output_file = self.config.get("output_file")
        self.input_key = self.config.get("input_key", "data")
        self.read_key = self.config.get("read_key", "prompt")
        self.output_text_key = self.config.get("output_key", "response")
        self.logger = get_logger()
        self.read_min_score: list = self.config.get('read_min_score', [])
        self.read_max_score: list = self.config.get('read_max_score', [])
        self.eval_stage = self.config.get('eval_stage', 4)
        # Ensure required paths and keys are provided
        if not hasattr(self,"storage") and (not self.input_file or not self.output_file):
            raise ValueError("Both input_file and output_file must be specified in the config.")

    def __init_model__(self):
        '''
        Initialize the model generator based on the configuration.
        '''
        generator_type = self.config.get("generator_type", "local").lower()
        if generator_type == "aisuite":
            return APIGenerator_aisuite(self.config)
        elif generator_type == "request":
            return APIGenerator_request(self.config)
        else:
            raise ValueError(f"Invalid generator type: {generator_type}")
    
    def _load_input(self):
        if hasattr(self, 'storage'):
            value_list = self.storage.read_code_json(
                [self.input_key], stage=self.eval_stage, syn='syn_q', format='SFT_Single', maxmin_scores=[dict(zip(['min_score', 'max_score'], list(_))) for _ in list(zip(self.read_min_score, self.read_max_score))]
            )
            return pd.DataFrame([
                {**item['data'], 'id': str(item['id'])}
                for item in value_list
            ])
        else:
            return pd.read_json(self.input_file, lines=True)

    def _write_output(self,save_path, dataframe, extractions):
        if hasattr(self, 'storage'):
            # output_rows = []
            # for i, row in dataframe.iterrows():
            #     output_rows.append({
            #         self.read_key: row[self.read_key],
            #         self.output_text_key: row[self.output_text_key]
            #     })
            output_rows = dataframe.where(pd.notnull(dataframe), None).to_dict(orient="records")
            self.storage.write_data(output_rows, format="SFT_Single", Synthetic="syn_qa")
        else:
            dataframe.to_json(save_path, orient="records", lines=True)

    def run(self):
        '''
        Runs the answer generation process, reading from the input file and saving results to output.
        '''
        # Read input file: only accept jsonl format
        # dataframe = pd.read_json(self.input_file, lines=True)
        dataframe = self._load_input()
        # print(dataframe)

        # Ensure the input and output keys are correctly set
        self._validate_dataframe(dataframe)

        # Extract the prompts and generate answers
        user_prompts = dataframe[self.read_key].tolist()
        answers = self.model_generator.generate_text_from_input(user_prompts)

        # Save the generated answers to the output file
        dataframe[self.output_text_key] = answers
        # dataframe.to_json(self.output_file, orient="records", lines=True)
        self._write_output(self.output_file, dataframe, None)

    def _validate_dataframe(self, dataframe: pd.DataFrame):
        '''
        Helper method to validate the input dataframe columns.
        '''
        # Check if the input prompt key exists in the dataframe
        if self.read_key not in dataframe.columns:
            raise ValueError(f"read_key: {self.read_key} not found in the dataframe.")
        
        # Check if the output text key already exists in the dataframe
        if self.output_text_key in dataframe.columns:
            raise ValueError(f"Found {self.output_text_key} in the dataframe, which would overwrite an existing column. Please use a different output_key.")
