from abc import ABC, abstractmethod
import asyncio
import logging

class NotificationService(ABC):
    @abstractmethod
    async def send_verification_code(self, phone_number: str, code: str) -> bool:
        pass

class SMSService(NotificationService):
    async def send_verification_code(self, phone_number: str, code: str) -> bool:
        await asyncio.sleep(0.1) 
        logging.info(f"SMS sent to {phone_number}: {code}")
        return True

class WhatsAppService(NotificationService):
    async def send_verification_code(self, phone_number: str, code: str) -> bool:
        await asyncio.sleep(0.1)
        logging.info(f"WhatsApp message sent to {phone_number}: {code}")
        return True