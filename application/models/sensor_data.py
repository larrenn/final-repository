from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    device_id: int
    timestamp: int
    temperature: float
    humidity: float
    pressure: int
    status: int

    class Config:
        schema_extra = {
            "example": {
                "device_id": 1234567890,
                "timestamp": 1690000000,
                "temperature": 23.5,
                "humidity": 45.2,
                "pressure": 1013,
                "status": 1
            }
        }

class SensorDataDB(SensorData):
    id: Optional[int] = None
    received_at: Optional[datetime] = None
    synced: Optional[bool] = False