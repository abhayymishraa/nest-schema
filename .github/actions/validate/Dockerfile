FROM python:3.13.5-alpine

WORKDIR /action

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY validate.py entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/action/entrypoint.sh"]
