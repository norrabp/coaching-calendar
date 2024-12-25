from enum import Enum

class AppointmentStatus(str, Enum):
    OPEN = 'OPEN'
    SCHEDULED = 'SCHEDULED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
