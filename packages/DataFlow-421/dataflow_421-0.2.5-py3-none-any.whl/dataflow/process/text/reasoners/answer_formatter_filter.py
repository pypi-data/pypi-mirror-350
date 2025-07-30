from dataflow.core import TextFilter, ReasonerFilter
import numpy as np
from dataflow.utils.registry import PROCESSOR_REGISTRY
import re
from datasets import Dataset
from dataflow.data import TextDataset
from dataflow.utils.utils import get_logger

@PROCESSOR_REGISTRY.register()
class AnswerFormatterFilter(ReasonerFilter):
    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.filter_name = 'AnswerFormatterFilter'
        self.logger = get_logger()
        self.eval_stage = args_dict.get('eval_stage', 4)
        self.dataset = self._load_input()
        
    def is_valid_answer(answer: str) -> bool:
        # check final answer in \boxed{} or not 
        if not re.search(r'\\boxed{.*}', answer):
            return False
        
        return True 
    
    def _load_input(self):
        if self.storage is not None:
            value_list = self.storage.read_code_json(
                [self.input_key], stage=self.eval_stage, format='SFT_Single', syn='syn_qa'
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
        indexes =  np.zeros(len(dataset)).astype(int)

        for i, item in enumerate(dataset):
            answer = item[self.keys]
            if AnswerFormatterFilter.is_valid_answer(answer):
                indexes[i] = 1

        return indexes