import unittest
from solution import (
    LibrarySearch,
    LocalCatalog,
    RemoteCatalogStub,
    MemoryProvider,
    CompositeSearchProvider
)

class TestLibrarySearch(unittest.TestCase):

    def setUp(self) -> None:
        self.memory_provider = MemoryProvider()
        self.search_service = LibrarySearch(self.memory_provider)

    # Тест 1: Проверка вызова MemoryProvider и сохранения истории
    def test_search_with_memory_provider(self) -> None:
        results = self.search_service.find_books("Тестирование")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Тестирование Дот Ком")
        self.assertIn("Тестирование", self.memory_provider.history)

    # Тест 2: Проверка поиска в LocalCatalog
    def test_local_catalog_search(self) -> None:
        self.search_service.set_provider(LocalCatalog())
        results = self.search_service.find_books("Код")
        self.assertEqual(len(results), 2)

    # Тест 3: Проверка взаимозаменяемости (замена провайдера на RemoteCatalogStub)
    def test_provider_swappability(self) -> None:
        self.search_service.set_provider(RemoteCatalogStub())
        results = self.search_service.find_books("Грокаем")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "Адитья Бхаргава")

    # Тест 4: Проверка CompositeSearchProvider (объединение 2 провайдеров)
    def test_composite_provider(self) -> None:
        local_p = LocalCatalog()
        remote_p = RemoteCatalogStub()
        composite = CompositeSearchProvider([local_p, remote_p])

        self.search_service.set_provider(composite)
        results = self.search_service.find_books("код")
        self.assertGreaterEqual(len(results), 2)

    # Ошибочный сценарий 1: Пустой поисковый запрос
    def test_error_empty_query(self) -> None:
        with self.assertRaises(ValueError):
            self.search_service.find_books("   ")

    # Ошибочный сценарий 2: Некорректный тип поискового запроса
    def test_error_invalid_query_type(self) -> None:
        with self.assertRaises(TypeError):
            self.search_service.find_books(123)  # type: ignore

    # Ошибочный сценарий 3: Передача пустого списка в CompositeSearchProvider
    def test_error_empty_composite_providers(self) -> None:
        with self.assertRaises(ValueError):
            CompositeSearchProvider([])

if __name__ == "__main__":
    unittest.main()
