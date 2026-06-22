import pygame

from food import Food
from settings import Settings, Color, GameMod
from snake import Snake

game_settings = Settings().__dict__


class PygameManager:
    def __init__(self, py_game, height, width, game_name, icon_path):
        self.pg = py_game
        self.game_name = game_name
        self.height = height
        self.width = width
        self.icon_path = icon_path
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
            new_icon = self.pg.image.load(self.icon_path)
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

    def end_game(self):
        self.game_mod.end_game = True
        self.snake.speed_x, self.snake.speed_y = 0, 0

    def run_program(self):
        self.init_pygame()
        screen = self.create_screen()
        self.set_icon()
        self.new_game()

        end_game_text = 'END GAME'
        end_game_continue_text = 'PRESS "ESC" TO START NEW GAME'

        font_mod = self.pg.font.Font(None, 50)
        end_game_mod = self.pg.font.Font(None, 80)
        font_score = self.pg.font.Font(None, 30)

        end_game_font = end_game_mod.render(end_game_text, True, self.color.background['white'])
        end_game_continue_font = font_mod.render(end_game_continue_text, True, self.color.background['white'])

        text_pause = font_mod.render('PAUSE', True, self.color.background['white'])
        start_text = font_mod.render('PRESS ENTER TO START', True, self.color.background['white'])

        while self.game_mod.running:
            self.screen_fill(screen, self.color.background['light_blue'])

            # Отображаем набранные очки в игре
            score_text = font_score.render(
                f'SCORE {self.score}', True, self.color.background['grey']
            )

            # Отображаем набранные очки в конце игры

            score_font = font_mod.render(f'YOUR SCORE {self.score}', True, self.color.background['white'])

            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    self.game_mod.running = False
                elif event.type == self.pg.KEYDOWN:
                    if event.key == 27:
                        self.new_game()
                    if event.key == 13 and not self.game_mod.game_started:
                        self.snake.speed_x = self.snake.snake_speed
                        self.game_mod.game_started = True
                    if not self.game_mod.end_game and self.game_mod.game_started:
                        if not self.game_mod.pause:
                            if event.key == 1073741904 and self.snake.speed_x <= 0:
                                self.snake.speed_x, self.snake.speed_y = -self.snake.snake_speed, 0
                            if event.key == 1073741903 and self.snake.speed_x >= 0:
                                self.snake.speed_x, self.snake.speed_y = self.snake.snake_speed, 0
                            if event.key == 1073741906 and self.snake.speed_y <= 0:
                                self.snake.speed_x, self.snake.speed_y = 0, -self.snake.snake_speed
                            if event.key == 1073741905 and self.snake.speed_y >= 0:
                                self.snake.speed_x, self.snake.speed_y = 0, self.snake.snake_speed
                            if event.key == 32:
                                self.snake.pause_x, self.snake.pause_y = self.snake.speed_x, self.snake.speed_y
                                self.snake.speed_x, self.snake.speed_y = 0, 0
                                self.game_mod.pause = True
                        elif self.game_mod.pause and event.key == 32:
                            self.game_mod.pause = False
                            self.snake.speed_x, self.snake.speed_y = self.snake.pause_x, self.snake.pause_y

            # Текст в начале игры

            if not self.game_mod.game_started:
                screen.blit(start_text, (230, 250))

            # Движение змейки

            self.snake.x += self.snake.speed_x
            self.snake.y += self.snake.speed_y

            if not self.game_mod.pause:
                new_snake_part = self.snake.make_snake_part(self.snake.x, self.snake.y)
                self.snake.snake_body.insert(0, new_snake_part)

            snake_body = self.snake.snake_body[:self.snake.snake_length]

            if self.game_mod.game_started:
                # Отрисовываем тело змейки

                for s_p in snake_body:
                    self.pg.draw.rect(screen, self.color.background['light_green'], s_p)

                # Добавляем еду в список при первом запуске и при сьедании в дальнейшем
                if not self.food.food_lst:
                    coord = self.food.food_coord(self.snake.snake_body[0], self.snake.snake_body[-1],
                                                 self.snake.snake_size)
                    self.food.food_lst.append(self.pg.Rect(coord, (self.food.food_size, self.food.food_size)))
                else:
                    for food in self.food.food_lst:
                        self.pg.draw.rect(screen, self.color.background['orange'], food)

                    # Проверяем сьела ли змейка еду, если да, то увеличиваем длину и скорость

                    if snake_body[0].colliderect(self.food.food_lst[0]):
                        self.snake.snake_length += 20
                        self.snake.snake_speed += 0.1
                        self.score += 1
                        self.food.food_lst.pop()

                screen.blit(score_text, (650, 25))

            # Рисуем глаза

            if self.snake.speed_x > 0 and self.snake.speed_y == 0:
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x + self.snake.snake_size - self.snake.eye_size,
                        self.snake.y,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
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

            elif self.snake.speed_x < 0 and self.snake.speed_y == 0:
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x,
                        self.snake.y + self.snake.snake_size - self.snake.eye_size,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
                )
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x,
                        self.snake.y,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
                )
            elif self.snake.speed_y > 0 and self.snake.speed_x == 0:
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x,
                        self.snake.y + self.snake.snake_size - self.snake.eye_size,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
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

            elif self.snake.speed_y < 0 and self.snake.speed_x == 0:
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x + self.snake.snake_size - self.snake.eye_size,
                        self.snake.y,
                        self.snake.eye_size,
                        self.snake.eye_size
                    )
                )
                self.pg.draw.rect(
                    screen,
                    self.color.background['yellow'],
                    (
                        self.snake.x,
                        self.snake.y,
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

            # Текст в конце игры

            if self.game_mod.end_game:
                screen.blit(end_game_font, (250, 180))
                screen.blit(score_font, (280, 250))
                screen.blit(end_game_continue_font, (130, 300))

            # Текст паузы

            if self.game_mod.pause:
                screen.blit(text_pause, (330, 250))

            self.pg.time.delay(10)
            self.pg.display.flip()

        self.quite_pygame()

    def __call__(self):
        self.run_program()


if __name__ == '__main__':
    pg = PygameManager(pygame, **game_settings)
    pg()
