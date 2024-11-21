from pathlib import Path
from typing import Any, Dict, List
import pygame
from dataclasses import dataclass, field
from utils import settings
from functools import lru_cache


@dataclass
class PlayerStyle:
    def __init__(self, PlayerPath: Path) -> None:
        self.PlayerPath: Path = PlayerPath
        self.Modern: PlayerVariation = PlayerVariation(PlayerPath.joinpath("Modern"))
        self.Retro: PlayerVariation = PlayerVariation(PlayerPath.joinpath("Retro"))


class PlayerVariation:
    def __init__(self, PlayerStylePath: Path) -> None:
        self.PlayerStylePath: Path = PlayerStylePath
        self.variation1 = self._load_variation("Bird-1.png")

    def _load_variation(self, variation: str) -> List[pygame.Surface]:
        sprite = pygame.image.load(
            self.PlayerStylePath.joinpath(variation), variation
        ).convert_alpha()
        # splte the surface into 16 x 16 sprites
        sprite = [
            pygame.transform.scale_by(
                sprite.subsurface(
                    pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE)
                ),
                settings.PLAYER_SCALE,
            )
            for y in range(0, sprite.get_height(), settings.TILE_SIZE)
            for x in range(0, sprite.get_width(), settings.TILE_SIZE)
        ]
        return sprite

    def get(self, __name: str) -> List[pygame.Surface]:
        return getattr(self, __name)


@dataclass
class BackgroundStyle:
    def __init__(self, BackgroundPath: Path) -> None:
        self.BackgroundPath: Path = BackgroundPath
        self.Modern: pygame.Surface = self._load_image("Background1.png")
        self.Retro: pygame.Surface = self._load_image("Background1.png")

    def _load_image(self, image: str) -> pygame.Surface:
        return pygame.transform.scale(
            pygame.image.load(self.BackgroundPath.joinpath(image)).convert_alpha(),
            settings.WINDOW_SIZE,
        )


from typing import List, Tuple
import pygame


@dataclass
class TileType:
    BASE_TILE_PATH: Path
    Tile_Name: str

    TILE_POS: Tuple[int, int] = field(default=(0, 2 * settings.TILE_SIZE))
    TILE_SIZE: Tuple[int, int] = field(default=(settings.TILE_SIZE, settings.TILE_SIZE))
    N_TILES: Tuple[int, int] = field(default=(1, 4))

    PIPE_POS: Tuple[int, int] = field(default=(0, 0))
    PIPE_SIZE: Tuple[int, int] = field(
        default=(settings.PIPE_WIDTH, settings.PIPE_HEIGHT)
    )
    N_PIPES: Tuple[int, int] = field(default=(1, 4))
    pipes: List[pygame.Surface] = field(default_factory=list)

    def __post_init__(self):
        self.image = pygame.image.load(
            self.BASE_TILE_PATH.joinpath(self.Tile_Name, "basetiles.png")
        ).convert_alpha()

        self.pipes = [
            pygame.transform.scale_by(
                self.image.subsurface(
                    pygame.Rect(
                        (col * self.PIPE_SIZE[0]) + self.PIPE_POS[0],
                        (row * self.PIPE_SIZE[1]) + self.PIPE_POS[1],
                        *self.PIPE_SIZE
                    )
                ),
                settings.PIPE_SCALE,
            )
            for col in range(self.N_PIPES[1])
            for row in range(self.N_PIPES[0])
        ]


class TileStyle:
    BasePath: Path

    @classmethod
    @property
    def Modern(self) -> TileType:
        return TileType(BASE_TILE_PATH=self.BasePath, Tile_Name="Modern")

    @classmethod
    @property
    def Classic(self) -> TileType:
        return TileType(BASE_TILE_PATH=self.BasePath, Tile_Name="Classic")


class TileMap:
    TILE_STYLE = TileStyle

    def __init__(self, tile_path: Path) -> None:
        self._tile_path = tile_path
        self.TILE_STYLE.BasePath = self._tile_path
        self.tile_style = None
        self.pipes = []

    def setTileStyle(self, tile_type: TileType) -> "TileMap":
        self.tile_style = tile_type
        self.pipes = self.tile_style.pipes
        return self


class ResourceManager:
    _Here = Path(__file__).parent.resolve()

    def __init__(self) -> None:
        self.assets_folder = self._Here.parent.resolve().joinpath("assets")
        self.player_resouce = PlayerStyle(
            PlayerPath=self.assets_folder.joinpath("Player")
        )
        self.backgrounds = BackgroundStyle(
            BackgroundPath=self.assets_folder.joinpath("Background")
        )
        self.tilemap = TileMap(self.assets_folder.joinpath("Tiles"))


if __name__ == "__main__":
    pygame.init()
    disp = pygame.display.set_mode((800, 600))
    rm = ResourceManager()
    print(rm.player_resouce.Modern.variation1)
    print(rm.backgrounds.Modern)
