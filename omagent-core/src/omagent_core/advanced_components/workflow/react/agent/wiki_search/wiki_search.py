from pathlib import Path
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.registry import registry
from omagent_core.tool_system.manager import ToolManager
from omagent_core.utils.logger import logging

CURRENT_PATH = Path(__file__).parents[0]

@registry.register_worker()
class WikiSearch(BaseWorker):
    """Wiki search worker that handles Search actions using web search tool"""
    
    tool_manager: ToolManager

    def _run(self, action_output: str, context: str, *args, **kwargs):
        """Execute search based on action output
        
        Args:
            action_output: Output from Action containing search parameters
            context: Current conversation context
        Returns:
            dict: Contains search results and updated context
        """
        # 记录输入信息
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='WikiSearch Input', 
            message=f'Action Output: {action_output}\nContext: {context}'
        )
        
        # Extract search term
        search_term = self._extract_search_term(action_output)
        
        # If no search term found, use action_output directly as observation
        if not search_term:
            step_number = self._get_step_number(context)
            observation = f"Observation {step_number}: {action_output}"
            return {
                'observation': observation,
                'context': f"{context}\n{observation}"
            }
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='WikiSearch Term', 
            message=f'Search Term: {search_term}'
        )
        
        # Execute search
        result = self._perform_search(search_term)
        
        # Get step number and format observation
        step_number = self._get_step_number(context)
        observation = f"Observation {step_number}: {result}"
        
        self.callback.info(
            agent_id=self.workflow_instance_id, 
            progress='WikiSearch Output', 
            message=f'Search Result: {result}'
        )
        
        return {
            'output': result,
            'context': f"{context}\nObservation {step_number}: {result}"
        }

    def _extract_search_term(self, action_output: str) -> str:
        """Extract search term from action output"""
        if 'Search[' in action_output:
            start = action_output.find('Search[') + 7
            end = action_output.find(']', start)
            return action_output[start:end]
        else:
            return ""

    def _perform_search(self, search_term: str) -> str:
        """Perform search using web search tool"""
        # Construct search query
        search_query = f"Please search for information about: {search_term}"
        
        # Execute search via tool manager
        execution_status, execution_results = self.tool_manager.execute_task(
            task=search_query
        )
        self.callback.send_block(
            agent_id=self.workflow_instance_id, 
            msg='Using web search tool to search for information'
        )
        logging.info(execution_results)

        # Store successful results or raise error
        if execution_status == "success":
            return execution_results
        else:
            return f"Search failed: {execution_results}"

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