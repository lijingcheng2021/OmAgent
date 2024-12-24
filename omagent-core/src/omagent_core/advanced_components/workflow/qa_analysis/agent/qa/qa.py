from pathlib import Path
from typing import List
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class QA(BaseLLMBackend, BaseWorker):
    """QA worker that uses GPT model to generate responses"""
    
    prompts: List[PromptTemplate] = Field(
        default=[
            PromptTemplate.from_file(
                CURRENT_PATH.joinpath("sys_prompt.prompt"), 
                role="system"
            ),
            PromptTemplate.from_file(
                CURRENT_PATH.joinpath("user_prompt.prompt"), 
                role="user"
            ),
        ]
    )

    def _run(self, query: str, *args, **kwargs):
        """Process the query and generate response using GPT model
        
        Args:
            query: The user's input question
        Returns:
            dict: Contains the model's response
        """
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Answering', 
            message=f'Processing query: {query}'
        )
        
        # Get streaming response from GPT model
        response = self.simple_infer(query=query)
        
        # Initialize output
        output = 'Answer: '
        self.callback.send_incomplete(
            agent_id=self.workflow_instance_id, 
            msg='Answer: '
        )
        
        # Process streaming response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                self.callback.send_incomplete(
                    agent_id=self.workflow_instance_id, 
                    msg=content
                )
                output += content
            else:
                self.callback.send_block(
                    agent_id=self.workflow_instance_id, 
                    msg=''
                )
                break
                
        return {'response': output} 