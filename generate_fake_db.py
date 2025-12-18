from faker import Faker
import json
import random
from models import (
    CharacterData, Character, MainCharacterInfo, StatInfo,
    WeaponItem, ArmorItem, SpellItem, CatalystItem, ConsumableItem,
    EquipmentSlots, ItemType, DamageType, DiceRoll, ScalingStat, ArmorType,
    SpellType, EffectType, CatalystType, ConsumableType, StatName
)
from datetime import datetime

fake = Faker()

def fake_weapon():
    return WeaponItem(
        name=fake.words(1)[0].capitalize() + " Sword",
        image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/longsword.png",
        slot=random.choice([EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND]),
        damageType=random.choice(list(DamageType)),
        dice=random.choice(list(DiceRoll)),
        scalingStat=random.choice([None] + list(['STR', 'DEX', 'FTH', 'INT'])),
        twoHanded=random.choice([True, False, None]),
        flatBonus=random.randint(5, 50)
    )

def fake_armor():
    return ArmorItem(
        name=fake.words(1)[0].capitalize() + " Armor",
        image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/alva_helm.png",
        slot=EquipmentSlots.ARMOR,
        armorType=random.choice(list(ArmorType)),
        flatBonus=random.randint(1, 30)
    )

def fake_spell():
    return SpellItem(
        name=fake.words(1)[0].capitalize() + " Spell",
        image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/heal_aid-icon.png",
        slot=random.choice([EquipmentSlots.SPELL_1, EquipmentSlots.SPELL_2, EquipmentSlots.SPELL_3, EquipmentSlots.SPELL_4]),
        spellType=random.choice(list(SpellType)),
        effectType=random.choice(list(EffectType)),
        dice=random.choice(list(DiceRoll)),
        scalingStat=random.choice([None] + list(['STR', 'DEX', 'FTH', 'INT'])),
        duration=random.choice([random.randint(1, 10), None]),
        requiresCatalyst=random.choice(list(CatalystType)),
        uses=random.randint(1, 5),
        max_uses=random.choice([random.randint(5, 20), None])
    )

def fake_catalyst():
    return CatalystItem(
        name=fake.words(1)[0].capitalize() + " Catalyst",
        image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/yorshkas_chime-icon.png",
        slot=random.choice([EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND]),
        catalystType=random.choice(list(CatalystType)),
        flatBonus=random.randint(1, 20)
    )

def fake_consumable():
    return ConsumableItem(
        name=fake.words(1)[0].capitalize() + " Flask",
        image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/estus_flask-icon.png",
        slot=EquipmentSlots.CONSUMABLE,
        consumableType=random.choice(list(ConsumableType)),
        effect=fake.sentence(),
        uses=random.randint(1, 10),
        max_uses=random.randint(10, 50)
    )

def fake_character_data():
    # Generate info
    name = fake.name()
    level = random.randint(0, 100)
    souls = random.randint(0, 10000)

    # Generate stats
    stats = {
        StatName.STRENGTH: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
        StatName.DEXTERITY: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
        StatName.FAITH: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
        StatName.INTELLIGENCE: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
        StatName.VITALITY: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
        StatName.ENDURANCE: StatInfo(value=random.randint(0, 99), modifier=random.randint(-20, 20)),
    }

    # Generate resources with current/max
    HP_current = random.randint(100, 1000)
    HP_max = HP_current + random.randint(50, 200)
    AP_current = random.randint(50, 500)
    AP_max = AP_current + random.randint(50, 200)
    spell_slots_current = random.randint(1, 4)
    spell_slots_max = max(spell_slots_current, spell_slots_current + random.randint(0, 4))
    hollowing_current = random.randint(0, 5)
    hollowing_max = 10  # fixed max

    resources = {
        'HP': {'current': HP_current, 'maximum': HP_max},
        'AP': {'current': AP_current, 'maximum': AP_max},
        'SpellSlots': {'current': spell_slots_current, 'maximum': spell_slots_max},
        'Hollowing': {'current': hollowing_current, 'maximum': hollowing_max}
    }

    character_data = {
        'name': name,
        'image': "https://media.discordapp.net/attachments/1152637343891718175/1378092621448347800/Sans_titre_2_20250530004519.png?ex=69410a04&is=693fb884&hm=a2bf92825d11d4a6a693837b55cc4bcd383dd7e5b5c7d73b6c1862634ecde4cb&=&format=webp&quality=lossless",
        'level': level,
        'souls': souls,
        'resources': resources,
        'stats': {k: v.model_dump() for k, v in stats.items()}
    }

    # Generate inventory with unique slots
    available_slots = set([
        EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND, EquipmentSlots.ARMOR,
        EquipmentSlots.CONSUMABLE, EquipmentSlots.SPELL_1, EquipmentSlots.SPELL_2,
        EquipmentSlots.SPELL_3, EquipmentSlots.SPELL_4
    ])

    inventory = {'weapons': [], 'armors': [], 'catalysts': [], 'items': [], 'spells': []}

    # Generate weapons (0-2, using hand slots)
    num_weapons = random.randint(0, 2)
    hand_slots = available_slots & {EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND}
    if hand_slots:
        chosen_weapons = random.sample(list(hand_slots), min(num_weapons, len(hand_slots)))
        for slot in chosen_weapons:
            available_slots.remove(slot)
            weapon = WeaponItem(
                name=fake.words(1)[0].capitalize() + " Sword",
                image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/longsword.png",
                slot=slot,
                damageType=random.choice(list(DamageType)),
                dice=random.choice(list(DiceRoll)),
                scalingStat=random.choice([None] + list(['STR', 'DEX', 'FTH', 'INT'])),
                twoHanded=random.choice([True, False, None]),
                flatBonus=random.randint(5, 50)
            ).model_dump()
            inventory['weapons'].append(weapon)

    # Generate catalysts (0-2, using hand slots)
    num_catalysts = random.randint(0, 2)
    hand_slots = available_slots & {EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND}
    if hand_slots:
        chosen_catalysts = random.sample(list(hand_slots), min(num_catalysts, len(hand_slots)))
        for slot in chosen_catalysts:
            available_slots.remove(slot)
            catalyst = CatalystItem(
                name=fake.words(1)[0].capitalize() + " Catalyst",
                image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/yorshkas_chime-icon.png",
                slot=slot,
                catalystType=random.choice(list(CatalystType)),
                flatBonus=random.randint(1, 20)
            ).model_dump()
            inventory['catalysts'].append(catalyst)

    # Generate armor (at most 1)
    if random.choice([True, False]) and EquipmentSlots.ARMOR in available_slots:
        available_slots.remove(EquipmentSlots.ARMOR)
        armor = ArmorItem(
            name=fake.words(1)[0].capitalize() + " Armor",
            image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/alva_helm.png",
            slot=EquipmentSlots.ARMOR,
            armorType=random.choice(list(ArmorType)),
            flatBonus=random.randint(1, 30)
        ).model_dump()
        inventory['armors'].append(armor)

    # Generate consumable (at most 1)
    if random.choice([True, False]) and EquipmentSlots.CONSUMABLE in available_slots:
        available_slots.remove(EquipmentSlots.CONSUMABLE)
        consumable = ConsumableItem(
            name=fake.words(1)[0].capitalize() + " Flask",
            image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/estus_flask-icon.png",
            slot=EquipmentSlots.CONSUMABLE,
            consumableType=random.choice(list(ConsumableType)),
            effect=fake.sentence(),
            uses=random.randint(1, 10),
            max_uses=random.randint(10, 50)
        ).model_dump()
        inventory['items'].append(consumable)

    # Generate spells (0-4 unique spell slots)
    spell_slots = available_slots & {EquipmentSlots.SPELL_1, EquipmentSlots.SPELL_2, EquipmentSlots.SPELL_3, EquipmentSlots.SPELL_4}
    num_spells = random.randint(0, len(spell_slots))
    chosen_spell_slots = random.sample(list(spell_slots), num_spells)
    for slot in chosen_spell_slots:
        available_slots.remove(slot)
        spell = SpellItem(
            name=fake.words(1)[0].capitalize() + " Spell",
            image="https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/heal_aid-icon.png",
            slot=slot,
            spellType=random.choice(list(SpellType)),
            effectType=random.choice(list(EffectType)),
            dice=random.choice(list(DiceRoll)),
            scalingStat=random.choice([None] + list(['STR', 'DEX', 'FTH', 'INT'])),
            duration=random.choice([random.randint(1, 10), None]),
            requiresCatalyst=random.choice(list(CatalystType)),
            uses=random.randint(1, 5),
            max_uses=random.choice([random.randint(5, 20), None])
        ).model_dump()
        inventory['spells'].append(spell)

    return {
        'character': character_data,
        'inventory': inventory
    }

# Generate multiple characters with IDs
database = {}
for i in range(1, 11):
    char_data = fake_character_data()
    database[str(i)] = char_data

# Save to JSON
with open('characters.json', 'w') as f:
    json.dump(database, f, indent=2, ensure_ascii=False)  # Match the database.py format

print("Fake database generated in characters.json")
