from enum import Enum
from datetime import time

class AppointmentStatus(str, Enum):
    OPEN = 'OPEN'
    SCHEDULED = 'SCHEDULED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

# Time slots between 8am and 5pm
DEFAULT_APPOINTMENT_SLOTS = [
    time(8, 0, 0),
    time(8, 15, 0),
    time(8, 30, 0),
    time(8, 45, 0),
    time(9, 0, 0),
    time(9, 15, 0),
    time(9, 30, 0),
    time(9, 45, 0),
    time(10, 0, 0),
    time(10, 15, 0),
    time(10, 30, 0),
    time(10, 45, 0),
    time(11, 0, 0),
    time(11, 15, 0),
    time(11, 30, 0),
    time(11, 45, 0),
    time(12, 0, 0),
    time(12, 15, 0),
    time(12, 30, 0),
    time(12, 45, 0),
    time(13, 0, 0),
    time(13, 15, 0),
    time(13, 30, 0),
    time(13, 45, 0),
    time(14, 0, 0),
    time(14, 15, 0),
    time(14, 30, 0),
    time(14, 45, 0),
    time(15, 0, 0),
]