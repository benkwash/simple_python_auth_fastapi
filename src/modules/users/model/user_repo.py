from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from datetime import datetime , timedelta, timezone
from ....config.db import dbClient
from ....config.env import SMS_CODE_EXPIRE_MINUTES

USERS_COLLECTION = "users"
VERIFICATION_CODES_COLLECTION = "verificationCodes"

user = dbClient[USERS_COLLECTION]
verificationCode = dbClient[VERIFICATION_CODES_COLLECTION]

async def create_indexes():
    await user.create_index([("userId", ASCENDING)], unique=True)
    await user.create_index([("name", ASCENDING)])
    await user.create_index([("email")], unique=True)
    await user.create_index([("phoneNumber")], unique=True)

    await verificationCode.create_index([("phoneNumber", ASCENDING)])
    await verificationCode.create_index([("expiresAt", ASCENDING)], expireAfterSeconds=0)

async def insert_user(data: dict):
    try:
        userDetails = await user.insert_one(data)
        return str(userDetails.inserted_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User already exists")

async def insert_verification_code(data: dict):
    expiresAt = datetime.now(timezone.utc) + timedelta(minutes=SMS_CODE_EXPIRE_MINUTES)
    try:
        verificationCodeDetails = await verificationCode.update_one({
            "phoneNumber": data["phoneNumber"]}, 
            {
                "$set": {
                    **data,
                    "verified": False,
                    "createdAt": datetime.now(timezone.utc),
                    "expiresAt": expiresAt

                }
             }, 
            upsert=True
        )
        return verificationCodeDetails
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Verification code already exists")

async def get_verification_code(phoneNumber: str, code: str,verified: bool=False):
    return await verificationCode.find_one({
        "phoneNumber": phoneNumber,
        "verificationCode": code,
        "verified": verified,
        "expiresAt": {"$gt": datetime.now(timezone.utc)}
    })

async def update_verification_code(phoneNumber: str, data: dict):
    return await verificationCode.update_one({"phoneNumber": phoneNumber}, {"$set": data})

async def get_user_by_email(email: str):
    return await user.find_one({"email": email})

async def get_user_by_number(email: str):
    return await user.find_one({"phoneNumber": email})

async def get_user_by_email_or_number(email: str, phoneNumber: str):
    return await user.find_one({"$or": [{"email": email}, {"phoneNumber": phoneNumber}]})

async def get_user_by_id(userId: str):
    return await user.find_one({"_id": userId})

async def get_users_by_vendorId(vendorId: str):
    return await user.find({"vendorId": vendorId})


async def update_user_by_number(phoneNumber: str, data: dict):
    return await user.update_one({"phoneNumber": phoneNumber}, {"$set": data})

