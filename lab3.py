"""
===============================================================================
АО «АЛМАТИНСКИЙ ТЕХНОЛОГИЧЕСКИЙ УНИВЕРСИТЕТ»
Кафедра «Информационные системы»
Дисциплина: Парадигмы программирования
ЛАБОРАТОРНАЯ РАБОТА № 3
Процедурное программирование: декомпозиция, процедуры, функции и области видимости

Студент: Сагаталиев Ильяс
Вариант: 1 (Посещаемость)
===============================================================================

1. НАЗНАЧЕНИЕ И ЦЕЛЬ РАБОТЫ:
Научиться проектировать процедурную программу на Python как систему небольших 
функций с явными контрактами, параметрами, возвращаемыми значениями и контролируемыми 
областями видимости без применения глобального изменяемого состояния.

2. ТАБЛИЦА ДЕКОМПОЗИЦИИ ФУНКЦИИ ИНДИВИДУАЛЬНОГО ВАРИАНТА № 1:
+------------------------+---------------------------------------+-----------------------------+---------------------------+-----------------------+
| Имя функции            | Назначение                            | Входные параметры           | Возвращаемое значение     | Исключения / Ошибки   |
+------------------------+---------------------------------------+-----------------------------+---------------------------+-----------------------+
| validate_mark          | Валидация отметки посещаемости        | mark (str)                  | float (1.0, 0.0 или 0.5)  | TypeError, ValueError |
| attendance_rate        | Расчет процента посещаемости          | marks (List[str])           | Optional[float] (0..100)  | TypeError, ValueError |
| determine_access       | Определение статуса допуска           | rate (Optional[float]), min | str ("допущен", и т.д.)   | ValueError            |
| summarize_student_att  | Сводка по студенту                    | student (dict), min_rate    | dict с метриками          | TypeError, ValueError |
| build_attendance_rating| Построение и сортировка рейтинга      | students (List[dict])       | List[dict] (по убыванию)  | TypeError             |
| format_attendance_rep  | Формирование текстового отчета        | rating (List[dict])         | str (многострочная строка)| None                  |
+------------------------+---------------------------------------+-----------------------------+---------------------------+-----------------------+

3. ПОЯСНЕНИЕ ОБЛАСТЕЙ ВИДИМОСТИ (LEGB):
- Local (L): Переменные, объявленные внутри функций (например, `checked_rates`, `total_points`).
- Enclosing (E): Охватывающая область видимости при вложенных функциях (демонстрируется в `make_call_counter`).
- Global (G): Переменные уровня модуля (например, имена самих функций).
- Built-in (B): Встроенные функции Python (`len`, `sum`, `isinstance`, `ValueError`).
В работе не используются `global` или глобальные изменяемые структуры данных для исключения неявных зависимостей.

4. ВЫВОД О КАЧЕСТВЕ ДЕКОМПОЗИЦИИ:
Декомпозиция задачи на небольшие чистые функции позволила полностью разделить вычислительную
логику и ввод-вывод. Каждая функция выполняет ровно одну подзадачу, получает необходимые данные
через параметры и не изменяет исходные коллекции. Благодаря этому программу легко тестировать,
сопровождать и расширять без риска возникновения побочных эффектов.

5. ОТВЕТЫ НА КОНТРОЛЬНЫЕ ВОПРОСЫ:
1. Процедурная декомпозиция — это разделение крупной программы на систему подпрограмм (функций),
   каждая из которых выполняет конкретную изолированную задачу.
2. Процедура выполняет действие с наблюдаемым побочным эффектом (например, печать), тогда как функция
   возвращает результат через `return` без побочных эффектов.
3. Параметр — это переменная в объявлении функции; аргумент — конкретное значение, передаваемое при вызове.
4. Функция без явного `return` возвращает значение `None`.
5. Побочный эффект — это любое изменение внешнего состояния (модификация глобальной переменной, вывод на экран, запись в файл).
6. Python ищет имена в следующем порядке: Local -> Enclosing -> Global -> Built-in (правило LEGB).
7. Присваивание внутри функции создает локальную переменную, чтобы предотвратить нечаянное изменение внешних переменных.
8. `global` и `nonlocal` применяются для явного переназначения переменных в глобальной или охватывающей области видимости.
9. Отделение I/O от вычислений позволяет тестировать логику автоматическими тестами без перехвата консоли.
10. Именованные аргументы повышают читаемость вызовов и позволяют передавать параметры в произвольном порядке.
11. Изменяемые значения (списки, словари) как параметры по умолчанию сохраняются между вызовами, что приводит к багам.
12. Тесты позволяют изолированно проверить каждую функцию на нормальных, граничных и ошибочных данных.
===============================================================================
"""

import unittest
from typing import List, Dict, Any, Optional

# =============================================================================
# РАЗДЕЛ 1. СКВОЗНАЯ ЗАДАЧА (Университетская ведомость)
# =============================================================================

def validate_score(score: Any) -> float:
    """Проверяет и возвращает float для корректного балла (0..100)."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Балл должен быть числом")
    if not 0 <= score <= 100:
        raise ValueError("Балл должен быть от 0 до 100")
    return float(score)

def calculate_average(scores: List[Any]) -> Optional[float]:
    """Возвращает средний балл или None для пустого списка."""
    checked = [validate_score(s) for s in scores]
    if not checked:
        return None
    return sum(checked) / len(checked)

def determine_status(average: Optional[float], pass_mark: float = 50.0) -> str:
    """Определяет статус допуска по среднему баллу."""
    if not 0 <= pass_mark <= 100:
        raise ValueError("Порог должен быть от 0 до 100")
    if average is None:
        return "нет данных"
    return "допущен" if average >= pass_mark else "не допущен"

def summarize_student(student: Dict[str, Any], pass_mark: float = 50.0) -> Dict[str, Any]:
    """Возвращает новую сводную запись студента."""
    student_id = student.get("id")
    name = student.get("name")
    
    if isinstance(student_id, bool) or not isinstance(student_id, int):
        raise TypeError("Идентификатор должен быть целым числом")
    if student_id <= 0 or not isinstance(name, str) or not name.strip():
        raise ValueError("Некорректные данные студента")
        
    scores = student.get("scores", [])
    average = calculate_average(scores)
    
    return {
        "id": student_id,
        "name": name.strip(),
        "average": average,
        "status": determine_status(average, pass_mark)
    }

def build_rating(students: List[Dict[str, Any]], pass_mark: float = 50.0) -> List[Dict[str, Any]]:
    """Формирует и сортирует рейтинг студентов."""
    summaries = [summarize_student(s, pass_mark) for s in students]
    return sorted(
        summaries,
        key=lambda item: (
            item["average"] is not None,
            item["average"] or 0.0
        ),
        reverse=True
    )

def format_report(rating: List[Dict[str, Any]]) -> str:
    """Формирует текстовый отчёт без печати в консоль."""
    lines = []
    for pos, item in enumerate(rating, start=1):
        avg_str = "" if item["average"] is None else f"{item['average']:.2f}"
        lines.append(f"{pos}. {item['name']}: {avg_str}; {item['status']}")
    return "\n".join(lines)


# =============================================================================
# РАЗДЕЛ 2. ИНДИВИДУАЛЬНЫЙ ВАРИАНТ № 1 (Посещаемость)
# Отметки: "P" (присутствовал = 1.0), "A" (отсутствовал = 0.0), "E" (уважительная = 0.5)
# =============================================================================

def validate_mark(mark: Any) -> float:
    """Преобразует строковую отметку посещаемости в числовые баллы."""
    if not isinstance(mark, str):
        raise TypeError("Отметка посещаемости должна быть строкой")
    
    formatted = mark.strip().upper()
    if formatted == "P":
        return 1.0
    elif formatted == "A":
        return 0.0
    elif formatted == "E":
        return 0.5
    else:
        raise ValueError(f"Неизвестная отметка посещаемости: {mark}")

def attendance_rate(marks: List[Any]) -> Optional[float]:
    """Вычисляет процент посещаемости студента (0..100%)."""
    if not isinstance(marks, list):
        raise TypeError("Список отметок должен быть типом list")
    if not marks:
        return None
        
    numeric_marks = [validate_mark(m) for m in marks]
    return (sum(numeric_marks) / len(numeric_marks)) * 100.0

def determine_access(rate: Optional[float], min_rate: float = 70.0) -> str:
    """Определяет статус допуска на основе процента посещаемости."""
    if not 0 <= min_rate <= 100:
        raise ValueError("Минимальный порог должен быть от 0 до 100")
    if rate is None:
        return "нет данных"
    return "допущен" if rate >= min_rate else "не допущен"

def summarize_student_att(student: Dict[str, Any], min_rate: float = 70.0) -> Dict[str, Any]:
    """Формирует сводную карточку посещаемости студента."""
    s_id = student.get("id")
    name = student.get("name")
    
    if isinstance(s_id, bool) or not isinstance(s_id, int) or s_id <= 0:
        raise ValueError("Идентификатор должен быть положительным целым числом")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Имя не может быть пустым")
        
    marks = student.get("marks", [])
    rate = attendance_rate(marks)
    
    return {
        "id": s_id,
        "name": name.strip(),
        "rate": rate,
        "status": determine_access(rate, min_rate)
    }

def build_attendance_rating(students: List[Dict[str, Any]], min_rate: float = 70.0) -> List[Dict[str, Any]]:
    """Строит рейтинг студентов по проценту посещаемости."""
    summaries = [summarize_student_att(s, min_rate) for s in students]
    return sorted(
        summaries,
        key=lambda x: (
            x["rate"] is not None,
            x["rate"] or 0.0
        ),
        reverse=True
    )

def format_attendance_report(rating: List[Dict[str, Any]]) -> str:
    """Форматирует сводный отчёт по посещаемости."""
    lines = []
    for pos, item in enumerate(rating, start=1):
        rate_str = "нет данных" if item["rate"] is None else f"{item['rate']:.1f}%"
        lines.append(f"{pos}. {item['name']} | Посещаемость: {rate_str} | Статус: {item['status']}")
    return "\n".join(lines)


# =============================================================================
# РАЗДЕЛ 3. ДЕМОНСТРАЦИЯ ОБЛАСТЕЙ ВИДИМОСТИ (LEGB)
# =============================================================================

def make_call_counter():
    """Демонстрация Enclosing (E) и nonlocal."""
    count = 0
    def register_call():
        nonlocal count
        count += 1
        return count
    return register_call


# =============================================================================
# РАЗДЕЛ 4. АВТОМАТИЧЕСКИЕ ТЕСТЫ (UNITTEST)
# =============================================================================

class TestAttendanceSystem(unittest.TestCase):
    
    # 1. Нормальный сценарий
    def test_attendance_rate_normal(self):
        marks = ["P", "P", "A", "E"]  # 1 + 1 + 0 + 0.5 = 2.5 / 4 = 62.5%
        self.assertAlmostEqual(attendance_rate(marks), 62.5)

    # 2. Граничный сценарий (100% посещаемость)
    def test_attendance_rate_full(self):
        marks = ["P", "P", "P"]
        self.assertEqual(attendance_rate(marks), 100.0)

    # 3. Пустой список
    def test_empty_marks(self):
        self.assertIsNone(attendance_rate([]))

    # 4. Ошибочный сценарий: неверная отметка
    def test_invalid_mark_value(self):
        with self.assertRaises(ValueError):
            attendance_rate(["P", "INVALID"])

    # 5. Ошибочный сценарий: неверный тип данных
    def test_invalid_mark_type(self):
        with self.assertRaises(TypeError):
            attendance_rate(["P", 123])

    # 6. Проверка неизменяемости входных данных
    def test_input_immutability(self):
        original = ["P", "A", "E"]
        copy_original = list(original)
        attendance_rate(original)
        self.assertEqual(original, copy_original)


# =============================================================================
# РАЗДЕЛ 5. ТОЧКА ВХОДА MAIN
# =============================================================================

def main():
    print("=== 1. ВЫПОЛНЕНИЕ СКВОЗНОЙ ЗАДАЧИ ===")
    demo_students = [
        {"id": 101, "name": "Amina", "scores": [88, 92, 79]},
        {"id": 102, "name": "Dias", "scores": [45, 52, 48]},
        {"id": 103, "name": "Mira", "scores": []},
    ]
    rating = build_rating(demo_students, pass_mark=50)
    print(format_report(rating))
    print()

    print("=== 2. ВЫПОЛНЕНИЕ ИНДИВИДУАЛЬНОГО ВАРИАНТА № 1 (ПОСЕЩАЕМОСТЬ) ===")
    attendance_data = [
        {"id": 1, "name": "Ильяс", "marks": ["P", "P", "P", "E"]},
        {"id": 2, "name": "Данияр", "marks": ["A", "A", "P", "A"]},
        {"id": 3, "name": "Аружан", "marks": ["P", "P", "P", "P"]},
        {"id": 4, "name": "Нурсултан", "marks": []},
    ]
    att_rating = build_attendance_rating(attendance_data, min_rate=70.0)
    print(format_attendance_report(att_rating))
    print()

    print("=== 3. ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAttendanceSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    main()
