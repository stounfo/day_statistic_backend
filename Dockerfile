FROM python:3.11.0

WORKDIR /src

COPY ./app ./app
COPY ./poetry.lock ./
COPY ./pyproject.toml ./

RUN pip install poetry==1.2.1
RUN poetry config virtualenvs.create false
RUN poetry install --only main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
