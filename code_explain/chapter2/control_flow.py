#!/usr/bin/env python3
"""
第2章：Python控制流
通过生动有趣的例子学习Python的控制流程
"""

print("="*50)
print("欢迎来到Python控制流教程！")
print("="*50)

# 1. 条件语句
print("\n1. 条件语句示例")
print("-"*30)

# 1.1 简单的if-elif-else
print("1.1 游乐园门票检查：")
age = int(input("请输入你的年龄："))

if age < 6:
    print("年龄太小了，不能玩刺激的游乐设施")
    ticket_price = 0
elif age < 18:
    print("可以玩一般的游乐设施，但不能玩太刺激的")
    ticket_price = 25
else:
    print("可以玩所有游乐设施")
    ticket_price = 50

print(f"门票价格：{ticket_price}元")

# 1.2 复杂条件判断
print("\n1.2 运动会参赛资格：")
height = float(input("请输入你的身高(米)："))
weight = float(input("请输入你的体重(公斤)："))

if height >= 1.6:
    if weight >= 50 and weight <= 80:
        print("恭喜！你符合参赛条件")
    else:
        print("体重不在要求范围内")
else:
    print("身高不够，继续加油！")

# 2. 循环语句
print("\n2. 循环语句示例")
print("-"*30)

# 2.1 for循环
print("2.1 班级点名：")
students = ["小明", "小红", "小华", "小李", "小张"]
for student in students:
    print(f"{student}，到！")

print("\n2.2 倒计时：")
print("比赛即将开始...")
for i in range(5, 0, -1):
    print(f"{i}!")
print("开始！")

# 2.3 while循环
print("\n2.3 猜数字游戏：")
import random
secret = random.randint(1, 10)
tries = 0
max_tries = 3

print(f"我想了一个1到10之间的数，你有{max_tries}次机会猜！")

while tries < max_tries:
    guess = int(input("你猜是几？"))
    tries += 1
    
    if guess == secret:
        print(f"太棒了！你用了{tries}次就猜对了！")
        break
    elif guess < secret:
        print("猜小了~")
    else:
        print("猜大了~")
    
    if tries < max_tries:
        print(f"还有{max_tries - tries}次机会")
    else:
        print(f"游戏结束，正确答案是{secret}")

# 3. 异常处理
print("\n3. 异常处理示例")
print("-"*30)

# 3.1 基本的try-except
print("3.1 安全的除法计算器：")
try:
    num1 = int(input("请输入第一个数："))
    num2 = int(input("请输入第二个数："))
    result = num1 / num2
    print(f"{num1} ÷ {num2} = {result}")
except ValueError:
    print("请输入有效的数字！")
except ZeroDivisionError:
    print("除数不能为0！")
except Exception as e:
    print(f"出现错误：{e}")

# 3.2 文件操作的异常处理
print("\n3.2 安全的文件操作：")
try:
    with open("diary.txt", "w") as f:
        f.write("今天学习了Python的控制流，很有趣！")
    print("日记保存成功！")
    
    with open("diary.txt", "r") as f:
        content = f.read()
        print(f"日记内容：{content}")
except FileNotFoundError:
    print("找不到文件！")
except PermissionError:
    print("没有权限操作文件！")
finally:
    print("文件操作完成。")

# 4. 综合练习
print("\n4. 综合练习")
print("-"*30)

# 4.1 购物系统
print("4.1 简单购物系统：")
items = {
    "苹果": 5,
    "香蕉": 3,
    "橙子": 4,
    "西瓜": 15
}

cart = []
total = 0

print("欢迎来到水果店！")
print("商品列表：")
for item, price in items.items():
    print(f"{item}: {price}元")

while True:
    choice = input("\n请输入要买的水果（输入'结算'完成购物）：")
    if choice == "结算":
        break
    
    if choice in items:
        cart.append(choice)
        total += items[choice]
        print(f"已添加{choice}到购物车")
    else:
        print("没有这个商品！")

print("\n购物清单：")
for item in cart:
    print(f"- {item}: {items[item]}元")
print(f"总计：{total}元")

print("\n恭喜！你已经掌握了Python的控制流！")
print("记住：多练习，多思考，编程的乐趣就在其中！") 