from pathlib import Path
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.registry import registry
from omagent_core.utils.logger import logging

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class Lookup(BaseWorker):
    """Lookup worker that handles Lookup actions by searching in previous context"""
    
    def _run(self, action_output: str, context: str, *args, **kwargs):
        """Execute lookup based on action output
        
        Args:
            action_output: Output from Action containing lookup parameters
            context: Current conversation context
        Returns:
            dict: Contains lookup results and updated context
        """
        # 记录输入信息
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Lookup Input', 
            message=f'Action Output: {action_output}\nContext: {context}'
        )
        
        # Extract lookup term
        lookup_term = self._extract_lookup_term(action_output)
        
        # If no lookup term found, use action_output directly as observation
        if not lookup_term:
            step_number = self._get_step_number(context)
            observation = f"Observation {step_number}: {action_output}"
            return {
                'observation': observation,
                'context': f"{context}\n{observation}"
            }
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Lookup Term', 
            message=f'Lookup Term: {lookup_term}'
        )
        
        # Execute lookup in previous observations
        result = self._perform_lookup(lookup_term, context)
        
        # Get step number and format observation
        step_number = self._get_step_number(context)
        observation = f"Observation {step_number}: (Result 1/1) {result}"
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='Lookup Output', 
            message=f'Lookup Result: {result}'
        )
        
        return {
            'output': result,
            'context': f"{context}\nObservation {step_number}: (Result 1/1) {result}"
        }

    def _extract_lookup_term(self, action_output: str) -> str:
        """Extract lookup term from action output"""
        if 'Lookup[' in action_output:
            start = action_output.find('Lookup[') + 7
            end = action_output.find(']', start)
            return action_output[start:end]
        return ""

    def _perform_lookup(self, lookup_term: str, context: str) -> str:
        """Perform lookup in previous observations"""
        # 分割上下文为行
        lines = context.split('\n')
        
        # 收集所有观察结果
        observations = []
        for line in lines:
            if line.strip().startswith('Observation'):
                observations.append(line)
        
        # 在观察结果中搜索相关信息
        relevant_info = []
        lookup_term_lower = lookup_term.lower()
        for obs in observations:
            if lookup_term_lower in obs.lower():
                # 提取观察内容（去除"Observation X:"前缀）
                content = obs.split(':', 1)[1].strip()
                relevant_info.append(content)
        
        # 如果找到相关信息，返回最相关的结果
        if relevant_info:
            return relevant_info[-1]  # 返回最新的相关观察
        
        return f"No relevant information found for '{lookup_term}' in previous observations."

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