import unittest
from exam_system import Question, Ticket, RandomStrategy, BalancedStrategy, ExamSystem

class TestExamSystem(unittest.TestCase):
    def setUp(self):
        self.bank = [
            Question(1, "Q1", "TopicA", 1),
            Question(2, "Q2", "TopicA", 2),
            Question(3, "Q3", "TopicB", 1),
            Question(4, "Q4", "TopicB", 3),
            Question(5, "Q5", "TopicC", 2),
            Question(6, "Q6", "TopicC", 3),
        ]
        self.system = ExamSystem(self.bank)

    def test_no_duplicate_questions_across_tickets(self):
        """Проверка отсутствия повторов вопросов между билетами."""
        tickets = self.system.generate_tickets(count=2, questions_per_ticket=3, strategy=RandomStrategy())
        
        all_ids = []
        for t in tickets:
            all_ids.extend([q.id for q in t.questions])
            
        self.assertEqual(len(all_ids), len(set(all_ids)), "Вопросы повторяются между билетами!")

    def test_insufficient_questions_handling(self):
        """Проверка ограничения, если вопросов в банке не хватает."""
        tickets = self.system.generate_tickets(count=5, questions_per_ticket=3, strategy=RandomStrategy())
        # Банк содержит 6 вопросов, по 3 на билет -> можно сделать максимум 2 билета
        self.assertEqual(len(tickets), 2)

    def test_balanced_strategy_coverage(self):
        """Проверка покрытия тем при BalancedStrategy."""
        tickets = self.system.generate_tickets(count=1, questions_per_ticket=3, strategy=BalancedStrategy())
        ticket = tickets[0]
        # Так как всего 3 темы и 3 вопроса в билете, должны быть охвачены все 3 темы
        self.assertEqual(len(ticket.topics_covered()), 3)

if __name__ == "__main__":
    unittest.main()