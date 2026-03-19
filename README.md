# backend-doc-comparison
## Multi-Document Comparison & Decision Assistant

Multi-Document Comparison & Decision Assistant is a backend application that helps users analyze several documents at the same time, such as contracts, offers, and specifications.

The system reads uploaded documents, creates a summary for each file, builds a comparison table, and produces a final conclusion to help users make a better decision.

## What the application does

This application is designed for people who need to compare multiple business or legal documents in one place.

It can:

- analyze multiple documents in one request

- generate a separate summary for each document

- compare documents by key points

- create a final decision-oriented conclusion

- save analysis history for registered users

## Supported file formats

The application works only with document files and currently supports:

- txt

- docx

- pdf

## File validation and security

The backend includes file validation to reduce the risk of uploading unsupported or potentially harmful files.

The system accepts only document formats that are intended for text-based analysis. This helps protect the application from files that are not meant for document processing.

## Rate limiting

A rate limiter is used to prevent too many requests in a short time.
This is important because document analysis communicates with an LLM model, and rate limiting helps:

- avoid unnecessary overload

- protect the backend from abuse

- keep the service more stable

## User features

Registered users have additional functionality.

They can:

- save their analysis results

- access their previous analysis history later

Anonymous users can still analyze documents, but their results are not stored.

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- LLM ollama model (https://ollama.com/)
- Docker

## LLM Integration

The application uses the cloud version of Ollama for document analysis.

This approach makes the system faster and easier to run because it does not require hosting a large local model on the server. It is especially useful for small or free server environments, such as lightweight cloud instances (AWS).

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