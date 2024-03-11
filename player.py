import pygame
from settings import *
from support import  *
from timer import Timer

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

        #Timers
        self.timers = {
            'tool use' : Timer(350,self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }
        #Aletler
        self.tools = ['hoe','axe','water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #tohumlar
        self.seeds = ['corn','tomato']
        self.seeds_index = 0
        self.selected_seed = self.seeds[self.seeds_index]

    def use_tool(self):
        pass
    def use_seed(self):
        pass
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

        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    def input(self):
        #burada karakterin hareket etmesi için gerekli işlemler yapılıyor
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active:
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
            #aletlerin kullanımı
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #aletler arası geçiş
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

                # tohumların kullanımı
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #tohumlar arası geçiş
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seeds_index+=1
                self.seeds_index = self.seeds_index if self.seeds_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seeds_index]
                print(self.selected_seed)

    def move(self,dt):

        if self.direction.magnitude() > 0:                              #vektör çapraz harektlerde normalinden daha hızlı->
            self.direction = self.direction.normalize()                 #->gitmesini engellemek için

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
        self.update_timers()

        self.move(dt)
        self.animated(dt)

