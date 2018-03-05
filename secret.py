import binascii

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Hash import SHA256


class CTR:
    def __init__(self, key):
        """
        Get a key as an hexdecimal format
        """
        self.key = binascii.unhexlify(key)

    def decrypt(self, enc):
        """
        Decrypt values from a hexdecimal format
        """
        enc = binascii.unhexlify(enc)
        iv = enc[:AES.block_size]
        enc = enc[AES.block_size:]
        ctr = Counter.new(128, initial_value=self._counter_iv(iv))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(enc).decode("utf-8")

    def encrypt(self, raw):
        """
        Encrypt and return in hexdecimal format
        """
        iv = Random.new().read(AES.block_size)
        ctr = Counter.new(128, initial_value=self._counter_iv(iv))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return binascii.hexlify(iv + cipher.encrypt(raw))

    @staticmethod
    def _counter_iv(iv):
        return int(binascii.hexlify(iv), 16)


sha256 = SHA256.new()
raw_key = 'mysecretkeynjanjnja_+='.encode('utf-8')
sha256.update(raw_key)
secret_key = binascii.hexlify(sha256.digest())

secret = CTR(secret_key)
