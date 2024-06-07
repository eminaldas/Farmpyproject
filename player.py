import pygame
from settings import *
from support import import_folder
from timer import Timer
from sprites import Tree
from datetime import datetime, timedelta  # Bu satırı ekleyin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, user_data):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Genel ayarlar
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # Hareket ayarları
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 600

        # Çarpışmalar
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        # Sayaçlar
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        # Aletler
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Tohumlar
        self.seeds = ['corn', 'tomato']
        self.seeds_index = 0
        self.selected_seed = self.seeds[self.seeds_index]

        # Envanter
        self.item_inventory = {'wood': 0, 'apple': 0, 'corn': 0, 'tomato': 0}
        self.seed_inventory = {'corn': 5, 'tomato': 5}
        self.money = 200

        # Etkileşimler
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        # Kullanıcı verileri
        self.user_data = user_data

        # Ses dosyaları
        pygame.mixer.init()
        self.hoe_sounds = [pygame.mixer.Sound(f'./data/Sounds/Hoe/hoe_sound_{i}.mp3') for i in range(1, 5)]
        self.axe_sounds = [pygame.mixer.Sound(f'./data/Sounds/Axe/axe_sound_{i}.mp3') for i in range(1, 5)]
        self.water_sounds = [pygame.mixer.Sound(f'./data/Sounds/Water/water_sound_1.mp3')]
        self.footstep_sounds = [pygame.mixer.Sound(f'./data/Sounds/Grass/Grass_hit{i}.mp3') for i in range(1, 5)]
        self.scissors_sounds = [pygame.mixer.Sound(f'./data/Sounds/Scissors/Scissors_sound1.ogg')]
        self.footstep_sound_index = 0
        self.footstep_timer = Timer(200)

        self.user_data = user_data
        self.game_time = datetime(year=1, month=1, day=1, hour=6)

        self.current_sound = None
        self.sound_zones = None

        # Ses indeksleri
        self.hoe_sound_index = 0
        self.axe_sound_index = 0
        self.water_sound_index = 0
        self.scissors_sound_index = 0
    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
            'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
            'right_scissors': [], 'left_scissors': [], 'up_scissors': [], 'down_scissors': [],
            'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []
        }
        for animation in self.animations.keys():
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
            self.hoe_sounds[self.hoe_sound_index].play()
            self.hoe_sound_index = (self.hoe_sound_index + 1) % len(self.hoe_sounds)
        elif 'axe' in self.selected_tool:
            damage = 1
            if self.selected_tool == 'axe_2':
                damage = 5
            elif self.selected_tool == 'axe_3':
                damage = 8
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos) and isinstance(tree, Tree):
                    tree.damage(damage)
                    self.axe_sounds[self.axe_sound_index].play()
                    self.axe_sound_index = (self.axe_sound_index + 1) % len(self.axe_sounds)
        elif self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.water_sounds[self.water_sound_index].play()
            self.water_sound_index = (self.water_sound_index + 1) % len(self.water_sounds)
        elif self.selected_tool == 'scissors':
            self.scissors_sounds[self.scissors_sounds_index].play()
            self.scissors_sounds_index = (self.scissors_sounds_index + 1) % len(self.scissors_sounds)
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos) and isinstance(tree, Tree):
                    tree.damage()

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        self.soil_layer.plant_seed(self.target_pos, self.selected_seed)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.timers['tool use'].active:
            tool_type = 'axe' if 'axe' in self.selected_tool else self.selected_tool
            self.status = self.status.split('_')[0] + '_' + tool_type

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
        self.footstep_timer.update()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active and not self.sleep:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if self.direction.magnitude() != 0 and not self.footstep_timer.active:
                self.footstep_sounds[self.footstep_sound_index].play()
                self.footstep_sound_index = (self.footstep_sound_index + 1) % len(self.footstep_sounds)
                self.footstep_timer.activate()

            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seeds_index += 1
                self.seeds_index = self.seeds_index if self.seeds_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seeds_index]

            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite and collided_interaction_sprite[0].name == 'Trader':
                    self.toggle_shop()
                else:
                    self.status = 'left_idle'
                    self.sleep = True

    def check_sound_zones(self, sound_zones):
        if self.sound_zones is None:
            self.sound_zones = sound_zones

        for zone in self.sound_zones:
            if zone['rect'].colliderect(self.hitbox):
                if self.current_sound != zone['sound']:
                    self.current_sound = zone['sound']
                    self.change_footstep_sound(self.current_sound)
                return

        # Eğer hiçbir ses bölgesinde değilse
        if self.current_sound != 'Grass':
            self.current_sound = 'Grass'
            self.change_footstep_sound(self.current_sound)

    def change_footstep_sound(self, sound):
        if sound == 'wood':
            self.footstep_sounds = [pygame.mixer.Sound(f'./data/Sounds/Wood/wood_hit{i}.mp3') for i in range(1, 5)]
        else:
            self.footstep_sounds = [pygame.mixer.Sound(f'./data/Sounds/Grass/Grass_hit{i}.mp3') for i in range(1, 5)]

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)

    def update_game_time(self, dt):
        self.game_time += timedelta(seconds=dt)
