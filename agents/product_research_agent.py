import asyncio
import string
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

class ProductResearchAgent:
    def __init__(self):
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a product research agent.
            Your task is to conduct comprehensive research on a given product idea, market trends, and user needs. 
            You will gather information from various sources, analyze competitors, and identify potential opportunities and challenges. 
            Provide insights and recommendations based on your research to help guide the product development process.
            """
        )   


    async def research_product(self, product_idea: str) -> str:
        task = f"Conduct research on the following product idea: {product_idea}. Provide insights on market trends, user needs, competitors, and potential opportunities and challenges."
        research_report = await self.agent.run(task)
        return research_report.text