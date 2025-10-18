from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.config import settings
from app.api.v1_router import router as api_router
import asyncio

app = FastAPI(title="Food Ordering Backend")


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Adds COOP and COEP headers to enable cross-origin isolation or compatible behavior."""
    response = await call_next(request)
    
    # Only apply to HTML responses, or just apply broadly if all pages need them
    # Applying broadly here is simplest for this context.
    response.headers["Cross-Origin-Opener-Policy"] = "restrict-properties"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"

    return response

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # your frontend (static HTML or Live Server)
        "http://localhost:5500",  # optional alias
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at the root
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/app")
async def health_check():
    return {"status": "ok"}

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_probe():
    return {"message": "Not implemented"}

