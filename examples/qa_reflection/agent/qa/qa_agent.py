from pathlib import Path
from typing import List

from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.tool_system.manager import ToolManager
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class QAAgent(BaseLLMBackend, BaseWorker):
    """QA agent that handles user queries and generates responses."""
    
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
    tool_manager: ToolManager

    def _run(self, query: str, *args, **kwargs):
        """Process the query and generate a response.

        Args:
            query (str): The user's question
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            dict: Response containing the answer
        """
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress="QA",
            message=f"Processing query: {query}"
        )

        # Generate response using LLM
        chat_complete_res = self.simple_infer(
            query=query,
            tools=self.tool_manager.generate_prompt(),
        )

        response = chat_complete_res["choices"][0]["message"]["content"]
        
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress="QA",
            message=f"Generated response"
        )

        return {"response": response} 