# react_reflexion.py

from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.utils.registry import registry
from omagent_core.models.llms.schemas import Message, Content
from omagent_core.utils.general import encode_image
from omagent_core.models.llms.prompt.parser import StrParser
from omagent_core.models.llms.openai_gpt import OpenaiGPTLLM
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.container import container

class ReflexionStrategy(Enum):
    NONE = "none"
    REFLEXION = "reflexion"
    LAST_ATTEMPT = "last_attempt"
    LAST_ATTEMPT_AND_REFLEXION = "last_attempt_and_reflexion"

REACT_BASE_PROMPT = """Solve a question answering task with interleaving Thought, Action, Observation steps. 
Thought can reason about the current situation, and Action can be:
(1) Search[entity] which searches entity
(2) Lookup[keyword] which finds the next sentence containing keyword in the last search
(3) Finish[answer] which gives the final answer
You may take as many steps as necessary.

Question: {question}{scratchpad}"""

REFLECT_PROMPT = """You are an advanced reasoning agent that can improve based on self reflection. 
Given the previous reasoning trail, diagnose a possible reason for failure and devise a new plan.

Previous trial:
{previous_trial}

Reflection:"""

LAST_TRIAL_HEADER = "\nPrevious Trial:\n"
REFLECTION_HEADER = "\nThe following reflections give a plan to avoid failing to answer the question in the same way you did previously.\n"

def format_reflections(reflections: List[str], header: str = REFLECTION_HEADER) -> str:
    if not reflections:
        return ''
    return header + 'Reflections:\n- ' + '\n- '.join([r.strip() for r in reflections])

def format_last_attempt(question: str, scratchpad: str, header: str = LAST_TRIAL_HEADER) -> str:
    return header + f'Question: {question}\n{scratchpad}\n(END PREVIOUS TRIAL)\n'

@registry.register_worker()
class ReflectionAction(BaseWorker, BaseLLMBackend):
    llm: OpenaiGPTLLM
    
    def _run(self, *args, **kwargs) -> Dict[str, Any]:
        # Get current state
        state = self.stm(self.workflow_instance_id)
        prompt = state['prompt']
        strategy = state.get('reflect_strategy', ReflexionStrategy.REFLEXION)
        
        # Build reflection prompt
        reflection_prompt = REFLECT_PROMPT.format(
            previous_trial=prompt
        )
        
        # Get reflection result
        chat_message = [Message(role="user", message_type='text', content=reflection_prompt)]
        reflection_res = self.llm.generate(records=chat_message)
        reflection = reflection_res["choices"][0]["message"]["content"]
        
        # Update reflection history
        if 'reflections' not in state:
            state['reflections'] = []
            
        if strategy == ReflexionStrategy.LAST_ATTEMPT:
            state['reflections'] = [prompt]
            reflections_str = format_last_attempt(
                state['original_question'],
                state['reflections'][0]
            )
        elif strategy == ReflexionStrategy.REFLEXION:
            state['reflections'].append(reflection)
            reflections_str = format_reflections(state['reflections'])
        elif strategy == ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION:
            reflections_str = format_last_attempt(state['original_question'], prompt)
            state['reflections'] = [reflection]
            reflections_str += format_reflections(
                state['reflections'],
                header=REFLECTION_HEADER
            )
        else:
            raise ValueError(f"Unknown reflection strategy: {strategy}")
        
        # Build new prompt
        new_prompt = REACT_BASE_PROMPT.format(
            question=state['original_question'],
            scratchpad="",
        )
        if reflections_str:
            new_prompt = reflections_str + "\n" + new_prompt
            
        # Update state
        state['prompt'] = new_prompt
        state['loop_index'] = 1
        
        return {"reflection_added": True}

@registry.register_worker()
class ReasoningAction(BaseWorker, BaseLLMBackend):
    llm: OpenaiGPTLLM

    def _run(self, *args, **kwargs) -> Dict[str, Any]:
        state = self.stm(self.workflow_instance_id)
        
        # Initialize state
        if 'prompt' not in state:
            raise ValueError("Prompt not found in state")
            
        if 'original_question' not in state:
            prompt = state['prompt']
            question = prompt.split("Question: ")[-1].strip().split("\n")[0]
            state['original_question'] = question
            
        if 'loop_index' not in state:
            state['loop_index'] = 1
            
        # Generate response
        loop_index = state['loop_index']
        prompt = state['prompt']
        
        chat_message = [Message(role="user", message_type='text', content=prompt)]
        chat_complete_res = self.llm.generate(records=chat_message)
        react_response = chat_complete_res["choices"][0]["message"]["content"]

        # Parse response
        thought_action = react_response.split(f"\nObservation {loop_index}:")[0]
        thought, action = thought_action.strip().split(f"\nAction {loop_index}: ")
        
        # Update state
        state['thought'] = thought
        state['action'] = action
        
        return {"response": react_response}

@registry.register_worker()
class ObservationAccess(BaseWorker, BaseLLMBackend):
    llm: OpenaiGPTLLM
    
    def _run(self, *args, **kwargs) -> Dict[str, Any]:
        state = self.stm(self.workflow_instance_id)
        thought = state['thought']
        action = state['action']
        loop_index = state['loop_index']
        prompt = state['prompt']

        # Execute action and get observation
        obs, reward, done, info = step(env, action[0].lower() + action[1:])
        obs = obs.replace('\\n', '')
        
        # Build step string
        step_str = (
            f"Thought {loop_index}: {thought}\n"
            f"Action {loop_index}: {action}\n"
            f"Observation {loop_index}: {obs}\n"
        )
        
        # Send step information
        self.callback.send_answer(self.workflow_instance_id, msg=f'\n{step_str}')
        
        # Update prompt and state
        prompt += step_str
        state['prompt'] = prompt
        
        if done:
            env.reset()
        
        loop_index += 1
        state['loop_index'] = loop_index

        # Check if forced termination is needed
        if loop_index >= 8 and not done:
            obs, reward, done, info = step(env, "finish[]")
            
            # Trigger reflection if forced termination
            if done:
                reflection_worker = ReflectionAction(
                    workflow_instance_id=self.workflow_instance_id,
                    llm=self.llm,
                    callback=self.callback,
                    stm=self.stm
                )
                reflection_worker._run()

        return {"done": done}

# Utility function
def step(env: Any, action: str) -> tuple:
    """Wrapper function for executing environment steps"""
    return env.step(action)