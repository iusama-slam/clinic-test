"""One evening run: confirmations out, call list printed, freed slots offered."""
import sys
from datetime import date, timedelta

from app.reminders import build_reminders, needs_call
from app.schedule import load_appointments
from app.sms import ConsoleSender
from app.waitlist import load_waitlist, offer_freed_slots


def main(appointments_csv: str, waitlist_csv: str) -> None:
    tomorrow = date.today() + timedelta(days=1)
    appointments = load_appointments(appointments_csv, tomorrow)
    sender = ConsoleSender()
    for reminder in build_reminders(appointments):
        sender.send(reminder.phone, reminder.text)
    calls = [a for a in appointments if needs_call(a)]
    print(f"{len(appointments)} appointments, {len(calls)} still need a call")
    for appointment in calls:
        print(f"  call {appointment.patient} ({appointment.location}) about {appointment.time}")
    offers = offer_freed_slots(appointments, load_waitlist(waitlist_csv))
    for offer in offers:
        sender.send(offer.phone, offer.text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python run.py appointments.csv waitlist.csv")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
