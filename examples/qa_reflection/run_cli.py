# Import required modules and components
import os
from pathlib import Path

from agent.input_interface.input_interface import InputInterface
from agent.qa.qa_agent import QAAgent
from agent.reflection.reflection import Reflection
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from omagent_core.clients.devices.cli.client import DefaultClient
from omagent_core.utils.container import container
from omagent_core.utils.logger import logging
from omagent_core.utils.registry import registry

logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = Path(__file__).parents[0]

# Create workflow instance
workflow = ConductorWorkflow(name="qa_reflection_workflow")

# Configure input task
client_input_task = simple_task(
    task_def_name=InputInterface,
    task_reference_name="input_interface",
)

# Configure QA task
qa_task = simple_task(
    task_def_name=QAAgent,
    task_reference_name="qa_agent",
    inputs={
        "query": client_input_task.output("query")
    },
)

# Configure reflection task
reflection_task = simple_task(
    task_def_name=Reflection,
    task_reference_name="reflection",
    inputs={
        "query": client_input_task.output("query"),
        "qa_response": qa_task.output("response")
    },
)

# Configure workflow execution flow: Input -> QA -> Reflection
workflow >> client_input_task >> qa_task >> reflection_task

# Register workflow
workflow.register(overwrite=True)

# Initialize and start CLI client with workflow configuration
config_path = CURRENT_PATH.joinpath("configs")
cli_client = DefaultClient(
    interactor=workflow, 
    config_path=config_path, 
    workers=[InputInterface()]
)
cli_client.start_interactor() 