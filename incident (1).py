from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentCreate(BaseModel):
    title: str
    description: str
    service: str
    severity: str


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    service: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    incident_id: str
    title: str
    description: str
    service: str
    severity: str
    status: str
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True