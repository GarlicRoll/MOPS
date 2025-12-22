from pymongo import MongoClient
import os
from datetime import datetime, timezone

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "iot_db")
MONGO_COLLECTION = os.getenv("MONGO_ALERTS_COLLECTION", "alerts")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
alerts = db[MONGO_COLLECTION]

def save_alert(alert: dict):
    alert["timestamp"] = int(datetime.utcnow().timestamp())
    alerts.insert_one(alert)
