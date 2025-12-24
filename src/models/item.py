"""
Item models for the Dark Souls API
"""

from typing import Union, Optional, List
from pydantic import BaseModel, Field, root_validator

from .base import (
    ItemType, EquipmentSlots, DamageType, DiceRoll, ScalingStat, 
    ArmorType, SpellType, EffectType, CatalystType, ConsumableType
)


class BaseItem(BaseModel):
    """Base item model with common fields"""
    name: str
    image: str
    slot: EquipmentSlots


class WeaponItem(BaseItem):
    """Weapon item model"""
    type: str = ItemType.WEAPON
    damageType: DamageType
    dice: DiceRoll
    scalingStat: Optional[ScalingStat] = None
    twoHanded: Optional[bool] = None
    flatBonus: int


class ArmorItem(BaseItem):
    """Armor item model"""
    type: str = ItemType.ARMOR
    armorType: ArmorType
    flatBonus: int


class SpellItem(BaseItem):
    """Spell item model"""
    type: str = ItemType.SPELL
    spellType: SpellType
    effectType: EffectType
    dice: DiceRoll
    scalingStat: Optional[ScalingStat] = None
    duration: Optional[int] = None
    requiresCatalyst: CatalystType
    uses: int
    max_uses: Optional[int] = None


class CatalystItem(BaseItem):
    """Catalyst item model"""
    type: str = ItemType.CATALYST
    catalystType: CatalystType
    flatBonus: int


class ConsumableItem(BaseItem):
    """Consumable item model"""
    type: str = ItemType.CONSUMABLE
    consumableType: ConsumableType
    effect: str
    uses: int
    max_uses: Optional[int] = None


# Union type for all item types
Item = Union[WeaponItem, ArmorItem, SpellItem, CatalystItem, ConsumableItem]


class Inventory(BaseModel):
    """Character inventory model"""
    weapons: List[WeaponItem] = []
    armors: List[ArmorItem] = []
    catalysts: List[CatalystItem] = []
    items: List[ConsumableItem] = []
    spells: List[SpellItem] = []

    @root_validator(pre=True)
    def validate_unique_slots(cls, values):
        """Validate that no two items occupy the same non-bag slot"""
        slots = set()
        for category in ["weapons", "armors", "catalysts", "items", "spells"]:
            items = values.get(category, [])
            for item in items:
                slot = item.get("slot")
                if slot and slot != "bag":  # Only validate equipped slots (not 'bag')
                    if slot in slots:
                        raise ValueError(f"Duplicate equipment slot '{slot}' found. Each slot can only have one item equipped.")
                    slots.add(slot)
        return values
