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
                counter[0] += 1
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

def generate_super_hard_puzzle(verbose=True):
    attempt = 0
    while True:
        attempt += 1
        if verbose and attempt % 10 == 0:
            print(f"🔄 Попытка #{attempt}")

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

        grid_copy = copy.deepcopy(grid)
        if not solve_with_counter(grid_copy):
            continue

        solution = copy.deepcopy(grid_copy)
        puzzle = copy.deepcopy(solution)
        cells = [(i, j) for i in range(SIZE) for j in range(SIZE)]
        random.shuffle(cells)
        clues = 81
        for row, col in cells:
            if clues <= 22:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            if count_solutions(copy.deepcopy(puzzle)) != 1:
                puzzle[row][col] = backup
            else:
                clues -= 1

        steps = [0]
        solve_with_counter(copy.deepcopy(puzzle), steps)

        if clues <= 22 and steps[0] > 1500:
            return puzzle, steps[0], clues

def print_grid(grid):
    for i in range(9):
        print(" ".join(str(n) if n != 0 else '.' for n in grid[i]))

def generate_with_timeout(timeout=60):
    attempt_count = 1
    while True:
        print(f"\nПопытка генерации #{attempt_count}")
        start_time = time.time()
        
        try:
            # Запускаем генерацию с таймаутом
            result = None
            def generate():
                nonlocal result
                result = generate_super_hard_puzzle(verbose=False)
            
            import threading
            thread = threading.Thread(target=generate)
            thread.start()
            thread.join(timeout=timeout)
            
            if thread.is_alive():
                print(f"⌛ Превышено время генерации ({timeout} сек). Пробуем снова...")
                attempt_count += 1
                continue
                
            if result:
                puzzle, steps, clues = result
                elapsed = time.time() - start_time
                print(f"\n✅ Сгенерировано за {elapsed:.2f} сек | Подсказок: {clues} | Шагов: {steps}")
                print_grid(puzzle)
                return puzzle
                
        except Exception as e:
            print(f"Ошибка при генерации: {e}. Пробуем снова...")
            attempt_count += 1

# Генерация и вывод
print("🚀 Генерация суперсложной судоку (максимум 60 секунд на попытку)...")
puzzle = generate_with_timeout()
