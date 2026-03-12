# backend-doc-comparison
Multi-Document Comparison & Decision Assistant

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- LLM ollama model (https://ollama.com/)
- Redis
- Celery
- Stripe
- drf-yasg (Swagger / OpenAPI)
- Docker

echo "*" > .venv/.gitignore
source venv/bin/activate

## Docker
```bash
#Build image
docker build -t docapp .
#Run container
docker run -p 8000:8000 docapp
#Run with env
docker run --env-file .env -p 8000:8000 docapp
```
## Docker Compose
```bash
#Build image
docker compose up --build
#Run container
docker compose up --build -d
#Run and build with env
docker compose --env-file .env up --build

#Stop container
docker compose down
```
