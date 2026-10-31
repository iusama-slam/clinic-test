from datetime import datetime

from app.schedule import Appointment
from app.waitlist import WaitlistEntry, offer_freed_slots


def test_a_cancelled_slot_goes_to_the_first_patient_who_can_make_it():
    cancelled = Appointment("A3", "Priya Shah", "+15550102", "Harbour", datetime(2026, 11, 1, 10, 0), "cancelled")
    waitlist = [WaitlistEntry("Ana Costa", "+15550200", "Northside", "11:00"), WaitlistEntry("Liam Chen", "+15550201", "Harbour", "10:00")]
    offers = offer_freed_slots([cancelled], waitlist)
    assert [o.phone for o in offers] == ["+15550201"]
    assert "10:00 at Harbour Dental" in offers[0].text
