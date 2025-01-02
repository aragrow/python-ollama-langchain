import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class GTTSecured:
    def __init__(self, password: str = None, stored_salt: bytes = None):
        print('Exec: GTTSecured.__init__()')
        """
        Initialize with a password to derive the encryption key.
        :param password: The password used to derive the encryption key.
        :param stored_salt: The salt used for key derivation (if validating)
        """
        self.password = password.encode() if password else None 
        if not stored_salt:
            # If we don't have a stored salt (first time encryption), generate and store it
            self.salt = os.urandom(16)
        else:
            self.salt = stored_salt

        # Generate the AES key from the password and salt
        self.key = self.derive_key(self.password, self.salt)  # Generate the AES key

    def derive_key(self, password: bytes, salt: bytes) -> bytes:
        print('Exec: GTTSecured.derive_key()')
        """
        Derives a secure encryption key from the password and salt using PBKDF2.
        :param password: The password used for key derivation.
        :param salt: The salt used with the password.
        :return: The derived AES encryption key (32 bytes for AES-256).
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Length of the key (32 bytes = 256-bit key for AES-256)
            salt=salt,
            iterations=100000,  # Increase iterations for higher security
            backend=default_backend()
        )
        return kdf.derive(password)

    def encrypt(self, plaintext: str) -> str:
        print('Exec: GTTSecured.encrypt()')

        """
        Encrypts the provided plaintext using AES encryption (GCM mode).
        :param plaintext: The plaintext to encrypt.
        :return: The encrypted data (ciphertext) as a hex string.
        """
        # Generate a random IV (Initialization Vector) for GCM mode
        #iv = os.urandom(12)

        # Use a fixed IV for reproducibility (NOT recommended for actual security)
        iv = self.key[:12]
        # Pad plaintext to be a multiple of block size (AES block size is 128 bits = 16 bytes)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # Set up the AES GCM cipher with the derived key, IV, and tag length
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Perform the encryption and get the tag
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        tag = encryptor.tag

        # Return as a hex-encoded string for easy storage/transfer
        encrypted_data = iv + tag + ciphertext  # Combine IV, tag, and ciphertext
        return encrypted_data.hex()  # Convert to hex string for easy storage/transfer

    def validate_password(self, encrypted_stored_password: str, plaintext_password: str) -> bool:
        print('Exec: GTTSecured.validate_password()')
        """
        Validate a plaintext password by encrypting it and comparing it to the stored encrypted password.
        :param encrypted_stored_password: The encrypted password stored in the database.
        :param plaintext_password: The plaintext password entered by the user.
        :return: True if the passwords match, False otherwise.
        """
        # Generate key from plaintext password using the stored salt
        key = self.derive_key(plaintext_password.encode(), self.salt)

        # Encrypt the plaintext password
        encrypted_password = self.encrypt(plaintext_password)

        # Compare the encrypted passwords
        return encrypted_password == encrypted_stored_password

    def get_salt(self) -> bytes:
        print('Exec: GTTSecured.get_salt()')
        """Return the stored salt to be used during validation or re-encryption."""
        thesalthex = os.getenv('GTT_SALT_HEX_2_DERIVE_KEY')
        self.salt = bytes.fromhex(thesalthex)
        return self.salt
