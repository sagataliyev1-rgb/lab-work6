print("=== ЗАДАНИЕ 1 ===")
x = 10
x = x + 5
x = x * 2
x = x - 8
x = x // 2
print("Финальное значение x:", x)  # Ожидается: 11
print()


print("=== ЗАДАНИЕ 2 ===")
price = 2500.0
quantity = 4
discount_percent = 10.0

total_no_discount = price * quantity
discount_amount = total_no_discount * (discount_percent / 100)
final_price = total_no_discount - discount_amount

print(f"Цена товара: {price}")
print(f"Количество: {quantity}")
print(f"Скидка: {discount_percent}%")
print(f"Стоимость без скидки: {total_no_discount}")
print(f"Размер скидки: {discount_amount}")
print(f"К оплате: {final_price}")
print()


print("=== ЗАДАНИЕ 3 ===")
score = 85  # Пример ввода тестового балла

if 0 <= score <= 100:
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 50:
        grade = "C"
    else:
        grade = "F"
    print(f"Балл: {score}, Оценка: {grade}")
else:
    print("Ошибка: балл должен быть в диапазоне от 0 до 100.")
print()


print("=== ЗАДАНИЕ 4 ===")
numbers = [12, 5, 8, 3, 21, 0, 14, -7]

total_sum = 0
positive_sum = 0
positive_count = 0
negative_count = 0
zero_count = 0

print("Таблица изменения состояния переменной total_sum на каждой итерации:")
print("Итерация | Элемент | total_sum (до) | total_sum (после)")
print("-" * 52)

for i, num in enumerate(numbers, 1):
    prev_sum = total_sum
    total_sum += num
    
    if num > 0:
        positive_sum += num
        positive_count += 1
    elif num < 0:
        negative_count += 1
    else:
        zero_count += 1
        
    print(f"{i:8d} | {num:7d} | {prev_sum:14d} | {total_sum:17d}")

print("-" * 52)
print("Сумма всех чисел:", total_sum)
print("Сумма положительных чисел:", positive_sum)
print("Количество положительных чисел:", positive_count)
print("Количество отрицательных чисел:", negative_count)
print("Количество нулей:", zero_count)
print()


print("=== ЗАДАНИЕ 5 ===")
scores = [67, 82, 45, 91, 76, 88, 54]
maximum = scores[0]

print("score | maximum до | score > maximum | maximum после")
print("-" * 50)

for score_val in scores:
    max_before = maximum
    is_greater = score_val > maximum
    if is_greater:
        maximum = score_val
    print(f"{score_val:5d} | {max_before:10d} | {str(is_greater):15s} | {maximum:13d}")

print("-" * 50)
print("Найденный максимум:", maximum)
print()


print("=== ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ № 1 (Банковский счет) ===")
balance = 50000.0  # Начальный баланс на счете
withdraw_amount = 15000.0  # Запрашиваемая сумма снятия

print(f"Текущий баланс: {balance} тг")
print(f"Запрос на снятие: {withdraw_amount} тг")

# Проверка условия возможности снятия средств
if withdraw_amount <= 0:
    print("Ошибка: сумма для снятия должна быть положительной.")
elif withdraw_amount <= balance:
    # Изменение состояния баланса только при достаточном количестве средств
    balance = balance - withdraw_amount
    print("Операция прошла успешно!")
    print(f"Новый баланс: {balance} тг")
else:
    print("Ошибка: недостаточно средств на счете для совершения операции.")

print()


print("=== ОБЯЗАТЕЛЬНОЕ СРАВНИТЕЛЬНОЕ ЗАДАНИЕ ===")
comp_numbers = [-4, 7, -2, 10, 5, -8]

# 1. Императивный стиль
comp_total_imp = 0
for number in comp_numbers:
    if number > 0:
        comp_total_imp = comp_total_imp + number
print("Императивный стиль -> Результат:", comp_total_imp)

# 2. Декларативный стиль
comp_total_decl = sum(number for number in comp_numbers if number > 0)
print("Декларативный стиль -> Результат:", comp_total_decl)
