import logging

import httpx


class SlackCanvasClient:
    SLACK_CANVAS_CREATE_URL = "https://slack.com/api/canvases.create"
    SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

    def __init__(self, token: str, channel_id: str, workspace_id: str, domain: str, logger: logging.Logger | None = None):
        self.token = token
        self.channel_id = channel_id
        self.workspace_id = workspace_id
        self.domain = domain
        self.logger = logger or logging.getLogger(__name__)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def validate(self) -> None:
        if not self.token:
            raise ValueError("Slack token is not set. Configure it in your environment.")
        if not self.channel_id:
            raise ValueError("Slack channel id is not set. Configure it in your environment.")
        if not self.workspace_id:
            raise ValueError("Slack workspace id is not set. Configure it in your environment.")
        if not self.domain:
            raise ValueError("Slack workspace domain is not set. Configure it in your environment.")

    async def create_canvas(self, title: str, content_markdown: str) -> str:
        self.validate()
        payload = {
            "title": title,
            "document_content": {
                "type": "markdown",
                "markdown": content_markdown,
            },
            "channel_id": self.channel_id,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.SLACK_CANVAS_CREATE_URL, headers=self._headers(), json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Slack API HTTP error {response.status_code}: {response.text}")

        data = response.json()
        if not data.get("ok", False):
            raise RuntimeError(f"Slack API error: {data.get('error', 'unknown_error')}")

        canvas_id = data.get("canvas_id")
        if not canvas_id:
            raise RuntimeError("Slack API did not return canvas_id.")

        return canvas_id

    async def post_message(self, message: str) -> None:
        self.validate()
        payload = {
            "channel": self.channel_id,
            "text": message,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.SLACK_POST_MESSAGE_URL, headers=self._headers(), json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Slack API HTTP error {response.status_code}: {response.text}")

        data = response.json()
        if not data.get("ok", False):
            raise RuntimeError(f"Slack API error: {data.get('error', 'unknown_error')}")

    def build_canvas_url(self, canvas_id: str) -> str:
        self.validate()
        return f"https://{self.domain}.slack.com/docs/{self.workspace_id}/{canvas_id}"