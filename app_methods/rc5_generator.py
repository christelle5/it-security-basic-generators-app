import time

from app_methods.md5_generator import MD5
from app_methods.pseudorandom_generator import Generator


class RC5:
    def __init__(self, key, w=64, R=20):
        self.count_of_elem_L = None
        self.w = w  # розмір слова в бітах (за замовчуванням 64)
        self.R = R  # кількість раундів шифрування (за замовчуванням 20)
        self.key = key  # слово-ключ (пароль)
        self.T = 2 * (R + 1)  # загальна кількість підключів
        self.block_size = w // 4  # розмір блоку (байти)
        self.word_bytes = w // 8  # байтів у слові
        self.mod = 2 ** self.w  # 2^w
        self.len_of_key = len(key)

        self.setL()
        self.setS()
        self.shuffle()

    def get_md5_key(pswrd) -> bytearray:  # перетворюємо ключ-пароль у (32-бітний) хеш
        md5_obj = MD5()
        result = md5_obj.md5(pswrd)
        return bytearray(result, encoding='utf-8')

    def shift_left(self, a: int, s: int) -> int:  # зсув числа вліво
        s %= self.w
        number = (a << s) | (a >> self.w - s)
        number %= 2 ** self.w
        return number

    def shift_right(self, a: int, s: int) -> int:  # зсув числа вліво
        s %= self.w
        number = (a >> s) | (a << self.w - s)
        number %= 2 ** self.w
        return number

    def setL(self):  # встановлює масив допоміжних значень L
        if self.len_of_key == 0:  # перевіряємо, чи ключ порожній
            self.count_of_elem_L = 1
        elif self.len_of_key % self.word_bytes:  # чи ключ кратний розміру слова у байтах
            self.key += b'\x00' * (self.word_bytes - self.len_of_key % self.word_bytes)  # доповнюємо до кратності
            self.len_of_key = len(self.key)  # оновили довжину
            self.count_of_elem_L = self.len_of_key // self.word_bytes  # кількість елементів L
        else:
            self.count_of_elem_L = self.len_of_key // self.word_bytes
        L = [0] * self.count_of_elem_L
        for i in range(self.len_of_key - 1, -1, -1):  # проходимось по кожному байту ключа у зворотньому порядку
            L[i // self.word_bytes] = (L[i // self.word_bytes] << 8) + self.key[i]  # за формулою
        self.L = L

    def Pw(self):  # константа Rw методу RC5 (у шістнадцятковому вигляді)
        if self.w == 16:
            return 0xB7E1
        elif self.w == 32:
            return 0xB7E15163
        elif self.w == 64:
            return 0xB7E151628AED2A6B

    def Qw(self):  # константа Qw методу RC5 (у шістнадцятковому вигляді)
        if self.w == 16:
            return 0x9E37
        elif self.w == 32:
            return 0x9E3779B9
        elif self.w == 64:
            return 0x9E3779B97F4A7C15

    def setS(self):  # масив підключів S
        P = self.Pw()
        Q = self.Qw()
        self.S = [P + Q * i for i in range(self.T)]

    def shuffle(self):  # змішування масиву L з масивом підключів S
        i, j, A, B = 0, 0, 0, 0
        for k in range(max(self.count_of_elem_L, self.T)):
            A = self.S[i] = self.shift_left((self.S[i] + A + B), 3)  # через зсув за формулами
            B = self.L[j] = self.shift_left((self.L[j] + A + B), A + B)
            i = (i + 1) % len(self.S)  # len(S) = 2r+2
            j = (j + 1) % len(self.L)  # len(L) = c у формулі

    def init_vector(self):  # вектор ініціалізації
        # m = 701; a = 3; c = 0; x0 = 1; період функ. генерації буде 700
        generator = Generator(701, 3, 0, 1, self.block_size)
        result = generator.generate()
        generated_sequence = result.get("sequence")
        i = 0
        result = bytearray()
        for _ in range(self.block_size):
            result.append(generated_sequence[i] % (2 ** 8))
            i += 1
        return result

    def encode_block(self, data):  # підготовка блоку для кодування
        A = (data >> self.w) % self.mod
        B = data % self.mod  # поділили дані на 2 половини блоку (ліва і права)
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod  # перше додавання підключів S[0] та S[1] до частин даних A та B
        for i in range(1, self.R + 1):  # змішування даних та підключа для обох половин
            A = (self.shift_left((A ^ B), B) + self.S[2 * i]) % self.mod
            B = (self.shift_left((A ^ B), A) + self.S[2 * i + 1]) % self.mod
        return ((A << self.w) | B).to_bytes(length=self.block_size, byteorder='little')
        # об'єднання змішаних даних у одне значення, яке повертається у вигляді зашифрованого блоку даних

    def encode_file(self, input_filename, output_filename):  # кодування
        start_time = time.time()
        with open(input_filename, 'rb') as inp, open(output_filename, 'wb') as out:
            run = True
            init_vector = self.init_vector()  # генеруємо вектор ініціалізації
            out.write(init_vector)  # записуємо цей вектор у початок вихідного файлу
            encoded_text = init_vector
            while run:
                text = inp.read(self.block_size)  # зчитується наступний блок даних з вхідного файлу
                if not text:
                    break
                if len(text) != self.block_size:  # доповнюємо, якщо треба (блок не відповідає потрібному розміру)
                    text = bytearray(text)
                    append_value = self.block_size - len(text)
                    for _ in range(append_value):
                        text.append(append_value)
                    run = False
                text_int = int.from_bytes(text, byteorder='little')
                encoded_text_int = int.from_bytes(encoded_text, byteorder='little')
                text_int ^= encoded_text_int
                # блок даних змішується з попереднім зашифрованим блоком за допомогою операції XOR

                encoded_text = self.encode_block(text_int)  # шифруємо блок
                out.write(encoded_text)  # зашифрований блок додається до вихідного файлу
            inp.close()
            out.close()
            print('Time (RC5 encode):' + str(time.time() - start_time))
            return True

    def decode_block(self, data):  # підготовка блоку для декодування
        A = data >> self.w
        B = data % self.mod  # поділили дані на 2 половини блоку (ліва і права)
        for i in range(self.R, 0, -1):  # змішування даних та підключа для обох половин
            B = self.shift_right((B - self.S[2 * i + 1]) % self.mod, A) ^ A
            A = self.shift_right((A - self.S[2 * i]) % self.mod, B) ^ B
        B = (B - self.S[1]) % self.mod  # віднімання підключів S[0] та S[1] від частин даних A та B
        A = (A - self.S[0]) % self.mod
        return (A << self.w) | B

    def decode_file(self, input_filename, output_filename):
        with open(input_filename, 'rb') as inp, open(output_filename, 'wb') as out:
            init_vector = inp.read(self.block_size)  # зчитує перший блок, що є вектором ініціалізації
            prev_encoded_text = init_vector  # початкове значення з попереднього блоку є цей вектор
            run = True
            while run:  # поки не прочитаємо весь файл
                encoded_text = inp.read(self.block_size)  # зчитується наступний блок даних з вхідного файлу
                if not encoded_text:
                    break  # закінчився файл
                if len(encoded_text) != self.block_size:
                    # якщо розмір блоку відрізняється від очікуваного розміру блоку для дешифрування,
                    # встановлюємо run в False, щоб припинити цикл
                    run = False
                encoded_text_int = int.from_bytes(encoded_text, byteorder='little')  # перетворюємо у ціле число блок
                text_int = self.decode_block(encoded_text_int) ^ int.from_bytes(prev_encoded_text, byteorder='little')
                # дешифруємо і змішуємо через xor з попереднім зашифрованим блоком
                text = text_int.to_bytes(length=self.block_size, byteorder='little')
                # результат дешифрування конвертується назад у байти
                prev_encoded_text = encoded_text

                # виправлення додаткових символів, які можуть бути додані під час дешифрування тексту
                last_byte = text[-1]
                # отримання значення останнього байта, яке відображає кількість байтів,
                # які можуть бути додані для доповнення блоку даних

                if last_byte <= len(text):  # чи останній байт не перевищує загальну довжину тексту
                    for byte in text[-last_byte:]:
                        # перевіряється кожен байт у частині тексту, яка відповідає доповненню
                        if byte != last_byte:
                            # якщо знайдено байт, відмінний від значення доповнення, цикл переривається
                            break
                    else:
                        text = text[:-last_byte]
                        # якщо всі байти в доповненні відповідають значенню доповнення, то вони видаляються з тексту,
                        # щоб повернутися до оригінального блоку даних без додаткових символів
                out.write(text)
            inp.close()
            out.close()
            return True
