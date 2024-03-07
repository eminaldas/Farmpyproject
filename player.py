import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

    #genel işlemler
        self.image = pygame.Surface((32,64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)

    #hareket özellikleri
        self.direction = pygame.math.Vector2()##
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animation ={
            'up':[],'down':[],'left':[],'right':[],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
            'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
            'right_water':[],'left_water':[],'up_water':[],'down_water':[]
        }
        for animation in self.animation.keys():
            full_path = './images/graphics/Characters/'+animation
            self.animation[animation] = import_folder(full_path)

    def input(self):
        #burada karakterin hareket etmesi için gerekli işlemler yapılıyor
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x =1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0


    def move(self,dt):

        if self.direction.magnitude() > 0:#vektör çapraz harektlerde normalinden daha hızlı->
            self.direction = self.direction.normalize()#->gitmesini engellemek için

        #yatay hareket
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        #dikey hareket

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self,dt):
        self.input()
        self.move(dt)