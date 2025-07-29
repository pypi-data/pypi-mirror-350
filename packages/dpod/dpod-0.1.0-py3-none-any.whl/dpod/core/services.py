from rich.console import Console
from rich.theme import Theme

from .interfaces import LoggerServiceABC


custom_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "info": "bold blue"
})

console = Console(theme=custom_theme)


class LoggerService(LoggerServiceABC):
    @staticmethod
    def success(msg: str):
        console.print(f"✓ {msg}", style="success")
    
    @staticmethod
    def error(msg: str):
        console.print(f"✗ {msg}", style="error")
    
    @staticmethod
    def info(msg: str):
        console.print(f"ℹ {msg}", style="info")
