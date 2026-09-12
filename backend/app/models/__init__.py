"""Domain models (planned).

Future iterations:
  venue.py   -> Venue
  court.py   -> Court (FK -> Venue)
  slot.py    -> Schedule/Slot (FK -> Court, start/end, price)
  booking.py -> Booking (FK -> Slot, customer, conflict guard)
  payment.py -> Payment (FK -> Booking, deposit/paid)
"""
