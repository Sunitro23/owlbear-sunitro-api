# Data Models Documentation

## Overview

This document describes all the Pydantic models and data structures used in the Dark Souls API. These models define the data validation, serialization, and API contracts.

## Base Models

### BaseResponse

Base response model for all API responses.

```python
class BaseResponse(BaseModel):
    message: str
```

**Fields:**
- `message` (str): Human-readable response message

### EquipmentSlots

Enumeration of valid equipment slots.

```python
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
```

### ItemType

Enumeration of item types.

```python
class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    SPELL = "spell"
    CATALYST = "catalyst"
    CONSUMABLE = "consumable"
```

### DamageType

Enumeration of damage types.

```python
class DamageType(str, Enum):
    SLASHING = "slashing"
    PIERCING = "piercing"
    BLUDGEONING = "bludgeoning"
    FIRE = "fire"
    LIGHTNING = "lightning"
    MAGIC = "magic"
    DARK = "dark"
    FROST = "frost"
```

### ArmorType

Enumeration of armor types.

```python
class ArmorType(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    FIRE = "fire"
    LIGHTNING = "lightning"
    MAGIC = "magic"
    DARK = "dark"
    FROST = "frost"
```

### SpellType

Enumeration of spell types.

```python
class SpellType(str, Enum):
    MAGIC = "magic"
    MIRACLE = "miracle"
    CRYOMANCY = "cryomancy"
    SORCERY = "sorcery"
```

### EffectType

Enumeration of effect types.

```python
class EffectType(str, Enum):
    DAMAGE = "damage"
    HEALING = "healing"
    BUFF = "buff"
    DEBUFF = "debuff"
    UTILITY = "utility"
```

### CatalystType

Enumeration of catalyst types.

```python
class CatalystType(str, Enum):
    STAFF = "staff"
    TALISMAN = "talisman"
    CHIME = "chime"
    PYROMANCY_FLAME = "pyromancy flame"
```

### ConsumableType

Enumeration of consumable types.

```python
class ConsumableType(str, Enum):
    ESTUS = "estus"
    KEY = "key"
    MATERIAL = "material"
    MISC = "misc"
```

### DiceRoll

Enumeration of dice types.

```python
class DiceRoll(str, Enum):
    D4 = "d4"
    D6 = "d6"
    D8 = "d8"
    D10 = "d10"
    D12 = "d12"
    D20 = "d20"
    D100 = "d100"
```

### StatName

Enumeration of character stats.

```python
class StatName(str, Enum):
    STRENGTH = "STR"
    DEXTERITY = "DEX"
    FAITH = "FTH"
    INTELLIGENCE = "INT"
    VITALITY = "VIT"
    ENDURANCE = "END"
```

## Character Models

### StatInfo

Represents a character stat with value and modifier.

```python
class StatInfo(BaseModel):
    value: conint(ge=0, le=99) = Field(description="Stat value between 0-99")
    modifier: int = Field(ge=-20, le=20, description="Modifier range")
```

**Fields:**
- `value` (int): Base stat value (0-99)
- `modifier` (int): Temporary modifier (-20 to +20)

**Validation:**
- Value must be between 0 and 99
- Modifier must be between -20 and 20

### ResourceInfo

Represents a character resource (HP, AP, etc.).

```python
class ResourceInfo(BaseModel):
    current: conint(ge=0)
    maximum: conint(ge=0)
```

**Fields:**
- `current` (int): Current resource amount
- `maximum` (int): Maximum resource amount

**Validation:**
- Both values must be non-negative

### MainCharacterInfo

Core character information.

```python
class MainCharacterInfo(BaseModel):
    name: str
    level: conint(ge=0, le=100)
    souls: conint(ge=0)
```

**Fields:**
- `name` (str): Character name
- `level` (int): Character level (0-100)
- `souls` (int): Amount of souls

**Validation:**
- Level must be between 0 and 100
- Souls must be non-negative

### Character

Complete character model.

```python
class Character(BaseModel):
    main: MainCharacterInfo
    stats: Dict[StatName, StatInfo]
    resources: Dict[str, ResourceInfo]
```

**Fields:**
- `main` (MainCharacterInfo): Core character data
- `stats` (Dict[StatName, StatInfo]): Character stats
- `resources` (Dict[str, ResourceInfo]): Character resources

### CharacterData

Complete character data with metadata.

```python
class CharacterData(BaseModel):
    character: Dict[str, Any]
    inventory: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

**Fields:**
- `character` (Dict): Character data
- `inventory` (Dict): Inventory data
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### CharacterCreate

Model for creating a new character.

```python
class CharacterCreate(BaseModel):
    character: Character
```

**Fields:**
- `character` (Character): Character data to create

### CharacterUpdate

Model for updating character data (all fields optional).

```python
class CharacterUpdate(BaseModel):
    character: Optional[Character] = None
```

**Fields:**
- `character` (Optional[Character]): Character data to update (partial)

### CharacterResponse

Response model that includes the character ID.

```python
class CharacterResponse(BaseModel):
    id: str
    character: Dict[str, Any]
```

**Fields:**
- `id` (str): Character UUID
- `character` (Dict): Character data

### EquipRequest

Model for equipping an item on a specific slot.

```python
class EquipRequest(BaseModel):
    item_name: str
    slot: EquipmentSlots
```

**Fields:**
- `item_name` (str): Name of the item to equip
- `slot` (EquipmentSlots): Target equipment slot

## Combat Models

### CombatParticipant

Represents a participant in combat.

```python
class CombatParticipant(BaseModel):
    characterSheetId: str
    isPlayer: bool
    initiative: int
    currentHP: Optional[int] = None
    maxHP: Optional[int] = None
    activeEffects: List[ActiveEffect] = Field(default_factory=list)
```

**Fields:**
- `characterSheetId` (str): Unique identifier for the character
- `isPlayer` (bool): Whether this is a player character
- `initiative` (int): Initiative roll for turn order
- `currentHP` (Optional[int]): Current hit points
- `maxHP` (Optional[int]): Maximum hit points
- `activeEffects` (List[ActiveEffect]): Active effects on this participant

### ActiveEffect

Represents an active effect on a participant.

```python
class ActiveEffect(BaseModel):
    name: str
    type: EffectType
    value: Optional[int] = None
    duration: int
    duration_type: EffectDurationType
    description: Optional[str] = None
```

**Fields:**
- `name` (str): Effect name
- `type` (EffectType): Type of effect (damage, healing, buff, etc.)
- `value` (Optional[int]): Effect value (damage amount, healing amount, etc.)
- `duration` (int): Remaining duration
- `duration_type` (EffectDurationType): Duration type (round or permanent)
- `description` (Optional[str]): Effect description

### EffectDurationType

Enumeration of effect duration types.

```python
class EffectDurationType(str, Enum):
    ROUND = "round"
    PERMANENT = "permanent"
```

### CombatState

Represents the current state of a combat session.

```python
class CombatState(BaseModel):
    combat_id: str
    is_active: bool
    currentRound: int = 1
    currentTurnIndex: int = 0
    turnOrder: List[str] = Field(default_factory=list)
    participants: Dict[str, CombatParticipant] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

**Fields:**
- `combat_id` (str): Unique combat identifier
- `is_active` (bool): Whether combat is currently active
- `currentRound` (int): Current round number
- `currentTurnIndex` (int): Index of current participant in turn order
- `turnOrder` (List[str]): Ordered list of participant IDs
- `participants` (Dict[str, CombatParticipant]): All participants
- `created_at` (datetime): Combat start time
- `updated_at` (datetime): Last update time

### ActionData

Represents an action to be performed in combat.

```python
class ActionData(BaseModel):
    actorId: str
    actionType: str
    targetId: Optional[str] = None
    spellName: Optional[str] = None
```

**Fields:**
- `actorId` (str): ID of the acting participant
- `actionType` (str): Type of action (Attack, Cast, Dodge, etc.)
- `targetId` (Optional[str]): Target participant ID
- `spellName` (Optional[str]): Name of spell to cast

## Item Models

### ItemBase

Base model for all items.

```python
class ItemBase(BaseModel):
    name: str
    type: ItemType
    rarity: str
    weight: float
    description: str
    slot: Optional[EquipmentSlots] = None
```

**Fields:**
- `name` (str): Item name
- `type` (ItemType): Item type
- `rarity` (str): Item rarity
- `weight` (float): Item weight
- `description` (str): Item description
- `slot` (Optional[EquipmentSlots]): Equipment slot (if applicable)

### Weapon

Weapon-specific model.

```python
class Weapon(ItemBase):
    damage: int
    damage_type: DamageType
    required_stats: Dict[StatName, int]
    scaling: Dict[ScalingStat, str]
    range: float
    attack_speed: float
```

**Fields:**
- `damage` (int): Base damage
- `damage_type` (DamageType): Type of damage
- `required_stats` (Dict[StatName, int]): Required stats to use
- `scaling` (Dict[ScalingStat, str]): Damage scaling with stats
- `range` (float): Attack range
- `attack_speed` (float): Attack speed modifier

### Armor

Armor-specific model.

```python
class Armor(ItemBase):
    defense: int
    armor_type: ArmorType
    required_stats: Dict[StatName, int]
    weight_reduction: float
```

**Fields:**
- `defense` (int): Defense value
- `armor_type` (ArmorType): Type of armor
- `required_stats` (Dict[StatName, int]): Required stats to wear
- `weight_reduction` (float): Weight reduction percentage

### Spell

Spell-specific model.

```python
class Spell(ItemBase):
    spell_type: SpellType
    cost: int
    effect: Dict[str, Any]
    range: float
    casting_time: float
```

**Fields:**
- `spell_type` (SpellType): Type of spell
- `cost` (int): Spell cost (AP)
- `effect` (Dict[str, Any]): Spell effects
- `range` (float): Spell range
- `casting_time` (float): Time to cast

### Catalyst

Catalyst-specific model.

```python
class Catalyst(ItemBase):
    catalyst_type: CatalystType
    scaling: Dict[ScalingStat, str]
    spell_buff: float
```

**Fields:**
- `catalyst_type` (CatalystType): Type of catalyst
- `scaling` (Dict[ScalingStat, str]): Spell damage scaling
- `spell_buff` (float): Spell damage multiplier

### Consumable

Consumable-specific model.

```python
class Consumable(ItemBase):
    consumable_type: ConsumableType
    effect: Dict[str, Any]
    quantity: int = 1
```

**Fields:**
- `consumable_type` (ConsumableType): Type of consumable
- `effect` (Dict[str, Any]): Effect when consumed
- `quantity` (int): Stack size

### Inventory

Complete inventory model.

```python
class Inventory(BaseModel):
    weapons: List[Weapon] = Field(default_factory=list)
    armors: List[Armor] = Field(default_factory=list)
    catalysts: List[Catalyst] = Field(default_factory=list)
    items: List[Consumable] = Field(default_factory=list)
    spells: List[Spell] = Field(default_factory=list)
```

**Fields:**
- `weapons` (List[Weapon]): Weapon inventory
- `armors` (List[Armor]): Armor inventory
- `catalysts` (List[Catalyst]): Catalyst inventory
- `items` (List[Consumable]): Consumable inventory
- `spells` (List[Spell]): Spell inventory

**Validation:**
- No duplicate items in the same slot
- Items must be properly categorized

## Usage Examples

### Creating a Character

```python
from src.models.character import CharacterCreate, Character, MainCharacterInfo, StatInfo, ResourceInfo

character_data = CharacterCreate(
    character=Character(
        main=MainCharacterInfo(
            name="Arthur",
            level=1,
            souls=0
        ),
        stats={
            "STR": StatInfo(value=10, modifier=0),
            "DEX": StatInfo(value=10, modifier=0)
        },
        resources={
            "HP": ResourceInfo(current=100, maximum=100),
            "AP": ResourceInfo(current=50, maximum=50)
        }
    )
)
```

### Creating a Combat Participant

```python
from src.models.combat import CombatParticipant, ActiveEffect, EffectType, EffectDurationType

participant = CombatParticipant(
    characterSheetId="player-1",
    isPlayer=True,
    initiative=18,
    currentHP=100,
    maxHP=100,
    activeEffects=[
        ActiveEffect(
            name="Blessing",
            type=EffectType.BUFF,
            value=5,
            duration=2,
            duration_type=EffectDurationType.ROUND,
            description="Attack bonus"
        )
    ]
)
```

### Creating an Item

```python
from src.models.item import Weapon, ItemType, DamageType, StatName

weapon = Weapon(
    name="Long Sword",
    type=ItemType.WEAPON,
    rarity="Common",
    weight=4.0,
    description="A standard long sword.",
    slot="right_hand",
    damage=15,
    damage_type=DamageType.SLASHING,
    required_stats={"STR": 12, "DEX": 10},
    scaling={"STR": "C", "DEX": "C"},
    range=1.5,
    attack_speed=1.2
)
```

## Validation Rules

### Character Validation
- Level must be between 0 and 100
- Stat values must be between 0 and 99
- Stat modifiers must be between -20 and 20
- Resource values must be non-negative

### Combat Validation
- Initiative must be a positive integer
- HP values must be non-negative
- Effect durations must be positive
- Turn order must contain valid participant IDs

### Item Validation
- Weight must be non-negative
- Required stats must be valid stat names
- Damage values must be positive
- Rarity must be a valid string

### Inventory Validation
- No duplicate items in the same slot
- Items must match their assigned slots
- Quantities must be positive
