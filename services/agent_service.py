from agent_framework import WorkflowBuilder, WorkflowViz

from agents.product_research_agent import ProductResearchAgent
from agents.prd_writing_agent import PRDWritingAgent
from agents.technical_consultant_agent import  TechnologyConsultantAgent
import logging

class AgentService:
    def __init__(self):
        self.research_agent = ProductResearchAgent()
        self.prd_writing_agent = PRDWritingAgent()
        self.technology_consultant_agent = TechnologyConsultantAgent()
        self.logger = logging.getLogger(__name__)


    async def product_development_workflow(self, product_idea: str, requirements: list) -> dict:
        self.logger.info("Starting product development workflow for idea: %s", product_idea)
        builder = WorkflowBuilder(start_executor=self.research_agent.research_product_executor)
        builder.add_edge(self.research_agent.research_product_executor, self.prd_writing_agent.write_prd_executor)
        builder.add_edge(self.prd_writing_agent.write_prd_executor, self.technology_consultant_agent.consult_technology_executor)
        workflow = builder.build()
        
        viz = WorkflowViz(workflow)
        print(viz.to_mermaid())
        
        result = await workflow.run(product_idea)
        self.logger.info("Completed product development workflow for idea: %s", product_idea)
        return result

    