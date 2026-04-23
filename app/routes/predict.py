from fastapi import APIRouter, Depends
from app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from app.services.model_service import model_service
from app.core.monitoring import (
    record_prediction,
    record_input,
    detect_drift,
    logger
)
from app.security.auth import verify_token
import uuid
import time

protected_router = APIRouter(dependencies=[Depends(verify_token)])

@protected_router.post("/predict")
def predict(request: PredictionRequest) -> PredictionResponse:
    data = request.model_dump()
    # Registro de input para monitoreo
    record_input(data)
    # Detección de drift
    alerts = detect_drift(data)
    if alerts:
        logger.warning(f"Drift detectado: {alerts}")
        
    # Predicción usando el servicio de modelo
    start = time.time()
    prediction = model_service.predict(data)
    latency = (time.time() - start) * 1000  # Latencia en ms
    
    # ID único para la solicitud
    request_id = str(uuid.uuid4())
    logger.info(f"Predicción realizada con request_id: {request_id}, input: {data}, prediction: {prediction}")
    
    record_prediction(prediction)
    return PredictionResponse(prediction=prediction, request_id=request_id, latency_ms=latency, drift_alerts=alerts)

