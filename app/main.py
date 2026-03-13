from fastapi import FastAPI, UploadFile, File
from app.core.config import settings
from app.routers.healthcheck import router as health_router
from app.routers.document import router as doc_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated


app = FastAPI(title=settings.title, version="0.1.0",
    openapi_version="3.0.3",)

allowed_org = settings.cors_origins

app.include_router(health_router)
app.include_router(doc_router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_org or ["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}