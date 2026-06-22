import random


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
