import asyncio
import string
import logging
from agent_framework import Agent, WorkflowContext, Executor, handler
from agent_framework.openai import OpenAIChatClient

class ProductResearchExecutor(Executor):
    """Executor for product research tasks"""
    def __init__(self, agent_ref):
        super().__init__(id="product_research")
        self.agent_ref = agent_ref
        self.logger = logging.getLogger(__name__)
    
    @handler
    async def research_product_executor(self, product_idea: str, ctx: WorkflowContext[str]) -> None:
        self.logger.info("Starting product research for idea: %s", product_idea)
        research_report = await self.agent_ref.research_product(product_idea)
        await ctx.send_message(research_report)

class ProductResearchAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a product research agent.
            Your task is to conduct comprehensive research on a given product idea, market trends, and user needs. 
            You will gather information from various sources, analyze competitors, and identify potential opportunities and challenges. 
            Provide insights and recommendations based on your research to help guide the product development process.
            """
        )   
        # Create executor instance that references this agent
        self.research_product_executor = ProductResearchExecutor(self)

    async def research_product(self, product_idea: str) -> str:
        task = f"Conduct research on the following product idea: {product_idea}. Provide insights on market trends, user needs, competitors, and potential opportunities and challenges."
        research_report = await self.agent.run(task)
        return research_report.text