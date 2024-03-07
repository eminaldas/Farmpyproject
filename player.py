import pygame
from settings import *
from support import  *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.import_assets()#karakterin bütün pozisyonları için hazırlanan görseller buradan alınıyor
        self.status = 'down_idle'#başlangıçta oyuncunun olması gereken pozisyon
        self.frame_index = 0#oyuncunun başlangıç indexi

    #genel işlemler
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    #hareket özellikleri
        self.direction = pygame.math.Vector2()##
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animations ={
            'up':[],'down':[],'left':[],'right':[],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
            'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
            'right_water':[],'left_water':[],'up_water':[],'down_water':[]
        }
        for animation in self.animations.keys():
            full_path = './graphics/character/'+animation
            self.animations[animation] = import_folder(full_path)

    def animated(self,dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0]+'_idle' #oyuncu animasyon ayarları


    def input(self):
        #burada karakterin hareket etmesi için gerekli işlemler yapılıyor
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x =1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
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
        #fonksiyonlar çağırılıyor
        self.input()
        self.get_status()
        self.move(dt)
        self.animated(dt)
