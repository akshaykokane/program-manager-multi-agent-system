import re
import logging
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from services.agent_service import AgentService

logger = logging.getLogger(__name__)
router = APIRouter()
agent_service = AgentService()


def _parse_product_idea(text: str) -> str | None:
    # Strip the leading <@BOT_ID> mention
    text = re.sub(r"^<@[A-Z0-9]+>\s*", "", text).strip()
    # Match "product idea: <idea>" (case-insensitive)
    match = re.search(r"product\s+idea\s*:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


async def _run_workflow(product_idea: str) -> None:
    try:
        await agent_service.product_development_workflow(product_idea, [])
    except Exception:
        logger.exception("Workflow failed for idea: %s", product_idea)


@router.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    # Slack URL verification handshake
    if body.get("type") == "url_verification":
        return JSONResponse({"challenge": body["challenge"]})

    event = body.get("event", {})
    if event.get("type") == "app_mention":
        text = event.get("text", "")
        product_idea = _parse_product_idea(text)
        if product_idea:
            logger.info("Received app_mention with product idea: %s", product_idea)
            background_tasks.add_task(_run_workflow, product_idea)
        else:
            logger.warning("app_mention received but no 'product idea: <...>' found in: %s", text)

    return JSONResponse({"ok": True})
