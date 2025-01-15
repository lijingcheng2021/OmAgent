from pathlib import Path
from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.utils.logger import logging
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.programmatic.client import ProgrammaticClient
from omagent_core.advanced_components.workflow.reflexion import ReflexionWorkflow

def process_results(results, dataset_name="example"):
    """Convert results to standard format"""
    formatted_output = {
        "dataset": dataset_name,
        "model_id": "gpt-3.5-turbo",
        "alg": "Reflexion",
        "model_result": []
    }
    
    for result in results:
        output_data = result.get('output', {})
        
        model_result = {
            "id": output_data.get('id'),
            "query": output_data.get('query'),
            "previous_attempts": output_data.get('previous_attempts', ''),
            "reflection": output_data.get('reflection', ''),
            "token_usage": output_data.get('token_usage', {})
        }
        
        formatted_output["model_result"].append(model_result)
    
    return formatted_output

# Initialize logging
logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = Path(__file__).parents[0]

# Import registered modules
registry.import_module(CURRENT_PATH.joinpath('agent'))

# Load container configuration
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# Initialize workflow
workflow = ConductorWorkflow(name='reflexion_workflow')

# Configure Reflexion workflow
reflexion_workflow = ReflexionWorkflow()
reflexion_workflow.set_input(
    query=workflow.input('query'),
    previous_attempts=workflow.input('previous_attempts'),
    id=workflow.input('id')
)

# Configure workflow execution flow
workflow >> reflexion_workflow

# Register workflow
workflow.register(overwrite=True)

# Initialize programmatic client
config_path = CURRENT_PATH.joinpath('configs')
programmatic_client = ProgrammaticClient(
    processor=workflow,
    config_path=config_path,
    workers=[]
)

# Example workflow inputs
workflow_input_list = [
    {
        "query": "What is 2+2?",
        "previous_attempts": "Previous attempt: 2+2 = 5",
        "id": "001"
    }
]

print(f"Processing {len(workflow_input_list)} queries...")

# Run workflow
results = programmatic_client.start_batch_processor(
    workflow_input_list=workflow_input_list
)

# Process results
formatted_results = process_results(results)

# Print results
for result in formatted_results['model_result']:
    print(f"\nReflection Results:")
    print(f"Query: {result['query']}")
    print(f"Previous Attempts: {result['previous_attempts']}")
    print(f"Reflection: {result['reflection']}")

programmatic_client.stop_processor()
