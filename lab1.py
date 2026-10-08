from typing import List, Optional

print("--- 1. ИМПЕРАТИВНЫЙ СТИЛЬ ---")
numbers = [4, 7, 2, 9, 12, 5, 8, 3]
total = 0
even_numbers = []
even_squares = []
iterations_count = 0

for number in numbers:
    iterations_count += 1
    if number % 2 == 0:
        even_numbers.append(number)
        square_val = number ** 2
        even_squares.append(square_val)
        total += square_val

print("Чётные числа:", even_numbers)
print("Квадраты чётных чисел:", even_squares)
print("Сумма квадратов:", total)
print("Количество итераций:", iterations_count)
print()


print("--- 2. ПРОЦЕДУРНЫЙ СТИЛЬ ---")
def is_even(number: int) -> bool:
    return number % 2 == 0

def square(number: int) -> int:
    return number ** 2

def get_even_numbers(values: List[int]) -> List[int]:
    return [n for n in values if is_even(n)]

def sum_even_squares(values: List[int]) -> int:
    total_sum = 0
    for number in values:
        if is_even(number):
            total_sum += square(number)
    return total_sum

# Проверка функций отдельными вызовами
print("Проверка is_even(4):", is_even(4))
print("Проверка square(4):", square(4))
print("Чётные числа:", get_even_numbers(numbers))
print("Сумма квадратов чётных чисел:", sum_even_squares(numbers))
print()


print("--- 3. ОБЪЕКТНО-ОРИЕНТИРОВАННЫЙ СТИЛЬ ---")
class NumberCollection:
    def __init__(self, numbers_list: List[int]) -> None:
        self._numbers = list(numbers_list)

    def get_even_numbers(self) -> List[int]:
        return [n for n in self._numbers if n % 2 == 0]

    def sum_even_squares(self) -> int:
        total_sum = 0
        for number in self._numbers:
            if number % 2 == 0:
                total_sum += number ** 2
        return total_sum

    def count_even_numbers(self) -> int:
        return len(self.get_even_numbers())

    def find_maximum(self) -> Optional[int]:
        return max(self._numbers) if self._numbers else None

    def calculate_average(self) -> float:
        return sum(self._numbers) / len(self._numbers) if self._numbers else 0.0

collection1 = NumberCollection(numbers)
print("Коллекция 1:")
print("  Чётные числа:", collection1.get_even_numbers())
print("  Сумма квадратов чётных:", collection1.sum_even_squares())
print("  Количество чётных чисел:", collection1.count_even_numbers())
print("  Максимум:", collection1.find_maximum())
print("  Среднее значение:", collection1.calculate_average())

collection2 = NumberCollection([10, 15, 20, 25, 30])
print("Коллекция 2 (другой набор):")
print("  Чётные числа:", collection2.get_even_numbers())
print("  Сумма квадратов чётных:", collection2.sum_even_squares())
print()


print("--- 4. ФУНКЦИОНАЛЬНЫЙ СТИЛЬ ---")
# Через map/filter
result_map_filter = sum(
    map(
        lambda number: number ** 2,
        filter(lambda number: number % 2 == 0, numbers)
    )
)

# Через генераторное выражение
result_gen = sum(n ** 2 for n in numbers if n % 2 == 0)

# Список квадратов чётных чисел
even_squares_list = [n ** 2 for n in numbers if n % 2 == 0]

print("Результат (map/filter):", result_map_filter)
print("Результат (генератор):", result_gen)
print("Список квадратов чётных чисел:", even_squares_list)
print()



print("--- ИНДИВИДУАЛЬНЫЙ ВАРИАНТ 1 ---")
data = [-5, 4, 3, -2, 0, 8, -1, 6]

# 1. Императивный стиль
var1_imp_total = 0
for x in data:
    if x > 0:
        var1_imp_total += x ** 2
print("1. Императивный стиль -> Результат:", var1_imp_total)

# 2. Процедурный стиль
def is_positive(x: int) -> bool:
    return x > 0

def sum_positive_squares(values: List[int]) -> int:
    acc = 0
    for x in values:
        if is_positive(x):
            acc += x ** 2
    return acc

print("2. Процедурный стиль -> Результат:", sum_positive_squares(data))

# 3. Функциональный стиль
var1_func_result = sum(x ** 2 for x in data if x > 0)
print("3. Функциональный стиль -> Результат:", var1_func_result)
print()



import tkinter as tk
from tkinter import messagebox

def run_gui():
    def calculate():
        input_text = entry.get().strip()
        try:
            if input_text:
                nums = [int(x) for x in input_text.split()]
            else:
                nums = numbers

            res = sum(n ** 2 for n in nums if n % 2 == 0)
            result_label.config(text=f"Результат: {res}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа через пробел.")

    def clear():
        entry.delete(0, tk.END)
        result_label.config(text="Нажмите кнопку")

    root = tk.Tk()
    root.title("Парадигмы программирования")

    tk.Label(root, text="Введите числа через пробел:").pack(padx=20, pady=5)
    entry = tk.Entry(root, width=40)
    entry.pack(padx=20, pady=5)

    result_label = tk.Label(root, text="Нажмите кнопку")
    result_label.pack(padx=20, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Вычислить", command=calculate).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Очистить", command=clear).pack(side=tk.LEFT, padx=5)

    root.mainloop()

# run_gui() 
