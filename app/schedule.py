"""Tomorrow's appointments, read from the practice management export."""
import csv
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Appointment:
    id: str
    patient: str
    phone: str
    location: str
    time: datetime
    status: str  # booked | confirmed | cancelled


def load_appointments(path: str, day: date) -> list[Appointment]:
    out: list[Appointment] = []
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            when = datetime.fromisoformat(row["time"])
            if when.date() != day:
                continue
            out.append(Appointment(
                id=row["id"],
                patient=row["patient"],
                phone=row.get("phone", "").strip(),
                location=row["location"],
                time=when,
                status=row.get("status", "booked"),
            ))
    return sorted(out, key=lambda a: a.time)
