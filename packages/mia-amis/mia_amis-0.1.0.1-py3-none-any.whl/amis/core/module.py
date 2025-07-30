from multiprocessing import Process, Queue
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, Tuple
from .config import Config

class Module(ABC):
    """

    """
    DEFAULT_CONFIG: Dict[str, Any] = {  }

    def __init__(self, path: str = ""):
        self.input = Queue()
        self.output = Queue()
        self._process = Process(
            target = self.execute,
            name = self.__class__.__name__,
            daemon = True
        )
        self.config = Config(self.DEFAULT_CONFIG, self.__class__.__name__, path)

    def start(self) -> Tuple[Queue, Queue]:
        self._process.start()
        return (self.input, self.output)

    def stop(self) -> bool:
        if self._process.is_alive():
            if self.config._observer != None:
                self.config.stop_watcher()
            self._process.terminate()
            return self._process.is_alive()
        return False

    def get(self) -> Dict:
        return self.output.get()

    def put(self, args: Dict[str, Any]):
        self.input.put(args)

    def configurable(self) -> bool:
        return len(self.config.default) != 0

    @abstractmethod
    def execute(self) -> Any:
        """The basic method that every plugin must implement"""
        raise NotImplementedError("The plugin must implement the execute() method.")
    
    @property
    def name(self) -> str:
        return self._process.name

    @property
    def metadata(self) -> Dict[str, Any]:
        """Plugin metadata"""
        return {
            "module_name": self.__class__.__name__,
            "version": "Unknown",
            "author": "Unknown"
        }