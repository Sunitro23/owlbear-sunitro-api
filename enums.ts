// Enums remain mostly the same, but remove WeaponType as instructed.
// Added ScalingStat as a new type for simplicity.
export const EquipmentSlots = {
    ARMOR: 'armor',
    RIGHT_HAND: 'right_hand',
    LEFT_HAND: 'left_hand',
    CONSUMABLE: 'consumable',
    BAG: 'bag'
} as const;

export type EquipmentSlot = keyof typeof EquipmentSlots;

export const ItemType = {
    WEAPON: 'weapon',
    ARMOR: 'armor',
    SPELL: 'spell',
    CATALYST: 'catalyst',
    CONSUMABLE: 'consumable',
} as const;

export type ItemTypeKey = keyof typeof ItemType;

export const DamageType = {
    SLASHING: 'slashing',
    PIERCING: 'piercing',
    BLUDGEONING: 'bludgeoning',
    FIRE: 'fire',
    LIGHTNING: 'lightning',
    MAGIC: 'magic',
    DARK: 'dark',
    FROST: 'frost'
} as const;

export type DamageTypeKey = keyof typeof DamageType;

export const ArmorType = {
    LIGHT: 'light',
    MEDIUM: 'medium',
    HEAVY: 'heavy',
    FIRE: 'fire',
    LIGHTNING: 'lightning',
    MAGIC: 'magic',
    DARK: 'dark',
    FROST: 'frost'
} as const;

export type ArmorTypeKey = keyof typeof ArmorType;

export const SpellType = {
    MAGIC: 'magic',
    MIRACLE: 'miracle',
    CRYOMANCY: 'cryomancy',
    SORCERY: 'sorcery'
} as const;

export type SpellTypeKey = keyof typeof SpellType;

export const EffectType = {
    DAMAGE: 'damage',
    HEALING: 'healing',
    BUFF: 'buff',
    DEBUFF: 'debuff',
    UTILITY: 'utility'
} as const;

export type EffectTypeKey = keyof typeof EffectType;

export const CatalystType = {
    STAFF: 'staff',
    TALISMAN: 'talisman',
    CHIME: 'chime',
    PYROMANCY_FLAME: 'pyromancy flame'
} as const;

export type CatalystTypeKey = keyof typeof CatalystType;

export const ConsumableType = {
    ESTUS: 'estus',
    KEY: 'key',
    MATERIAL: 'material',
    MISC: 'misc'
} as const;

export type ConsumableTypeKey = keyof typeof ConsumableType;

export type ScalingStat = 'STR' | 'DEX' | 'FTH' | 'INT';

export const DiceRoll = {
    D4: 'd4',
    D6: 'd6',
    D8: 'd8',
    D10: 'd10',
    D12: 'd12',
    D20: 'd20',
    D100: 'd100'
} as const;

export type DiceRollKey = keyof typeof DiceRoll;

// Simplified BaseItem: removed description, value, rarity, requirements, and stackable.
interface BaseItem {
    id: string;              // Unique identifier
    name: string;            // Display name
    slot: EquipmentSlot;     // Slot where the item is stored/equipped
}

// Discriminated unions for items.
export type Item =
| WeaponItem
| ArmorItem
| SpellItem
| CatalystItem
| ConsumableItem;

export interface WeaponItem extends BaseItem {
    type: typeof ItemType.WEAPON;
    damageType: DamageTypeKey;
    dice: DiceRollKey;
    scalingStat?: ScalingStat;
    twoHanded?: boolean;
    flatBonus: number;       // For weapon upgrades
}

export interface ArmorItem extends BaseItem {
    type: typeof ItemType.ARMOR;
    armorType: ArmorTypeKey;
    flatBonus: number;       // For armor upgrades
    // Flat reduction and resistances are derived from armorType externally.
    // No defense or resistances fields here.
}

export interface SpellItem extends BaseItem {
    type: typeof ItemType.SPELL;
    spellType: SpellTypeKey;
    effectType: EffectTypeKey;
    manaCost: number;
    dice: DiceRollKey;
    scalingStat?: ScalingStat;
    duration?: number;
    requiresCatalyst: CatalystTypeKey; // Required: Specific catalyst (e.g., map from spellType)
}

export interface CatalystItem extends BaseItem {
    type: typeof ItemType.CATALYST;
    catalystType: CatalystTypeKey;
    flatBonus: number;  
}

export interface ConsumableItem extends BaseItem {
    type: typeof ItemType.CONSUMABLE;
    consumableType: ConsumableTypeKey;
    effect: string;
    quantity: number;
}

// Inventory structure organized by category with separate arrays for each item type
export interface Inventory {
    weapons: WeaponItem[];
    armors: ArmorItem[];
    catalysts: CatalystItem[];
    items: ConsumableItem[];  // Consumables and misc items
    spells: SpellItem[];
}
