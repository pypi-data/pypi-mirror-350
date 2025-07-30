def prepare_huggingface_model(pretrained_model_name_or_path,
                              return_model=True,
                              trust_remote_code=False):
    """
    Prepare and load a HuggingFace model with the corresponding processor.

    :param pretrained_model_name_or_path: model name or path
    :param return_model: return model or not
    :param trust_remote_code: passed to transformers
    :return: a tuple (model, input processor) if `return_model` is True;
             otherwise, only the processor is returned.
    """
    import transformers
    from transformers import AutoConfig, AutoProcessor, AutoModel
    
    processor = AutoProcessor.from_pretrained(
        pretrained_model_name_or_path, trust_remote_code=trust_remote_code)

    if return_model:
        config = AutoConfig.from_pretrained(
            pretrained_model_name_or_path, trust_remote_code=trust_remote_code)

        model = AutoModel.from_config(config, trust_remote_code=trust_remote_code)

    return (model, processor) if return_model else processor

def wget_model(url, path):
    import os
    import subprocess
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        # Build the wget command
        command = ['wget', '-c', url, '-O', path]
        # Execute the command
        subprocess.run(command, check=True)
        
        print(f"File downloaded successfully and saved to: {path}")
        return path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the file: {e}")
        return None

def gdown_model(url, path):
    import os
    import gdown
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(path):
        gdown.download(url, path)


def _cuda_device_count():

    import torch
    return torch.cuda.device_count()


_CUDA_DEVICE_COUNT = _cuda_device_count()


def cuda_device_count():
    return _CUDA_DEVICE_COUNT


def is_cuda_available():
    return _CUDA_DEVICE_COUNT > 0

import torch
import gc
import time
from typing import Optional, Dict, Any
from vllm import LLM
import logging

logger = logging.getLogger(__name__)

class ModelInitializer:
    """
    大模型初始化工具类，处理 GPU 显存管理和模型加载
    """
    def __init__(self, max_retries: int = 3, retry_delay: int = 5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def clear_gpu_memory(self) -> None:
        """
        清理 GPU 显存
        """
        try:
            # 检查 GPU 显存
            memory_info = ModelInitializer.get_gpu_memory_info()
            print("清理前: memory_info: ", memory_info)

            # 清理 CUDA 清理前缓存
            torch.cuda.empty_cache()

            # 清理 Python 垃圾回收
            gc.collect()

            # 如果有多个 GPU，清理所有 GPU
            if torch.cuda.is_available():
                for i in range(torch.cuda.device_count()):
                    with torch.cuda.device(i):
                        torch.cuda.empty_cache()
                        torch.cuda.ipc_collect()

            # 检查 GPU 清理后显存
            memory_info = ModelInitializer.get_gpu_memory_info()
            print("清理后: memory_info: ", memory_info)

            logger.info("GPU memory cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing GPU memory: {e}")
            raise

    def initialize_llm(
        self,
        model_path: str,
        device: str = "cuda",
        max_model_len: int = 2048,
        gpu_memory_utilization: float = 0.9,
        tensor_parallel_size: int = 1,
        quantization: Optional[str] = None,
        **kwargs
    ) -> LLM:
        """
        初始化 LLM 模型

        Args:
            model_path: 模型路径
            device: 设备类型
            max_model_len: 最大序列长度
            gpu_memory_utilization: GPU 显存使用率
            tensor_parallel_size: 并行 GPU 数量
            quantization: 量化类型
            **kwargs: 其他参数

        Returns:
            LLM: 初始化后的模型实例
        """
        for attempt in range(self.max_retries):
            try:
                # 清理 GPU 显存
                self.clear_gpu_memory()
                logger.info(f"Attempt {attempt + 1}: Initializing model from {model_path}")

                # 初始化模型
                llm = LLM(
                    model=model_path,
                    device=device,
                    max_model_len=max_model_len,
                    gpu_memory_utilization=gpu_memory_utilization,
                    tensor_parallel_size=tensor_parallel_size,
                    quantization=quantization,
                    **kwargs
                )

                logger.info("Model initialized successfully!")
                return llm

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Waiting {self.retry_delay} seconds before retry...")
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed to initialize model after {self.max_retries} attempts")

    @staticmethod
    def get_gpu_memory_info() -> Dict[str, Any]:
        """
        获取 GPU 显存信息

        Returns:
            Dict[str, Any]: GPU 显存信息
        """
        if not torch.cuda.is_available():
            return {"available": False}

        memory_info = {}
        for i in range(torch.cuda.device_count()):
            with torch.cuda.device(i):
                memory_info[f"gpu_{i}"] = {
                    "allocated": torch.cuda.memory_allocated() / 1024**2,  # MB
                    "cached": torch.cuda.memory_reserved() / 1024**2,  # MB
                    "total": torch.cuda.get_device_properties(i).total_memory / 1024**2  # MB
                }
        return memory_info
