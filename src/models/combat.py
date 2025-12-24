"""
Combat models for the Dark Souls API
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid

from .base import EffectType


class EffectDurationType(str, Enum):
    INSTANT = "instant"
    ROUND = "round"
    PERMANENT = "permanent"


class ActiveEffect(BaseModel):
    """Active effect on a participant"""
    name: str
    type: EffectType
    duration: int = Field(ge=0)  # 0 = instant, >0 = number of rounds
    duration_type: EffectDurationType = EffectDurationType.ROUND
    value: Optional[int] = None
    stat_modifier: Optional[Dict[str, int]] = None
    description: Optional[str] = None


class CombatParticipant(BaseModel):
    """Combat participant with combat-specific data"""
    characterSheetId: str  # ID of the token Owlbear Rodeo
    isPlayer: bool = False
    controlledBy: List[str] = Field(default_factory=list)  # UUIDs of players
    initiative: int = Field(ge=0, le=100)
    activeEffects: List[ActiveEffect] = Field(default_factory=list)

    @validator("controlledBy", pre=True)
    def ensure_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v if isinstance(v, list) else []


class CombatState(BaseModel):
    """Main combat state"""
    turnOrder: List[str] = Field(default_factory=list)  # List of tokenId sorted by initiative descending
    currentTurnIndex: int = Field(default=0, ge=0)
    currentRound: int = Field(default=1, ge=1)
    participants: Dict[str, CombatParticipant] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def get_current_participant_id(self) -> Optional[str]:
        """Return the ID of the current participant"""
        if self.turnOrder and 0 <= self.currentTurnIndex < len(self.turnOrder):
            return self.turnOrder[self.currentTurnIndex]
        return None

    def get_current_participant(self) -> Optional[CombatParticipant]:
        """Return the current participant"""
        participant_id = self.get_current_participant_id()
        return self.participants.get(participant_id) if participant_id else None

    def get_next_participant_id(self) -> Optional[str]:
        """Return the ID of the next participant"""
        if not self.turnOrder:
            return None

        next_index = (self.currentTurnIndex + 1) % len(self.turnOrder)
        return self.turnOrder[next_index]

    def end_turn(self) -> None:
        """Move to the next participant"""
        if self.turnOrder:
            self.currentTurnIndex = (self.currentTurnIndex + 1) % len(self.turnOrder)
            # If we're back to the beginning, start a new round
            if self.currentTurnIndex == 0:
                self.currentRound += 1
            self.updated_at = datetime.now()

    def add_participant(self, participant: CombatParticipant) -> None:
        """Add a participant and update turn order"""
        self.participants[participant.characterSheetId] = participant
        self._update_turn_order()
        self.updated_at = datetime.now()

    def remove_participant(self, participant_id: str) -> bool:
        """Remove a participant from combat"""
        if participant_id in self.participants:
            del self.participants[participant_id]
            self._update_turn_order()
            self.updated_at = datetime.now()
            return True
        return False

    def _update_turn_order(self) -> None:
        """Update turn order by sorting by initiative descending"""
        sorted_participants = sorted(self.participants.values(), key=lambda p: p.initiative, reverse=True)
        self.turnOrder = [p.characterSheetId for p in sorted_participants]

        # Adjust current turn index if necessary
        if self.currentTurnIndex >= len(self.turnOrder):
            self.currentTurnIndex = max(0, len(self.turnOrder) - 1)

    def apply_effect(self, participant_id: str, effect: ActiveEffect) -> bool:
        """Apply an effect to a participant"""
        if participant_id not in self.participants:
            return False

        participant = self.participants[participant_id]

        # If it's an instant effect, apply it and remove it
        if effect.duration_type == EffectDurationType.INSTANT:
            # Instant effects are handled differently (damage, healing, etc.)
            return True

        # For duration effects, add to the list
        participant.activeEffects.append(effect)
        self.updated_at = datetime.now()
        return True

    def remove_effect(self, participant_id: str, effect_name: str) -> bool:
        """Remove an effect from a participant"""
        if participant_id not in self.participants:
            return False

        participant = self.participants[participant_id]
        initial_count = len(participant.activeEffects)

        participant.activeEffects = [effect for effect in participant.activeEffects if effect.name != effect_name]

        if len(participant.activeEffects) < initial_count:
            self.updated_at = datetime.now()
            return True
        return False

    def update_effects(self) -> List[Dict[str, Any]]:
        """Update active effects and return expired effects"""
        expired_effects = []

        for participant_id, participant in self.participants.items():
            active_effects = []

            for effect in participant.activeEffects:
                if effect.duration_type == EffectDurationType.ROUND:
                    effect.duration -= 1
                    if effect.duration > 0:
                        active_effects.append(effect)
                    else:
                        expired_effects.append({"participant_id": participant_id, "effect_name": effect.name, "effect": effect})
                else:
                    # For permanent effects or other types
                    active_effects.append(effect)

            participant.activeEffects = active_effects

        if expired_effects:
            self.updated_at = datetime.now()

        return expired_effects

    def is_combat_over(self) -> bool:
        """Check if combat is over (only one active participant left)"""
        active_participants = sum(1 for p in self.participants.values() if p.activeEffects)
        return len(self.participants) <= 1


class ActionData(BaseModel):
    """Action data for performAction"""
    actorId: str
    actionType: str  # Attack, Cast, Dodge, Parry, Search, etc.
    targetId: Optional[str] = None
    spellName: Optional[str] = None
    weaponName: Optional[str] = None
