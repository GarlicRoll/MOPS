FROM python:3.13

WORKDIR /app

COPY iot_controller/requirements.txt .
RUN pip install -r requirements.txt

COPY iot_controller/app app
COPY common common

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]