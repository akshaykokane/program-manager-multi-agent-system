# Program Manager Multi-Agent System

A FastAPI-based multi-agent system that helps turn a product idea into a draft PRD and proofreading feedback.

## What It Does

This project orchestrates three agents:

- Product Research Agent: researches market trends, user needs, and competitors.
- PRD Writing Agent: generates a Product Requirements Document from an idea and requirements.
- Proof Reader Agent: reviews the PRD and flags quality issues.

The orchestration happens in `AgentService`, exposed through a single HTTP endpoint.

## Project Structure

```text
main.py
requirements.txt
agents/
  __init__.py
  product_research_agent.py
  prd_writing_agent.py
  proof_reader_agent.py
routers/
  api/
    product_research_route.py
services/
  agent_service.py
```

## Prerequisites

- Python 3.10+
- Azure OpenAI deployment configured

## Environment Variables

Create a `.env` file in the project root with:

```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_MODEL=your_model_name
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

Default server URL: `http://127.0.0.1:8000`

## API Endpoint

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

Response shape:

```json
{
  "research_report": {
    "research_product": "...",
    "prd": "...",
    "feedback": "...",
    "issue_detected": false,
    "status": [
      "Starting product research...",
      "Product research completed.",
      "Starting PRD writing...",
      "PRD writing completed.",
      "Starting PRD proofreading...",
      "PRD proofreading completed."
    ]
  }
}
```

## Notes

- Keep `.env` out of version control.
- If credentials were accidentally exposed, rotate them immediately.
- Some dependencies are pre-release/beta versions from the agent framework ecosystem.
