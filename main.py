import pygame, sys
from settings import *
from level import level
from startScreen import StartScreen
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sporut Land")
        self.clock = pygame.time.Clock()
        self.level = level()
        self.start_screen = StartScreen(self.screen)
        self.state = 'start'

    def run(self):
        while True:
            if self.state == 'start':
                self.handle_start_screen()
            elif self.state == 'running':
                self.handle_gameplay()

    def handle_start_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = self.start_screen.check_events(event)
            if result == 'start_game':
                self.state = 'running'
            elif result == 'exit':
                pygame.quit()
                sys.exit()
        self.start_screen.draw()
        pygame.display.update()

    def handle_gameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dt = self.clock.tick(60) / 1000
        self.level.run(dt)
        pygame.display.update()


if __name__ == "__main__":                                                                           # Oyunu başlatmak ve çalıştırmak için ana başlangıç noktası.
    game = Game()
    game.run()