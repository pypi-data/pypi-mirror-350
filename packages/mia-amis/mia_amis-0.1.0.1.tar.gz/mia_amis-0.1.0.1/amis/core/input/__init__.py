from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import json

class InputHandler(ABC):
    """Screen base class for handling input"""
    
    @abstractmethod
    def receive(self) -> str:
        """Receiving and primary processing of input data"""
        pass