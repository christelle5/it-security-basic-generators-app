import unittest
from app_methods.rc5_generator import RC5


class TestRC5(unittest.TestCase):
    def setUp(self):
        self.key = b'my_secret_key'
        self.rc5 = RC5(self.key)

    def test_setL(self):  # чи встановлюється правильна кількість елементів L при ініціалізації об'єкту RC5
        self.assertEqual(self.rc5.count_of_elem_L, 2)

    def test_Pw(self):  # чи коректно обчислюється константа Pw для об'єкту RC5
        self.assertEqual(self.rc5.Pw(), 0xB7E151628AED2A6B)

    def test_Qw(self): # чи коректно обчислюється константа Qw для об'єкту RC5
        self.assertEqual(self.rc5.Qw(), 0x9E3779B97F4A7C15)

    def test_setS(self):  # чи правильно встановлюється розмір масиву підключів S
        self.assertEqual(len(self.rc5.S), 42)

    def test_init_vector(self):  # чи генерується вектор ініціалізації правильного розміру для об'єкту RC5
        iv = self.rc5.init_vector()
        self.assertEqual(len(iv), self.rc5.block_size)

    def test_shift_left(self):  # чи коректно працює метод shift_left для зсуву числа вліво
        self.assertEqual(self.rc5.shift_left(8, 2), 32)

    def test_shift_right(self):  # чи коректно працює метод shift_right для зсуву числа вправо
        self.assertEqual(self.rc5.shift_right(32, 2), 8)

    def test_encode_block(self):  # чи метод encode_block правильно шифрує блок даних
        data = int.from_bytes(b'This is a test', byteorder='little')
        encoded_block = self.rc5.encode_block(data)
        self.assertEqual(len(encoded_block), self.rc5.block_size)

    # чи метод decode_block правильно дешифрує зашифрований блок даних і повертає початковий блок
    def test_decode_block(self):
        data = int.from_bytes(b'This is a test', byteorder='little')
        encoded_block = self.rc5.encode_block(data)
        decoded_block = self.rc5.decode_block(int.from_bytes(encoded_block, byteorder='little'))
        self.assertEqual(data, decoded_block)


if __name__ == '__main__':
    unittest.main()
