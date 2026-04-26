from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

class TechnologyConsultantAgent:
    def __init__(self):
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a technology consultant agent.
            Your task is to review and the prd document to tell technical feasibility, identify potential technical challenges, and provide recommendations for technology stack and architecture.
            At end add "Decision:" Feasible or Not Feasible and "Issue:" if any technical issue is detected in the PRD.
            """
        )

    async def consult_technology(self, prd: str) -> tuple[str, bool]:
        task = f"Consult the following PRD: {prd}. Provide feedback on technical feasibility, potential technical challenges, and recommendations for technology stack and architecture."
        feedback = await self.agent.run(task)
        
        issue_detected = False

        if "Issue:" in feedback.text:
            issue_detected = True

        return feedback.text, issue_detected