
from app.database import get_connection


def get_business_hours(company_id: int):
    """Retrieve a company's weekly business hours."""

    query = """
        SELECT *
        FROM business_hours
        WHERE company_id = %s
        ORDER BY day_of_week;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (company_id,))
            return cur.fetchall()


def set_business_hours(
    company_id: int,
    day_of_week: int,
    opens_at,
    closes_at,
    is_closed: bool = False,
):
    """Create or update business hours for a weekday."""

    if day_of_week not in range(7):
        raise ValueError("Day of week must be between 0 and 6.")

    if not is_closed:
        if opens_at is None or closes_at is None:
            raise ValueError("Opening and closing times are required.")

        if opens_at >= closes_at:
            raise ValueError("Closing time must be after opening time.")

    query = """
        INSERT INTO business_hours (
            company_id,
            day_of_week,
            opens_at,
            closes_at,
            is_closed
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (company_id, day_of_week)
        DO UPDATE SET
            opens_at = EXCLUDED.opens_at,
            closes_at = EXCLUDED.closes_at,
            is_closed = EXCLUDED.is_closed
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    company_id,
                    day_of_week,
                    opens_at,
                    closes_at,
                    is_closed,
                ),
            )
            return cur.fetchone()
