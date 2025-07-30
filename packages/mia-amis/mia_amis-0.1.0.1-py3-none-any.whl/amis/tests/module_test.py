import pytest
import time
from pathlib import Path
from amis.core import ModuleManager, Config
from amis.core.exceptions import ModuleLoadError
from ..modules.media_control import MediaControl
from unittest.mock import MagicMock


class TestModuleManager:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Подготовка тестового окружения"""
        self.manager = ModuleManager()
        self.temp_dir = tmp_path

    def test_media_control(self):        
        # Инициализация
        self.manager.load(MediaControl, "MediaControl")
        input, output = self.manager.start("MediaControl")
        module = self.manager["MediaControl"]
        
        # 1. Тест next track
        module.put({"action": "next"})
        time.sleep(0.5)  # Даем время на обработку

        module.put({"action": "play"})
        time.sleep(0.5)

        module.put({"action": "volume_up"})
        time.sleep(0.5)
        
        # 3. Проверяем вывод
        assert output.qsize() >= 2
        while not output.empty():
            response = output.get()
            assert response["status"] == "success"
            assert response["action"] in ["next", "play", "volume_up"]
        
        # Остановка
        assert self.manager.stop("MediaControl")

@pytest.fixture
def cleanup_configs():
    """Фикстура для очистки конфигов после тестов"""
    yield
    config_dir = Path("configs")
    if config_dir.exists():
        for config_file in config_dir.glob("*.json"):
            config_file.unlink()
        config_dir.rmdir()