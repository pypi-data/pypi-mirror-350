from prefect import task
from prefect_ray import RayTaskRunner
from dataflow.utils.registry import MODEL_REGISTRY, PROCESSOR_REGISTRY, FORMATTER_REGISTRY, GENERATOR_REGISTRY
import importlib
from typing import Dict, Any, Optional, List, Union
import time
from datetime import timedelta, datetime  

class RegistryAdapter:
    """
    用于将DataFlow算子转换为Prefect任务
    """
    def __init__(self, ensure_modules_loaded=True):
        if ensure_modules_loaded:
            self._ensure_modules_loaded()
    
    def _ensure_modules_loaded(self):
        try:
            # 加载Processor模块
            importlib.import_module("dataflow.process.text.filters")
            importlib.import_module("dataflow.process.text.refiners")
            importlib.import_module("dataflow.process.text.reasoners")
            
            # 加载Eval模块
            importlib.import_module("dataflow.Eval.Text")
            importlib.import_module("dataflow.Eval.image")
            
            # 加载Formattter器模块
            importlib.import_module("dataflow.format")
            
            # 加载Generator模块
            importlib.import_module("dataflow.generator.algorithms")
            importlib.import_module("dataflow.generator.utils")
                        
        except ImportError as e:
            print(f"模块加载失败: {e}")
    
    def create_processor_task(self, processor_name: str, args_dict: Dict[str, Any] = None):
        if args_dict is None:
            args_dict = {}
            
        @task(
            name=f"dataflow_processor_{processor_name}",
            retries=3,
            retry_delay_seconds=60,
            tags=["processor", processor_name],
            task_run_name=f"{processor_name}", 
            cache_key_fn=lambda context, *args, **kwargs: f"{processor_name}_{args}_{kwargs}",
            cache_expiration=timedelta(hours=1)
        )
        def processor_task(dataset=None):
            from prefect import get_run_logger
            logger = get_run_logger()
            
            print(f"开始执行 Processor: {processor_name}")
            logger.info(f"开始执行 Processor: {processor_name}")
            start_time = time.time()
            
            try:
                processor_cls = PROCESSOR_REGISTRY.get(processor_name)
                if processor_cls is None:
                    raise ValueError(f"Processor not found: {processor_name}")
                    
                processor = processor_cls(args_dict)
                # 统一使用 run 方法
                print(f"ready to run procssor(dataset): {dataset}")
                logger.info(f"ready to run procssor(dataset): {dataset}")
                result = processor.run()
                
                execution_time = time.time() - start_time
                logger.info(f"Processor {processor_name} 执行完成，耗时: {execution_time:.2f}秒")
                print(f"Processor {processor_name} 执行完成，耗时: {execution_time:.2f}秒")
                return result
                
            except Exception as e:
                print(f"Processor {processor_name} 执行失败: {str(e)}")
                raise
            
        return processor_task

    # 添加用于获取任务状态的辅助方法
    def get_task_runs(self, task_name: str = None, tags: List[str] = None):
        """获取任务运行记录"""
        from prefect.client import get_client
        
        async def get_runs():
            async with get_client() as client:
                return await client.read_task_runs(
                    task_name=task_name,
                    tags=tags,
                )
        
        return get_runs()

    def exec_processor(self, processor_name: str, dataset, args_dict: Dict[str, Any] = None):
        """直接执行处理器"""
        task = self.create_processor_task(processor_name, args_dict)
        try:
            return processor.run() 
        except Exception as e:
            print(f"Processor {processor_name} 执行失败: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise

    
    def create_model_task(self, model_name: str, args_dict: Dict[str, Any] = None):
        """创建模型任务但不执行"""
        if args_dict is None:
            args_dict = {}
            
        @task(
            name=f"dataflow_model_{model_name}",
            retries=3,
            retry_delay_seconds=60,
            tags=["model", model_name],
            task_run_name=f"{model_name}", 
            cache_key_fn=lambda context, *args, **kwargs: f"{model_name}_{args}_{kwargs}",
            cache_expiration=timedelta(hours=1)
        )
        def model_task(dataset=None):
            from prefect import get_run_logger
            logger = get_run_logger()
            
            logger.info(f"开始执行 Model: {model_name}")
            start_time = time.time()
            
            try:
                model_cls = MODEL_REGISTRY.get(model_name)
                if model_cls is None:
                    raise ValueError(f"Model not found: {model_name}")
                    
                model = model_cls(args_dict)
                result = model.run()
                
                execution_time = time.time() - start_time
                print(f"Model {model_name} 执行完成，耗时: {execution_time:.2f}秒")
                return result
            except Exception as e:
                print(f"Model {model_name} 执行失败: {str(e)}")
                raise
            
        return model_task

    def create_formatter_task(self, formatter_name: str, args_dict: Dict[str, Any] = None):
        """创建格式化器任务但不执行"""
        if args_dict is None:
            args_dict = {}
            
        @task(
            name=f"dataflow_formatter_{formatter_name}",
            retries=3,
            retry_delay_seconds=60,
            tags=["formatter", formatter_name],
            task_run_name=f"{formatter_name}", 
            cache_key_fn=lambda context, *args, **kwargs: f"{formatter_name}_{args}_{kwargs}",
            cache_expiration=timedelta(hours=1)
        )
        def formatter_task(dataset=None):
            from prefect import get_run_logger
            logger = get_run_logger()
            
            logger.info(f"开始执行 Formatter: {formatter_name}")
            start_time = time.time()
            
            try:
                formatter_cls = FORMATTER_REGISTRY.get(formatter_name)
                if formatter_cls is None:
                    raise ValueError(f"Formatter not found: {formatter_name}")
                    
                formatter = formatter_cls(args_dict)
                result = formatter.load_dataset()
                
                execution_time = time.time() - start_time
                print(f"Formatter {formatter_name} 执行完成，耗时: {execution_time:.2f}秒")
                return result
            except Exception as e:
                print(f"Formatter {formatter_name} 执行失败: {str(e)}")
                raise
            
        return formatter_task

    def create_generator_task(self, generator_type: str, args_dict: Dict[str, Any] = None):
        """创建生成器任务但不执行"""
        if args_dict is None:
            args_dict = {}
                
        @task(
            name=f"dataflow_generator_{generator_type}",
            retries=3,
            retry_delay_seconds=60,
            tags=["generator", generator_type],
            task_run_name=f"{generator_type}", 
            cache_key_fn=lambda context, *args, **kwargs: f"{generator_type}_{args}_{kwargs}",
            cache_expiration=timedelta(hours=1)
        )
        def generator_task(dataset=None):
            from prefect import get_run_logger
            from dataflow.utils.utils import get_generator
            logger = get_run_logger()
                
            print(f"开始执行 Generator: {generator_type}, args_dict: {args_dict}")
            start_time = time.time()
                
            try:
                generator = get_generator(generator_type, args_dict)
                print(f"ready to exec generator.run()")                
                result = generator.run()
                
                execution_time = time.time() - start_time
                print(f"Generator {generator_type} 执行完成，耗时: {execution_time:.2f}秒")
                return result
            except Exception as e:
                print(f"Generator {generator_type} 执行失败: {str(e)}")
                raise
                
        return generator_task