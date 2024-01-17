import sys
import pygame
from pygame import Surface, sprite
from pygame.locals import *
from platforms import *
from player_dino import *
from cactuses import *
from fire import *


pygame.init()
fps = 60
clock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
lvl_image = pygame.image.load("images/fon_level.png")
monsters = pygame.sprite.Group()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + 800 / 2, -t + 400 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - 800), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - 400), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

def terminate():
    pygame.quit()
    sys.exit()

def main():
    new_screen = pygame.display.set_mode((800, 250))
    pygame.init()  # Инициация PyGame, обязательная строчка
    bg = Surface((800, 250))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(176, 224, 230))  # Заливаем поверхность сплошным цветом
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    level = [
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                     /                                 --------                       ----------       /                ",
        "                   ------                                                                            --------           ",
        "    ------ *                        --------                        *---------                                          ",
        "------------------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == '*':
                ct = Cactus(x, y)
                entities.add(ct)
                platforms.append(ct)
            if col == '/':
                mn = Fire(x, y, 2, 3, 150, 15)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
                monsters.update(platforms)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
        new_screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        # entities.draw(screen) # отображение
        for event in entities:
            new_screen.blit(event.image, camera.apply(event))

        pygame.display.update()  # обновление и вывод всех изменений на экран


def draw_screensaver(screen):
    screen.fill((194, 237, 206))  # изменить цвет
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 35)

    text = font.render("Hello. These are Dino-Cats", True, (0, 0, 0))  # изменить цвет надписи и её саму
    text2 = font2.render("Start Game", True, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - 50
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (150, 200, 170), ((250, 250), (150, 50)), 0)
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (260, 260))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 250 and event.pos[0] <= 400 and event.pos[1] >= 250 and event.pos[1] <= 300:
                    return

        pygame.display.flip()
        clock.tick(fps)


def draw_menu(screen):
    while True:
        screen.blit(lvl_image, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 47 and event.pos[0] <= 134 and event.pos[1] >= 155 and event.pos[1] <= 240:
                    main()
        # Update.

        # Draw.
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    draw_screensaver(screen)
    draw_menu(screen)
