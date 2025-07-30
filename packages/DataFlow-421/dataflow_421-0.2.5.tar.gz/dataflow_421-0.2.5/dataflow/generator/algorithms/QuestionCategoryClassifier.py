import json
import os
import pandas as pd
from dataflow.generator.utils import APIGenerator_aisuite, APIGenerator_request
from dataflow.generator.utils.Prompts import QuestionCategoryPrompt
import re
from dataflow.utils.registry import GENERATOR_REGISTRY
import logging
from dataflow.utils.utils import get_logger
from dataflow.data import MyScaleStorage, DatabaseConfig

@GENERATOR_REGISTRY.register()
class QuestionCategoryClassifier():
    def __init__(self, args):
        """
        Initialize the QuestionCategoryClassifier with the provided configuration.
        """
        self.config = args
        self.prompts = QuestionCategoryPrompt()
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
            self.output_file= args.get("output_file")
        self.read_key = self.config.get("read_key", "question")
        self.input_key = self.config.get("input_key", "data")  # default key for question input
        self.output_key = self.config.get("output_key", "classification_result")  # default output key
        self.logger = get_logger()
        self.read_min_score = self.config.get('read_min_score', 0.9)
        self.read_max_score = self.config.get('read_max_score', 2.0)
        self.eval_stage = self.config.get('eval_stage', 2)
        


        # Ensure input_file and output_file are provided
        if not hasattr(self, "storage") and (not self.input_file or not self.output_file):
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
        for text in dataframe[self.read_key]:
            used_prompt = self.prompts.question_synthesis_prompt(text)
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
            output_1 = []
            for row in output_rows:
                primary = int(row.get("primary_category", 10))
                secondary = int(row.get("secondary_category",90))
                category = primary * 8 + secondary

                output_1.append({
                    "id": row.get("id"),
                    "category": category
                })
            self.storage.write_eval(output_1, algo_name="QuestionCategoryClassifier", score_key="category")
        else:
            output_dir = os.path.dirname(save_path)
            os.makedirs(output_dir, exist_ok=True)
            dataframe.to_json(self.output_file, orient="records", lines=True, force_ascii=False)

    def run(self):
        """
        Run the question category classification process.
        """
        # Read the input file
        # dataframe = pd.read_json(self.input_file, lines=True)
        dataframe = self._load_input()

        # Reformat the prompts for classification
        formatted_prompts = self._reformat_prompt(dataframe)

        # Generate responses using the model
        responses = self.model.generate_text_from_input(formatted_prompts)

        for (idx, row), classification_str in zip(dataframe.iterrows(), responses):
            try:
                if not classification_str:
                    raise ValueError("空字符串")

                # 去除 Markdown 代码块包裹
                cleaned_str = re.sub(r"^```json\s*|\s*```$", "", classification_str.strip(), flags=re.DOTALL)

                # 去除非 ASCII 字符（可选）
                cleaned_str = re.sub(r"[^\x00-\x7F]+", "", cleaned_str)

                classification = json.loads(cleaned_str)

                primary_raw = classification.get("primary_category", 10)
                secondary_raw = classification.get("secondary_category", 90)

                # 提取 primary 的整数部分
                primary_match = re.search(r"(\d+)", primary_raw)
                primary_category = primary_match.group(1) if primary_match else ""

                # 提取 secondary 小数点后的数字
                secondary_match = re.search(r"\d+\.(\d+)", secondary_raw)
                secondary_category = secondary_match.group(1) if secondary_match else ""

                dataframe.at[idx, "primary_category"] = primary_category
                dataframe.at[idx, "secondary_category"] = secondary_category

            except json.JSONDecodeError:
                self.logger.warning(f"[警告] JSON 解析失败，收到的原始数据: {repr(classification_str)}")
            except Exception as e:
                self.logger.error(f"[错误] 解析分类结果失败: {e}")
                self.logger.debug(f"[DEBUG] 原始字符串：{repr(classification_str)}")


        if self.output_key in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key} in the dataframe, which leads to overwriting the existing column, please check the output_text_key: {key_list}")
        

        # Save DataFrame to the output file
        # dataframe.to_json(self.output_file, orient="records", lines=True, force_ascii=False)
        self._write_output(self.output_file, dataframe, None)

        self.logger.info(f"Classification results saved to {self.output_file}")
        return
