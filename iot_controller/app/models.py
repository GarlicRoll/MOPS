from pydantic import BaseModel, Field
from datetime import datetime

class IoTPacket(BaseModel):
    device_id: int = Field(..., description="ID устройства")
    battery: float = Field(..., description="Уровень заряда батареи устройства")
    temperature: float = Field(..., description="Температура устройства")
    timestamp: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
