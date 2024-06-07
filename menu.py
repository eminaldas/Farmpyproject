import pygame
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)

        # options
        self.width = 167
        self.height = 100
        self.space = 0  # No space between cells
        self.padding = 8
        self.cell_radius = 6
        self.grid_rows = 4
        self.grid_cols = 3

        # background
        self.bg_image = pygame.image.load('./graphics/menu/trader.png').convert_alpha()
        self.bg_rect = self.bg_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        # entries
        self.options = list(self.player.item_inventory.keys())
        while len(self.options) < 6:
            self.options.append('Empty')

        self.options += list(self.player.seed_inventory.keys())
        while len(self.options) < 8:  # Make space for scissors
            self.options.append('Empty')

        self.options += ['axe_2', 'axe_3', 'scissors']  # Yeni aletler
        while len(self.options) < 12:
            self.options.append('Empty')

        self.sell_border = 5  # First 6 are for selling

        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
        # load images
        self.images = {}
        for item in self.options:
            if item != 'Empty':
                if item in self.player.item_inventory:
                    image_path = f'./graphics/trader/sell/{item}.png'
                else:
                    image_path = f'./graphics/trader/buy/{item}.png'
                self.images[item] = pygame.image.load(image_path).convert_alpha()

        # create the text surfaces
        self.text_surfs = {}
        for item in self.options:
            if item != 'Empty':
                if item in self.player.item_inventory:
                    price = SALE_PRICES[item]
                else:
                    price = PURCHASE_PRICES[item]
                self.text_surfs[item] = self.font.render(f'{price}', False, 'Black')

        self.menu_left = self.bg_rect.left + 103
        self.menu_top = self.bg_rect.top + 80

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= self.grid_cols
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += self.grid_cols
                self.timer.activate()

            if keys[pygame.K_LEFT]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_RIGHT]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # get item
                current_item = self.options[self.index]

                # sell
                if current_item != 'Empty' and self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

                # buy
                elif current_item != 'Empty' and self.index > self.sell_border:
                    price = PURCHASE_PRICES[current_item]
                    if self.player.money >= price:
                        self.player.money -= price
                        if current_item in self.player.seed_inventory:
                            self.player.seed_inventory[current_item] += 1
                        elif current_item.startswith('axe') or current_item == 'scissors':
                            if current_item == 'scissors':
                                if current_item not in self.player.tools:
                                    self.player.tools.append(current_item)
                            else:
                                if current_item != 'scissors' and 'axe' in self.player.tools:
                                    self.player.tools.remove('axe')
                                self.player.tools.append(current_item)
                            self.player.selected_tool = current_item

        # clamp the values
        self.index = max(0, min(self.index, len(self.options) - 1))

    def show_entry(self, item, top_left, selected):
        # background
        bg_rect = pygame.Rect(top_left[0], top_left[1], self.width, self.height)
        # No background fill to make it transparent

        # image or empty text
        if item != 'Empty':
            image = self.images[item]
            image_rect = image.get_rect(midtop=(bg_rect.centerx, bg_rect.top + 10))
            self.display_surface.blit(image, image_rect)

            # price
            price_surf = self.text_surfs[item]
            price_rect = price_surf.get_rect(midbottom=(bg_rect.centerx, bg_rect.bottom - 10))
            self.display_surface.blit(price_surf, price_rect)
        else:
            empty_surf = self.font.render('Empty', False, 'Black')
            empty_rect = empty_surf.get_rect(center=bg_rect.center)
            self.display_surface.blit(empty_surf, empty_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, self.cell_radius)

    def update(self):
        self.input()
        self.display_surface.blit(self.bg_image, self.bg_rect)
        self.display_money()

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                cell_index = row * self.grid_cols + col
                if cell_index < len(self.options):
                    item = self.options[cell_index]
                    top_left = (self.menu_left + col * self.width,
                                self.menu_top + row * self.height)
                    self.show_entry(item, top_left, self.index == cell_index)
