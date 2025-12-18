from pydantic import BaseModel, Field, conint, validator, root_validator
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
from datetime import datetime


class EquipmentSlots(str, Enum):
    ARMOR = 'armor'
    RIGHT_HAND = 'right_hand'
    LEFT_HAND = 'left_hand'
    CONSUMABLE = 'consumable'
    BAG = 'bag'
    SPELL_1 = 'spell_1'
    SPELL_2 = 'spell_2'
    SPELL_3 = 'spell_3'
    SPELL_4 = 'spell_4'


class ItemType(str, Enum):
    WEAPON = 'weapon'
    ARMOR = 'armor'
    SPELL = 'spell'
    CATALYST = 'catalyst'
    CONSUMABLE = 'consumable'


class DamageType(str, Enum):
    SLASHING = 'slashing'
    PIERCING = 'piercing'
    BLUDGEONING = 'bludgeoning'
    FIRE = 'fire'
    LIGHTNING = 'lightning'
    MAGIC = 'magic'
    DARK = 'dark'
    FROST = 'frost'


class ArmorType(str, Enum):
    LIGHT = 'light'
    MEDIUM = 'medium'
    HEAVY = 'heavy'
    FIRE = 'fire'
    LIGHTNING = 'lightning'
    MAGIC = 'magic'
    DARK = 'dark'
    FROST = 'frost'


class SpellType(str, Enum):
    MAGIC = 'magic'
    MIRACLE = 'miracle'
    CRYOMANCY = 'cryomancy'
    SORCERY = 'sorcery'


class EffectType(str, Enum):
    DAMAGE = 'damage'
    HEALING = 'healing'
    BUFF = 'buff'
    DEBUFF = 'debuff'
    UTILITY = 'utility'


class CatalystType(str, Enum):
    STAFF = 'staff'
    TALISMAN = 'talisman'
    CHIME = 'chime'
    PYROMANCY_FLAME = 'pyromancy flame'


class ConsumableType(str, Enum):
    ESTUS = 'estus'
    KEY = 'key'
    MATERIAL = 'material'
    MISC = 'misc'


class DiceRoll(str, Enum):
    D4 = 'd4'
    D6 = 'd6'
    D8 = 'd8'
    D10 = 'd10'
    D12 = 'd12'
    D20 = 'd20'
    D100 = 'd100'


ScalingStat = Literal['STR', 'DEX', 'FTH', 'INT']


class StatName(str, Enum):
    STRENGTH = 'STR'
    DEXTERITY = 'DEX'
    FAITH = 'FTH'
    INTELLIGENCE = 'INT'
    VITALITY = 'VIT'
    ENDURANCE = 'END'


class StatInfo(BaseModel):
    value: conint(ge=0, le=99) = Field(description="Stat value between 0-99")
    modifier: int = Field(ge=-20, le=20, description="Modifier range")


class ResourceInfo(BaseModel):
    current: conint(ge=0)
    maximum: conint(ge=0)


class MainCharacterInfo(BaseModel):
    name: str
    level: conint(ge=0, le=100)
    souls: conint(ge=0)


class Character(BaseModel):
    main: MainCharacterInfo
    stats: Dict[StatName, StatInfo]
    resources: Dict[str, ResourceInfo]


class BaseItem(BaseModel):
    name: str
    image: str
    slot: EquipmentSlots


class WeaponItem(BaseItem):
    type: Literal[ItemType.WEAPON] = ItemType.WEAPON
    damageType: DamageType
    dice: DiceRoll
    scalingStat: Optional[ScalingStat] = None
    twoHanded: Optional[bool] = None
    flatBonus: int


class ArmorItem(BaseItem):
    type: Literal[ItemType.ARMOR] = ItemType.ARMOR
    armorType: ArmorType
    flatBonus: int


class SpellItem(BaseItem):
    type: Literal[ItemType.SPELL] = ItemType.SPELL
    spellType: SpellType
    effectType: EffectType
    dice: DiceRoll
    scalingStat: Optional[ScalingStat] = None
    duration: Optional[int] = None
    requiresCatalyst: CatalystType
    uses: int
    max_uses: Optional[int] = None


class CatalystItem(BaseItem):
    type: Literal[ItemType.CATALYST] = ItemType.CATALYST
    catalystType: CatalystType
    flatBonus: int


class ConsumableItem(BaseItem):
    type: Literal[ItemType.CONSUMABLE] = ItemType.CONSUMABLE
    consumableType: ConsumableType
    effect: str
    uses: int
    max_uses: Optional[int] = None

Item = Union[WeaponItem, ArmorItem, SpellItem, CatalystItem, ConsumableItem]


class Inventory(BaseModel):
    weapons: List[WeaponItem]
    armors: List[ArmorItem]
    catalysts: List[CatalystItem]
    items: List[ConsumableItem]
    spells: List[SpellItem]

    @root_validator(pre=True)
    def validate_unique_slots(cls, values):
        slots = set()
        for category in ['weapons', 'armors', 'catalysts', 'items', 'spells']:
            items = values.get(category, [])
            for item in items:
                slot = item.get('slot')
                if slot and slot != 'bag':  # Only validate equipped slots (not 'bag')
                    if slot in slots:
                        raise ValueError(f"Duplicate equipment slot '{slot}' found. Each slot can only have one item equipped.")
                    slots.add(slot)
        return values


class CharacterData(BaseModel):
    character: Dict[str, Any]
    inventory: Inventory
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CharacterCreate(BaseModel):
    """Model for creating a new character"""
    character: Character
    inventory: Inventory


class CharacterUpdate(BaseModel):
    """Model for updating character data (all fields optional)"""
    character: Optional[Character] = None
    inventory: Optional[Inventory] = None


class CharacterResponse(BaseModel):
    """Response model that includes the character ID"""
    id: int
    character: Dict[str, Any]
    inventory: Inventory


class EquipRequest(BaseModel):
    """Model for equipping an item on a specific slot"""
    item_name: str
    slot: EquipmentSlots


class MessageResponse(BaseModel):
    """Generic response for operations like delete"""
    message: str
