"""
第六章：异步编程
本章介绍Python的异步编程特性，包括协程、异步IO、事件循环等概念
"""

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*50)
    print(title)
    print("="*50)

#############################
# 1. 协程基础
#############################
print_section("1. 协程基础")
print("协程特点：异步执行、非阻塞、高效处理IO密集型任务")

# 1.1 定义和使用协程
print("\n1.1 定义和使用协程:")

import asyncio
import time

async def hello(name: str, delay: float) -> str:
    """
    简单的协程函数
    Args:
        name: 名称
        delay: 延迟时间
    """
    print(f"开始处理 {name}")
    await asyncio.sleep(delay)  # 模拟IO操作
    print(f"完成处理 {name}")
    return f"Hello, {name}!"

# 运行协程
async def main_hello():
    result = await hello("World", 1)
    print(result)

# 注意：实际运行时使用
# asyncio.run(main_hello())

# 1.2 并发执行多个协程
print("\n1.2 并发执行多个协程:")

async def main_concurrent():
    """并发执行多个协程"""
    tasks = [
        hello("Task1", 1),
        hello("Task2", 2),
        hello("Task3", 1.5)
    ]
    results = await asyncio.gather(*tasks)
    print(f"所有任务结果: {results}")

# asyncio.run(main_concurrent())

#############################
# 2. 异步上下文管理器
#############################
print_section("2. 异步上下文管理器")

class AsyncResource:
    """异步资源管理示例"""
    async def __aenter__(self):
        print("获取资源")
        await asyncio.sleep(1)  # 模拟资源获取
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
        await asyncio.sleep(0.5)  # 模拟资源释放
    
    async def process(self):
        print("处理资源")
        await asyncio.sleep(1)

async def use_resource():
    async with AsyncResource() as resource:
        await resource.process()

# asyncio.run(use_resource())

#############################
# 3. 异步迭代器
#############################
print_section("3. 异步迭代器")

class AsyncDataStream:
    """异步数据流示例"""
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        
        self.current += 1
        await asyncio.sleep(0.5)  # 模拟数据获取延迟
        return self.current - 1

async def process_stream():
    async for number in AsyncDataStream(0, 5):
        print(f"处理数据: {number}")

# asyncio.run(process_stream())

#############################
# 4. 项目实践：异步监控系统
#############################
print_section("4. 项目实践：异步监控系统")

from typing import Dict, Any
import random

class AsyncSystemMonitor:
    """异步系统监控类"""
    
    async def collect_cpu_metrics(self) -> float:
        """收集CPU指标"""
        await asyncio.sleep(1)  # 模拟IO操作
        return random.uniform(0, 100)
    
    async def collect_memory_metrics(self) -> float:
        """收集内存指标"""
        await asyncio.sleep(0.5)  # 模拟IO操作
        return random.uniform(0, 100)
    
    async def collect_disk_metrics(self) -> float:
        """收集磁盘指标"""
        await asyncio.sleep(0.8)  # 模拟IO操作
        return random.uniform(0, 100)
    
    async def collect_all_metrics(self) -> Dict[str, float]:
        """并发收集所有指标"""
        cpu, memory, disk = await asyncio.gather(
            self.collect_cpu_metrics(),
            self.collect_memory_metrics(),
            self.collect_disk_metrics()
        )
        return {
            "cpu_usage": cpu,
            "memory_usage": memory,
            "disk_usage": disk
        }

class AsyncMetricsCollector:
    """异步指标收集器"""
    def __init__(self, interval: float = 5.0):
        self.interval = interval
        self.monitor = AsyncSystemMonitor()
        self.is_running = False
    
    async def start_collecting(self):
        """开始收集指标"""
        self.is_running = True
        while self.is_running:
            metrics = await self.monitor.collect_all_metrics()
            print(f"当前系统指标: {metrics}")
            await asyncio.sleep(self.interval)
    
    async def stop_collecting(self):
        """停止收集指标"""
        self.is_running = False

async def monitor_demo():
    """监控系统演示"""
    collector = AsyncMetricsCollector(interval=2)
    
    # 运行5秒后停止
    asyncio.create_task(collector.start_collecting())
    await asyncio.sleep(5)
    await collector.stop_collecting()

# 运行演示
# asyncio.run(monitor_demo())

#############################
# 5. 异步最佳实践
#############################
print_section("5. 异步最佳实践")

# 5.1 异常处理
print("\n5.1 异常处理:")

async def risky_operation():
    """可能抛出异常的操作"""
    await asyncio.sleep(1)
    raise ValueError("操作失败")

async def handle_errors():
    try:
        await risky_operation()
    except ValueError as e:
        print(f"捕获到异常: {e}")

# 5.2 超时处理
print("\n5.2 超时处理:")

async def long_operation():
    """耗时操作"""
    await asyncio.sleep(5)
    return "操作完成"

async def with_timeout():
    try:
        async with asyncio.timeout(2):
            result = await long_operation()
            print(result)
    except asyncio.TimeoutError:
        print("操作超时")

"""
练习题：
1. 创建一个异步文件读取器，能够异步读取大文件
2. 实现一个异步HTTP客户端，支持并发请求
3. 创建一个异步队列，实现生产者-消费者模式
4. 实现一个支持异步操作的缓存系统
""" 