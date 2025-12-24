# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for this API.

## Response Format

All responses are in JSON format with the following structure:

```json
{
  "message": "Success message",
  "data": { /* response data */ },
  "error": "Error message (if applicable)"
}
```

## HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

---

## Characters

### Get All Characters

**GET** `/characters`

Retrieve all characters in the database.

**Response:**
```json
{
  "characters": {
    "uuid-1": {
      "id": "uuid-1",
      "character": {
        "main": {
          "name": "Arthur",
          "level": 1,
          "souls": 0
        },
        "stats": {
          "STR": {"value": 10, "modifier": 0},
          "DEX": {"value": 10, "modifier": 0}
        },
        "resources": {
          "HP": {"current": 100, "maximum": 100},
          "AP": {"current": 50, "maximum": 50}
        }
      },
      "inventory": {
        "weapons": [],
        "armors": [],
        "catalysts": [],
        "items": [],
        "spells": []
      }
    }
  }
}
```

### Get Character IDs

**GET** `/characters/ids`

Get a list of all character IDs.

**Response:**
```json
{
  "character_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

### Get Character by ID

**GET** `/characters/{id}`

Retrieve a specific character by their ID.

**Path Parameters:**
- `id` (string, required): The character's UUID

**Response:**
```json
{
  "id": "uuid-1",
  "character": { /* character data */ },
  "inventory": { /* inventory data */ }
}
```

**Error Responses:**
- `404 Not Found`: Character not found

### Create Character

**POST** `/characters`

Create a new character.

**Request Body:**
```json
{
  "character": {
    "main": {
      "name": "Arthur",
      "level": 1,
      "souls": 0
    },
    "stats": {
      "STR": {"value": 10, "modifier": 0},
      "DEX": {"value": 10, "modifier": 0}
    },
    "resources": {
      "HP": {"current": 100, "maximum": 100},
      "AP": {"current": 50, "maximum": 50}
    }
  }
}
```

**Response:**
```json
{
  "id": "new-uuid",
  "character": { /* created character data */ },
  "inventory": { /* empty inventory */ }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid character data

### Update Character (Full)

**PUT** `/characters/{id}`

Replace the entire character data.

**Path Parameters:**
- `id` (string, required): The character's UUID

**Request Body:**
```json
{
  "character": {
    "main": {
      "name": "Arthur Updated",
      "level": 2,
      "souls": 1000
    },
    "stats": {
      "STR": {"value": 12, "modifier": 0},
      "DEX": {"value": 11, "modifier": 0}
    },
    "resources": {
      "HP": {"current": 120, "maximum": 120},
      "AP": {"current": 55, "maximum": 55}
    }
  }
}
```

**Response:**
```json
{
  "id": "uuid-1",
  "character": { /* updated character data */ },
  "inventory": { /* inventory data */ }
}
```

**Error Responses:**
- `404 Not Found`: Character not found
- `400 Bad Request`: Invalid character data

### Update Character (Partial)

**PATCH** `/characters/{id}`

Update specific fields of a character.

**Path Parameters:**
- `id` (string, required): The character's UUID

**Request Body:**
```json
{
  "character": {
    "souls": 15000,
    "stats": {
      "STR": {"value": 15}
    }
  }
}
```

**Response:**
```json
{
  "id": "uuid-1",
  "character": { /* character with updated fields */ },
  "inventory": { /* inventory data */ }
}
```

**Error Responses:**
- `404 Not Found`: Character not found
- `400 Bad Request`: Invalid update data

### Equip Item

**PATCH** `/characters/{id}/equip`

Equip an item on a specific slot.

**Path Parameters:**
- `id` (string, required): The character's UUID

**Request Body:**
```json
{
  "item_name": "Long Sword",
  "slot": "right_hand"
}
```

**Slot Options:**
- `armor`: Armor slot
- `right_hand`: Right hand weapon slot
- `left_hand`: Left hand shield/off-hand slot
- `consumable`: Consumable item slot
- `bag`: Bag/inventory slot
- `spell_1` to `spell_4`: Spell slots

**Response:**
```json
{
  "id": "uuid-1",
  "character": { /* character data */ },
  "inventory": { /* updated inventory with equipped item */ }
}
```

**Error Responses:**
- `404 Not Found`: Character not found
- `400 Bad Request`: Item not found or invalid slot

### Delete Character

**DELETE** `/characters/{id}`

Delete a character by ID.

**Path Parameters:**
- `id` (string, required): The character's UUID

**Response:**
```json
{
  "message": "Personnage avec l'ID uuid-1 supprimé avec succès"
}
```

**Error Responses:**
- `404 Not Found`: Character not found

---

## Combat System

### Get Combat Status

**GET** `/combat/status`

Get the current combat state.

**Response:**
```json
{
  "combat_id": "combat-uuid",
  "is_active": true,
  "current_round": 2,
  "current_turn_index": 1,
  "turn_order": ["player-1", "enemy-1", "player-2"],
  "participants_count": 3,
  "participants": {
    "player-1": {
      "characterSheetId": "player-1",
      "isPlayer": true,
      "initiative": 18,
      "currentHP": 100,
      "maxHP": 100,
      "activeEffects": []
    }
  },
  "created_at": "2023-12-22T10:00:00",
  "updated_at": "2023-12-22T10:15:00"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress

### Start Combat

**POST** `/combat/start`

Initialize a new combat session.

**Request Body:**
```json
[
  {
    "characterSheetId": "player-1",
    "isPlayer": true,
    "initiative": 18
  },
  {
    "characterSheetId": "enemy-1",
    "isPlayer": false,
    "initiative": 12
  }
]
```

**Response:**
```json
{
  "message": "Combat démarré avec succès",
  "combat_id": "combat-uuid"
}
```

**Error Responses:**
- `409 Conflict`: Combat already in progress
- `400 Bad Request`: Invalid participant data

### End Combat

**POST** `/combat/end`

End the current combat session.

**Response:**
```json
{
  "message": "Combat terminé avec succès"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress

### Get Current Turn

**GET** `/combat/turn`

Get information about the current turn.

**Response:**
```json
{
  "current_round": 2,
  "current_turn_index": 1,
  "current_participant_id": "player-1",
  "current_participant": {
    "characterSheetId": "player-1",
    "isPlayer": true,
    "initiative": 18,
    "currentHP": 100,
    "maxHP": 100,
    "activeEffects": []
  },
  "turn_order": ["player-1", "enemy-1", "player-2"]
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress

### End Current Turn

**POST** `/combat/end-turn`

End the current participant's turn and move to the next.

**Response:**
```json
{
  "message": "Tour terminé, passage au participant suivant",
  "next_participant_id": "enemy-1",
  "current_round": 2
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress
- `500 Internal Server Error`: Error ending turn

### Add Participant

**POST** `/combat/participant`

Add a participant to the current combat.

**Request Body:**
```json
{
  "characterSheetId": "player-3",
  "isPlayer": true,
  "initiative": 15
}
```

**Response:**
```json
{
  "message": "Participant player-3 ajouté au combat"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress
- `400 Bad Request`: Invalid participant data

### Remove Participant

**DELETE** `/combat/participant/{participant_id}`

Remove a participant from the current combat.

**Path Parameters:**
- `participant_id` (string, required): The participant's ID

**Response:**
```json
{
  "message": "Participant player-3 supprimé du combat"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress or participant not found

### Get Participant Info

**GET** `/combat/participant/{participant_id}`

Get detailed information about a specific participant.

**Path Parameters:**
- `participant_id` (string, required): The participant's ID

**Response:**
```json
{
  "characterSheetId": "player-1",
  "isPlayer": true,
  "initiative": 18,
  "currentHP": 100,
  "maxHP": 100,
  "activeEffects": [
    {
      "name": "Poison",
      "type": "damage",
      "value": 5,
      "duration": 3,
      "duration_type": "round",
      "description": "Poison damage over time"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress or participant not found

### Apply Effect

**POST** `/combat/effect`

Apply an effect to a participant.

**Request Body:**
```json
{
  "participant_id": "player-1",
  "effect": {
    "name": "Blessing",
    "type": "buff",
    "value": 5,
    "duration": 2,
    "duration_type": "round",
    "description": "Attack bonus"
  }
}
```

**Response:**
```json
{
  "message": "Effet Blessing appliqué au participant player-1"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress or participant not found

### Remove Effect

**DELETE** `/combat/effect/{participant_id}/{effect_name}`

Remove an effect from a participant.

**Path Parameters:**
- `participant_id` (string, required): The participant's ID
- `effect_name` (string, required): The effect name

**Response:**
```json
{
  "message": "Effet Blessing supprimé du participant player-1"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress, participant not found, or effect not found

### Update Effects

**POST** `/combat/effects/update`

Update all active effects and return expired ones.

**Response:**
```json
{
  "message": "2 effets ont expiré",
  "expired_effects": [
    {
      "participant_id": "player-1",
      "effect_name": "Poison"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress

### Perform Action

**POST** `/combat/action`

Execute an action in combat.

**Request Body:**
```json
{
  "actorId": "player-1",
  "actionType": "Attack",
  "targetId": "enemy-1",
  "spellName": "Fireball"
}
```

**Action Types:**
- `Attack`: Physical attack
- `Cast`: Cast a spell
- `Dodge`: Dodge action
- `Parry`: Parry action
- `Search`: Search action

**Response:**
```json
{
  "success": true,
  "action": "Attack",
  "actor": "player-1",
  "target": "enemy-1",
  "damage": 25,
  "roll": 15,
  "message": "Attaque réussie contre enemy-1"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress
- `400 Bad Request`: Invalid action or not current participant's turn

### Delay Turn

**POST** `/combat/delay`

Delay a participant's turn to the end of the round.

**Request Body:**
```json
{
  "actorId": "player-1"
}
```

**Response:**
```json
{
  "success": true,
  "actor": "player-1",
  "message": "Tour de player-1 retardé (jouera en dernier ce round)"
}
```

**Error Responses:**
- `404 Not Found`: No combat in progress
- `400 Bad Request`: Participant not found

---

## Health Check

### Health Status

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-22T10:00:00Z",
  "version": "2.0.0"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error description"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., combat already in progress)
- `500 Internal Server Error`: Server error

### Validation Errors

When data validation fails, FastAPI returns detailed error information:

```json
{
  "detail": [
    {
      "loc": ["body", "character", "main", "name"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## Rate Limiting

No rate limiting is currently implemented. Consider adding rate limiting in production environments.

## CORS

CORS is enabled with default settings. Configure CORS settings in `src/api/main.py` for production use.
