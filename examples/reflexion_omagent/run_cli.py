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
from agent.react.react_reflexion import ReflexionStrategy  # Import Reflexion strategy enum

# Initialize logging
logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = Path(__file__).parents[0]

# Import registered modules
registry.import_module(project_path=CURRENT_PATH.joinpath('agent'))

# Register state management
container.register_stm("RedisSTM")

# Load container configuration from YAML file
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# Initialize reflexion workflow
workflow = ConductorWorkflow(name='reflexion')

# Configure workflow tasks:
# 1. Input interface for user's question
client_input_task = simple_task(
    task_def_name='InputInterface',
    task_reference_name='input_task'
)

# 2. Set reflexion strategy
set_strategy_task = SetVariableTask(
    task_ref_name='set_strategy',
    input_parameters={
        'reflect_strategy': ReflexionStrategy.REFLEXION.value
    }
)

# 3. Main reasoning and observation tasks
task_react = simple_task(
    task_def_name="ReasoningAction",
    task_reference_name='reasoning_action'
)

task_observation = simple_task(
    task_def_name="ObservationAccess",
    task_reference_name='observation_access'
)

# Configure main reasoning loop with reflexion
react_loop = DoWhileTask(
    task_ref_name='react_loop',
    tasks=[task_react, task_observation],
    termination_condition='if ($.observation_acess["done"] == true){false;} else {true;} '
)

# Configure workflow execution flow:
# Input -> Set Strategy -> Reasoning Loop
workflow >> client_input_task >> set_strategy_task >> react_loop

# Register workflow
workflow.register(True)

# Initialize and start CLI client with workflow configuration
config_path = CURRENT_PATH.joinpath('configs')
cli_client = DefaultClient(
    interactor=workflow,
    config_path=config_path,
    workers=[InputInterface()]
)

cli_client.start_interactor()