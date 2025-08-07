from ..users_requests_and_responses import UserSignInRequest
from ..model.user_repo import get_user_by_number,update_user_by_number
from ..model.user_schema import AccountStatus
from fastapi import HTTPException
from ....utils.security import verify_password, create_access_token
from ....config.env import MAX_LOGIN_ATTEMPTS, ACCOUNT_LOCKOUT_DURATION_MINUTES
from datetime import datetime, timezone, timedelta
from ....utils.phone_number import parse_phone_number
from ...logger.services import log_event
from ...logger.model.logger_schema import LogEvent

async def sign_in(data: UserSignInRequest):
    phoneNumber = parse_phone_number(data.phoneNumber)

    user = await get_user_by_number(phoneNumber)

    isPasswordValid = False
    if user:
        isPasswordValid = verify_password(data.password, user["password"])
        print("Password valid: ", isPasswordValid)

    if not user or not isPasswordValid:
        await log_event({
            "eventType": LogEvent.LOGIN_FAILED.value,
            "phoneNumber": phoneNumber,
            "reason": "invalid_credentials"
        })

        if user:
            newAttempt = user["loginAttempts"] + 1
            update = {
                "loginAttempts": newAttempt
            }

            if newAttempt >= MAX_LOGIN_ATTEMPTS:
                update["lockedUntil"] = datetime.now(timezone.utc) + timedelta(minutes=ACCOUNT_LOCKOUT_DURATION_MINUTES)
                update["accountStatus"] = AccountStatus.LOCKED.value

            await log_event({
                "eventType": LogEvent.ACCOUNT_LOCKED.value,
                "phoneNumber": phoneNumber,
                "userId": user["userId"],
            })
            await update_user_by_number(phoneNumber, update)

        raise HTTPException(status_code=404, detail="Invalid phone number or password!")
    
    if user["accountStatus"] == AccountStatus.SUSPENDED.value:
        raise HTTPException(status_code=403, detail="Account is suspended!")

    if user["accountStatus"] == AccountStatus.INACTIVE.value:
        raise HTTPException(status_code=403, detail="Account is not verified. Please verify your account!")

    lockedUntil = user["lockedUntil"]

    nowDate = datetime.now(timezone.utc)
    if lockedUntil and lockedUntil.replace(tzinfo=timezone.utc)> nowDate:
        raise HTTPException(status_code=423, detail="Account is locked until " + str(lockedUntil))
    
    # update login details and reset login attempts
    await update_user_by_number(phoneNumber, {
        "lastLogin": datetime.now(timezone.utc),
        "loginAttempts": 0,
        "lockedUntil": None,
        "accountStatus": AccountStatus.ACTIVE.value
    })
    
    await log_event({
        "eventType": LogEvent.LOGIN_SUCCESS.value,
        "phoneNumber": phoneNumber,
    })
    
    token = create_access_token({
        "phoneNumber": phoneNumber,
        "email": user["email"],
        "userId": user["userId"]
    })


    return token