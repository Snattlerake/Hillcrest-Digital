
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.booking_service import (
    create_appointment,
    get_appointments,
    get_appointment,
    cancel_appointment,
    reschedule_appointment,
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


class AppointmentCreate(BaseModel):
    service: str
    starts_at: datetime
    duration_minutes: int
    provider_name: str
    customer_name: str
    customer_phone: str
    notes: str | None = None


class AppointmentReschedule(BaseModel):
    starts_at: datetime


@router.post("/")
def create_new_appointment(
    company_id: int,
    appointment: AppointmentCreate
):
    try:
        return create_appointment(
            company_id=company_id,
            **appointment.model_dump()
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/")
def list_appointments(
    company_id: int,
    start_date: datetime,
    end_date: datetime
):
    if start_date >= end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date."
        )

    return get_appointments(company_id, start_date, end_date)


@router.get("/{appointment_id}")
def retrieve_appointment(
    appointment_id: int,
    company_id: int
):
    appointment = get_appointment(company_id, appointment_id)

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    company_id: int
):
    appointment = cancel_appointment(company_id, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found or already cancelled"
        )

    return appointment


@router.patch("/{appointment_id}/reschedule")
def reschedule_existing_appointment(
    appointment_id: int,
    company_id: int,
    request: AppointmentReschedule
):
    try:
        appointment = reschedule_appointment(
            company_id,
            appointment_id,
            request.starts_at
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found or already cancelled"
        )

    return appointment
