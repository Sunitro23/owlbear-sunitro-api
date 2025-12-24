"""
Repository layer for the Dark Souls API
"""

import uuid
from typing import Dict, Optional, List
from datetime import datetime

from src.models.character import CharacterData, CharacterCreate, CharacterUpdate
from src.database.storage import StorageInterface, JSONStorage


class CharacterRepository:
    """Repository for character data operations"""
    
    def __init__(self, storage: StorageInterface):
        self.storage = storage
    
    def get_character(self, character_id: str) -> Optional[CharacterData]:
        """Get a character by ID"""
        characters = self.storage.load()
        character_data = characters.get(character_id)

        if character_data:
            return CharacterData(**character_data)
        return None

    def get_all_characters(self) -> Dict[str, CharacterData]:
        """Get all characters"""
        characters = self.storage.load()
        result = {}

        for char_id, char_data in characters.items():
            result[char_id] = CharacterData(**char_data)

        return result

    def create_character(self, character_data: CharacterCreate) -> str:
        """Create a new character and return the assigned ID"""
        characters = self.storage.load()

        # Generate a new UUID
        new_id = str(uuid.uuid4())

        # Convert the Pydantic model to dict
        characters[new_id] = character_data.model_dump()

        self.storage.save(characters)
        return new_id

    def update_character(self, character_id: str, character_update: CharacterUpdate) -> Optional[CharacterData]:
        """Update an existing character"""
        characters = self.storage.load()

        if character_id not in characters:
            return None

        # Get current character data
        current_data = characters[character_id]

        # Update only the provided fields
        update_dict = character_update.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            if value is not None:
                current_data[key] = value

        characters[character_id] = current_data
        self.storage.save(characters)

        return CharacterData(**current_data)

    def delete_character(self, character_id: str) -> bool:
        """Delete a character by ID. Returns True if successful, False if not found"""
        characters = self.storage.load()

        if character_id in characters:
            del characters[character_id]
            self.storage.save(characters)
            return True

        return False

    def get_character_ids(self) -> List[str]:
        """Get list of all character IDs"""
        characters = self.storage.load()
        return list(characters.keys())

    def equip_item(self, character_id: str, item_name: str, slot: str) -> Optional[CharacterData]:
        """Equip an item on a specific slot for a character"""
        characters = self.storage.load()

        if character_id not in characters:
            return None

        character_data = characters[character_id]

        # First, unequip any item currently in the target slot
        for category in ["weapons", "armors", "catalysts", "items", "spells"]:
            if category in character_data.get("inventory", {}):
                for item in character_data["inventory"][category]:
                    if item.get("slot") == slot:
                        item["slot"] = "bag"
                        break

        # Find the item in the inventory and update its slot
        item_found = False
        for category in ["weapons", "armors", "catalysts", "items", "spells"]:
            if category in character_data.get("inventory", {}):
                for item in character_data["inventory"][category]:
                    if item.get("name") == item_name:
                        item["slot"] = slot
                        item_found = True
                        break
            if item_found:
                break

        if not item_found:
            return None

        # Validate the inventory (check for duplicate slots)
        # We need to temporarily create an Inventory object to validate
        try:
            from src.models.item import Inventory

            inventory_data = character_data.get("inventory", {})
            Inventory(**inventory_data)  # This will raise an error if validation fails
        except Exception as e:
            return None  # Invalid inventory state

        characters[character_id] = character_data
        self.storage.save(characters)

        return CharacterData(**character_data)


# Default repository instance using JSON storage
default_storage = JSONStorage()
character_repository = CharacterRepository(default_storage)
