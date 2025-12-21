from fastapi import FastAPI, HTTPException, status, Request
from typing import List, Dict
from models import (
    CharacterData, CharacterCreate, CharacterUpdate,
    CharacterResponse, MessageResponse, EquipRequest
)
import database as db

app = FastAPI(
    title="Dark Souls API", 
    description="API complète pour gérer les personnages Dark Souls avec opérations CRUD",
    version="2.0.0"
)


@app.get("/", response_model=MessageResponse)
def read_root():
    """Point d'entrée de l'API"""
    return {"message": "Bienvenue dans l'API Dark Souls ! Utilisez /docs pour voir la documentation complète."}


@app.get("/characters", response_model=Dict[str, CharacterData])
def get_all_characters():
    """
    Récupère tous les personnages disponibles.

    Retourne un dictionnaire avec les IDs comme clés et les données des personnages comme valeurs.
    """
    return db.get_all_characters()


@app.get("/characters/ids", response_model=List[str])
def get_character_ids():
    """
    Liste tous les IDs de personnages disponibles.

    Utile pour connaître les personnages existants avant de les récupérer individuellement.
    """
    return db.get_character_ids()


@app.get("/characters/{character_id}", response_model=CharacterResponse)
def get_character(character_id: str):
    """
    Récupère les informations complètes d'un personnage par son ID.
    
    - **character_id**: L'ID du personnage à récupérer
    
    Retourne une erreur 404 si le personnage n'existe pas.
    """
    character_data = db.get_character(character_id)
    
    if not character_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personnage avec l'ID {character_id} non trouvé"
        )
    
    return CharacterResponse(
        id=character_id,
        character=character_data.character,
        inventory=character_data.inventory
    )


@app.post("/characters", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(character: CharacterCreate):
    """
    Crée un nouveau personnage.
    
    - **character**: Les données complètes du personnage à créer
    
    Retourne le personnage créé avec son ID assigné automatiquement.
    """
    character_id = db.create_character(character)
    created_character = db.get_character(character_id)
    
    return CharacterResponse(
        id=character_id,
        character=created_character.character,
        inventory=created_character.inventory
    )


@app.put("/characters/{character_id}", response_model=CharacterResponse)
def update_character(character_id: str, character_update: CharacterUpdate):
    """
    Met à jour un personnage existant.
    
    - **character_id**: L'ID du personnage à mettre à jour
    - **character_update**: Les données à mettre à jour (tous les champs sont optionnels)
    
    Seuls les champs fournis seront mis à jour. Les autres restent inchangés.
    Retourne une erreur 404 si le personnage n'existe pas.
    """
    updated_character = db.update_character(character_id, character_update)
    
    if not updated_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personnage avec l'ID {character_id} non trouvé"
        )
    
    return CharacterResponse(
        id=character_id,
        character=updated_character.character,
        inventory=updated_character.inventory
    )


@app.delete("/characters/{character_id}", response_model=MessageResponse)
def delete_character(character_id: str):
    """
    Supprime un personnage.
    
    - **character_id**: L'ID du personnage à supprimer
    
    Retourne une erreur 404 si le personnage n'existe pas.
    """
    success = db.delete_character(character_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personnage avec l'ID {character_id} non trouvé"
        )
    
    return {"message": f"Personnage avec l'ID {character_id} supprimé avec succès"}


@app.patch("/characters/{character_id}/equip", response_model=CharacterResponse)
def equip_item(character_id: str, equip_request: EquipRequest):
    """
    Équipe un item sur un emplacement spécifique pour un personnage.

    - **character_id**: L'ID du personnage
    - **equip_request**: Les détails de l'équipement (item_name et slot)

    Retourne une erreur 404 si le personnage n'existe pas.
    Retourne une erreur 400 si l'item n'existe pas ou si le slot cause un conflit.
    """
    equipped_character = db.equip_item(character_id, equip_request.item_name, equip_request.slot)

    if not equipped_character:
        # Check if character exists
        character_exists = db.get_character(character_id)
        if not character_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personnage avec l'ID {character_id} non trouvé"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible d'équiper l'item {equip_request.item_name} sur le slot {equip_request.slot}"
            )

    return CharacterResponse(
        id=character_id,
        character=equipped_character.character,
        inventory=equipped_character.inventory
    )

# Health check endpoint
@app.get("/health", response_model=MessageResponse)
def health_check():
    """Vérification de l'état de l'API"""
    return {"message": "API opérationnelle"}
