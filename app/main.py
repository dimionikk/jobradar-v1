from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, profile, vacancies, ai, saved, applications
from app.core.database import AsyncSessionLocal
from app.services.parser import run_all_parsers

app = FastAPI(title="JobRadar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()


async def scheduled_parse():
    async with AsyncSessionLocal() as db:
        results = await run_all_parsers(db)
        print(f"Parsing done: {results}")


@app.on_event("startup")
async def startup():
    scheduler.add_job(
        scheduled_parse,
        trigger=IntervalTrigger(hours=6),
        id="parse_vacancies",
        replace_existing=True,
    )
    scheduler.start()
    await scheduled_parse()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()


app.include_router(auth.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(vacancies.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(saved.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}