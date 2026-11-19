import pygame
from random import randrange

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (207, 224, 252)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Радиус яблока
RADIUS = GRID_SIZE // 2

# Цвет головы змейки
SNAKE_HEAD_COLOR = (255, 122, 0)

# Цвет туловища змейки
SNAKE_BODY_COLOR = (255, 100, 0)

# Радиус яблока
RADIUS = GRID_SIZE // 2

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(
            self,
            position,
            body_color
            ):
        self.position = position
        self.body_color = body_color


class Snake(GameObject):
    def __init__(
            self,
            surface,
            body_color=None
            ):
        super().__init__(position=(0, 0),
                         body_color=body_color or SNAKE_BODY_COLOR
                         )
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.surface = surface
        self.last = None
        start_position = self.randomize_position()
        self.positions = [start_position]

    def randomize_position(self):
        """Появление змейки на карте."""
        grid_width = SCREEN_WIDTH // GRID_SIZE
        grid_height = SCREEN_HEIGHT // GRID_SIZE
        wight_pos = randrange(grid_width) * GRID_SIZE
        height_pos = randrange(grid_height) * GRID_SIZE
        return wight_pos, height_pos

    def get_head_position(self):
        return self.positions[0]

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """Движение змейки."""
        col, row = self.get_head_position()
        col_offset, row_offset = self.direction
        new_col = (col + col_offset) % GRID_WIDTH
        new_row = (row + row_offset) % GRID_HEIGHT
        new_head = (new_col, new_row)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        start_position = (start_x, start_y)
        self.position = start_position
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def draw(self, surface=None):
        """Отрисовка головы и тела змейки"""
        if surface is None:
            surface = self.surface
        for segment_index, (col, row) in enumerate(self.positions):
            screen_x = col * GRID_SIZE
            screen_y = row * GRID_SIZE
            rect = pygame.Rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE)
            if segment_index == 0:
                color = SNAKE_HEAD_COLOR
            else:
                color = SNAKE_BODY_COLOR

            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def get_speed_level(self, base_length=5, step_size=1):
        """Ускорение змейки."""
        return (self.length - 1) // base_length


class Apple(GameObject):
    def __init__(
            self,
            surface,
            body_color=None
            ):
        super().__init__(
            position=(0, 0),
            body_color=body_color or APPLE_COLOR
            )
        self.surface = surface
        self.position = self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """Появление яблока на карте."""
        cells_x = GRID_WIDTH
        cells_y = GRID_HEIGHT
        max_attempts = 100
        for _ in range(max_attempts):
            col = randrange(cells_x)
            row = randrange(cells_y)
            pos = (col, row)
            if snake_positions is None or pos not in snake_positions:
                return pos

        return randrange(cells_x), randrange(cells_y)

    def draw(self, surface=None):
        """Отрисовка яблока."""
        if surface is None:
            surface = self.surface
        col, row = self.position
        screen_x = col * GRID_SIZE
        screen_y = row * GRID_SIZE
        center_x = screen_x + GRID_SIZE // 2
        center_y = screen_y + GRID_SIZE // 2
        pygame.draw.circle(surface, self.body_color,
                           (center_x, center_y), RADIUS)
        stem_w, stem_h = 4, 6
        stem_x = center_x - stem_w // 2
        stem_y = screen_y + 2
        pygame.draw.rect(surface, (101, 67, 33),
                         (stem_x, stem_y, stem_w, stem_h))
        leaf_w, leaf_h = 8, 4
        leaf_x = stem_x + stem_w
        leaf_y = stem_y - leaf_h // 2
        pygame.draw.ellipse(surface, (0, 128, 0),
                            (leaf_x, leaf_y, leaf_w, leaf_h))


class GameGrid:
    def __init__(
            self,
            surface,
            width,
            height,
            size):
        self.surface = surface
        self.width = width
        self.height = height
        self.size = size

    def draw(self):
        """Отрисовка поля."""
        color = (200, 200, 200)
        for vector_x in range(0, self.width, self.size):
            pygame.draw.line(self.surface, color,
                             (vector_x, 0), (vector_x, self.height))
        for vector_y in range(0, self.height, self.size):
            pygame.draw.line(self.surface, color,
                             (0, vector_y), (self.width, vector_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    snake = Snake(screen)
    apple = Apple(screen)
    base_speed = 10
    speed_step = 2
    max_speed = 60
    grid = GameGrid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.change_direction(RIGHT)
        snake.move()
        acceleration_level = snake.get_speed_level(base_length=5, step_size=1)
        current_speed = base_speed + acceleration_level * speed_step
        current_speed = min(current_speed, max_speed)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(
                snake_positions=snake.positions)
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(
                snake_positions=snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        grid.draw()
        snake.draw()
        apple.draw()
        pygame.display.flip()
        clock.tick(current_speed)
    pygame.quit()


if __name__ == '__main__':
    main()
