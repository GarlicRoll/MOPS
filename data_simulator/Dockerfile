FROM python:3.13

WORKDIR /app

COPY data_simulator/requirements.txt .
RUN pip install -r requirements.txt

COPY data_simulator/app app
COPY data_simulator/config config
COPY common common

CMD ["python", "-m", "app.simulator"]
