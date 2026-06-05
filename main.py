import os
import random
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
        self.screen_fill(screen, self.background['light_blue'])

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # (110, 215, 2)
            # (184, 172, 95)
            # new_color = tuple(random.randint(0, 255) for i in range(3))
            # print(new_color)
            # self.screen_fill(screen, new_color)
            # self.pg.draw.rect(screen, self.background['yellow'], (100, 100, 100, 100))

            c = random.randint(10, 400)
            self.pg.draw.rect(screen, random.choice(list(self.background.values())), (c, c, c, c))

            self.pg.display.flip()
            pygame.time.delay(3000)

        self.quite_pygame()

    def __call__(self):
        self.run_program()


icon = 'schmetterling16.png'

pg = PygameManager(pygame, 800, 600, icon)
pg()
