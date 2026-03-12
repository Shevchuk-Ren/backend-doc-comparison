from fastapi import FastAPI
from app.core.config import settings
import uvicorn

app = FastAPI(title=settings.title)





@app.get("/")
async def root():
    return {"message": "Hello World"}