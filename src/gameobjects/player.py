import pygame
from typing import TYPE_CHECKING
from utils import PLAYER_SPEED

if TYPE_CHECKING:
    from ..game import Game
    from ..utils import resourcemanager


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        game: "Game",
        playerstyle: "resourcemanager.PlayerVariation",
        type: str = "variation1",
        pos=(0, 0),
        group: pygame.sprite.Group = None,
    ) -> None:
        super().__init__(group)
        self.game = game
        self.direction = pygame.math.Vector2(0, 0)
        self.playervariation = playerstyle.get(type)
        self.image = self.playervariation[0]
        self.rect = self.image.get_rect(center=pos)

    def _handle_movement(self):
        """Handle Key presses and move the player"""
        if self.game.keys_pressed[pygame.K_w]:
            self.direction.y = -1
        elif self.game.keys_pressed[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.game.keys_pressed[pygame.K_a]:
            self.direction.x = -1
        elif self.game.keys_pressed[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def _handle_collisions(self):
        pass

    def _move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self._handle_collisions()
        self.rect.center += self.direction * PLAYER_SPEED * dt

    def update(self, dt) -> None:
        self._handle_movement()
        self._move(dt)
