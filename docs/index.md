# Dark Souls API Documentation

Welcome to the comprehensive documentation for the Dark Souls API! This RESTful API provides complete character management and turn-based combat system functionality for Dark Souls-style role-playing games.

## 📖 Table of Contents

- [Quick Start](#quick-start)
- [API Reference](api-reference.md)
- [Architecture](architecture.md)
- [Data Models](models.md)
- [Services](services.md)
- [Usage Examples](usage-examples.md)
- [Deployment](deployment.md)
- [Troubleshooting](troubleshooting.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd darksouls_api
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start the server**:
```bash
# Option 1: Using the main.py entry point (recommended)
python main.py

# Option 2: Direct uvicorn command
python -m uvicorn src.api.main:app --reload

# Option 3: Using uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API**:
   - Base URL: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`

### Basic Usage

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
       }
     }'
```

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

## 🏗️ Architecture Overview

The Dark Souls API follows a clean architecture pattern with the following layers:

```
┌─────────────────────────────────────────┐
│              API Layer                  │  ← FastAPI routes and HTTP handling
├─────────────────────────────────────────┤
│            Service Layer                │  ← Business logic and orchestration
├─────────────────────────────────────────┤
│             Model Layer                 │  ← Pydantic models and validation
├─────────────────────────────────────────┤
│           Database Layer                │  ← Data persistence and storage
└─────────────────────────────────────────┘
```

**Key Features**:
- ✅ Full CRUD operations for characters
- ✅ Turn-based combat system
- ✅ Inventory and equipment management
- ✅ Status effects and combat actions
- ✅ RESTful API design
- ✅ Comprehensive error handling
- ✅ Data validation with Pydantic

## 📊 API Endpoints

### Characters
- `GET /characters` - Get all characters
- `GET /characters/ids` - List character IDs
- `GET /characters/{id}` - Get specific character
- `POST /characters` - Create new character
- `PUT /characters/{id}` - Update entire character
- `PATCH /characters/{id}` - Partial character updates
- `PATCH /characters/{id}/equip` - Equip items
- `DELETE /characters/{id}` - Delete character

### Combat System
- `GET /combat/status` - Get combat status
- `POST /combat/start` - Start combat
- `POST /combat/end` - End combat
- `GET /combat/turn` - Get current turn
- `POST /combat/end-turn` - End current turn
- `POST /combat/action` - Perform combat actions
- `POST /combat/effect` - Apply effects
- `POST /combat/effects/update` - Update effects

### Health Check
- `GET /health` - API health status

## 🔧 Development

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_character_service.py
```

### Code Quality
```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. **Models**: Add new Pydantic models in `src/models/`
2. **Services**: Implement business logic in `src/services/`
3. **Routes**: Add endpoints in `src/api/routes/`
4. **Tests**: Write tests in `tests/`

## 🤝 Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [API Reference](api-reference.md)
3. Look at [Usage Examples](usage-examples.md)
4. Check existing [Issues](https://github.com/your-repo/issues)
5. Create a new issue with detailed information

## 📞 Contact

For questions or support, please reach out through:
- GitHub Issues
- Project documentation
- Community forums

---

**Happy coding and may the gods guide your journey!** ⚔️
