import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pymongo import MongoClient
from datetime import datetime

# MongoDB'ye bağlanma
client = MongoClient("mongodb://localhost:27017/")
db = client.gameDatabase
users_collection = db.users

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2-55, 420, 70)
        self.register_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 +45, 420, 70)
        self.exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 145, 420, 70)
        self.font = pygame.font.Font(None, 50)
        self.active_btn = None
        self.background_image = pygame.image.load('./graphics/starting/BASLANGIC.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        for btn in [self.start_btn, self.register_btn, self.exit_btn]:
            color = '#f1e8bf' if btn != self.active_btn else '#ffe8c5'
            border_color = '#a47e0b'
            pygame.draw.rect(self.screen, color, btn, border_radius=5)
            pygame.draw.rect(self.screen, border_color, btn, 2, 5)

            if btn == self.start_btn:
                text = 'OYUNA GİRİŞ'
            elif btn == self.register_btn:
                text = 'KAYIT OL'
            else:
                text = 'OYUNDAN ÇIKIŞ'
            text_surf = self.font.render(text, True, border_color)
            self.screen.blit(text_surf, text_surf.get_rect(center=btn.center))

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_btn.collidepoint(event.pos):
                return 'login'
            elif self.register_btn.collidepoint(event.pos):
                return 'register'
            elif self.exit_btn.collidepoint(event.pos):
                return 'exit'
        if event.type == pygame.MOUSEMOTION:
            self.active_btn = (
                self.start_btn if self.start_btn.collidepoint(event.pos) else
                self.register_btn if self.register_btn.collidepoint(event.pos) else
                self.exit_btn if self.exit_btn.collidepoint(event.pos) else None
            )
        return None

class RegistrationScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        self.username_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 50)
        self.password_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70, 300, 50)
        self.gender_box_male = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, 140, 40)
        self.gender_box_female = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 30, 140, 40)
        self.register_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 240, 300, 50)
        self.photo_boxes = [pygame.Rect(SCREEN_WIDTH // 2 - 300 + i * 120, SCREEN_HEIGHT // 2 + 140, 100, 100) for i in range(5)]
        self.username = ''
        self.password = ''
        self.gender = 'male'
        self.selected_photo = None
        self.active_box = None
        self.photos = {
            'male': [pygame.image.load(f'./data/Avatars/male/male_{i}.png') for i in range(1, 6)],
            'female': [pygame.image.load(f'./data/Avatars/female/female_{i}.png') for i in range(1, 6)]
        }
        self.resized_photos = {
            'male': [pygame.transform.scale(photo, (100, 100)) for photo in self.photos['male']],
            'female': [pygame.transform.scale(photo, (100, 100)) for photo in self.photos['female']]
        }

    def draw(self):
        self.screen.fill('#f1e8bf')
        pygame.draw.rect(self.screen, '#a47e0b', self.username_box, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.password_box, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.gender_box_male, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.gender_box_female, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.register_btn, 2)

        username_surf = self.font.render(self.username, True, '#000000')
        password_surf = self.font.render('*' * len(self.password), True, '#000000')
        self.screen.blit(username_surf, (self.username_box.x + 10, self.username_box.y + 10))
        self.screen.blit(password_surf, (self.password_box.x + 10, self.password_box.y + 10))

        gender_text_male = self.font.render('Erkek', True, '#000000')
        gender_text_female = self.font.render('Kadın', True, '#000000')
        self.screen.blit(gender_text_male, (self.gender_box_male.x + 10, self.gender_box_male.y + 5))
        self.screen.blit(gender_text_female, (self.gender_box_female.x + 10, self.gender_box_female.y + 5))

        if self.gender == 'male':
            pygame.draw.circle(self.screen, '#000000', (self.gender_box_male.x + 120, self.gender_box_male.y + 20), 10)
        else:
            pygame.draw.circle(self.screen, '#000000', (self.gender_box_female.x + 120, self.gender_box_female.y + 20), 10)

        for i, photo_box in enumerate(self.photo_boxes):
            pygame.draw.rect(self.screen, '#a47e0b', photo_box, 2)
            self.screen.blit(self.resized_photos[self.gender][i], (photo_box.x, photo_box.y))
            if self.selected_photo == i:
                pygame.draw.rect(self.screen, '#00ff00', photo_box, 4)

        register_text = self.font.render('KAYIT OL', True, '#000000')
        self.screen.blit(register_text, register_text.get_rect(center=self.register_btn.center))

        self.screen.blit(self.small_font.render('Kullanıcı Adı:', True, '#000000'), (self.username_box.x, self.username_box.y - 30))
        self.screen.blit(self.small_font.render('Şifre:', True, '#000000'), (self.password_box.x, self.password_box.y - 30))
        self.screen.blit(self.small_font.render('Cinsiyet:', True, '#000000'), (self.gender_box_male.x, self.gender_box_male.y - 35))
        self.screen.blit(self.small_font.render('Fotoğraf Seçimi:', True, '#000000'), (self.photo_boxes[0].x, self.photo_boxes[0].y - 40))
        pygame.display.flip()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_box.collidepoint(event.pos):
                self.active_box = self.username_box
            elif self.password_box.collidepoint(event.pos):
                self.active_box = self.password_box
            elif self.gender_box_male.collidepoint(event.pos):
                self.gender = 'male'
            elif self.gender_box_female.collidepoint(event.pos):
                self.gender = 'female'
            elif self.register_btn.collidepoint(event.pos):
                self.save_user()
                return 'registered'
            for i, photo_box in enumerate(self.photo_boxes):
                if photo_box.collidepoint(event.pos):
                    self.selected_photo = i
        if event.type == pygame.KEYDOWN:
            if self.active_box == self.username_box:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_box == self.password_box:
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
        return None

    def save_user(self):
        user_data = {
            'username': self.username,
            'password': self.password,  # Not: Parolalar güvenli şekilde saklanmalıdır. Bu örnek sadece temel yapı içindir.
            'gender': self.gender,
            'photo': self.selected_photo,
            'registration_date': datetime.now()
        }
        users_collection.insert_one(user_data)
        print('User registered successfully!')
        # Debug: Veritabanındaki kullanıcıları yazdırın
        print(list(users_collection.find()))

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        self.username_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 50)
        self.password_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        self.login_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)
        self.username = ''
        self.password = ''
        self.active_box = None
        self.logged_in_user = None  # Logged-in user data

    def draw(self):
        self.screen.fill('#f1e8bf')
        pygame.draw.rect(self.screen, '#a47e0b', self.username_box, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.password_box, 2)
        pygame.draw.rect(self.screen, '#a47e0b', self.login_btn, 2)

        username_surf = self.font.render(self.username, True, '#000000')
        password_surf = self.font.render('*' * len(self.password), True, '#000000')
        self.screen.blit(username_surf, (self.username_box.x + 10, self.username_box.y + 10))
        self.screen.blit(password_surf, (self.password_box.x + 10, self.password_box.y + 10))

        login_text = self.font.render('GİRİŞ YAP', True, '#000000')
        self.screen.blit(login_text, login_text.get_rect(center=self.login_btn.center))

        self.screen.blit(self.small_font.render('Kullanıcı Adı:', True, '#000000'), (self.username_box.x, self.username_box.y - 30))
        self.screen.blit(self.small_font.render('Şifre:', True, '#000000'), (self.password_box.x, self.password_box.y - 30))
        pygame.display.flip()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_box.collidepoint(event.pos):
                self.active_box = self.username_box
            elif self.password_box.collidepoint(event.pos):
                self.active_box = self.password_box
            elif self.login_btn.collidepoint(event.pos):
                if self.validate_user():
                    return 'login_success', self.logged_in_user
        if event.type == pygame.KEYDOWN:
            if self.active_box == self.username_box:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_box == self.password_box:
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
        return None, None

    def validate_user(self):
        print(f'Trying to login with username: {self.username} and password: {self.password}')
        
        user = users_collection.find_one({
            'username': self.username,
            'password': self.password  # Not: Parolaların düz metin olarak kontrolü yerine hash kullanılması önerilir.
        })
        
        if user:
            print('Login successful!')
            self.logged_in_user = user
            return True
        else:
            print('Invalid credentials!')
            return False
