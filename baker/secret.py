import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from baker import logger
from baker import settings
from baker.storage import Storage


class SecretKey:
    """
    Secret key is the key generated from a key pass to encrypt and decript secret values in recipes
    """
    @staticmethod
    def generate(key_pass):
        """
        Generate secret key from key pass
        """
        b_key_pass = key_pass.encode(settings.get('ENCODING'))
        sha256 = SHA256.new(b_key_pass)
        secret_key = sha256.digest()
        secret_store = binascii.hexlify(secret_key).decode(settings.get('ENCODING'))
        Storage.file(settings.get('STORAGE_KEY_PATH'), secret_store)
        logger.log("Generated secret key '{0}' "
                   "and saved at '{1}'".format(secret_store, settings.get('STORAGE_KEY_PATH')))
        return secret_store

    @property
    def key(self):
        """
        Read secret key from storage file
        """
        return Storage.file(settings.get('STORAGE_KEY_PATH'))


class Encryption:
    """
    Encryption for secret values in recipes
    """
    def __init__(self, secret_key):
        """
        Initialize with a security key in hexadecimal utf-8 as default format
        """
        self.key = binascii.unhexlify(secret_key)
        self.sep = '\\'

    def encrypt(self, raw):
        """
        Encrypt and return an hexadecimal utf-8 as default format
        """
        b_raw = raw.encode(settings.get('ENCODING'))
        cipher = AES.new(self.key, AES.MODE_EAX)
        b_cipher, tag = cipher.encrypt_and_digest(b_raw)
        return self._build_encrypt(cipher.nonce, b_cipher, tag)

    def decrypt(self, encrypt):
        """
        Decrypt values from a hexadecimal utf-8 as default format to plaintext
        """
        nonce, tag, b_cipher = self._split_encrypt(encrypt)
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        try:
            return cipher.decrypt_and_verify(b_cipher, tag).decode(settings.get('ENCODING'))
        except ValueError:
            raise ValueError("Encryption '%s' is corrupted." % encrypt)

    def _build_encrypt(self, nonce, b_cipher, tag):
        """
        Build a unique encrypt with all sections of cipher
        """
        return self._to_hex(nonce) + self.sep + self._to_hex(tag) + \
            self.sep + self._to_hex(b_cipher)

    def _split_encrypt(self, encrypt):
        """
        Split encrypt on sections to decrypt and check data integrity
        """
        try:
            nonce, tag, cipher = encrypt.split(self.sep)
            return self._to_bin(nonce), self._to_bin(tag), self._to_bin(cipher)
        except ValueError:
            raise ValueError("Encryption '%s' is corrupted." % encrypt)

    @staticmethod
    def _to_hex(binary):
        """
        Convert binary string into hexadecimal decoded in utf-8 as default
        """
        return binascii.hexlify(binary).decode(settings.get('ENCODING'))

    @staticmethod
    def _to_bin(hexadecimal):
        """
        Convert hexadecimal string encoded in utf-8 as default into binary
        """
        return binascii.unhexlify(hexadecimal.encode(settings.get('ENCODING')))
