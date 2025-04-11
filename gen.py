import random
import copy
import time

SIZE = 9
BOX_SIZE = 3

def is_valid(grid, row, col, num):
    for i in range(SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = row - row % BOX_SIZE, col - col % BOX_SIZE
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(grid):
    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_with_counter(grid, counter=None):
    empty = find_empty(grid)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if counter is not None:
                counter[0] += 1  # считаем шаг
            if solve_with_counter(grid, counter):
                return True
            grid[row][col] = 0
    return False

def count_solutions(grid, limit=2):
    empty = find_empty(grid)
    if not empty:
        return 1
    row, col = empty
    count = 0
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count += count_solutions(grid, limit)
            if count >= limit:
                break
            grid[row][col] = 0
    grid[row][col] = 0
    return count

def generate_hard_puzzle():
    while True:
        # 1. Случайно заполняем 11 клеток
        grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        positions = random.sample(range(SIZE * SIZE), 11)
        for pos in positions:
            row, col = divmod(pos, SIZE)
            nums = list(range(1, 10))
            random.shuffle(nums)
            for num in nums:
                if is_valid(grid, row, col, num):
                    grid[row][col] = num
                    break

        # 2. Решаем
        grid_copy = copy.deepcopy(grid)
        if not solve_with_counter(grid_copy):
            continue  # нерешаемо

        solution = copy.deepcopy(grid_copy)

        # 3. Удаляем максимум
        puzzle = copy.deepcopy(solution)
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        clues = 81
        for row, col in cells:
            if clues <= 22:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            test_grid = copy.deepcopy(puzzle)
            if count_solutions(test_grid) != 1:
                puzzle[row][col] = backup
            else:
                clues -= 1

        # 4. Сложность: считаем шаги решения
        test_copy = copy.deepcopy(puzzle)
        steps = [0]
        solve_with_counter(test_copy, steps)

        if clues <= 22 and steps[0] > 300:
            return puzzle, steps[0], clues  # достаточно сложное

def print_grid(grid):
    for i in range(9):
        row = ''
        for j in range(9):
            val = grid[i][j]
            row += str(val) if val != 0 else '.'
            row += ' '
            if (j + 1) % 3 == 0 and j < 8:
                row += '| '
        print(row)
        if (i + 1) % 3 == 0 and i < 8:
            print('-' * 21)

# Генерация и вывод
sudoku, difficulty_score, clues = generate_hard_puzzle()
print(f"\n🧩 Сложная судоку | Подсказок: {clues} | Шагов решения: {difficulty_score}")
print_grid(sudoku)
