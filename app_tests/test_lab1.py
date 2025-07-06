import unittest
from app_methods.pseudorandom_generator import Generator


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = Generator(m=10, a=2, c=3, x0=4, k=6)

    def test_generate_period(self):
        result = self.generator.generate()
        self.assertEqual(result['period'], 5)  # Перевірка відповідності очікуваному періоду

    def test_generate_sequence(self):
        result = self.generator.generate()
        expected_sequence = [4, 1, 5, 3, 9, 4]  # Очікувана послідовність
        self.assertEqual(result['sequence'], expected_sequence)  # Перевірка послідовності

    def test_generate_sequence_length(self):
        result = self.generator.generate()
        self.assertEqual(len(result['sequence']), 6)  # Перевірка довжини послідовності

    def test_generate_invalid_input(self):
        invalid_generator = Generator(m=0, a=0, c=0, x0=0, k=0)  # Генератор з некоректними значеннями
        with self.assertRaises(ZeroDivisionError):  # Перевірка на виняток
            invalid_generator.generate()


if __name__ == '__main__':
    unittest.main()
