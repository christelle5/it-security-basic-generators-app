from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import DSA
from Cryptodome.Signature import DSS
import time


class SignatureGenerator:
    def __init__(self):
        self.signature = None
        self.private_key_file = None
        self.filename = None
        self.public_key_file = None
        self.size = 1024
        self.key = None
        self.message_to_sign = ''

    def get_pair_of_key(self):
        size = self.size
        self.key = DSA.generate(bits=size)
        current_time = time.localtime()
        time_str = time.strftime("%d-%m-%Y_%H-%M-%S", current_time)
        privatefile = "private_" + f"{time_str}" + ".pem"
        publicfile = "public_" + f"{time_str}" + ".pem"
        with open(privatefile, "wb") as pr_file:
            pr_file.write(self.key.exportKey())
        with open(publicfile, "wb") as pub_file:
            pub_file.write(self.key.publickey().exportKey())
        return f"{time_str}" + ".pem"

    def sign(self, private_key, message_to_sign):
        start_time = time.time()
        with open(private_key, 'rb') as file:
            self.private_key_file = DSA.import_key(file.read())
        self.message_to_sign = message_to_sign
        mess_enc = SHA256.new(self.message_to_sign)
        sign = DSS.new(self.private_key_file, 'fips-186-3')
        signature = sign.sign(mess_enc)
        print('Time (sign):' + str(time.time() - start_time))
        return signature.hex()

    def verify(self, public_key, message, signature):
        with open(public_key, 'rb') as file:
            self.public_key_file = DSA.import_key(file.read())
        self.message_to_sign = bytes(message)
        mess_enc = SHA256.new(self.message_to_sign)
        self.signature = bytes.fromhex(signature)
        verifier = DSS.new(self.public_key_file, 'fips-186-3')
        try:
            verifier.verify(mess_enc, self.signature)
            return True
        except ValueError:
            return False
        pass

