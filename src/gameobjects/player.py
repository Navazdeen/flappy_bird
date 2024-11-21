import pygame
from typing import TYPE_CHECKING
from utils import PLAYER_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH, PLAYER_JUMP

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
        self.frame = 0
        self.game = game
        self.direction = pygame.math.Vector2(0, 0)
        self.playervariation = playerstyle.get(type)
        self.image = self.playervariation[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.gravity = 50
        self.jump_speed = 0
        self.current_rotation = 0

    def _handle_movement(self):
        """Handle Key presses and move the player"""
        if self.game.keys_pressed[pygame.K_SPACE]:
            self.jump_speed = -PLAYER_JUMP

    def _move(self, dt):
        self._handle_collisions()
        self.jump_speed += self.gravity
        self.jump_speed = min(self.jump_speed, 150)
        self.rect.centery += self.jump_speed * dt

    def _handle_collisions(self):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.jump_speed = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.jump_speed = 0

    def _animate(self, dt):
        self.frame += 0.25
        if int(self.frame) > len(self.playervariation) - 1:
            self.frame = 0
        self.image = self.playervariation[int(self.frame)]
        rot_speed = 100
        if self.jump_speed == 0:
            self.current_rotation = 0
        elif self.jump_speed > 0:
            if self.current_rotation > 0:
                self.current_rotation = 0
            self.current_rotation = max(self.current_rotation - (rot_speed * dt), -15)
        else:
            self.current_rotation = min(self.current_rotation + (rot_speed * dt), 15)
        self.image = pygame.transform.rotate(self.image, self.current_rotation)

    def update(self, dt) -> None:
        self._handle_movement()
        self._move(dt)
        self._handle_collisions()
        self._animate(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
