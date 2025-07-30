import torch
import json
import requests
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from dataflow.core import TextScorer
from dataflow.utils.registry import MODEL_REGISTRY
from dataflow.utils.utils import get_logger

# Instag instruction complexity evaluation
# cited from: #INSTAG: INSTRUCTION TAGGING FOR ANALYZING SUPERVISED FINE-TUNING OF LARGE LANGUAGE MODELS
@MODEL_REGISTRY.register()
class InstagScorer(TextScorer):
    def __init__(self, args_dict):
        super().__init__(args_dict)
        self.model_path = args_dict.get('model_path')
        self.max_new_tokens = args_dict.get('max_new_tokens', 1024)  # 降低默认值至100
        self.model_cache_dir = args_dict.get('model_cache_dir')  
        self.temperature = args_dict.get('temperature', 1.0)
        self.do_sample = args_dict.get('do_sample', False)
        self.num_return_sequences = args_dict.get('num_return_sequences', 1)
        self.return_dict_in_generate = args_dict.get('return_dict_in_generate', True)
        self.device = args_dict.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.use_API = args_dict.get('use_API', False)  # 默认使用本地
        self.API_url = args_dict.get('API_url', 'http://0.0.0.0:8003')  # 更新默认端口为8003
        self.API_model_name = args_dict.get('API_model_name')  # 使用vLLM时需要指定
        self.batch_size = 1
        self.score_type = float  
        self.data_type = 'text' 
        self.score_name = 'InstagScore'
        self.logger = get_logger()
        
        if self.use_API:
            self.logger.info(f"Using API mode with URL: {self.API_url}, model: {self.API_model_name}")
            self.logger.info(f"最大令牌输出数: {self.max_new_tokens}")
        else:
            self.logger.info(f"Using local model: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, cache_dir=self.model_cache_dir)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path, cache_dir=self.model_cache_dir).to(self.device)
            self.model.requires_grad_(False)
            self.model.eval()

    def make_prompt(self, query):
        prompt = f"Please identify tags of user intentions in the following user query and provide an explanation for each tag. Please respond in the JSON format {{\"tag\": str, \"explanation\": str}}.\nUser query: {query}"
        messages = [("user", prompt), ("Assistant", None)]
        seps = [" ", "</s>"]
        ret = "system: A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions." + seps[0]
        for i, (role, message) in enumerate(messages):
            if message:
                ret += role + ": " + message + seps[i % 2]
            else:
                ret += role + ":"
        return ret

    def format_api_messages(self, query):
        """格式化用于API调用的消息"""
        system_prompt = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions."
        user_content = (
            f"Please identify tags of user intentions in the following user query and provide an explanation for each tag. "
            f"Please respond in the JSON format {{'tag': str, 'explanation': str}}.\n"
            f"User query: {query}"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        return messages

    def inference_batch(self, queries):
        if self.use_API:
            # API模式
            json_outputs = []
            for query in queries:
                messages = self.format_api_messages(query)
                
                payload = {
                    "model": self.API_model_name,
                    "messages": messages,
                    "max_tokens": self.max_new_tokens,  # 固定较小的max_tokens值，避免超出上下文限制
                    "temperature": self.temperature
                    # vLLM API不支持do_sample参数，当temperature=0时等同于do_sample=False
                }
                
                try:
                    self.logger.info(f"调用API: {self.API_url}/v1/chat/completions, query: {query[:30]}...")
                    response = requests.post(f"{self.API_url}/v1/chat/completions", json=payload, timeout=60)
                    response.raise_for_status()
                    result = response.json()
                    
                    self.logger.info(f"API返回结果: {str(result)[:200]}...")
                    
                    if result["choices"] and result["choices"][0].get("message"):
                        generated_text = result["choices"][0]["message"].get("content", "")
                        self.logger.info(f"生成的文本: {generated_text[:100]}...")
                        
                        string_output = generated_text.strip()
                        # 处理可能包含的markdown代码块
                        if string_output.startswith("```json"):
                            string_output = string_output.split("```json", 1)[1].strip()
                            if string_output.endswith("```"):
                                string_output = string_output[:-3].strip()
                        elif string_output.startswith("```"):
                            string_output = string_output.split("```", 1)[1].strip()
                            if string_output.endswith("```"):
                                string_output = string_output[:-3].strip()
                        
                        try:
                            json_output = json.loads(string_output)
                            self.logger.info(f"解析的JSON: {json_output}")
                        except json.JSONDecodeError:
                            self.logger.warning(f"JSON解析错误，原始文本: {string_output}")
                            # 尝试提取可能格式不规范的JSON
                            if "{" in string_output and "}" in string_output:
                                try:
                                    json_text = string_output[string_output.find("{"):string_output.rfind("}")+1]
                                    json_output = json.loads(json_text)
                                    self.logger.info(f"二次尝试解析JSON成功: {json_output}")
                                except:
                                    json_output = {"tag": "解析错误", "explanation": string_output[:100]}
                            else:
                                json_output = {"tag": "解析错误", "explanation": string_output[:100]}
                        
                        json_outputs.append(json_output)
                    else:
                        self.logger.warning(f"API响应格式错误: {result}")
                        json_outputs.append({"tag": "API响应格式错误", "explanation": str(result)[:100]})
                
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"调用API错误: {e}")
                    if 'response' in locals():
                        self.logger.error(f"响应内容: {response.text if hasattr(response, 'text') else 'No response text'}")
                    json_outputs.append({"tag": "API调用错误", "explanation": str(e)})
            
            return json_outputs
        else:
            # 本地推理模式
            input_strs = [self.make_prompt(query) for query in queries]
            input_tokens = self.tokenizer(input_strs, return_tensors="pt", padding=True)
            
            if torch.cuda.is_available():
                input_tokens = {key: value.to(self.device) for key, value in input_tokens.items()}

            output = self.model.generate(
                input_tokens['input_ids'],
                temperature=self.temperature,
                do_sample=self.do_sample,
                max_new_tokens=self.max_new_tokens,
                num_return_sequences=self.num_return_sequences,
                return_dict_in_generate=self.return_dict_in_generate,
            )
            
            num_input_tokens = input_tokens["input_ids"].shape[1]
            output_tokens = output.sequences
            generated_tokens = output_tokens[:, num_input_tokens:]
            generated_texts = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            
            json_outputs = []
            for generated_text in generated_texts:
                string_output = generated_text.strip()
                try:
                    json_output = json.loads(string_output)
                except json.JSONDecodeError:
                    self.logger.warning(f"JSON解析错误: {string_output}")
                    # 尝试提取可能格式不规范的JSON
                    if "{" in string_output and "}" in string_output:
                        try:
                            json_text = string_output[string_output.find("{"):string_output.rfind("}")+1]
                            json_output = json.loads(json_text)
                        except:
                            json_output = {"tag": "解析错误", "explanation": string_output[:100]}
                    else:
                        json_output = {"tag": "解析错误", "explanation": string_output[:100]}
                json_outputs.append(json_output)
            
            return json_outputs

    def evaluate_batch(self, batch):
        queries = batch.get('instruction', ['']) 
        json_outputs = self.inference_batch(queries)
        
        scores = []
        for json_output in json_outputs:
            if isinstance(json_output, list):
                complexity_score = len(json_output)
                self.logger.info(f"列表类型JSON，标签数量: {complexity_score}")
            elif isinstance(json_output, dict) and "tag" in json_output:  # 单个标签返回为字典
                complexity_score = 1
                self.logger.info(f"字典类型JSON，包含tag字段，评分为1")
            elif isinstance(json_output, dict) and len(json_output) > 0:  # 其他字典类型，有内容
                complexity_score = 1
                self.logger.info(f"其他字典类型JSON，评分为1: {json_output}")
            else:
                complexity_score = 0
                self.logger.warning(f"未识别的JSON类型或空数据，评分为0: {json_output}")
            
            scores.append(int(complexity_score))
        
        return scores
