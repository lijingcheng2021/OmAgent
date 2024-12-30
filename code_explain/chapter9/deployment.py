#!/usr/bin/env python3
"""
第9章：Python项目部署与运维示例代码
"""

import os
import json
import yaml
import logging
import shutil
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel, validator
import aiohttp
import asyncio

# 1. 配置管理

## 1.1 环境变量配置
class Settings(BaseModel):
    """应用配置管理"""
    # API配置
    api_key: str
    api_endpoint: Optional[str] = None
    
    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str
    db_password: str
    
    # 应用配置
    debug: bool = False
    log_level: str = "INFO"
    
    @validator('db_port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()

## 1.2 YAML配置
class ConfigManager:
    """配置管理器"""
    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self.config_cache: Dict[str, Any] = {}
    
    def load_config(self, name: str) -> Dict[str, Any]:
        """加载YAML配置"""
        config_path = self.config_dir / f"{name}.yml"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file {name}.yml not found")
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
            self.config_cache[name] = config
            return config
    
    def save_config(self, name: str, config: Dict[str, Any]):
        """保存配置到YAML文件"""
        config_path = self.config_dir / f"{name}.yml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        self.config_cache[name] = config

# 2. 日志系统

class AppLogger:
    """应用日志记录器"""
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._create_formatter())
        self.logger.addHandler(console_handler)
        
        # 添加文件处理器
        file_handler = logging.FileHandler(f"{name}.log")
        file_handler.setFormatter(self._create_formatter())
        self.logger.addHandler(file_handler)
    
    def _create_formatter(self):
        """创建日志格式化器"""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def info(self, message: str, **kwargs):
        """记录信息日志"""
        self._log('info', message, kwargs)
    
    def error(self, message: str, **kwargs):
        """记录错误日志"""
        self._log('error', message, kwargs)
    
    def _log(self, level: str, message: str, extra: Dict[str, Any]):
        """格式化并记录日志"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            **extra
        }
        getattr(self.logger, level)(json.dumps(log_data))

# 3. 系统监控

@dataclass
class SystemMetrics:
    """系统指标数据类"""
    cpu_percent: float
    memory_used: float
    memory_total: float
    disk_used: float
    disk_total: float

class SystemMonitor:
    """系统监控器"""
    def __init__(self):
        self.logger = AppLogger("system_monitor")
    
    def collect_metrics(self) -> SystemMetrics:
        """收集系统指标"""
        cpu_percent = psutil.cpu_percent(interval=1)
        
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 ** 3)  # GB
        memory_total = memory.total / (1024 ** 3)  # GB
        
        disk = psutil.disk_usage('/')
        disk_used = disk.used / (1024 ** 3)  # GB
        disk_total = disk.total / (1024 ** 3)  # GB
        
        metrics = SystemMetrics(
            cpu_percent=cpu_percent,
            memory_used=memory_used,
            memory_total=memory_total,
            disk_used=disk_used,
            disk_total=disk_total
        )
        
        self.logger.info(
            "System metrics collected",
            cpu_percent=cpu_percent,
            memory_used=f"{memory_used:.2f}GB",
            memory_total=f"{memory_total:.2f}GB",
            disk_used=f"{disk_used:.2f}GB",
            disk_total=f"{disk_total:.2f}GB"
        )
        
        return metrics

# 4. 健康检查

class HealthCheck:
    """健康检查服务"""
    def __init__(self):
        self.logger = AppLogger("health_check")
        self.services = {}
    
    def register_service(self, name: str, url: str):
        """注册服务"""
        self.services[name] = url
        self.logger.info(f"Service registered", name=name, url=url)
    
    async def check_service(self, name: str, url: str) -> Dict[str, Any]:
        """检查单个服务"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health") as response:
                    if response.status == 200:
                        return {"status": "healthy", "code": 200}
                    return {"status": "unhealthy", "code": response.status}
        except Exception as e:
            self.logger.error(
                "Service check failed",
                service=name,
                error=str(e)
            )
            return {"status": "error", "message": str(e)}
    
    async def check_all(self) -> Dict[str, Dict[str, Any]]:
        """检查所有服务"""
        tasks = [
            self.check_service(name, url)
            for name, url in self.services.items()
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(self.services.keys(), results))

# 5. 备份管理

class BackupManager:
    """备份管理器"""
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logger = AppLogger("backup_manager")
    
    def create_backup(self, source_dir: str, name: str = None) -> Path:
        """创建备份"""
        source = Path(source_dir)
        if not source.exists():
            raise FileNotFoundError(f"Source directory {source} not found")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or source.name
        backup_file = self.backup_dir / f"{backup_name}_{timestamp}.tar.gz"
        
        try:
            shutil.make_archive(
                str(backup_file.with_suffix('')),
                'gztar',
                source_dir
            )
            self.logger.info(
                "Backup created",
                source=str(source),
                backup_file=str(backup_file)
            )
            return backup_file
        except Exception as e:
            self.logger.error(
                "Backup failed",
                source=str(source),
                error=str(e)
            )
            raise

def main():
    """主函数：演示各个组件的使用"""
    # 1. 配置管理示例
    print("\n1. 配置管理示例:")
    try:
        settings = Settings(
            api_key="test_key",
            db_user="admin",
            db_password="secret"
        )
        print(f"配置验证成功: {settings.dict()}")
    except Exception as e:
        print(f"配置验证失败: {e}")
    
    # 2. 日志系统示例
    print("\n2. 日志系统示例:")
    logger = AppLogger("demo_app")
    logger.info("应用启动", version="1.0.0")
    logger.error("示例错误", error_code=500)
    
    # 3. 系统监控示例
    print("\n3. 系统监控示例:")
    monitor = SystemMonitor()
    metrics = monitor.collect_metrics()
    print(f"系统指标: {metrics}")
    
    # 4. 健康检查示例
    print("\n4. 健康检查示例:")
    health_checker = HealthCheck()
    health_checker.register_service("api", "http://localhost:8000")
    health_checker.register_service("db", "http://localhost:5432")
    
    async def run_health_check():
        results = await health_checker.check_all()
        print(f"健康检查结果: {results}")
    
    asyncio.run(run_health_check())
    
    # 5. 备份管理示例
    print("\n5. 备份管理示例:")
    backup_mgr = BackupManager("./backups")
    try:
        backup_file = backup_mgr.create_backup("./test_data", "test_backup")
        print(f"备份文件创建成功: {backup_file}")
    except Exception as e:
        print(f"备份创建失败: {e}")

if __name__ == "__main__":
    main() 