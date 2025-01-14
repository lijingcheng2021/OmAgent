from omagent_core.engine.worker.base import BaseWorker
from omagent_core.utils.registry import registry
from omagent_core.utils.logger import logging
from langchain.agents.react.base import DocstoreExplorer
from langchain_community.docstore.wikipedia import Wikipedia

@registry.register_worker()
class WikiSearchPro(BaseWorker):
    """Wiki Search worker for React Pro workflow"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docstore = DocstoreExplorer(Wikipedia())


    def _run(self, action_output: str, *args, **kwargs):
        """Execute search or lookup based on action output"""
        try:
            # 从STM获取context和其他状态
            state = self.stm(self.workflow_instance_id)
            context = state.get('context', '')
            
            # 获取或初始化 token_usage
            token_usage = state.get('token_usage', {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            })
            
            # 获取当前步骤号
            current_step = state.get('step_number', 1)
            
            #query 和 id，从 STM 中获取
            query = state.get('query', '')
            id = state.get('id', '')
            
            if 'Search[' in action_output:
                result = self._handle_search(action_output)
            elif 'Lookup[' in action_output:
                result = self._handle_lookup(action_output)
            else:
                result = action_output
                
            # 更新context（只在STM中保存，不在响应中返回）
            new_context = f"{context}\nObservation {current_step}: {result}"
            
            # 更新状态，包括 context、query、id 和 token_usage
            state.update({
                'context': new_context,
                'token_usage': token_usage,
                'step_number': current_step + 1  # 增加步骤号
            })
            
            # 返回结果，包含所有必要的信息
            return {
                'output': result,
                'query': query,
                'id': id,
                'token_usage': token_usage
            }
            
        except Exception as e:
            logging.error(f"Error in _run: {str(e)}")
            raise

    def _handle_search(self, action_output: str) -> str:
        """Handle Search action"""
        search_term = self._extract_term('Search', action_output)
        if not search_term:
            return action_output
        
        try:
            result = self.docstore.search(search_term)
            if result:
                result_text = result.strip('\n').strip().replace('\n', '')
                
                # 更新状态
                self.stm(self.workflow_instance_id).update({
                    'current_document': {'content': result},
                    'lookup_str': '',
                    'lookup_index': 0
                })
                
                return result_text
            else:
                return f"No content found for '{search_term}'"
        except Exception as e:
            return f"Error occurred during search: {str(e)}"

    def _handle_lookup(self, action_output: str) -> str:
        """Handle Lookup action"""
        lookup_term = self._extract_term('Lookup', action_output)
        if not lookup_term:
            return action_output
            
        try:
            # 从状态管理器获取状态
            state = self.stm(self.workflow_instance_id)
            current_document = state.get('current_document', {})
            lookup_str = state.get('lookup_str', '')
            lookup_index = state.get('lookup_index', 0)

            if not current_document:
                return "No previous search results available. Please perform a search first."
            
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
            
            # 更新状态
            self.stm(self.workflow_instance_id).update({
                'lookup_str': new_lookup_str,
                'lookup_index': new_lookup_index
            })
            
            return result
            
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            return f"Error occurred during lookup: {str(e)}"


    def _extract_term(self, action_type: str, action_output: str) -> str:
        """Extract term from action output"""
        if f'{action_type}[' in action_output:
            start = action_output.find(f'{action_type}[') + len(action_type) + 1
            end = action_output.find(']', start)
            return action_output[start:end].strip()
        return "" 