from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from omagent_core.advanced_components.workflow.qa_evaluation.agent.qa.qa import QA
from omagent_core.advanced_components.workflow.qa_evaluation.agent.evaluator.evaluator import ResponseEvaluator

class QAEvaluationWorkflow(ConductorWorkflow):
    def __init__(self):
        super().__init__(name='qa_evaluation_workflow')
        
    def set_input(self, query: str):
        self.query = query
        self._configure_tasks()
        self._configure_workflow()
        
    def _configure_tasks(self):
        # QA task for model Q&A
        self.qa_task = simple_task(
            task_def_name=QA,
            task_reference_name='qa',
            inputs={'query': self.query}
        )
        
        # Evaluation task for response evaluation
        self.evaluator_task = simple_task(
            task_def_name=ResponseEvaluator, 
            task_reference_name='evaluator',
            inputs={
                'query': self.query,
                'response': self.qa_task.output('response')
            }
        )
        
    def _configure_workflow(self):
        # Configure workflow execution flow: QA -> Evaluation
        self >> self.qa_task >> self.evaluator_task
        
        # Set workflow outputs
        self.qa_result = self.qa_task.output('response')
        self.evaluation_result = self.evaluator_task.output('evaluation') 