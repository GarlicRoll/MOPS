from fastapi import FastAPI, HTTPException
from app.models import IoTPacket
from app.db import save_packet
from app.mq import publish_packet
from app.metrics import (
    PACKETS_RECEIVED,
    PACKETS_SAVED,
    PACKET_PROCESSING_TIME
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from common.logger import setup_logger

logger = setup_logger("iot_controller")
logger.info(f"IOT controller started")

app = FastAPI(title="IoT Controller")

@app.post("/packet")
async def ingest_packet(packet: IoTPacket):
    start = time.time()
    try:
        PACKETS_RECEIVED.inc()
        data = packet.dict()
        packet_id = save_packet(packet.dict())
        PACKETS_SAVED.inc()
        publish_packet(data)
        logger.info(f"ingest packet ok {packet_id}")
        return {"status": "ok", "id": packet_id}
    except Exception as e:
        logger.error(f"ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        PACKET_PROCESSING_TIME.observe(time.time() - start)

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/health")
async def health():
    logger.info(f"health check ok")
    return {"status": "ok"}