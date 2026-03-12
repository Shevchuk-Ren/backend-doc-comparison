from fastapi import FastAPI
from app.core.config import settings
import uvicorn

app = FastAPI(title=settings.title)

host = settings.host
port = int(settings.port)
uvicorn.run("app.main:app", host=host, port=port, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}