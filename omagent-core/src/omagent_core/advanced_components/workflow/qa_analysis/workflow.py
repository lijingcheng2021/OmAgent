from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from omagent_core.advanced_components.workflow.qa_analysis.agent.qa.qa import QA
from omagent_core.advanced_components.workflow.qa_analysis.agent.analyzer.analyzer import Analyzer

class QAAnalysisWorkflow(ConductorWorkflow):
    def __init__(self):
        super().__init__(name='qa_analysis_workflow')
        
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
        
        # Analysis task for result analysis
        self.analyzer_task = simple_task(
            task_def_name=Analyzer, 
            task_reference_name='analyzer',
            inputs={'qa_result': self.qa_task.output('result')}
        )
        
    def _configure_workflow(self):
        # Configure workflow execution flow: QA -> Analysis
        self >> self.qa_task >> self.analyzer_task
        
        # Set workflow outputs
        self.qa_result = self.qa_task.output('result')
        self.analysis_result = self.analyzer_task.output('analysis')
