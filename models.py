from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class StatInfo(BaseModel):
    value: int
    modifier: int


class ResourceInfo(BaseModel):
    name: str
    current: int
    max: int


class DamageType(BaseModel):
    type: str
    value: str


class StatusEffect(BaseModel):
    status: str
    value: str


class SpellEffect(BaseModel):
    effect_type: str
    value: str


class Weapon(BaseModel):
    type: str
    name: str
    damage_types: List[DamageType]
    status_effects: List[StatusEffect]


class Shield(BaseModel):
    type: str
    name: str
    shield_type: str


class Armor(BaseModel):
    name: str
    types: List[str]


class Equipment(BaseModel):
    main_hand: Weapon
    off_hand: Shield
    armor: Armor


class Spell(BaseModel):
    name: str
    spell_type: str
    effects: List[SpellEffect]


class Character(BaseModel):
    name: str
    level: int
    hollowing: int
    souls: int
    stats: Dict[str, StatInfo]
    resources: List[ResourceInfo]


class CharacterData(BaseModel):
    character: Character
    equipment: Equipment
    inventory: List[Dict[str, Any]]
    spells: List[Spell]


class CharacterCreate(BaseModel):
    """Model for creating a new character"""
    character: Character
    equipment: Equipment
    inventory: List[Dict[str, Any]] = []
    spells: List[Spell] = []


class CharacterUpdate(BaseModel):
    """Model for updating character data (all fields optional)"""
    character: Optional[Character] = None
    equipment: Optional[Equipment] = None
    inventory: Optional[List[Dict[str, Any]]] = None
    spells: Optional[List[Spell]] = None


class CharacterResponse(BaseModel):
    """Response model that includes the character ID"""
    id: int
    character: Character
    equipment: Equipment
    inventory: List[Dict[str, Any]]
    spells: List[Spell]


class MessageResponse(BaseModel):
    """Generic response for operations like delete"""
    message: str
