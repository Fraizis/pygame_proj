from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Settings:
    height: int = 800
    width: int = 600
    game_name: str = 'Snake'
    icon_path: str = 'snake_img.png'


@dataclass
class GameMod:
    game_started: bool = False
    end_game: bool = False
    running: bool = True
    pause: bool = False


@dataclass
class Color:
    background: ClassVar[dict[str, tuple]] = {
        'blue': (135, 206, 250),
        'light_blue': (76, 166, 204),
        'purple': (66, 28, 161),
        'light_green': (121, 246, 157),
        'orange': (242, 58, 28),
        'yellow': (255, 255, 0),
        'white': (255, 255, 255),
        'grey': (225, 225, 225),
    }
