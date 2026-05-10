# Program Manager Multi-Agent System

A FastAPI-based multi-agent system that turns a product idea into:

- a product research report
- a generated PRD
- a technical feasibility review

## What It Does

This project orchestrates a 3-step workflow:

1. Product Research Agent
2. PRD Writing Agent
3. Technology Consultant Agent

The workflow is built in `AgentService` and exposed through one FastAPI endpoint: `POST /product-research`.

## Project Structure

```text
main.py
requirements.txt
README.md
agents/
  __init__.py
  product_research_agent.py
  prd_writing_agent.py
  technical_consultant_agent.py
api/
  __init__.py
  routers/
    product_research_route.py
services/
  __init__.py
  agent_service.py
  slack_client.py
  tavily_client.py
```

## Prerequisites

- Python 3.10+
- Ollama running locally (agents currently use `OllamaChatClient`)
- Tavily API key for web research
- Slack credentials for canvas creation and posting messages

## Environment Variables

Create a `.env` file in the project root:

```env
# Required for product research
TAVILY_API_KEY=your_tavily_api_key

# Required for PRD writing Slack canvas
SLACK_USER_TOKEN=your_slack_user_token

# Required for technology consultant Slack canvas
TECH_SLACK_USER_TOKEN=your_tech_slack_user_token
TECH_SLACK_CANVAS_CHANNEL_ID=your_tech_slack_channel_id
TECH_SLACK_WORKSPACE_ID=your_tech_slack_workspace_id
TECH_SLACK_WORKSPACE_DOMAIN=your_tech_slack_workspace_domain

# Optional (currently only read/logged in main.py)
AZURE_OPENAI_MODEL=your_model_name
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run with FastAPI

Start the server with Uvicorn:

```bash
python -m uvicorn main:app --reload
```

FastAPI app URL: `http://127.0.0.1:8000`

Open interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Usage

### POST `/product-research`

Request body:

```json
{
  "product_idea": "AI assistant for student project planning",
  "requirements": [
    "Task timeline generation",
    "Weekly progress dashboard",
    "Deadline reminders"
  ]
}
```

Example cURL:

```bash
curl -X POST "http://127.0.0.1:8000/product-research" \
  -H "Content-Type: application/json" \
  -d '{
    "product_idea": "AI assistant for student project planning",
    "requirements": [
      "Task timeline generation",
      "Weekly progress dashboard",
      "Deadline reminders"
    ]
  }'
```

Response shape:

```json
{
  "research_report": "...final workflow output..."
}
```

## Notes

- Keep `.env` out of version control.
- If credentials were accidentally exposed, rotate them immediately.
- Several dependencies are pre-release/beta versions from the agent framework ecosystem.
