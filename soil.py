from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil,check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f'./graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26,-self.rect.height*0.4)
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True
                print(self.harvestable)

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))


class SoilLayer:
    def __init__(self, all_sprites,collision_sprites):
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        self.soil_surfs = import_folder_dict('./graphics/soil/')
        self.water_surf = import_folder('./graphics/soil_water')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('./graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        offset_x, offset_y = 576 // TILE_SIZE, 576 // TILE_SIZE

        for x, y, _ in load_pygame('./data/map.tmx').get_layer_by_name('Farmable').tiles():
            adjusted_x = x - offset_x
            adjusted_y = y - offset_y
            if 0 <= adjusted_x < h_tiles and 0 <= adjusted_y < v_tiles:
                self.grid[adjusted_y][adjusted_x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE + 576
                    y = index_row * TILE_SIZE + 576
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = (rect.x - 576) // TILE_SIZE
                y = (rect.y - 576) // TILE_SIZE

                if x < len(self.grid[0]) and y < len(self.grid) and 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = (soil_sprite.rect.x - 576) // TILE_SIZE
                y = (soil_sprite.rect.y - 576) // TILE_SIZE
                if 'F' in self.grid[y][x]:  # Check if the soil is farmable
                    self.grid[y][x].append('W')  # Mark the soil as watered
                    pos = (x * TILE_SIZE + 576, y * TILE_SIZE + 576)
                    surf = choice(self.water_surf)
                    WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x = index_col * TILE_SIZE + 576
                    y = index_row * TILE_SIZE + 576
                    WaterTile((x, y), choice(self.water_surf), [self.all_sprites, self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self,pos):
        x = (pos[0] - 576) // TILE_SIZE
        y = (pos[1] - 576) // TILE_SIZE

        cell  = self.grid[y][x]
        is_watered ='W' in cell
        return is_watered

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x =( soil_sprite.rect.x - 576) // TILE_SIZE
                y =( soil_sprite.rect.y - 576) // TILE_SIZE

                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(seed, [self.all_sprites, self.plant_sprites,self.collision_sprites], soil_sprite,self.check_watered)

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    # Check surrounding tiles
                    t = index_row > 0 and 'X' in self.grid[index_row-1][index_col]
                    b = index_row < len(self.grid) - 1 and 'X' in self.grid[index_row+1][index_col]
                    r = index_col < len(row) - 1 and 'X' in row[index_col+1]
                    l = index_col > 0 and 'X' in row[index_col-1]

                    # Determine the tile type based on the surrounding tiles
                    tile_type = self.determine_tile_type(t, b, r, l)

                    # Create and add soil tile
                    SoilTile(pos=(index_col * TILE_SIZE + 576, index_row * TILE_SIZE + 576),
                             surf=self.soil_surfs[tile_type],
                             groups=[self.all_sprites, self.soil_sprites])

    def determine_tile_type(self, t, b, r, l):
        if t and b and r and l:
            return 'x'
        if l and not any((t, r, b)):
            return 'r'
        if r and not any((t, l, b)):
            return 'l'
        if r and l and not any((t, b)):
            return 'lr'
        if t and not any((r, l, b)):
            return 'b'
        if b and not any((r, l, t)):
            return 't'
        if b and t and not any((r, l)):
            return 'tb'
        if l and b and not any((t, r)):
            return 'tr'
        if r and b and not any((t, l)):
            return 'tl'
        if l and t and not any((b, r)):
            return 'br'
        if r and t and not any((b, l)):
            return 'bl'
        if all((t, b, r)) and not l:
            return 'tbr'
        if all((t, b, l)) and not r:
            return 'tbl'
        if all((l, r, t)) and not b:
            return 'lrb'
        if all((l, r, b)) and not t:
            return 'lrt'

        return 'o'
