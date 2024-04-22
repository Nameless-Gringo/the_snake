from random import choice, randint

import pygame

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
BORDER_COLOR = (0, 0, 0)
# BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс GameObject. Описывает позицию и цвет объекта."""

    position: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    body_color: tuple = (255, 0, 0)

    def __init__(self):
        self.position = GameObject.position
        self.body_color = GameObject.body_color

    def draw(self):
        """Метод, наследуемый в дочерних классах."""
        pass


class Apple(GameObject):
    """Этот дочерний класс описывает поведение "яблока"."""

    body_color: tuple = APPLE_COLOR
    position: tuple = GameObject.position

    def __init__(self):
        super().__init__()
        self.body_color = Apple.body_color
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Этот метод вычисляет положение яблока на игровом поле (рандомно)."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.position

    def draw(self):
        """Этот метод отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Этот дочерний класс описывает поведение "змейки"."""

    positions: list = [GameObject.position]  # Список с кортежами пикселей.
    length: int = 1  # Длина positions, т.е. длина змейки.
    direction: tuple = LEFT  # Направление движения змейки.
    next_direction = None  # Следующее направление.
    body_color = SNAKE_COLOR  # Цвет змейки.

    def __init__(self):
        super().__init__()
        self.positions = Snake.positions
        self.direction = Snake.direction
        self.body_color = Snake.body_color
        self.next_direction = Snake.next_direction
        self.last = None

    def update_direction(self):
        """Метод обновляет текущее направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращает кортеж,
        который отрисовывается первым (голову).
        """
        return self.positions[0]

    def draw(self):
        """Метод отрисовывает змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

            # # Затирание последнего сегмента
            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """
        Этот метод отвечает за движение змейки.

        В нем идут проверки на условия:
        если направление UP, DOWN, LEFT, RIGHT, то
        осуществляется дополнительная проверка,
        выходит ли в переменной head значение
        x и y за рамки поля:
        0 и SCREEN_WIDTH, 0 и SCREEN_HEIGHT соответственно.

        Если да - то выполняется код,
        который добавляет в кортеж head противоположные
        значения на соответствующие координаты.
        Это сделано, чтобы змейка выходила с противоположной стороны поля.
        """
        head = self.get_head_position()
        if self.length:
            if len(self.positions) > self.length:
                self.positions.pop()
            else:
                if self.direction == RIGHT:
                    if head[0] == SCREEN_WIDTH:
                        self.positions.insert(0, (0, self.positions[0][1]))
                    else:
                        dx, dy = head  # Распаковка кортежа/головы змейки
                        dxr, dyr = RIGHT  # Распаковка кортежа/направления
                        self.positions.insert(0, ((dx + dxr * GRID_SIZE),
                                                  (dy + dyr * GRID_SIZE)))

                elif self.direction == LEFT:
                    if head[0] == 0:
                        self.positions.insert(0, (SCREEN_WIDTH,
                                                  self.positions[0][1]))

                    else:
                        dx, dy = head  # Распаковка кортежа/головы змейки
                        dxl, dyl = LEFT  # Распаковка кортежа/направления
                        self.positions.insert(0, ((dx + dxl * GRID_SIZE),
                                                  (dy + dyl * GRID_SIZE)))

                elif self.direction == UP:
                    if head[1] == 0:
                        self.positions.insert(0, (self.positions[0][0],
                                                  SCREEN_HEIGHT))

                    else:
                        dx, dy = head  # Распаковка кортежа/головы змейки
                        dxu, dyu = UP  # Распаковка кортежа/направления
                        self.positions.insert(0, ((dx + dxu * GRID_SIZE),
                                                  (dy + dyu * GRID_SIZE)))

                elif self.direction == DOWN:
                    if head[1] == SCREEN_HEIGHT:
                        self.positions.insert(0, (self.positions[0][0], 0))

                    else:
                        dx, dy = head  # Распаковка кортежа/головы змейки
                        dxd, dyd = DOWN  # Распаковка кортежа/направления
                        self.positions.insert(0, ((dx + dxd * GRID_SIZE),
                                                  (dy + dyd * GRID_SIZE)))

    def reset(self):
        """Метод, который сбрасывает параметры змейки."""
        self.length = 1
        self.positions = [GameObject.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Функция handle_keys отвечает за реагирование на нажатие клавиш.
    В условии отслеживается, какая клавиша нажата и если текущее
    направление змейки не противоположно нажатой клавише
    (нельзя двигаться назад), то атрибуту next_direction экземпляра класса
    snake присваивается значение, которое равно нажатой клавише.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция, запускающая код игры.
    В бесконечном цикле выполняются функции отрисовки
    яблока и змейки, обновления экрана и реагирования
    на нажатия клавиш.
    """
    # Инициализация PyGame:
    running = True
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()
        if snake.positions[0] == apple.position:
            apple.randomize_position()
            snake.length += 1
            apple.draw()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            apple.draw()
            snake.draw()
            pygame.display.update()
        pygame.display.update()
        # Тут опишите основную логику игры.
        # ...
    pygame.quit()


if __name__ == '__main__':
    main()
