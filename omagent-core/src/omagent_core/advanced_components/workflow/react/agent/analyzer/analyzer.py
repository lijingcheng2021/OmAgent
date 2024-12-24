from pathlib import Path
from typing import List
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Analyzer(BaseLLMBackend, BaseWorker):
    """Analyzer worker that determines if the QA response is reasonable"""
    
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

    def _run(self, query: str, response: str, *args, **kwargs):
        """Analyze if the response is reasonable
        
        Args:
            query: Original user question
            response: Response from QA model
        Returns:
            dict: Contains the analysis result (0 for reasonable, 1 for unreasonable)
        """
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Analyzing', 
            message=f'Checking response reasonability...'
        )
        
        # Get response for analysis
        result = self.simple_infer(query=query, response=response)
        
        # Extract the binary result (0 or 1)
        try:
            is_unreasonable = result['choices'][0]['message']['content'].strip()
        except (ValueError, AssertionError):
            self.callback.info(
                agent_id=self.workflow_instance_id,
                progress='Error',
                message='Invalid analysis result, defaulting to unreasonable (1)'
            )
            is_unreasonable = 1
            
        status = "reasonable" if is_unreasonable == 0 else "unreasonable"
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress='Complete',
            message=f'Response is {status}'
        )
                
        return {'analysis': is_unreasonable} 