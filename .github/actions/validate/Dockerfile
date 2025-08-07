FROM python:3.13.5-alpine

WORKDIR /app

RUN pip install --no-cache-dir owasp-schema PyYAML

COPY validate.py entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
