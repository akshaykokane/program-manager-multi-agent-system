from fastapi import APIRouter
from fastapi import HTTPException
from services.agent_service import AgentService
from pydantic import BaseModel

class ProductResearchRequest(BaseModel):
    product_idea: str
    requirements: list[str]
    
router = APIRouter()
agent_service = AgentService()

@router.post("/product-research")
async def product_research(request: ProductResearchRequest):
    try:
        research_report = await agent_service.handle_task(request.product_idea, request.requirements)
        return {"research_report": research_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
