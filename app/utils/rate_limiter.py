from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time


# Simple in-memory rate limiter (per IP)
RATE_LIMIT_STORAGE = {}


def rate_limit(max_requests: int, period: int):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            ip = request.client.host
            now = time.time()
            if ip not in RATE_LIMIT_STORAGE:
                RATE_LIMIT_STORAGE[ip] = []
            RATE_LIMIT_STORAGE[ip] = [t for t in RATE_LIMIT_STORAGE[ip] if now - t < period]
            if len(RATE_LIMIT_STORAGE[ip]) >= max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            RATE_LIMIT_STORAGE[ip].append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator