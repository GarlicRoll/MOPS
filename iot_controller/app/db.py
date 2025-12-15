from pymongo import MongoClient
import os

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "iot_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "packets")

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def save_packet(packet: dict):
    result = collection.insert_one(packet)
    return str(result.inserted_id)