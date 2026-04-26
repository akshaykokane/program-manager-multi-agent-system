from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

class ProductReaderAgent:
    def __init__(self):
        self.agent = Agent(
            client = OpenAIChatClient(),
            instructions = """You are a proof reader agent.
            Your task is to review and proofread the provided Product Requirement Document (PRD) for clarity, coherence, and completeness. 
            Check for any grammatical errors, inconsistencies, or missing information. 
            Provide feedback and suggestions for improvement to ensure that the PRD is well-structured, easy to understand, and effectively communicates the product requirements to the development team.
            If there are any issue, please provide feedback starting with "Issue:" and then provide the feedback. If there are no issues, please respond with "No issues found."
            """
        )

    async def proofread_prd(self, prd: str) -> tuple[str, bool]:
        task = f"Proofread the following PRD: {prd}. Provide feedback on clarity, coherence, completeness, and any grammatical errors. Suggest improvements to enhance the quality of the PRD."
        feedback = await self.agent.run(task)
        
        issue_detected = False

        if "Issue:" in feedback.text:
            issue_detected = True

        return feedback.text, issue_detected