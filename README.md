# Clinic Reminders

A small service for a dental clinic with three locations. Every evening the
front desk confirms the next day's appointments by phone; this tool sends the
confirmations by SMS instead and fills cancelled slots from a waitlist.

## What is here

- `app/schedule.py` loads tomorrow's appointments from the practice export (CSV).
- `app/reminders.py` builds the confirmation message for each patient and
  decides who still needs a call (no phone number, or no reply by 20:00).
- `app/waitlist.py` offers a freed slot to the first matching waitlist entry.
- `app/sms.py` is the sending boundary; only the console sender is wired today.
- `run.py` ties it together for one evening run.

## Run

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python run.py data/appointments.csv data/waitlist.csv
pytest
```

## Known gaps

- Replies are not read back yet: a patient's "C" or "X" has to be keyed in by hand.
- The waitlist match ignores the location, so a Northside patient can be offered a Harbour slot.
- Twilio is not wired; `ConsoleSender` prints instead of sending.
