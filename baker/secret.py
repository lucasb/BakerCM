import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class SecretKey:
    def __init__(self, key_pass):
        """
        Initialize with a key pass in plaintext in utf-8 format
        """
        self.key_pass = key_pass

    def generate(self):
        """
        Generate secret key from key pass
        """
        b_key_pass = self.key_pass.encode('utf-8')
        sha256 = SHA256.new(b_key_pass)
        secret_key = sha256.digest()
        return binascii.hexlify(secret_key).decode('utf-8')


class Encryption:
    def __init__(self, secret_key):
        """
        Initialize with a security key in hexadecimal utf-8 format
        """
        self.key = binascii.unhexlify(secret_key)
        self.sep = '\\'

    def encrypt(self, raw):
        """
        Encrypt and return an hexdecimal utf-8 format
        """
        b_raw = raw.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_EAX)
        b_cipher, tag = cipher.encrypt_and_digest(b_raw)
        return self._build_encrypt(cipher.nonce, b_cipher, tag)

    def decrypt(self, encrypt):
        """
        Decrypt values from a hexdecimal utf-8 format to plaintext
        """
        nonce, tag, b_cipher = self._split_encrypt(encrypt)
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        try:
            return cipher.decrypt_and_verify(b_cipher, tag).decode("utf-8")
        except ValueError:
            raise ValueError("ERROR: Encryption '" + encrypt + "' is corrupted.")

    def _build_encrypt(self, nonce, b_cipher, tag):
        """
        Build a unique encrypt with all sections of cipher
        """
        return self._to_hex(nonce) + self.sep + self._to_hex(tag) + self.sep + self._to_hex(b_cipher)

    def _split_encrypt(self, encrypt):
        """
        Split encrypt on sections to decrypt and check data integrity
        """
        try:
            nonce, tag, cipher = encrypt.split(self.sep)
            return self._to_bin(nonce), self._to_bin(tag), self._to_bin(cipher)
        except ValueError:
            raise ValueError("ERROR: Encryption '" + encrypt + "' is corrupted.")

    @staticmethod
    def _to_hex(binary):
        """
        Convert binary string into hexdecimal decoded in utf8
        """
        return binascii.hexlify(binary).decode('utf-8')

    @staticmethod
    def _to_bin(hexadecimal):
        """
        Convert hexadecimal string encoded in utf-8 into binary
        """
        return binascii.unhexlify(hexadecimal.encode('utf-8'))
