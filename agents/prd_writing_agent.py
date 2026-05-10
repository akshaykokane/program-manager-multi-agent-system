import os
import logging
from agent_framework import Agent, WorkflowContext, Executor, handler
from agent_framework_ollama import OllamaChatClient
from services.slack_client import SlackCanvasClient

class PRDWritingExecutor(Executor):
    SLACK_CHANNEL_ID = "C0B1E1ASWF5"
    SLACK_WORKSPACE_ID = "T0APZ9GFN81"
    SLACK_WORKSPACE_DOMAIN = "developer-wfk8430"
    
    """Executor for PRD writing tasks"""
    def __init__(self):
        super().__init__(id="prd_writing")
        self.logger = logging.getLogger(__name__)
        self.slack_client = SlackCanvasClient(
            token=os.getenv("SLACK_USER_TOKEN", ""),
            channel_id=self.SLACK_CHANNEL_ID,
            workspace_id=self.SLACK_WORKSPACE_ID,
            domain=self.SLACK_WORKSPACE_DOMAIN,
            logger=self.logger,
        )
    
    @handler
    async def write_prd_executor(self, product_research: str, ctx: WorkflowContext[str]) -> None:
        self.logger.info("Starting PRD writing based on product research.")
        self.slack_client.validate()
        async with Agent(
            client=OllamaChatClient(),
            instructions="""You are a PRD writing agent.
            Your task is to create a detailed Product Requirement Document (PRD)
            based on the provided product idea and requirements.
            The PRD should include sections such as Introduction, Objectives, User Stories,
            Functional Requirements, Non-Functional Requirements, and any other relevant information.
            Ensure that the PRD is clear, concise, and comprehensive.
            Return only the PRD content.

            PRD should be structured as follows:
            ## Introduction
            [Brief overview of the product idea and its purpose]
            ## Objectives
            [List of key objectives and goals for the product]
            ## User Stories
            [Detailed user stories that describe the features and functionalities from the user's perspective]
            ## Functional Requirements
            [Specific functional requirements that the product must meet]
            ## Non-Functional Requirements
            [Performance, security, usability, and other non-functional requirements]

            """,
        ) as agent:
            result = await agent.run(product_research)

        canvas_id = await self.slack_client.create_canvas("Product Requirements Document", result.text)
        canvas_url = self.slack_client.build_canvas_url(canvas_id)
        await self.slack_client.post_message(f"PRD canvas created: {canvas_url}")
        await ctx.send_message(result.text)