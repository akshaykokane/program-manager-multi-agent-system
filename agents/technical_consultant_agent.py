from agent_framework import Agent, MCPStreamableHTTPTool, WorkflowContext, Executor, handler
from agent_framework.openai import OpenAIChatClient
import logging

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
        
        await ctx.send_message((feedback, issue_detected))

class TechnologyConsultantAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.info("Initializing TechnologyConsultantAgent...")
        self.mcp_tool = MCPStreamableHTTPTool(
            name="Drawio Diagram Generator",
            description="""A tool to generate architecture diagrams using Draw.io. 
            Use this tool to create visual representations of technical architectures and workflows.
            
            Available tool:
            - create_diagram: Creates a diagram from draw.io XML (mxGraphModel format) or Mermaid syntax.
              Input: { "xml": "<mxGraphModel>...</mxGraphModel>" } OR { "mermaid": "graph TD\n  A-->B" }
              Returns: { "svg": "<svg>...</svg>", "xml": "...", "url": "..." }
              The 'svg' field in the response contains embeddable SVG markup for the diagram.
            
            Always use Mermaid syntax for simplicity unless complex layout is needed.
            For architecture diagrams, use 'graph LR' or 'graph TD' Mermaid flowcharts.
            """,
            url="https://mcp.draw.io/mcp",
            load_prompts=False,
            stream_response=False
        )

        

        self.agent = Agent(
            client=OpenAIChatClient(),
            instructions="""You are a technology consultant agent.
                Your task is to review the PRD document to assess technical feasibility, identify potential 
                technical challenges, and provide recommendations for technology stack and architecture.

                Use the Drawio Diagram Generator tool to create a technical architecture diagram:
                - Call create_diagram with a Mermaid flowchart representing the system architecture from the PRD.
                - The tool returns a JSON response with an 'svg' field containing a full SVG string.
                - You MUST copy the COMPLETE svg string exactly as returned — do NOT summarize, truncate, 
                or paraphrase it. Do NOT write '[SVG content is embedded]' or any placeholder.
                - Embed the raw SVG string directly in the report with NO markdown code fences around it.

                CORRECT format for the diagram section:
                ## Technical Architecture Diagram
                <svg xmlns="http://www.w3.org/2000/svg" ...>...</svg>

                WRONG format (never do this):
                ## Technical Architecture Diagram
                ```xml
                <svg>[SVG content is embedded]</svg>
                ```

                Structure your final report with these exact sections:

                ## Technical Architecture Diagram
                [Raw SVG string from create_diagram, no code fences, no truncation]

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
            tools=self.mcp_tool
        )
        
        # Create executor instance that references this agent
        self.consult_technology_executor = TechnologyConsultantExecutor(self)

    async def consult_technology(self, prd: str) -> tuple[str, bool]:
        
        task = f"Consult the following PRD: {prd}. Provide feedback on technical feasibility, potential technical challenges, and recommendations for technology stack and architecture."
        self.logger.info("Starting technology consultation for PRD: %s", prd)

        # MCP tools are async context managers and must be entered before running.
        async with self.agent:
            feedback = await self.agent.run(task)

        self.logger.info("Technology consultation completed for PRD: %s", prd)
        
        issue_detected = False

        if "Issue:" in feedback.text:
            issue_detected = True

        return feedback.text, issue_detected