FROM python:3.10-slim

WORKDIR /app

# installing poetry
RUN pip install "poetry==1.3.2"

# copy poetry metadata
COPY poetry.lock .
COPY pyproject.toml .

COPY script/ .

RUN poetry config virtualenvs.create false && \
    poetry install --only script

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]