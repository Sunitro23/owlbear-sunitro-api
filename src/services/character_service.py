"""
Character service for the Dark Souls API
"""

from typing import Dict, Optional, List
from fastapi import HTTPException, status

from src.models.character import CharacterData, CharacterCreate, CharacterUpdate, CharacterResponse, EquipRequest
from src.database.repository import character_repository


class CharacterService:
    """Service layer for character operations"""
    
    def __init__(self, repository=character_repository):
        self.repository = repository
    
    def get_all_characters(self) -> Dict[str, CharacterData]:
        """Get all characters"""
        return self.repository.get_all_characters()

    def get_character_ids(self) -> List[str]:
        """Get list of all character IDs"""
        return self.repository.get_character_ids()

    def get_character(self, character_id: str) -> CharacterResponse:
        """Get a character by ID with full response"""
        character_data = self.repository.get_character(character_id)

        if not character_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personnage avec l'ID {character_id} non trouvé",
            )

        return CharacterResponse(
            id=character_id,
            character=character_data.character,
            inventory=character_data.inventory,
        )

    def create_character(self, character: CharacterCreate) -> CharacterResponse:
        """Create a new character"""
        character_id = self.repository.create_character(character)
        created_character = self.repository.get_character(character_id)

        return CharacterResponse(
            id=character_id,
            character=created_character.character,
            inventory=created_character.inventory,
        )

    def update_character(self, character_id: str, character_update: CharacterUpdate) -> CharacterResponse:
        """Update an existing character"""
        updated_character = self.repository.update_character(character_id, character_update)

        if not updated_character:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personnage avec l'ID {character_id} non trouvé",
            )

        return CharacterResponse(
            id=character_id,
            character=updated_character.character,
            inventory=updated_character.inventory,
        )

    def delete_character(self, character_id: str) -> Dict[str, str]:
        """Delete a character"""
        success = self.repository.delete_character(character_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personnage avec l'ID {character_id} non trouvé",
            )

        return {"message": f"Personnage avec l'ID {character_id} supprimé avec succès"}

    def equip_item(self, character_id: str, equip_request: EquipRequest) -> CharacterResponse:
        """Equip an item on a specific slot for a character"""
        equipped_character = self.repository.equip_item(character_id, equip_request.item_name, equip_request.slot)

        if not equipped_character:
            # Check if character exists
            character_exists = self.repository.get_character(character_id)
            if not character_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Personnage avec l'ID {character_id} non trouvé",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Impossible d'équiper l'item {equip_request.item_name} sur le slot {equip_request.slot}",
                )

        return CharacterResponse(
            id=character_id,
            character=equipped_character.character,
            inventory=equipped_character.inventory,
        )


# Default service instance
character_service = CharacterService()
