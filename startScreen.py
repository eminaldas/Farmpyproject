import pygame
from settings import *


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2, 420, 70)
        self.exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 100, 420, 70)
        self.font = pygame.font.Font(None, 50)
        self.active_btn = None
        self.background_image = pygame.image.load('./graphics/starting/BASLANGIC.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        # Buttons
        for btn in [self.start_btn, self.exit_btn]:
            # Apply hover effect with a darker shade when active
            color = '#f1e8bf' if btn != self.active_btn else '#ffe8c5'
            border_color = '#a47e0b'
            pygame.draw.rect(self.screen, color, btn, border_radius=5)  # Rounded corners
            pygame.draw.rect(self.screen, border_color, btn, 2, 5)  # Slightly larger border radius for a subtle edge effect

            # Button Text
            text = 'OYUNA GİRİŞ' if btn == self.start_btn else 'OYUNDAN ÇIKIŞ'
            text_surf = self.font.render(text, True, border_color)
            self.screen.blit(text_surf, text_surf.get_rect(center=btn.center))

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_btn.collidepoint(event.pos):
                return 'start_game'
            elif self.exit_btn.collidepoint(event.pos):
                return 'exit'
        if event.type == pygame.MOUSEMOTION:
            # Update active button based on mouse position for hover effect
            self.active_btn = self.start_btn if self.start_btn.collidepoint(event.pos) else self.exit_btn if self.exit_btn.collidepoint(event.pos) else None
        return None
