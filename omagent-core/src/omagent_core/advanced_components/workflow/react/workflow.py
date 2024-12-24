from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from omagent_core.engine.workflow.task.do_while_task import DoWhileTask
from .agent.analyzer.analyzer import Analyzer
from .agent.think.think import Think

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
            inputs={'query': self.query}
        )
        
        # Analyzer task
        self.analyzer_task = simple_task(
            task_def_name=Analyzer,
            task_reference_name='analyzer',
            inputs={
                'query': self.query,
                'response': self.think_task.output('response')
            }
        )
        
        # Do-While loop that continues until we get a reasonable answer
        self.loop_task = DoWhileTask(
            task_ref_name='qa_loop',
            tasks=[self.think_task, self.analyzer_task],
            termination_condition='if ($.analyzer["analysis"] == "1"){true;} else {false;}'
        )
        
    def _configure_workflow(self):
        # Configure workflow execution flow
        self >> self.loop_task
        
        # Set workflow outputs
        self.qa_result = self.think_task.output('response')
        self.analysis_result = self.analyzer_task.output('analysis')
