from app.prompts.document_decision import build_decision_prompt, SYSTEM_PROMPT
from .ollama_service import OllamaService
from fastapi import HTTPException, status
import json


class DecisionService:
    def __init__(self):
        self.ollama_service = OllamaService()

    async def goal_analysis(self, summary_data, comparise_table):

        goal_analysis = await self.ollama_service.chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_decision_prompt(summary_data, comparise_table),
        )
        try:
            decision_data = json.loads(goal_analysis)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid JSON returned by LLM for data",
            )
        return {"best_options": decision_data}
