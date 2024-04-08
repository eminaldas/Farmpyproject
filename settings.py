from pygame.math import Vector2

#Ekran için veriler
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
TILE_SIZE = 64

#kaplamaların pozisyonları
OVERLAY_POSITON = {
    'tool': (40,SCREEN_HEIGHT-15),
    'seed': (70,SCREEN_HEIGHT-5)
}

#aletlerin kullanıcı üzerindeki konumu
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50,40),
    'right': Vector2(50,40),
    'up': Vector2(0,-10),
    'down': Vector2(0,50)
}

#oyuna eklenecek katmanların sıralaması
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

#bitkilerin büyüme hızı
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

#satış fiyatları
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}

#alış fiyatları
PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}

