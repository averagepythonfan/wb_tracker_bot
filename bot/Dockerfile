FROM python:3.10-slim

WORKDIR /app

# installing poetry
RUN pip install "poetry==1.3.2"

# copy poetry metadata
COPY poetry.lock .
COPY pyproject.toml .

COPY bot/ .

RUN poetry config virtualenvs.create false && \
    poetry install --only bot

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]