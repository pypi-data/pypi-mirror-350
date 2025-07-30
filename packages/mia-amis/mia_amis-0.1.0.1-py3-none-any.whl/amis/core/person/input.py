from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import json

class InputHandler(ABC):
    """Screen base class for handling input"""
    
    @abstractmethod
    def receive(self) -> Optional[Dict[str, Any]]:
        """Receiving and primary processing of input data"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validation of input data structure"""
        pass
    
    @abstractmethod
    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizing data to a standard format"""
        pass