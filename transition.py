import pygame
from settings import *

class Transition:
    def __init__(self, reset, player):
        # setup kısmı
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 155
        self.speed = -2

    def play(self):
        self.color += self.speed
        if self.color <= 80:
            self.speed *= -1
            self.color = 80
            self.reset()
            self.player.game_time = self.player.game_time.replace(hour=6, minute=0, second=0)

        if self.color > 155:
            self.color = 155
            self.player.sleep = False
            self.speed = -2
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
