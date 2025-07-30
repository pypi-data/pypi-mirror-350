import base64
import os
import typing

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .ConfigSettings import settings

PBKDF2_ITERATIONS = 1000  # Extracted as a constant for configurability

class Encryption:
    """
    Encryption utility class for cryptographic operations.

    This class provides methods for generating cryptographic keys and salts, encrypting
    and decrypting data, and encoding/decoding data in Base64. It is designed to help
    with secure handling of sensitive information using Fernet encryption and PBKDF2 key
    derivation methods.

    :ivar key: The cryptographic key used for encryption and decryption.
    :type key: bytes
    """
    def __init__(self, key: typing.Union[bytes, str] = settings.FN_KEY):
        self.key = key if isinstance(key, bytes) else key.encode()  # Inline setter logic

    @classmethod
    def generate_fernet_key(cls) -> bytes:
        """
        Generates and returns a new Fernet key for encryption purposes.

        This class method creates a new key using Python's cryptography library
        and provides it as a byte sequence. This key can be used for securely
        encrypting and decrypting data.

        :return: The generated Fernet key as a byte sequence.
        :rtype: bytes
        """
        return Fernet.generate_key()

    @classmethod
    def generate_salt_and_key(cls, password: str, salt: typing.Union[bytes, str] = None) -> typing.Tuple[str, str]:
        """
        Generate a cryptographic salt and derive a secure key using PBKDF2 with HMAC-SHA256 algorithm. If a salt is
        not provided, a new random salt is generated. Otherwise, a provided salt (in bytes or string format) is used.

        :param password:
            The password from which the key is derived.
        :param salt:
            The salt used in key derivation, either as a bytes object or a base64-encoded string. If None,
            a new random salt is generated.

        :return:
            A tuple where the first element is the base64-encoded salt and the second element is
            the base64-encoded derived key.
        """
        salt = os.urandom(16) if salt is None else (base64.urlsafe_b64decode(salt) if isinstance(salt, str) else salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        salt_encoded = base64.urlsafe_b64encode(salt).decode()
        key_encoded = base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()
        return salt_encoded, key_encoded

    def encrypt(self, plaintext: typing.Union[bytes, str]) -> bytes:
        """
        Encrypts a given plaintext using the Fernet symmetric encryption algorithm. The input
        can be either a string or bytes. If the input is a string, it is automatically encoded
        to bytes using UTF-8 encoding before encryption. The method ensures that the data is
        securely encrypted using the provided encryption key.

        :param plaintext: Data to be encrypted by the method. Accepts either a string
            or bytes.
        :type plaintext: typing.Union[bytes, str]
        :return: Encrypted data as a bytes object.
        :rtype: bytes
        """
        plaintext = plaintext.encode() if isinstance(plaintext, str) else plaintext
        return Fernet(self.key).encrypt(plaintext)

    def decrypt(self, ciphertext: typing.Union[bytes, str]) -> str:
        """
        Decrypts an encrypted message using the Fernet symmetric encryption scheme.

        This function accepts an encrypted message in either bytes or string format,
        and decrypts it using the provided symmetric key stored in the `self.key` attribute.
        If the decryption fails due to an invalid token or a corrupt ciphertext, the function
        returns a placeholder string 'InvalidToken'.

        :param ciphertext: The encrypted message to decrypt, can be provided as bytes
                           or a string.
        :type ciphertext: typing.Union[bytes, str]

        :return: The decrypted message as a string if decryption is successful, or
                 the string 'InvalidToken' if decryption fails.
        :rtype: str
        """
        ciphertext = ciphertext.encode() if isinstance(ciphertext, str) else ciphertext
        try:
            decrypted = Fernet(self.key).decrypt(ciphertext)
        except InvalidToken:
            decrypted = b'InvalidToken'
        return decrypted.decode()

    @staticmethod
    def base64_encode(data: typing.Union[bytes, str]) -> str:
        """
        Encodes the given input data using Base64 encoding and returns the encoded string.

        The method accepts either a string or bytes object and converts it into a
        Base64 encoded string. If the input is a string, it will be encoded into bytes
        before processing. The result is returned as a string.

        :param data: The input data to be encoded. It can be a string or bytes.
        :type data: typing.Union[bytes, str]
        :return: A string containing the Base64 encoded representation of the input data.
        :rtype: str
        """
        data = data.encode() if isinstance(data, str) else data
        return base64.b64encode(data).decode()

    @staticmethod
    def base64_decode(encoded_data: typing.Union[bytes, str]) -> str:
        """
        Decodes a Base64 encoded string or bytes and returns the original decoded string.

        :param encoded_data: Base64 encoded data, given as a string or bytes.
        :type encoded_data: typing.Union[bytes, str]
        :return: Decoded string obtained from the provided Base64 encoded data.
        :rtype: str
        """
        encoded_data = encoded_data.encode() if isinstance(encoded_data, str) else encoded_data
        return base64.b64decode(encoded_data, validate=True).decode()

    @staticmethod
    def is_base64_encoded(data: str) -> bool:
        """
        Checks whether the given string is a valid Base64-encoded string.

        :param data: The string to validate as Base64 encoded.
        :return: True if the string is valid Base64, otherwise False.
        """
        try:
            # Validate input: must be a non-empty string
            if not isinstance(data, str) or not data.strip():
                return False

            # Decode and re-encode to verify Base64 format
            decoded_data = base64.b64decode(data, validate=True)
            re_encoded_data = base64.b64encode(decoded_data).decode('utf-8')
            return data == re_encoded_data
        except (ValueError, TypeError):
            # Decoding or encoding failed, therefore not Base64
            return False