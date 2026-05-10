# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the API server
uvicorn main:app --reload
```

There are no tests currently in this project.

## Environment Variables

Create a `.env` file with:

```env
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=...
AZURE_OPENAI_MODEL=...

SLACK_USER_TOKEN=...
TECH_SLACK_USER_TOKEN=...
TECH_SLACK_CANVAS_CHANNEL_ID=...
TECH_SLACK_WORKSPACE_ID=...
TECH_SLACK_WORKSPACE_DOMAIN=...
```

The PRD agent hardcodes its Slack channel/workspace IDs in [agents/prd_writing_agent.py](agents/prd_writing_agent.py) as class constants; the technology consultant reads its Slack config from env vars.

## Architecture

This is a FastAPI app that orchestrates a three-agent pipeline using the `agent-framework` library (v1.2.0). The single HTTP endpoint `POST /product-research` drives the entire workflow.

### Agent pipeline (DAG, left to right)

```
ProductResearchAgent → PRDWritingExecutor → TechnologyConsultantAgent
```

Each step receives the prior step's output as its input via `WorkflowContext.send_message()`. The workflow is assembled in `AgentService.product_development_workflow()` using `WorkflowBuilder` with `add_edge()`.

### Key patterns

**Agent + Executor split** — Each agent is two classes:
- An `Agent` class (e.g. `ProductResearchAgent`) owns the LLM client and system prompt. It has an async method that calls `agent.run(task)`.
- An `Executor` subclass (e.g. `ProductResearchExecutor`) wraps the agent's method with `@handler` and `WorkflowContext` plumbing so it can be wired into a workflow.

`PRDWritingExecutor` is the exception — it combines both roles in one class, using `Agent` as an async context manager inside `@handler`.

**Slack side-effects** — Both `PRDWritingExecutor` and `TechnologyConsultantAgent` write their output to Slack Canvases and post a link message after each step. `SlackCanvasClient` in [services/slack_client.py](services/slack_client.py) handles the Slack API calls. It must be `validate()`d before use (raises `ValueError` if tokens/IDs are missing).

**LLM client** — All agents use `OpenAIChatClient` from `agent_framework.openai`, which reads the `AZURE_OPENAI_*` environment variables automatically.

### Request/response flow

1. `POST /product-research` → [api/routers/product_research_route.py](api/routers/product_research_route.py)
2. Router calls `AgentService.product_development_workflow(product_idea, requirements)`
3. Workflow runs: research → PRD writing (+ Slack canvas) → tech consultation (+ Slack canvas)
4. Returns the final tech consultant output wrapped in `{"research_report": ...}`
