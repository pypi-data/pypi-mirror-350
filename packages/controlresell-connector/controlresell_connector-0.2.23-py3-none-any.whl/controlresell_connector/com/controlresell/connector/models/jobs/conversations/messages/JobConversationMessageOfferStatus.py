from enum import Enum

class JobConversationMessageOfferStatus(str, Enum):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'
