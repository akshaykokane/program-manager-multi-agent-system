from agents.product_research_agent import ProductResearchAgent
from agents.prd_writing_agent import PRDWritingAgent
from agents.proof_reader_agent import ProductReaderAgent


class AgentService:
    def __init__(self):
        self.research_agent = ProductResearchAgent()
        self.prd_writing_agent = PRDWritingAgent()
        self.proof_reader_agent = ProductReaderAgent()

    async def handle_task(self, product_idea: str, requirements: list) -> dict:
        status = []
        
        status.append("Starting product research...")

        # Step 1: Research the product idea
        research_product = await self.research_agent.research_product(product_idea)
        status.append("Product research completed.")

        status.append("Starting PRD writing...")
        # Step 2: Write the PRD based on the research
        prd = await self.prd_writing_agent.write_prd(product_idea, requirements)
        status.append("PRD writing completed.")

        status.append("Starting PRD proofreading...")

        # Step 3: Proofread the PRD
        feedback, issue_detected = await self.proof_reader_agent.proofread_prd(prd)
        status.append("PRD proofreading completed.")

        return {
            "research_product": research_product,
            "prd": prd,
            "feedback": feedback,
            "issue_detected": issue_detected,
            "status": status}


    