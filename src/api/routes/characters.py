"""
Character routes for the Dark Souls API
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

from src.models.character import CharacterCreate, CharacterUpdate, CharacterResponse, EquipRequest
from src.models.base import BaseResponse
from src.services.character_service import character_service

router = APIRouter()


@router.get("/", response_model=Dict[str, Dict])
async def get_all_characters():
    """
    Récupère tous les personnages disponibles.

    Retourne un dictionnaire avec les IDs comme clés et les données des personnages comme valeurs.
    """
    return character_service.get_all_characters()


@router.get("/ids", response_model=List[str])
async def get_character_ids():
    """
    Liste tous les IDs de personnages disponibles.

    Utile pour connaître les personnages existants avant de les récupérer individuellement.
    """
    return character_service.get_character_ids()


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: str):
    """
    Récupère les informations complètes d'un personnage par son ID.

    - **character_id**: L'ID du personnage à récupérer

    Retourne une erreur 404 si le personnage n'existe pas.
    """
    return character_service.get_character(character_id)


@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_character(character: CharacterCreate):
    """
    Crée un nouveau personnage.

    - **character**: Les données complètes du personnage à créer

    Retourne le personnage créé avec son ID assigné automatiquement.
    """
    return character_service.create_character(character)


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(character_id: str, character_update: CharacterUpdate):
    """
    Met à jour un personnage existant.

    - **character_id**: L'ID du personnage à mettre à jour
    - **character_update**: Les données à mettre à jour (tous les champs sont optionnels)

    Seuls les champs fournis seront mis à jour. Les autres restent inchangés.
    Retourne une erreur 404 si le personnage n'existe pas.
    """
    return character_service.update_character(character_id, character_update)


@router.delete("/{character_id}", response_model=BaseResponse)
async def delete_character(character_id: str):
    """
    Supprime un personnage.

    - **character_id**: L'ID du personnage à supprimer

    Retourne une erreur 404 si le personnage n'existe pas.
    """
    return character_service.delete_character(character_id)


@router.patch("/{character_id}/equip", response_model=CharacterResponse)
async def equip_item(character_id: str, equip_request: EquipRequest):
    """
    Équipe un item sur un emplacement spécifique pour un personnage.

    - **character_id**: L'ID du personnage
    - **equip_request**: Les détails de l'équipement (item_name et slot)

    Retourne une erreur 404 si le personnage n'existe pas.
    Retourne une erreur 400 si l'item n'existe pas ou si le slot cause un conflit.
    """
    return character_service.equip_item(character_id, equip_request)
