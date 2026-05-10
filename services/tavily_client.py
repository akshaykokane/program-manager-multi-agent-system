import os
from tavily import TavilyClient
import logging


class TavilyClientHelper:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.logger = logging.getLogger(__name__)
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set. Please configure it in your environment.")
        self.travy_client = TavilyClient(self.api_key)

    def search(self, query: str) -> str:
        # Placeholder for web search functionality
        self.logger.info("Performing Tavily search for query: %s", query)
        response = self.travy_client.search(query)
        self.logger.info("Tavily search response: %s", response)
        return response

