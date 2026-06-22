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
