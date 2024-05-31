import pygame
from settings import *
from random import randint, choice
from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

class Water(Generic):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        super().__init__(
            pos=pos,
            surf=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration=200, moving=False):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(randint(-2, 2), -3)
            self.speed = randint(50, 100)

    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)
        self.health = 20
        self.alive = True
        stump_path = f'./graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)
        self.apple_surf = pygame.image.load('./graphics/fruit/apple.png')

        print(f"Initializing Tree with name: {name}")

        # Ensure name is either 'Small' or 'Large'
        if name not in APPLE_POS:
            raise ValueError(f"Invalid tree name: {name}")

        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()
        self.player_add = player_add

    def create_fruit(self):
        if self.alive:
            for pos in self.apple_pos:
                if randint(0, 10) < 2:
                    x = pos[0] + self.rect.left
                    y = pos[1] + self.rect.top
                    Generic(
                        pos=(x, y),
                        surf=self.apple_surf,
                        groups=[self.apple_sprites, self.groups()],
                        z=LAYERS['fruit'])

    def damage(self, amount=0):
        self.health -= amount
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos=random_apple.rect.topleft,
                surf=random_apple.image,
                groups=self.groups(),
                z=LAYERS['fruit'],
                duration=300,
                moving=True)
            self.player_add('apple')
            random_apple.kill()

        self.check_death()

    def check_death(self):
        if self.health <= 0 and self.alive:
            Particle(
                pos=self.rect.topleft,
                surf=self.image,
                groups=self.groups(),
                z=LAYERS['fruit'],
                duration=300,
                moving=False)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)

            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        self.invul_timer.update()
