import json
import uuid
import pandas as pd
from abc import ABC, abstractmethod
from typing import Any, Literal
from clickhouse_driver import Client
from dataflow.utils.utils import get_logger
from .storage import DataFlowStorage

class DataFlowFileStorage(DataFlowStorage):

    def __init__(self):
        pass

    def read_code_json(self, key_list: list, **kwargs) -> list:
        """Read code data from file with JSON format"""
        if not hasattr(self, 'input_file'):
            raise ValueError("input_file not set")
        data = pd.read_json(self.input_file, lines=True)
        if 'maxmin_scores' in kwargs:
            # Implement score filtering logic for file storage
            pass
        return data.to_dict('records')

    def write_data(self, data: list, **kwargs) -> None:
        """Write data to file"""
        if not hasattr(self, 'output_file'):
            raise ValueError("output_file not set")
        with open(self.output_file, 'w') as f:
            for item in data:
                json.dump(item, f)
                f.write('\n')

    def write_eval(self, data: list, **kwargs) -> None:
        """Write evaluation results to file"""
        if not hasattr(self, 'output_file'):
            raise ValueError("output_file not set")
        with open(self.output_file, 'w') as f:
            for item in data:
                json.dump(item, f)
                f.write('\n')

    def write_code_json(self, data: list, **kwargs) -> None:
        """Write code data to file with JSON format"""
        if not hasattr(self, 'output_file'):
            raise ValueError("output_file not set")
        with open(self.output_file, 'w') as f:
            for item in data:
                json.dump(item, f)
                f.write('\n')
