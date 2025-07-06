import unittest
from app_methods.md5_generator import MD5


class TestMD5(unittest.TestCase):
    def setUp(self):
        self.md5 = MD5()

    def test_md5_empty_string(self):
        result = self.md5.md5('')
        self.assertEqual(result, 'd41d8cd98f00b204e9800998ecf8427e')  # Перевірка для порожнього рядка

    def test_md5_a(self):
        result = self.md5.md5('a')
        self.assertEqual(result, '0cc175b9c0f1b6a831c399e269772661')  # Перевірка для рядка 'a'

    def test_md5_unicode(self):
        result = self.md5.md5('Привіт, світе!')
        self.assertEqual(result, '544023b2aed083c7205e09d8a36b06e4')  # Перевірка для рядка з Unicode-символами

    def test_md5_large_input(self):
        # Тест для великого об'єму даних
        large_input = 'A' * 100000  # Рядок з 100000 символів 'A'
        result = self.md5.md5(large_input)
        expected_result = '5793f7e3037448b250ae716b43ece2c2'  # Очікуваний хеш для великого введення
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
