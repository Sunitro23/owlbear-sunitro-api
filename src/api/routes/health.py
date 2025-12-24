"""
Health check routes for the Dark Souls API
"""

from fastapi import APIRouter
from src.models.base import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def health_check():
    """Vérification de l'état de l'API"""
    return {"message": "API opérationnelle"}
