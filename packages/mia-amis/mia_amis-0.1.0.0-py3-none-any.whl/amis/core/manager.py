import json

from multiprocessing import Process, Queue
from typing import Dict, Type, Any, Optional, Tuple
from .config import Config
from .module import Module
from .exceptions import ModuleLoadError, ModuleNotFoundError

class ModuleManager:
    def __init__(self):
        self.modules: Dict[str, Type[Module]] = {  }
        self.config = Config(
            {
                "config_auto_save" : False,
                "config_hot_reload" : False,
                "module_settings" : {  }
            },
            self.__class__.__name__
        )

    def __getitem__(self, key: str) -> Optional[Module]:
        return self.modules.get(key)

    def load(
            self, 
            module_class: Type[Module], 
            module_name: str = None,
            config_path: str = ""
        ):
        
        if not issubclass(module_class, Module):
            raise ModuleLoadError(f"{module_class.__name__} is not a subclass of Module")
        
        try:
            module = module_class(config_path)
        except Exception as e:
            raise ModuleLoadError(f"Failed to initialize module: {str(e)}") from e
        
        if module_name and module_name != module.name:
            module._process.name = module_name

        if module.configurable():
            if module_name not in self.config["module_settings"]:
                self.config["module_settings"][module_name] = {
                    "config_auto_save" : False,
                    "config_watcher" : False
                }

            module_config = self.config["module_settings"][module_name]
        
            module.config.auto_save = module_config["config_auto_save"]
            if module_config["config_watcher"]:
                module.config.start_watcher()

        if self.config["config_auto_save"]:
            self.config.save()
        self.modules[module_name if module_name else module.name] = module

    def start(self, module_name: str) -> Tuple[Queue, Queue]:
        if self.get(module_name) is None:
            raise ModuleNotFoundError(f"Plugin {module_name} not found")
        
        return self.modules[module_name].start()

    def stop(self, module_name: str) -> bool:
        if self.get(module_name) is not None:
            return self.modules[module_name].stop()
        return False

    def remove(self, module_name: str):
        self.get(module_name).stop()
        del self.modules[module_name]

    def get(self, module_name: str) -> Type[Module] | None:
        return self.modules.get(module_name)