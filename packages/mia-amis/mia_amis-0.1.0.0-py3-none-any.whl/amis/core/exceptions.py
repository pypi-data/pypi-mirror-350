class ModuleError(Exception):
    """Базовое исключение для ошибок плагинов."""
    pass

class ModuleLoadError(ModuleError):
    """Ошибка загрузки плагина."""
    pass

class ModuleNotFoundError(ModuleError):
    """Плагин не найден."""
    pass