from pydantic import BaseModel, Field
from datetime import datetime

class IoTPacket(BaseModel):
    device_id: int = Field(..., description="ID устройства")
    A: float = Field(..., description="Значение поля A")
    B: float = Field(..., description="Значение поля B")
    timestamp: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
