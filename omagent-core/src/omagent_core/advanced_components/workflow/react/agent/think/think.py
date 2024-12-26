from pathlib import Path
from typing import List, Any
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

    def _run(self, query: str, next_step: str = "Thought", *args, **kwargs):
        """Process the query using ReAct approach"""
        # 从STM获取context
        context = self.stm(self.workflow_instance_id).get('context', '')
        
        # 记录输入信息
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Think Input', 
            message=f'Query: {query}\nContext: {context}\nNext Step: {next_step}'
        )
        
        # 构建 prompt
        step_number = self._get_step_number(context)
        full_prompt = f"{context}\n{next_step} {step_number}:" if context else f"{query}\n{next_step} {step_number}:"
        
        # 添加动态的步骤编号提示
        full_prompt += f"\nNote: Only output Thought {step_number}."
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Think Prompt', 
            message=f'Full Prompt: {full_prompt}'
        )
        
        # Get response
        response = self.simple_infer(query=query, context=full_prompt)
        output = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                output += content
                
        # 记录输出信息
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Think Output', 
            message=f'Response: {output}'
        )
        
        # 更新context并存入STM
        new_context = f"{context}\n{next_step} {step_number}: {output}" if context else f"{query}\n{next_step} {step_number}: {output}"
        self.stm(self.workflow_instance_id).update({'context': new_context})
        
        return {
            'response': output
        }
        
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