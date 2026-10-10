from fastapi import FastAPI

from app.api.routes.datasets import router as datasets_router
from app.api.routes.health import router as health_router
from app.config import settings
from app.logging import configure_logging

logger = configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="TrustAI — AI Reliability Lab backend foundation.",
)

app.include_router(health_router)
app.include_router(datasets_router)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("TrustAI application starting", extra={"environment": settings.environment})


@app.on_event("shutdown")
def shutdown_event() -> None:
    logger.info("TrustAI application shutting down")
