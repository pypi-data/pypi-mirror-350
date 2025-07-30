from dataflow.core import TextScorer
from dataflow.utils.registry import MODEL_REGISTRY
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from scipy.special import softmax
import requests
import torch
from dataflow.utils.utils import get_logger

@MODEL_REGISTRY.register()
class DeitaQualityScorer(TextScorer):
    def __init__(self, args_dict):
        super().__init__(args_dict)
        self.device = args_dict.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = args_dict.get('model_name')
        self.model_cache_dir = args_dict.get('model_cache_dir') 
        self.use_API = args_dict.get('use_API', False)  # 默认使用本地
        self.api_url = args_dict.get('API_url', 'http://localhost:8000')
        self.api_model_name = args_dict.get('API_model_name')  # 使用vLLM时需要指定
        self.max_length = args_dict.get('max_length', 10)
        self.batch_size = 1
        self.score_type = float
        self.data_type = 'text'
        self.score_name = 'DeitaQualityScore'
        self.logger = get_logger()
        if self.use_API:
            self.logger.info(f"Using API mode with model: {self.api_model_name}")
        else:
            self.logger.info(f"Using local model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.model_cache_dir)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, cache_dir=self.model_cache_dir).to(self.device)

        # token_str
        self.token_strs = ["1", "2", "3", "4", "5", "6"]
        self.score_template = np.array([1, 2, 3, 4, 5, 6])

    def infer_quality(self, input_text, resp_text):
        quality_template = ("You are a helpful assistant. Please identify the quality score of the Response corresponding to the Question.\n"
                            "#Question#:\n{instruction}\n#Response#:\n{output}\n##Quality: ")
        user_input = quality_template.format(instruction=input_text, output=resp_text)

        if self.use_API:
            # API模式
            payload = {
                "model": self.api_model_name,
                "messages": [
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": self.max_length,
                "temperature": 0,
                "logprobs": True,
                "top_logprobs": 6
            }

            response = requests.post(f"{self.api_url}/v1/chat/completions", json=payload)
            response.raise_for_status()
            result = response.json()

            logprobs_list = result["choices"][0]["logprobs"]["content"][0]["top_logprobs"]

            score_logits = []
            for token_str in self.token_strs:
                logprob = next((entry["logprob"] for entry in logprobs_list if entry["token"].strip() == token_str), -100)
                score_logits.append(logprob)

            score_logits = np.array(score_logits)
            score_npy = softmax(score_logits, axis=0)
            score_npy = score_npy * self.score_template
            final_score = np.sum(score_npy, axis=0)
            return final_score

        else:
            # 本地推理模式
            input_ids = self.tokenizer.encode(user_input, return_tensors="pt").to(self.device)
            outputs = self.model.generate(input_ids, max_new_tokens=self.max_length, num_return_sequences=1, return_dict_in_generate=True, output_scores=True)
            logprobs_list = outputs.scores[0][0]

            id2score = {
                29896: "1",
                29906: "2",
                29941: "3",
                29946: "4",
                29945: "5",
                29953: "6"
            }

            score_logits = []
            for k in id2score:
                score_logits.append(logprobs_list[k].cpu().numpy())

            score_logits = np.array(score_logits)
            score_npy = softmax(score_logits, axis=0)
            score_npy = score_npy * self.score_template
            final_score = np.sum(score_npy, axis=0)
            return final_score

    def evaluate_batch(self, batch):
        input_texts = batch.get('instruction', '')
        output_texts = batch.get('output', '')

        if not input_texts or not output_texts:
            quality_score = None
        else:
            quality_score = self.infer_quality(input_texts, output_texts)

        return [quality_score]
