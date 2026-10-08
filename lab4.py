import os
import sys
import unittest
from typing import List, Dict, Any, Optional


def validate_scores(scores: Any) -> List[float]:
    """Возвращает проверенную копию последовательности баллов."""
    if not isinstance(scores, (list, tuple)):
        raise TypeError("scores должен быть списком или кортежем")
    checked = []
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not 0 <= score <= 100:
            raise ValueError("Балл должен быть от 0 до 100")
        checked.append(float(score))
    return checked

def validate_student(student: Any) -> None:
    """Проверяет обязательные поля записи студента."""
    if not isinstance(student, dict):
        raise TypeError("Запись студента должна быть словарём")
    required = {"id", "name", "scores"}
    missing = required - student.keys()
    if missing:
        raise ValueError(f"Отсутствуют поля: {sorted(list(missing))}")


# --- 1.2. Модуль calculations.py ---
PASSING_AVERAGE = 50.0

def calculate_average(scores: List[float]) -> Optional[float]:
    """Возвращает среднее или None для пустой последовательности."""
    return sum(scores) / len(scores) if scores else None

def determine_status(average: Optional[float]) -> str:
    """Возвращает статус допуска по среднему баллу."""
    if average is None:
        return "нет данных"
    return "допущен" if average >= PASSING_AVERAGE else "не допущен"

def determine_letter_grade(average: Optional[float]) -> str:
    """Индивидуальное расширение (Вариант 1): Возвращает буквенную оценку."""
    if average is None:
        return "N/A"
    if average >= 90.0:
        return "A"
    elif average >= 80.0:
        return "B"
    elif average >= 70.0:
        return "C"
    elif average >= 50.0:
        return "D"
    else:
        return "F"


# --- 1.3. Модуль rating.py ---
def build_student_result(student: Dict[str, Any]) -> Dict[str, Any]:
    """Формирует новую итоговую запись одного студента."""
    validate_student(student)
    scores = validate_scores(student["scores"])
    average = calculate_average(scores)
    return {
        "id": student["id"],
        "name": student["name"],
        "average": average,
        "status": determine_status(average),
        "letter_grade": determine_letter_grade(average)
    }

def _sort_key(item: Dict[str, Any]):
    """Внутренний ключ для сортировки рейтинга."""
    average = item["average"]
    return average is not None, average or 0.0

def build_rating(students: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает рейтинг, не изменяя исходные записи."""
    results = [build_student_result(item) for item in students]
    return sorted(results, key=_sort_key, reverse=True)


# --- 1.4. Модуль report.py ---
def format_average(value: Optional[float]) -> str:
    """Форматирует числовое значение среднего балла."""
    return "-" if value is None else f"{value:.2f}"

def format_rating(rows: List[Dict[str, Any]]) -> str:
    """Формирует текстовое представление рейтинга группы."""
    lines = ["Рейтинг группы"]
    for position, row in enumerate(rows, start=1):
        average = format_average(row["average"])
        lines.append(
            f"{position}. {row['name']}: {average} | Оценка: {row['letter_grade']} | Status: {row['status']}"
        )
    return "\n".join(lines)


# --- 1.5. Модуль main.py ---
def load_demo_data() -> List[Dict[str, Any]]:
    """Возвращает демонстрационные данные студентов."""
    return [
        {"id": 101, "name": "Amina", "scores": [88, 92, 79]},
        {"id": 102, "name": "Dias", "scores": [45, 52, 48]},
        {"id": 103, "name": "Mira", "scores": []},
        {"id": 104, "name": "Ilyas", "scores": [95, 98, 100]}
    ]

def run_app():
    """Точка входа приложения."""
    students = load_demo_data()
    rating = build_rating(students)
    print(format_rating(rating))



# РАЗДЕЛ 2. АВТОМАТИЧЕСКИЕ ТЕСТЫ (TESTS/TEST_RATING.PY)


class RatingTests(unittest.TestCase):
    
    def test_empty_average(self):
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        self.assertEqual(determine_status(49.99), "не допущен")
        self.assertEqual(determine_status(50.0), "допущен")

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_source_is_not_changed(self):
        students = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        before = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        build_rating(students)
        self.assertEqual(students, before)

    # Тесты для индивидуального варианта № 1 (Буквенная оценка)
    def test_letter_grades(self):
        self.assertEqual(determine_letter_grade(95.0), "A")
        self.assertEqual(determine_letter_grade(85.0), "B")
        self.assertEqual(determine_letter_grade(75.0), "C")
        self.assertEqual(determine_letter_grade(60.0), "D")
        self.assertEqual(determine_letter_grade(40.0), "F")
        self.assertEqual(determine_letter_grade(None), "N/A")



# РАЗДЕЛ 3. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ СОЗДАНИЯ ФИЗИЧЕСКОЙ СТРУКТУРЫ ПАКЕТА


def generate_package_files():
    """Создает реальную файловую структуру пакета lab4_project на диске."""
    base_dir = "lab4_project"
    pkg_dir = os.path.join(base_dir, "university_rating")
    tests_dir = os.path.join(base_dir, "tests")
    
    os.makedirs(pkg_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)
    
    files = {
        os.path.join(pkg_dir, "__init__.py"): 'from .rating import build_rating, build_student_result\n__all__ = ["build_rating", "build_student_result"]\n',
        os.path.join(pkg_dir, "validation.py"): '''def validate_scores(scores):\n    if not isinstance(scores, (list, tuple)):\n        raise TypeError("scores должен быть списком или кортежем")\n    checked = []\n    for score in scores:\n        if isinstance(score, bool) or not isinstance(score, (int, float)):\n            raise TypeError("Балл должен быть числом")\n        if not 0 <= score <= 100:\n            raise ValueError("Балл должен быть от 0 до 100")\n        checked.append(float(score))\n    return checked\n\ndef validate_student(student):\n    if not isinstance(student, dict):\n        raise TypeError("Запись студента должна быть словарём")\n    required = {"id", "name", "scores"}\n    missing = required - student.keys()\n    if missing:\n        raise ValueError(f"Отсутствуют поля: {sorted(list(missing))}")\n''',
        os.path.join(pkg_dir, "calculations.py"): '''PASSING_AVERAGE = 50.0\n\ndef calculate_average(scores):\n    return sum(scores) / len(scores) if scores else None\n\ndef determine_status(average):\n    if average is None:\n        return "нет данных"\n    return "допущен" if average >= PASSING_AVERAGE else "не допущен"\n\ndef determine_letter_grade(average):\n    if average is None: return "N/A"\n    if average >= 90.0: return "A"\n    elif average >= 80.0: return "B"\n    elif average >= 70.0: return "C"\n    elif average >= 50.0: return "D"\n    else: return "F"\n''',
        os.path.join(pkg_dir, "rating.py"): '''from .calculations import calculate_average, determine_status, determine_letter_grade\nfrom .validation import validate_scores, validate_student\n\ndef build_student_result(student):\n    validate_student(student)\n    scores = validate_scores(student["scores"])\n    average = calculate_average(scores)\n    return {\n        "id": student["id"],\n        "name": student["name"],\n        "average": average,\n        "status": determine_status(average),\n        "letter_grade": determine_letter_grade(average)\n    }\n\ndef _sort_key(item):\n    average = item["average"]\n    return average is not None, average or 0.0\n\ndef build_rating(students):\n    results = [build_student_result(item) for item in students]\n    return sorted(results, key=_sort_key, reverse=True)\n''',
        os.path.join(pkg_dir, "report.py"): '''def format_average(value):\n    return "-" if value is None else f"{value:.2f}"\n\ndef format_rating(rows):\n    lines = ["Рейтинг группы"]\n    for position, row in enumerate(rows, start=1):\n        average = format_average(row["average"])\n        lines.append(f"{position}. {row[\'name\']}: {average} | Оценка: {row[\'letter_grade\']} | Status: {row[\'status\']}")\n    return "\\n".join(lines)\n''',
        os.path.join(pkg_dir, "main.py"): '''from .rating import build_rating\nfrom .report import format_rating\n\ndef load_demo_data():\n    return [\n        {"id": 101, "name": "Amina", "scores": [88, 92, 79]},\n        {"id": 102, "name": "Dias", "scores": [45, 52, 48]},\n        {"id": 103, "name": "Mira", "scores": []},\n        {"id": 104, "name": "Ilyas", "scores": [95, 98, 100]}\n    ]\n\ndef main():\n    students = load_demo_data()\n    rating = build_rating(students)\n    print(format_rating(rating))\n\nif __name__ == "__main__":\n    main()\n''',
        os.path.join(tests_dir, "test_rating.py"): '''import unittest\nfrom university_rating.calculations import calculate_average, determine_status, determine_letter_grade\nfrom university_rating.rating import build_rating\nfrom university_rating.validation import validate_scores\n\nclass RatingTests(unittest.TestCase):\n    def test_empty_average(self):\n        self.assertIsNone(calculate_average([]))\n    def test_status_boundary(self):\n        self.assertEqual(determine_status(49.99), "не допущен")\n        self.assertEqual(determine_status(50.0), "допущен")\n    def test_invalid_score(self):\n        with self.assertRaises(ValueError):\n            validate_scores([80, 101])\n    def test_letter_grades(self):\n        self.assertEqual(determine_letter_grade(95.0), "A")\n        self.assertEqual(determine_letter_grade(40.0), "F")\n'''
    }
    
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"[+] Структура пакета успешно сгенерирована в каталоге: {os.path.abspath(base_dir)}")



# РАЗДЕЛ 4. ГЛАВНЫЙ БЛОК ВЫПОЛНЕНИЯ


if __name__ == "__main__":
    print("=== 1. ЗАПУСК ПРИЛОЖЕНИЯ (UNIVERSITY_RATING) ===")
    run_app()
    print()

    print("=== 2. ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ (UNITTEST) ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(RatingTests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print()

    print("=== 3. СОЗДАНИЕ ФИЗИЧЕСКИХ ФАЙЛОВ ПАКЕТА ДЛЯ РЕПОЗИТОРИЯ ===")
    generate_package_files()
