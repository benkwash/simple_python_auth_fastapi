from fastapi import Request, HTTPException
from starlette.datastructures import MutableHeaders
import time

RATE_LIMIT_PER_MINUTE = 5
RATE_LIMIT_WINDOW_SECONDS = 60
IPRequests = {}

async def rate_limiter(request: Request):
    clientIP = request.client.host
    now = time.time()

    if clientIP not in IPRequests:
        IPRequests[clientIP] = []

    IPRequests[clientIP] = [t for t in IPRequests[clientIP] if now - t < RATE_LIMIT_WINDOW_SECONDS]

    if len(IPRequests[clientIP]) >= RATE_LIMIT_PER_MINUTE:
        wait_time = int(RATE_LIMIT_WINDOW_SECONDS - (now - IPRequests[clientIP][0]))
        
        response_headers = {"X-RateLimit-Retry-After": str(wait_time)}
        
        mutable_headers = MutableHeaders(response_headers)
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests. Please try again later.",
            headers=mutable_headers,
        )

    IPRequests[clientIP].append(now)

    return

