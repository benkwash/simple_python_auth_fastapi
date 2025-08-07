from ....utils.notification_service import SMSService, WhatsAppService
from ..model.user_schema import VerificationMethod
from ...logger.services import log_event
from ...logger.model.logger_schema import LogEvent


async def send_verification_code(phoneNumber: str, code: str, verificationMethod: VerificationMethod) -> bool:
    if verificationMethod == VerificationMethod.SMS.value:
        await SMSService().send_verification_code(phoneNumber, code)
        await log_event({
            "eventType": LogEvent.VERIFICATION_SENT.value,
            "phoneNumber": phoneNumber,
            "verificationMethod": verificationMethod
        })
        
    elif verificationMethod == VerificationMethod.WHATSAPP.value:
        await WhatsAppService().send_verification_code(phoneNumber, code)
        await log_event({
            "eventType": LogEvent.VERIFICATION_SENT.value,
            "phoneNumber": phoneNumber,
            "verificationMethod": verificationMethod
        })

    

