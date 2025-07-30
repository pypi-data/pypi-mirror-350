from amis.core import Module
import time
from typing import Dict, Any

class EchoModule(Module):
    """Тестовый модуль для проверки базовой функциональности"""
    DEFAULT_CONFIG = {
        "response_delay": 0.1,
        "default_response": "Echo: "
    }

    def execute(self) -> None:
        while True:
            data = self.input.get()
            time.sleep(self.config["response_delay"])
            response = f"{self.config['default_response']}{data['message']}"
            self.output.put({"response": response})

class CounterModule(Module):
    """Модуль-счётчик для проверки состояния"""
    def execute(self) -> None:
        counter = 0
        while True:
            self.output.put({"count": counter})
            counter += 1
            time.sleep(0.5)

class ConfigurableModule(Module):
    """Модуль с конфигурацией для тестирования настроек"""
    DEFAULT_CONFIG = {
        "param1": "default",
        "param2": 42
    }

    def execute(self) -> None:
        while True:
            config = self.config.data
            self.output.put(config)
            time.sleep(1)