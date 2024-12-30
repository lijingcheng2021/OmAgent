#!/usr/bin/env python3
"""
第8章：Python网络编程和Web开发
通过生动有趣的例子学习Python的网络编程和Web开发
"""

print("="*50)
print("欢迎来到Python网络编程和Web开发教程！")
print("="*50)

# 1. 基本网络编程
print("\n1. 基本网络编程示例")
print("-"*30)

# 1.1 TCP服务器和客户端
print("1.1 简单聊天室：")
import socket
import threading
import time

class ChatServer:
    """聊天服务器"""
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
    
    def start(self):
        """启动服务器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"服务器启动在 {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"新客户端连接：{address}")
            self.clients.append(client_socket)
            
            # 为���个客户端创建一个线程
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            client_thread.start()
    
    def handle_client(self, client_socket):
        """处理客户端连接"""
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                print(f"收到消息：{message}")
                # 广播消息给所有客户端
                self.broadcast(message, client_socket)
        
        except Exception as e:
            print(f"处理客户端时出错：{str(e)}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
    
    def broadcast(self, message, sender_socket):
        """广播消息给所有其他客户端"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.clients.remove(client)

class ChatClient:
    """聊天客户端"""
    def __init__(self, host='localhost', port=9999):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
    
    def send_message(self, message):
        """发送消息"""
        self.socket.send(message.encode('utf-8'))
    
    def receive_messages(self):
        """接收消息"""
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"收到：{message}")
            except:
                break

# 注释掉实际运行的代码，因为需要在不同的进程中运行服务器和客户端
"""
# 运行服务器
server = ChatServer()
server.start()

# 运行客户端
client = ChatClient()
receive_thread = threading.Thread(target=client.receive_messages)
receive_thread.start()

# 发送消息
client.send_message("你好！")
"""

# 2. HTTP客户端
print("\n2. HTTP客户端示例")
print("-"*30)

# 2.1 使用requests库
print("2.1 天气查询器：")
import requests

class WeatherChecker:
    """天气查询器"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """获取城市天气"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_cn'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                '城市': data['name'],
                '温度': f"{data['main']['temp']}°C",
                '天气': data['weather'][0]['description'],
                '湿度': f"{data['main']['humidity']}%"
            }
        
        except requests.RequestException as e:
            return f"获取天气信息失败：{str(e)}"

# 注释掉实际API调用，因为需要API密钥
"""
weather = WeatherChecker('your_api_key')
result = weather.get_weather('Beijing')
print(result)
"""

# 3. Web服务器
print("\n3. Web服务器示例")
print("-"*30)

# 3.1 使用Flask框架
print("3.1 简单博客系统：")
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据库
blog_posts = []

@app.route('/posts', methods=['GET'])
def get_posts():
    """获取所有博客文章"""
    return jsonify(blog_posts)

@app.route('/posts', methods=['POST'])
def create_post():
    """创建新文章"""
    data = request.get_json()
    post = {
        'id': len(blog_posts) + 1,
        'title': data.get('title'),
        'content': data.get('content'),
        'author': data.get('author'),
        'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    blog_posts.append(post)
    return jsonify(post), 201

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取特定文章"""
    post = next(
        (post for post in blog_posts if post['id'] == post_id),
        None
    )
    if post is None:
        return jsonify({'error': '文章不存在'}), 404
    return jsonify(post)

# 注释掉实际运行的代码
"""
if __name__ == '__main__':
    app.run(debug=True)
"""

# 4. WebSocket示例
print("\n4. WebSocket示例")
print("-"*30)

# 4.1 实时聊天室
print("4.1 WebSocket聊天室：")
from websockets import serve
import asyncio
import json

class ChatRoom:
    """WebSocket聊天室"""
    def __init__(self):
        self.clients = set()
    
    async def register(self, websocket):
        """注册新客户端"""
        self.clients.add(websocket)
        await self.notify_all({"type": "system", "message": "新用户加入聊天室"})
    
    async def unregister(self, websocket):
        """注销客户端"""
        self.clients.remove(websocket)
        await self.notify_all({"type": "system", "message": "用户离开聊天室"})
    
    async def notify_all(self, message):
        """向所有客户端发送消息"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients]
            )
    
    async def handle_message(self, websocket, message):
        """处理收到的消息"""
        data = json.loads(message)
        await self.notify_all({
            "type": "chat",
            "user": data.get("user", "匿名"),
            "message": data.get("message", "")
        })

# 注释掉实际运行的代码
"""
chat_room = ChatRoom()

async def chat_server(websocket, path):
    await chat_room.register(websocket)
    try:
        async for message in websocket:
            await chat_room.handle_message(websocket, message)
    finally:
        await chat_room.unregister(websocket)

async def main():
    async with serve(chat_server, "localhost", 8765):
        await asyncio.Future()  # 运行永不结束

asyncio.run(main())
"""

# 5. 网络安全
print("\n5. 网络安全示例")
print("-"*30)

# 5.1 安全通信
print("5.1 加密通信：")
from cryptography.fernet import Fernet

class SecureCommunication:
    """安全通信示例"""
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_message(self, message):
        """加密消息"""
        return self.cipher_suite.encrypt(message.encode())
    
    def decrypt_message(self, encrypted_message):
        """解密消息"""
        return self.cipher_suite.decrypt(encrypted_message).decode()

# 测试安全通信
secure_comm = SecureCommunication()
message = "这是一条机密消息！"
print(f"原始消息：{message}")

encrypted = secure_comm.encrypt_message(message)
print(f"加密后：{encrypted}")

decrypted = secure_comm.decrypt_message(encrypted)
print(f"解密后：{decrypted}")

print("\n恭喜！你已经掌握了Python的网络编程和Web开发！")
print("记住：网络编程要注意安全性，Web开发要关注用户体验！") 