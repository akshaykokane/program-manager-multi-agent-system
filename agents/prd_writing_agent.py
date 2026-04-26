import asyncio
import string
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

class PRDWritingAgent:
    def __init__(self):
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a PRD writing agent. 
            Your task is to create a detailed Product Requirement Document (PRD) 
            based on the provided product idea and requirements. 
            The PRD should include sections such as Introduction, Objectives, User Stories, Functional Requirements, Non-Functional Requirements, and any other relevant information. 
            Ensure that the PRD is clear, concise, and comprehensive.
            """
        )

    async def write_prd(self, product_idea: str, requirements: list) -> str:
        task = f"Write a PRD for the following product idea: {product_idea} with these requirements: {requirements}"
        prd = await self.agent.run(task)
        return prd.text