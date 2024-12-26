from pathlib import Path
from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.registry import registry
from omagent_core.utils.logger import logging
from langchain.agents.react.base import DocstoreExplorer
from langchain_community.docstore.wikipedia import Wikipedia
from pydantic import Field

@registry.register_worker()
class WikiSearch(BaseWorker):
    tool_manager: dict = Field(...)  # 改为 dict 类型
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docstore = DocstoreExplorer(Wikipedia())

    def _run(self, action_output: str, workflow_id: str, *args, **kwargs):
        """Execute search or lookup based on action output"""
        try:
            # 从STM获取context和其他状态
            state = self.stm(workflow_id)
            context = state.get('context', '')
            current_document = state.get('current_document', {})
            
            if 'Search[' in action_output:
                result = self._handle_search(action_output, context)
            elif 'Lookup[' in action_output:
                result = self._handle_lookup(action_output, context)
            else:
                result = self._format_response(action_output, context)
                
            # 更新context
            self.stm(workflow_id).update({'context': result['context']})
            
            # 移除context从返回值中(因为已经存在STM中)
            if 'context' in result:
                del result['context']
                
            return result
            
        except Exception as e:
            logging.error(f"Error in _run: {str(e)}")
            raise

    def _handle_search(self, action_output: str, context: str):
        """Handle Search action"""
        search_term = self._extract_term('Search', action_output)
        if not search_term:
            return self._format_response(action_output, context)
        
        try:
            result = self.docstore.search(search_term)
            if result:
                result_text = result.strip('\n').strip().replace('\n', '')
                # 使用状态管理器存储状态
                self.stm(self.workflow_instance_id).update({
                    'current_document': {'content': result},
                    'lookup_str': '',
                    'lookup_index': 0
                })
                return {
                    'output': result_text,
                    'context': f"{context}\nObservation {self._get_step_number(context)}: {result_text}"
                }
            else:
                return self._format_response(f"No content found for '{search_term}'", context)
        except Exception as e:
            return self._format_response(f"Error occurred during search: {str(e)}", context)

    def _handle_lookup(self, action_output: str, context: str):
        """Handle Lookup action"""
        lookup_term = self._extract_term('Lookup', action_output)
        if not lookup_term:
            return self._format_response(action_output, context)
            
        try:
            # 从状态管理器获取状态
            state = self.stm(self.workflow_instance_id)
            current_document = state.get('current_document', {})
            lookup_str = state.get('lookup_str', '')
            lookup_index = state.get('lookup_index', 0)

            if not current_document:
                raise ValueError("No previous search results available. Please perform a search first.")
            
            paragraphs = current_document['content'].split('\n\n')
            
            # 更新lookup状态
            new_lookup_index = lookup_index
            if lookup_term.lower() != lookup_str:
                new_lookup_str = lookup_term.lower()
                new_lookup_index = 0
            else:
                new_lookup_str = lookup_str
                new_lookup_index += 1
                
            lookups = [p for p in paragraphs if lookup_term.lower() in p.lower()]
            
            if len(lookups) == 0:
                result = "No Results"
            elif new_lookup_index >= len(lookups):
                result = "No More Results"
            else:
                result_prefix = f"(Result {new_lookup_index + 1}/{len(lookups)})"
                result = f"{result_prefix} {lookups[new_lookup_index]}"
                result = result.strip('\n').strip().replace('\n', '')
            
            # 更新状态管理器中的状态
            state.update({
                'lookup_str': new_lookup_str,
                'lookup_index': new_lookup_index
            })
            
            return {
                'output': result,
                'context': f"{context}\nObservation {self._get_step_number(context)}: {result}"
            }
            
        except ValueError as ve:
            return self._format_response(str(ve), context)
        except Exception as e:
            return self._format_response(f"Error occurred during lookup: {str(e)}", context)

    def _format_response(self, result: str, context: str):
        """Format basic response"""
        return {
            'output': result,
            'context': f"{context}\nObservation {self._get_step_number(context)}: {result}",
            'current_document': None,
            'lookup_str': '',
            'lookup_index': 0
        }

    def _extract_term(self, action_type: str, action_output: str) -> str:
        """Extract term from action output"""
        if f'{action_type}[' in action_output:
            start = action_output.find(f'{action_type}[') + len(action_type) + 1
            end = action_output.find(']', start)
            return action_output[start:end].strip()
        return ""

    def _get_step_number(self, context: str) -> int:
        """Get the next step number based on context"""
        if not context:
            return 1
        lines = context.split('\n')
        step_count = sum(1 for line in lines if any(
            line.strip().startswith(f"{marker} ") and any(c.isdigit() for c in line)
            for marker in ['Thought', 'Action', 'Observation']
        ))
        return (step_count // 3) + 1 