import os
import random
import threading
import time
from time import sleep

import pygame
import requests


class PygameManager:
    def __init__(self, py_game, height, width, icon_path):
        self.pg = py_game
        self.height = height
        self.width = width
        self.icon = icon_path
        self.background = {
            'blue': (135, 206, 250),
            'light_blue': (76, 166, 204),
            'purple': (66, 28, 161),
            'light_green': (121, 246, 157),
            'orange': (242, 58, 28),
            'yellow': (255, 255, 0),
            'white': (255, 255, 255),
            'ert': (51, 25, 0)
        }

    def create_screen(self):
        new_screen = self.pg.display.set_mode((self.height, self.width))
        self.pg.display.set_caption('Game')
        print(f'Окно размером {self.height} * {self.width} создано!')
        return new_screen

    def change_icon(self):
        try:
            icon = self.pg.image.load(self.icon)
            self.pg.display.set_icon(icon)
        except FileNotFoundError as exc:
            print(exc)

    def init_pygame(self):
        self.pg.init()
        if self.pg.get_init():
            print("Инициализация завершена успешно!")
        else:
            print("Ошибка при инициализации!")

    def quite_pygame(self):
        self.pg.quit()
        print('Pygame закрыт')

    def screen_fill(self, screen, color):
        screen.fill(color)

    def run_program(self):
        self.init_pygame()
        self.change_icon()
        screen = self.create_screen()
        FPS = 60
        clock = self.pg.time.Clock()
        snake_direction = 'RIGHT'

        r, g, b = (random.randint(0, 255) for i in range(3))

        speed_x, speed_y = 0, 0
        timer = pygame.time.get_ticks()
        x, y = 400, 300
        size = 20
        text_size = 50
        speed = 2
        snake_body = [[x, y]]

        font = self.pg.font.Font(None, text_size)  # Создание объекта шрифта
        text_surface = font.render('END GAME', True, (255, 255, 255))  # Создание текстовой поверхности
        range_a = 9
        range_b = 27
        n = 10

        # start = self.pg.time.get_ticks()
        stop_game = False
        move = False
        running = True

        while running:
            self.screen_fill(screen, self.background['light_blue'])
            keys = self.pg.key.get_pressed()

            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    running = False
                elif event.type == self.pg.KEYDOWN:
                    print(event.key)
                    if event.key == 13 and not move:
                        speed_x = speed
                        move = True
                    elif event.key == 1073741904 and speed_x == 0 and move and not stop_game:
                        speed_x, speed_y = -speed, 0
                    elif event.key == 1073741903 and speed_x == 0 and move and not stop_game:
                        speed_x, speed_y = speed, 0
                    elif event.key == 1073741906 and speed_y == 0 and move and not stop_game:
                        speed_x, speed_y = 0, -speed
                    elif event.key == 1073741905 and speed_y == 0 and move and not stop_game:
                        speed_x, speed_y = 0, speed
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     print(f"Клик мыши в позиции {event.pos}")
                # elif event.type == pygame.MOUSEMOTION:
                #     print(f"Движение мыши в позицию {event.pos}")

            x += speed_x
            y += speed_y
            snake_body.insert(0, [x, y])
            snake_body = snake_body[:n]

            for b in snake_body:
                self.pg.draw.rect(screen, self.background['light_green'], (b[0], b[1], size, size))

            self.pg.draw.lines(screen, (102, 102, 0), True, [(1, 598), (798, 598), (798, 1), (1, 1)], 10)

            if x <= range_a or x >= self.height - range_b or y <= range_a or y >= self.width - range_b:
                screen.blit(text_surface, (300, 250))
                stop_game = True
                speed_x, speed_y = 0, 0

            # x_pos = random.randint(11, 790)
            # if x_pos not in
            self.pg.draw.rect(screen, self.background['yellow'], (600, 100, 20, 20))

            # if y <= 10 or y >= 600 - 20:
            #     speed_y = -speed_y
            #     print('Отскок')

            # pygame.draw.circle(surface, color, (center_x, center_y), radius)

            # self.pg.draw.rect(screen, RED, (x, y, 50, 50))
            # if self.pg.time.get_ticks() >= timer + 5000:
            #     if speed_x1 >= 0:
            #         speed_x1 += 2
            #     else:
            #         speed_x1 -= 2
            #
            #     if speed_y1 >= 0:
            #         speed_y1 += 2
            #     else:
            #         speed_y1 -= 2
            #
            #     timer = self.pg.time.get_ticks()

            # print(speed_x1, speed_y1)
            # screen.blit(text_surface, (x1, y1))

            # clock.tick(FPS)
            self.pg.time.delay(10)

            self.pg.display.flip()

            # pygame.time.delay(3000)

        self.quite_pygame()

    def __call__(self):
        self.run_program()


class Food:
    def __init__(self, screen, position=None, size=10, color=(255, 255, 0)):
        if position is None:
            self.position = (400, 300)
        self.screen = screen
        self.size = size
        self.color = color

    def make_food_on_screen(self, pg):
        x_pos = random.randint(11, 790)
        pg.draw.rect(self.screen, self.color, (600, 100, 10, 10))


icon = 'schmetterling16.png'

pg = PygameManager(pygame, 800, 600, icon)
# pg()
# r, g, b = (random.randint(0, 255) for i in range(3))
# print(r, g, b)
#
# pygame.init()
#
# game = True
#
# fps = 60
# clock= pygame.time.Clock()
#
# size = width, high = (800, 600)
#
# sc = pygame.display.set_mode(size)
# pygame.display.set_caption('Змейка - 4G')
#
# lst = []#тело змейки
# n = 1  #макс длина змейки
#
# x = 300
# y = 300
#
# dx = 0
# dy = 0
#
# #food
# x_food = 200
# y_food = 100
# food = 0#сколько съела
#
# fonte = pygame.font.Font(None, 50)
# surface4 = fonte.render('нажмите "W" или "S" или "A" или "D"', 1, pygame.Color('brown'))
# text = True
# start_text = True
#
# excr = []
#
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             start_text = False
#             if event.key == pygame.K_w:
#                 if dy != 2:
#                     dy = -2
#                     dx = 0
#             elif event.key == pygame.K_s:
#                 if dy != -2:
#                     dy = 2
#                     dx = 0
#             elif event.key== pygame.K_d:
#                 if dx != -2:
#                     dx = 2
#                     dy = 0
#             elif event.key == pygame.K_a:
#                 if dx != 2:
#                     dx = -2
#                     dy = 0
#             elif event.key == pygame.K_SPACE:
#                 lst = [(300, 300)]
#                 n = 1
#                 x_food = 200
#                 y_food = 100
#                 food = 0
#                 fps = 60
#                 game = True
#                 dx = 0
#                 dy = 0
#                 x = y = 300
#                 excr = []
#
#
#
#     #изменение координат
#     x += dx
#     y += dy
#     lst.insert(0, (x, y))
#     lst = lst[:n]
#
#
#
#     #Захват еды.
#     if abs(x-x_food)<41 and abs(y-y_food)<41:
#         n +=10#увеличение длины
#         fps+=5#ускорение
#         food+=1#счётчик еды
#         excr.append((lst[-1][0]+ 20, lst[-1][1]+20))
#         x_food = random.randrange(0, width - 40, 40)
#         y_food = random.randrange(0, high - 40, 40)
#         if abs(x-x_food)<41 and abs(y-y_food)<41:
#             x_food = random.randrange(0, width - 40, 40)
#             y_food = random.randrange(0, high - 40, 40)
#
#     surface = fonte.render('game over', 1, pygame.Color('brown'))
#     surface1 = fonte.render(f'Вы набрали: {food} очков', 1, pygame.Color('brown'))
#     surface2 = fonte.render('нажмите пробел', 1, pygame.Color('brown'))
#
#     #проверка на выход за границы
#     if x < 0 or x > width - 40 or y < 0 or y > high - 40:
#         game = False
#
#
#
#
#     #рисуем фон, еду и змейку
#     sc.fill((0, 200, 150))
#     if start_text:
#         sc.blit(surface4, (80, 250))
#     if game:
#         pygame.draw.rect(sc, pygame.Color((0, 150, 50)), (x_food, y_food, 40, 40), 15)
#         for i in lst:
#             pygame.draw.rect(sc, pygame.Color('brown'), (i[0], i[1], 40, 40))
#         for i in excr:
#             pygame.draw.circle(sc, (80, 5, 5), (i[0], i[1]), 5)
#     else:
#         sc.blit(surface,  (305, 250))
#         sc.blit(surface1, (215, 300))
#         sc.blit(surface2, (255, 350))
#         for i in excr:
#             pygame.draw.circle(sc, (80, 5, 5), (i[0], i[1]), 5)
#
#     pygame.display.flip()
#
#     clock.tick(fps)
#
# pygame.quit()
