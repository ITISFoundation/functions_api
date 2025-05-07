from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel


class Function(BaseModel):
    id: Optional[int] = None
    name: str
    type: str
    url: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None  # JSON Schema ## TODO improve typing
    output_schema: Optional[Dict[str, Any]] = None  # JSON Schema
    tags: Optional[List[str]] = None  # Added tags field

class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class FunctionJob(BaseModel):
    id: Optional[int] = None
    functionID: int
    status: Optional[JobStatus] = JobStatus.PENDING
    inputs: Optional[dict] = None
    outputs: Optional[dict] = None
    job_info: Optional[dict] = None
    created_at: Optional[datetime] = None


class FunctionJobCollection(BaseModel):
    """Model for a collection of function jobs"""

    id: Optional[int]
    name: str
    description: Optional[str]
    job_ids: List[int]
    status: str

    class Config:
        from_attributes = True
