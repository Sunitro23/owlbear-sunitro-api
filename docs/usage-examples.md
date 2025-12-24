# Usage Examples and Tutorials

## Overview

This document provides practical examples and tutorials for using the Dark Souls API. It covers common use cases, integration examples, and best practices for developers.

## Getting Started

### Prerequisites

Before using the API, ensure you have:

- Python 3.9+ installed
- FastAPI and dependencies installed
- The API server running locally

### Starting the Server

```bash
# Navigate to the project directory
cd darksouls_api

# Install dependencies
pip install -r requirements.txt

# Start the development server
python -m uvicorn src.api.main:app --reload

# Server will be available at http://localhost:8000
```

## Character Management Examples

### Creating a Character

#### Basic Character Creation

```python
import requests
import json

# Character data
character_data = {
    "character": {
        "main": {
            "name": "Arthur",
            "level": 1,
            "souls": 0
        },
        "stats": {
            "STR": {"value": 10, "modifier": 0},
            "DEX": {"value": 10, "modifier": 0},
            "FTH": {"value": 8, "modifier": 0},
            "INT": {"value": 8, "modifier": 0}
        },
        "resources": {
            "HP": {"current": 100, "maximum": 100},
            "AP": {"current": 50, "maximum": 50}
        }
    }
}

# Create character
response = requests.post(
    "http://localhost:8000/characters",
    json=character_data
)

if response.status_code == 201:
    character = response.json()
    print(f"Character created with ID: {character['id']}")
else:
    print(f"Error: {response.json()}")
```

#### Creating a Character with Inventory

```python
import requests

character_with_inventory = {
    "character": {
        "main": {
            "name": "Gwyn",
            "level": 120,
            "souls": 100000
        },
        "stats": {
            "STR": {"value": 20, "modifier": 0},
            "DEX": {"value": 20, "modifier": 0},
            "FTH": {"value": 20, "modifier": 0},
            "INT": {"value": 20, "modifier": 0}
        },
        "resources": {
            "HP": {"current": 150, "maximum": 150},
            "AP": {"current": 75, "maximum": 75}
        }
    },
    "inventory": {
        "weapons": [
            {
                "name": "Sunlight Straight Sword",
                "type": "weapon",
                "rarity": "Legendary",
                "weight": 8.0,
                "description": "A sword blessed by the sun.",
                "slot": "right_hand",
                "damage": 25,
                "damage_type": "holy",
                "required_stats": {"STR": 15, "DEX": 15},
                "scaling": {"STR": "C", "DEX": "C"},
                "range": 1.2,
                "attack_speed": 1.0
            }
        ],
        "armors": [],
        "catalysts": [],
        "items": [
            {
                "name": "Estus Flask",
                "type": "consumable",
                "rarity": "Common",
                "weight": 0.5,
                "description": "Restores HP.",
                "slot": "consumable",
                "consumable_type": "estus",
                "effect": {"healing": 50},
                "quantity": 5
            }
        ],
        "spells": []
    }
}

response = requests.post(
    "http://localhost:8000/characters",
    json=character_with_inventory
)
```

### Updating Characters

#### Full Character Update

```python
import requests

# Update entire character
updated_data = {
    "character": {
        "main": {
            "name": "Arthur the Brave",
            "level": 5,
            "souls": 5000
        },
        "stats": {
            "STR": {"value": 12, "modifier": 0},
            "DEX": {"value": 12, "modifier": 0},
            "FTH": {"value": 10, "modifier": 0},
            "INT": {"value": 10, "modifier": 0}
        },
        "resources": {
            "HP": {"current": 120, "maximum": 120},
            "AP": {"current": 60, "maximum": 60}
        }
    }
}

response = requests.put(
    "http://localhost:8000/characters/your-character-id",
    json=updated_data
)
```

#### Partial Character Update (PATCH)

```python
import requests

# Update only specific fields
partial_update = {
    "character": {
        "souls": 15000,
        "stats": {
            "STR": {"value": 15}
        }
    }
}

response = requests.patch(
    "http://localhost:8000/characters/your-character-id",
    json=partial_update
)
```

### Equipping Items

```python
import requests

# Equip a weapon
equip_data = {
    "item_name": "Long Sword",
    "slot": "right_hand"
}

response = requests.patch(
    "http://localhost:8000/characters/your-character-id/equip",
    json=equip_data
)

if response.status_code == 200:
    updated_character = response.json()
    print("Item equipped successfully!")
else:
    print(f"Error: {response.json()}")
```

### Character Management Script

```python
import requests
import json

class DarkSoulsClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def create_character(self, character_data):
        """Create a new character"""
        response = requests.post(
            f"{self.base_url}/characters",
            json=character_data
        )
        return response.json()
    
    def get_character(self, character_id):
        """Get a character by ID"""
        response = requests.get(f"{self.base_url}/characters/{character_id}")
        return response.json()
    
    def update_character(self, character_id, update_data):
        """Update a character"""
        response = requests.patch(
            f"{self.base_url}/characters/{character_id}",
            json=update_data
        )
        return response.json()
    
    def equip_item(self, character_id, item_name, slot):
        """Equip an item"""
        data = {"item_name": item_name, "slot": slot}
        response = requests.patch(
            f"{self.base_url}/characters/{character_id}/equip",
            json=data
        )
        return response.json()
    
    def delete_character(self, character_id):
        """Delete a character"""
        response = requests.delete(f"{self.base_url}/characters/{character_id}")
        return response.json()

# Usage example
client = DarkSoulsClient()

# Create a character
character_data = {
    "character": {
        "main": {"name": "Player", "level": 1, "souls": 0},
        "stats": {"STR": {"value": 10, "modifier": 0}, "DEX": {"value": 10, "modifier": 0}},
        "resources": {"HP": {"current": 100, "maximum": 100}, "AP": {"current": 50, "maximum": 50}}
    }
}

created = client.create_character(character_data)
character_id = created["id"]

# Update character
client.update_character(character_id, {"character": {"souls": 1000}})

# Equip item
client.equip_item(character_id, "Long Sword", "right_hand")
```

## Combat System Examples

### Starting a Combat Session

```python
import requests

# Define participants
participants = [
    {
        "characterSheetId": "player-1",
        "isPlayer": True,
        "initiative": 18,
        "currentHP": 100,
        "maxHP": 100
    },
    {
        "characterSheetId": "enemy-1",
        "isPlayer": False,
        "initiative": 12,
        "currentHP": 80,
        "maxHP": 80
    },
    {
        "characterSheetId": "enemy-2",
        "isPlayer": False,
        "initiative": 15,
        "currentHP": 60,
        "maxHP": 60
    }
]

# Start combat
response = requests.post(
    "http://localhost:8000/combat/start",
    json=participants
)

if response.status_code == 200:
    result = response.json()
    print(f"Combat started: {result['message']}")
    print(f"Combat ID: {result['combat_id']}")
else:
    print(f"Error starting combat: {response.json()}")
```

### Performing Combat Actions

```python
import requests
import time

def perform_combat_actions():
    # Get current turn
    response = requests.get("http://localhost:8000/combat/turn")
    turn_info = response.json()
    
    current_participant = turn_info["current_participant_id"]
    
    # Perform action based on participant type
    if "player" in current_participant:
        # Player action
        action = {
            "actorId": current_participant,
            "actionType": "Attack",
            "targetId": "enemy-1"
        }
    else:
        # Enemy action (simplified AI)
        action = {
            "actorId": current_participant,
            "actionType": "Attack",
            "targetId": "player-1"
        }
    
    # Execute action
    response = requests.post(
        "http://localhost:8000/combat/action",
        json=action
    )
    
    result = response.json()
    print(f"Action result: {result}")
    
    # End turn
    response = requests.post("http://localhost:8000/combat/end-turn")
    next_turn = response.json()
    print(f"Next turn: {next_turn}")

# Run combat loop
while True:
    try:
        perform_combat_actions()
        time.sleep(1)  # Wait between actions
    except Exception as e:
        print(f"Combat ended: {e}")
        break
```

### Managing Combat Effects

```python
import requests

# Apply a buff effect
buff_effect = {
    "participant_id": "player-1",
    "effect": {
        "name": "Blessing",
        "type": "buff",
        "value": 5,
        "duration": 3,
        "duration_type": "round",
        "description": "Attack bonus"
    }
}

response = requests.post(
    "http://localhost:8000/combat/effect",
    json=buff_effect
)

# Apply a damage over time effect
poison_effect = {
    "participant_id": "enemy-1",
    "effect": {
        "name": "Poison",
        "type": "damage",
        "value": 3,
        "duration": 5,
        "duration_type": "round",
        "description": "Poison damage over time"
    }
}

response = requests.post(
    "http://localhost:8000/combat/effect",
    json=poison_effect
)

# Update effects (process durations)
response = requests.post("http://localhost:8000/combat/effects/update")
result = response.json()
print(f"Expired effects: {result['expired_effects']}")
```

### Combat Management Script

```python
import requests
import random

class CombatManager:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def start_combat(self, participants):
        """Start a new combat"""
        response = requests.post(
            f"{self.base_url}/combat/start",
            json=participants
        )
        return response.json()
    
    def get_combat_status(self):
        """Get current combat status"""
        response = requests.get(f"{self.base_url}/combat/status")
        return response.json()
    
    def perform_action(self, action_data):
        """Perform an action in combat"""
        response = requests.post(
            f"{self.base_url}/combat/action",
            json=action_data
        )
        return response.json()
    
    def end_combat(self):
        """End current combat"""
        response = requests.post(f"{self.base_url}/combat/end")
        return response.json()
    
    def get_current_turn(self):
        """Get current turn information"""
        response = requests.get(f"{self.base_url}/combat/turn")
        return response.json()
    
    def end_turn(self):
        """End current turn"""
        response = requests.post(f"{self.base_url}/combat/end-turn")
        return response.json()

# Usage example
combat = CombatManager()

# Start combat
participants = [
    {"characterSheetId": "player-1", "isPlayer": True, "initiative": 18},
    {"characterSheetId": "enemy-1", "isPlayer": False, "initiative": 12}
]

combat.start_combat(participants)

# Combat loop
while True:
    try:
        turn = combat.get_current_turn()
        current_id = turn["current_participant_id"]
        
        # Simple AI logic
        if "player" in current_id:
            action = {
                "actorId": current_id,
                "actionType": "Attack",
                "targetId": "enemy-1"
            }
        else:
            action = {
                "actorId": current_id,
                "actionType": "Attack",
                "targetId": "player-1"
            }
        
        # Perform action
        result = combat.perform_action(action)
        print(f"Action result: {result}")
        
        # End turn
        combat.end_turn()
        
    except Exception as e:
        print(f"Combat ended: {e}")
        break
```

## Advanced Examples

### Character Progression System

```python
import requests
import time

class CharacterProgression:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def level_up_character(self, character_id, levels=1):
        """Level up a character and distribute stats"""
        # Get current character data
        response = requests.get(f"{self.base_url}/characters/{character_id}")
        character = response.json()
        
        current_level = character["character"]["main"]["level"]
        new_level = current_level + levels
        
        # Calculate stat increases (simplified)
        stat_increases = {
            "STR": {"value": character["character"]["stats"]["STR"]["value"] + levels},
            "DEX": {"value": character["character"]["stats"]["DEX"]["value"] + levels},
            "FTH": {"value": character["character"]["stats"]["FTH"]["value"] + levels},
            "INT": {"value": character["character"]["stats"]["INT"]["value"] + levels}
        }
        
        # Update character
        update_data = {
            "character": {
                "main": {"level": new_level},
                "stats": stat_increases
            }
        }
        
        response = requests.patch(
            f"{self.base_url}/characters/{character_id}",
            json=update_data
        )
        
        return response.json()
    
    def gain_souls(self, character_id, souls_gained):
        """Add souls to character"""
        response = requests.get(f"{self.base_url}/characters/{character_id}")
        character = response.json()
        
        current_souls = character["character"]["main"]["souls"]
        new_souls = current_souls + souls_gained
        
        update_data = {
            "character": {"main": {"souls": new_souls}}
        }
        
        response = requests.patch(
            f"{self.base_url}/characters/{character_id}",
            json=update_data
        )
        
        return response.json()

# Usage example
progression = CharacterProgression()

# Level up character
character_id = "your-character-id"
progression.level_up_character(character_id, levels=5)

# Gain souls from defeating enemy
progression.gain_souls(character_id, souls_gained=2500)
```

### Inventory Management System

```python
import requests

class InventoryManager:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def add_item_to_inventory(self, character_id, item_data):
        """Add an item to character's inventory"""
        # Get current inventory
        response = requests.get(f"{self.base_url}/characters/{character_id}")
        character = response.json()
        
        inventory = character["inventory"]
        
        # Add item to appropriate category
        item_type = item_data["type"]
        if item_type == "weapon":
            inventory["weapons"].append(item_data)
        elif item_type == "armor":
            inventory["armors"].append(item_data)
        elif item_type == "spell":
            inventory["spells"].append(item_data)
        elif item_type == "consumable":
            inventory["items"].append(item_data)
        
        # Update character
        update_data = {"inventory": inventory}
        response = requests.patch(
            f"{self.base_url}/characters/{character_id}",
            json=update_data
        )
        
        return response.json()
    
    def use_consumable(self, character_id, item_name):
        """Use a consumable item"""
        # Get character data
        response = requests.get(f"{self.base_url}/characters/{character_id}")
        character = response.json()
        
        # Find and use the consumable
        for item in character["inventory"]["items"]:
            if item["name"] == item_name and item["consumable_type"] == "estus":
                # Apply effect (healing)
                current_hp = character["character"]["resources"]["HP"]["current"]
                max_hp = character["character"]["resources"]["HP"]["maximum"]
                healing = item["effect"]["healing"]
                
                new_hp = min(current_hp + healing, max_hp)
                
                # Update HP
                update_data = {
                    "character": {
                        "resources": {
                            "HP": {"current": new_hp}
                        }
                    }
                }
                
                response = requests.patch(
                    f"{self.base_url}/characters/{character_id}",
                    json=update_data
                )
                
                return response.json()
        
        return {"error": "Consumable not found"}

# Usage example
inventory = InventoryManager()

# Add a weapon to inventory
weapon = {
    "name": "Broadsword",
    "type": "weapon",
    "rarity": "Common",
    "weight": 4.0,
    "description": "A standard broadsword.",
    "slot": "right_hand",
    "damage": 12,
    "damage_type": "slashing",
    "required_stats": {"STR": 10, "DEX": 10},
    "scaling": {"STR": "C", "DEX": "C"},
    "range": 1.0,
    "attack_speed": 1.2
}

inventory.add_item_to_inventory("character-id", weapon)

# Use an estus flask
inventory.use_consumable("character-id", "Estus Flask")
```

### Integration with Game Client

```python
import requests
import asyncio
import websockets
import json

class GameClient:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.websocket_url = "ws://localhost:8000/ws"  # If WebSocket endpoint exists
    
    async def connect_to_game(self):
        """Connect to game server via WebSocket"""
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                while True:
                    # Receive game events
                    message = await websocket.recv()
                    event = json.loads(message)
                    
                    # Handle different event types
                    if event["type"] == "combat_start":
                        await self.handle_combat_start(event)
                    elif event["type"] == "character_action":
                        await self.handle_character_action(event)
                    elif event["type"] == "item_pickup":
                        await self.handle_item_pickup(event)
                    
        except websockets.exceptions.ConnectionClosed:
            print("Game connection closed")
    
    async def handle_combat_start(self, event):
        """Handle combat start event"""
        participants = event["participants"]
        
        # Start combat via API
        response = requests.post(
            f"{self.api_url}/combat/start",
            json=participants
        )
        
        print(f"Combat started: {response.json()}")
    
    async def handle_character_action(self, event):
        """Handle character action event"""
        action = event["action"]
        
        # Perform action via API
        response = requests.post(
            f"{self.api_url}/combat/action",
            json=action
        )
        
        result = response.json()
        print(f"Action result: {result}")
    
    async def handle_item_pickup(self, event):
        """Handle item pickup event"""
        character_id = event["character_id"]
        item_data = event["item"]
        
        # Add item to inventory via API
        response = requests.patch(
            f"{self.api_url}/characters/{character_id}/inventory",
            json=item_data
        )
        
        print(f"Item picked up: {response.json()}")

# Usage example
async def main():
    client = GameClient()
    await client.connect_to_game()

# Run the game client
# asyncio.run(main())
```

## Best Practices

### Error Handling

```python
import requests

def safe_api_call(url, method="GET", data=None, retries=3):
    """Make a safe API call with error handling and retries"""
    for attempt in range(retries):
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            elif method == "PUT":
                response = requests.put(url, json=data)
            elif method == "PATCH":
                response = requests.patch(url, json=data)
            elif method == "DELETE":
                response = requests.delete(url)
            
            # Check for successful response
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
            if attempt == retries - 1:
                raise
            time.sleep(1)  # Wait before retry

# Usage
try:
    character = safe_api_call("http://localhost:8000/characters/123")
    print(f"Character loaded: {character['character']['main']['name']}")
except Exception as e:
    print(f"Failed to load character: {e}")
```

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second=10):
    """Decorator to limit API call rate"""
    min_interval = 1.0 / calls_per_second
    last_call_time = 0
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            elapsed = time.time() - last_call_time
            
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            
            last_call_time = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limit(calls_per_second=5)
def api_call(url):
    """Rate-limited API call"""
    return requests.get(url).json()

# Usage
for i in range(20):
    result = api_call("http://localhost:8000/characters")
    print(f"Call {i+1}: {len(result)} characters")
```

### Data Validation

```python
from pydantic import BaseModel, ValidationError

class CharacterValidator(BaseModel):
    name: str
    level: int
    souls: int
    
    class Config:
        extra = "forbid"

def validate_character_data(data):
    """Validate character data before sending to API"""
    try:
        validator = CharacterValidator(**data)
        return True, validator.dict()
    except ValidationError as e:
        return False, e.errors()

# Usage
character_data = {
    "name": "Arthur",
    "level": 1,
    "souls": 0,
    "invalid_field": "should be ignored"
}

is_valid, result = validate_character_data(character_data)
if is_valid:
    # Send to API
    response = requests.post("http://localhost:8000/characters", json={"character": result})
else:
    print(f"Validation errors: {result}")
```

## Common Use Cases

### 1. Character Creation Wizard

```python
def create_character_wizard():
    """Interactive character creation"""
    print("=== Character Creation ===")
    
    name = input("Enter character name: ")
    level = int(input("Enter starting level (1-100): "))
    
    # Validate inputs
    if not (1 <= level <= 100):
        print("Level must be between 1 and 100")
        return
    
    # Create base stats based on level
    base_stats = 10 + (level // 10)
    
    character_data = {
        "character": {
            "main": {"name": name, "level": level, "souls": 0},
            "stats": {
                "STR": {"value": base_stats, "modifier": 0},
                "DEX": {"value": base_stats, "modifier": 0},
                "FTH": {"value": base_stats, "modifier": 0},
                "INT": {"value": base_stats, "modifier": 0}
            },
            "resources": {
                "HP": {"current": 100 + (level * 5), "maximum": 100 + (level * 5)},
                "AP": {"current": 50 + (level * 2), "maximum": 50 + (level * 2)}
            }
        }
    }
    
    # Create character via API
    response = requests.post("http://localhost:8000/characters", json=character_data)
    
    if response.status_code == 201:
        character = response.json()
        print(f"Character created successfully! ID: {character['id']}")
    else:
        print(f"Error creating character: {response.json()}")

# Run wizard
# create_character_wizard()
```

### 2. Combat Simulator

```python
import random

def simulate_combat():
    """Simulate a combat between two characters"""
    
    # Setup participants
    participants = [
        {
            "characterSheetId": "player",
            "isPlayer": True,
            "initiative": random.randint(10, 20),
            "currentHP": 100,
            "maxHP": 100
        },
        {
            "characterSheetId": "enemy",
            "isPlayer": False,
            "initiative": random.randint(8, 18),
            "currentHP": 80,
            "maxHP": 80
        }
    ]
    
    # Start combat
    response = requests.post("http://localhost:8000/combat/start", json=participants)
    print("Combat started!")
    
    # Combat loop
    round_num = 1
    while True:
        try:
            # Get current turn
            turn_response = requests.get("http://localhost:8000/combat/turn")
            turn_data = turn_response.json()
            
            current_participant = turn_data["current_participant_id"]
            
            # Determine action
            if current_participant == "player":
                action_type = random.choice(["Attack", "Dodge"])
                target = "enemy"
            else:
                action_type = "Attack"
                target = "player"
            
            # Perform action
            action_data = {
                "actorId": current_participant,
                "actionType": action_type,
                "targetId": target
            }
            
            action_response = requests.post("http://localhost:8000/combat/action", json=action_data)
            result = action_response.json()
            
            print(f"Round {round_num} - {current_participant} uses {action_type}")
            if "damage" in result:
                print(f"  Damage dealt: {result['damage']}")
            
            # End turn
            requests.post("http://localhost:8000/combat/end-turn")
            
            # Check if combat should end
            status_response = requests.get("http://localhost:8000/combat/status")
            status = status_response.json()
            
            if not status["is_active"]:
                print("Combat ended!")
                break
            
            round_num += 1
            time.sleep(1)  # Pause between turns
            
        except Exception as e:
            print(f"Combat ended: {e}")
            break

# Run simulation
# simulate_combat()
```

### 3. Character Progression Tracker

```python
import json
import os
from datetime import datetime

class ProgressionTracker:
    def __init__(self, save_file="progression_log.json"):
        self.save_file = save_file
        self.log = self.load_log()
    
    def load_log(self):
        """Load progression log from file"""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_log(self):
        """Save progression log to file"""
        with open(self.save_file, 'w') as f:
            json.dump(self.log, f, indent=2)
    
    def log_event(self, character_id, event_type, details):
        """Log a progression event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "character_id": character_id,
            "event_type": event_type,
            "details": details
        }
        
        self.log.append(event)
        self.save_log()
    
    def get_character_progression(self, character_id):
        """Get progression history for a character"""
        return [event for event in self.log if event["character_id"] == character_id]
    
    def print_progression_report(self, character_id):
        """Print a progression report"""
        events = self.get_character_progression(character_id)
        
        print(f"=== Progression Report for {character_id} ===")
        for event in events:
            print(f"{event['timestamp']} - {event['event_type']}: {event['details']}")

# Usage example
tracker = ProgressionTracker()

# Log events during gameplay
tracker.log_event("player-1", "level_up", "Level 1 → Level 2")
tracker.log_event("player-1", "soul_gain", "+1000 souls")
tracker.log_event("player-1", "item_acquired", "Long Sword")

# Print report
tracker.print_progression_report("player-1")
```

These examples demonstrate various ways to interact with the Dark Souls API, from basic CRUD operations to complex game systems. Adapt these examples to fit your specific use case and requirements.
