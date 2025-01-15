import os
os.environ["custom_openai_key"] = "notneeded"
os.environ["custom_openai_endpoint"] = "http://140.207.201.47:11434/v1"
os.environ['HTTP_PROXY'] = 'http://10.8.21.200:47890'
os.environ['HTTPS_PROXY'] = 'http://10.8.21.200:47890'

from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.lite_version.cli import DefaultClient
from omagent_core.utils.logger import logging
from omagent_core.advanced_components.workflow.react_pro.workflow import ReactProWorkflow
from omagent_core.engine.worker.base import BaseWorker

@registry.register_worker()
class SimpleInput(BaseWorker):
    def _run(self, query, *args, **kwargs):
        return {"query": query, "id": "lite_test"}

logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = root_path = Path(__file__).parents[0]

# Import registered modules
registry.import_module(CURRENT_PATH.joinpath('agent'))

# Load container configuration
container.register_stm("SharedMemSTM")

# Initialize workflow
workflow = ConductorWorkflow(name='react_pro_lite', lite_version=True)

# Configure workflow tasks:
# 1. Input interface for user interaction
client_input_task = simple_task(task_def_name=SimpleInput, task_reference_name='input_interface')

# Configure React Pro workflow
react_workflow = ReactProWorkflow()
react_workflow.set_input(
    query=client_input_task.output('query'),
    id=client_input_task.output('id')
)

# Configure workflow execution flow
workflow >> client_input_task >> react_workflow

# Register workflow
workflow.register(overwrite=True)

# Initialize and start app client with workflow configuration
config_path = CURRENT_PATH.joinpath('configs')
cli_client = DefaultClient(
    interactor=workflow, 
    config_path=config_path, 
    workers=[SimpleInput()]
)

# Start the interaction with a test query
cli_client.start_processor_with_input({"query": "What is the capital of France?"}) 