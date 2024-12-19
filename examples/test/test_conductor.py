import requests

# Conductor服务器地址
URL = "http://140.207.201.47:8080/api"

# 0. 先检查服务器是否正常
try:
    health = requests.get(f"{URL}/health")
    print(f"服务器状态: {health.status_code}")
except Exception as e:
    print(f"无法连接到服务器: {e}")
    exit(1)

# 1. 定义最简单的工作流
workflow = {
    "name": "hello_workflow",
    "version": 1,
    "schemaVersion": 2,
    "ownerEmail": "test@example.com",
    "tasks": [
        {
            "name": "hello_task",
            "taskReferenceName": "hello_ref",
            "type": "SIMPLE",
            "inputParameters": {}
        }
    ]
}

# 2. 注册工作流
response = requests.post(f"{URL}/metadata/workflow", json=workflow)
print(f"注册状态: {response.status_code}")
print(f"注册响应: {response.text}")  # 打印详细错误信息

if response.status_code != 200:
    print("工作流注册失败，退出程序")
    exit(1)

# 3. 运行工作流
response = requests.post(f"{URL}/workflow", 
    json={"name": "hello_workflow", "version": 1})
workflow_id = response.text
print(f"工作流ID: {workflow_id}")

# 4. 查看状态
response = requests.get(f"{URL}/workflow/{workflow_id}")
if response.status_code == 200:
    status = response.json()["status"]
    print(f"工作流状态: {status}")
else:
    print(f"获取状态失败: {response.text}")
