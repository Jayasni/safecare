import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"