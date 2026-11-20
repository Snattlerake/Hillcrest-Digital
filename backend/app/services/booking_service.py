
from datetime import datetime, timedelta, timezone

from app.database import get_connection


def create_appointment(
    company_id: int,
    service: str,
    starts_at: datetime,
    duration_minutes: int,
    provider_name: str,
    customer_name: str,
    customer_phone: str,
    notes: str | None = None,
):
    """Create and save a new appointment."""

    if duration_minutes < 15 or duration_minutes % 15 != 0:
        raise ValueError("Duration must be a multiple of 15 minutes.")

    if starts_at.minute % 15 != 0 or starts_at.second != 0:
        raise ValueError("Appointments must start on 15-minute intervals.")

    if starts_at.tzinfo is None:
        raise ValueError("Appointment time must include a timezone.")

    query = """
        INSERT INTO appointments (
            company_id,
            service,
            starts_at,
            duration_minutes,
            provider_name,
            customer_name,
            customer_phone,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    company_id,
                    service,
                    starts_at,
                    duration_minutes,
                    provider_name,
                    customer_name,
                    customer_phone,
                    notes,
                ),
            )
            return cur.fetchone()


def get_appointments(
    company_id: int,
    start_date: datetime,
    end_date: datetime,
):
    """Retrieve a company's appointments within a date range."""

    query = """
        SELECT *
        FROM appointments
        WHERE company_id = %s
          AND starts_at >= %s
          AND starts_at < %s
        ORDER BY starts_at ASC;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (company_id, start_date, end_date))
            return cur.fetchall()


def get_appointment(company_id: int, appointment_id: int):
    """Retrieve one appointment belonging to a company."""

    query = """
        SELECT *
        FROM appointments
        WHERE company_id = %s
          AND id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (company_id, appointment_id))
            return cur.fetchone()


def cancel_appointment(company_id: int, appointment_id: int):
    """Cancel an appointment without deleting its history."""

    query = """
        UPDATE appointments
        SET status = 'cancelled'
        WHERE company_id = %s
          AND id = %s
          AND status = 'booked'
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (company_id, appointment_id))
            return cur.fetchone()


def reschedule_appointment(
    company_id: int,
    appointment_id: int,
    new_starts_at: datetime,
):
    """Change the start time of an existing appointment."""

    if new_starts_at.tzinfo is None:
        raise ValueError("Appointment time must include a timezone.")

    if new_starts_at.minute % 15 != 0 or new_starts_at.second != 0:
        raise ValueError("Appointments must start on 15-minute intervals.")

    query = """
        UPDATE appointments
        SET starts_at = %s
        WHERE company_id = %s
          AND id = %s
          AND status = 'booked'
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (new_starts_at, company_id, appointment_id),
            )
            return cur.fetchone()
