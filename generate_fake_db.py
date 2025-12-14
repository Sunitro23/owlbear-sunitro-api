from faker import Faker
import json
import random
from models import (
    CharacterData, Character, MainCharacterInfo, StatInfo, ResourceInfo,
    WeaponItem, ArmorItem, SpellItem, CatalystItem, ConsumableItem,
    EquipmentSlots, ItemType, DamageType, DiceRoll, ScalingStat, ArmorType,
    SpellType, EffectType, CatalystType, ConsumableType, SoulInfo
)

fake = Faker()

def fake_weapon():
    return WeaponItem(
        id=fake.uuid4(),
        name=fake.words(1)[0].capitalize() + " Sword",
        slot=random.choice([EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND]),
        damageType=random.choice(list(DamageType)),
        dice=random.choice(list(DiceRoll)),
        scalingStat=random.choice([None] + list(['STR', 'DEX', 'FTH', 'INT'])),
        twoHanded=random.choice([True, False, None]),
        flatBonus=random.randint(5, 50)
    )

def fake_armor():
    return ArmorItem(
        id=fake.uuid4(),
        name=fake.words(1)[0].capitalize() + " Armor",
        slot=EquipmentSlots.ARMOR,
        armorType=random.choice(list(ArmorType)),
        flatBonus=random.randint(1, 30)
    )

def fake_spell():
    return SpellItem(
        id=fake.uuid4(),
        name=fake.words(1)[0].capitalize() + " Spell",
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
        id=fake.uuid4(),
        name=fake.words(1)[0].capitalize() + " Catalyst",
        slot=random.choice([EquipmentSlots.RIGHT_HAND, EquipmentSlots.LEFT_HAND]),
        catalystType=random.choice(list(CatalystType)),
        flatBonus=random.randint(1, 20)
    )

def fake_consumable():
    return ConsumableItem(
        id=fake.uuid4(),
        name=fake.words(1)[0].capitalize() + " Flask",
        slot=EquipmentSlots.CONSUMABLE,
        consumableType=random.choice(list(ConsumableType)),
        effect=fake.sentence(),
        uses=random.randint(1, 10),
        max_uses=random.randint(10, 50)
    )

def fake_character_data():
    # Generate info
    name = fake.name()
    level = SoulInfo(value=random.randint(1, 100), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/level.png', label='Level')
    hollowing = SoulInfo(value=random.randint(0, 5), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/humanity.png', label='Hollowing')
    souls = SoulInfo(value=random.randint(0, 10000), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/soul.png', label='Souls')

    # Generate stats
    stats = {
        'STR': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/strength.png', label='Strength'),
        'DEX': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/dexterity.png', label='Dexterity'),
        'FTH': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/faith.png', label='Faith'),
        'INT': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/intelligence.png', label='Intelligence'),
        'VIT': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/vigor.png', label='Vitality'),
        'END': StatInfo(value=random.randint(1, 99), modifier=random.randint(-5, 10), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/endurance.png', label='Endurance'),
    }

    # Generate resources
    resources = {
        'HP': ResourceInfo(value=random.randint(100, 1000), max=random.randint(1000, 10000), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/hp.png', label='Health'),
        'AP': ResourceInfo(value=random.randint(50, 500), max=random.randint(500, 5000), icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/stamina.png', label='Action Points'),
        'SpellSlots': ResourceInfo(value=random.randint(1, 4), max=4, icon='https://darksouls3.wdfiles.com/local--files/image-sets:menu-icons/fp.png', label='Spell Slots'),
    }

    character_data = {
        'name': name,
        'image': fake.image_url(width=300, height=300),
        'resources': {
            'level': level.model_dump(),
            'souls': souls.model_dump(),
            'hollowing': hollowing.model_dump(),
            'HP': resources['HP'].model_dump(),
            'AP': resources['AP'].model_dump(),
            'SpellSlots': resources['SpellSlots'].model_dump()
        },
        'stats': {k: v.model_dump() for k, v in stats.items()}
    }

    # Generate inventory
    inventory = {
        'weapons': [fake_weapon().model_dump() for _ in range(random.randint(0, 5))],
        'armors': [fake_armor().model_dump() for _ in range(random.randint(0, 3))],
        'catalysts': [fake_catalyst().model_dump() for _ in range(random.randint(0, 3))],
        'items': [fake_consumable().model_dump() for _ in range(random.randint(15, 25))],
        'spells': [fake_spell().model_dump() for _ in range(random.randint(0, 5))]
    }

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
