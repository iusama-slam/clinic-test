"""Confirmation messages and the evening call list."""
from dataclasses import dataclass
from datetime import datetime

from app.schedule import Appointment

CUTOFF_HOUR = 20


@dataclass
class Reminder:
    appointment_id: str
    phone: str
    text: str


def message_for(appointment: Appointment) -> str:
    when = appointment.time.strftime("%-I:%M %p")
    return (
        f"Hi {appointment.patient.split()[0]}, this is {appointment.location} Dental. "
        f"You have an appointment tomorrow at {when}. Reply C to confirm or X to cancel."
    )


def build_reminders(appointments: list[Appointment]) -> list[Reminder]:
    return [
        Reminder(a.id, a.phone, message_for(a))
        for a in appointments
        if a.phone and a.status == "booked"
    ]


def needs_call(appointment: Appointment, now: datetime | None = None) -> bool:
    """A patient still needs a phone call when we cannot text them, or when
    the evening cutoff has passed without a reply."""
    if appointment.status != "booked":
        return False
    if not appointment.phone:
        return True
    current = now or datetime.now()
    return current.hour >= CUTOFF_HOUR
