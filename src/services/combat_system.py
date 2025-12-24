"""
Combat system for the Dark Souls API
Gère un seul combat à la fois avec un ID de token Owlbear Rodeo comme identifiant unique
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid
import random


class EffectType(str, Enum):
    DAMAGE = "damage"
    HEALING = "healing"
    BUFF = "buff"
    DEBUFF = "debuff"
    UTILITY = "utility"


class EffectDurationType(str, Enum):
    INSTANT = "instant"
    ROUND = "round"
    PERMANENT = "permanent"


class ActiveEffect(BaseModel):
    """Effet actif sur un participant"""

    name: str
    type: EffectType
    duration: int = Field(ge=0)  # 0 = instant, >0 = nombre de rounds
    duration_type: EffectDurationType = EffectDurationType.ROUND
    value: Optional[int] = None
    stat_modifier: Optional[Dict[str, int]] = None
    description: Optional[str] = None


class CombatParticipant(BaseModel):
    """Participant au combat avec données spécifiques au combat"""

    characterSheetId: str  # ID du token Owlbear Rodeo
    isPlayer: bool = False
    controlledBy: List[str] = Field(default_factory=list)  # UUID des joueurs
    initiative: int = Field(ge=0, le=100)
    activeEffects: List[ActiveEffect] = Field(default_factory=list)

    @validator("controlledBy", pre=True)
    def ensure_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v if isinstance(v, list) else []


class CombatState(BaseModel):
    """État principal du combat"""

    turnOrder: List[str] = Field(default_factory=list)  # Liste des tokenId triés par initiative décroissante
    currentTurnIndex: int = Field(default=0, ge=0)
    currentRound: int = Field(default=1, ge=1)
    participants: Dict[str, CombatParticipant] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def get_current_participant_id(self) -> Optional[str]:
        """Renvoie l'ID du participant actuel"""
        if self.turnOrder and 0 <= self.currentTurnIndex < len(self.turnOrder):
            return self.turnOrder[self.currentTurnIndex]
        return None

    def get_current_participant(self) -> Optional[CombatParticipant]:
        """Renvoie le participant actuel"""
        participant_id = self.get_current_participant_id()
        return self.participants.get(participant_id) if participant_id else None

    def get_next_participant_id(self) -> Optional[str]:
        """Renvoie l'ID du prochain participant"""
        if not self.turnOrder:
            return None

        next_index = (self.currentTurnIndex + 1) % len(self.turnOrder)
        return self.turnOrder[next_index]

    def end_turn(self) -> None:
        """Passe au participant suivant"""
        if self.turnOrder:
            self.currentTurnIndex = (self.currentTurnIndex + 1) % len(self.turnOrder)
            # Si on revient au début, on commence un nouveau round
            if self.currentTurnIndex == 0:
                self.currentRound += 1
            self.updated_at = datetime.now()

    def add_participant(self, participant: CombatParticipant) -> None:
        """Ajoute un participant et met à jour l'ordre des tours"""
        self.participants[participant.characterSheetId] = participant
        self._update_turn_order()
        self.updated_at = datetime.now()

    def remove_participant(self, participant_id: str) -> bool:
        """Supprime un participant du combat"""
        if participant_id in self.participants:
            del self.participants[participant_id]
            self._update_turn_order()
            self.updated_at = datetime.now()
            return True
        return False

    def _update_turn_order(self) -> None:
        """Met à jour l'ordre des tours en triant par initiative décroissante"""
        sorted_participants = sorted(self.participants.values(), key=lambda p: p.initiative, reverse=True)
        self.turnOrder = [p.characterSheetId for p in sorted_participants]

        # Ajuste l'index du tour actuel si nécessaire
        if self.currentTurnIndex >= len(self.turnOrder):
            self.currentTurnIndex = max(0, len(self.turnOrder) - 1)

    def apply_effect(self, participant_id: str, effect: ActiveEffect) -> bool:
        """Applique un effet à un participant"""
        if participant_id not in self.participants:
            return False

        participant = self.participants[participant_id]

        # Si c'est un effet instantané, on l'applique et on le supprime
        if effect.duration_type == EffectDurationType.INSTANT:
            # Les effets instantanés sont gérés différemment (dégâts, soins, etc.)
            return True

        # Pour les effets à durée, on les ajoute à la liste
        participant.activeEffects.append(effect)
        self.updated_at = datetime.now()
        return True

    def remove_effect(self, participant_id: str, effect_name: str) -> bool:
        """Supprime un effet d'un participant"""
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
        """Met à jour les effets actifs et renvoie les effets expirés"""
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
                    # Pour les effets permanents ou autres types
                    active_effects.append(effect)

            participant.activeEffects = active_effects

        if expired_effects:
            self.updated_at = datetime.now()

        return expired_effects

    def is_combat_over(self) -> bool:
        """Vérifie si le combat est terminé (plus d'un participant actif)"""
        active_participants = sum(1 for p in self.participants.values() if p.activeEffects)
        return len(self.participants) <= 1


class CombatManager:
    """Gestionnaire de combat - gère un seul combat à la fois"""

    def __init__(self):
        self._combat_state: Optional[CombatState] = None
        self._combat_id: Optional[str] = None

    def start_combat(self, participants: List[CombatParticipant]) -> str:
        """Démarre un nouveau combat avec les participants spécifiés"""
        if self._combat_state and self._combat_state.is_active:
            raise Exception("Un combat est déjà en cours. Terminez-le avant d'en commencer un nouveau.")

        # Crée un nouvel état de combat
        self._combat_id = str(uuid.uuid4())
        self._combat_state = CombatState()

        # Ajoute tous les participants
        for participant in participants:
            self._combat_state.add_participant(participant)

        return self._combat_id

    def end_combat(self) -> bool:
        """Termine le combat actuel"""
        if self._combat_state:
            self._combat_state.is_active = False
            self._combat_state.updated_at = datetime.now()
            return True
        return False

    def get_combat_state(self) -> Optional[CombatState]:
        """Renvoie l'état du combat actuel"""
        return self._combat_state

    def get_combat_id(self) -> Optional[str]:
        """Renvoie l'ID du combat actuel"""
        return self._combat_id

    def is_combat_active(self) -> bool:
        """Vérifie si un combat est actif"""
        return self._combat_state is not None and self._combat_state.is_active

    def end_current_turn(self) -> Optional[str]:
        """Termine le tour actuel et passe au suivant"""
        if not self._combat_state:
            return None

        self._combat_state.end_turn()
        return self._combat_state.get_current_participant_id()

    def get_current_turn_info(self) -> Optional[Dict[str, Any]]:
        """Renvoie les informations sur le tour actuel"""
        if not self._combat_state:
            return None

        current_participant = self._combat_state.get_current_participant()
        if not current_participant:
            return None

        return {
            "combat_id": self._combat_id,
            "current_round": self._combat_state.currentRound,
            "current_turn_index": self._combat_state.currentTurnIndex,
            "current_participant": {"characterSheetId": current_participant.characterSheetId, "isPlayer": current_participant.isPlayer, "initiative": current_participant.initiative, "activeEffects": [effect.dict() for effect in current_participant.activeEffects]},
            "turn_order": self._combat_state.turnOrder,
            "total_participants": len(self._combat_state.participants),
        }

    def add_participant_to_combat(self, participant: CombatParticipant) -> bool:
        """Ajoute un participant au combat en cours"""
        if not self._combat_state or not self._combat_state.is_active:
            return False

        self._combat_state.add_participant(participant)
        return True

    def remove_participant_from_combat(self, participant_id: str) -> bool:
        """Supprime un participant du combat en cours"""
        if not self._combat_state or not self._combat_state.is_active:
            return False

        return self._combat_state.remove_participant(participant_id)

    def apply_effect_to_participant(self, participant_id: str, effect: ActiveEffect) -> bool:
        """Applique un effet à un participant"""
        if not self._combat_state or not self._combat_state.is_active:
            return False

        return self._combat_state.apply_effect(participant_id, effect)

    def remove_effect_from_participant(self, participant_id: str, effect_name: str) -> bool:
        """Supprime un effet d'un participant"""
        if not self._combat_state or not self._combat_state.is_active:
            return False

        return self._combat_state.remove_effect(participant_id, effect_name)

    def update_all_effects(self) -> List[Dict[str, Any]]:
        """Met à jour tous les effets actifs"""
        if not self._combat_state or not self._combat_state.is_active:
            return []

        return self._combat_state.update_effects()

    def get_participant_info(self, participant_id: str) -> Optional[Dict[str, Any]]:
        """Renvoie les informations détaillées d'un participant"""
        if not self._combat_state:
            return None

        participant = self._combat_state.participants.get(participant_id)
        if not participant:
            return None

        return {
            "characterSheetId": participant.characterSheetId,
            "isPlayer": participant.isPlayer,
            "controlledBy": participant.controlledBy,
            "initiative": participant.initiative,
            "activeEffects": [effect.dict() for effect in participant.activeEffects],
            "total_effects": len(participant.activeEffects),
        }

    def get_all_participants_info(self) -> Dict[str, Dict[str, Any]]:
        """Renvoie les informations de tous les participants"""
        if not self._combat_state:
            return {}

        return {participant_id: self.get_participant_info(participant_id) for participant_id in self._combat_state.participants.keys()}


# Instance globale du gestionnaire de combat
combat_manager = CombatManager()


# === FONCTIONS DE LOGIQUE DE COMBAT ===


class ActionData(BaseModel):
    """Données d'action pour performAction"""

    actorId: str
    actionType: str  # Attack, Cast, Dodge, Parry, Search, etc.
    targetId: Optional[str] = None
    spellName: Optional[str] = None
    weaponName: Optional[str] = None


def start_combat(characters: List[Dict[str, Any]]) -> str:
    """
    Initialise un combat avec les personnages fournis.

    Args:
        characters: Liste de personnages avec leurs données complètes

    Returns:
        str: ID du combat créé
    """
    participants = []

    for character_data in characters:
        # Calcul de l'initiative : d20 + modificateur AGL (ou DEX)
        # Pour cet exemple, on utilise un d20 + un modificateur basé sur DEX
        d20_roll = random.randint(1, 20)
        dex_modifier = character_data.get("character", {}).get("stats", {}).get("DEX", {}).get("modifier", 0)
        initiative = d20_roll + dex_modifier

        participant = CombatParticipant(characterSheetId=character_data.get("character", {}).get("main", {}).get("name", "Unknown"), isPlayer=True, controlledBy=["system"], initiative=initiative, activeEffects=[])  # À adapter selon vos besoins  # À adapter selon vos besoins

        participants.append(participant)

    return combat_manager.start_combat(participants)


def next_turn() -> Optional[Dict[str, Any]]:
    """
    Passe au tour suivant et gère les effets de fin/début de tour.

    Returns:
        Dict: Informations sur le nouveau tour, ou None si aucun combat actif
    """
    if not combat_manager.is_combat_active():
        return None

    combat_state = combat_manager.get_combat_state()
    if not combat_state:
        return None

    # 1. Appliquer les effets de fin de tour pour le participant précédent
    previous_participant = combat_state.get_current_participant()
    if previous_participant:
        # Appliquer les effets de fin de tour (ex: dégâts de poison)
        apply_end_of_turn_effects(previous_participant)

        # Décrémenter la durée des effets
        for effect in previous_participant.activeEffects:
            if effect.duration_type == EffectDurationType.ROUND and effect.duration > 0:
                effect.duration -= 1

    # 2. Passer au tour suivant
    next_participant_id = combat_manager.end_current_turn()

    # 3. Gérer le début du nouveau tour
    if next_participant_id:
        new_participant = combat_state.participants.get(next_participant_id)
        if new_participant:
            # Réinitialiser les AP (exemple: END / 4)
            # Note: Cette partie nécessiterait d'accéder aux données du personnage complet
            # Pour l'instant, on applique simplement les effets de début de tour

            # Appliquer les effets de début de tour
            apply_start_of_turn_effects(new_participant)

    # 4. Mettre à jour les effets expirés
    expired_effects = combat_manager.update_all_effects()

    # 5. Retourner les informations du nouveau tour
    return combat_manager.get_current_turn_info()


def apply_end_of_turn_effects(participant: CombatParticipant) -> None:
    """
    Applique les effets de fin de tour pour un participant.
    """
    for effect in participant.activeEffects:
        if effect.type == EffectType.DAMAGE and effect.duration_type == EffectDurationType.ROUND:
            # Appliquer les dégâts de fin de tour (ex: poison)
            print(f"{participant.characterSheetId} subit {effect.value} dégâts de {effect.name}")


def apply_start_of_turn_effects(participant: CombatParticipant) -> None:
    """
    Applique les effets de début de tour pour un participant.
    """
    for effect in participant.activeEffects:
        if effect.type == EffectType.BUFF and effect.duration_type == EffectDurationType.ROUND:
            # Appliquer les effets de début de tour
            print(f"{participant.characterSheetId} bénéficie de {effect.name}")


def perform_action(action_data: ActionData) -> Dict[str, Any]:
    """
    Exécute une action dans le combat.

    Args:
        action_data: Données de l'action à exécuter

    Returns:
        Dict: Résultat de l'action
    """
    if not combat_manager.is_combat_active():
        return {"error": "Aucun combat en cours"}

    combat_state = combat_manager.get_combat_state()
    if not combat_state:
        return {"error": "État du combat non disponible"}

    # 1. Vérifier que l'acteur existe et c'est bien son tour
    actor = combat_state.participants.get(action_data.actorId)
    if not actor:
        return {"error": f"Acteur {action_data.actorId} non trouvé"}

    # Vérifier que c'est bien le tour de l'acteur
    current_participant_id = combat_state.get_current_participant_id()
    if current_participant_id != action_data.actorId:
        return {"error": f"Ce n'est pas le tour de {action_data.actorId}"}

    # 2. Vérifier les ressources (AP, uses, etc.)
    # Note: Cette vérification nécessiterait d'accéder aux données complètes du personnage
    # Pour l'exemple, on suppose que les ressources sont suffisantes

    # 3. Exécuter l'action selon son type
    result = {"success": True, "action": action_data.actionType, "actor": action_data.actorId}

    if action_data.actionType == "Attack":
        result.update(handle_attack_action(actor, action_data, combat_state))

    elif action_data.actionType == "Cast":
        result.update(handle_cast_action(actor, action_data, combat_state))

    elif action_data.actionType in ["Dodge", "Parry", "Search"]:
        result.update(handle_utility_action(actor, action_data, combat_state))

    else:
        return {"error": f"Type d'action inconnu: {action_data.actionType}"}

    # 4. Mettre à jour l'état du combat
    combat_state.updated_at = datetime.now()

    return result


def handle_attack_action(actor: CombatParticipant, action_data: ActionData, combat_state: CombatState) -> Dict[str, Any]:
    """Gère une action d'attaque."""
    if not action_data.targetId:
        return {"error": "Cible requise pour une attaque"}

    target = combat_state.participants.get(action_data.targetId)
    if not target:
        return {"error": f"Cible {action_data.targetId} non trouvée"}

    # Calcul des dégâts (exemple simplifié)
    d20_roll = random.randint(1, 20)
    base_damage = 10
    total_damage = base_damage + d20_roll

    # Appliquer les dégâts (simulation)
    # Note: Dans un vrai système, on modifierait les HP de la cible
    print(f"{actor.characterSheetId} attaque {target.characterSheetId} et inflige {total_damage} dégâts")

    return {"target": action_data.targetId, "damage": total_damage, "roll": d20_roll, "message": f"Attaque réussie contre {target.characterSheetId}"}


def handle_cast_action(actor: CombatParticipant, action_data: ActionData, combat_state: CombatState) -> Dict[str, Any]:
    """Gère une action de sort."""
    if not action_data.spellName:
        return {"error": "Nom du sort requis"}

    # Simulation de l'effet du sort
    spell_effects = {"Boule de Feu": {"damage": 25, "type": EffectType.DAMAGE}, "Soins": {"healing": 15, "type": EffectType.HEALING}, "Renforcement": {"buff": "ATK+2", "type": EffectType.BUFF}}

    spell_effect = spell_effects.get(action_data.spellName)
    if not spell_effect:
        return {"error": f"Sort {action_data.spellName} inconnu"}

    target_id = action_data.targetId or action_data.actorId  # Cible par défaut: l'acteur

    print(f"{actor.characterSheetId} lance {action_data.spellName} sur {target_id}")

    return {"spell": action_data.spellName, "target": target_id, "effect": spell_effect, "message": f"Sort {action_data.spellName} lancé avec succès"}


def handle_utility_action(actor: CombatParticipant, action_data: ActionData, combat_state: CombatState) -> Dict[str, Any]:
    """Gère une action utilitaire (Dodge, Parry, Search)."""
    # Jet de compétence (d20 + modificateur)
    d20_roll = random.randint(1, 20)
    difficulty = 10  # Difficulté de base

    success = d20_roll >= difficulty

    if success:
        # Appliquer l'effet de l'action
        if action_data.actionType == "Dodge":
            effect = ActiveEffect(name="Esquive Active", type=EffectType.BUFF, duration=1, duration_type=EffectDurationType.ROUND, description="Esquive augmentée pour ce round")
            combat_manager.apply_effect_to_participant(actor.characterSheetId, effect)

        elif action_data.actionType == "Parry":
            effect = ActiveEffect(name="Parade Active", type=EffectType.BUFF, duration=1, duration_type=EffectDurationType.ROUND, description="Parade augmentée pour ce round")
            combat_manager.apply_effect_to_participant(actor.characterSheetId, effect)

    return {"action": action_data.actionType, "success": success, "roll": d20_roll, "difficulty": difficulty, "message": f"{action_data.actionType} {'réussi' if success else 'échoué'}"}


def delay_turn(actor_id: str) -> Dict[str, Any]:
    """
    Retarde le tour d'un participant (le place en fin de round).

    Args:
        actor_id: ID du participant dont on retarde le tour

    Returns:
        Dict: Résultat de l'opération
    """
    if not combat_manager.is_combat_active():
        return {"error": "Aucun combat en cours"}

    combat_state = combat_manager.get_combat_state()
    if not combat_state:
        return {"error": "État du combat non disponible"}

    if actor_id not in combat_state.participants:
        return {"error": f"Participant {actor_id} non trouvé"}

    # Retirer le participant de sa position actuelle
    if actor_id in combat_state.turnOrder:
        combat_state.turnOrder.remove(actor_id)

    # L'ajouter à la fin
    combat_state.turnOrder.append(actor_id)

    # Ajuster l'index du tour si nécessaire
    current_participant_id = combat_state.get_current_participant_id()
    if current_participant_id == actor_id:
        # Si c'était le tour de ce participant, passer au suivant
        combat_state.currentTurnIndex = (combat_state.currentTurnIndex + 1) % len(combat_state.turnOrder)

    combat_state.updated_at = datetime.now()

    return {"success": True, "actor": actor_id, "message": f"Tour de {actor_id} retardé (jouera en dernier ce round)"}
