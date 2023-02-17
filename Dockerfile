FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-slim

WORKDIR /app

COPY /handlers /handlers
COPY /sqdb /sqdb
COPY .env .env
COPY config.py config.py
COPY main.py main.py
COPY script.py script.py

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

CMD ["bash"]