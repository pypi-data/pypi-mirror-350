from pyfiglet import figlet_format
from typing import Any as Banner

def create_banner(text: str, font: str) -> Banner:

    _banner = figlet_format(text, font = font)

    return _banner
