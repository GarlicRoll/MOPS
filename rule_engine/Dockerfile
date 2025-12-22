FROM python:3.13

WORKDIR /app

COPY rule_engine/requirements.txt .
RUN pip install -r requirements.txt

COPY rule_engine/app app
COPY rule_engine/config config
COPY common common

CMD ["python", "-m", "app.main"]
