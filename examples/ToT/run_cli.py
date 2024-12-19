# Import required modules and components
from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.cli.client import DefaultClient
from omagent_core.engine.workflow.task.set_variable_task import SetVariableTask
from omagent_core.utils.logger import logging
from omagent_core.engine.workflow.task.do_while_task import DoWhileTask

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



# Initialize simple VQA workflow
workflow = ConductorWorkflow(name='step1_simpleVQA')

# Configure workflow tasks:
# 1. Input interface for user 4 numbers
client_input_task = simple_task(task_def_name='InputInterface', task_reference_name='input_task')

task_prediction = simple_task(task_def_name='NextStatePrediction', task_reference_name='next_state_prediction')

task_evaluation = simple_task(task_def_name='StateEvaluation', task_reference_name='state_evaluation')

task_selection = simple_task(task_def_name='StateSelection', task_reference_name='state_selection')

task_check = simple_task(task_def_name="CompletionCheck", task_reference_name="completion_check")

tot_loop = DoWhileTask(task_ref_name='tot_loop', tasks=[task_prediction, task_evaluation, task_selection, task_check], 
                             termination_condition='if ($.completion_check["finish"] == true){false;} else {true;} ')

output_interface = simple_task(task_def_name='OutputInterface', task_reference_name='output_interface')

# Configure workflow execution flow: Input -> TOT_LOOP -> Output
workflow >> client_input_task >> tot_loop >> output_interface

# Register workflow
workflow.register(True)

# Initialize and start CLI client with workflow configuration
config_path = CURRENT_PATH.joinpath('configs')
cli_client = DefaultClient(interactor=workflow, config_path=config_path, workers=[InputInterface()])
cli_client.start_interactor()
