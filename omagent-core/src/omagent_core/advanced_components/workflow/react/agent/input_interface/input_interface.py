from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.logger import logging

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class InputInterface(BaseWorker):
    def _run(self, *args, **kwargs):
        user_input = self.input.read_input(
            workflow_instance_id=self.workflow_instance_id, 
            input_prompt='Please input your question:'
        )
        messages = user_input['messages']
        message = messages[-1]
        text = None
        for each_content in message['content']:
            if each_content['type'] == 'text':
                text = each_content['data']
        return {'query': text} 