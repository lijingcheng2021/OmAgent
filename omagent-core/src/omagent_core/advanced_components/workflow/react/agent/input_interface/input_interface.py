from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.logger import logging

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class InputInterface(BaseWorker):
    def _run(self, *args, **kwargs):
        try:
            user_input = self.input.read_input(
                workflow_instance_id=self.workflow_instance_id, 
                input_prompt='Please input your question:'
            )
            
            # 添加日志
            logging.info(f"Received user_input: {user_input}")
            
            if not user_input or 'messages' not in user_input:
                logging.error(f"Invalid input format: {user_input}")
                return {'query': None}
                
            messages = user_input['messages']
            if not messages:
                logging.error("No messages in input")
                return {'query': None}
                
            message = messages[-1]
            text = None
            for each_content in message.get('content', []):
                if each_content.get('type') == 'text':
                    text = each_content.get('data')
                    
            if text is None:
                logging.error(f"No text content found in message: {message}")
                
            return {'query': text}
            
        except Exception as e:
            logging.error(f"Error in InputInterface._run: {str(e)}")
            raise 