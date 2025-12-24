# Dark Souls API

A FastAPI-based REST API for managing Dark Souls character data with full CRUD operations including the new PATCH method for partial updates.

## 🏗️ Architecture

This project follows a clean architecture pattern with the following structure:

```
darksouls_api/
├── src/
│   ├── api/              # FastAPI application and routes
│   ├── core/             # Core functionality (config, exceptions, logging)
│   ├── models/           # Pydantic models and schemas
│   ├── services/         # Business logic layer
│   ├── database/         # Data access layer (repository pattern)
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── docs/                 # Documentation
```

## 🚀 Features

- ✅ **GET** `/characters` - Retrieve all characters
- ✅ **GET** `/characters/ids` - List all character IDs
- ✅ **GET** `/characters/{id}` - Get specific character details
- ✅ **POST** `/characters` - Create new character
- ✅ **PUT** `/characters/{id}` - Update entire character
- ✅ **PATCH** `/characters/{id}` - **Partial character updates** (NEW!)
- ✅ **DELETE** `/characters/{id}` - Delete character
- ✅ **GET** `/health` - Health check endpoint

### Combat System

- ✅ **Combat Management**: Turn-based combat system
- ✅ **Participant Management**: Add/remove participants
- ✅ **Effect System**: Apply/remove effects with duration
- ✅ **Action System**: Attack, Cast, Dodge, Parry, Search
- ✅ **Turn Management**: Automatic turn progression

## 📦 Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd darksouls_api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python -m uvicorn src.api.main:app --reload
```

4. Visit `/docs` for interactive API documentation.

## 🎮 Usage

### Character Management

#### Create a Character
```bash
curl -X POST "http://localhost:8000/characters" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

#### Partial Updates (PATCH)
```bash
curl -X PATCH "http://localhost:8000/characters/1" \
     -H "Content-Type: application/json" \
     -d '{
       "character": {
         "souls": 15000
       }
     }'
```

#### Equip Items
```bash
curl -X PATCH "http://localhost:8000/characters/1/equip" \
     -H "Content-Type: application/json" \
     -d '{
       "item_name": "Long Sword",
       "slot": "right_hand"
     }'
```

### Combat System

#### Start Combat
```bash
curl -X POST "http://localhost:8000/combat/start" \
     -H "Content-Type: application/json" \
     -d '[
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
     ]'
```

#### Perform Actions
```bash
curl -X POST "http://localhost:8000/combat/action" \
     -H "Content-Type: application/json" \
     -d '{
       "actorId": "player-1",
       "actionType": "Attack",
       "targetId": "enemy-1"
     }'
```

## 📊 Data Structure

### Character Data
Each character contains:
- **Character**: Name, level, hollowing, souls, stats, resources
- **Equipment**: Main hand weapon, off-hand shield, armor
- **Inventory**: List of items
- **Spells**: List of spells with effects

### Combat State
- **Turn Order**: Participants sorted by initiative
- **Current Turn**: Active participant and round
- **Effects**: Active effects with duration tracking
- **Participants**: Complete participant information

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Development

### Code Quality
This project uses several tools for maintaining code quality:

- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

Run all quality checks:
```bash
black src/ tests/
ruff check src/ tests/
mypy src/
pytest tests/
```

### Adding New Features

1. **Models**: Add new Pydantic models in `src/models/`
2. **Services**: Implement business logic in `src/services/`
3. **Routes**: Add endpoints in `src/api/routes/`
4. **Tests**: Write tests in `tests/`

## 📚 Documentation

- **API Documentation**: Available at `/docs` when server is running
- **Architecture**: See `docs/architecture.md`
- **API Reference**: See `docs/api.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pydantic for data validation
- The Dark Souls community for inspiration
