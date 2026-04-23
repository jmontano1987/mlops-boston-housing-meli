from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    CRIM: float = Field(..., example=0.1)
    ZN: float = Field(..., example=18)
    INDUS: float = Field(..., example=2.3)
    CHAS: int = Field(..., example=0)
    NOX: float = Field(..., example=0.5)
    RM: float = Field(..., example=6.5)
    AGE: float = Field(..., example=65)
    DIS: float = Field(..., example=4.2)
    RAD: int = Field(..., example=1)
    TAX: float = Field(..., example=300)
    PTRATIO: float = Field(..., example=15)
    B: float = Field(..., example=390)
    LSTAT: float = Field(..., example=10)


class PredictionResponse(BaseModel):
    prediction: float
    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    latency_ms: float = Field(..., example=50.5)
    drift_alerts: list[str] = Field(default_factory=list, example=["Feature 'RM' has drifted significantly."])