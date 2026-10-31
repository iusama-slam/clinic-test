from datetime import datetime

from app.reminders import build_reminders, message_for, needs_call
from app.schedule import Appointment


def appointment(**overrides) -> Appointment:
    base = dict(id="A1", patient="Maria Lopez", phone="+15550100", location="Northside", time=datetime(2026, 11, 1, 9, 0), status="booked")
    base.update(overrides)
    return Appointment(**base)


def test_message_names_the_location_and_time():
    assert message_for(appointment()) == "Hi Maria, this is Northside Dental. You have an appointment tomorrow at 9:00 AM. Reply C to confirm or X to cancel."


def test_only_booked_patients_with_a_phone_get_a_text():
    reminders = build_reminders([appointment(), appointment(id="A2", phone=""), appointment(id="A3", status="confirmed")])
    assert [r.appointment_id for r in reminders] == ["A1"]


def test_call_list_before_and_after_the_cutoff():
    assert needs_call(appointment(phone=""))
    assert not needs_call(appointment(), now=datetime(2026, 10, 31, 19, 0))
    assert needs_call(appointment(), now=datetime(2026, 10, 31, 20, 0))
