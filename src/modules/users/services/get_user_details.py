from ..model.user_repo import get_user_by_number
from ..users_requests_and_responses import UserResponse
from ....utils.phone_number import parse_phone_number

async def get_user_details(phoneNumber: str):
    number = parse_phone_number(phoneNumber)

    user = await get_user_by_number(number)

    return UserResponse(**user)