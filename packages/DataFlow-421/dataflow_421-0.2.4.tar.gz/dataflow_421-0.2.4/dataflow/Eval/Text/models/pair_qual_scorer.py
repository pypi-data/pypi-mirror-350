from dataflow.core import TextScorer
from dataflow.utils.registry import MODEL_REGISTRY
import torch
from torch import nn
import transformers
import requests
import numpy as np
from dataflow.utils.utils import get_logger
import json # Added for logging payload

class BertForRegression(nn.Module):
    def __init__(self, model_name):
        super().__init__()
        self.bert = transformers.BertModel.from_pretrained(model_name)
        self.regression = nn.Sequential(
            nn.Linear(self.bert.pooler.dense.out_features, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 1)
        )

    def forward(self, inputs):
        encoded = self.bert(**inputs)
        score = self.regression(encoded['pooler_output'])
        return encoded, score

@MODEL_REGISTRY.register()
class PairQualScorer(TextScorer):
    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.device = args_dict.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = args_dict.get('model_name', 'BAAI/bge-base-en-v1.5')
        self.model_state_dict = args_dict.get('model_state_dict', None)
        self.model_cache_dir = args_dict.get('model_cache_dir')
        self.use_API = args_dict.get('use_API', False)  # 默认使用本地
        self.API_url = args_dict.get('API_url', 'http://localhost:8000')
        self.API_model_name = args_dict.get('API_model_name')
        self.max_length = args_dict.get('max_length', 512) # Token limit
        self.score_type = float
        self.data_type = 'text'
        self.score_name = 'PairQualScorer'
        self.batch_size = 1
        self.logger = get_logger()

        # 始终初始化tokenizer，以便在API模式下也能用于精确截断
        self.logger.info(f"Initializing tokenizer with model_name: {self.model_name}")
        try:
            self.tokenizer = transformers.BertTokenizerFast.from_pretrained(
                self.model_name, 
                cache_dir=self.model_cache_dir
            )
            self.logger.info(f"Tokenizer initialized successfully for {self.model_name}.")
        except Exception as e:
            self.logger.error(f"Failed to initialize tokenizer for {self.model_name}: {e}")
            # 如果tokenizer初始化失败，后续依赖它的操作会出问题，这里可以选择抛出异常或设置tokenizer为None
            # raise e # 或者 self.tokenizer = None，并在使用前检查

        if self.use_API:
            self.logger.info(f"Using API mode with URL: {self.API_url}, model: {self.API_model_name}")
            if not self.API_model_name:
                self.logger.error("API_model_name is not configured for API mode. This will cause errors.")
            # 在API模式下，如果需要tokenizer进行精确截断，确保它已初始化
            if not hasattr(self, 'tokenizer') or self.tokenizer is None:
                 self.logger.error("Tokenizer is not available for API mode truncation. Please check initialization.")
        else:
            self.logger.info(f"Using local model: {self.model_name}")
            self.model = BertForRegression(self.model_name)
            # Tokenizer初始化已移到前面
            if self.model_state_dict:
                self.model.load_state_dict(torch.load(self.model_state_dict, map_location='cpu'))
            self.model.to(self.device).eval()

    def get_embeddings_api(self, texts): # texts is expected to be a list of strings
        """
        使用vLLM API获取文本嵌入
        """
        try:
            if not isinstance(texts, list) or not all(isinstance(text, str) for text in texts):
                self.logger.error(f"Invalid 'texts' argument for get_embeddings_api. Expected list of strings, got: {type(texts)} with content: {str(texts)[:200]}")
                return None
            
            payload = {
                "model": self.API_model_name,
                "input": texts,
            }
            # Log the exact payload being sent
            try:
                payload_str = json.dumps(payload)
            except TypeError as te: # Handle potential non-serializable content in texts for logging
                self.logger.error(f"Could not serialize payload for logging due to: {te}. Input texts (first 200 chars each): {[str(t)[:200] for t in texts]}")
                payload_str = f'{{"model": "{self.API_model_name}", "input": "Error serializing input for log"}}'

            self.logger.info(f"Sending API request to {self.API_url}/v1/embeddings with payload: {payload_str[:500]}...") # Log first 500 chars of payload
            
            response = requests.post(f"{self.API_url}/v1/embeddings", json=payload, timeout=60) 
            
            self.logger.info(f"API response status code: {response.status_code} for input (first 200 chars of first text): {str(texts[0])[:200] if texts else 'N/A'}")
            if response.status_code != 200:
                self.logger.error(f"API error response content: {response.text[:1000]}") # Log first 1000 chars of error
            response.raise_for_status() # Will raise HTTPError for 4xx/5xx status
            
            result = response.json()
            
            embeddings = [data["embedding"] for data in result["data"]]
            return np.array(embeddings)
        except requests.exceptions.HTTPError as http_err:
            # response.text is already logged if status_code != 200 by the block above.
            # If raise_for_status() was triggered, response.text contains the error.
            self.logger.error(f"HTTP error occurred: {http_err}") 
            return None
        except Exception as e:
            self.logger.error(f"API request failed with generic exception: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                self.logger.error(f"Response content at time of generic exception: {response.text[:1000]}")
            return None
            
    def inference(self, input_text):
        """
        根据use_API标志决定使用API或本地模型进行推理
        
        Args:
            input_text: 输入文本
            
        Returns:
            推理得分
        """
        if self.use_API:
            if not isinstance(input_text, str): # Ensure input_text is a string
                self.logger.warning(f"inference called with non-string input_text (type: {type(input_text)}). Value (first 200 chars): {str(input_text)[:200]}. Skipping embedding.")
                return 0.0

            input_text_to_embed = input_text
            if hasattr(self, 'tokenizer') and self.tokenizer:
                # 使用tokenizer进行精确截断
                self.logger.info(f"Original text length for API: {len(input_text)} chars.")
                tokenized_output = self.tokenizer(
                    input_text,
                    truncation=True,
                    max_length=self.max_length, # self.max_length is the token limit (e.g., 512)
                    return_attention_mask=False,
                    return_token_type_ids=False,
                )
                input_text_to_embed = self.tokenizer.decode(tokenized_output['input_ids'], skip_special_tokens=True)
                if len(input_text_to_embed) < len(input_text):
                    self.logger.warning(f"Input text truncated by tokenizer for API. Original char len: {len(input_text)}, Truncated char len: {len(input_text_to_embed)}. Truncated text (first 200 chars): '{input_text_to_embed[:200]}...'")
            else:
                # Fallback to character-based truncation if tokenizer is not available (should not happen with new __init__)
                self.logger.warning("Tokenizer not available for API mode, falling back to character-based truncation.")
                char_limit = self.max_length * 3 
                if len(input_text) > char_limit:
                    self.logger.warning(f"Input text length ({len(input_text)} chars) exceeds estimated char limit ({char_limit}) for API. Truncating to {char_limit} chars.")
                    input_text_to_embed = input_text[:char_limit]
            
            self.logger.info(f"Attempting to get embedding for input_text (type: {type(input_text_to_embed)}, len: {len(input_text_to_embed)} chars): '{str(input_text_to_embed)[:200]}...'")
            
            embeddings = self.get_embeddings_api([input_text_to_embed]) # Pass it as a list of one string
            
            if embeddings is None or embeddings.size == 0: # Check if embeddings are valid
                self.logger.warning(f"Failed to get embeddings or got empty embeddings for input_text: '{str(input_text_to_embed)[:200]}...'")
                return 0.0
            
            # 加载回归模型并应用
            if not hasattr(self, 'regression_model'):
                # 只初始化回归层
                embedding_dim = embeddings.shape[1]  # 嵌入维度
                self.regression_model = nn.Sequential(
                    nn.Linear(embedding_dim, 512),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(512, 1)
                ).to(self.device)
                
                # 如果有训练好的权重，可以在这里加载
                if self.model_state_dict:
                    # 注意：这里可能需要调整，因为state_dict包含了BERT和回归层的权重
                    # 只加载回归层的权重
                    state_dict = torch.load(self.model_state_dict, map_location='cpu')
                    # 提取回归层权重
                    regression_state_dict = {k.replace('regression.', ''): v for k, v in state_dict.items() 
                                       if k.startswith('regression.')}
                    # 加载回归层权重
                    try:
                        self.regression_model.load_state_dict(regression_state_dict)
                    except Exception as e:
                        self.logger.warning(f"Could not load regression weights: {e}")
            
            # 转换嵌入向量为tensor并预测分数
            embedding_tensor = torch.tensor(embeddings, dtype=torch.float32).to(self.device)
            with torch.no_grad():
                score = self.regression_model(embedding_tensor)
            return score.item()
        else:
            # 使用本地模型进行推理
            inputs = self.tokenizer(input_text, return_tensors='pt', padding=True, truncation=True, max_length=self.max_length)
            inputs.to(self.device)
            with torch.no_grad():
                _, score = self.model(inputs)
            return score.item()

    def evaluate_batch(self, batch):
        """处理批量数据并返回评分结果"""
        raw_content_value = batch.get('raw_content')

        score = None
        if not raw_content_value:
            self.logger.warning(f"evaluate_batch received empty or None input for key 'raw_content'. Batch content (first 200 chars): {str(batch)[:200]}")
        elif isinstance(raw_content_value, list):
            if not raw_content_value: # Empty list
                self.logger.warning(f"evaluate_batch received an empty list for key 'raw_content'. Batch content: {str(batch)[:200]}")
            elif not isinstance(raw_content_value[0], str):
                self.logger.warning(f"evaluate_batch: First element of list 'raw_content' is not a string (type: {type(raw_content_value[0])}). Value (first 200 chars): {str(raw_content_value[0])[:200]}.")
            else:
                input_to_score = raw_content_value[0] # Take the first string from the list
                self.logger.info(f"evaluate_batch processing first element from list 'raw_content': {input_to_score[:100]}...")
                score = self.inference(input_to_score)
        elif isinstance(raw_content_value, str):
            self.logger.info(f"evaluate_batch processing string 'raw_content': {raw_content_value[:100]}...")
            score = self.inference(raw_content_value)
        else:
             self.logger.warning(f"evaluate_batch received unexpected type for key 'raw_content' (type: {type(raw_content_value)}). Value (first 200 chars): {str(raw_content_value)[:200]}.")
        
        return [score]