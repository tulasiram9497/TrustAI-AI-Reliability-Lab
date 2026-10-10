from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "environment": settings.environment}
