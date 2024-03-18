import  pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic

class level:
    def __init__(self):
                                                                                #get the display surface
        self.display_surface = pygame.display.get_surface()

                                                                                #sprite group
        self.all_sprites = CameraGroup()
                                                                                #tüm canlıların çilmiesinde kolaylık sağlar
        self.setup()
        self.overlay = Overlay(self.player)
    def setup(self):
        self.player = Player((640,360),self.all_sprites)                   #oyuncunun konumunu ekranda belirtip çiziyor
        Generic(pos =(0,0),
                surf = pygame.image.load('./graphics/world/ground.png'),
                groups = self.all_sprites,
                z = LAYERS['ground']
                )


    def run(self,dt):
        self.display_surface.fill('black')                                      #ekran arka plana verilen renk
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        #ekran yenilenirken güncellenmesi
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)