from fastapi import APIRouter,Depends
from .modules.users.users_routes import user_routes, public_user_routes
from .middlewares.jwt import auth_middleware
from .middlewares.rate_limiter import rate_limiter

public_routes = APIRouter(
    dependencies=[Depends(rate_limiter)],
)

routes = APIRouter(
    dependencies=[Depends(auth_middleware),Depends(rate_limiter)],
)


public_routes.include_router(public_user_routes)

routes.include_router(user_routes)