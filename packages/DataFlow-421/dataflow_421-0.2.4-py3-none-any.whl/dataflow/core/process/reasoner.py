from dataflow.data import DataFlowDataset
from dataflow.core import ScoreRecord
from dataflow.format import TextFormatter
from dataflow.utils.utils import get_logger
from datasets import Dataset
from dataflow.data import MyScaleStorage, DatabaseConfig
import os

class Reasoner():
    def __init__(self, args=None):
        pass
        
    def reason_func(self, dataset):
        pass
    
    def __call__(self, dataset: DataFlowDataset):
        pass

class ReasonerFilter(Reasoner):
    def __init__(self, args=None):
        super().__init__()
        self.data_type = "text"
        self.filter_name = "ReasonerFilter"
        self.args = args
        self.input_key = args.get("input_key","data")
        
        self.input_question_key = args.get("input_question_key","")
        self.max_worker = args.get("max_worker",1)
        
        # answer format filter
        self.keys = args.get("input_keys","")
        # self.output_question_key = args.get("output_question_key","")
        
        # answer gt verification
        self.test_answer_key = args.get("test_answer_key","")
        self.gt_answer_key = args.get("gt_answer_key","")

        
        # ngram filter
        self.question_key = args.get("question_key","")
        self.answer_key = args.get("answer_key","")
        
        self.result_key = args.get("result_key","")
        # api args
        api_args = args.get('api_args', None)
        if api_args is not None:
            self.model_name = api_args['model_name']
            self.api_url = api_args['api_url']
            self.mode_test = api_args['mode_test']
            
        # if "input_file" in args.keys():
        #     self.formatter = TextFormatter(args)
        #     self.dataset = self.formatter.load_dataset()
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
            # self.dataset = self._load_input()
        elif "input_file" in args.keys():
            self.formatter = TextFormatter(args)
            self.dataset = self.formatter.load_dataset()

    def _load_input(self):
        pass

    # def _load_input(self):
    #     if self.storage is not None:
    #         value_list = self.storage.read_code_json(
    #             [self.input_key], stage=0, format='SFT_Single', syn='syn_q'
    #         )
    #         value_list = [        
    #             {**item['data'], 'id': str(item['id'])}
    #             for item in value_list
    #         ]
            
    #         dataset = Dataset.from_list(value_list)
    #         return dataset
    #     else:
    #         raise ValueError("No storage or input file provided")

    def _write_output(self, label, ids):
        pass

    # def _write_output(self, labels):
    #     if self.storage is not None:
    #         output_rows = []
    #         for i, label in enumerate(labels):
    #             output_rows.append({
    #                 self.result_key: label,
    #             })
    #         output_1 = []
    #         for row in output_rows:
    #             primary = int(row.get("primary_category", "10"))
    #             secondary = int(row.get("secondary_category","90"))
    #             category = primary * 8 + secondary

    #             output_1.append({
    #                 "id": row.get("id"),
    #                 self.result_key: label,
    #             })
    #         self.storage.write_eval(output_rows, algo_name=self.filter_name, score_key="category")
    #     else:
    #         raise ValueError("No storage or output file provided")
    
    def filter_func(self, dataset):
        pass

    def __call__(self, dataset: DataFlowDataset):
        """Processes the dataset using the reasoner"""
        
        init_len = len(dataset)        
        score_record = ScoreRecord()
        dataset.set_score_record(score_record)
        
        labels = self.filter_func(dataset)
        if isinstance(dataset.dataset, Dataset):
            def filter_by_labels(example, index):
                try:
                    return labels[index] == 1
                except:
                    logger = get_logger()
                    logger.info("This index is out of range, so it will be skipped. index: %d", index)
            dataset.dataset = dataset.dataset.filter(filter_by_labels, with_indices=True)
            filtered_dataset = dataset
        else:
            filtered_dataset = dataset.filter(labels)

        print(f'Implemented {self.filter_name}. Data Number: {init_len} -> {len(filtered_dataset)}', flush=True)
        return labels, filtered_dataset
    
    def run(self):
        ids = self.dataset['id']
        labels, filtered_dataset = self.__call__(self.dataset)
        if self.storage is not None:
            self._write_output(labels, ids)
        elif "output_file" in self.args.keys():
            filtered_dataset.dump(save_path=self.args['output_file'])
        else:
            raise ValueError("No storage or output file provided")