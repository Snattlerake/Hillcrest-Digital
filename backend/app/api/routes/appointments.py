
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.get("/")
def get_appointments():
    return {
        "message": "Appointment retrieval endpoint is working"
    }


@router.post("/")
def create_appointment():
    return {
        "message": "Appointment creation endpoint is working"
    }


@router.get("/{appointment_id}")
def get_appointment(appointment_id: int):
    return {
        "message": "Single appointment endpoint is working",
        "appointment_id": appointment_id
    }


@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: int):
    return {
        "message": "Appointment cancellation endpoint is working",
        "appointment_id": appointment_id
    }
