import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle, Trader
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from datetime import datetime, timedelta

class Level:
    def __init__(self, user_data):
        self.user_data = user_data
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False
        self.user_photo_size = 50 * 4
        self.user_photo = pygame.transform.scale(pygame.image.load(
            f'./data/Avatars/{self.user_data["gender"]}/{self.user_data["gender"]}_{self.user_data["photo"] + 1}.png'),
                                                 (self.user_photo_size, self.user_photo_size))
        self.user_font = pygame.font.Font(None, 36)
        self.time_scale = 86400 / 300  # 24 saat = 86400 saniye, 5 dakika = 300 saniye

    def setup(self):
        tmx_data = load_pygame('./data/map.tmx')
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        water_frames = import_folder('./graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)



        for obj in tmx_data.get_layer_by_name('Objects'):
            Trader((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        for layer in ['Hills']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['Hills'])

        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
        for obj in tmx_data.get_layer_by_name('Trees'):
            tree_name = obj.name if obj.name in ['Small', 'Large'] else None
            if tree_name:
                Tree(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                    name=tree_name,
                    player_add=self.player_add)
            else:
                print(f"Warning: Tree object at ({obj.x}, {obj.y}) has an invalid name: {obj.name}")
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop)
            elif obj.name == "Bed":
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
            elif obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
            elif obj.name == 'Coni':
                Generic((obj.x, obj.y), obj.image, self.all_sprites, LAYERS['main'])

        Generic(
            pos=(0, 0),
            surf=pygame.image.load('./graphics/world/map.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def reset(self):
        self.soil_layer.update_plants()
        self.soil_layer.remove_water()
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()
        for tree in self.tree_sprites.sprites():
            if isinstance(tree, Tree):
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()
        self.sky.start_color = [255, 255, 255]

    def plant_collisions(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    self.soil_layer.grid[(plant.rect.centery - 576) // TILE_SIZE][
                        (plant.rect.centerx - 576) // TILE_SIZE].remove('P')

    def draw_user_info(self):
        self.display_surface.blit(self.user_photo, (SCREEN_WIDTH - self.user_photo_size - 10, 10))
        username_surf = self.user_font.render(self.user_data['username'], True, '#000000')
        self.display_surface.blit(username_surf, (SCREEN_WIDTH - self.user_photo_size - 20 - username_surf.get_width(), 20))

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collisions()
        self.overlay.display()
        if self.raining and not self.shop_active:
            self.rain.update()
        self.sky.display(dt)
        if self.player.sleep:
            self.transition.play()
        self.draw_user_info()
        self.player.update_game_time(dt * self.time_scale)
        self.update_day_cycle()

    def update_day_cycle(self):
        current_hour = self.player.game_time.hour
        current_minute = self.player.game_time.minute
        current_second = self.player.game_time.second
        total_seconds = current_hour * 3600 + current_minute * 60 + current_second

        # Gündüz (05:00 - 17:00)
        if 5 * 3600 <= total_seconds < 17 * 3600:
            self.sky.start_color = pygame.Color(255, 255, 255, 0)  # Şeffaf
        # Gün batımı (17:00 - 19:00)
        elif 17 * 3600 <= total_seconds < 19 * 3600:
            sunset_progress = (total_seconds - 17 * 3600) / (
                        2 * 3600)  # 17:00 ile 19:00 arasında %0 ile %100 arası ilerleme
            color_value = int(38 * (1 - sunset_progress))
            alpha_value = int(255 * sunset_progress * 0.65)  # %65 opaklık
            self.sky.start_color = pygame.Color(38, 101, 189, alpha_value)  # Lacivert rengi ile opaklık
        # Gece (19:00 - 05:00)
        elif 19 * 3600 <= total_seconds or total_seconds < 5 * 3600:
            self.sky.start_color = pygame.Color(38, 101, 189, int(255 * 0.65))  # %65 opaklık ile lacivert
        # Gün doğumu (05:00 - 06:00)
        elif 5 * 3600 <= total_seconds < 6 * 3600:
            sunrise_progress = (total_seconds - 5 * 3600) / (
                        1 * 3600)  # 05:00 ile 06:00 arasında %0 ile %100 arası ilerleme
            color_value = int(38 * sunrise_progress)
            alpha_value = int(255 * (1 - sunrise_progress) * 0.65)  # %65 opaklık
            self.sky.start_color = pygame.Color(38, 101, 189, alpha_value)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
