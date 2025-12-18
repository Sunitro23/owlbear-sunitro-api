import json
import os
from typing import Dict, Optional, List
from models import CharacterData, CharacterCreate, CharacterUpdate

DB_FILE = "characters.json"


def load_characters() -> Dict[str, dict]:
    """Load characters from JSON file"""
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_characters(characters: Dict[str, dict]) -> None:
    """Save characters to JSON file"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(characters, f, indent=2, ensure_ascii=False)


def get_character(character_id: int) -> Optional[CharacterData]:
    """Get a character by ID"""
    characters = load_characters()
    character_data = characters.get(str(character_id))
    
    if character_data:
        return CharacterData(**character_data)
    return None


def get_all_characters() -> Dict[int, CharacterData]:
    """Get all characters"""
    characters = load_characters()
    result = {}
    
    for char_id, char_data in characters.items():
        try:
            result[int(char_id)] = CharacterData(**char_data)
        except ValueError:
            continue  # Skip invalid IDs
    
    return result


def create_character(character_data: CharacterCreate) -> int:
    """Create a new character and return the assigned ID"""
    characters = load_characters()
    
    # Find the next available ID
    if characters:
        next_id = max(int(id_) for id_ in characters.keys()) + 1
    else:
        next_id = 1
    
    # Convert the Pydantic model to dict
    characters[str(next_id)] = character_data.model_dump()
    
    save_characters(characters)
    return next_id


def update_character(character_id: int, character_update: CharacterUpdate) -> Optional[CharacterData]:
    """Update an existing character"""
    characters = load_characters()
    
    if str(character_id) not in characters:
        return None
    
    # Get current character data
    current_data = characters[str(character_id)]
    
    # Update only the provided fields
    update_dict = character_update.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        if value is not None:
            current_data[key] = value
    
    characters[str(character_id)] = current_data
    save_characters(characters)
    
    return CharacterData(**current_data)


def delete_character(character_id: int) -> bool:
    """Delete a character by ID. Returns True if successful, False if not found"""
    characters = load_characters()
    
    if str(character_id) in characters:
        del characters[str(character_id)]
        save_characters(characters)
        return True
    
    return False


def get_character_ids() -> List[int]:
    """Get list of all character IDs"""
    characters = load_characters()
    return [int(id_) for id_ in characters.keys() if id_.isdigit()]


def equip_item(character_id: int, item_name: str, slot: str) -> Optional[CharacterData]:
    """Equip an item on a specific slot for a character"""
    characters = load_characters()

    if str(character_id) not in characters:
        return None

    character_data = characters[str(character_id)]

    # First, unequip any item currently in the target slot
    for category in ['weapons', 'armors', 'catalysts', 'items', 'spells']:
        if category in character_data.get('inventory', {}):
            for item in character_data['inventory'][category]:
                if item.get('slot') == slot:
                    item['slot'] = 'bag'
                    break

    # Find the item in the inventory and update its slot
    item_found = False
    for category in ['weapons', 'armors', 'catalysts', 'items', 'spells']:
        if category in character_data.get('inventory', {}):
            for item in character_data['inventory'][category]:
                if item.get('name') == item_name:
                    item['slot'] = slot
                    item_found = True
                    break
        if item_found:
            break

    if not item_found:
        return None

    # Validate the inventory (check for duplicate slots)
    # We need to temporarily create an Inventory object to validate
    try:
        from models import Inventory
        inventory_data = character_data.get('inventory', {})
        Inventory(**inventory_data)  # This will raise an error if validation fails
    except Exception as e:
        return None  # Invalid inventory state

    characters[str(character_id)] = character_data
    save_characters(characters)

    return CharacterData(**character_data)
