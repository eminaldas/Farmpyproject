import pygame
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
class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

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

    def water(self,target_pos):
        for soil_sprites in self.soil_sprites.sprites():
            if soil_sprites.rect.collidepoint(target_pos):

                x = soil_sprites.rect.x // TILE_SIZE
                y = soil_sprites.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                pos  = soil_sprites.rect.topleft
                surf = choice(self.water_surf)
                WaterTile(pos  ,surf,[self.all_sprites,self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')
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
