"""
Models package for the Dark Souls API
"""

# Base models and enums
from .base import (
    EquipmentSlots, ItemType, DamageType, DiceRoll, ScalingStat,
    ArmorType, SpellType, EffectType, CatalystType, ConsumableType,
    StatName, BaseResponse
)

# Character models
from .character import (
    StatInfo, ResourceInfo, MainCharacterInfo, Character,
    CharacterData, CharacterCreate, CharacterUpdate, CharacterResponse,
    EquipRequest
)

# Item models
from .item import (
    BaseItem, WeaponItem, ArmorItem, SpellItem, CatalystItem,
    ConsumableItem, Item, Inventory
)

# Combat models
from .combat import (
    EffectDurationType, ActiveEffect, CombatParticipant,
    CombatState, ActionData
)

__all__ = [
    # Base
    "EquipmentSlots", "ItemType", "DamageType", "DiceRoll", "ScalingStat",
    "ArmorType", "SpellType", "EffectType", "CatalystType", "ConsumableType",
    "StatName", "BaseResponse",
    
    # Character
    "StatInfo", "ResourceInfo", "MainCharacterInfo", "Character",
    "CharacterData", "CharacterCreate", "CharacterUpdate", "CharacterResponse",
    "EquipRequest",
    
    # Item
    "BaseItem", "WeaponItem", "ArmorItem", "SpellItem", "CatalystItem",
    "ConsumableItem", "Item", "Inventory",
    
    # Combat
    "EffectDurationType", "ActiveEffect", "CombatParticipant",
    "CombatState", "ActionData"
]
