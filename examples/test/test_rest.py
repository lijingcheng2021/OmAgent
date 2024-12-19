# 安装: pip install redis
import redis

# 1. 连接到Redis
redis_client = redis.Redis(
    host='140.207.201.47',  # Redis服务器地址
    port=6379         # Redis端口
)

# 2. 存储数据
redis_client.set('user:1:name', 'Alice')  # 像字典一样存储
redis_client.set('user:1:age', '25')

# 3. 读取数据
name = redis_client.get('user:1:name')  # 获取值
print(f"名字是: {name.decode('utf-8')}")  # 输出: 名字是: Alice

age = redis_client.get('user:1:age')
print(f"年龄是: {age.decode('utf-8')}")   # 输出: 年龄是: 25
