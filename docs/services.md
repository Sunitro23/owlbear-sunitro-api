# Services Documentation

## Overview

This document describes the service layer of the Dark Souls API, which contains the business logic and orchestrates operations between different layers of the application.

## Service Architecture

The service layer follows a clean architecture pattern where services encapsulate business logic and coordinate between the API layer and data access layer. Each service is responsible for a specific domain area.

## Character Service

### CharacterService

The `CharacterService` class handles all character-related business operations.

**Location**: `src/services/character_service.py`

**Dependencies**:
- `CharacterRepository`: For data persistence operations

**Key Methods**:

#### get_all_characters()
```python
def get_all_characters(self) -> Dict[str, CharacterData]:
    """Get all characters"""
```
- **Purpose**: Retrieves all characters from storage
- **Returns**: Dictionary mapping character IDs to CharacterData objects
- **Error Handling**: None (returns empty dict if no characters exist)

#### get_character_ids()
```python
def get_character_ids(self) -> List[str]:
    """Get list of all character IDs"""
```
- **Purpose**: Returns a list of all character UUIDs
- **Returns**: List of character ID strings
- **Use Case**: Useful for API endpoints that need to list available characters

#### get_character(character_id: str)
```python
def get_character(self, character_id: str) -> CharacterResponse:
    """Get a character by ID with full response"""
```
- **Purpose**: Retrieves a specific character by ID
- **Parameters**: `character_id` (str) - The UUID of the character
- **Returns**: CharacterResponse object with full character data
- **Error Handling**: Raises HTTPException with 404 status if character not found

#### create_character(character: CharacterCreate)
```python
def create_character(self, character: CharacterCreate) -> CharacterResponse:
    """Create a new character"""
```
- **Purpose**: Creates a new character in the system
- **Parameters**: `character` (CharacterCreate) - Character data to create
- **Returns**: CharacterResponse with the created character data
- **Process**:
  1. Generates a new UUID for the character
  2. Persists the character data
  3. Returns the created character with its new ID

#### update_character(character_id: str, character_update: CharacterUpdate)
```python
def update_character(self, character_id: str, character_update: CharacterUpdate) -> CharacterResponse:
    """Update an existing character"""
```
- **Purpose**: Updates an existing character with partial data
- **Parameters**:
  - `character_id` (str) - The UUID of the character to update
  - `character_update` (CharacterUpdate) - Partial character data
- **Returns**: CharacterResponse with updated character data
- **Error Handling**: Raises HTTPException with 404 status if character not found
- **Validation**: Only updates fields that are provided (partial update)

#### delete_character(character_id: str)
```python
def delete_character(self, character_id: str) -> Dict[str, str]:
    """Delete a character"""
```
- **Purpose**: Removes a character from the system
- **Parameters**: `character_id` (str) - The UUID of the character to delete
- **Returns**: Success message dictionary
- **Error Handling**: Raises HTTPException with 404 status if character not found

#### equip_item(character_id: str, equip_request: EquipRequest)
```python
def equip_item(self, character_id: str, equip_request: EquipRequest) -> CharacterResponse:
    """Equip an item on a specific slot for a character"""
```
- **Purpose**: Equips an item in a specific equipment slot
- **Parameters**:
  - `character_id` (str) - The UUID of the character
  - `equip_request` (EquipRequest) - Item name and target slot
- **Returns**: CharacterResponse with updated character data
- **Process**:
  1. Finds the item in the character's inventory
  2. Unequips any item currently in the target slot
  3. Equips the new item in the target slot
  4. Validates the inventory state
- **Error Handling**:
  - Raises HTTPException with 404 if character not found
  - Raises HTTPException with 400 if item not found or slot invalid

### Service Usage Example

```python
from src.services.character_service import character_service

# Create a new character
character_data = CharacterCreate(...)
created_character = character_service.create_character(character_data)

# Update a character
update_data = CharacterUpdate(character={"souls": 15000})
updated_character = character_service.update_character("uuid-123", update_data)

# Equip an item
equip_data = EquipRequest(item_name="Long Sword", slot="right_hand")
equipped_character = character_service.equip_item("uuid-123", equip_data)
```

## Combat Service

### CombatService

The `CombatService` class manages all combat-related operations and business logic.

**Location**: `src/services/combat_service.py`

**Dependencies**:
- `CombatManager`: Core combat engine from combat_system module

**Key Methods**:

#### get_combat_status()
```python
def get_combat_status(self) -> Dict[str, Any]:
    """Get current combat status"""
```
- **Purpose**: Returns the current state of any active combat
- **Returns**: Dictionary with combat state information
- **Error Handling**: Returns message if no combat is active

#### start_combat(participants: List[CombatParticipant])
```python
def start_combat(self, participants: List[CombatParticipant]) -> Dict[str, str]:
    """Start a new combat"""
```
- **Purpose**: Initializes a new combat session
- **Parameters**: `participants` (List[CombatParticipant]) - List of combat participants
- **Returns**: Success message with combat ID
- **Error Handling**: Raises HTTPException with 409 if combat already in progress

#### end_combat()
```python
def end_combat(self) -> Dict[str, str]:
    """End current combat"""
```
- **Purpose**: Terminates the current combat session
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

#### get_current_turn()
```python
def get_current_turn(self) -> Dict[str, Any]:
    """Get current turn information"""
```
- **Purpose**: Returns information about the current participant's turn
- **Returns**: Dictionary with current turn details
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

#### end_current_turn()
```python
def end_current_turn(self) -> Dict[str, Any]:
    """End current turn and move to next participant"""
```
- **Purpose**: Advances combat to the next participant's turn
- **Returns**: Information about the next participant
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

#### add_participant(participant: CombatParticipant)
```python
def add_participant(self, participant: CombatParticipant) -> Dict[str, str]:
    """Add a participant to current combat"""
```
- **Purpose**: Adds a new participant to an ongoing combat
- **Parameters**: `participant` (CombatParticipant) - The participant to add
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

#### remove_participant(participant_id: str)
```python
def remove_participant(self, participant_id: str) -> Dict[str, str]:
    """Remove a participant from current combat"""
```
- **Purpose**: Removes a participant from an ongoing combat
- **Parameters**: `participant_id` (str) - The ID of the participant to remove
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if participant not found

#### get_participant_info(participant_id: str)
```python
def get_participant_info(self, participant_id: str) -> Dict[str, Any]:
    """Get detailed information about a participant"""
```
- **Purpose**: Returns complete information about a specific participant
- **Parameters**: `participant_id` (str) - The ID of the participant
- **Returns**: Dictionary with participant details
- **Error Handling**: Raises HTTPException with 404 if participant not found

#### apply_effect(participant_id: str, effect: ActiveEffect)
```python
def apply_effect(self, participant_id: str, effect: ActiveEffect) -> Dict[str, str]:
    """Apply an effect to a participant"""
```
- **Purpose**: Applies a status effect to a participant
- **Parameters**:
  - `participant_id` (str) - The ID of the target participant
  - `effect` (ActiveEffect) - The effect to apply
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if participant not found

#### remove_effect(participant_id: str, effect_name: str)
```python
def remove_effect(self, participant_id: str, effect_name: str) -> Dict[str, str]:
    """Remove an effect from a participant"""
```
- **Purpose**: Removes a status effect from a participant
- **Parameters**:
  - `participant_id` (str) - The ID of the target participant
  - `effect_name` (str) - The name of the effect to remove
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if participant or effect not found

#### update_effects()
```python
def update_effects(self) -> Dict[str, Any]:
    """Update all active effects and return expired ones"""
```
- **Purpose**: Processes effect duration updates and returns expired effects
- **Returns**: Dictionary with expired effects information
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

### Combat Logic Methods

#### initialize_combat(characters: List[Dict[str, Any]])
```python
def initialize_combat(self, characters: List[Dict[str, Any]]) -> Dict[str, str]:
    """Initialize combat with provided characters"""
```
- **Purpose**: Sets up a new combat session with character data
- **Parameters**: `characters` (List[Dict[str, Any]]) - List of character data
- **Returns**: Success message with combat ID
- **Error Handling**: Raises HTTPException with 400 if initialization fails

#### advance_turn()
```python
def advance_turn(self) -> Optional[Dict[str, Any]]:
    """Advance to next turn and handle end/begin of turn effects"""
```
- **Purpose**: Advances combat to the next turn with effect processing
- **Returns**: Information about the new turn or None if no combat
- **Process**:
  1. Applies end-of-turn effects for previous participant
  2. Decrements effect durations
  3. Advances to next participant
  4. Applies start-of-turn effects
  5. Updates expired effects

#### perform_action(action_data: ActionData)
```python
def perform_action(self, action_data: ActionData) -> Dict[str, Any]:
    """Execute an action in combat"""
```
- **Purpose**: Executes a combat action (attack, cast, etc.)
- **Parameters**: `action_data` (ActionData) - Action to perform
- **Returns**: Dictionary with action results
- **Process**:
  1. Validates that it's the actor's turn
  2. Executes the appropriate action type
  3. Returns action results with damage, effects, etc.

#### delay_turn(actor_id: str)
```python
def delay_turn(self, actor_id: str) -> Dict[str, Any]:
    """Delay a participant's turn (move to end of round)"""
```
- **Purpose**: Moves a participant's turn to the end of the current round
- **Parameters**: `actor_id` (str) - The ID of the participant
- **Returns**: Success message
- **Error Handling**: Raises HTTPException with 404 if no combat in progress

### Action Handling

The combat service includes specialized methods for handling different action types:

#### _handle_attack_action(actor, action_data, combat_state)
- **Purpose**: Processes attack actions
- **Logic**: Calculates damage, applies to target, returns results

#### _handle_cast_action(actor, action_data, combat_state)
- **Purpose**: Processes spell casting actions
- **Logic**: Applies spell effects based on predefined spell mappings

#### _handle_utility_action(actor, action_data, combat_state)
- **Purpose**: Processes utility actions (dodge, parry, search)
- **Logic**: Rolls d20, applies success/failure effects

### Service Usage Example

```python
from src.services.combat_service import combat_service

# Start combat
participants = [CombatParticipant(...), CombatParticipant(...)]
combat_service.start_combat(participants)

# Perform an action
action = ActionData(actorId="player-1", actionType="Attack", targetId="enemy-1")
result = combat_service.perform_action(action)

# Apply an effect
effect = ActiveEffect(name="Poison", type=EffectType.DAMAGE, value=5, duration=3, duration_type=EffectDurationType.ROUND)
combat_service.apply_effect("player-1", effect)

# End combat
combat_service.end_combat()
```

## Service Patterns

### Error Handling

Both services follow consistent error handling patterns:

1. **HTTP Exceptions**: Use FastAPI's HTTPException for standardized error responses
2. **Status Codes**: Appropriate HTTP status codes (404, 400, 409, etc.)
3. **Error Messages**: Clear, descriptive error messages in French
4. **Validation**: Input validation before processing

### Business Logic Separation

- **API Layer**: Handles HTTP concerns (requests, responses, routing)
- **Service Layer**: Contains business rules and orchestration
- **Repository Layer**: Manages data persistence
- **Models**: Define data structures and validation

### Dependency Injection

Services use dependency injection for loose coupling:

```python
class CharacterService:
    def __init__(self, repository=character_repository):
        self.repository = repository
```

This allows for:
- Easy testing with mock dependencies
- Flexible configuration
- Clear separation of concerns

### Transaction Management

Services handle business transactions appropriately:

- **Character Operations**: Single operations (create, update, delete)
- **Combat Operations**: Multi-step operations with state management
- **Error Recovery**: Rollback on failures where appropriate

## Best Practices

### Service Design Principles

1. **Single Responsibility**: Each service handles one domain area
2. **Dependency Injection**: Services receive dependencies rather than creating them
3. **Error Handling**: Consistent error handling with appropriate HTTP status codes
4. **Validation**: Input validation at service boundaries
5. **Logging**: Appropriate logging for debugging and monitoring

### Performance Considerations

1. **Lazy Loading**: Load data only when needed
2. **Caching**: Consider caching for frequently accessed data
3. **Batch Operations**: Process multiple items efficiently when possible
4. **Async Operations**: Use async methods for I/O operations

### Testing Strategy

Services are designed to be easily testable:

1. **Unit Tests**: Test individual service methods
2. **Mock Dependencies**: Use mocks for repositories and other services
3. **Integration Tests**: Test service interactions
4. **Error Scenarios**: Test error handling paths

## Future Enhancements

Potential improvements to the service layer:

1. **Caching Layer**: Add caching for frequently accessed data
2. **Event System**: Implement domain events for better decoupling
3. **Validation Framework**: Centralized validation logic
4. **Metrics**: Add performance monitoring and metrics
5. **Background Tasks**: Async processing for long-running operations
