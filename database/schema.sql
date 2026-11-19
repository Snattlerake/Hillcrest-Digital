
-- =====================================================
-- HILLCREST DIGITAL - DATABASE SCHEMA
-- =====================================================

-- 1. USERS
-- Two accounts per company:
-- company_admin and employee

CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    company_id BIGINT NOT NULL,

    username VARCHAR(100) NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    role VARCHAR(30) NOT NULL
        CHECK (role IN ('company_admin', 'employee')),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_company
    ON users(company_id);


-- 2. APPOINTMENTS

CREATE TABLE appointments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    company_id BIGINT NOT NULL,

    service TEXT NOT NULL,

    starts_at TIMESTAMPTZ NOT NULL,

    duration_minutes INTEGER NOT NULL
        CHECK (
            duration_minutes >= 15
            AND duration_minutes % 15 = 0
        ),

    provider_name TEXT NOT NULL,

    customer_name TEXT NOT NULL,

    customer_phone TEXT NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'booked'
        CHECK (
            status IN ('booked', 'cancelled', 'completed')
        ),

    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CHECK (
        EXTRACT(MINUTE FROM starts_at)::INTEGER % 15 = 0
        AND EXTRACT(SECOND FROM starts_at) = 0
    )
);

CREATE INDEX idx_appointments_company_date
    ON appointments(company_id, starts_at);

CREATE INDEX idx_appointments_company_status
    ON appointments(company_id, status);


-- 3. BUSINESS HOURS

CREATE TABLE business_hours (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    company_id BIGINT NOT NULL,

    day_of_week SMALLINT NOT NULL
        CHECK (day_of_week BETWEEN 0 AND 6),

    opens_at TIME,

    closes_at TIME,

    is_closed BOOLEAN NOT NULL DEFAULT FALSE,

    CHECK (
        (is_closed = TRUE)
        OR
        (
            opens_at IS NOT NULL
            AND closes_at IS NOT NULL
            AND opens_at < closes_at
        )
    ),

    UNIQUE(company_id, day_of_week)
);


-- 4. SMS NOTIFICATIONS

CREATE TABLE sms_notifications (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    appointment_id BIGINT NOT NULL
        REFERENCES appointments(id) ON DELETE CASCADE,

    provider_message_id TEXT,

    scheduled_for TIMESTAMPTZ NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'scheduled',
                'sent',
                'delivered',
                'failed',
                'cancelled'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sms_appointment
    ON sms_notifications(appointment_id);

CREATE INDEX idx_sms_scheduled
    ON sms_notifications(status, scheduled_for);


-- =====================================================
-- END OF SCHEMA
-- =====================================================
