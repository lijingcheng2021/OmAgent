#!/usr/bin/env python3
"""
第9章：Python测试和调试
通过生动有趣的例子学习Python的测试和调试技巧
"""

print("="*50)
print("欢迎来到Python测试和调试教程！")
print("="*50)

# 1. 单元测试
print("\n1. 单元测试示例")
print("-"*30)

# 1.1 购物车类
print("1.1 购物车实现：")
class ShoppingCart:
    """购物车类"""
    def __init__(self):
        self.items = {}
    
    def add_item(self, item, quantity=1):
        """添加商品"""
        if quantity <= 0:
            raise ValueError("数量必须大于0")
        
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
    
    def remove_item(self, item, quantity=1):
        """移除商品"""
        if item not in self.items:
            raise KeyError(f"商品'{item}'不在购物车中")
        
        if quantity <= 0:
            raise ValueError("数量必须大于0")
        
        if quantity >= self.items[item]:
            del self.items[item]
        else:
            self.items[item] -= quantity
    
    def get_total_quantity(self):
        """获取总数量"""
        return sum(self.items.values())
    
    def clear(self):
        """清空购物车"""
        self.items.clear()

# 1.2 购物车测试
print("1.2 购物车测试：")
import unittest

class TestShoppingCart(unittest.TestCase):
    """购物车测试类"""
    def setUp(self):
        """每个测试方法前运行"""
        self.cart = ShoppingCart()
    
    def test_add_item(self):
        """测试添加商品"""
        self.cart.add_item("苹果", 2)
        self.assertEqual(self.cart.items["苹果"], 2)
    
    def test_add_negative_quantity(self):
        """测试添加负数数量"""
        with self.assertRaises(ValueError):
            self.cart.add_item("苹果", -1)
    
    def test_remove_item(self):
        """测试移除商品"""
        self.cart.add_item("苹果", 3)
        self.cart.remove_item("苹果", 2)
        self.assertEqual(self.cart.items["苹果"], 1)
    
    def test_remove_nonexistent_item(self):
        """测试移除不存在的商品"""
        with self.assertRaises(KeyError):
            self.cart.remove_item("香蕉")
    
    def test_get_total_quantity(self):
        """测试获取总数量"""
        self.cart.add_item("苹果", 2)
        self.cart.add_item("香蕉", 3)
        self.assertEqual(self.cart.get_total_quantity(), 5)
    
    def test_clear(self):
        """测试清空购物车"""
        self.cart.add_item("苹果", 2)
        self.cart.clear()
        self.assertEqual(len(self.cart.items), 0)

# 2. 集成测试
print("\n2. 集成测试示例")
print("-"*30)

# 2.1 订单系统
print("2.1 订单系统实现：")
class Product:
    """商品类"""
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
    
    def reduce_stock(self, quantity):
        """减少库存"""
        if quantity > self.stock:
            raise ValueError("库存不足")
        self.stock -= quantity

class Order:
    """订单类"""
    def __init__(self, cart, products):
        self.cart = cart
        self.products = products
    
    def checkout(self):
        """结算订单"""
        total_price = 0
        for item, quantity in self.cart.items.items():
            if item not in self.products:
                raise KeyError(f"商品'{item}'不存在")
            
            product = self.products[item]
            product.reduce_stock(quantity)
            total_price += product.price * quantity
        
        self.cart.clear()
        return total_price

# 2.2 订单系统测试
print("2.2 订单系统测试：")
class TestOrderSystem(unittest.TestCase):
    """订单系统测试类"""
    def setUp(self):
        """设置测试环境"""
        self.cart = ShoppingCart()
        self.products = {
            "苹果": Product("苹果", 5.0, 10),
            "香蕉": Product("香蕉", 3.0, 15)
        }
        self.order = Order(self.cart, self.products)
    
    def test_successful_checkout(self):
        """测试成功结算"""
        self.cart.add_item("苹果", 2)
        self.cart.add_item("香蕉", 3)
        
        total = self.order.checkout()
        
        self.assertEqual(total, 19.0)  # 2*5 + 3*3 = 19
        self.assertEqual(self.products["苹果"].stock, 8)
        self.assertEqual(self.products["香蕉"].stock, 12)
        self.assertEqual(len(self.cart.items), 0)
    
    def test_checkout_with_insufficient_stock(self):
        """测试库存不足"""
        self.cart.add_item("苹果", 15)  # 库存只有10个
        
        with self.assertRaises(ValueError):
            self.order.checkout()

# 3. 性能测试
print("\n3. 性能测试示例")
print("-"*30)

# 3.1 性能测试装饰器
print("3.1 性能测试装饰器：")
import time
import functools

def measure_time(func):
    """测量函数执行时间的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间：{end_time - start_time:.4f}秒")
        return result
    return wrapper

# 3.2 性能测试示例
print("3.2 排序性能测试：")
@measure_time
def bubble_sort(arr):
    """冒泡排序"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

@measure_time
def quick_sort(arr):
    """快速排序"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 测试排序性能
import random
test_array = random.sample(range(1000), 100)
bubble_sort(test_array.copy())
quick_sort(test_array.copy())

# 4. 调试技巧
print("\n4. 调试技巧示例")
print("-"*30)

# 4.1 调试装饰器
print("4.1 调试装饰器：")
def debug(func):
    """调试装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"调用 {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__} 返回 {result!r}")
            return result
        except Exception as e:
            print(f"{func.__name__} 抛出异常: {type(e).__name__}: {str(e)}")
            raise
    return wrapper

# 4.2 调试示例
print("4.2 计算器调试：")
@debug
def divide(a, b):
    """除法计算"""
    return a / b

# 测试调试装饰器
try:
    print(divide(10, 2))
    print(divide(10, 0))
except ZeroDivisionError:
    pass

# 5. 日志记录
print("\n5. 日志记录示例")
print("-"*30)

# 5.1 日志配置
print("5.1 配置日志：")
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)

# 5.2 日志使用示例
print("5.2 银行账户示例：")
class BankAccount:
    """银行账户类"""
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        logger.info(f"创建账户 {account_number}，初始余额：{balance}")
    
    def deposit(self, amount):
        """存款"""
        try:
            if amount <= 0:
                logger.error(f"存款金额无效：{amount}")
                raise ValueError("存款金额必须大于0")
            
            self.balance += amount
            logger.info(f"账户 {self.account_number} 存款 {amount}，当前余额：{self.balance}")
            return self.balance
        
        except Exception as e:
            logger.exception("存款操作失败")
            raise
    
    def withdraw(self, amount):
        """取款"""
        try:
            if amount <= 0:
                logger.error(f"取款金额无效：{amount}")
                raise ValueError("取款金额必须大于0")
            
            if amount > self.balance:
                logger.warning(f"账户 {self.account_number} 余额不足，当前余额：{self.balance}，尝试取款：{amount}")
                raise ValueError("余额不足")
            
            self.balance -= amount
            logger.info(f"账户 {self.account_number} 取款 {amount}，当前余额：{self.balance}")
            return self.balance
        
        except Exception as e:
            logger.exception("取款操作失败")
            raise

# 测试银行账户
account = BankAccount("12345", 1000)
try:
    account.deposit(500)
    account.withdraw(200)
    account.withdraw(2000)  # 将引发异常
except ValueError:
    pass

print("\n恭喜！你已经掌握了Python的测试和调试技巧！")
print("记住：好的测试能让代码更可靠，好的调试能让开发更高效！") 