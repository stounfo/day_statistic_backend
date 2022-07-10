FROM python:3.10.5-slim

WORKDIR /app

COPY ./app ./
COPY ./poetry.lock ./
COPY ./pyproject.toml ./

RUN pip install poetry==1.1.14
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
