#!/usr/bin/env python3
"""
第6章：Python错误处理和调试
通过生动有趣的例子学习Python的错误处理和调试技巧
"""

print("="*50)
print("欢迎来到Python错误处理和调试教程！")
print("="*50)

# 1. 基本异常处理
print("\n1. 基本异常处理示例")
print("-"*30)

# 1.1 简单的除法计算器
print("1.1 除法计算器：")
def divide_numbers():
    """演示基本的异常处理"""
    try:
        x = int(input("请输入被除数："))
        y = int(input("请输入除数："))
        result = x / y
        print(f"{x} ÷ {y} = {result}")
    except ValueError:
        print("错误：请输入有效的数字！")
    except ZeroDivisionError:
        print("错误：除数不能为零！")
    except Exception as e:
        print(f"发生未知错误：{str(e)}")
    else:
        print("计算成功完成！")
    finally:
        print("计算器运行结束")

# 注释掉交互式输入，改用模拟数据
def test_divide_numbers():
    """测试除法计算器的各种情况"""
    test_cases = [
        (10, 2),    # 正常情况
        (10, 0),    # 除零错误
        ("a", 2),   # 类型错误
    ]
    
    for x, y in test_cases:
        print(f"\n测试输入：{x}, {y}")
        try:
            result = x / y
            print(f"{x} ÷ {y} = {result}")
        except TypeError:
            print("错误：请输入有效的数字！")
        except ZeroDivisionError:
            print("错误：除数不能为零！")
        except Exception as e:
            print(f"发生未知错误：{str(e)}")
        else:
            print("计算成功完成！")
        finally:
            print("本次测试结束")

# 运行测试
test_divide_numbers()

# 2. 自定义异常
print("\n2. 自定义异常示例")
print("-"*30)

# 2.1 银行账户异常
print("2.1 银行账户操作：")
class InsufficientFundsError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足！当前余额：{balance}元，需要：{amount}元")

class BankAccount:
    """银行账户类"""
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        """取款方法"""
        if amount <= 0:
            raise ValueError("取款���额必须大于0！")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return f"取款成功！当前余额：{self.balance}元"

# 测试银行账户
account = BankAccount(100)
test_amounts = [50, 0, 200]

for amount in test_amounts:
    print(f"\n尝试取款：{amount}元")
    try:
        result = account.withdraw(amount)
        print(result)
    except ValueError as e:
        print(f"错误：{str(e)}")
    except InsufficientFundsError as e:
        print(f"错误：{str(e)}")

# 3. 调试技巧
print("\n3. 调试技巧示例")
print("-"*30)

# 3.1 使用断言
print("3.1 使用断言：")
def calculate_rectangle_area(width, height):
    """计算矩形面积，使用断言确保参数有效"""
    assert width > 0, "宽度必须大于0"
    assert height > 0, "高度必须大于0"
    return width * height

# 测试断言
test_dimensions = [
    (5, 3),    # 正常情况
    (-1, 3),   # 无效宽度
    (5, -2)    # 无效高度
]

for width, height in test_dimensions:
    print(f"\n计算面积：宽={width}, 高={height}")
    try:
        area = calculate_rectangle_area(width, height)
        print(f"矩形面积：{area}")
    except AssertionError as e:
        print(f"断言���误：{str(e)}")

# 3.2 使用日志
print("\n3.2 使用日志：")
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_user_data(user_dict):
    """处理用户数据，使用日志记录关键信息"""
    logging.info(f"开始处理用户数据：{user_dict}")
    
    try:
        # 验证数据
        if not isinstance(user_dict, dict):
            raise TypeError("输入必须是字典类型")
        
        # 检查必要字段
        required_fields = ['name', 'age']
        for field in required_fields:
            if field not in user_dict:
                logging.error(f"缺少必要字段：{field}")
                raise ValueError(f"缺少必要字段：{field}")
        
        # 处理数据
        logging.debug("验证通过，处理数据...")
        result = {
            'name': user_dict['name'].upper(),
            'age': int(user_dict['age']),
            'status': 'processed'
        }
        
        logging.info("数据处理成功")
        return result
    
    except Exception as e:
        logging.error(f"处理数据时出错：{str(e)}")
        raise

# 测试数据处理
test_data = [
    {'name': '张三', 'age': '20'},           # 正确数据
    {'name': '李四'},                        # 缺少年龄
    'invalid_data',                         # 无效数据类型
]

for data in test_data:
    print(f"\n处理数据：{data}")
    try:
        result = process_user_data(data)
        print(f"处理结果：{result}")
    except Exception as e:
        print(f"错误：{str(e)}")

# 4. 上下文管理器
print("\n4. 上下文管理器示例")
print("-"*30)

# 4.1 自定义文件操作器
print("4.1 文件操作器：")
class FileHandler:
    """文件处理器"""
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """进入上下文"""
        print(f"打开文件：{self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        print(f"关闭文件：{self.filename}")
        if self.file:
            self.file.close()
        if exc_type is not None:
            print(f"处理文件时出错：{str(exc_val)}")
        return True

# 测试文件操作
filename = "test.txt"

# 写入文件
print("\n写入文件：")
try:
    with FileHandler(filename, 'w') as f:
        f.write("Hello, World!")
except Exception as e:
    print(f"写入文件时出错：{str(e)}")

# 读取文件
print("\n读取文件：")
try:
    with FileHandler(filename, 'r') as f:
        content = f.read()
        print(f"文件内容：{content}")
except Exception as e:
    print(f"读取文件时出错：{str(e)}")

# 5. 综合示例
print("\n5. 综合示例")
print("-"*30)

# 5.1 商品库存管理
print("5.1 商品库存管理：")
class InventoryError(Exception):
    """库存相关异常的基类"""
    pass

class OutOfStockError(InventoryError):
    """库存不足异常"""
    def __init__(self, product, quantity, stock):
        self.product = product
        self.quantity = quantity
        self.stock = stock
        super().__init__(
            f"商品'{product}'库存不足！"
            f"当前库存：{stock}，需要：{quantity}"
        )

class InvalidQuantityError(InventoryError):
    """无效数量异常"""
    def __init__(self, quantity):
        self.quantity = quantity
        super().__init__(f"无效的数量：{quantity}，必须大于0")

class InventoryManager:
    """库存管理器"""
    def __init__(self):
        self.inventory = {}
        logging.info("初始化库存管理器")
    
    def add_product(self, product, quantity):
        """添加商品库存"""
        logging.debug(f"添加商品：{product}, 数量：{quantity}")
        try:
            if quantity <= 0:
                raise InvalidQuantityError(quantity)
            
            if product in self.inventory:
                self.inventory[product] += quantity
            else:
                self.inventory[product] = quantity
            
            logging.info(f"成功添加商品'{product}'，当前库存：{self.inventory[product]}")
            return f"成功添加{quantity}个'{product}'"
        
        except Exception as e:
            logging.error(f"添加商品时出错：{str(e)}")
            raise
    
    def remove_product(self, product, quantity):
        """减少商品库存"""
        logging.debug(f"减少商品：{product}, 数量：{quantity}")
        try:
            if quantity <= 0:
                raise InvalidQuantityError(quantity)
            
            if product not in self.inventory:
                raise KeyError(f"商品'{product}'不存在")
            
            if self.inventory[product] < quantity:
                raise OutOfStockError(
                    product, quantity, self.inventory[product]
                )
            
            self.inventory[product] -= quantity
            logging.info(f"成功减少商品'{product}'，当前库存：{self.inventory[product]}")
            return f"成功减少{quantity}个'{product}'"
        
        except Exception as e:
            logging.error(f"减少商品时出错：{str(e)}")
            raise
    
    def check_stock(self, product):
        """查看商品库存"""
        logging.debug(f"查看商品库存：{product}")
        try:
            if product not in self.inventory:
                raise KeyError(f"商品'{product}'不存在")
            
            stock = self.inventory[product]
            logging.info(f"商品'{product}'当前库存：{stock}")
            return stock
        
        except Exception as e:
            logging.error(f"查看库存时出错：{str(e)}")
            raise

# 测试库存管理
manager = InventoryManager()

# 测试添加商品
print("\n测试添加商品：")
test_additions = [
    ("苹果", 100),    # 正常添加
    ("香蕉", -5),     # 无效数量
    ("苹果", 50)      # 追加库存
]

for product, quantity in test_additions:
    try:
        result = manager.add_product(product, quantity)
        print(result)
    except InventoryError as e:
        print(f"库存错误：{str(e)}")
    except Exception as e:
        print(f"其他错误：{str(e)}")

# 测试减少商品
print("\n测试减少商品：")
test_removals = [
    ("苹果", 30),     # 正常减少
    ("香蕉", 10),     # 不存在的商品
    ("苹果", 200)     # 库存不足
]

for product, quantity in test_removals:
    try:
        result = manager.remove_product(product, quantity)
        print(result)
    except InventoryError as e:
        print(f"库存错误：{str(e)}")
    except Exception as e:
        print(f"其他错误：{str(e)}")

# 测试查看库存
print("\n测试查看库存：")
test_products = ["苹果", "香蕉"]

for product in test_products:
    try:
        stock = manager.check_stock(product)
        print(f"商品'{product}'的库存：{stock}")
    except Exception as e:
        print(f"错误：{str(e)}")

print("\n恭喜！你已经掌握了Python的错误处理和调试技巧！")
print("记住：好的错误处理能让程序更健壮、更可靠！") 