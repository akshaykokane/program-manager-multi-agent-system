from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the application...")
load_dotenv(override=True)

from api.routers import product_research_route as product_research
from api.routers import slack_events_route as slack_events

logger.info("Environment variables loaded successfully.")
app = FastAPI()

logger.info("FastAPI application initialized successfully.")
app.include_router(product_research.router)
app.include_router(slack_events.router)
