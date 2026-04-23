import time
from fastapi import FastAPI, Request
from app.routes.monitoring import router as monitoring_router
from app.routes.predict import protected_router as predict_router
from app.routes.auth import router as auth_router
from app.core.monitoring import setup_logging, record_request, logger

setup_logging()

app = FastAPI(
    title="Boston Housing Price Prediction API",
    description="API para predicción de precios de viviendas usando un modelo entrenado en Boston Housing",
    version="0.1.0"
)

app.include_router(predict_router)
app.include_router(monitoring_router)
app.include_router(auth_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    record_request()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        "method=%s path=%s status=%d duration_ms=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/")
def home():
    return {"message": "API funcionando"}
