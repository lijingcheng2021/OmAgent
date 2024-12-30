# Python控制流

欢迎来到Python控制流的学习！想象你在玩一个冒险游戏，需要根据不同的情况做出不同的选择，这就是"控制流"。

## 1. 条件语句（if-elif-else）

### 1.1 什么是条件语句？
想象你是一个门卫，要根据不同的情况做出不同的决定：
```python
# 检查年龄是否可以进入游乐场
age = 12

if age < 6:
    print("年龄太小了，不能玩刺激的游乐设施")
elif age < 18:
    print("可以玩一般的游乐设施，但不能玩太刺激的")
else:
    print("可以玩所有游乐设施")
```

### 1.2 条件组合
就像检查多个条件：
```python
# 判断能否参加比赛
age = 15
height = 170
weight = 55

if age >= 14 and height >= 160:
    if weight >= 50:
        print("可以参加比赛")
    else:
        print("体重不够，不能参加")
else:
    print("年龄或身高不够，不能参加")
```

## 2. 循环语句

### 2.1 for循环
想象你在点名或数数：
```python
# 点名
students = ["小明", "小红", "小华"]
for student in students:
    print(f"{student}，到！")

# 数数
for i in range(1, 6):  # 从1数到5
    print(f"数到{i}")
```

### 2.2 while循环
想象你在玩游戏，不断尝试直到成功：
```python
# 猜数字游戏
import random
secret = random.randint(1, 10)
tries = 0

while tries < 3:
    guess = int(input("猜一个1到10之间的数："))
    tries += 1
    
    if guess == secret:
        print("猜对了！")
        break
    else:
        print("猜错了，再试试")
```

## 3. 异常处理

### 3.1 try-except
就像带着安全气囊开车，即使出错也不会受伤：
```python
# 安全地转换用户输入
try:
    age = int(input("请输入你的年龄："))
    print(f"明年你{age + 1}岁了")
except ValueError:
    print("抱歉，请输入一个有效的数字")
```

### 3.2 try-except-else-finally
像游戏的完整流程：开始、进行、成功、结束
```python
try:
    # 尝试打开文件（开始）
    file = open("scores.txt")
    score = int(file.read())
except FileNotFoundError:
    # 处理文件不存在的情况
    print("找不到成绩单")
except ValueError:
    # 处理数据格式错误
    print("成绩格式不对")
else:
    # 成功读取后的操作
    print(f"你的成绩是：{score}")
finally:
    # 最后一定要做的事（结束）
    print("成绩查询完毕")
```

## 4. 上下文管理（with语句）

就像进出图书馆：自动帮你开门、关门
```python
# 读写文件更安全的方式
with open("diary.txt", "w") as diary:
    diary.write("今天天气真好！")
# 文件会自动关闭，不用担心忘记关闭

# 多个上下文，就像同时开多个门
with open("in.txt") as source, open("out.txt", "w") as target:
    content = source.read()
    target.write(content.upper())
```

## 5. 练习题

1. 小明的成绩单：
```python
score = 85
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 60:
    grade = "及格"
else:
    grade = "需要努力"
print(f"小明的成绩是{score}分，等级是{grade}")
```

2. 购物车计算：
```python
cart = ["苹果", "香蕉", "橙子"]
prices = {"苹果": 5, "香蕉": 3, "橙子": 4}
total = 0

for item in cart:
    total += prices[item]
    print(f"添加{item}，价格{prices[item]}元")

print(f"总价：{total}元")
```

## 6. 小贴士
1. 条件语句要注意缩进，这是Python的特色
2. 循环时要小心无限循环，记得设置退出条件
3. 处理异常时要具体到特定的异常类型
4. 使用with语句处理文件更安全

## 7. 下一步
- 试着写一个小游戏，结合条件和循环
- 处理文件时多用with语句
- 记住：编程就像玩游戏，多练习才能熟练！ 