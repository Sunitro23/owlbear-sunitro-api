#!/usr/bin/env python3
"""
Test script to verify the refactored structure works correctly
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        # Test models
        from models.base import EquipmentSlots, ItemType, StatName
        from models.character import Character, CharacterCreate, CharacterResponse
        from models.item import WeaponItem, ArmorItem, Inventory
        from models.combat import CombatParticipant, ActiveEffect, ActionData
        print("✅ Models imported successfully")
        
        # Test database
        from database.storage import JSONStorage, StorageInterface
        from database.repository import CharacterRepository, character_repository
        print("✅ Database layer imported successfully")
        
        # Test services
        from services.character_service import CharacterService, character_service
        from services.combat_service import CombatService, combat_service
        print("✅ Services imported successfully")
        
        # Test API
        from api.main import app
        from api.routes import characters_router, combat_router, health_router
        print("✅ API imported successfully")
        
        # Test combat system (now in services)
        from services.combat_system import combat_manager
        print("✅ Combat system imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of the refactored components"""
    print("\nTesting basic functionality...")
    
    try:
        # Test model creation
        from models.character import Character, MainCharacterInfo, StatInfo, ResourceInfo
        from models.item import WeaponItem, EquipmentSlots
        
        # Create a character
        character = Character(
            main=MainCharacterInfo(name="Test Character", level=1, souls=0),
            stats={"STR": StatInfo(value=10, modifier=0)},
            resources={"HP": ResourceInfo(current=100, maximum=100)}
        )
        print("✅ Character model creation works")
        
        # Create an item
        weapon = WeaponItem(
            name="Test Sword",
            image="test.png",
            slot=EquipmentSlots.RIGHT_HAND,
            damageType="slashing",
            dice="d6",
            flatBonus=5
        )
        print("✅ Item model creation works")
        
        # Test service instantiation
        from services.character_service import CharacterService
        service = CharacterService()
        print("✅ Service instantiation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing refactored Dark Souls API structure\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print(f"\n{'='*50}")
    if imports_ok and functionality_ok:
        print("🎉 All tests passed! Refactored structure is working correctly.")
        print("\nNext steps:")
        print("1. Run 'python -m uvicorn src.api.main:app --reload' to start the server")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Run 'pytest tests/' to run the test suite")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
