from ..model.user_repo import( 
    get_verification_code, 
    update_verification_code, 
    get_user_by_number,
    update_user_by_number
)
from ..model.user_schema import AccountStatus
from fastapi import HTTPException
from ..users_requests_and_responses import VerificationCodeRequest
from ....utils.phone_number import parse_phone_number
from ...logger.services import log_event
from ...logger.model.logger_schema import LogEvent

async def verify_code(phoneNumber: str, code: str):
    verification = await get_verification_code(phoneNumber, code)
        
    if verification:
        await update_verification_code(
            phoneNumber,
            {"verified": True}
        )
        return True
    return False

async def process_verification_code(data: VerificationCodeRequest):
    phoneNumber = parse_phone_number(data.phoneNumber)

    verified = await verify_code(phoneNumber, data.verificationCode)
    if not verified:
        await log_event({
            "eventType": LogEvent.VERIFICATION_FAILED.value,
            "phoneNumber": phoneNumber,
        })
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user = await get_user_by_number(phoneNumber)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await update_user_by_number(phoneNumber, {
        "accountStatus": AccountStatus.ACTIVE.value,
        "verificationStatus": True
    })
    # log
    await log_event({
        "eventType": LogEvent.VERIFICATION_SUCCESS.value,
        "phoneNumber": phoneNumber,
    })
    return {"message": "Verification successful! Login to continue."}
    
    