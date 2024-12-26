# Import required modules and components
import multiprocessing
import time
from omagent_core.engine.automator.task_handler import TaskHandler
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.build import build_from_file
from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.programmatic.client import ProgrammaticClient
from omagent_core.utils.logger import logging
import requests

from agent.input_interface.input_interface import InputInterface

# Initialize logging
logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = Path(__file__).parents[0]

# Import registered modules
registry.import_module(project_path=CURRENT_PATH.joinpath('agent'))

container.register_stm("RedisSTM")
# Load container configuration from YAML file
container.from_config(CURRENT_PATH.joinpath('container.yaml'))



workflow = ConductorWorkflow(name='wdj_test')

@registry.register_worker()
class SimpleTest(BaseWorker):

    def _run(self, id:str, file_path:str):

        print("sleep 3 seconds...")
        time.sleep(3)

        print("id:", id)
        print("file_path:", file_path)

task1 = simple_task(task_def_name="SimpleTest", task_reference_name="simple_test", inputs={"id": workflow.input("id"), "file_path": workflow.input("file_path")})

workflow >> task1

config_path = CURRENT_PATH.joinpath("configs")
programmatic_client = ProgrammaticClient(processor=workflow, config_path=config_path, workers=[SimpleTest()])

workflow_input_list = []
for i in range(3):
    workflow_input_list.append({"id": str(i), "file_path": f"/Users/wdj/Desktop/test{i}.png"})
programmatic_client.start_batch_processor(workflow_input_list=workflow_input_list)
programmatic_client.stop_processor() 

# for i in range(3):
#     programmatic_client.start_processor_with_input(workflow_input={"id": str(i), "file_path": f"/Users/wdj/Desktop/test{i}.png"})
# programmatic_client.stop_processor() 
