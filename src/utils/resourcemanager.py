from pathlib import Path
from typing import List, TYPE_CHECKING
import pygame
from dataclasses import dataclass, field
from utils import settings
from gameobjects.pipes import Pipe
import random

if TYPE_CHECKING:
    from ..game import Game


@dataclass
class PlayerStyle:
    def __init__(self, PlayerPath: Path) -> None:
        self.PlayerPath: Path = PlayerPath
        self.Retro: PlayerVariation = PlayerVariation(PlayerPath.joinpath("Retro"))
        self.Modern: PlayerVariation = PlayerVariation(PlayerPath.joinpath("Modern"))


class PlayerVariation:
    def __init__(self, PlayerStylePath: Path) -> None:
        self.PlayerStylePath: Path = PlayerStylePath
        self.variation1 = self._load_variation("Bird-1.png")
        self.variation2 = self._load_variation("Bird-2.png")
        self.variation3 = self._load_variation("Bird-3.png")
        self.variation4 = self._load_variation("Bird-4.png")
        self.variation5 = self._load_variation("Bird-5.png")
        self.variation6 = self._load_variation("Bird-6.png")
        self.variation7 = self._load_variation("Bird-7.png")

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
        self.Classic: pygame.Surface = self._load_image("Background1.png")
        self.Modern: pygame.Surface = self._load_image("Background2.png")
        self.City: pygame.Surface = self._load_image("Background3.png")
        self.CityNight: pygame.Surface = self._load_image("Background4.png")
        self.CityNightLight: pygame.Surface = self._load_image("Background5.png")
        self.Dessert: pygame.Surface = self._load_image("Background9.png")

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

    # Pipes
    PIPE_POS: Tuple[int, int] = field(default=(0, 0))
    PIPE_SIZE: Tuple[int, int] = field(
        default=(settings.PIPE_WIDTH, settings.PIPE_HEIGHT)
    )
    PIPE_SCALE: Tuple[int, int] = field(
        default=settings.PIPE_SCALE
    )
    N_PIPES: Tuple[int, int] = field(default=(1, 4))

    # Tiles
    TILE_POS: Tuple[int, int] = field(default=(0, 48))
    TILE_SIZE: Tuple[int, int] = field(default=(settings.TILE_SIZE, settings.TILE_SIZE))
    TILE_SCALE: Tuple[int, int] = field(
        default=settings.TILE_SCALE
    )
    N_TILES: Tuple[int, int] = field(default=(1, 4))

    pipes: List[pygame.Surface] = field(default_factory=list)
    tiles: List[pygame.Surface] = field(default_factory=list)

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
                self.PIPE_SCALE,
            )
            for col in range(self.N_PIPES[1])
            for row in range(self.N_PIPES[0])
        ]

        self.tiles = [
            pygame.transform.scale_by(
                self.image.subsurface(
                    pygame.Rect(
                        (col * self.TILE_SIZE[0]) + self.TILE_POS[0],
                        (row * self.TILE_SIZE[1]) + self.TILE_POS[1],
                        *self.TILE_SIZE
                    )
                ),
                self.TILE_SCALE,
            )
            for col in range(self.N_TILES[1])
            for row in range(self.N_TILES[0])
        ]


class TileStyle:
    BasePath: Path

    @classmethod
    @property
    def Modern(self) -> TileType:
        return TileType(
            BASE_TILE_PATH=self.BasePath,
            Tile_Name="Modern",
            PIPE_SIZE=(32, 80),
            PIPE_SCALE=(3, 2),
            TILE_POS=(0, 80),
            TILE_SIZE=(32, 32),
            TILE_SCALE=(3, 2),
        )

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
        self.tiles = []

    def setTileStyle(self, tile_type: TileType) -> "TileMap":
        self.tile_style = tile_type
        self.pipes = self.tile_style.pipes
        self.tiles = self.tile_style.tiles
        return self

    def draw_pipes(
        self,
        n: int,
        groups: List[pygame.sprite.Group] | pygame.sprite.Group,
        game: "Game",
    ):
        for i in range(n):
            Pipe(game=game, pipes=self.pipes, group=groups, n=i)


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
        self.icon = pygame.image.load(self.assets_folder.joinpath("icon.png"))


if __name__ == "__main__":
    pygame.init()
    disp = pygame.display.set_mode((800, 600))
    rm = ResourceManager()
    print(rm.player_resouce.Modern.variation1)
    print(rm.backgrounds.Classic)
