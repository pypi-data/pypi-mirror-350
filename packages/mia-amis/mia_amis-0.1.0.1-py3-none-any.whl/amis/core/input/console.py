from . import InputHandler
from typing import Any, Dict, Optional

class ConsoleInput(InputHandler):
    """Ввод с консоли"""
    def receive(self) -> str:
        return input("Вы: ")