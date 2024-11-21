from typing import List
import pygame


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        sprites: List[pygame.sprite.Sprite] = self.sprites()
        for sprite in sprites:
            sprite.draw(surface)