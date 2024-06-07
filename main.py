import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from level import Level
from startScreen import StartScreen, LoginScreen, RegistrationScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sporut Land")
        self.clock = pygame.time.Clock()
        self.level = None
        self.start_screen = StartScreen(self.screen)
        self.login_screen = LoginScreen(self.screen)
        self.registration_screen = RegistrationScreen(self.screen)
        self.state = 'start'
        self.user_data = None
        # Müzik ayarları

    def run(self):
        while True:
            if self.state == 'start':
                self.handle_start_screen()
            elif self.state == 'login':
                self.handle_login_screen()
            elif self.state == 'register':
                self.handle_registration_screen()
            elif self.state == 'running':
                self.handle_gameplay()

    def handle_start_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = self.start_screen.check_events(event)
            if result == 'login':
                self.state = 'login'
            elif result == 'register':
                self.state = 'register'
            elif result == 'exit':
                pygame.quit()
                sys.exit()
        self.start_screen.draw()
        pygame.display.update()

    def handle_login_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result, user_data = self.login_screen.check_events(event)
            if result == 'login_success':
                self.user_data = user_data
                self.level = Level(self.user_data)  # Pass user data to level
                self.state = 'running'
        self.login_screen.draw()
        pygame.display.update()

    def handle_registration_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = self.registration_screen.check_events(event)
            if result == 'registered':
                self.state = 'start'
        self.registration_screen.draw()
        pygame.display.update()

    def handle_gameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # 'S' tuşuna basıldığında oyuncu uyur
                self.level.player.sleep()
        dt = self.clock.tick() / 1000
        self.level.run(dt)
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
