import pygame, sys
from settings import *
from level import level
class Game:
    def __init__(self):                                                         #sınıfa girdiğimizde başlaması için tanımladık
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    #ekranın boyutların girdik
        pygame.display.set_caption("sporut land")
        self.clock = pygame.time.Clock()                                        #oyunun FPS ayarı buradan yapılıyor
        self.level = level()
    def run(self):                                                              #oyunun başladığı kısım
        while True:                                                             #oyunun sonsuz dönküye girmesi için
            for event in pygame.event.get():                                    #burada pygame içindeki işlemleri event içine atılıyor
                if event.type == pygame.QUIT:                                   #burada quit kısmına basıldığında gerçekleşen işlemler
                    pygame.quit()                                               #pygame kütüphaneden çıkış işlemi
                    exit(1)                                                     #uygulamayı kapatma işlemi
            dt = self.clock.tick()/1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == "__main__":
                                                                                # Oyunu başlatmak ve çalıştırmak için ana başlangıç noktası.
    game = Game()
    game.run()