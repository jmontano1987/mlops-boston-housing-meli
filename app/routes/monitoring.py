from fastapi import APIRouter
from app.core.monitoring import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():
    return get_metrics()



@router.get("/health")
def health_check():
    return {"status": "ok"}
