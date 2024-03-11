import  pygame
from settings import *
from player import Player
from overlay import Overlay

class level:
    def __init__(self):
                                                                                #get the display surface
        self.display_surface = pygame.display.get_surface()

                                                                                #sprite group
        self.all_sprites = pygame.sprite.Group()
                                                                                #tüm canlıların çilmiesinde kolaylık sağlar
        self.setup()
        self.overlay = Overlay(self.player)
    def setup(self):
        self.player = Player((640,360),self.all_sprites)                   #oyuncunun konumunu ekranda belirtip çiziyor


    def run(self,dt):
        self.display_surface.fill('black')                                      #ekran arka plana verilen renk
        self.all_sprites.draw(self.display_surface)                             #oyuncunun ekrana çizilmesi
        self.all_sprites.update(dt)                                             #ekran yenilenirken güncellenmesi