from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...users.model.user_schema import VerificationMethod
from pydantic import BaseModel

class LogEvent(str, Enum):
    USER_REGISTERED = "user_registered"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    ACCOUNT_LOCKED = "account_locked"
    VERIFICATION_SENT = "verification_sent"
    VERIFICATION_SUCCESS = "verification_success"
    VERIFICATION_FAILED = "verification_failed"

class LogModel(BaseModel):
    userId: Optional[str]
    eventType: LogEvent
    phoneNumber: Optional[str]
    verificationMethod: Optional[VerificationMethod]
    timestamp: datetime

@dataclass
class LoggerSchema:
    userId: Optional[str]
    eventType: LogEvent
    phoneNumber: Optional[str]
    verificationMethod: Optional[VerificationMethod]
    timestamp: datetime

