import json
import uuid
import pandas as pd
from abc import ABC, abstractmethod
from typing import Any, Literal
from clickhouse_driver import Client
from dataflow.utils.utils import get_logger

class DataFlowStorage(ABC):

    @abstractmethod
    def read_code_json(self, key_list: list, **kwargs) -> list:
        """Read code data from storage with JSON format

        Args:
            key_list: List of keys to read
            **kwargs: Additional parameters including:
                - stage: Current stage
                - format: Data format
                - syn: Synthetic flag
                - maxmin_scores: Optional list of score ranges
        """
        pass

    @abstractmethod
    def write_data(self, data: list, **kwargs) -> None:
        """Write data to storage

        Args:
            data: List of data items to write
            **kwargs: Additional parameters to update
        """
        pass

    @abstractmethod
    def write_eval(self, data: list, **kwargs) -> None:
        """Write evaluation results to storage

        Args:
            data: List of evaluation results
            **kwargs: Must include:
                - algo_name: Algorithm name
                - score_key: Score field name
                - info_key: Optional info field name
        """
        pass

    @abstractmethod
    def write_code_json(self, data: list, **kwargs) -> None:
        """Write code data to storage with JSON format

        Args:
            data: List of code data items
            **kwargs: Must include:
                - format: Data format
                - syn: Synthetic flag
        """
        pass
