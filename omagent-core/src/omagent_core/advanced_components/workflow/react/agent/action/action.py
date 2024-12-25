from pathlib import Path
from typing import List
from omagent_core.models.llms.base import BaseLLMBackend
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.models.llms.prompt import PromptTemplate
from omagent_core.utils.registry import registry
from pydantic import Field

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Action(BaseLLMBackend, BaseWorker):
    """Action worker that determines the next step in ReAct chain"""
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._step_number = 1  # 使用实例变量来跟踪步骤

    def _run(self, query: str, context: str, next_step: str = "Action", *args, **kwargs):
        """Determine the next action based on context"""
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Acting', 
            message=f'Determining next action...'
        )
        
        # 记录输入信息
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Action Input', 
            message=f'Query: {query}\nContext: {context}\nNext Step: {next_step}'
        )
        
        # 构建完整的 prompt
        step_number = self._get_step_number(context)
        full_prompt = f"{context}\n{next_step} {step_number}:"
        full_prompt += f"\nNote: Only output Action {step_number}."
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Action Prompt', 
            message=f'Full Prompt: {full_prompt}'
        )
        
        # 获取并处理响应
        raw_response = self.simple_infer(query=query, context=full_prompt)
        
        # 处理响应
        if isinstance(raw_response, dict):
            response = raw_response['choices'][0]['message']['content']
        else:  # 以防万一保留对其他类型响应的处理
            response = str(raw_response)
        
        # 从响应中提取动作类型
        action_type = 'Search' if 'Search[' in response else 'Lookup' if 'Lookup[' in response else 'Finish' if 'Finish[' in response else None
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Action Output', 
            message=f'Response: {response}\nAction Type: {action_type}'
        )
        
        # 如果是完成动作，直接返回结果
        if action_type == "Finish":
            # 提取最终答案
            answer = self._extract_finish_answer(response)
            return {
                'action_type': action_type,
                'step_number': step_number,
                'output': answer,
                'context': f"{context}\n{next_step} {step_number}: {response}",
                'final_answer': answer
            }
            
        result = {
            'action_type': action_type,
            'step_number': step_number,
            'output': response,
            'context': f"{context}\n{next_step} {step_number}: {response}"
        }
        
        # 添加调试日志
        self.callback.info(
            agent_id=self.workflow_instance_id,
            progress='Action Result',
            message=f'Returning result: {result}'
        )
        
        return result
        
    def _parse_action_type(self, response: str) -> str:
        """Parse the action type from response"""
        if "Search[" in response:
            return "Search"
        elif "Lookup[" in response:
            return "Lookup"
        elif "Finish[" in response:
            return "Finish"
        return "Unknown"
        
    def _get_step_number(self, context: str) -> int:
        """Get the next step number based on context"""
        if not context:
            return 1
            
        # 按行分割上下文
        lines = context.split('\n')
        step_count = 0
        
        # 遍历每一行，检查是否是步骤标记
        for line in lines:
            line = line.strip()
            # 检查行是否以步骤标记开始（标记词 + 空格 + 数字）
            if any(line.startswith(f"{marker} ") and any(c.isdigit() for c in line)
                  for marker in ['Thought', 'Action', 'Observation']):
                step_count += 1
                
        # 返回下一个步骤号
        return (step_count // 3) + 1  # 每组三个步骤（Thought/Action/Observation）共享同一个编号
        
    def _extract_finish_answer(self, response: str) -> str:
        """Extract the final answer from Finish action"""
        if "Finish[" in response:
            start = response.find("Finish[") + 7
            end = response.find("]", start)
            if start > 6 and end > start:
                return response[start:end]
        return response 