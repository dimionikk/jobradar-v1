from fastapi import FastAPI

from app.routers import auth, profile

app = FastAPI(title="JobRadar")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}