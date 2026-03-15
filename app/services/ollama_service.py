import httpx
from fastapi import HTTPException, status
from app.core.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_host.rstrip("/")
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout
        self.api_key = settings.ollama_key

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.base_url}/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM service is unavailable",
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"LLM request failed:{exc.response.text}",
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
