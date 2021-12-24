FROM python:3.9-alpine
ENV TZ=UTC

RUN apk add --update --no-cache \
    alpine-sdk \
    build-base \
    libffi-dev \
    mysql-dev \
    postgresql-dev \
    python3-dev \
    tzdata

RUN addgroup -g 1000 app && \
    adduser -S -H -h /app -s /sbin/nologin -u 1000 -G app app

WORKDIR /app

COPY --chown=app:app requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app /data && chown app:app /app /data
COPY --chown=app:app . .

USER app
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
