from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from .model.user_schema import AccountStatus,VerificationMethod


class UserSignUpRequest(BaseModel):
    name: str = Field(..., description="User's name")
    email: EmailStr = Field(..., description="User's email address")
    phoneNumber: str = Field(..., description="User's phone number")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    address: Optional[str] = Field(..., description="User's address")
    referralCode: Optional[str] = Field(None, max_length=20)
    verificationMethod: VerificationMethod


class UserSignInRequest(BaseModel):
    phoneNumber: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    userId: str
    phoneNumber: str
    email: str
    name: str
    accountStatus: AccountStatus
    verificationStatus: bool
    createdAt: datetime

class VerificationCodeRequest(BaseModel):
    phoneNumber: str
    verificationCode: str

class SigninResponse(BaseModel):
    token: str