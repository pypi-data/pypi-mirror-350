import pytest
import time
from pathlib import Path
from amis.core import ModuleManager, Config
from amis.core.exceptions import ModuleLoadError
from ..modules.test_module import EchoModule, CounterModule

class TestModuleManager:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Подготовка тестового окружения"""
        self.manager = ModuleManager()
        self.temp_dir = tmp_path
        
    def test_module_loading(self):
        """Тест загрузки модуля"""
        self.manager.load(EchoModule)
        assert "EchoModule" in self.manager.modules
        
        module = self.manager["EchoModule"]
        assert module is not None
        assert module.configurable() is True

    def test_module_communication(self):
        """Тест обмена сообщениями"""
        self.manager.load(EchoModule)
        input, output = self.manager.start("EchoModule")
        
        test_message = {"message": "Hello AMIS!"}
        self.manager["EchoModule"].put(test_message)
        
        response = output.get(timeout=1)
        assert response["response"] == "Echo: Hello AMIS!"

    def test_module_lifecycle(self):
        """Тест жизненного цикла модуля"""
        self.manager.load(CounterModule)
        input, output = self.manager.start("CounterModule")
        
        # Проверка работы
        first = output.get(timeout=1)
        second = output.get(timeout=1)
        assert second["count"] == first["count"] + 1
        
        # Проверка остановки
        assert self.manager.stop("CounterModule") is True
        time.sleep(0.1)
        assert self.manager["CounterModule"]._process.is_alive() is False

    def test_invalid_module(self):
        """Тест обработки невалидных модулей"""
        class InvalidClass: pass
        
        with pytest.raises(ModuleLoadError):
            self.manager.load(InvalidClass)

@pytest.fixture
def cleanup_configs():
    """Фикстура для очистки конфигов после тестов"""
    yield
    config_dir = Path("configs")
    if config_dir.exists():
        for config_file in config_dir.glob("*.json"):
            config_file.unlink()
        config_dir.rmdir()