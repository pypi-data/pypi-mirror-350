from abc import ABC, abstractmethod
from typing import Any, Dict
from amis.core.input import InputHandler
from amis.core.output import OutputHandler
from amis.core import ModuleManager

class Person:
    def __init__(self, 
                 input_handler: InputHandler,
                 output_handler: OutputHandler,
                 module_manager: ModuleManager,
                 name: str = "MAI"):
        self.input = input_handler
        self.output = output_handler
        self.module_manager = module_manager
        self.name = name
    
    def run(self):
        """Основной цикл выполнения"""
        while True:
            # 1. Получение ввода
            input_data = self.input.receive().split()
            
            # 2. Обработка данных
            data = { 
                "module": input_data[0],
                "action": input_data[1],
                "params": input_data[2] 
                }
            
            self.module_manager[data["module"]].put({"action" : data["action"]})
            
            response = self._process("ok")


            
            # 3. Отправка вывода
            self.output.send({
                "response": response,
                "sender": self.name
            })
    
    def _process(self, data: Dict[str, Any]) -> str:
        """Простая обработка сообщения"""
        return f"Я получила: '{data.get('text', '')}'"