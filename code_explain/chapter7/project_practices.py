"""
第七章：项目实践与高级特性
本章结合OmAgent项目，介绍Python在实际项目中的应用，以及一些高级特性的使用
"""

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*50)
    print(title)
    print("="*50)

#############################
# 1. 项目架构和设计模式
#############################
print_section("1. 项目架构和设计模式")

# 1.1 单例模式
print("\n1.1 单例模式:")

from typing import Dict, Any, Optional
import json
from pathlib import Path

class Config:
    """配置管理类（单例模式）"""
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_config(self, config_path: str):
        """加载配置文件"""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r') as f:
                self._config = json.load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(key, default)

# 1.2 工厂模式
print("\n1.2 工厂模式:")

from abc import ABC, abstractmethod

class MetricsCollector(ABC):
    """指标收集器接口"""
    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        pass

class CPUCollector(MetricsCollector):
    """CPU指标收集器"""
    def collect(self) -> Dict[str, Any]:
        return {"cpu_usage": 75.5}

class MemoryCollector(MetricsCollector):
    """内存指标收集器"""
    def collect(self) -> Dict[str, Any]:
        return {"memory_usage": 60.2}

class CollectorFactory:
    """收集器工厂"""
    @staticmethod
    def create_collector(collector_type: str) -> MetricsCollector:
        if collector_type == "cpu":
            return CPUCollector()
        elif collector_type == "memory":
            return MemoryCollector()
        else:
            raise ValueError(f"Unknown collector type: {collector_type}")

#############################
# 2. 高级特性应用
#############################
print_section("2. 高级特性应用")

# 2.1 上下文管理器
print("\n2.1 上下文管理器:")

class DatabaseConnection:
    """数据库连接管理器"""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
    
    def __enter__(self):
        print(f"连接到数据库 {self.host}:{self.port}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关闭数据库连接")
        if exc_type:
            print(f"处理异常: {exc_type.__name__}: {exc_val}")
        return False  # 不吞没异常

# 2.2 描述符
print("\n2.2 描述符:")

class Validated:
    """验证描述符基类"""
    def __init__(self, name: str = None):
        self.name = name
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

class RangeValidated(Validated):
    """范围验证描述符"""
    def __init__(self, min_val: float, max_val: float):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
    
    def __set__(self, instance, value):
        if not self.min_val <= value <= self.max_val:
            raise ValueError(
                f"{self.name} must be between {self.min_val} "
                f"and {self.max_val}"
            )
        instance.__dict__[self.name] = value

class SystemMetrics:
    """系统指标类"""
    cpu_usage = RangeValidated(0, 100)
    memory_usage = RangeValidated(0, 100)
    disk_usage = RangeValidated(0, 100)

#############################
# 3. 元编程
#############################
print_section("3. 元编程")

# 3.1 装饰器工厂
print("\n3.1 装饰器工厂:")

def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    print(f"重试第 {attempts} 次...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# 3.2 元类
print("\n3.2 元类:")

class Singleton(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    """日志类（使用元类实现单例）"""
    def __init__(self):
        self.logs = []
    
    def log(self, message: str):
        self.logs.append(message)
        print(f"LOG: {message}")

#############################
# 4. 项目最佳实践
#############################
print_section("4. 项目最佳实践")

# 4.1 配置管理
print("\n4.1 配置管理:")

from dataclasses import dataclass
from typing import Optional

@dataclass
class ServerConfig:
    """服务器配置数据类"""
    host: str
    port: int
    debug: bool = False
    timeout: Optional[int] = None

# 4.2 日志记录
print("\n4.2 日志记录:")

import logging
from functools import wraps

def setup_logger():
    """配置日志记录器"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def log_function_call(func):
    """记录函数调用的装饰器"""
    logger = setup_logger()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"调用函数 {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {str(e)}")
            raise
    return wrapper

# 4.3 错误处理
print("\n4.3 错误处理:")

class ApplicationError(Exception):
    """应用程序基础异常类"""
    def __init__(self, message: str, error_code: int = None):
        super().__init__(message)
        self.error_code = error_code

class ConfigError(ApplicationError):
    """配置错误"""
    pass

class NetworkError(ApplicationError):
    """网络错误"""
    pass

def handle_application_error(func):
    """处理应用程序异常的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConfigError as e:
            print(f"配置错误 (代码: {e.error_code}): {str(e)}")
        except NetworkError as e:
            print(f"网络错误 (代码: {e.error_code}): {str(e)}")
        except ApplicationError as e:
            print(f"应用错误 (代码: {e.error_code}): {str(e)}")
        except Exception as e:
            print(f"未知错误: {str(e)}")
    return wrapper

#############################
# 5. 测试和调试
#############################
print_section("5. 测试和调试")

import unittest
from unittest.mock import Mock, patch

class TestMetricsCollector(unittest.TestCase):
    """指标收集器测试类"""
    
    def setUp(self):
        self.collector = CPUCollector()
    
    def test_collect_metrics(self):
        """测试指标收集"""
        metrics = self.collector.collect()
        self.assertIn("cpu_usage", metrics)
        self.assertIsInstance(metrics["cpu_usage"], (int, float))
    
    @patch('builtins.print')
    def test_logging(self, mock_print):
        """测试日志记录"""
        logger = Logger()
        logger.log("测试消息")
        mock_print.assert_called_with("LOG: 测试消息")

"""
练习题：
1. 实现一个完整的配置管理系统，支持多种格式（JSON、YAML等）
2. 创建一个通用的重试机制，可以处理不同类型的错误
3. 设计一个插件系统，支持动态加载和卸载功能模块
4. 实现一个完整的日志系统，支持多种输出方式和日志级别
""" 