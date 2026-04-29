from fastapi import FastAPI
from dotenv import load_dotenv
from routers.api import product_research_route as product_research
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the application...")
load_dotenv()                                   

logger.info("Environment variables loaded successfully.")
app = FastAPI()

logger.info("FastAPI application initialized successfully.")
app.include_router(product_research.router)
