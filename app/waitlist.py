"""Offer freed slots to the waitlist."""
import csv
from dataclasses import dataclass

from app.schedule import Appointment


@dataclass
class WaitlistEntry:
    patient: str
    phone: str
    location: str
    earliest: str  # HH:MM


@dataclass
class Offer:
    phone: str
    text: str


def load_waitlist(path: str) -> list[WaitlistEntry]:
    with open(path, newline="") as handle:
        return [WaitlistEntry(r["patient"], r["phone"], r["location"], r["earliest"]) for r in csv.DictReader(handle)]


def offer_freed_slots(appointments: list[Appointment], waitlist: list[WaitlistEntry]) -> list[Offer]:
    offers: list[Offer] = []
    remaining = list(waitlist)
    for appointment in appointments:
        if appointment.status != "cancelled":
            continue
        slot = appointment.time.strftime("%H:%M")
        for entry in remaining:
            if entry.earliest <= slot:
                offers.append(Offer(entry.phone, f"A slot opened tomorrow at {slot} at {appointment.location} Dental. Reply Y to take it."))
                remaining.remove(entry)
                break
    return offers
