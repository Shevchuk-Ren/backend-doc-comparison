# backend-doc-comparison
Multi-Document Comparison & Decision Assistant

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- LLM ollama model (https://ollama.com/)
- Docker

## Enviroment
```bash
echo "*" > .venv/.gitignore
source venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m pip install <package-name>
pip freeze > requirements.txt

```

## For tests
```bash
pytest
```

## Coverage
```bash
coverage run -m pytest
coverage report -m

#debuging
coverage run -m pytest -vv -s
```
## Linting & Formatting
# Flake
```bash
flake8 .
```
# Black
```bash
black .

#Check
black --check .
```

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

## Migrations
```bash
docker compose exec app alembic revision --autogenerate -m "init"
docker compose exec app alembic upgrade head

```