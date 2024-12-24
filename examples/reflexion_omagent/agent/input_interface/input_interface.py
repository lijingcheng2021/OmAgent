from pathlib import Path

from omagent_core.utils.registry import registry
from omagent_core.utils.general import read_image
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.logger import logging
from .utils import get_webthink_prompt

CURRENT_PATH = Path(__file__).parents[0]


@registry.register_worker()
class InputInterface(BaseWorker):
    """Input interface processor that handles user instructions and image input.
    
    This processor:
    1. Reads user input containing question and image via input interface
    2. Extracts text instruction and image path from the input
    3. Loads and caches the image in workflow storage
    4. Returns the user instruction for next steps
    """

    def _run(self, *args, **kwargs):
        # Read user input through configured input interface
        user_input = self.input.read_input(workflow_instance_id=self.workflow_instance_id, input_prompt='Please tell me your question.')
        
        # Extract text and image content from input message
        content = user_input['messages'][-1]['content']
        for content_item in content:
            if content_item['type'] == 'text':
                question = content_item['data']
        
        logging.info(f'question: {question}\n')
        self.stm(self.workflow_instance_id)['question'] = question
        prompt = get_webthink_prompt()
        prompt += f'Question: {question}\n'
        self.stm(self.workflow_instance_id)['prompt'] = prompt
        # print(222, prompt)
        

        return {'user_instruction': question}
