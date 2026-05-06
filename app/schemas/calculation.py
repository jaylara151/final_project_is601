from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CalculationCreate(BaseModel):
    first_number: float
    second_number: float
    operation: str
    note: Optional[str] = ""


class CalculationUpdate(BaseModel):
    note: str


class CalculationResponse(BaseModel):
    id: int
    first_number: float
    second_number: float
    operation: str
    result: float
    note: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CalculationReport(BaseModel):
    total_calculations: int
    average_result: float | None
    highest_result: float | None
    lowest_result: float | None
    most_common_operation: str | None
    latest_result: float | None