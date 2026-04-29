import asyncio
import string
import logging
from agent_framework import Agent, WorkflowContext, Executor, handler
from agent_framework.openai import OpenAIChatClient

class PRDWritingExecutor(Executor):
    """Executor for PRD writing tasks"""
    def __init__(self, agent_ref):
        super().__init__(id="prd_writing")
        self.agent_ref = agent_ref
        self.logger = logging.getLogger(__name__)
    
    @handler
    async def write_prd_executor(self, product_research: str, ctx: WorkflowContext[str]) -> None:
        self.logger.info("Starting PRD writing based on product research.")
        # Message contains the product research report from previous executor
        # TODO: Get requirements from workflow context or agent service
        prd = await self.agent_ref.write_prd(product_research, [])
        await ctx.send_message(prd)

class PRDWritingAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a PRD writing agent. 
            Your task is to create a detailed Product Requirement Document (PRD) 
            based on the provided product idea and requirements. 
            The PRD should include sections such as Introduction, Objectives, User Stories, Functional Requirements, Non-Functional Requirements, and any other relevant information. 
            Ensure that the PRD is clear, concise, and comprehensive.
            """
        )
        # Create executor instance that references this agent
        self.write_prd_executor = PRDWritingExecutor(self)

    async def write_prd(self, product_research: str, requirements: list) -> str:
        task = f"Write a PRD for the following product research: {product_research} with these requirements: {requirements}"
        prd = await self.agent.run(task)
        return prd.text