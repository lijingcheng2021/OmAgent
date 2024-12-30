from pathlib import Path
from typing import List

from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Reflection(BaseLLMBackend, BaseWorker):
    """Reflection agent that analyzes the QA process and response."""
    
    prompts: List[PromptTemplate] = Field(
        default=[
            PromptTemplate.from_file(
                CURRENT_PATH.joinpath("sys_prompt.prompt"), role="system"
            ),
            PromptTemplate.from_file(
                CURRENT_PATH.joinpath("user_prompt.prompt"), role="user"
            ),
        ]
    )

    def _run(self, query: str, qa_response: str, *args, **kwargs):
        """Analyze the QA process and generate reflection.

        Args:
            query (str): The original user query
            qa_response (str): The response from QA agent
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            dict: Analysis results and potential improvements
        """
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress="Reflection",
            message="Analyzing QA process"
        )

        # Generate reflection using LLM
        chat_complete_res = self.simple_infer(
            query=query,
            response=qa_response
        )

        analysis = chat_complete_res["choices"][0]["message"]["content"]
        
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress="Reflection",
            message="Analysis complete"
        )

        return {"analysis": analysis} 