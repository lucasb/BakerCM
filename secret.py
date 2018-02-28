from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Hash import SHA256


class CTR:
    def __init__(self, key):
        """
        Get a key as an hexdecimal format
        """
        self.key = key.decode('hex')

    def decrypt(self, enc):
        """
        Decrypt values from a hexdecimal format
        """
        enc = enc.decode('hex')
        iv = enc[:AES.block_size]
        enc = enc[AES.block_size:]
        ctr = Counter.new(128, initial_value=self._counter_iv(iv))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(enc)

    def encrypt(self, raw):
        """
        Encrypt and return in hexdecimal format
        """
        iv = Random.new().read(AES.block_size)
        ctr = Counter.new(128, initial_value=self._counter_iv(iv))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return (iv + cipher.encrypt(raw)).encode('hex')

    @staticmethod
    def _counter_iv(iv):
        return long(iv.encode('hex'), 16)


sha256 = SHA256.new()
sha256.update('mysecretkeynjanjnja_+=')
secret_key = sha256.digest().encode('hex')

secret = CTR(secret_key)
