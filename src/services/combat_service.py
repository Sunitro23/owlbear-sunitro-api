"""
Combat service for the Dark Souls API
"""

from typing import Dict, List, Any, Optional
from fastapi import HTTPException, status

from src.models.combat import CombatParticipant, ActiveEffect, EffectType, EffectDurationType, ActionData
from src.services.combat_system import combat_manager


class CombatService:
    """Service layer for combat operations"""
    
    def __init__(self, manager=combat_manager):
        self.manager = manager
    
    def get_combat_status(self) -> Dict[str, Any]:
        """Get current combat status"""
        if not self.manager.is_combat_active():
            return {"message": "Aucun combat en cours"}

        combat_state = self.manager.get_combat_state()
        return {
            "combat_id": self.manager.get_combat_id(),
            "is_active": combat_state.is_active,
            "current_round": combat_state.currentRound,
            "current_turn_index": combat_state.currentTurnIndex,
            "turn_order": combat_state.turnOrder,
            "participants_count": len(combat_state.participants),
            "participants": self.manager.get_all_participants_info(),
            "created_at": combat_state.created_at,
            "updated_at": combat_state.updated_at,
        }

    def start_combat(self, participants: List[CombatParticipant]) -> Dict[str, str]:
        """Start a new combat"""
        try:
            combat_id = self.manager.start_combat(participants)
            return {"message": f"Combat démarré avec succès", "combat_id": combat_id}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    def end_combat(self) -> Dict[str, str]:
        """End current combat"""
        if not self.manager.is_combat_active():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun combat en cours à terminer",
            )

        success = self.manager.end_combat()
        if success:
            return {"message": "Combat terminé avec succès"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la terminaison du combat",
            )

    def get_current_turn(self) -> Dict[str, Any]:
        """Get current turn information"""
        turn_info = self.manager.get_current_turn_info()
        if not turn_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        return turn_info

    def end_current_turn(self) -> Dict[str, Any]:
        """End current turn and move to next participant"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        next_participant_id = self.manager.end_current_turn()
        if next_participant_id:
            return {
                "message": "Tour terminé, passage au participant suivant",
                "next_participant_id": next_participant_id,
                "current_round": self.manager.get_combat_state().currentRound,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la fin du tour",
            )

    def add_participant(self, participant: CombatParticipant) -> Dict[str, str]:
        """Add a participant to current combat"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        success = self.manager.add_participant_to_combat(participant)
        if success:
            return {"message": f"Participant {participant.characterSheetId} ajouté au combat"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de l'ajout du participant",
            )

    def remove_participant(self, participant_id: str) -> Dict[str, str]:
        """Remove a participant from current combat"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        success = self.manager.remove_participant_from_combat(participant_id)
        if success:
            return {"message": f"Participant {participant_id} supprimé du combat"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participant {participant_id} non trouvé dans le combat",
            )

    def get_participant_info(self, participant_id: str) -> Dict[str, Any]:
        """Get detailed information about a participant"""
        participant_info = self.manager.get_participant_info(participant_id)
        if not participant_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participant {participant_id} non trouvé dans le combat",
            )

        return participant_info

    def get_all_participants(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all participants"""
        if not self.manager.is_combat_active():
            return {}

        return self.manager.get_all_participants_info()

    def apply_effect(self, participant_id: str, effect: ActiveEffect) -> Dict[str, str]:
        """Apply an effect to a participant"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        success = self.manager.apply_effect_to_participant(participant_id, effect)
        if success:
            return {"message": f"Effet {effect.name} appliqué au participant {participant_id}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participant {participant_id} non trouvé dans le combat",
            )

    def remove_effect(self, participant_id: str, effect_name: str) -> Dict[str, str]:
        """Remove an effect from a participant"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        success = self.manager.remove_effect_from_participant(participant_id, effect_name)
        if success:
            return {"message": f"Effet {effect_name} supprimé du participant {participant_id}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Participant {participant_id} ou effet {effect_name} non trouvé",
            )

    def update_effects(self) -> Dict[str, Any]:
        """Update all active effects and return expired ones"""
        if not self.manager.is_combat_active():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun combat en cours")

        expired_effects = self.manager.update_all_effects()
        return {
            "message": f"{len(expired_effects)} effets ont expiré",
            "expired_effects": expired_effects,
        }

    # === COMBAT LOGIC METHODS ===

    def initialize_combat(self, characters: List[Dict[str, Any]]) -> Dict[str, str]:
        """Initialize combat with provided characters"""
        try:
            combat_id = self.manager.start_combat(characters)
            return {"message": "Combat initialisé avec succès", "combat_id": combat_id}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def advance_turn(self) -> Optional[Dict[str, Any]]:
        """Advance to next turn and handle end/begin of turn effects"""
        if not self.manager.is_combat_active():
            return None

        combat_state = self.manager.get_combat_state()
        if not combat_state:
            return None

        # Apply end of turn effects for previous participant
        previous_participant = combat_state.get_current_participant()
        if previous_participant:
            self._apply_end_of_turn_effects(previous_participant)

            # Decrement effect durations
            for effect in previous_participant.activeEffects:
                if effect.duration_type == EffectDurationType.ROUND and effect.duration > 0:
                    effect.duration -= 1

        # Move to next turn
        next_participant_id = self.manager.end_current_turn()

        # Handle start of new turn
        if next_participant_id:
            new_participant = combat_state.participants.get(next_participant_id)
            if new_participant:
                self._apply_start_of_turn_effects(new_participant)

        # Update expired effects
        expired_effects = self.manager.update_all_effects()

        # Return new turn information
        return self.manager.get_current_turn_info()

    def perform_action(self, action_data: ActionData) -> Dict[str, Any]:
        """Execute an action in combat"""
        if not self.manager.is_combat_active():
            return {"error": "Aucun combat en cours"}

        combat_state = self.manager.get_combat_state()
        if not combat_state:
            return {"error": "État du combat non disponible"}

        # Verify actor exists and it's their turn
        actor = combat_state.participants.get(action_data.actorId)
        if not actor:
            return {"error": f"Acteur {action_data.actorId} non trouvé"}

        current_participant_id = combat_state.get_current_participant_id()
        if current_participant_id != action_data.actorId:
            return {"error": f"Ce n'est pas le tour de {action_data.actorId}"}

        # Execute action based on type
        result = {"success": True, "action": action_data.actionType, "actor": action_data.actorId}

        if action_data.actionType == "Attack":
            result.update(self._handle_attack_action(actor, action_data, combat_state))
        elif action_data.actionType == "Cast":
            result.update(self._handle_cast_action(actor, action_data, combat_state))
        elif action_data.actionType in ["Dodge", "Parry", "Search"]:
            result.update(self._handle_utility_action(actor, action_data, combat_state))
        else:
            return {"error": f"Type d'action inconnu: {action_data.actionType}"}

        # Update combat state
        combat_state.updated_at = combat_state.updated_at

        return result

    def delay_turn(self, actor_id: str) -> Dict[str, Any]:
        """Delay a participant's turn (move to end of round)"""
        if not self.manager.is_combat_active():
            return {"error": "Aucun combat en cours"}

        combat_state = self.manager.get_combat_state()
        if not combat_state:
            return {"error": "État du combat non disponible"}

        if actor_id not in combat_state.participants:
            return {"error": f"Participant {actor_id} non trouvé"}

        # Remove participant from current position
        if actor_id in combat_state.turnOrder:
            combat_state.turnOrder.remove(actor_id)

        # Add to end
        combat_state.turnOrder.append(actor_id)

        # Adjust turn index if necessary
        current_participant_id = combat_state.get_current_participant_id()
        if current_participant_id == actor_id:
            # If it was this participant's turn, move to next
            combat_state.currentTurnIndex = (combat_state.currentTurnIndex + 1) % len(combat_state.turnOrder)

        combat_state.updated_at = combat_state.updated_at

        return {"success": True, "actor": actor_id, "message": f"Tour de {actor_id} retardé (jouera en dernier ce round)"}

    def _apply_end_of_turn_effects(self, participant: CombatParticipant) -> None:
        """Apply end of turn effects for a participant"""
        for effect in participant.activeEffects:
            if effect.type == EffectType.DAMAGE and effect.duration_type == EffectDurationType.ROUND:
                # Apply end of turn damage (e.g., poison)
                print(f"{participant.characterSheetId} subit {effect.value} dégâts de {effect.name}")

    def _apply_start_of_turn_effects(self, participant: CombatParticipant) -> None:
        """Apply start of turn effects for a participant"""
        for effect in participant.activeEffects:
            if effect.type == EffectType.BUFF and effect.duration_type == EffectDurationType.ROUND:
                # Apply start of turn buffs
                print(f"{participant.characterSheetId} bénéficie de {effect.name}")

    def _handle_attack_action(self, actor: CombatParticipant, action_data: ActionData, combat_state) -> Dict[str, Any]:
        """Handle attack action"""
        if not action_data.targetId:
            return {"error": "Cible requise pour une attaque"}

        target = combat_state.participants.get(action_data.targetId)
        if not target:
            return {"error": f"Cible {action_data.targetId} non trouvée"}

        # Calculate damage (simplified)
        import random
        d20_roll = random.randint(1, 20)
        base_damage = 10
        total_damage = base_damage + d20_roll

        print(f"{actor.characterSheetId} attaque {target.characterSheetId} et inflige {total_damage} dégâts")

        return {"target": action_data.targetId, "damage": total_damage, "roll": d20_roll, "message": f"Attaque réussie contre {target.characterSheetId}"}

    def _handle_cast_action(self, actor: CombatParticipant, action_data: ActionData, combat_state) -> Dict[str, Any]:
        """Handle cast action"""
        if not action_data.spellName:
            return {"error": "Nom du sort requis"}

        # Spell effects mapping
        spell_effects = {
            "Boule de Feu": {"damage": 25, "type": EffectType.DAMAGE},
            "Soins": {"healing": 15, "type": EffectType.HEALING},
            "Renforcement": {"buff": "ATK+2", "type": EffectType.BUFF}
        }

        spell_effect = spell_effects.get(action_data.spellName)
        if not spell_effect:
            return {"error": f"Sort {action_data.spellName} inconnu"}

        target_id = action_data.targetId or action_data.actorId  # Default to actor

        print(f"{actor.characterSheetId} lance {action_data.spellName} sur {target_id}")

        return {"spell": action_data.spellName, "target": target_id, "effect": spell_effect, "message": f"Sort {action_data.spellName} lancé avec succès"}

    def _handle_utility_action(self, actor: CombatParticipant, action_data: ActionData, combat_state) -> Dict[str, Any]:
        """Handle utility actions (Dodge, Parry, Search)"""
        import random
        d20_roll = random.randint(1, 20)
        difficulty = 10
        success = d20_roll >= difficulty

        if success:
            # Apply action effect
            if action_data.actionType == "Dodge":
                effect = ActiveEffect(name="Esquive Active", type=EffectType.BUFF, duration=1, duration_type=EffectDurationType.ROUND, description="Esquive augmentée pour ce round")
                self.manager.apply_effect_to_participant(actor.characterSheetId, effect)
            elif action_data.actionType == "Parry":
                effect = ActiveEffect(name="Parade Active", type=EffectType.BUFF, duration=1, duration_type=EffectDurationType.ROUND, description="Parade augmentée pour ce round")
                self.manager.apply_effect_to_participant(actor.characterSheetId, effect)

        return {"action": action_data.actionType, "success": success, "roll": d20_roll, "difficulty": difficulty, "message": f"{action_data.actionType} {'réussi' if success else 'échoué'}"}


# Default service instance
combat_service = CombatService()
