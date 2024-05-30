from pygame.math import Vector2

# Ekran için veriler
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
TILE_SIZE = 64

# Kaplamaların pozisyonları
OVERLAY_POSITION = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

# Aletlerin kullanıcı üzerindeki konumu
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

# Oyuna eklenecek katmanların sıralaması
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10,
}

# Bitkilerin büyüme hızı
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

# Satış fiyatları
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}

# Alış fiyatları
PURCHASE_PRICES = {
    'corn': 5,
    'tomato': 7,
    'axe_2': 200,
    'axe_3': 1000,
    'scissors': 50
}

APPLE_POS = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)]
}
