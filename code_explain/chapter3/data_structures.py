#!/usr/bin/env python3
"""
第3章：Python数据结构
通过生动有趣的例子学习Python的数据结构
"""

print("="*50)
print("欢迎来到Python数据结构教程！")
print("="*50)

# 1. 列表（List）
print("\n1. 列表示例")
print("-"*30)

# 1.1 文具盒示例
print("1.1 文具盒管理：")
stationery = ["铅笔", "钢笔", "橡皮", "尺子"]
print(f"文具盒里现在有：{stationery}")

# 添加新文具
stationery.append("圆珠笔")
print(f"添加圆珠笔后：{stationery}")

# 在特定位置插入
stationery.insert(1, "记号笔")
print(f"在第二个位置插入记号笔后：{stationery}")

# 删除文具
removed_item = stationery.pop()
print(f"拿出了：{removed_item}")
print(f"现在文具盒里有：{stationery}")

# 2. 元组（Tuple）
print("\n2. 元组示例")
print("-"*30)

# 2.1 文具套装示例
print("2.1 文具套装：")
basic_set = ("铅笔", "钢笔", "橡皮")
print(f"基础文具套装包含：{basic_set}")

# 2.2 坐标点示例
print("\n2.2 坐标点：")
point = (3, 4)
x, y = point  # 解包
print(f"点的坐标：({x}, {y})")
distance = (x**2 + y**2)**0.5
print(f"到原点的距离：{distance}")

# 3. 字典（Dictionary）
print("\n3. 字典示例")
print("-"*30)

# 3.1 学生信息管理
print("3.1 学生信息管理：")
student = {
    "name": "小明",
    "age": 15,
    "grade": "初三",
    "hobbies": ["足球", "画画"]
}

print(f"学生姓名：{student['name']}")
print(f"学生年龄：{student['age']}")
print(f"爱好：{', '.join(student['hobbies'])}")

# 修改信息
student["age"] = 16
print(f"修改后的年龄：{student['age']}")

# 添加新信息
student["phone"] = "123-4567"
print(f"添加联系电话：{student['phone']}")

# 安全地获取信息
email = student.get("email", "未登记")
print(f"电子邮箱：{email}")

# 4. 集合（Set）
print("\n4. 集合示例")
print("-"*30)

# 4.1 水果收藏
print("4.1 水果收藏比较：")
ming_fruits = {"苹果", "香蕉", "橙子"}
hong_fruits = {"香蕉", "葡萄", "橙子"}

print(f"小明的水果：{ming_fruits}")
print(f"小红的水果：{hong_fruits}")

# 共同喜欢的水果
common_fruits = ming_fruits & hong_fruits
print(f"共同喜欢的水果：{common_fruits}")

# 所有不重复的水果
all_fruits = ming_fruits | hong_fruits
print(f"所有水果：{all_fruits}")

# 5. 数据序列化
print("\n5. 数据序列化示例")
print("-"*30)

# 5.1 JSON处理
print("5.1 JSON处理：")
import json

student_info = {
    "name": "小明",
    "age": 15,
    "scores": [90, 85, 88]
}

# 转换成JSON字符串
json_str = json.dumps(student_info, ensure_ascii=False)
print(f"JSON字符串：{json_str}")

# 转回Python对象
data = json.loads(json_str)
print(f"Python对象：{data}")

# 5.2 YAML处理
print("\n5.2 YAML处理：")
import yaml

config = {
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "settings": {
        "debug": True,
        "theme": "dark"
    }
}

# 转换成YAML
yaml_str = yaml.dump(config)
print("YAML格式：")
print(yaml_str)

# 6. 综合练习
print("\n6. 综合练习")
print("-"*30)

# 6.1 购物清单管理器
print("6.1 购物清单管理器：")
shopping_list = []

def add_item(item, quantity):
    """添加商品到购物清单"""
    shopping_list.append({
        "item": item,
        "quantity": quantity
    })
    print(f"添加了 {quantity} 个 {item}")

add_item("苹果", 5)
add_item("面包", 2)

print("\n购物清单：")
for item in shopping_list:
    print(f"- {item['item']}: {item['quantity']}个")

# 6.2 学生成绩管理
print("\n6.2 学生成绩管理：")
grades = {
    "小明": {"语文": 85, "数学": 92, "英语": 78},
    "小红": {"语文": 88, "数学": 95, "英语": 90}
}

def calculate_average(student_name):
    """计算学生平均分"""
    scores = grades[student_name].values()
    return sum(scores) / len(scores)

for student in grades:
    average = calculate_average(student)
    print(f"{student}的平均分是：{average:.2f}")

print("\n恭喜！你已经掌握了Python的数据结构！")
print("记住：选择合适的数据结构可以让程序更高效！") 