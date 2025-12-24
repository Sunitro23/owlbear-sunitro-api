"""
Storage abstraction for the Dark Souls API
"""

import json
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class StorageInterface(ABC):
    """Abstract interface for storage operations"""
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load data from storage"""
        pass
    
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        """Save data to storage"""
        pass


class JSONStorage(StorageInterface):
    """JSON file storage implementation"""
    
    def __init__(self, file_path: str = "characters.json"):
        self.file_path = file_path
    
    def load(self) -> Dict[str, Any]:
        """Load characters from JSON file"""
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def save(self, data: Dict[str, Any]) -> None:
        """Save characters to JSON file"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
