import random
from dataclasses import dataclass, field
from typing import List, Callable, Dict, Set, Optional
from abc import ABC, abstractmethod


# ==========================================
# 1. Модели данных (Question, Ticket)
# ==========================================

@dataclass(frozen=True)
class Question:
    id: int
    text: str
    topic: str
    difficulty: int  # Например: 1 - легкий, 2 - средний, 3 - сложный

    def __hash__(self):
        return hash(self.id)


@dataclass
class Ticket:
    ticket_id: int
    questions: List[Question] = field(default_factory=list)

    def topics_covered(self) -> Set[str]:
        return {q.topic for q in self.questions}

    def total_difficulty(self) -> int:
        return sum(q.difficulty for q in self.questions)


# ==========================================
# 2. Функции высшего порядка (Фильтры)
# ==========================================

# Тип для предиката фильтрации
QuestionFilter = Callable[[Question], bool]

def filter_by_topic(topic: str) -> QuestionFilter:
    """Возвращает функцию-предикат для фильтрации по теме."""
    return lambda q: q.topic == topic

def filter_by_difficulty(min_diff: int, max_diff: int) -> QuestionFilter:
    """Возвращает функцию-предикат для фильтрации по сложности."""
    return lambda q: min_diff <= q.difficulty <= max_diff

def combine_filters(*filters: QuestionFilter) -> QuestionFilter:
    """Компоновка нескольких фильтров в один (ФВП)."""
    return lambda q: all(f(q) for f in filters)

def apply_filter(questions: List[Question], predicate: QuestionFilter) -> List[Question]:
    """Применение фильтра к списку вопросов."""
    return [q for q in questions if predicate(q)]


# ==========================================
# 3. Стратегии генерации билетов (SelectionStrategy)
# ==========================================

class SelectionStrategy(ABC):
    @abstractmethod
    def generate_ticket(
        self,
        ticket_id: int,
        bank: List[Question],
        questions_per_ticket: int,
        used_questions: Set[int]
    ) -> Optional[Ticket]:
        pass


class RandomStrategy(SelectionStrategy):
    """Случайный выбор вопросов с контролем повторов."""
    
    def generate_ticket(
        self,
        ticket_id: int,
        bank: List[Question],
        questions_per_ticket: int,
        used_questions: Set[int]
    ) -> Optional[Ticket]:
        available = [q for q in bank if q.id not in used_questions]
        if len(available) < questions_per_ticket:
            return None
        
        selected = random.sample(available, questions_per_ticket)
        for q in selected:
            used_questions.add(q.id)
            
        return Ticket(ticket_id=ticket_id, questions=selected)


class BalancedStrategy(SelectionStrategy):
    """Сбалансированный выбор: распределение по темам и уникальность."""
    
    def generate_ticket(
        self,
        ticket_id: int,
        bank: List[Question],
        questions_per_ticket: int,
        used_questions: Set[int]
    ) -> Optional[Ticket]:
        available = [q for q in bank if q.id not in used_questions]
        
        # Группировка вопросов по темам
        by_topic: Dict[str, List[Question]] = {}
        for q in available:
            by_topic.setdefault(q.topic, []).append(q)
            
        selected: List[Question] = []
        topics = list(by_topic.keys())
        random.shuffle(topics)
        
        # Разбираем по 1 вопросу из каждой темы для равномерного покрытия
        idx = 0
        while len(selected) < questions_per_ticket and available:
            if not topics:
                break
            topic = topics[idx % len(topics)]
            if by_topic[topic]:
                q = random.choice(by_topic[topic])
                selected.append(q)
                by_topic[topic].remove(q)
                available.remove(q)
            else:
                topics.remove(topic)
                if not topics:
                    break
            idx += 1
            
        if len(selected) < questions_per_ticket:
            return None
            
        for q in selected:
            used_questions.add(q.id)
            
        return Ticket(ticket_id=ticket_id, questions=selected)


# ==========================================
# 4. Система генерации и Матрица покрытия
# ==========================================

class ExamSystem:
    def __init__(self, bank: List[Question]):
        self.bank = bank

    def generate_tickets(
        self, 
        count: int, 
        questions_per_ticket: int, 
        strategy: SelectionStrategy
    ) -> List[Ticket]:
        tickets = []
        used_questions: Set[int] = set()
        
        for i in range(1, count + 1):
            ticket = strategy.generate_ticket(i, self.bank, questions_per_ticket, used_questions)
            if ticket:
                tickets.append(ticket)
            else:
                print(f"Предупреждение: Не удалось сгенерировать билет №{i} (недостаточно уникальных вопросов).")
                break
                
        return tickets

    def get_coverage_matrix(self, tickets: List[Ticket]) -> Dict[str, Dict[int, int]]:
        """
        Формирует матрицу покрытия тем:
        {Тема: {ID_Билета: Количество_Вопросов}}
        """
        all_topics = {q.topic for q in self.bank}
        matrix = {topic: {t.ticket_id: 0 for t in tickets} for topic in all_topics}
        
        for ticket in tickets:
            for q in ticket.questions:
                matrix[q.topic][ticket.ticket_id] += 1
                
        return matrix


# ==========================================
# 5. Демонстрация работы
# ==========================================

if __name__ == "__main__":
    # Создаем банк вопросов
    demo_bank = [
        Question(1, "Что такое ООП?", "ООП", 1),
        Question(2, "Что такое Инкапсуляция?", "ООП", 2),
        Question(3, "Что такое Полиморфизм?", "ООП", 3),
        Question(4, "Что такое Чистая функция?", "ФП", 1),
        Question(5, "Что такое Каррирование?", "ФП", 3),
        Question(6, "Что такое Лямбда-выражение?", "ФП", 2),
        Question(7, "Что такое Селекты в SQL?", "БД", 1),
        Question(8, "Что такое Индексы и B-Tree?", "БД", 3),
        Question(9, "Что такое Транзакции и ACID?", "БД", 2),
        Question(10, "Что такое Docker контейнер?", "DevOps", 2),
        Question(11, "Что такое CI/CD?", "DevOps", 2),
        Question(12, "Что такое Kubernetes?", "DevOps", 3),
    ]

    print("=== 1. Фильтрация вопросов (ФВП) ===")
    easy_fp_filter = combine_filters(filter_by_topic("ФП"), filter_by_difficulty(1, 2))
    filtered_questions = apply_filter(demo_bank, easy_fp_filter)
    print("Легкие/средние вопросы по ФП:", [q.text for q in filtered_questions])

    print("\n=== 2. Генерация сбалансированных билетов ===")
    system = ExamSystem(demo_bank)
    balanced_strategy = BalancedStrategy()
    tickets = system.generate_tickets(count=3, questions_per_ticket=3, strategy=balanced_strategy)

    for ticket in tickets:
        print(f"\nБилет №{ticket.ticket_id} (Сложность: {ticket.total_difficulty()}):")
        for q in ticket.questions:
            print(f"  - [{q.topic}] (Сл: {q.difficulty}) {q.text}")

    print("\n=== 3. Матрица покрытия тем ===")
    coverage = system.get_coverage_matrix(tickets)
    header = "Тема \\ Билет\t" + "\t".join([f"№{t.ticket_id}" for t in tickets])
    print(header)
    print("-" * 40)
    for topic, counts in coverage.items():
        row = f"{topic:<15}\t" + "\t".join([str(counts[t.ticket_id]) for t in tickets])
        print(row)