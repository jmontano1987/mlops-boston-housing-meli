import logging
from collections import deque
from threading import Lock

logger = logging.getLogger("boston_housing")

_lock = Lock()
_metrics: dict = {
    "total_requests": 0,
    "total_predictions": 0,
    "prediction_values": deque(maxlen=1000),
}

_baseline = {
    "RM": {"mean": 6.2, "std": 0.7},
    "LSTAT": {"mean": 12.5, "std": 5.0},
}

_input_buffer = deque(maxlen=1000)

def record_input(data: dict) -> None:
    with _lock:
        _input_buffer.append(data)
        

def detect_drift(data: dict) -> list:
    alerts = []

    for feature, stats in _baseline.items():
        value = data.get(feature)

        if value is None:
            continue

        if stats["std"] == 0:
            continue

        z_score = abs((value - stats["mean"]) / stats["std"])

        if z_score > 3:
            alerts.append(f"Drift detectado en {feature}")

    return alerts
        
def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def record_request() -> None:
    with _lock:
        _metrics["total_requests"] += 1


def record_prediction(value: float) -> None:
    with _lock:
        _metrics["total_predictions"] += 1
        _metrics["prediction_values"].append(value)


def get_metrics() -> dict:
    with _lock:
        values = list(_metrics["prediction_values"])
    avg = round(sum(values) / len(values), 4) if values else None
    return {
        "total_requests": _metrics["total_requests"],
        "total_predictions": _metrics["total_predictions"],
        "avg_prediction": avg,
        "min_prediction": round(min(values), 4) if values else None,
        "max_prediction": round(max(values), 4) if values else None,
    }
