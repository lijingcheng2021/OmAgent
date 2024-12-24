import os
from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.cli.client import DefaultClient
from omagent_core.utils.logger import logging
from agent.input_interface.input_interface import InputInterface
from omagent_core.advanced_components.workflow.react.workflow import ReactWorkflow
from omagent_core.engine.workflow.task.switch_task import SwitchTask

logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = Path(__file__).parents[0]

# Load container configuration
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# Initialize workflow
workflow = ConductorWorkflow(name='react_example')

# Configure workflow tasks
input_task = simple_task(
    task_def_name=InputInterface, 
    task_reference_name='input_interface'
)

react_workflow = ReactWorkflow()
react_workflow.set_input(query=input_task.output('query'))

# Configure workflow execution flow
workflow >> input_task >> react_workflow

# Register workflow
workflow.register(overwrite=True)

# Initialize and start CLI client
config_path = CURRENT_PATH.joinpath('configs')
cli_client = DefaultClient(
    interactor=workflow,
    config_path=config_path,
    workers=[InputInterface()]
)
cli_client.start_interactor()
