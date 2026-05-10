import os
import logging
from agent_framework import Agent, WorkflowContext, Executor, handler
from agent_framework_ollama import OllamaChatClient
from services.slack_client import SlackCanvasClient

class TechnologyConsultantExecutor(Executor):
    """Executor for technology consultation tasks"""
    def __init__(self, agent_ref):
        super().__init__(id="technology_consultant")
        self.agent_ref = agent_ref
        self.logger = logging.getLogger(__name__)
    
    @handler
    async def consult_technology_executor(self, prd: str, ctx: WorkflowContext[str]) -> None:
        self.logger.info("Starting technology consultation for PRD: %s", prd)
        
        feedback, issue_detected = await self.agent_ref.consult_technology(prd)
        
        await ctx.send_message(feedback)

class TechnologyConsultantAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.slack_client = SlackCanvasClient(
            token=os.getenv("TECH_SLACK_USER_TOKEN", ""),
            channel_id=os.getenv("TECH_SLACK_CANVAS_CHANNEL_ID", ""),
            workspace_id=os.getenv("TECH_SLACK_WORKSPACE_ID", os.getenv("SLACK_WORKSPACE_ID", "")),
            domain=os.getenv("TECH_SLACK_WORKSPACE_DOMAIN", os.getenv("SLACK_WORKSPACE_DOMAIN", "developer-wfk8430")),
            logger=self.logger,
        )

        self.logger.info("Initializing TechnologyConsultantAgent...")

        

        self.agent = Agent(
            client=OllamaChatClient(),
            instructions="""You are a technology consultant agent.
                Your task is to review the PRD document to assess technical feasibility, identify potential 
                technical challenges, and provide recommendations for technology stack and architecture.
                The complete PRD text is provided directly in the user message.
                Never ask for external resources, uploads, or links.
  
                Structure your final report with these exact sections:

                ## Technical Feasibility
                [Your assessment of whether the PRD is technically feasible, with reasoning]

                ## Recommended Tech Stack
                [List recommended technologies, frameworks, and services]

                ## Potential Technical Challenges
                [List and describe key technical risks or challenges]

                ## Issue Detected
                [Only include this section if there are technical issues. Omit if none.]

                Decision: Feasible / Not Feasible
                Issue: [One-line summary, or "None"]
                """,
        )
        
        # Create executor instance that references this agent
        self.consult_technology_executor = TechnologyConsultantExecutor(self)

    async def consult_technology(self, prd: str) -> tuple[str, bool]:
        self.slack_client.validate()

        task = (
            "Analyze the PRD text below and provide a technical assessment. "
            "Use only the provided PRD content and do not request additional documents.\n\n"
            f"PRD:\n{prd}"
        )
        self.logger.info("Starting technology consultation for PRD: %s", prd)

        # MCP tools are async context managers and must be entered before running.
        async with self.agent:
            feedback = await self.agent.run(task)

        self.logger.info("Technology consultation completed for PRD: %s", prd)
        
        issue_detected = False

        if "Issue:" in feedback.text:
            issue_detected = True

        canvas_id = await self.slack_client.create_canvas("Technical Consultant Review", feedback.text)
        canvas_url = self.slack_client.build_canvas_url(canvas_id)
        await self.slack_client.post_message(f"Technical review canvas created: {canvas_url}")
        self.logger.info("Created Slack canvas: %s", canvas_id)

        return feedback.text, issue_detected