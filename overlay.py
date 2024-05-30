import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        # General settings and surface initialization
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # Setup for tools and seeds
        overlay_path = './graphics/overlay/'
        self.tools_surf = {
            'hoe': pygame.image.load(f'{overlay_path}hoe.png').convert_alpha(),
            'axe': pygame.image.load(f'{overlay_path}axe.png').convert_alpha(),
            'axe_2': pygame.image.load(f'{overlay_path}axe_2.png').convert_alpha(),  # or axe_2.png if different image
            'axe_3': pygame.image.load(f'{overlay_path}axe_3.png').convert_alpha(),  # or axe_3.png if different image
            'water': pygame.image.load(f'{overlay_path}water.png').convert_alpha()
        }
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

        # Inventory display settings
        self.tool_size = 70
        self.bar_color = pygame.Color("#f1e8bf")
        self.border_color = pygame.Color("#a47e0b")
        self.selected_color = pygame.Color("#a47e0b")

        # Load inventory item graphics
        self.item_images = {item: pygame.image.load(f'./graphics/fruit/{item}.png').convert_alpha()
                            for item in player.item_inventory.keys()}
        self.font = pygame.font.Font(None, 40)

    def draw_tools(self):
        y_offset = SCREEN_HEIGHT - 3 * self.tool_size
        for index, tool in enumerate(self.player.tools):
            rect = pygame.Rect(10, y_offset + index * self.tool_size, self.tool_size, self.tool_size)
            pygame.draw.rect(self.display_surface, self.bar_color, rect)
            if index == self.player.tool_index:
                pygame.draw.rect(self.display_surface, self.selected_color, rect)
                self.tool_text = tool.upper()  # Update tool name on select
                self.text_alpha = 255  # Reset text alpha for fade effect
            pygame.draw.rect(self.display_surface, self.border_color, rect, 2, 5)
            tool_surf = self.tools_surf[tool]
            self.display_surface.blit(tool_surf, tool_surf.get_rect(center=rect.center))

    def draw_seeds(self):
        y_offset = SCREEN_HEIGHT - 6 * self.tool_size
        for index, seed in enumerate(self.player.seeds):
            rect = pygame.Rect(10, y_offset + index * self.tool_size, self.tool_size, self.tool_size)
            pygame.draw.rect(self.display_surface, self.bar_color, rect)
            if index == self.player.seeds_index:
                pygame.draw.rect(self.display_surface, self.selected_color, rect)
            pygame.draw.rect(self.display_surface, self.border_color, rect, 2, 5)
            seed_surf = self.seeds_surf[seed]
            self.display_surface.blit(seed_surf, seed_surf.get_rect(center=rect.center))

    def display_text(self):
        if self.tool_text:
            text_surf = self.font.render(self.tool_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            text_surf.set_alpha(self.text_alpha)
            self.display_surface.blit(text_surf, text_rect)

            self.text_alpha = max(0, self.text_alpha - 5)

    def draw_inventory(self):
        total_width = len(self.player.item_inventory) * self.tool_size
        start_x = (SCREEN_WIDTH - total_width) // 2
        y_pos = SCREEN_HEIGHT - self.tool_size - 20

        # envanter kutuları çizimi
        for index, (item, count) in enumerate(self.player.item_inventory.items()):
            x_pos = start_x + index * self.tool_size
            rect = pygame.Rect(x_pos, y_pos, self.tool_size, self.tool_size)
            pygame.draw.rect(self.display_surface, self.bar_color, rect)
            pygame.draw.rect(self.display_surface, self.border_color, rect, 2, 5)

            # görselleri ekle
            item_image = self.item_images[item]
            self.display_surface.blit(item_image, item_image.get_rect(
                center=(x_pos + self.tool_size // 2, y_pos + self.tool_size // 2)))

            # Draw the quantity text below the item
            quantity_text = self.font.render(str(count), True, (164, 126, 11))
            text_rect = quantity_text.get_rect(center=(x_pos + self.tool_size // 2, y_pos + self.tool_size))
            self.display_surface.blit(quantity_text, text_rect)

    def display(self):
        self.draw_tools()
        self.draw_seeds()
        self.display_text()
        self.draw_inventory()
