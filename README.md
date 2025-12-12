# Dark Souls API

A FastAPI-based REST API for managing Dark Souls character data with full CRUD operations including the new PATCH method for partial updates.

## Features

- ✅ **GET** `/characters` - Retrieve all characters
- ✅ **GET** `/characters/ids` - List all character IDs
- ✅ **GET** `/characters/{id}` - Get specific character details
- ✅ **POST** `/characters` - Create new character
- ✅ **PUT** `/characters/{id}` - Update entire character
- ✅ **PATCH** `/characters/{id}` - **Partial character updates** (NEW!)
- ✅ **DELETE** `/characters/{id}` - Delete character
- ✅ **GET** `/health` - Health check endpoint

## Character Data Structure

Each character contains:
- **Character**: Name, level, hollowing, souls, stats, resources
- **Equipment**: Main hand weapon, off-hand shield, armor
- **Inventory**: List of items
- **Spells**: List of spells with effects

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd darksouls_api
```

2. Install dependencies:
```bash
pip install fastapi uvicorn
```

3. Run the server:
```bash
python -m uvicorn main:app --reload
```

4. Visit `/docs` for interactive API documentation.

## API Usage

### PATCH Method (New Feature)

The PATCH endpoint allows partial updates to character data. Only the fields you provide will be updated:

```bash
curl -X PATCH "http://localhost:8000/characters/1" \
     -H "Content-Type: application/json" \
     -d '{
       "character": {
         "souls": 15000
       }
     }'
```

### Example Response

```json
{
  "id": 1,
  "character": {
    "name": "SAAL D'ASTORA",
    "level": 0,
    "hollowing": 0,
    "souls": 15000,
    "stats": {
      "vitality": {"value": 10, "modifier": -1}
    },
    "resources": [...]
  },
  "equipment": {...},
  "inventory": [...],
  "spells": [...]
}
```

## Debugging

The PATCH endpoint includes debug logging (🔥 print statements) to help identify data format issues. When you make a PATCH request, check the console output for detailed information about what data was received.

## Database

Characters are stored in `characters.json` as JSON data. The API automatically handles file operations and data validation.

## License

This project is part of the owbear-sunitro-api collection.
