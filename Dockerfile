FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

RUN apt update && apt install -y curl && apt install -y net-tools && addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

COPY handlers/ handlers/
COPY logger/ logger/
COPY sqdb/ sqdb/
COPY config.py .
COPY main.py .

USER app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
