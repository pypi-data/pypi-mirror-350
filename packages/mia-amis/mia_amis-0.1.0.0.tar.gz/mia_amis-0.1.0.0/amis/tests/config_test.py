import pytest
import time
import json
from pathlib import Path
from unittest.mock import MagicMock
from amis.core import ModuleManager, Config
from amis.core.exceptions import ModuleLoadError
from ..modules.test_module import ConfigurableModule

class TestModuleManager:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Подготовка тестового окружения"""
        self.manager = ModuleManager()
        self.temp_dir = tmp_path

    def test_config_handling(self):
        """Тест работы с конфигурацией"""
        # Проверка создания конфига
        self.manager.load(ConfigurableModule, config_path=self.temp_dir)
        config_path = self.temp_dir / f"configs/ConfigurableModule.json"
        assert config_path.exists()
        
        # Проверка переопределения конфига
        self.manager.load(
            ConfigurableModule,
            module_name="CustomConfigModule"
        )

        self.manager.get("CustomConfigModule").config["param1"] = "custom_value"
        
        module = self.manager["CustomConfigModule"]
        assert module.config["param1"] == "custom_value"
        assert module.config["param2"] == 42  # Значение по умолчанию

    def test_config_watcher(self):
        """Тестирование горячей перезагрузки конфига"""
        # 1. Подготовка тестового файла конфига
        config_dir = self.temp_dir
        config_file = config_dir / "configs" / "test_config.json"
        
        initial_config = {"key": "value"}
        
        # 2. Инициализация конфига
        config = Config(default=initial_config, name="test_config", path=str(config_dir))
        
        # 4. Запускаем watcher
        config.start_watcher()
        
        try:
            # 5. Проверяем начальную загрузку
            assert config["key"] == "value"
            new_config = {"key" : "new_value"}
            # 6. Имитируем изменение файла
            try:
                with open(config_file, 'w', encoding='utf-8') as file:
                    json.dump(new_config, file, indent=4, ensure_ascii=False)
            except (IOError, TypeError) as e:
                print("JSON error:", e)

            # 7. Даем время на обнаружение изменений
            time.sleep(1)  # Для watchdog нужно немного времени
            
            # 8. Проверяем что конфиг обновился
            assert config["key"] == "new_value"
            
            # 9. Имитируем невалидное изменение
            with open(config_file, 'w') as f:
                f.write("{invalid_json")
            
            # 10. Проверяем что предыдущее значение сохранилось
            time.sleep(1)
            assert config["key"] == "new_value"
            
        finally:
            # 11. Останавливаем watcher
            config.stop_watcher()

    def test_multiple_watchers(self):
        """Тестирование нескольких одновременных watcher"""
        config_dir = self.temp_dir
        config1 = Config({"key1": "value1"}, "config1", str(config_dir))
        config2 = Config({"key2": "value2"}, "config2", str(config_dir))
        
        config1.start_watcher()
        config2.start_watcher()
        
        try:
            # Изменяем только config1
            (config_dir / "configs" / "config1.json").write_text('{"key1": "updated"}')
            time.sleep(1)
            
            assert config1["key1"] == "updated"
            assert config2["key2"] == "value2"  # Не должен измениться
            
        finally:
            config1.stop_watcher()
            config2.stop_watcher()

    def test_watcher_with_manual_changes(self):
        """Тестирование ручного изменения конфига"""
        config_dir = self.temp_dir
        config = Config({"param": 1}, "manual_config", str(config_dir))
        
        config.start_watcher()
        
        try:
            # Ручное изменение через API
            config.auto_save = True
            config["param"] = 2
            time.sleep(0.5)  # Даем время на сохранение
            
            # Но файл должен обновиться
            with open(config.config_path) as f:
                assert json.load(f)["param"] == 2
                
        finally:
            config.stop_watcher()

@pytest.fixture
def cleanup_configs():
    """Фикстура для очистки конфигов после тестов"""
    yield
    config_dir = Path("configs")
    if config_dir.exists():
        for config_file in config_dir.glob("*.json"):
            config_file.unlink()
        config_dir.rmdir()