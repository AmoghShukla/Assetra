from enum import Enum

class RoleName(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ORG_ADMIN = "ORG_ADMIN"
    IT_ADMIN = "IT_ADMIN"
    EMPLOYEE = "EMPLOYEE"


class AssetStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ALLOCATED = "ALLOCATED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    RETIRED = "RETIRED"


class TicketStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


TICKET_TRANSITIONS = {
    TicketStatus.TODO: [TicketStatus.IN_PROGRESS],
    TicketStatus.IN_PROGRESS: [TicketStatus.RESOLVED],
    TicketStatus.RESOLVED: [],
}

TICKET_MAX_DESCRIPTION_LENGTH = 1000
