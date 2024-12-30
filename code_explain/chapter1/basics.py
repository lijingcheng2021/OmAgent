#!/usr/bin/env python3
"""
第1章：Python基础知识
通过生动有趣的例子学习Python基础
"""

print("="*50)
print("欢迎来到Python基础教程！")
print("="*50)

# 1. 变量和数据类型
print("\n1. 变量和数据类型示例")
print("-"*30)

# 1.1 变量的基本使用
print("1.1 变量就像带标签的盒子：")
# 创建一个装着数字5的盒子，标签是"age"
age = 5
print(f"盒子里原来的数字是: {age}")

# 往盒子里放入新的数字
age = 6
print(f"盒子里现在的数字是: {age}")

# 1.2 不同的数据类型
print("\n1.2 不同类型的数据：")

# 整数（想象是你的年龄）
student_age = 18
print(f"小明今年 {student_age} 岁")

# 浮点数（想象是你的身高体重）
height = 1.75
weight = 68.5
print(f"小明身高 {height} 米，体重 {weight} 公斤")

# 字符串（想象是你的名字）
name = "小明"
greeting = '你好，世界！'
print(f"我叫{name}，想对你说：{greeting}")

# 布尔值（想象是开关）
is_student = True
is_teacher = False
print(f"小明是学生吗？{is_student}")
print(f"小明是老师吗？{is_teacher}")

# 1.3 类型转换
print("\n1.3 类型转换示例：")
# 字符串转数字
age_str = "25"
age_num = int(age_str)
print(f"把字符串 '{age_str}' 转换成数字: {age_num}")

# 数字转字符串
num = 25
num_str = str(num)
print(f"把数字 {num} 转换成字符串: '{num_str}'")

# 2. 基本运算符
print("\n2. 基本运算符示例")
print("-"*30)

# 2.1 算术运算符
print("2.1 算术运算符（想象买苹果）：")
# 买苹果
apples = 3 + 2
print(f"买了3个苹果，又买了2个，总共有{apples}个苹果")

# 吃掉苹果
remaining = 5 - 1
print(f"吃掉1个苹果，还剩{remaining}个")

# 买多份
total = 3 * 4
print(f"买了3份，每份4个苹果，总共有{total}个苹果")

# 分苹果
each = 10 / 2
print(f"10个苹果分给2个人，每人{each}个")

# 2.2 比较运算符
print("\n2.2 比较运算符（想象比较大小）：")
# 比身高
is_taller = 180 > 170
print(f"180厘米比170厘米高吗？{is_taller}")

# 比年龄
is_same_age = 25 == 25
print(f"都是25岁，年龄相同吗？{is_same_age}")

# 比分数
is_different = 90 != 85
print(f"90分和85分不一样吗？{is_different}")

# 3. 输入输出
print("\n3. 输入输出示例")
print("-"*30)

# 3.1 基本输出
print("3.1 基本输出（想象说话）：")
print("你好！")
name = "小明"
age = 18
print(f"{name}今年{age}岁了")

# 3.2 获取用户输入
print("\n3.2 获取用户输入（想象对话）：")
# 注意：input()会暂停程序等待用户输入

# 问对方名字
your_name = input("你叫什么名字？")
print(f"你好，{your_name}！")

# 问对方年龄
your_age_str = input("你今年多大了？")
your_age = int(your_age_str)
print(f"原来你{your_age}岁啊！")

# 4. 实践练习
print("\n4. 实践练习")
print("-"*30)

# 4.1 小明的零花钱
print("4.1 小明的零花钱：")
money = 100
toy_price = 30
remaining = money - toy_price
print(f"小明有{money}元零花钱")
print(f"买了一个{toy_price}元的玩具")
print(f"还剩{remaining}元")

# 4.2 温度转换器
print("\n4.2 温度转换器：")
celsius = float(input("请输入摄氏度："))
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}摄氏度 = {fahrenheit}华氏度")

print("\n恭喜！你已经完成了Python基础的学习！")
print("记住：多练习，多思考，编程的乐趣就在其中！") 