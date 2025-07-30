from amis.core import ModuleManager
from amis.core.person import Person
from amis.core.input.console import ConsoleInput
from amis.core.output.console import ConsoleOutput

if __name__ == "__main__":
    # Инициализация
    manager = ModuleManager()
    ai = Person(ConsoleInput(), ConsoleOutput(), manager)
    ai.run()
    # Выполнение команды
    
    print(result)