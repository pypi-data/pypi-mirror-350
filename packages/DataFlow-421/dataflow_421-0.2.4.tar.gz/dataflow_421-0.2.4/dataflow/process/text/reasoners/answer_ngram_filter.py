from dataflow.core import ReasonerFilter
import numpy as np
import re
from dataflow.utils.registry import PROCESSOR_REGISTRY
from dataflow.Eval.Text import NgramScorer
from dataflow.utils.utils import get_logger
from datasets import Dataset
from dataflow.data import TextDataset


@PROCESSOR_REGISTRY.register()
class AnswerNgramFilter(ReasonerFilter):
    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.filter_name = 'AnswerNgramFilter'
        self.min_score = args_dict['min_score']
        self.max_score = args_dict['max_score']
        self.ngrams = args_dict['ngrams']
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
        scores = []
        for sample in dataset:
            answer = sample[self.question_key]
            try:
                answer += sample[self.answer_key]
            except:
                pass
            content = answer.lower()
            content = re.sub(r'[^\w\s]', '', content)
            words = content.split()
            ngrams = [' '.join(words[i:i + self.ngrams]) for i in range(len(words) - (self.ngrams - 1))]
            unique_ngrams = set(ngrams)

            total_ngrams = len(ngrams)
            unique_ngrams_count = len(unique_ngrams)

            repetition_score = unique_ngrams_count / total_ngrams if total_ngrams > 0 else 0.0
            scores.append(repetition_score) 

        return np.array([self.min_score <= score <= self.max_score for score in scores]).astype(int)