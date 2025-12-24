"""
Character models for the Dark Souls API
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator, root_validator, conint
from datetime import datetime

from .base import StatName, StatName, EquipmentSlots


class StatInfo(BaseModel):
    """Character stat information"""
    value: conint(ge=0, le=99) = Field(description="Stat value between 0-99")
    modifier: int = Field(ge=-20, le=20, description="Modifier range")


class ResourceInfo(BaseModel):
    """Character resource information (HP, AP, etc.)"""
    current: conint(ge=0)
    maximum: conint(ge=0)


class MainCharacterInfo(BaseModel):
    """Main character information"""
    name: str
    level: conint(ge=0, le=100)
    souls: conint(ge=0)


class Character(BaseModel):
    """Complete character model"""
    main: MainCharacterInfo
    stats: Dict[StatName, StatInfo]
    resources: Dict[str, ResourceInfo]


class CharacterData(BaseModel):
    """Complete character data with metadata"""
    character: Dict[str, Any]
    inventory: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CharacterCreate(BaseModel):
    """Model for creating a new character"""
    character: Character


class CharacterUpdate(BaseModel):
    """Model for updating character data (all fields optional)"""
    character: Optional[Character] = None


class CharacterResponse(BaseModel):
    """Response model that includes the character ID and complete inventory"""
    id: str
    character: Dict[str, Any]
    inventory: Dict[str, Any]


class EquipRequest(BaseModel):
    """Model for equipping an item on a specific slot"""
    item_name: str
    slot: EquipmentSlots
