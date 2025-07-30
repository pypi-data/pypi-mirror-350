import keyboard
import time
from typing import Dict, Any
from ..core import Module

class MediaControl(Module):
    """
    Global media player control module
    
    Features:
    - System-wide media control
    - Hotkey emulation
    - Multi-player support
    """
    DEFAULT_CONFIG = {
        "track_change_delay": 0.5
    }

    def execute(self) -> None:
        """Основной цикл обработки команд"""
        while True:
            if not self.input.empty():
                command = self.input.get()
                self._handle_command(command)
            time.sleep(0.1)

    def _handle_command(self, command: Dict[str, Any]) -> None:
        """Обработка входящих команд"""
        action = command.get("action")
        
        try:
            if action == "play":
                self._play()
            elif action == "pause":
                self._pause()
            elif action == "next":
                self._next_track()
            elif action == "prev":
                self._prev_track()
            elif action == "volume_up":
                self._volume_up()
            elif action == "volume_down":
                self._volume_down()
            elif action == "mute":
                self._mute()
                
            self.output.put({"status": "success", "action": action})
            time.sleep(self.config["track_change_delay"])
            
        except Exception as e:
            self.output.put({"status": "error", "message": str(e)})

    def _play(self) -> None:
        """Play"""
        keyboard.send("play")

    def _pause(self) -> None:
        """Pause"""
        keyboard.send("pause")

    def _next_track(self) -> None:
        """Следующий трек"""
        keyboard.send("next track")

    def _prev_track(self) -> None:
        """Предыдущий трек"""
        keyboard.send("previous track")

    def _volume_up(self) -> None:
        """Увеличить громкость"""
        keyboard.send("volume up")

    def _volume_down(self) -> None:
        """Уменьшить громкость"""
        keyboard.send("volume down")

    def _mute(self) -> None:
        """Отключить звук"""
        keyboard.send("volume mute")

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "module_name": "MediaControl",
            "version": "1.0",
            "author": "RayzorST",
            "description": "Media control using system hotkeys"
        }