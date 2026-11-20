from random import randrange

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (107, 107, 148)
APPLE_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (255, 122, 0)
SNAKE_BODY_COLOR = (255, 100, 0)
STEM_COLOR = (101, 67, 33)
LEAF_COLOR = (0, 128, 0)
STEM_WIDTH, STEM_HEIGHT = 4, 6
LEAF_WIDTH, LEAF_HEIGHT = 8, 4
RADIUS = GRID_SIZE // 2
SPEED = 10

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        center_col = GRID_WIDTH // 2
        center_row = GRID_HEIGHT // 2
        self.position = (center_col, center_row)
        self.body_color = body_color

    def draw(self, surface=None):
        """Родительский метод для отрисовки."""


class Snake(GameObject):
    """Змейка: наследуется от GameObject."""

    def __init__(self, surface=screen, body_color=SNAKE_BODY_COLOR):
        super().__init__(body_color=body_color)
        self.surface = surface
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1

    def change_direction(self, new_direction):
        """Запрет разворота змейки на 180С."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """Движение змейки с обновлением позиции головы."""
        col, row = self.get_head_position()
        col_offset, row_offset = self.direction
        new_col = (col + col_offset) % GRID_WIDTH
        new_row = (row + row_offset) % GRID_HEIGHT
        new_head = (new_col, new_row)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        self.position = self.get_head_position()

    def reset(self):
        """Сброс змейки при столкновении."""
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.position = start
        self.positions = [start]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Применяет сохранённое следующее направление, если оно задано."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Сохранение позиции головы змейки."""
        return self.positions[0]

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
    """Яблоко: наследуется от GameObject."""

    def __init__(
            self,
            snake_positions=None,
            surface=screen,
            body_color=APPLE_COLOR
    ):
        super().__init__(body_color=body_color)
        self.surface = surface
        self.position = self.randomize_position(
            snake_positions=snake_positions)

    def randomize_position(self, snake_positions=None):
        """Появление яблока на поле."""
        max_attempts = 100
        for _ in range(max_attempts):
            col = randrange(GRID_WIDTH)
            row = randrange(GRID_HEIGHT)
            pos = (col, row)
            if snake_positions is None or pos not in snake_positions:
                return pos
        return randrange(GRID_WIDTH), randrange(GRID_HEIGHT)

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
        stem_x = center_x - STEM_WIDTH // 2
        stem_y = screen_y + 2
        pygame.draw.rect(surface, STEM_COLOR,
                         (stem_x, stem_y, STEM_WIDTH, STEM_HEIGHT))
        leaf_x = stem_x + STEM_WIDTH
        leaf_y = stem_y - LEAF_HEIGHT // 2
        pygame.draw.ellipse(surface, LEAF_COLOR,
                            (leaf_x, leaf_y, LEAF_WIDTH, LEAF_HEIGHT))


class GameGrid:
    """Класс для создания ячеек."""

    def __init__(self, surface=screen):
        self.surface = surface

    def draw(self):
        """Отрисовка ячеек."""
        color = (40, 40, 40)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.surface, color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.surface, color, (0, y), (SCREEN_WIDTH, y))


def handle_keys(snake):
    """Управление змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.change_direction(RIGHT)
    return True


def main():
    """Инициализация игры."""
    snake = Snake(screen)
    apple = Apple(snake_positions=snake.positions, surface=screen)
    grid = GameGrid(screen)
    base_speed = 10
    speed_step = 2
    max_speed = 60
    running = True
    while running:
        running = handle_keys(snake)
        if not running:
            break
        snake.update_direction()
        snake.move()
        if snake.position == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(
                snake_positions=snake.positions)
        head = snake.positions[0]
        if len(snake.positions) > 3 and head in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(
                snake_positions=snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        grid.draw()
        snake.draw()
        apple.draw()
        pygame.display.flip()
        acceleration_level = snake.get_speed_level(base_length=5, step_size=1)
        current_speed = base_speed + acceleration_level * speed_step
        current_speed = min(current_speed, max_speed)
        clock.tick(current_speed)
    pygame.quit()


if __name__ == '__main__':
    main()
