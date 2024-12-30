#!/usr/bin/env python3
"""
第7章：Python文件和数据处理
通过生动有趣的例子学习Python的文件操作和数据处理
"""

print("="*50)
print("欢迎来到Python文件和数据处理教程！")
print("="*50)

# 1. 基本文件操作
print("\n1. 基本文件操作示例")
print("-"*30)

# 1.1 写入和读取文本文件
print("1.1 写入和读取文本文件：")

# 写入文件
def write_diary():
    """写日记示例"""
    print("写入日记...")
    with open("diary.txt", "w", encoding="utf-8") as f:
        f.write("亲爱的日记：\n")
        f.write("今天是个好天气！\n")
        f.write("我学会了Python的文件操作！\n")

# 读取文件
def read_diary():
    """读取日记示例"""
    print("\n读取日记...")
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("找不到日记文件！")

# 测试日记操作
write_diary()
read_diary()

# 1.2 逐行读取
print("\n1.2 逐行读取示例：")
def read_diary_lines():
    """逐行读取示例"""
    print("逐行读取日记...")
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                print(f"第{line_number}行：{line.strip()}")
    except FileNotFoundError:
        print("找不到日记文件！")

read_diary_lines()

# 2. CSV文件处理
print("\n2. CSV文件处理示例")
print("-"*30)

# 2.1 写入和读取CSV
print("2.1 学生成绩管理：")
import csv

# 写入CSV
def save_grades():
    """保存学生成绩"""
    print("保存学生成绩...")
    grades = [
        ["姓名", "语文", "数学", "英语"],
        ["小明", 95, 92, 88],
        ["小红", 88, 95, 90],
        ["小华", 82, 89, 85]
    ]
    
    with open("grades.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(grades)

# 读取CSV
def read_grades():
    """读取学生成绩"""
    print("\n读取学生成绩...")
    try:
        with open("grades.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(" | ".join(str(cell) for cell in row))
    except FileNotFoundError:
        print("找不到成绩文件！")

# 测试成绩管理
save_grades()
read_grades()

# 3. JSON数据处理
print("\n3. JSON数据处理示例")
print("-"*30)

# 3.1 处理JSON数据
print("3.1 图书管理系统：")
import json

class Book:
    """图书类"""
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
    
    def to_dict(self):
        """转换为字典"""
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            data["title"],
            data["author"],
            data["price"]
        )

# 保存图书信息
def save_books():
    """保存图书信息到JSON文件"""
    print("保存图书信息...")
    books = [
        Book("Python入门", "张三", 59.9),
        Book("数据分析", "李四", 79.9),
        Book("机器学习", "王五", 89.9)
    ]
    
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(
            [book.to_dict() for book in books],
            f,
            ensure_ascii=False,
            indent=2
        )

# 读取图书信息
def load_books():
    """从JSON文件读取图书信息"""
    print("\n读取图书信息...")
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            books = [Book.from_dict(item) for item in data]
            
            for book in books:
                print(f"《{book.title}》 作者：{book.author} 价格：{book.price}元")
    
    except FileNotFoundError:
        print("找不到图书文件！")

# 测试图书管理
save_books()
load_books()

# 4. 二进制文件处理
print("\n4. 二进制文件处理示例")
print("-"*30)

# 4.1 图片文件复制
print("4.1 图片文件复制：")
def copy_image(source, target):
    """复制图片文件"""
    try:
        # 读取图片
        with open(source, "rb") as f:
            data = f.read()
        
        # 写入副本
        with open(target, "wb") as f:
            f.write(data)
        
        print(f"成功将图片从 {source} 复制到 {target}")
    
    except FileNotFoundError:
        print(f"找不到文件：{source}")
    except Exception as e:
        print(f"复制文件时出错：{str(e)}")

# 注释掉实际的图片复制操作，因为示例环境中可能没有图片文件
# copy_image("original.jpg", "copy.jpg")

# 5. 文件和目录操作
print("\n5. 文件和目录操作示例")
print("-"*30)

# 5.1 文件管理器
print("5.1 简单文件管理器：")
import os
import shutil
from datetime import datetime

class FileManager:
    """文件管理器"""
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
    
    def list_files(self):
        """列出文件和目录"""
        print(f"\n当前目录 {self.root_dir} 的内容：")
        try:
            for item in os.listdir(self.root_dir):
                path = os.path.join(self.root_dir, item)
                stats = os.stat(path)
                size = stats.st_size
                modified = datetime.fromtimestamp(stats.st_mtime)
                item_type = "文件夹" if os.path.isdir(path) else "文件"
                
                print(f"{item:20} | {item_type:6} | "
                      f"{size:8,d}字节 | {modified}")
        
        except Exception as e:
            print(f"列出目录内容时出错：{str(e)}")
    
    def create_directory(self, name):
        """创建目录"""
        path = os.path.join(self.root_dir, name)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"成功创建目录：{name}")
        except Exception as e:
            print(f"创建目录时出错：{str(e)}")
    
    def delete_item(self, name):
        """删除文件或目录"""
        path = os.path.join(self.root_dir, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"成功删除目录：{name}")
            else:
                os.remove(path)
                print(f"成功删除文件：{name}")
        except Exception as e:
            print(f"删除时出错：{str(e)}")

# 测试文件管理器
manager = FileManager()

print("创建测试目录...")
manager.create_directory("test_folder")

print("\n列出当前目录内容...")
manager.list_files()

print("\n删除测试目录...")
manager.delete_item("test_folder")

# 6. 数据处理实用工具
print("\n6. 数据处理实用工具示例")
print("-"*30)

# 6.1 文本分析器
print("6.1 文本分析器：")
class TextAnalyzer:
    """文本分析器"""
    def __init__(self, text):
        self.text = text
    
    def count_words(self):
        """统计词频"""
        words = self.text.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        return word_count
    
    def get_statistics(self):
        """获取文本统计信息"""
        lines = self.text.split("\n")
        words = self.text.split()
        chars = len(self.text)
        
        return {
            "行数": len(lines),
            "词数": len(words),
            "字符数": chars
        }

# 测试文本分析器
sample_text = """Python是一种很棒的编程语言，
Python简单易学，
Python功能强大！"""

analyzer = TextAnalyzer(sample_text)

print("文本统计信息：")
for key, value in analyzer.get_statistics().items():
    print(f"{key}: {value}")

print("\n词频统计：")
for word, count in analyzer.count_words().items():
    print(f"'{word}': {count}次")

print("\n恭喜！你已经掌握了Python的文件和数据处理！")
print("记住：文件操作要注意异常处理，数据处理要选择合适的格式！") 