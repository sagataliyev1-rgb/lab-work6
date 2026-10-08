from typing import Protocol, List, Dict, Any, Optional
import unittest

# 1. Определение контракта (Protocol)
class SearchProvider(Protocol):
    """Интерфейс провайдера поиска литературы."""
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Ищет книги по запросу и возвращает список словарей с описанием книг."""
        ...

# 2. Взаимозаменяемые реализации SearchProvider

class LocalCatalog:
    """Локальный каталог книг."""
    def __init__(self, books: Optional[List[Dict[str, Any]]] = None) -> None:
        self._books = books or [
            {"title": "Чистый код", "author": "Роберт Мартин", "year": 2008},
            {"title": "Совершенный код", "author": "Стив Макконнелл", "year": 2004},
            {"title": "Паттерны проектирования", "author": "Эрик Фримен", "year": 2020}
        ]

    def search(self, query: str) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        return [
            book for book in self._books
            if query_lower in book["title"].lower() or query_lower in book["author"].lower()
        ]

class RemoteCatalogStub:
    """Заглушка удалённого каталога (например, внешняя библиотека)."""
    def __init__(self) -> None:
        self._remote_books = [
            {"title": "Алгоритмы: построение и анализ", "author": "Томас Кормен", "year": 2013},
            {"title": "Грокаем алгоритмы", "author": "Адитья Бхаргава", "year": 2017}
        ]

    def search(self, query: str) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        return [
            book for book in self._remote_books
            if query_lower in book["title"].lower() or query_lower in book["author"].lower()
        ]

class MemoryProvider:
    """Тестовый дублёр: сохраняет истории запросов и результаты в памяти."""
    def __init__(self) -> None:
        self.history: List[str] = []
        self._books = [
            {"title": "Тестирование Дот Ком", "author": "Роман Савин", "year": 2007}
        ]

    def search(self, query: str) -> List[Dict[str, Any]]:
        self.history.append(query)
        query_lower = query.lower()
        return [
            book for book in self._books
            if query_lower in book["title"].lower() or query_lower in book["author"].lower()
        ]

class CompositeSearchProvider:
    """Объединяет результаты нескольких провайдеров (Повышенная сложность)."""
    def __init__(self, providers: List[SearchProvider]) -> None:
        if not providers:
            raise ValueError("Список провайдеров не может быть пустым")
        self._providers = providers

    def search(self, query: str) -> List[Dict[str, Any]]:
        combined_results = []
        seen_titles = set()

        for provider in self._providers:
            results = provider.search(query)
            for book in results:
                if book["title"] not in seen_titles:
                    seen_titles.add(book["title"])
                    combined_results.append(book)

        return combined_results

# 3. Прикладной сервис LibrarySearch (Композиция)

class LibrarySearch:
    """Сервис поиска книг, использующий внешнего провайдера поиска."""
    def __init__(self, provider: SearchProvider) -> None:
        self._provider = provider

    def set_provider(self, provider: SearchProvider) -> None:
        """Позволяет налету менять провайдер поиска."""
        self._provider = provider

    def find_books(self, query: str) -> List[Dict[str, Any]]:
        if not isinstance(query, str):
            raise TypeError("Запрос должен быть строкой")
        clean_query = query.strip()
        if not clean_query:
            raise ValueError("Поисковый запрос не может быть пустым")

        return self._provider.search(clean_query)


# 4. Демонстрационный запуск
if __name__ == "__main__":
    local_p = LocalCatalog()
    remote_p = RemoteCatalogStub()
    composite_p = CompositeSearchProvider([local_p, remote_p])

    service = LibrarySearch(local_p)

    print("=== Поиск в локальном каталоге ===")
    print(service.find_books("Код"))

    print("\n=== Поиск через составной провайдер (Composite) ===")
    service.set_provider(composite_p)
    print(service.find_books("алгоритмы"))
