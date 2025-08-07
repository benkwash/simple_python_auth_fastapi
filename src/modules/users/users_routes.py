from fastapi import APIRouter, status, Request
from .users_requests_and_responses import (
    UserSignInRequest, 
    UserSignUpRequest, 
    UserResponse,
    VerificationCodeRequest,
    SigninResponse
)
from .services import (
    sign_in, 
    sign_up, 
    process_verification_code,
    get_user_details
)
v1_routes = APIRouter()
v1_public_routes = APIRouter()

@v1_public_routes.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up_controller(data: UserSignUpRequest):
    data = await sign_up(data)
    return data

@v1_public_routes.post("/login", response_model=SigninResponse, status_code=status.HTTP_200_OK)
async def sign_in_controller(data: UserSignInRequest):
    token = await sign_in(data)
    return {"token": token}

@v1_public_routes.post("/verify-code", status_code=status.HTTP_200_OK)
async def verify_code_controller(data: VerificationCodeRequest):
    message = await process_verification_code(data)
    return message

@v1_routes.get("/me", status_code=status.HTTP_200_OK)
async def me_controller(request: Request):
    user = request.state.user
    user = await get_user_details(user["phoneNumber"])
    return user

public_user_routes = APIRouter(
    prefix="/v1/auth", 
    tags=["Public User API"],
)
public_user_routes.include_router(v1_public_routes)


user_routes = APIRouter(
    prefix="/v1/users", 
    tags=["User API"],
)
user_routes.include_router(v1_routes)

