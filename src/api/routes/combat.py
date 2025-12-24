"""
Combat routes for the Dark Souls API
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional

from src.models.combat import CombatParticipant, ActiveEffect, ActionData
from src.models.base import BaseResponse
from src.services.combat_service import combat_service

router = APIRouter()


@router.get("/status", response_model=Dict[str, Any])
async def get_combat_status():
    """
    Renvoie l'état du combat actuel.

    Retourne les informations sur le combat en cours, y compris l'ordre des tours,
    le tour actuel, les participants, etc.
    """
    return combat_service.get_combat_status()


@router.post("/start", response_model=Dict[str, str])
async def start_combat(participants: List[CombatParticipant]):
    """
    Démarre un nouveau combat avec les participants spécifiés.

    - **participants**: Liste des participants au combat

    Retourne une erreur 409 si un combat est déjà en cours.
    """
    return combat_service.start_combat(participants)


@router.post("/end", response_model=BaseResponse)
async def end_combat():
    """
    Termine le combat actuel.

    Retourne une erreur 404 si aucun combat n'est en cours.
    """
    return combat_service.end_combat()


@router.get("/turn", response_model=Dict[str, Any])
async def get_current_turn():
    """
    Renvoie les informations sur le tour actuel.

    Retourne le participant actuel, le round, l'index du tour, etc.
    """
    return combat_service.get_current_turn()


@router.post("/turn/end", response_model=Dict[str, Any])
async def end_current_turn():
    """
    Termine le tour actuel et passe au participant suivant.

    Retourne les informations sur le nouveau participant actuel.
    """
    return combat_service.end_current_turn()


@router.post("/participant/add", response_model=BaseResponse)
async def add_participant_to_combat(participant: CombatParticipant):
    """
    Ajoute un participant au combat en cours.

    - **participant**: Informations du participant à ajouter

    Retourne une erreur 404 si aucun combat n'est en cours.
    """
    return combat_service.add_participant(participant)


@router.delete("/participant/{participant_id}", response_model=BaseResponse)
async def remove_participant_from_combat(participant_id: str):
    """
    Supprime un participant du combat en cours.

    - **participant_id**: ID du participant à supprimer

    Retourne une erreur 404 si aucun combat n'est en cours.
    """
    return combat_service.remove_participant(participant_id)


@router.get("/participant/{participant_id}", response_model=Dict[str, Any])
async def get_participant_info(participant_id: str):
    """
    Renvoie les informations détaillées d'un participant.

    - **participant_id**: ID du participant

    Retourne une erreur 404 si le participant n'est pas dans le combat.
    """
    return combat_service.get_participant_info(participant_id)


@router.get("/participants", response_model=Dict[str, Dict[str, Any]])
async def get_all_participants():
    """
    Renvoie les informations de tous les participants au combat.
    """
    return combat_service.get_all_participants()


@router.post("/effect/apply", response_model=BaseResponse)
async def apply_effect_to_participant(participant_id: str, effect: ActiveEffect):
    """
    Applique un effet à un participant.

    - **participant_id**: ID du participant
    - **effect**: Effet à appliquer

    Retourne une erreur 404 si aucun combat n'est en cours ou si le participant n'est pas trouvé.
    """
    return combat_service.apply_effect(participant_id, effect)


@router.delete("/effect/{participant_id}/{effect_name}", response_model=BaseResponse)
async def remove_effect_from_participant(participant_id: str, effect_name: str):
    """
    Supprime un effet d'un participant.

    - **participant_id**: ID du participant
    - **effect_name**: Nom de l'effet à supprimer

    Retourne une erreur 404 si aucun combat n'est en cours ou si le participant/effect n'est pas trouvé.
    """
    return combat_service.remove_effect(participant_id, effect_name)


@router.post("/effects/update", response_model=Dict[str, Any])
async def update_all_effects():
    """
    Met à jour tous les effets actifs (décrémente les durées, retire les effets expirés).

    Retourne la liste des effets expirés.
    """
    return combat_service.update_effects()


# === NOUVEAUX ENDPOINTS POUR LA LOGIQUE DE COMBAT ===


@router.post("/init", response_model=Dict[str, str])
async def initialize_combat(characters: List[Dict[str, Any]]):
    """
    Initialise un combat avec les personnages fournis.

    - **characters**: Liste de personnages avec leurs données complètes

    Retourne l'ID du combat créé.
    """
    return combat_service.initialize_combat(characters)


@router.post("/turn/next", response_model=Dict[str, Any])
async def advance_turn():
    """
    Passe au tour suivant et gère les effets de fin/début de tour.

    Retourne les informations sur le nouveau tour.
    """
    return combat_service.advance_turn()


@router.post("/action", response_model=Dict[str, Any])
async def execute_action(action_data: ActionData):
    """
    Exécute une action dans le combat.

    - **action_data**: Données de l'action à exécuter

    Types d'actions supportés :
    - Attack: Attaque avec arme
    - Cast: Lancer un sort
    - Dodge: Esquiver
    - Parry: Parer
    - Search: Fouiller

    Retourne le résultat de l'action.
    """
    return combat_service.perform_action(action_data)


@router.post("/turn/delay", response_model=Dict[str, Any])
async def delay_participant_turn(actor_id: str):
    """
    Retarde le tour d'un participant (le place en fin de round).

    - **actor_id**: ID du participant dont on retarde le tour

    Retourne le résultat de l'opération.
    """
    return combat_service.delay_turn(actor_id)
