import math


class MD5:
    def __init__(self):
        # MD-буфер, ініціалізація початкових значень регістрів [A, B, C, D]
        self.buffer_ABCD = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

        # 64-елементна таблиця T[1...64], складена зі значень синуса
        # i-й елемент таблиці T = ціла частина числа 2**32 * |sin(i)|, де i - кут в радіанах
        # кожен |sin(i)| є [0; 1], кожен елемент T є цілим числом, що може бути представлене через 32 біти
        # таблиця дає "випадкову" множину 32-бітних значень
        # потрібна для ліквідації регулярностей у вхідних даних
        self.T = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

        # таблиця зсувів для кожного циклу обробки
        self.shift_values = [
            [7, 12, 17, 22],
            [5, 9, 14, 20],
            [4, 11, 16, 23],
            [6, 10, 15, 21]
        ]
        self.MD_functions = [self.func_F, self.func_G, self.func_H, self.func_I]

    # 4 функції для 4 циклів відповідно - для обробки кожного 512-бітного блоку
    def func_F(self, x, y, z):
        return (x & y) | (~x & z)

    def func_G(self, x, y, z):
        return (x & z) | (y & ~z)

    def func_H(self, x, y, z):
        return x ^ y ^ z

    def func_I(self, x, y, z):
        return y ^ (x | ~z)

    # циклічний зсув значення x на задану кількість бітів вліво
    def circular_shift(self, x, amount):
        x &= 0xFFFFFFFF  # упевнюємось, що x представлене через 32 біти
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    # перестановки; в межах 1 раунду кожне з 16 слів X[0...15] застосовується лише один раз,
    # для одного кроку, а порядок, в якому використаються слова, змінюється відповідно до циклу
    def index_to_reshuffle(self, x):
        if x < 16:
            return x  # для 1-го циклу
        if 16 <= x < 32:
            return (1 + 5 * x) % 16  # для 2-го циклу
        if 32 <= x < 48:
            return (5 + 3 * x) % 16  # для 3-го циклу
        if 48 <= x < 64:
            return (7 * x) % 16  # для 4-го циклу

    def md5(self, message=''):
        message = bytearray(message, encoding='utf-8')  # конвертуємо вхідне повідомлення байтовий масив
        orig_len_in_bits = (8 * len(message)) & 0xFFFFFFFF  # довжина початкового повідомлення в бітах (32-бітне число)
        message.append(0x80)  # додається байт 0x80 в кінець повідомлення, позначаючи початок даних

        # доповнюємо повідомлення нулями, поки остача від ділення на 64 байти (64*8 = 512 біти)
        # не рівна 56 байтів (54*8 = 448 бітів)
        while len(message) % 64 != 56:
            message.append(0)

        # додаємо в кінець довжину повідомлення в бітах у вигляді 64-бітового числа (little-endian),
        # де найменш значущі байти знаходяться спочатку
        message += orig_len_in_bits.to_bytes(8, byteorder='little')

        registers = self.buffer_ABCD[:]  # MD-буфер

        for chunk_length in range(0, len(message), 64):  # розділення повідомлення на блоки по 64 байти (64*8 = 512 біт)
            a, b, c, d = registers  # регістри [A, B, C, D] MD-буфера для поточного блоку
            chunk = message[chunk_length:chunk_length + 64]  # виділення 64-байтового блоку для обробки

            # обчислення хешу для кожного блоку
            for i in range(64):
                f = self.MD_functions[i // 16](b, c, d)  # вибір функції на основі номера раунду
                index = self.index_to_reshuffle(i)  # отримання індексу для перестановки слів блоку

                # оновлення регістрів [A, B, C, D] MD-буфера за формулою
                bb = (b + self.circular_shift(a + f + self.T[i] + int.from_bytes(chunk[4 * index:4 * index + 4],
                                              byteorder='little'), self.shift_values[i // 16][i % 4])) & 0xFFFFFFFF
                # 'int.from_bytes(chunk[4 * index:4 * index + 4], byteorder='little') - це частина повідомлення, яка
                # береться у вигляді 32-бітного числа (4 байти беруться залежно від index у кожному циклі);
                # у формулі це X[k]

                a, b, c, d = d, bb, b, c  # оновлення значень регістрів для наступного раунду

            for i, val in enumerate([a, b, c, d]):  # оновлення значень регістрів MD-буфера
                registers[i] = (registers[i] + val) & 0xFFFFFFFF

        # повернення хешу у шістнадцятковому вигляді з довжиною 32 символи
        result = '{:032x}'.format(
            int.from_bytes(sum(x << (32 * i) for i, x in enumerate(registers)).to_bytes(16, byteorder='little'),
                           byteorder='big'))
        return result
 