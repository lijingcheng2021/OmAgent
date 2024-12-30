"""
第五章：面向对象编程（OOP）
本章介绍Python的面向对象编程特性，包括类、继承、多态、魔术方法等
"""

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*50)
    print(title)
    print("="*50)

#############################
# 1. 类和对象基础
#############################
print_section("1. 类和对象基础")
print("类的特点：封装、继承、多态")

# 1.1 类的定义和实例化
print("\n1.1 类的定义和实例化:")

class Student:
    """学生类"""
    # 类变量
    school = "Python大学"
    
    def __init__(self, name: str, age: int):
        """
        初始化方法
        Args:
            name: 学生姓名
            age: 学生年龄
        """
        # 实例变量
        self.name = name
        self.age = age
        self._score = 0  # 私有变量（约定）
    
    def study(self, subject: str):
        """学习方法"""
        print(f"{self.name}正在学习{subject}")
    
    @property
    def score(self) -> int:
        """分数属性"""
        return self._score
    
    @score.setter
    def score(self, value: int):
        """设置分数"""
        if 0 <= value <= 100:
            self._score = value
        else:
            raise ValueError("分数必须在0-100之间")

# 创建实例
student = Student("张三", 20)
student.study("Python")
student.score = 85
print(f"学生分数: {student.score}")

# 1.2 类方法和静态方法
print("\n1.2 类方法和静态方法:")

class Calculator:
    """计算器类"""
    
    @classmethod
    def add_numbers(cls, *numbers: float) -> float:
        """类方法示例"""
        return sum(numbers)
    
    @staticmethod
    def is_even(number: int) -> bool:
        """静态方法示例"""
        return number % 2 == 0

print(f"求和结果: {Calculator.add_numbers(1, 2, 3)}")
print(f"4是偶数吗？ {Calculator.is_even(4)}")

#############################
# 2. 继承和多态
#############################
print_section("2. 继承和多态")

# 2.1 基类和派生类
print("\n2.1 基类和派生类:")

class Animal:
    """动物基类"""
    def __init__(self, name: str):
        self.name = name
    
    def speak(self):
        """发出声音"""
        pass

class Dog(Animal):
    """狗类"""
    def speak(self):
        return f"{self.name}说：汪汪！"

class Cat(Animal):
    """猫类"""
    def speak(self):
        return f"{self.name}说：喵喵！"

# 多态示例
def animal_speak(animal: Animal):
    """多态函数"""
    print(animal.speak())

dog = Dog("旺财")
cat = Cat("咪咪")
animal_speak(dog)
animal_speak(cat)

# 2.2 多重继承
print("\n2.2 多重继承:")

class Flyable:
    """可飞行接口"""
    def fly(self):
        print("正在飞行...")

class Swimmable:
    """可游泳接口"""
    def swim(self):
        print("正在游泳...")

class Duck(Animal, Flyable, Swimmable):
    """鸭子类"""
    def speak(self):
        return f"{self.name}说：嘎嘎！"

duck = Duck("唐老鸭")
duck.speak()
duck.fly()
duck.swim()

#############################
# 3. 魔术方法
#############################
print_section("3. 魔术方法")

class Vector:
    """向量类，展示魔术方法的使用"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other: 'Vector') -> 'Vector':
        """向量加法"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __len__(self) -> float:
        """向量长度"""
        return int((self.x**2 + self.y**2)**0.5)

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(f"v1 = {v1}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1的长度: {len(v1)}")

#############################
# 4. 项目实践：OmAgent中的类设计
#############################
print_section("4. 项目实践：OmAgent中的类设计")

# 4.1 基础设施监控类
print("\n4.1 基础设施监控类:")

from abc import ABC, abstractmethod
from typing import Dict, Any

class Monitor(ABC):
    """抽象监控类"""
    
    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """收集指标"""
        pass
    
    @abstractmethod
    def check_health(self) -> bool:
        """检查健康状态"""
        pass

class SystemMonitor(Monitor):
    """系统监控类"""
    def __init__(self):
        self.metrics = {}
    
    def collect_metrics(self) -> Dict[str, Any]:
        # 模拟收集系统指标
        self.metrics = {
            "cpu_usage": 45.5,
            "memory_usage": 60.2,
            "disk_usage": 78.1
        }
        return self.metrics
    
    def check_health(self) -> bool:
        # 检查系统健康状态
        return all(v < 90 for v in self.metrics.values())

# 4.2 配置管理类
print("\n4.2 配置管理类:")

class ConfigManager:
    """单例配置管理类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = {}
            self.initialized = True
    
    def load_config(self, config_file: str):
        """加载配置"""
        # 模拟加载配置
        self.config = {
            "host": "localhost",
            "port": 8080,
            "timeout": 30
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)

# 使用示例
monitor = SystemMonitor()
print(f"系统指标: {monitor.collect_metrics()}")
print(f"系统健康状态: {monitor.check_health()}")

config = ConfigManager()
config.load_config("config.json")
print(f"服务器地址: {config.get('host')}:{config.get('port')}")

"""
练习题：
1. 创建一个银行账户类，实现存款、取款功能，并使用属性装饰器管理余额
2. 实现一个简单的日志类，使用单例模式确保只有一个日志实例
3. 创建一个图形类继承体系，包括圆形、矩形等，实现面积计算
4. 使用魔术方法实现一个分数类，支持基本算术运算
""" 