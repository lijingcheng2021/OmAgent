from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from omagent_core.engine.workflow.task.do_while_task import DoWhileTask
from .agent.action.action import Action
from .agent.think.think import Think
from .agent.wiki_search.wiki_search import WikiSearch
from omagent_core.utils.logger import logging
from omagent_core.utils.container import container

class ReactWorkflow(ConductorWorkflow):
    def __init__(self):
        super().__init__(name='react')
        
    def set_input(self, query: str):
        self.query = query
        self._configure_tasks()
        self._configure_workflow()
        
    def _configure_tasks(self):
        # Think task
        self.think_task = simple_task(
            task_def_name=Think,                
            task_reference_name='think',
            inputs={
                'query': self.query,
                'next_step': 'Thought',
                'workflow_id': '${workflow.workflowId}'
            }
        )
        
        # Action task
        self.action_task = simple_task(
            task_def_name=Action,
            task_reference_name='action',
            inputs={
                'query': self.query,
                'next_step': 'Action',
                'workflow_id': '${workflow.workflowId}'
            }
        )
        
        # Wiki Search task
        self.wiki_search_task = simple_task(
            task_def_name=WikiSearch,
            task_reference_name='wiki_search',
            inputs={
                'action_output': self.action_task.output('output'),
                'workflow_id': '${workflow.workflowId}'
            }
        )
        
        # Do-While loop
        self.loop_task = DoWhileTask(
            task_ref_name='react_loop',
            tasks=[self.think_task, self.action_task, self.wiki_search_task],
            termination_condition='if ($.action.action_type == "Finish"){false;} else {true;}'
        )
        
    def _configure_workflow(self):
        # Configure workflow execution flow
        self >> self.loop_task
        
        # Set workflow outputs
        self.output_fields = {
            'final_answer': '${action.output.final_answer}',
            'context': '${action.output.context}'
        }
