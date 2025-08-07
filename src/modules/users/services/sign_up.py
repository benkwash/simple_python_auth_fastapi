from fastapi import HTTPException
import secrets
from datetime import datetime, timezone
from ..users_requests_and_responses import UserSignUpRequest, UserResponse
from ..model.user_schema import UserSchema, AccountStatus, VerificationMethod
from ..model.user_repo import insert_user, insert_verification_code
from ....utils.security import hash_password, generate_verification_code
from ....utils.phone_number import parse_phone_number
from .send_verification_code import send_verification_code
from ...logger.services import log_event
from ...logger.model.logger_schema import LogEvent

async def sign_up(data: UserSignUpRequest):    
    user = data.model_dump(exclude_unset=True)
    
    phoneNumber = parse_phone_number(data.phoneNumber)

    hashedPassword = hash_password(data.password)
    

    userId = secrets.token_urlsafe(16)

    userData = {
        "userId": userId,
        "name": data.name,
        "email": data.email,
        "phoneNumber": phoneNumber,
        "password": hashedPassword,
        "address": data.address,
        "referralCodeUsed": data.referralCode,
        "accountStatus": AccountStatus.INACTIVE.value,
        "verificationStatus": False,
        "loginAttempts": 0,
        "lockedUntil": None,
        "lastLogin": None,
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc),
    }

    verificationCode = generate_verification_code()

    
    await insert_user(userData)
    await insert_verification_code({
        "phoneNumber": phoneNumber, 
        "verificationCode": verificationCode, 
        "verificationMethod": data.verificationMethod,

    })

    await log_event({
        "userId": userId,
        "eventType": LogEvent.USER_REGISTERED.value,
        "phoneNumber": phoneNumber,
        "verificationMethod": data.verificationMethod
    })

    await send_verification_code(phoneNumber, verificationCode, data.verificationMethod)
    
    
    return UserResponse(
        userId=userData["userId"],
        phoneNumber=userData["phoneNumber"],
        email=userData["email"],
        name=userData["name"],
        accountStatus=userData["accountStatus"],
        verificationStatus=userData["verificationStatus"],
        createdAt=userData["createdAt"],
    )