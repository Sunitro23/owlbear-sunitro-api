"""
Base models and enums for the Dark Souls API
"""

from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class EquipmentSlots(str, Enum):
    ARMOR = "armor"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"
    CONSUMABLE = "consumable"
    BAG = "bag"
    SPELL_1 = "spell_1"
    SPELL_2 = "spell_2"
    SPELL_3 = "spell_3"
    SPELL_4 = "spell_4"


class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    SPELL = "spell"
    CATALYST = "catalyst"
    CONSUMABLE = "consumable"


class DamageType(str, Enum):
    SLASHING = "slashing"
    PIERCING = "piercing"
    BLUDGEONING = "bludgeoning"
    FIRE = "fire"
    LIGHTNING = "lightning"
    MAGIC = "magic"
    DARK = "dark"
    FROST = "frost"


class ArmorType(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    FIRE = "fire"
    LIGHTNING = "lightning"
    MAGIC = "magic"
    DARK = "dark"
    FROST = "frost"


class SpellType(str, Enum):
    MAGIC = "magic"
    MIRACLE = "miracle"
    CRYOMANCY = "cryomancy"
    SORCERY = "sorcery"


class EffectType(str, Enum):
    DAMAGE = "damage"
    HEALING = "healing"
    BUFF = "buff"
    DEBUFF = "debuff"
    UTILITY = "utility"


class CatalystType(str, Enum):
    STAFF = "staff"
    TALISMAN = "talisman"
    CHIME = "chime"
    PYROMANCY_FLAME = "pyromancy flame"


class ConsumableType(str, Enum):
    ESTUS = "estus"
    KEY = "key"
    MATERIAL = "material"
    MISC = "misc"


class DiceRoll(str, Enum):
    D4 = "d4"
    D6 = "d6"
    D8 = "d8"
    D10 = "d10"
    D12 = "d12"
    D20 = "d20"
    D100 = "d100"


ScalingStat = Literal["STR", "DEX", "FTH", "INT"]


class StatName(str, Enum):
    STRENGTH = "STR"
    DEXTERITY = "DEX"
    FAITH = "FTH"
    INTELLIGENCE = "INT"
    VITALITY = "VIT"
    ENDURANCE = "END"


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    message: str
