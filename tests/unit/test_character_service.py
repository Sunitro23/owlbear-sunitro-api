"""
Unit tests for character service
"""

import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, status

from src.models.character import CharacterData, CharacterCreate, CharacterUpdate, CharacterResponse, EquipRequest, Character, MainCharacterInfo, StatInfo, ResourceInfo
from src.services.character_service import CharacterService


class TestCharacterService:
    """Test cases for CharacterService"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_repository = Mock()
        self.service = CharacterService(repository=self.mock_repository)
    
    def test_get_all_characters(self):
        """Test getting all characters"""
        # Arrange
        expected_characters = {"char1": CharacterData(character={"name": "Test"}, inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []})}
        self.mock_repository.get_all_characters.return_value = expected_characters
        
        # Act
        result = self.service.get_all_characters()
        
        # Assert
        assert result == expected_characters
        self.mock_repository.get_all_characters.assert_called_once()
    
    def test_get_character_ids(self):
        """Test getting character IDs"""
        # Arrange
        expected_ids = ["char1", "char2"]
        self.mock_repository.get_character_ids.return_value = expected_ids
        
        # Act
        result = self.service.get_character_ids()
        
        # Assert
        assert result == expected_ids
        self.mock_repository.get_character_ids.assert_called_once()
    
    def test_get_character_success(self):
        """Test getting a character that exists"""
        # Arrange
        character_id = "char1"
        character_data = CharacterData(character={"name": "Test"}, inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []})
        self.mock_repository.get_character.return_value = character_data
        
        # Act
        result = self.service.get_character(character_id)
        
        # Assert
        assert isinstance(result, CharacterResponse)
        assert result.id == character_id
        assert result.character == character_data.character
        self.mock_repository.get_character.assert_called_once_with(character_id)
    
    def test_get_character_not_found(self):
        """Test getting a character that doesn't exist"""
        # Arrange
        character_id = "nonexistent"
        self.mock_repository.get_character.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.get_character(character_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"Personnage avec l'ID {character_id} non trouvé" in str(exc_info.value.detail)
    
    def test_create_character(self):
        """Test creating a character"""
        # Arrange
        character_data = CharacterCreate(
            character=Character(
                main=MainCharacterInfo(name="New Character", level=1, souls=0),
                stats={"STR": StatInfo(value=10, modifier=0)},
                resources={"HP": ResourceInfo(current=100, maximum=100)}
            )
        )
        created_id = "new-char-id"
        created_character = CharacterData(
            character={"name": "New Character"},
            inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []}
        )
        
        self.mock_repository.create_character.return_value = created_id
        self.mock_repository.get_character.return_value = created_character
        
        # Act
        result = self.service.create_character(character_data)
        
        # Assert
        assert isinstance(result, CharacterResponse)
        assert result.id == created_id
        assert result.character == created_character.character
        self.mock_repository.create_character.assert_called_once_with(character_data)
    
    def test_update_character_success(self):
        """Test updating a character that exists"""
        # Arrange
        character_id = "char1"
        character_update = CharacterUpdate(
            character=Character(
                main=MainCharacterInfo(name="Updated Name", level=1, souls=0),
                stats={"STR": StatInfo(value=10, modifier=0)},
                resources={"HP": ResourceInfo(current=100, maximum=100)}
            )
        )
        updated_character = CharacterData(
            character={"name": "Updated Name"},
            inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []}
        )
        
        self.mock_repository.update_character.return_value = updated_character
        
        # Act
        result = self.service.update_character(character_id, character_update)
        
        # Assert
        assert isinstance(result, CharacterResponse)
        assert result.id == character_id
        assert result.character == updated_character.character
        self.mock_repository.update_character.assert_called_once_with(character_id, character_update)
    
    def test_update_character_not_found(self):
        """Test updating a character that doesn't exist"""
        # Arrange
        character_id = "nonexistent"
        character_update = CharacterUpdate(
            character=Character(
                main=MainCharacterInfo(name="Updated Name", level=1, souls=0),
                stats={"STR": StatInfo(value=10, modifier=0)},
                resources={"HP": ResourceInfo(current=100, maximum=100)}
            )
        )
        self.mock_repository.update_character.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.update_character(character_id, character_update)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"Personnage avec l'ID {character_id} non trouvé" in str(exc_info.value.detail)
    
    def test_delete_character_success(self):
        """Test deleting a character that exists"""
        # Arrange
        character_id = "char1"
        self.mock_repository.delete_character.return_value = True
        
        # Act
        result = self.service.delete_character(character_id)
        
        # Assert
        assert result == {"message": f"Personnage avec l'ID {character_id} supprimé avec succès"}
        self.mock_repository.delete_character.assert_called_once_with(character_id)
    
    def test_delete_character_not_found(self):
        """Test deleting a character that doesn't exist"""
        # Arrange
        character_id = "nonexistent"
        self.mock_repository.delete_character.return_value = False
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.delete_character(character_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"Personnage avec l'ID {character_id} non trouvé" in str(exc_info.value.detail)
    
    def test_equip_item_success(self):
        """Test equipping an item successfully"""
        # Arrange
        character_id = "char1"
        equip_request = EquipRequest(item_name="Sword", slot="right_hand")
        equipped_character = CharacterData(character={"name": "Test"}, inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []})
        
        self.mock_repository.equip_item.return_value = equipped_character
        
        # Act
        result = self.service.equip_item(character_id, equip_request)
        
        # Assert
        assert isinstance(result, CharacterResponse)
        assert result.id == character_id
        assert result.character == equipped_character.character
        self.mock_repository.equip_item.assert_called_once_with(character_id, equip_request.item_name, equip_request.slot)
    
    def test_equip_item_character_not_found(self):
        """Test equipping an item on a character that doesn't exist"""
        # Arrange
        character_id = "nonexistent"
        equip_request = EquipRequest(item_name="Sword", slot="right_hand")
        self.mock_repository.equip_item.return_value = None
        self.mock_repository.get_character.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.equip_item(character_id, equip_request)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"Personnage avec l'ID {character_id} non trouvé" in str(exc_info.value.detail)
    
    def test_equip_item_invalid_slot(self):
        """Test equipping an item with invalid slot"""
        # Arrange
        character_id = "char1"
        equip_request = EquipRequest(item_name="Sword", slot="right_hand")
        self.mock_repository.equip_item.return_value = None
        self.mock_repository.get_character.return_value = CharacterData(character={"name": "Test"}, inventory={"weapons": [], "armors": [], "catalysts": [], "items": [], "spells": []})
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.equip_item(character_id, equip_request)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert f"Impossible d'équiper l'item {equip_request.item_name} sur le slot {equip_request.slot}" in str(exc_info.value.detail)
