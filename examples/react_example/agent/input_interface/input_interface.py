from pathlib import Path
from omagent_core.utils.registry import registry
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.logger import logging
import uuid

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class InputInterface(BaseWorker):
    def _process_input(self, input_data):
        """处理输入数据，提取文本内容"""
        if not input_data or 'messages' not in input_data:
            return None
        
        message = input_data['messages'][-1]
        for content in message.get('content', []):
            if content.get('type') == 'text':
                return content.get('data', '').strip()
        return None

    def _run(self, *args, **kwargs):
        # 获取 example 输入
        example_input = self.input.read_input(
            workflow_instance_id=self.workflow_instance_id, 
            input_prompt='Please input example (press Enter to skip):'
        )
        example = self._process_input(example_input)

        # 获取 max_turns 输入
        max_turns_input = self.input.read_input(
            workflow_instance_id=self.workflow_instance_id, 
            input_prompt='Please input max turns (default is 10, press Enter to use default):'
        )
        max_turns = 10  # 默认值
        max_turns_text = self._process_input(max_turns_input)
        if max_turns_text:
            try:
                max_turns = int(max_turns_text)
            except ValueError:
                logging.warning(f"Invalid max_turns input: {max_turns_text}, using default value: 10")

        # 获取主要问题输入
        user_input = self.input.read_input(
            workflow_instance_id=self.workflow_instance_id, 
            input_prompt='Please input your question:'
        )
        query = self._process_input(user_input)
        
        # 返回所有参数
        return {
            'query': query,                   # 用户输入的问题
            'id': str(uuid.uuid4()),          # 生成唯一ID
            'example': example,               # 用户输入的示例或None
            'max_turns': max_turns            # 用户输入的最大轮次或默认值
        } 