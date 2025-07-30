from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import json

class OutputHandler(ABC):
    """Abstract base class for output handling"""
    
    @abstractmethod
    def send(self, data: Dict[str, Any]) -> bool:
        """Sending processed data"""
        pass
    
    @abstractmethod
    def format(self, data: Dict[str, Any]) -> Any:
        """Formatting the output as required"""
        pass
