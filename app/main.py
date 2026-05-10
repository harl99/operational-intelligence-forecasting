from fastapi import FastAPI
from pydantic import BaseModel
import random


app = FastAPI(
    title="Operational Intelligence Forecasting API",
    description="""
Enterprise-style forecasting and operational intelligence API
for industrial energy analytics and predictive operations.
""",
    version="1.0.0"
)


class ForecastRequest(BaseModel):
    production_throughput_units: float
    ambient_temperature_c: float
    maintenance_event: int = 0
    anomaly_event: int = 0


@app.get("/")
def root():
    return {
        "message": "Operational Intelligence Forecasting API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/forecast")
def forecast_energy(request: ForecastRequest):

    base_energy = 450

    throughput_load = (
        request.production_throughput_units * 2.7
    )

    temperature_load = (
        max(request.ambient_temperature_c - 28, 0) * 9
    )

    maintenance_adjustment = (
        -180 if request.maintenance_event == 1 else 0
    )

    anomaly_adjustment = (
        random.uniform(50, 120)
        if request.anomaly_event == 1
        else 0
    )

    predicted_energy_kwh = (
        base_energy
        + throughput_load
        + temperature_load
        + maintenance_adjustment
        + anomaly_adjustment
    )

    predicted_cost_usd = (
        predicted_energy_kwh * 0.13
    )

    return {
        "predicted_energy_kwh": round(predicted_energy_kwh, 2),
        "predicted_cost_usd": round(predicted_cost_usd, 2),
        "operational_status": (
            "high_load"
            if predicted_energy_kwh > 850
            else "normal"
        )
    }
