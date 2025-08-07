from enum import Enum
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

class VerificationMethod(str, Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"

class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    LOCKED = "locked"

@dataclass
class Token:
    userId: str
    email: EmailStr
    phoneNumber: str

@dataclass
class UserSchema:
    userId: str
    name: str
    email: EmailStr
    phoneNumber: str
    password: str
    address: str
    accountStatus: AccountStatus
    verificationStatus: bool
    referralCodeUsed: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    loginAttempts: int = 0
    lockedUntil: Optional[datetime] = None
    lastLogin: Optional[datetime] = None

@dataclass
class VerificationCodeSchema:
    phoneNumber: str
    verificationCode: str
    verificationMethod: VerificationMethod
    expiresAt: datetime
    createdAt: datetime