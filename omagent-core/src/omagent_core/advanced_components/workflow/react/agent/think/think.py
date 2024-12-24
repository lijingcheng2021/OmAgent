from pathlib import Path
from typing import List
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Think(BaseLLMBackend, BaseWorker):
    """Think worker that implements ReAct (Reasoning and Acting) approach"""
    
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
        """Process the query using ReAct approach with Thought, Action, Observation steps
        
        Args:
            query: The user's input question
        Returns:
            dict: Contains the model's response and reasoning process
        """
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Thinking', 
            message=f'Processing query: {query}'
        )
        
        # Get response with reasoning steps
        response = self.simple_infer(query=query)
        
        # Initialize output to capture the full reasoning process
        output = ''
        self.callback.send_incomplete(
            agent_id=self.workflow_instance_id, 
            msg=''
        )
        
        # Process streaming response to show reasoning steps
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