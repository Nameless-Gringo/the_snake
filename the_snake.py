from random import choice, randint

import pygame as pg

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

# Центр экрана.
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс GameObject. Описывает позицию и цвет объекта."""

    def __init__(self, positions=SCREEN_CENTER, color=BORDER_COLOR):
        self.position = positions
        self.body_color = color

    def draw(self):
        """Метод переопределяется в дочерних классах."""


class Apple(GameObject):
    """Этот дочерний класс описывает поведение "яблока"."""

    def __init__(self, occupied_cells=[SCREEN_CENTER], color=APPLE_COLOR):
        self.randomize_position(occupied_cells)
        super().__init__(self.position, color)

    def randomize_position(self, occupied_cells):
        """Этот метод вычисляет положение яблока на игровом поле (рандомно)."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Этот метод отрисовывает яблоко на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Этот дочерний класс описывает поведение "змейки"."""

    def __init__(self, positions=SCREEN_CENTER, color=SNAKE_COLOR):
        super().__init__(positions, color)
        self.reset()
        self.next_direction = None
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
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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

        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            dx, dy = head  # Распаковка кортежа/головы змейки
            dxr, dyr = self.direction  # Распаковка кортежа/направления
            self.positions.insert(0, ((dx + dxr * GRID_SIZE) % SCREEN_WIDTH,
                                      (dy + dyr * GRID_SIZE) % SCREEN_HEIGHT))

    def reset(self):
        """Метод, который сбрасывает параметры змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Функция handle_keys отвечает за реагирование на нажатие клавиш.
    В условии отслеживается, какая клавиша нажата и если текущее
    направление змейки не противоположно нажатой клавише
    (нельзя двигаться назад), то атрибуту next_direction экземпляра класса
    snake присваивается значение, которое равно нажатой клавише.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:  # Добавлена кнопка выхода
                pg.quit()
                raise SystemExit


def main():
    """Главная функция, запускающая код игры.
    В бесконечном цикле выполняются функции отрисовки
    яблока и змейки, обновления экрана и реагирования
    на нажатия клавиш.
    """
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1
            apple.draw()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
