import os

# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'http://10.8.21.200:47890'
os.environ['HTTPS_PROXY'] = 'http://10.8.21.200:47890'

from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.cli.client import DefaultClient
from omagent_core.utils.logger import logging
from omagent_core.advanced_components.workflow.react.workflow import ReactWorkflow
from agent.input_interface.input_interface import InputInterface

logging.init_logger("omagent", "omagent", level="INFO")

# 设置当前工作目录路径
CURRENT_PATH = Path(__file__).parents[0]

# 导入注册的模块
registry.import_module(CURRENT_PATH.joinpath('agent'))

# 加载 container 配置从 YAML 文件
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# 初始化工作流
workflow = ConductorWorkflow(name='react_basic_workflow_example')

# 配置输入任务
input_task = simple_task(
    task_def_name=InputInterface,
    task_reference_name='input_interface'
)

# 配置 React Basic 工作流
react_workflow = ReactWorkflow()
react_workflow.set_input(
    query=input_task.output('query'),
    id=input_task.output('id'),
    example=input_task.output('example'),
    max_turns=input_task.output('max_turns')
)

# 配置工作流执行流程
workflow >> input_task >> react_workflow 

# 注册工作流
workflow.register(overwrite=True)

# 初始化并启动 CLI client
config_path = CURRENT_PATH.joinpath('configs')
cli_client = DefaultClient(
    interactor=workflow, config_path=config_path, workers=[InputInterface()]
)

# 启动CLI客户端
cli_client.start_interactor()

#毛泽东的出生日期