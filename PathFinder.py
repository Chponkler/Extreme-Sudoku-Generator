from constraint import Problem, AllDifferentConstraint
import matplotlib.pyplot as plt

# ---------- Парсинг строки ----------
def parse_sudoku_from_text(s):
    s = ''.join(c if c.isdigit() else '.' for c in s)
    if len(s) != 81:
        raise ValueError("❌ Ошибка: строка должна содержать ровно 81 символ.")
    return [[int(c) if c != '.' else 0 for c in s[i*9:(i+1)*9]] for i in range(9)]

# ---------- Решение судоку ----------
def solve_sudoku(grid):
    problem = Problem()
    
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val == 0:
                problem.addVariable((r, c), range(1, 10))
            else:
                problem.addVariable((r, c), [val])

    for r in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(r, c) for c in range(9)])
    for c in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(r, c) for r in range(9)])
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [(r, c) for r in range(br, br+3) for c in range(bc, bc+3)]
            problem.addConstraint(AllDifferentConstraint(), block)

    solution = problem.getSolution()
    if not solution:
        raise ValueError("❌ Судоку не имеет допустимого решения.")

    return [[solution[(r, c)] for c in range(9)] for r in range(9)]

# ---------- Визуализация ----------
def visualize_sudoku(grid, title="Судоку"):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title(title)

    for i in range(10):
        lw = 2 if i % 3 == 0 else 1
        ax.axhline(i, lw=lw, color='black')
        ax.axvline(i, lw=lw, color='black')

    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val != 0:
                ax.text(j + 0.5, 8.5 - i, str(val), va='center', ha='center', fontsize=14)

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.axis('off')
    plt.show()

# ---------- Основной код ----------
if __name__ == "__main__":
    print("🧩 Введите судоку как строку из 81 символа.")
    print("    Цифры 1–9 — заполненные ячейки.")
    print("    Точки или любые другие символы — пустые ячейки.")
    print("    Пример:\n        3........97..1....6..583...2.....9..5..621..3..8.....5...435..2....9..56........1\n")

    user_input = input("Вставьте вашу строку судоку: ").strip()
    try:
        grid = parse_sudoku_from_text(user_input)
        print("\n🔍 Исходное судоку:")
        visualize_sudoku(grid, "Исходное судоку")

        solved = solve_sudoku(grid)

        print("✅ Решено:")
        visualize_sudoku(solved, "Решение")
    except Exception as e:
        print(f"\n{e}")
