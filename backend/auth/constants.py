from enum import Enum


class UserRole(str, Enum):
    COACH = "COACH",
    STUDENT = "STUDENT",
    ROOT = "ROOT"
