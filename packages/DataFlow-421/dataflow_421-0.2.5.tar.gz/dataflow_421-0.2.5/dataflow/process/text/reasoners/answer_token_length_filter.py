from dataflow.core import ReasonerFilter
import numpy as np
from dataflow.utils.registry import PROCESSOR_REGISTRY
from transformers import AutoTokenizer
from dataflow.utils.utils import get_logger
from datasets import Dataset
from dataflow.data import TextDataset


@PROCESSOR_REGISTRY.register()
class AnswerTokenLengthFilter(ReasonerFilter):
    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.filter_name = 'AnswerTokenLengthFilter'
        self.max_answer_token_length = args_dict['max_answer_token_length']
        self.tokenizer = AutoTokenizer.from_pretrained(args_dict['tokenizer_dir'])
        self.logger = get_logger()
        self.read_min_score: list = args_dict['read_min_score']
        self.read_max_score: list = args_dict['read_max_score']
        self.eval_stage = args_dict['eval_stage']
        self.dataset = self._load_input()

    def _load_input(self):
        if self.storage is not None:
            value_list = self.storage.read_code_json(
                [self.input_key], stage=self.eval_stage, format='SFT_Single', syn='syn_qa', maxmin_scores=[dict(zip(['min_score', 'max_score'], list(_))) for _ in list(zip(self.read_min_score, self.read_max_score))]
            )
            value_list = [        
                {**item['data'], 'id': str(item['id'])}
                for item in value_list
            ]
            
            dataset = Dataset.from_list(value_list)
            return TextDataset(
                dataset=dataset,
                keys=value_list[0].keys(),
                metadata=None 
            )
        else:
            raise ValueError("No storage or input file provided")
        
    def _write_output(self, labels, ids):
        if self.storage is not None:
            output_rows = []
            for _, label in zip(ids, labels):
                output_rows.append({
                    self.result_key: label,
                    'id': _
                })
            self.storage.write_eval(output_rows, algo_name=self.filter_name, score_key=self.result_key)
        else:
            raise ValueError("No storage or output file provided")

    def filter_func(self, dataset):
        def get_token_count(input_string):
            tokens = self.tokenizer.encode(input_string, add_special_tokens=False)
            return len(tokens)

        return np.array([get_token_count(item[self.keys]) <= self.max_answer_token_length for item in dataset]).astype(int)