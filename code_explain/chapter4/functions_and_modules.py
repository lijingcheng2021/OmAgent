#!/usr/bin/env python3
"""
第4章：Python函数和模块
通过生动有趣的例子学习Python的函数和模块
"""

print("="*50)
print("欢迎来到Python函数和模块教程！")
print("="*50)

# 1. 基本函数
print("\n1. 基本函数示例")
print("-"*30)

# 1.1 简单的问候函数
print("1.1 问候函数：")
def greet(name):
    """向指定的人说问候语"""
    return f"你好，{name}！祝你今天开心！"

# 使用函数
print(greet("小明"))
print(greet("小红"))

# 1.2 计算器函数
print("\n1.2 简单计算器：")
def calculator(a, b, operation='+'):
    """基础计算器函数"""
    if operation == '+':
        return f"{a} + {b} = {a + b}"
    elif operation == '-':
        return f"{a} - {b} = {a - b}"
    elif operation == '*':
        return f"{a} × {b} = {a * b}"
    elif operation == '/':
        if b != 0:
            return f"{a} ÷ {b} = {a / b}"
        return "除数不能为零！"
    else:
        return "不支持的运算！"

# 测试计算器
print(calculator(5, 3, '+'))
print(calculator(10, 2, '*'))
print(calculator(15, 3, '/'))

# 2. 函数参数
print("\n2. 函数参数示例")
print("-"*30)

# 2.1 购物车函数
print("2.1 购物车函数：")
def calculate_total(*items, discount=0):
    """计算购物车总价
    
    Args:
        *items: 商品价格列表
        discount: 折扣率（0-1之间）
    """
    total = sum(items)
    final_price = total * (1 - discount)
    return f"原价：{total}元\n折扣：{discount*100}%\n实付：{final_price}元"

# 测试购物车
print(calculate_total(99.9, 45.5, 78.6, discount=0.1))

# 2.2 学生信息函数
print("\n2.2 学生信息函数：")
def create_student(**info):
    """创建学生信息卡
    
    Args:
        **info: 学生信息字典
    """
    return "\n".join([f"{k}: {v}" for k, v in info.items()])

# 测试学生信息
student_info = create_student(
    name="小明",
    age=15,
    grade="初三",
    hobby="足球"
)
print(student_info)

# 3. 装饰器
print("\n3. 装饰器示例")
print("-"*30)

# 3.1 时间记录装饰器
print("3.1 时间记录装饰器：")
import time
import functools

def timer_decorator(func):
    """记录函数执行时间的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间：{end_time - start_time:.4f}秒")
        return result
    return wrapper

@timer_decorator
def slow_function():
    """模拟耗时操作"""
    time.sleep(1)
    return "操作完成！"

# 测试装饰器
print(slow_function())

# 4. 生成器
print("\n4. 生成器示例")
print("-"*30)

# 4.1 斐波那契数列生成器
print("4.1 斐波那契数列：")
def fibonacci(n):
    """生成斐波那契数列的前n个数"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 打印斐波那契数列
print("斐波那契数列前10个数：")
for num in fibonacci(10):
    print(num, end=" ")
print()

# 5. 模块导入
print("\n5. 模块导入示例")
print("-"*30)

# 5.1 常用模块示例
print("5.1 常用模块：")
import random
import datetime
import math

# random模块
print("\nrandom模块示例：")
print(f"随机数（1-100）：{random.randint(1, 100)}")
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print(f"随机选择水果：{random.choice(fruits)}")

# datetime模块
print("\ndatetime模块示例：")
now = datetime.datetime.now()
print(f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")

# math模块
print("\nmath模块示例：")
print(f"π的值：{math.pi:.4f}")
print(f"2的平方根：{math.sqrt(2):.4f}")

# 6. 自定义模块
print("\n6. 自定义模块示例")
print("-"*30)

# 6.1 创建工具模块
print("6.1 工具模块：")

class Calculator:
    """简单计算器类"""
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

# 使用自定义类
calc = Calculator()
print(f"10 + 5 = {calc.add(10, 5)}")
print(f"6 × 8 = {calc.multiply(6, 8)}")

# 7. 异常处理
print("\n7. 异常处理示例")
print("-"*30)

# 7.1 安全的除法函数
print("7.1 安全的除法：")
def safe_divide(a, b):
    """安全的除法函数"""
    try:
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except ZeroDivisionError:
        return "错误：除数不能为零！"
    except TypeError:
        return "错误：请输入有效的数字！"

# 测试异常处理
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide(10, "abc"))

print("\n恭喜！你已经掌握了Python的函数和模块！")
print("记住：好的函数设计能让代码更清晰、更易维护！") 