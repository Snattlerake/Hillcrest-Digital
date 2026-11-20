
from fastapi import FastAPI

from app.api.routes import appointments

app = FastAPI(
    title="Hillcrest Digital API",
    description="Backend API for Hillcrest Digital",
    version="1.0.0"
)

app.include_router(appointments.router)


@app.get("/")
def root():
    return {
        "message": "Hillcrest Digital API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
