import json

from pathlib import Path
from typing import Any, Dict, List, Union

class Config:
    """
    
    """
    @property
    def data(self) -> Dict[str, Any]:
        return self._data.copy()
    
    def __init__(self, default: Dict[str, Any], name: str, path: str = ""):
        """
        Initializing the configuration for the module.
        
        :param default: Standard configuration to be used if there is no file
        :param name: The name of the module (to be used as the name of the config file)
        """
        self.default = default
        self._data: Dict[str, Any] = {  }
        self._observer = None
        if len(default) > 0:
            config_dir = Path(f"{path}/configs")
            self.config_path = config_dir / f"{name}.json"
            config_dir.mkdir(exist_ok=True)
            self.auto_save = False
            if not self.load():
                self.save()

    def __getitem__(self, key: str) -> Any | None:
        return self._data.get(key)
    
    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
        if self.auto_save:
            self.save()

    def __delitem__(self, key: str):
        self._data[key] = self.default[key]
        if self.auto_save:
            self.save()

    def load(self) -> bool:
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    self._data = json.load(file)
                return True
            self._data = self.default.copy()
            print(self._data)
            return False
        except (json.JSONDecodeError, IOError):
            self.save()
            return False
        
    def save(self) -> bool:
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                json.dump(self._data, file, indent=4, ensure_ascii=False)
            return True
        except (IOError, TypeError):
            return False
        
    def reset(self) -> None:
        self._data = self.default.copy()
        self.save()

    def validate(self) -> bool:
        """Validate the current configuration against the default."""
        for key, default_value in self.default.items():
            if key not in self._data:
                return False
            if not isinstance(self._data[key], type(default_value)):
                return False
        return True
        
    def start_watcher(self) -> None:
        """Запускает наблюдение за файлом конфига."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class ConfigFileHandler(FileSystemEventHandler):
            def __init__(self, config: Config):
                self.config = config

            def on_modified(self, event):
                if event.src_path == str(self.config.config_path):
                    self.config._on_modified()

        self._observer = Observer()
        self._last_mtime = 0
        self._observer.schedule(
            ConfigFileHandler(self),
            path=str(self.config_path.parent),
        )
        self._observer.start()

    def _on_modified(self) -> None:
        """Вызывается при изменении файла конфига."""
        current_mtime = self.config_path.stat().st_mtime
        if current_mtime != self._last_mtime:
            self._last_mtime = current_mtime
            self.load()
            print(f"Config reloaded from {self.config_path}")

    def stop_watcher(self) -> None:
        """Останавливает наблюдение за файлом."""
        if self._observer:
            self._observer.stop()
            self._observer.join()