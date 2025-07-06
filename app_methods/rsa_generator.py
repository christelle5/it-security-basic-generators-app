from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import time


class RSAGenerator:
    def __init__(self):
        self.private_key_file = None
        self.filename = None
        self.public_key_file = None
        self.size = 1024
        self.key = None

    def get_pair_of_key(self):
        size = self.size
        self.key = RSA.generate(bits=size)
        current_time = time.localtime()
        time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
        privatefile = "private_" + f"{time_str}" + ".pem"
        publicfile = "public_" + f"{time_str}" + ".pem"
        with open(privatefile, "wb") as pr_file:
            pr_file.write(self.key.exportKey())
        with open(publicfile, "wb") as pub_file:
            pub_file.write(self.key.publickey().exportKey())
        return f"{time_str}" + ".pem"

    def encrypt(self, input_file, public_key):
        self.filename = input_file
        self.public_key_file = public_key
        current_time = time.localtime()
        time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
        start_time = time.time()
        with open(self.public_key_file, "rb") as rsa_file:
            rsa_pub = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))
        with open(self.filename, "rb") as input_file:
            encrypted_text = rsa_pub.encrypt(input_file.read())
        with open('encrypted_' + self.filename, 'wb') as res:
            res.write(encrypted_text)
        print('Time of encryption, RSA:' + str(time.time() - start_time))
        return 'encrypted_' + self.filename

    def decrypt(self, input_file, private_key):
        self.private_key_file = private_key
        self.filename = input_file
        start_time = time.time()
        with open(self.private_key_file, "rb") as rsa_file:
            rsa_priv = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))
        with open(self.filename, "rb") as input_file:
            text = rsa_priv.decrypt(input_file.read())
        with open('decrypted_' + self.filename, 'wb') as res:
            res.write(text)
        print('Time of decryption, RSA: ' + str(time.time() - start_time))
        return 'decrypted_' + self.filename
