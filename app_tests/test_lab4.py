import unittest
from app_methods.rsa_generator import RSAGenerator


class TestRSAGenerator(unittest.TestCase):
    def setUp(self):
        self.rsa = RSAGenerator()

    def test_key_generation(self):
        generated_key = self.rsa.get_pair_of_key()
        # Перевірка, чи файл згенеровано
        self.assertIsNotNone(generated_key)

    def test_encryption_and_decryption(self):
        input_file = 'result.txt'
        public_key = 'public_12-12-2023_21-50-07.pem'
        private_key = 'private_12-12-2023_21-50-07.pem'

        generated_key = self.rsa.get_pair_of_key()
        self.assertEqual(self.rsa.encrypt(input_file, public_key), 'encrypted_' + input_file)
        decrypted_file = self.rsa.decrypt('encrypted_' + input_file, private_key)
        self.assertEqual(decrypted_file, 'decrypted_encrypted_' + input_file)

        # Перевірка, чи розшифрований файл ідентичний оригінальному
        with open(input_file, 'rb') as original_file, open(decrypted_file, 'rb') as decrypted:
            original_data = original_file.read()
            decrypted_data = decrypted.read()
            self.assertEqual(original_data, decrypted_data)


if __name__ == '__main__':
    unittest.main()
