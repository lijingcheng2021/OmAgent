import requests
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conductor服务器地址
URL = "http://140.207.201.47:8080/api"

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
logger.info("正在注册工作流...")
response = requests.post(f"{URL}/metadata/workflow", json=workflow)
logger.info(f"注册状态: {response.status_code}")

# 3. 运行工作流
logger.info("开始执行工作流...")
response = requests.post(
    f"{URL}/workflow", 
    json={
        "name": "hello_workflow",
        "version": 1,
        "input": {}
    }
)
workflow_id = response.text
logger.info(f"工作流ID: {workflow_id}")

# 4. 查看状态
logger.info("等待工作完成...")
for _ in range(5):  # 只检查5次
    response = requests.get(f"{URL}/workflow/{workflow_id}")
    if response.status_code == 200:
        data = response.json()
        status = data["status"]
        logger.info(f"工作流状态: {status}")
        
        # 打印任务状态
        for task in data.get('tasks', []):
            logger.info(f"任务 [{task['taskDefName']}] 状态: {task['status']}")
    
    time.sleep(1)  # 等待1秒
