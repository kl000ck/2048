#!/usr/bin/env python3
"""2048 для терминала.

Запуск:
    python3 game_2048.py

Меню:
    ↑ ↓         выбор пункта
    Enter       подтвердить

Управление в игре:
    ← ↑ → ↓ / WASD / HJKL   двигать плитки
    U                       отменить ход
    R                       начать заново
    Q                       вернуться в меню
"""

import os
import random
import sys

SIZE = 4
CELL_WIDTH = 7
BOARD_WIDTH = SIZE * CELL_WIDTH + SIZE + 1

CLEAR = "\x1b[2J\x1b[H"
BORDER_COLOR = 240
MESSAGE_COLOR = 214
GAME_OVER_COLOR = 203

# (цвет текста, цвет фона) в 256-цветном режиме терминала
TILE_COLORS = {
    2: (235, 252),
    4: (235, 250),
    8: (235, 215),
    16: (255, 209),
    32: (255, 203),
    64: (255, 197),
    128: (235, 227),
    256: (235, 226),
    512: (235, 220),
    1024: (235, 214),
    2048: (235, 208),
}

BEST_FILE = os.path.join(os.path.expanduser("~"), ".2048_best")

_TITLE = "2 0 4 8"
_TITLE_COLOR = 214

_DIRECTIONS = {"up", "down", "left", "right"}

_KEYMAP = {
    "w": "up",
    "k": "up",
    "ц": "up",
    "л": "up",
    "s": "down",
    "j": "down",
    "ы": "down",
    "о": "down",
    "a": "left",
    "h": "left",
    "ф": "left",
    "р": "left",
    "d": "right",
    "l": "right",
    "в": "right",
    "д": "right",
    "q": "q",
    "й": "q",
    "r": "r",
    "к": "r",
    "u": "u",
    "г": "u",
}


# ---------------------------------------------------------------------------
# Отрисовка
# ---------------------------------------------------------------------------

def colors_enabled():
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(text, fg=None, bg=None, bold=False):
    if not colors_enabled():
        return text
    codes = []
    if bold:
        codes.append("1")
    if fg is not None:
        codes.append(f"38;5;{fg}")
    if bg is not None:
        codes.append(f"48;5;{bg}")
    if not codes:
        return text
    return f"\x1b[{';'.join(codes)}m{text}\x1b[0m"


def render_cell(value):
    if value == 0:
        return paint(" " * CELL_WIDTH, bg=237)
    fg, bg = TILE_COLORS.get(
        value, (255, 196) if value > 2048 else TILE_COLORS[2048]
    )
    return paint(str(value).center(CELL_WIDTH), fg=fg, bg=bg)


def border_line(left, middle, right):
    line = left + middle.join("─" * CELL_WIDTH for _ in range(SIZE)) + right
    return paint(line, fg=BORDER_COLOR)


def render(board, score, best, message="", dead=False):
    lines = [CLEAR, ""]
    lines.append("  " + paint(_TITLE.center(BOARD_WIDTH), fg=_TITLE_COLOR, bold=True))
    lines.append("")

    left = f"Счёт: {score}"
    right = f"Рекорд: {best}"
    gap = max(1, BOARD_WIDTH - len(left) - len(right))
    lines.append("  " + left + " " * gap + right)
    lines.append("")

    lines.append("  " + border_line("┌", "┬", "┐"))
    for row in range(SIZE):
        if row:
            lines.append("  " + border_line("├", "┼", "┤"))
        cells = "│".join(render_cell(value) for value in board[row])
        lines.append(
            "  " + paint("│", fg=BORDER_COLOR) + cells + paint("│", fg=BORDER_COLOR)
        )
    lines.append("  " + border_line("└", "┴", "┘"))
    lines.append("")

    if message:
        color = GAME_OVER_COLOR if dead else MESSAGE_COLOR
        lines.append("  " + paint(message, fg=color, bold=True))
        lines.append("")

    lines.append(paint("  Управление: ← ↑ → ↓, WASD или HJKL", fg=245))
    lines.append(paint("  U — отмена   R — новая игра   Q — в меню", fg=245))

    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


_MENU_ITEMS = ("Новая игра", "Правила", "Выход")


def render_menu(selected, best):
    lines = [CLEAR, ""]
    lines.append("  " + paint(_TITLE.center(BOARD_WIDTH), fg=_TITLE_COLOR, bold=True))
    lines.append("")
    lines.append("  " + paint("терминальная версия".center(BOARD_WIDTH), fg=245))
    lines.append("")
    lines.append("")

    label_width = max(len(item) for item in _MENU_ITEMS)
    left = max(0, (BOARD_WIDTH - label_width - 2) // 2)
    for index, item in enumerate(_MENU_ITEMS):
        marker = "▸ " if index == selected else "  "
        text = marker + item.ljust(label_width)
        prefix = "  " + " " * left
        if index == selected:
            lines.append(prefix + paint(text, fg=235, bg=214, bold=True))
        else:
            lines.append(prefix + paint(text, fg=250))

    lines.append("")
    lines.append("  " + paint(f"Рекорд: {best}".center(BOARD_WIDTH), fg=214))
    lines.append("")
    lines.append(paint("  ↑ ↓ — выбор    Enter — подтвердить", fg=245))

    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


def render_rules():
    rules = [
        "Как играть",
        "",
        "Стрелками, WASD или HJKL двигайте плитки.",
        "После каждого хода появляется новая плитка.",
        "Две одинаковые плитки при столкновении",
        "сливаются в одну — число на ней удваивается.",
        "",
        "Цель — собрать плитку 2048.",
        "После победы можно продолжить игру.",
        "",
        "U — отменить ход",
        "R — начать заново",
        "Q — вернуться в меню",
    ]

    lines = [CLEAR, ""]
    lines.append("  " + paint(_TITLE.center(BOARD_WIDTH), fg=_TITLE_COLOR, bold=True))
    lines.append("")
    for index, rule in enumerate(rules):
        if index == 0:
            lines.append("  " + paint(rule.center(BOARD_WIDTH), fg=214, bold=True))
        else:
            lines.append("  " + rule)
    lines.append("")
    lines.append(paint("  Нажмите любую клавишу, чтобы вернуться...", fg=245))

    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


def main_menu(best):
    """Показывает меню. Возвращает True, если нужно начать игру."""
    selected = 0

    while True:
        render_menu(selected, best)
        key = read_key()

        if key == "up":
            selected = (selected - 1) % len(_MENU_ITEMS)
        elif key == "down":
            selected = (selected + 1) % len(_MENU_ITEMS)
        elif key == "q":
            return False
        elif key == "enter":
            item = _MENU_ITEMS[selected]
            if item == "Новая игра":
                return True
            if item == "Правила":
                render_rules()
                read_key()
            else:
                return False


# ---------------------------------------------------------------------------
# Логика игры
# ---------------------------------------------------------------------------

def new_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    spawn_tile(board)
    spawn_tile(board)
    return board


def empty_cells(board):
    return [
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
        if board[row][col] == 0
    ]


def spawn_tile(board):
    cells = empty_cells(board)
    if not cells:
        return
    row, col = random.choice(cells)
    board[row][col] = 4 if random.random() < 0.1 else 2


def merge_line(line):
    """Сдвигает и сливает одну линию по направлению к её началу."""
    numbers = [value for value in line if value]
    merged = []
    gained = 0
    skip = False

    for index, value in enumerate(numbers):
        if skip:
            skip = False
            continue
        if index + 1 < len(numbers) and numbers[index + 1] == value:
            doubled = value * 2
            merged.append(doubled)
            gained += doubled
            skip = True
        else:
            merged.append(value)

    merged.extend([0] * (SIZE - len(merged)))
    return merged, gained


def move(board, direction):
    """Делает ход. Возвращает (был ли ход, сколько очков получено)."""
    gained = 0
    moved = False

    for index in range(SIZE):
        if direction in ("left", "right"):
            line = list(board[index])
        else:
            line = [board[row][index] for row in range(SIZE)]

        target = line[::-1] if direction in ("right", "down") else line
        merged, points = merge_line(target)
        if direction in ("right", "down"):
            merged = merged[::-1]

        gained += points
        if merged != line:
            moved = True

        for position, value in enumerate(merged):
            if direction in ("left", "right"):
                board[index][position] = value
            else:
                board[position][index] = value

    return moved, gained


def is_game_over(board):
    if empty_cells(board):
        return False
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if col + 1 < SIZE and board[row][col + 1] == value:
                return False
            if row + 1 < SIZE and board[row + 1][col] == value:
                return False
    return True


def has_won(board):
    return any(value >= 2048 for row in board for value in row)


# ---------------------------------------------------------------------------
# Рекорд
# ---------------------------------------------------------------------------

def load_best():
    try:
        with open(BEST_FILE, encoding="utf-8") as file:
            return max(0, int(file.read().strip() or 0))
    except (OSError, ValueError):
        return 0


def save_best(score):
    try:
        with open(BEST_FILE, "w", encoding="utf-8") as file:
            file.write(str(score))
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Ввод с клавиатуры
# ---------------------------------------------------------------------------

_TERMINAL_STATE = None
_ARROWS = {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}
_WINDOWS_ARROWS = {"H": "up", "P": "down", "K": "left", "M": "right"}


def terminal_enter():
    global _TERMINAL_STATE
    if os.name != "nt":
        import termios
        import tty

        fd = sys.stdin.fileno()
        _TERMINAL_STATE = termios.tcgetattr(fd)
        tty.setcbreak(fd)
    if sys.stdout.isatty():
        sys.stdout.write("\x1b[?25l")  # спрятать курсор
        sys.stdout.flush()


def terminal_leave():
    global _TERMINAL_STATE
    if _TERMINAL_STATE is not None and os.name != "nt":
        import termios

        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _TERMINAL_STATE)
        _TERMINAL_STATE = None
    if sys.stdout.isatty():
        sys.stdout.write("\x1b[?25h\n")  # вернуть курсор
        sys.stdout.flush()


def read_key():
    if os.name == "nt":
        import msvcrt

        char = msvcrt.getwch()
        if char in ("\x00", "\xe0"):
            return _WINDOWS_ARROWS.get(msvcrt.getwch(), "")
        if char in ("\r", "\n"):
            return "enter"
        return _KEYMAP.get(char.lower(), char.lower())

    char = sys.stdin.read(1)
    if not char:
        return "q"
    if char == "\x1b":
        sequence = sys.stdin.read(2)
        return _ARROWS.get(sequence, "")
    if char in ("\r", "\n"):
        return "enter"
    return _KEYMAP.get(char.lower(), char.lower())


# ---------------------------------------------------------------------------
# Игровой цикл
# ---------------------------------------------------------------------------

def run_game():
    board = new_board()
    score = 0
    best = load_best()
    undo_stack = []
    won = False
    dead = False
    message = ""

    while True:
        render(board, score, best, message, dead)
        message = ""
        key = read_key()

        if key == "q":
            save_best(best)
            return

        if key == "r":
            board = new_board()
            score = 0
            undo_stack.clear()
            won = False
            dead = False
            continue

        if key == "u":
            if undo_stack:
                board, score = undo_stack.pop()
                dead = is_game_over(board)
                message = "Ход отменён"
            else:
                message = "Отменять пока нечего"
            continue

        if key not in _DIRECTIONS or dead:
            continue

        snapshot = ([row[:] for row in board], score)
        moved, gained = move(board, key)
        if not moved:
            message = "В эту сторону ходить нельзя"
            continue

        undo_stack.append(snapshot)
        if len(undo_stack) > 20:
            undo_stack.pop(0)

        score += gained
        if score > best:
            best = score
            save_best(best)

        spawn_tile(board)

        if not won and has_won(board):
            won = True
            message = "Вы собрали 2048! Можно играть дальше."

        if is_game_over(board):
            dead = True
            message = "Игра окончена! R — заново, U — отмена, Q — в меню"


def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Запустите игру в интерактивном терминале:")
        print("    python3 game_2048.py")
        return 1

    try:
        terminal_enter()
    except Exception:
        print("Не удалось включить режим терминала.")
        return 1

    try:
        while main_menu(load_best()):
            run_game()
    except KeyboardInterrupt:
        pass
    finally:
        terminal_leave()

    print("Спасибо за игру!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
