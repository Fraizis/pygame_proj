import random

from dataclasses import dataclass
from typing import ClassVar

import pygame


@dataclass
class GameMod:
    game_started: bool = False
    end_game: bool = False
    running: bool = True
    pause: bool = False


@dataclass
class Color:
    background: ClassVar[dict[str, tuple]] = {
        'blue': (135, 206, 250),
        'light_blue': (76, 166, 204),
        'purple': (66, 28, 161),
        'light_green': (121, 246, 157),
        'orange': (242, 58, 28),
        'yellow': (255, 255, 0),
        'white': (255, 255, 255),
        'ert': (51, 25, 0)
    }


class Snake:
    def __init__(self, snake_game, x, y):
        self.snake_size = 30
        self.snake_speed = 2
        self.snake_length = 1
        self.snake_game = snake_game
        self.x, self.y = (x, y)
        self.speed_x, self.speed_y = (0, 0)
        self.pause_x, self.pause_y = (0, 0)
        self.snake_part = self.snake_game.Rect((self.x, self.y), (self.snake_size, self.snake_size))
        self.snake_body = [self.snake_part]

    def insert_body(self, x, y):
        self.snake_body.append(self.snake_game.Rect((x, y), (self.snake_size, self.snake_size)))
        # return self.snake_body[:self.snake_length]


class Food:
    def __init__(self, height, width):
        self.food_size = 15
        self.food_lst = []
        self.border_x = (self.food_size, height - self.food_size)
        self.border_y = (self.food_size, width - self.food_size)

    def food_coord(self, snake_head, snake_tail, snake_size):
        snake_x = (snake_head[0], snake_tail[0] + snake_size)
        snake_y = (snake_head[1], snake_tail[1] + snake_size)
        # Выбираем новые координаты для еды, исключая тело змейки и границы
        new_food_x = random.choice(
            list(set(range(self.border_x[0], self.border_x[1])) - set(range(snake_x[0], snake_x[1] + 1)))
        )
        new_food_y = random.choice(
            list(set(range(self.border_y[0], self.border_y[1])) - set(range(snake_y[0], snake_y[1] + 1)))
        )
        return new_food_x, new_food_y


class PygameManager:
    def __init__(self, py_game, height, width, game_name, icon):
        self.pg = py_game
        self.game_name = game_name
        self.height = height
        self.width = width
        self.icon = icon
        self.start_pos = (self.height / 2, self.width / 2)
        self.x, self.y = self.start_pos
        self.snake = None
        self.food = None
        self.game_mod = None
        self.color = Color

    def create_screen(self):
        new_screen = self.pg.display.set_mode((self.height, self.width))
        self.pg.display.set_caption(self.game_name)
        print(f'Окно размером {self.height} * {self.width} создано!')
        return new_screen

    def set_new_icon(self):
        try:
            new_icon = self.pg.image.load(self.icon)
            self.pg.display.set_icon(new_icon)
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

    def new_game(self):
        self.x, self.y = self.start_pos
        self.snake = Snake(self.pg, self.x, self.y)
        self.food = Food(height=self.height, width=self.width)
        self.game_mod = GameMod()
        print('NEW GAME')
        # self.game_mod.game_started = False
        # self.game_mod.end_game = False
        # self.game_mod.running = True
        # self.game_mod.pause = False

    def run_program(self):
        self.init_pygame()
        screen = self.create_screen()
        self.new_game()
        text_size = 50

        font = self.pg.font.Font(None, text_size)
        text_surface = font.render('END GAME', True, (255, 255, 255))
        text_pause = font.render('PAUSE', True, (255, 255, 255))
        start_text = font.render('PRESS ENTER TO START', True, (255, 255, 255))
        end_border = (9, 33)


        while self.game_mod.running:
            self.screen_fill(screen, self.color.background['light_blue'])
            keys = pygame.key.get_pressed()
            # print(keys)

            if not self.game_mod.game_started:
                screen.blit(start_text, (230, 250))

            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    self.game_mod.running = False
                elif event.type == self.pg.KEYDOWN:
                    print(event.key)
                    if event.key == 27:
                        self.new_game()
                    if event.key == 13 and not self.game_mod.game_started:
                        self.snake.speed_x = self.snake.snake_speed
                        self.game_mod.game_started = True
                    if not self.game_mod.end_game and self.game_mod.game_started:
                        if not self.game_mod.pause:
                            if event.key == 1073741904 and self.snake.speed_x <= 0:
                                self.snake.speed_x, self.snake.speed_y = -self.snake.snake_speed, 0
                                print('LEFT')
                            if event.key == 1073741903 and self.snake.speed_x >= 0:
                                self.snake.speed_x, self.snake.speed_y = self.snake.snake_speed, 0
                                print('RIGHT')
                            if event.key == 1073741906 and self.snake.speed_y <= 0:
                                self.snake.speed_x, self.snake.speed_y = 0, -self.snake.snake_speed
                                print('UP')
                            if event.key == 1073741905 and self.snake.speed_y >= 0:
                                self.snake.speed_x, self.snake.speed_y = 0, self.snake.snake_speed
                                print('DOWN')
                            if event.key == 32:
                                self.snake.pause_x, self.snake.pause_y = self.snake.speed_x, self.snake.speed_y
                                self.snake.speed_x, self.snake.speed_y = 0, 0
                                self.game_mod.pause = True
                                print('PAUSE')
                        elif self.game_mod.pause and event.key == 32:
                            self.game_mod.pause = False
                            self.snake.speed_x, self.snake.speed_y = self.snake.pause_x, self.snake.pause_y
                            print('UNPAUSE')
                            # if event.key == 32 and self.game_mod.game_started:
                            #     self.snake.pause_x, self.snake.pause_y = self.snake.speed_x, self.snake.speed_y
                            #     self.snake.speed_x, self.snake.speed_y = 0, 0
                            #     self.game_mod.pause = True
                            #     print('PAUSE')
                        # else:
                            self.game_mod.pause = False
                            self.snake.speed_x, self.snake.speed_y = self.snake.pause_x, self.snake.pause_y
                            print('UNPAUSE')

                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     print(f"Клик мыши в позиции {event.pos}")
                # elif event.type == pygame.MOUSEMOTION:
                #     print(f"Движение мыши в позицию {event.pos}")

            self.snake.x += self.snake.speed_x
            self.snake.y += self.snake.speed_y

            snake_part = self.pg.Rect((self.snake.x, self.snake.y), (self.snake.snake_size, self.snake.snake_size))
            # self.snake.insert_body(self.snake.x, self.snake.y)
            # snake_body = [snake_part]
            self.snake.snake_body.insert(0, snake_part)
            snake_body = self.snake.snake_body[:self.snake.snake_length]


            for s_p in snake_body:
                self.pg.draw.rect(screen, self.color.background['light_green'], s_p)

            self.pg.draw.lines(screen, (102, 102, 0), True, [(1, 598), (798, 598), (798, 1), (1, 1)], 10)

            if (self.snake.x <= end_border[0] or self.snake.x >= self.height - end_border[1] or
                    self.snake.y <= end_border[0] or self.snake.y >= self.width - end_border[1]):
                screen.blit(text_surface, (300, 250))
                self.game_mod.end_game = True
                self.snake.speed_x, self.snake.speed_y = 0, 0


            if not self.food.food_lst:
                coord = self.food.food_coord(self.snake.snake_body[0], self.snake.snake_body[-1], self.snake.snake_size)
                self.food.food_lst.append(self.pg.Rect(coord, (self.food.food_size, self.food.food_size)))
            else:
                for food in self.food.food_lst:
                    self.pg.draw.rect(screen, self.color.background['yellow'], food)

                if snake_body[0].colliderect(self.food.food_lst[0]):
                    self.snake.snake_length += 20
                    self.snake.snake_speed += 0.1
                    self.food.food_lst.pop()

            # print(self.snake.snake_length)

            if self.game_mod.pause:
                screen.blit(text_pause, (330, 250))

            self.pg.time.delay(10)
            self.pg.display.flip()

        self.quite_pygame()

    def __call__(self):
        self.run_program()


icon = 'schmetterling16.png'

pg = PygameManager(pygame, 800, 600, game_name='Snake', icon=icon)
pg()
# print(pg.food_coord([[400, 300]]))

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
