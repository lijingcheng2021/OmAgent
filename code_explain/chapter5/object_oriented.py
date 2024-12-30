#!/usr/bin/env python3
"""
第5章：Python面向对象编程
通过生动有趣的例子学习Python的面向对象编程
"""

print("="*50)
print("欢迎来到Python面向对象编程教程！")
print("="*50)

# 1. 基本类定义
print("\n1. 基本类定义示例")
print("-"*30)

# 1.1 宠物类
print("1.1 宠物类：")
class Pet:
    """宠物基类"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"我是{self.name}，今年{self.age}岁了"
    
    def make_sound(self):
        return "..."

# 创建宠物实例
my_pet = Pet("小白", 2)
print(my_pet.introduce())

# 2. 继承
print("\n2. 继承示例")
print("-"*30)

# 2.1 具体宠物类
print("2.1 具体宠物类：")
class Dog(Pet):
    """狗类"""
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def make_sound(self):
        return "汪汪！"
    
    def fetch_ball(self):
        return f"{self.name}飞快地去捡球了！"

class Cat(Pet):
    """猫类"""
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def make_sound(self):
        return "喵喵～"
    
    def catch_mouse(self):
        return f"{self.color}色的{self.name}正在捉老鼠..."

# 创建具体宠物实例
my_dog = Dog("旺财", 3, "金毛")
my_cat = Cat("咪咪", 2, "橘")

print(my_dog.introduce())
print(my_dog.make_sound())
print(my_dog.fetch_ball())

print(my_cat.introduce())
print(my_cat.make_sound())
print(my_cat.catch_mouse())

# 3. 封装
print("\n3. 封装示例")
print("-"*30)

# 3.1 银行账户类
print("3.1 银行账户类：")
class BankAccount:
    """银行账户类"""
    def __init__(self, account_number, owner):
        self._account_number = account_number  # 受保护的属性
        self._owner = owner
        self.__balance = 0  # 私有属性
    
    def deposit(self, amount):
        """存款方法"""
        if amount > 0:
            self.__balance += amount
            return f"存款成功！当前余额：{self.__balance}元"
        return "存款金额必须大于0！"
    
    def withdraw(self, amount):
        """取款方法"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"取款成��！当前余额：{self.__balance}元"
        return "余额不足或取款金额无效！"
    
    def get_balance(self):
        """查询余额"""
        return f"{self._owner}的账户余额：{self.__balance}元"

# 测试银行账户
account = BankAccount("1234567", "张三")
print(account.deposit(1000))
print(account.withdraw(500))
print(account.get_balance())

# 4. 多态
print("\n4. 多态示例")
print("-"*30)

# 4.1 图形类
print("4.1 图形类：")
from math import pi

class Shape:
    """图形基类"""
    def area(self):
        """计算面积"""
        pass
    
    def perimeter(self):
        """计算周长"""
        pass

class Circle(Shape):
    """圆形类"""
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * pi * self.radius

class Rectangle(Shape):
    """矩形类"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# 测试多态
def print_shape_info(shape):
    """打印图形信息"""
    print(f"面积：{shape.area():.2f}")
    print(f"周长：{shape.perimeter():.2f}")

circle = Circle(5)
rectangle = Rectangle(4, 6)

print("圆形信息：")
print_shape_info(circle)
print("\n矩形信息：")
print_shape_info(rectangle)

# 5. 类方法和静态方法
print("\n5. 类方法和静态方法示例")
print("-"*30)

# 5.1 日期类
print("5.1 日期类：")
class Date:
    """日期类"""
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        """从字符串创建日期对象"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @staticmethod
    def is_valid_date(date_string):
        """验证日期字符串格式"""
        try:
            year, month, day = map(int, date_string.split('-'))
            return 1 <= month <= 12 and 1 <= day <= 31
        except:
            return False
    
    def __str__(self):
        return f"{self.year}年{self.month}月{self.day}日"

# 测试日期类
print(f"2023-5-1 是否是有效日期：{Date.is_valid_date('2023-5-1')}")
date = Date.from_string('2023-5-1')
print(f"创建的日期：{date}")

# 6. 属性装饰器
print("\n6. 属性装饰器���例")
print("-"*30)

# 6.1 温度转换类
print("6.1 温度转换类：")
class Temperature:
    """温度类"""
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度！")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """华氏度"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# 测试温度类
temp = Temperature(25)
print(f"摄氏度：{temp.celsius}°C")
print(f"华氏度：{temp.fahrenheit}°F")
temp.fahrenheit = 100
print(f"转换后的摄氏度：{temp.celsius:.2f}°C")

# 7. 综合示例
print("\n7. 综合示例")
print("-"*30)

# 7.1 图书管理系统
print("7.1 简单图书管理系统：")
class Book:
    """图书类"""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
    
    def __str__(self):
        status = "已借出" if self.is_borrowed else "可借��"
        return f"《{self.title}》 作者：{self.author} [{status}]"

class Library:
    """图书馆类"""
    def __init__(self, name):
        self.name = name
        self.books = {}
    
    def add_book(self, book):
        """添加图书"""
        self.books[book.isbn] = book
        return f"《{book.title}》已添加到{self.name}"
    
    def borrow_book(self, isbn):
        """借书"""
        if isbn in self.books:
            book = self.books[isbn]
            if not book.is_borrowed:
                book.is_borrowed = True
                return f"《{book.title}》借阅成功！"
            return f"《{book.title}》已被借出"
        return "未找到该图书"
    
    def return_book(self, isbn):
        """还书"""
        if isbn in self.books:
            book = self.books[isbn]
            if book.is_borrowed:
                book.is_borrowed = False
                return f"《{book.title}》已归还，谢谢！"
            return f"《{book.title}》未被借出"
        return "未找到该图书"
    
    def list_books(self):
        """列出所有图书"""
        return "\n".join(str(book) for book in self.books.values())

# 测试图书管理系统
library = Library("快乐图书馆")
book1 = Book("Python编程", "张三", "001")
book2 = Book("数据结构", "李四", "002")

print(library.add_book(book1))
print(library.add_book(book2))
print("\n所有图书：")
print(library.list_books())
print("\n借书测试：")
print(library.borrow_book("001"))
print("\n当前图书状态：")
print(library.list_books())
print("\n还书测试：")
print(library.return_book("001"))

print("\n恭喜！你已经掌握了Python的面向对象编程！")
print("记住：好的类设计能让代码更有组织、更易扩展！") 