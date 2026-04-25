from fastapi import FastAPI
from dotenv import load_dotenv
from routers.api import product_research_route as product_research

load_dotenv()                                   

app = FastAPI()

app.include_router(product_research.router)
