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
        'grey': (225, 225, 225),
    }


class Snake:
    def __init__(self, snake_game, x, y):
        self.snake_size = 30
        self.snake_speed = 2
        self.snake_length = 1
        self.eye_size = 5
        self.snake_game = snake_game
        self.x, self.y = (x, y)
        self.speed_x, self.speed_y = (0, 0)
        self.pause_x, self.pause_y = (0, 0)
        self.snake_body = [self.make_snake_part(self.x, self.y)]

    def make_snake_part(self, x, y):
        return self.snake_game.Rect((x, y), (self.snake_size, self.snake_size))


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
        self.color = Color()
        self.end_border = (9, 33)
        self.score = 0

    def create_screen(self):
        new_screen = self.pg.display.set_mode((self.height, self.width))
        self.pg.display.set_caption(self.game_name)
        print(f'Окно размером {self.height} * {self.width} создано!')
        return new_screen

    def set_icon(self):
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
        self.score = 0

    def run_program(self):
        self.init_pygame()
        screen = self.create_screen()
        self.set_icon()
        self.new_game()

        font_mod = self.pg.font.Font(None, 50)
        font_score = self.pg.font.Font(None, 30)
        text_end_game = font_mod.render('END GAME', True, self.color.background['white'])
        text_pause = font_mod.render('PAUSE', True, self.color.background['white'])
        start_text = font_mod.render('PRESS ENTER TO START', True, self.color.background['white'])

        while self.game_mod.running:
            # Отображаем набранные очки
            score_text = font_score.render(
                f'SCORE {self.score}', True, self.color.background['grey']
            )
            self.screen_fill(screen, self.color.background['light_blue'])

            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    self.game_mod.running = False
                elif event.type == self.pg.KEYDOWN:
                    # print(event.key)
                    if event.key == 27:
                        self.new_game()
                        print('NEW GAME')
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

            if not self.game_mod.game_started:
                screen.blit(start_text, (230, 250))

            self.snake.x += self.snake.speed_x
            self.snake.y += self.snake.speed_y

            new_snake_part = self.snake.make_snake_part(self.snake.x, self.snake.y)
            self.snake.snake_body.insert(0, new_snake_part)
            snake_body = self.snake.snake_body[:self.snake.snake_length]

            # Отрисовываем тело змейки
            for s_p in snake_body:
                self.pg.draw.rect(screen, self.color.background['light_green'], s_p)

            if self.snake.speed_x > 0 and self.snake.speed_y == 0:
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (self.snake.x + self.snake.snake_size - self.snake.eye_size, self.snake.y, self.snake.eye_size, self.snake.eye_size)
                )
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x + self.snake.snake_size - self.snake.eye_size,
                        self.snake.y + self.snake.snake_size - self.snake.eye_size,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
                )

            # Рисуем границы для большей атмосферности

            self.pg.draw.lines(screen, (102, 102, 0), True, [(1, 598), (798, 598), (798, 1), (1, 1)], 10)

            # Проверяем границы карты на столкновения

            if (self.snake.x <= self.end_border[0] or self.snake.x >= self.height - self.end_border[1] or
                    self.snake.y <= self.end_border[0] or self.snake.y >= self.width - self.end_border[1]):
                self.end_game()

            # Проверяем врезалась ли змейка в саму себя
            if self.snake.snake_length > 1:
                for s in snake_body[1:]:
                    if (snake_body[0].x, snake_body[0].y) == (s.x, s.y):
                        self.end_game()

            if self.game_mod.end_game:
                screen.blit(text_end_game, (300, 250))

            # Добавляем еду в список при первом запуске и при сьедании в дальнейшем
            if not self.food.food_lst:
                coord = self.food.food_coord(self.snake.snake_body[0], self.snake.snake_body[-1], self.snake.snake_size)
                self.food.food_lst.append(self.pg.Rect(coord, (self.food.food_size, self.food.food_size)))
            else:
                for food in self.food.food_lst:
                    f = self.pg.draw.rect(screen, self.color.background['yellow'], food)

                # Проверяем сьела ли змейка еду, если да, то увеличиваем длину и скорость

                if snake_body[0].colliderect(self.food.food_lst[0]):
                    self.snake.snake_length += 20
                    self.snake.snake_speed += 0.1
                    self.score += 1
                    self.food.food_lst.pop()

            if self.game_mod.pause:
                screen.blit(text_pause, (330, 250))

            screen.blit(score_text, (650, 25))

            self.pg.time.delay(10)
            self.pg.display.flip()

        self.quite_pygame()

    def __call__(self):
        self.run_program()

    def end_game(self):
        self.game_mod.end_game = True
        self.snake.speed_x, self.snake.speed_y = 0, 0


icon = 'schmetterling16.png'

pg = PygameManager(pygame, 800, 600, game_name='Snake', icon=icon)
pg()
