import pygame
from typing import TYPE_CHECKING, List, Literal
from utils import PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT
import random

if TYPE_CHECKING:
    from ..game import Game


class Pipe(pygame.sprite.Sprite):
    def __init__(
        self,
        game: "Game",
        pipes: List[pygame.Surface],
        pos: tuple[int, int] = (0, 0),
        group: pygame.sprite.Group = None,
        n: int = 0,
        min_gap: int = 50,
    ) -> None:
        super().__init__(group)
        self.game = game
        self.pipevariation = pipes
        self.min_gap = min_gap
        self.n = n
        self.reposition_pipe()

    def update(self, dt) -> None:
        # Move pipes to the left
        self.top_rect.centerx -= PLAYER_SPEED * dt
        self.bot_rect.centerx = self.top_rect.centerx

        # Reposition pipe when it goes off-screen
        if self.top_rect.right < 0:
            self.reposition_pipe()

    def reposition_pipe(self):
        # Create the top pipe
        self.top_image = pygame.transform.scale_by(
            random.choice(self.pipevariation), (1, 3)
        )
        self.bottom_image = pygame.transform.flip(self.top_image, False, True)

        offset = self.n * self.top_image.get_width()
        self.top_rect = self.top_image.get_rect(
            topleft=(
                random.randint(
                    WINDOW_WIDTH,
                    WINDOW_WIDTH + offset,
                ),
                -random.randint(50, 250),
            )
        )

        # Create the bottom pipe
        self.bot_rect = self.bottom_image.get_rect(
            topleft=(
                self.top_rect.left,
                self.top_rect.bottom + random.randint(250, 500),
            )
        )
        gap_scale = random.randint(2, 4)
        for sprite in self.game.collision_sprite:
            while sprite is not self and self.top_rect.inflate(
                self.min_gap * gap_scale, 0
            ).colliderect(sprite.top_rect.inflate(sprite.min_gap * gap_scale, 0)):
                self.top_rect.left += self.min_gap

        self.bot_rect.left = self.top_rect.left
        self.bot_rect.top = self.top_rect.bottom + random.randint(75, 150)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.top_image, self.top_rect)
        surface.blit(self.bottom_image, self.bot_rect)
