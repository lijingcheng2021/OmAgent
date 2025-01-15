from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from .agent.reflect.reflect import Reflect

class ReflexionWorkflow(ConductorWorkflow):
    def __init__(self):
        super().__init__(name='reflexion')
        
    def set_input(self, query: str, previous_attempts: str = "", id: str = ""):
        self.query = query
        self.previous_attempts = previous_attempts
        self.id = id
        self._configure_tasks()
        self._configure_workflow()
        
    def _configure_tasks(self):
        # Reflect task
        self.reflect_task = simple_task(
            task_def_name=Reflect,                
            task_reference_name='reflect',
            inputs={
                'query': self.query,
                'previous_attempts': self.previous_attempts,
                'id': self.id
            }
        )
        
    def _configure_workflow(self):
        # Configure workflow execution sequence
        self >> self.reflect_task
