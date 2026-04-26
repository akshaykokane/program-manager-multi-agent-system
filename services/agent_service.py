from agents.product_research_agent import ProductResearchAgent
from agents.prd_writing_agent import PRDWritingAgent
from agents.technical_consultant_agent import  TechnologyConsultantAgent


class AgentService:
    def __init__(self):
        self.research_agent = ProductResearchAgent()
        self.prd_writing_agent = PRDWritingAgent()
        self.technology_consultant_agent = TechnologyConsultantAgent()

    async def handle_task(self, product_idea: str, requirements: list) -> dict:
        status = []
        
        status.append("Starting product research...")

        # Step 1: Research the product idea
        research_product = await self.research_agent.research_product(product_idea)
        status.append("Product research completed.")

        status.append("Starting PRD writing...")
        # Step 2: Write the PRD based on the research
        prd = await self.prd_writing_agent.write_prd(research_product, requirements)
        status.append("PRD writing completed.")

        status.append("Starting PRD technology consultation...")

        # Step 3: Consult technology for the PRD
        feedback, issue_detected = await self.technology_consultant_agent.consult_technology(prd)
        status.append("PRD technology consultation completed.")

        return {
            "research_product": research_product,
            "prd": prd,
            "feedback": feedback,
            "issue_detected": issue_detected,
            "status": status}


    