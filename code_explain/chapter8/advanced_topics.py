#!/usr/bin/env python3
"""
第8章：Python高级主题示例代码
"""

import functools
import time
import threading
import multiprocessing
from typing import TypeVar, Generic, List, Optional
from dataclasses import dataclass
from contextlib import contextmanager

# 1. 元编程

## 1.1 装饰器
def timing_decorator(func):
    """测量函数执行时间的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """测试用的慢函数"""
    time.sleep(1)
    return "完成"

## 1.2 元类
class SingletonMeta(type):
    """单例模式元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """使��单例模式的数据库连接类"""
    def __init__(self):
        self.connected = False
    
    def connect(self):
        if not self.connected:
            print("建立数据库连接...")
            self.connected = True
        return self

# 2. 并发编程

## 2.1 多线程
class ThreadWorker:
    """线程工作者示例"""
    def __init__(self):
        self.result = None
        self._lock = threading.Lock()
    
    def process_data(self, data: List[int]):
        """处理数据的线程函数"""
        with self._lock:
            self.result = sum(data)
            print(f"线程 {threading.current_thread().name} 计算结果: {self.result}")

## 2.2 多进程
def process_worker(numbers: List[int], queue: multiprocessing.Queue):
    """进程工作函数"""
    result = sum(numbers)
    queue.put(result)

class ProcessPool:
    """简单的进程池实现"""
    def __init__(self, num_processes: int):
        self.num_processes = num_processes
        self.queue = multiprocessing.Queue()
    
    def map(self, data: List[List[int]]) -> List[int]:
        """并行处理数据"""
        processes = []
        for chunk in data:
            p = multiprocessing.Process(
                target=process_worker,
                args=(chunk, self.queue)
            )
            processes.append(p)
            p.start()
        
        results = []
        for _ in processes:
            results.append(self.queue.get())
        
        for p in processes:
            p.join()
        
        return results

# 3. 泛型编程

T = TypeVar('T')

class Stack(Generic[T]):
    """泛型栈实现"""
    def __init__(self):
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        if not self._items:
            return None
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        if not self._items:
            return None
        return self._items[-1]
    
    def is_empty(self) -> bool:
        return len(self._items) == 0

# 4. 上下文管理

@contextmanager
def timer():
    """计时器上下文管理器"""
    start = time.time()
    yield
    end = time.time()
    print(f"执行时间: {end - start:.4f} 秒")

# 5. 数据类

@dataclass
class Point:
    """二维点数据类"""
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        """计算到原点的距离"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

def main():
    """主函数：演示各种高级特性的���用"""
    # 1. 装饰器示例
    print("\n1. 装饰器示例:")
    result = slow_function()
    print(f"函数返回: {result}")
    
    # 2. 单例模式示例
    print("\n2. 单例模式示例:")
    db1 = Database().connect()
    db2 = Database().connect()
    print(f"db1 和 db2 是同一个实例: {db1 is db2}")
    
    # 3. 多线程示例
    print("\n3. 多线程示例:")
    worker = ThreadWorker()
    threads = []
    data_chunks = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    for i, chunk in enumerate(data_chunks):
        thread = threading.Thread(
            target=worker.process_data,
            args=(chunk,),
            name=f"Thread-{i}"
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # 4. 多进程示例
    print("\n4. 多进程示例:")
    pool = ProcessPool(3)
    results = pool.map(data_chunks)
    print(f"多进程计算结果: {results}")
    
    # 5. 泛型栈示例
    print("\n5. 泛型栈示例:")
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"整数栈顶元素: {int_stack.peek()}")
    
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"字符串栈顶元素: {str_stack.peek()}")
    
    # 6. 上下文管理器示例
    print("\n6. 上下文管理器示例:")
    with timer():
        time.sleep(0.5)
    
    # 7. 数据类示例
    print("\n7. 数据类示例:")
    point = Point(3.0, 4.0)
    print(f"点 {point} 到原点的距离: {point.distance_from_origin()}")

if __name__ == "__main__":
    main() 