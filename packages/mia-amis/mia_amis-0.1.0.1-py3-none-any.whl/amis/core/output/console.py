from . import OutputHandler
from typing import Any, Dict, Optional

class ConsoleOutput(OutputHandler):
    """Вывод в консоль"""
    def send(self, data: Dict[str, Any]) -> bool:
        print(f"{data['sender']}: {data['response']}")
        return True