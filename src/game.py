import sys
import pygame
from pygame import math as pygame_math
from utils import settings
from utils.resourcemanager import ResourceManager, TileMap
from gameobjects.player import Player
import math
from utils.group import CustomGroup

pygame.init()


class Game:
    def __init__(self) -> None:
        self.dt: float = 0
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.resourcemanager = ResourceManager()
        self._mouse_pos = pygame.mouse.get_pos()
        self.all_sprite = CustomGroup()
        self.collision_sprite = pygame.sprite.Group()
        self.setup()

    def setup(self):
        self.player = Player(
            self,
            self.resourcemanager.player_resouce.Modern,
            type="variation1",
            pos=(settings.WINDOW_WIDTH // 2 - 200, settings.WINDOW_HEIGHT // 2),
            group=self.all_sprite,
        )
        self.tile_map = self.resourcemanager.tilemap.setTileStyle(
            TileMap.TILE_STYLE.Modern
        )
        self.tile_map.draw_pipes(
            n=115, groups=[self.all_sprite, self.collision_sprite], game=self
        )

    @property
    def mouse_pos(self):
        return pygame_math.Vector2(self._mouse_pos)

    def run(self):
        while self.running:
            self._mouse_pos = pygame.mouse.get_pos()
            self.keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(
                self.resourcemanager.backgrounds.Retro,
                (0, 0),
            )
            self.all_sprite.update(self.dt)
            self.all_sprite.draw(self.screen)
            pygame.display.update()
            self.dt = self.clock.tick(settings.FPS) / 1000


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
