import os

# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'http://10.8.21.200:47890'
os.environ['HTTPS_PROXY'] = 'http://10.8.21.200:47890'

from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.programmatic.client import ProgrammaticClient
from omagent_core.utils.logger import logging
from agent.input_interface.input_interface import InputInterface
from omagent_core.advanced_components.workflow.react.workflow import ReactWorkflow
import json

def process_results(res, dataset_name="react_test"):
    return {
        "dataset": dataset_name,
        "results": res
    }

logging.init_logger("omagent", "omagent", level="INFO")

# 设置当前工作目录路径
CURRENT_PATH = Path(__file__).parents[0]

# 导入注册的模块
registry.import_module(CURRENT_PATH.joinpath('agent'))

# 加载 container 配置从 YAML 文件
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# 初始化工作流
workflow = ConductorWorkflow(name='react_example')

# 配置 React 工作流
react_workflow = ReactWorkflow()
react_workflow.set_input(query=workflow.input('query'))

# 配置工作流执行流程
workflow >> react_workflow

# 注册工作流
workflow.register(overwrite=True)

# 从文件读取输入文本
def read_input_texts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# 使用示例
input_file = "/home/li_jingcheng/项目/OmAgent/question.txt"
input_texts = read_input_texts(input_file)

workflow_input_list = [
    {"query": text} for text in input_texts
]

# 初始化并启动 programmatic client
config_path = CURRENT_PATH.joinpath('configs')
programmatic_client = ProgrammaticClient(
    processor=workflow,
    config_path=config_path,
    workers=[]  # React workflow 不需要额外的 workers
)

print(f"Starting batch processing for {len(workflow_input_list)} queries...")
res = programmatic_client.start_batch_processor(
    workflow_input_list=workflow_input_list
)
print("Batch processing completed")

programmatic_client.stop_processor()

# 处理并保存结果
print("Processing and saving results...")
results = process_results(res)
output_path = CURRENT_PATH.joinpath("output/results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"Results saved in {output_path}") 