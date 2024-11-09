from omagent_core.services.connectors.redis import RedisConnector
from omagent_core.utils.container import container
from omagent_core.engine.configuration.configuration import Configuration
container.register_connector(name='conductor_config', connector=Configuration)
container.register_connector(name='redis_stream_client', connector=RedisConnector)
from omagent_core.engine.configuration.configuration import Configuration
from omagent_core.engine.orkes.orkes_workflow_client import OrkesWorkflowClient
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.utils.build import build_from_file
from omagent_core.engine.automator.task_handler import TaskHandler
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.http.models.workflow_status import running_status
from omagent_core.engine.automator.task_handler import TaskHandler
from omagent_core.utils.build import build_from_file
from omagent_core.utils.registry import registry
from omagent_core.clients.devices.app.input import AppInput
from omagent_core.clients.devices.cli.callback import DefaultCallback
import yaml
from time import sleep
import json
from colorama import Fore, Style
from omagent_core.utils.container import container
from omagent_core.utils.logger import logging

registry.import_module()

container.register_stm(stm='RedisSTM')
container.register_callback(callback=DefaultCallback)
container.register_input(input=AppInput)

class DefaultClient:
    def __init__(
        self,
        interactor: ConductorWorkflow,
        processor: ConductorWorkflow = None,
        config_path: str = "./config",
        workers: list = [],
    ) -> None:
        self._interactor = interactor
        self._processor = processor
        self._config_path = config_path
        self._workers = workers

    def start_interactor(self):
        worker_config = build_from_file(self._config_path)
        self._task_handler_interactor = TaskHandler(worker_config=worker_config, workers=self._workers)
        self._task_handler_interactor.start_processes()
        workflow_instance_id = self._interactor.start_workflow_with_input(workflow_input={})

        stream_name = f"{workflow_instance_id}_output"
        consumer_name = f"{workflow_instance_id}_agent"  # consumer name
        group_name = "omappagent"  # replace with your consumer group name
        poll_interval = 1

        configuration = Configuration()
        client = OrkesWorkflowClient(configuration=configuration)
        
        try:
            container.get_connector('redis_stream_client')._client.xgroup_create(
                stream_name, group_name, id="0", mkstream=True
            )
        except Exception as e:
            logging.info(f"Consumer group may already exist: {e}")

        
        while True: 
            try:
                status = self._interactor.get_workflow(workflow_id=workflow_instance_id).status    #获取执行状态
                if status == 'COMPLETED':
                    break
                data_flag = False
                content = None
                # logging.info(f"Checking workflow status: {workflow_instance_id}")
                workflow_status = client.get_workflow_status(workflow_instance_id)
                if workflow_status.status not in running_status:
                    logging.info(f"Workflow {workflow_instance_id} is not running, exiting...")
                    break

                # read new messages from consumer group
                messages = container.get_connector('redis_stream_client')._client.xreadgroup(
                    group_name, consumer_name, {stream_name: ">"}, count=1
                )
                # Convert byte data to string
                messages = [
                    (stream, [(message_id, {k.decode('utf-8'): v.decode('utf-8') for k, v in message.items()}) for message_id, message in message_list])
                    for stream, message_list in messages
                ]
                # logging.info(f"Messages: {messages}")
                
                for stream, message_list in messages:
                    for message_id, message in message_list:
                        data_flag, content = self.process_message(message)
                        # confirm message has been processed
                        container.get_connector('redis_stream_client')._client.xack(
                            stream_name, group_name, message_id
                        )
                if data_flag:
                    user_input = input(f"{Fore.GREEN}{content}:{Style.RESET_ALL}")
                    result = {
                        "agent_id": workflow_instance_id,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                        {
                                        "type": "text",
                                        "data": user_input
                                    }
                                ]
                            }
                        ],
                        "kwargs": {}    
                    }
                    container.get_connector('redis_stream_client')._client.xadd(f"{workflow_instance_id}_input", {"payload":json.dumps(result, ensure_ascii=False) })
                # Sleep for the specified interval before checking for new messages again
                # logging.info(f"Sleeping for {poll_interval} seconds, waiting for {stream_name} ...")
                sleep(poll_interval)
            except Exception as e:
                logging.error(f"Error while listening to stream: {e}")
                sleep(poll_interval)  # Wait before retrying
        self.stop_interactor()

    def stop_interactor(self):
        self._task_handler_interactor.stop_processes()
        
    def start_processor(self):
        worker_config = yaml.load(
            open(self._config_path + "/processor/worker.yaml", "r"),
            Loader=yaml.FullLoader,
        )
        self._task_handler_processor = TaskHandler(worker_config=worker_config)
        self._task_handler_processor.start_processes()

    def stop_processor(self):
        self._task_handler_processor.stop_processes()

    def process_message(self, message):
        logging.info(f"Received message: {message}")
        try:
            payload = message.get("payload")
            # check payload data
            if not payload:
                logging.error("Payload is empty")
                return False, None

            try:
                payload_data = json.loads(payload)
            except json.JSONDecodeError as e:
                logging.error(f"Payload is not a valid JSON: {e}")
                return False, None
            
            if "interaction_type" in payload_data and payload_data["interaction_type"] == 1:
                content = payload_data["message"]["content"]
                return True, content
                
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return False, None
        return False, None  

