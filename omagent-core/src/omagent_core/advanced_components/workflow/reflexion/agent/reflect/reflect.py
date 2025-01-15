from pathlib import Path
from typing import List, Any
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Reflect(BaseLLMBackend, BaseWorker):
    """Reflect worker that implements Reflexion approach for self-reflection"""
    
    example: str = Field(default="")
    
    prompts: List[PromptTemplate] = Field(
        default=[
            PromptTemplate.from_file(
                CURRENT_PATH.joinpath("user_prompt.prompt"), 
                role="user"
            ),
        ]
    )

    def _run(self, query: str, previous_attempts: str = "", id: str = "", *args, **kwargs):
        """Process the query using Reflexion approach"""
        # Get context from STM
        state = self.stm(self.workflow_instance_id)
        context = state.get('context', '')

        # Initialize token_usage
        token_usage = state.get('token_usage', {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        })
        
        # Build prompt with previous attempts if available
        full_prompt = f"{self.example}\nPrevious Attempts: {previous_attempts}\nQuestion: {query}"
        if context:
            full_prompt = f"{context}\nReflection:"
        
        # Get response from model
        response = self.simple_infer(query=query, context=full_prompt)

        # Get model call parameters
        message = self.prep_prompt([{"question": query}])
        body = self.llm._msg2req(message[0])
        state["body"] = body
        
        # Process response
        output = response['choices'][0]['message']['content']
        
        # Update token usage
        if 'usage' in response:
            token_usage['prompt_tokens'] += response['usage']['prompt_tokens']
            token_usage['completion_tokens'] += response['usage']['completion_tokens']
            token_usage['total_tokens'] += response['usage']['total_tokens']
            state.update({'token_usage': token_usage})
    
        # Record output information
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Reflect', 
            message=f'Reflection: {output}'
        )
        
        # Update context and store in STM
        new_context = f"{context}\nReflection: {output}" if context else f"{self.example}\nQuestion: {query}\nReflection: {output}"
        state.update({
            'context': new_context,
            'id': id,
            'query': query
        })

        return {
            'response': output,
            'reflection': output
        } 