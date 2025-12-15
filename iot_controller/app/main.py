from fastapi import FastAPI, HTTPException
from app.models import IoTPacket
from app.db import save_packet
from app.mq import publish_packet

app = FastAPI(title="IoT Controller")

@app.post("/packet")
async def ingest_packet(packet: IoTPacket):
    try:
        data = packet.dict()
        packet_id = save_packet(packet.dict())
        publish_packet(data)
        return {"status": "ok", "id": packet_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}