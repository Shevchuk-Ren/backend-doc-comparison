from fastapi import FastAPI
from app.core.config import settings
from app.routers.healthcheck import router as health_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.title)

allowed_org = settings.cors_origins

app.include_router(health_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_org or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)