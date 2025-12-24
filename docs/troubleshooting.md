# Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues with the Dark Souls API. It covers error scenarios, debugging techniques, and solutions for various problems.

## Common Issues and Solutions

### 1. Server Won't Start

#### Problem: Module Import Error
```bash
# Error message
ERROR:    Error loading ASGI app. Could not import module "main".
```

**Solution**:
```bash
# Option 1: Use the main.py entry point (recommended)
python main.py

# Option 2: Use full module path
python -m uvicorn src.api.main:app --reload

# Option 3: Use uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Problem: Port Already in Use
```bash
# Error message
OSError: [Errno 98] Address already in use
```

**Solution**:
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
uvicorn src.api.main:app --port 8001
```

#### Problem: Import Errors
```bash
# Error message
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; print(fastapi.__version__)"
```

#### Problem: Permission Denied
```bash
# Error message
PermissionError: [Errno 13] Permission denied
```

**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER /path/to/darksouls_api
sudo chmod -R 755 /path/to/darksouls_api

# Or run with sudo (not recommended for development)
sudo uvicorn src.api.main:app --reload
```

### 2. API Endpoints Not Working

#### Problem: 404 Not Found
```bash
# Error when accessing http://localhost:8000/characters
{"detail":"Not Found"}
```

**Solution**:
```bash
# Check if the server is running
curl http://localhost:8000/

# Verify the endpoint exists
curl http://localhost:8000/docs

# Check server logs for errors
uvicorn src.api.main:app --reload --log-level debug
```

#### Problem: 500 Internal Server Error
```bash
# Error in response
{"detail":"Internal Server Error"}
```

**Solution**:
```bash
# Enable debug mode to see detailed errors
export DEBUG=true
uvicorn src.api.main:app --reload --log-level debug

# Check server logs for stack traces
# Look for specific error messages and fix accordingly
```

### 3. Database Issues

#### Problem: Characters Not Persisting
```bash
# Characters disappear after server restart
```

**Solution**:
```python
# Check storage path configuration
# Ensure data directory exists and is writable
import os
os.makedirs('./data', exist_ok=True)

# Verify file permissions
ls -la ./data/
```

#### Problem: JSON Decode Error
```bash
# Error message
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution**:
```python
# Check if data files are corrupted
# Backup and recreate data directory
import shutil
shutil.rmtree('./data')
os.makedirs('./data')
```

#### Problem: Character Validation Errors
```bash
# Error when creating character
{"detail":[{"loc":["body","character","main","level"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
```

**Solution**:
```python
# Ensure all required fields are provided
# Check data types match expected types
character_data = {
    "character": {
        "main": {
            "name": "Arthur",
            "level": 1,  # Must be integer, not string
            "souls": 0   # Must be integer
        },
        "stats": {
            "STR": {"value": 10, "modifier": 0},  # Both must be integers
            "DEX": {"value": 10, "modifier": 0}
        },
        "resources": {
            "HP": {"current": 100, "maximum": 100},  # Both must be integers
            "AP": {"current": 50, "maximum": 50}
        }
    }
}
```

### 4. Combat System Issues

#### Problem: Combat Not Starting
```bash
# Error when starting combat
{"detail":"Combat already in progress"}
```

**Solution**:
```python
# End current combat first
response = requests.post("http://localhost:8000/combat/end")

# Or check if combat is active
response = requests.get("http://localhost:8000/combat/status")
```

#### Problem: Invalid Participant ID
```bash
# Error when adding participant
{"detail":"Participant player-1 non trouvé dans le combat"}
```

**Solution**:
```python
# Ensure participant exists in combat
# Check participant IDs match exactly
participants = [
    {"characterSheetId": "player-1", "isPlayer": True, "initiative": 18},
    {"characterSheetId": "enemy-1", "isPlayer": False, "initiative": 12}
]
```

#### Problem: Turn Order Issues
```bash
# Participants not in correct order
```

**Solution**:
```python
# Verify initiative values are correct
# Higher initiative = earlier turn
# Check for duplicate initiative values
```

### 5. Inventory and Equipment Issues

#### Problem: Item Not Found
```bash
# Error when equipping item
{"detail":"Impossible d'équiper l'item Long Sword sur le slot right_hand"}
```

**Solution**:
```python
# Check if item exists in inventory
# Verify item name matches exactly
# Ensure item is not already equipped
```

#### Problem: Invalid Slot
```bash
# Error with equipment slot
{"detail":"Invalid enum value"}
```

**Solution**:
```python
# Use valid slot names
valid_slots = ["armor", "right_hand", "left_hand", "consumable", "bag", "spell_1", "spell_2", "spell_3", "spell_4"]

equip_data = {
    "item_name": "Long Sword",
    "slot": "right_hand"  # Must be one of valid_slots
}
```

## Debugging Techniques

### 1. Enable Debug Logging

```python
# In src/api/main.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or use environment variable
export LOG_LEVEL=debug
```

### 2. Use FastAPI's Built-in Debug Mode

```python
# In main.py
app = FastAPI(debug=True)

# Or set environment variable
export DEBUG=true
```

### 3. Check Request/Response Details

```python
# Add middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### 4. Validate Data Manually

```python
# Test data validation
from src.models.character import CharacterCreate

try:
    character = CharacterCreate(**character_data)
    print("Data is valid")
except ValidationError as e:
    print(f"Validation errors: {e.errors()}")
```

### 5. Check Database State

```python
# Inspect stored data
from src.database.repository import character_repository

# Get all characters
characters = character_repository.get_all_characters()
print(f"Found {len(characters)} characters")

# Check specific character
character = character_repository.get_character("uuid-123")
if character:
    print(f"Character found: {character.character['main']['name']}")
else:
    print("Character not found")
```

## Performance Issues

### 1. Slow Response Times

**Causes and Solutions**:
```python
# Large data files
# Solution: Implement pagination or filtering

@app.get("/characters")
async def get_characters(skip: int = 0, limit: int = 10):
    all_chars = character_service.get_all_characters()
    return list(all_chars.values())[skip:skip+limit]

# Inefficient queries
# Solution: Optimize data access patterns

# Memory issues
# Solution: Use streaming or chunking for large datasets
```

### 2. High Memory Usage

**Causes and Solutions**:
```python
# Loading all data into memory
# Solution: Implement lazy loading

# Large character objects
# Solution: Use dataclasses or optimize data structures

# Memory leaks
# Solution: Monitor memory usage and fix leaks
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")
```

### 3. High CPU Usage

**Causes and Solutions**:
```python
# Complex calculations in request handlers
# Solution: Move heavy computation to background tasks

# Inefficient algorithms
# Solution: Optimize algorithms and data structures

# Too many concurrent requests
# Solution: Implement rate limiting and queuing
```

## Network Issues

### 1. CORS Errors

```javascript
// Frontend error
Access to fetch at 'http://localhost:8000/characters' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**:
```python
# In src/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Connection Timeouts

```bash
# Error message
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded
```

**Solution**:
```python
# Check if server is running
curl http://localhost:8000/health

# Increase timeout
response = requests.get("http://localhost:8000/characters", timeout=10)

# Check network connectivity
netstat -an | grep 8000
```

### 3. SSL/TLS Issues

```bash
# HTTPS errors
requests.exceptions.SSLError: HTTPSConnectionPool(host='yourdomain.com', port=443)
```

**Solution**:
```python
# For development (not recommended for production)
response = requests.get("https://yourdomain.com/characters", verify=False)

# Proper SSL configuration
# Ensure SSL certificates are valid and properly configured
```

## Production Issues

### 1. Environment Variables Not Loading

```bash
# Error: Environment variable not found
```

**Solution**:
```bash
# Check if .env file exists
ls -la .env

# Verify environment variables are set
echo $ENVIRONMENT

# Load .env file manually
source .env
```

### 2. File Permissions in Production

```bash
# Error: Permission denied
```

**Solution**:
```bash
# Set proper ownership
sudo chown -R www-data:www-data /path/to/darksouls_api

# Set proper permissions
sudo chmod -R 755 /path/to/darksouls_api
sudo chmod -R 644 /path/to/darksouls_api/data
```

### 3. Database Lock Issues

```bash
# Error: Database is locked
```

**Solution**:
```python
# Implement proper file locking
import fcntl

# Use atomic operations
# Consider switching to a proper database system
```

## Testing Issues

### 1. Tests Failing

```bash
# Pytest errors
ERROR: file or directory not found: tests/
```

**Solution**:
```bash
# Ensure tests directory exists
ls -la tests/

# Run specific test
pytest tests/unit/test_character_service.py

# Run with verbose output
pytest -v
```

### 2. Test Data Conflicts

```bash
# Tests interfering with each other
```

**Solution**:
```python
# Use test fixtures
@pytest.fixture
def test_character():
    return CharacterCreate(...)

# Use temporary directories
import tempfile
with tempfile.TemporaryDirectory() as temp_dir:
    # Test with temporary data
```

### 3. Mocking Issues

```python
# Mock not working properly
```

**Solution**:
```python
# Proper mocking
from unittest.mock import Mock, patch

@patch('src.services.character_service.character_repository')
def test_create_character(mock_repo):
    mock_repo.create_character.return_value = "test-id"
    # Test logic
```

## Getting Help

### 1. Check Logs

```bash
# Application logs
tail -f /var/log/darksouls-api.log

# System logs
journalctl -u darksouls-api -f

# Docker logs
docker logs <container-id>
```

### 2. Use Debug Tools

```python
# Add breakpoints
import pdb; pdb.set_trace()

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")

# Use profiling
import cProfile
cProfile.run('your_function()')
```

### 3. Community Support

- Check FastAPI documentation: https://fastapi.tiangolo.com/
- Python debugging: https://docs.python.org/3/library/pdb.html
- Pydantic validation: https://pydantic-docs.helpmanual.io/

### 4. Common Debugging Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check environment variables
printenv

# Check file permissions
ls -la

# Check network connections
netstat -an

# Check system resources
top
htop
df -h
```

Remember: Always test fixes in a development environment before applying them to production systems.
