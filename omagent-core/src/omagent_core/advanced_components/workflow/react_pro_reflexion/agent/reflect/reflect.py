from pathlib import Path
from typing import Dict, Any

from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.models.llms.prompt.prompt import PromptTemplate
from omagent_core.utils.registry import registry

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Reflect(BaseWorker):
    """Worker for reflection process in React Pro workflow"""
    
    def __init__(self):
        super().__init__()
        self.llm: BaseLLMBackend = None
        self.sys_prompt = PromptTemplate(CURRENT_PATH.joinpath("sys_prompt.prompt"))
        self.user_prompt = PromptTemplate(CURRENT_PATH.joinpath("user_prompt.prompt"))
        
    def _run(self, query: str, action_output: str, workflow_id: str, *args, **kwargs) -> Dict[str, Any]:
        """Run reflection process on the action output
        
        Args:
            query: The original query
            action_output: The output from React process
            workflow_id: Workflow instance ID
            
        Returns:
            Dict containing reflection results and whether to retry
        """
        # Get state from STM
        state = self.stm(workflow_id)
        reflection_history = state.get('reflection_history', [])
        
        # Prepare prompts
        sys_prompt = self.sys_prompt.format()
        user_prompt = self.user_prompt.format(
            query=query,
            action_output=action_output,
            reflection_history=reflection_history
        )
        
        # Get reflection from LLM
        reflection = self.llm.chat_completion(
            system=sys_prompt,
            user=user_prompt
        )
        
        # Update reflection history
        reflection_history.append(reflection)
        state['reflection_history'] = reflection_history
        
        # Analyze if we need to retry
        should_retry = "incorrect" in reflection.lower() or "wrong" in reflection.lower()
        
        return {
            'reflection': reflection,
            'should_retry': should_retry,
            'reflection_history': reflection_history
        } 