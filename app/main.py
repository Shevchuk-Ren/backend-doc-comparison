from fastapi import FastAPI
from app.core.config import settings
from app.routers.healthcheck import router as health_router
from app.routers.document import router as doc_router
from app.routers.users import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(
    title=settings.title,
    version="0.1.0",
    openapi_version="3.0.3",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allowed_org = settings.cors_origins

app.include_router(health_router)
app.include_router(doc_router)
app.include_router(auth_router)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_org or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
