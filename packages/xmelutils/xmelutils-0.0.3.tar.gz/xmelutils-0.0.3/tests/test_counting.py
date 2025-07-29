import unittest
from xmelutils import count_occurrences, many_count

class TestStringUtils(unittest.TestCase):
    def test_count_occurrences(self):
        # Базовый тест
        self.assertEqual(count_occurrences("hello", "l"), 2)
        
        # Подстроки
        self.assertEqual(count_occurrences("ababa", "aba", as_substrings=True), 2)
        
        # Регистронезависимость
        self.assertEqual(count_occurrences("Apple", "p", case_insensitive=True), 2)
        
        # Список символов
        self.assertEqual(count_occurrences("hello", ["l", "o"]), 3)
        
        # Тест алиаса
        self.assertEqual(many_count("hello", "l"), 2)

if __name__ == "__main__":
    unittest.main()