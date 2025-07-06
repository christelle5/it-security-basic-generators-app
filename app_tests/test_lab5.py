import unittest
from app_methods.signature_generator import SignatureGenerator


class TestSignatureGenerator(unittest.TestCase):
    def setUp(self):
        self.signature_gen = SignatureGenerator()

    def test_key_generation(self):
        generated_key = self.signature_gen.get_pair_of_key()
        # Перевірка, чи файл згенеровано
        self.assertIsNotNone(generated_key)

    def test_sign_and_verify(self):
        private_key = 'private_12-12-2023_22-07-32.pem'
        public_key = 'public_12-12-2023_22-07-32.pem'
        message = 'Test message'

        generated_key = self.signature_gen.get_pair_of_key()

        # Підписати повідомлення та перевірити підпис
        signature = self.signature_gen.sign(private_key, message)
        self.assertTrue(self.signature_gen.verify(public_key, message, signature))

    def test_verification_with_wrong_message(self):
        private_key = 'private_12-12-2023_22-07-32.pem'
        public_key = 'public_12-12-2023_22-07-32.pem'
        message = 'Test message'
        wrong_message = 'Modified message'

        generated_key = self.signature_gen.get_pair_of_key()

        # Підписати правильне повідомлення
        signature = self.signature_gen.sign(private_key, message)

        # Перевірити підпис з зміненим повідомленням
        self.assertFalse(self.signature_gen.verify(public_key, wrong_message, signature))


if __name__ == '__main__':
    unittest.main()
