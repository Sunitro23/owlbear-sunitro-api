"""
Main FastAPI application for the Dark Souls API
"""

from fastapi import FastAPI
from src.api.routes import characters_router, combat_router, health_router

app = FastAPI(title="Dark Souls API", description="API complète pour gérer les personnages Dark Souls avec opérations CRUD", version="2.0.0")


@app.get("/", response_model=dict)
async def read_root():
    """Point d'entrée de l'API"""
    return {"message": "Bienvenue dans l'API Dark Souls ! Utilisez /docs pour voir la documentation complète."}


# Include all routers
app.include_router(characters_router, prefix="/characters", tags=["Characters"])
app.include_router(combat_router, prefix="/combat", tags=["Combat"])
app.include_router(health_router, prefix="/health", tags=["Health"])
