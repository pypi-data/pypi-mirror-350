import os
import base64
import hmac
import hashlib
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class AES256():

    #agl ____config____
    def __init__(self):

        self.HEADER_VERSION = b'v2' #! version control for future updates
        self.PEPPER = os.urandom(32) #! secret key
        self.ARGON2_TIME_COST = 10 #! higher = saver, but slower (lowest 3)
        self.ARGON2_MEM_COST = 1048576 #! 1GB RAM per Hash (resistance against GPU-Attacks)
        self.ARGON2_PARALLELISM = 2 #! CPU-Threads (not too high, DDOS vulnerable)

    #agl ____set_header_version_and_pepper
    def set_values(self, **kwargs):

        if "header_version" in kwargs:

            self.HEADER_VERSION = kwargs["header_version"]

        if "pepper" in kwargs:

            self.PEPPER = kwargs["pepper"]

    @staticmethod
    def generate_pepper() -> bytes:

        return os.urandom(32)

    #agl ____generate_key____
    def _generate_key(self, password: str, salt: bytes) -> bytes:

        """
        Generates a Key with Argon2 + Peppering (Server-Secret).
        """

        password_hasher = PasswordHasher(

            time_cost = self.ARGON2_TIME_COST,
            memory_cost = self.ARGON2_MEM_COST,
            parallelism = self.ARGON2_PARALLELISM,
            hash_len = 32,
        )

        #! Password + Salt + Pepper → extreme resistant against Rainbow Tables
        return password_hasher.hash(password + salt.hex() + self.PEPPER.hex()).encode()[:32]

    #agl ____encrypt____
    def encrypt(self, plaintext: str, password: str) -> str:

        """
        Encrypts with AES-256-GCM + HMAC-SHA256 + Pepper.
        """

        if not isinstance(plaintext, str) or not isinstance(password, str):

            raise TypeError("Only strings allowed!")

        salt = os.urandom(32) #! 256-Bit Salt
        iv = os.urandom(12) #! 96-Bit IV for GCM
        key = self._generate_key(password, salt)

        #! AES-GCM Encryption (Authenticated Encryption)
        encryptor = Cipher(

            algorithms.AES(key),
            modes.GCM(iv),
            backend = default_backend()
        ).encryptor()

        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        #! HMAC-SHA256 for additional integrity (Defense in Depth)
        hkdf = HKDF(algorithm = hashes.SHA256(), length = 32, salt = None, info = b"HMAC Key")
        hmac_key = hkdf.derive(key + self.PEPPER)
        tag = hmac.new(hmac_key, iv + ciphertext, hashlib.sha256).digest()

        #! Structure: [VERSION][SALT][IV][CIPHERTEXT][GCM-TAG][HMAC-TAG]
        encrypted_data = (

            self.HEADER_VERSION + 
            salt + 
            iv + 
            ciphertext + 
            encryptor.tag +  #! GCMs internal tag (16 Byte)
            tag             #! Our HMAC (32 Byte)
        )
        return base64.b64encode(encrypted_data).decode()
    
    #agl ____decrypt____
    def decrypt(self, ciphertext: str, password: str) -> str:

        """
        Decrypts with double authenticity check (GCM + HMAC).
        """

        try:

            #! input validation
            if not isinstance(ciphertext, str) or not isinstance(password, str):

                raise TypeError("only strings allowed")

            data = base64.b64decode(ciphertext.encode())

            if len(data) < 94: #! minimal size: 2 (Version) + 32 (Salt) + 12 (IV) + 16 (GCM-Tag) + 32 (HMAC)

                raise ValueError("Invalid data length")

            #! Header-Check (versioning)
            if not constant_time.bytes_eq(data[:2], self.HEADER_VERSION):

                raise ValueError("Unsupported version!")

            #! extract data
            salt = data[2:34]
            iv = data[34:46]
            ciphertext = data[46:-48]
            gcm_tag = data[-48:-32]
            hmac_tag = data[-32:]

            #! Keygen (with Pepper)
            key = self._generate_key(password, salt)

            #! 1. HMAC-Validation (constant time)
            hkdf = HKDF(algorithm = hashes.SHA256(), length = 32, salt = None, info = b"HMAC Key")
            hmac_key = hkdf.derive(key + self.PEPPER)
            expected_hmac = hmac.new(hmac_key, iv + ciphertext, hashlib.sha256).digest()

            if not constant_time.bytes_eq(hmac_tag, expected_hmac):

                raise ValueError("HMAC-Validation failed")

            #! 2. AES-GCM Decryption
            decryptor = Cipher(

                algorithms.AES(key),
                modes.GCM(iv, gcm_tag),
                backend = default_backend()
            ).decryptor()

            decrypted = decryptor.update(ciphertext) + decryptor.finalize()

            return decrypted.decode()

        except:

            raise ValueError("Encryption failed") from None

if __name__ == "__main__":

    from colorama import init as colorama_init, Fore as c_colors

    #agl ____init_colorama____
    colorama_init()

    #agl ____create_object____
    aes_256 = AES256()

    #agl ____set_password_and_message____
    text = "Message"
    password = "PaSSwOrd69Thatis12charlong"

    #agl ____generate_pepper____
    pepper = aes_256.generate_pepper()

    #agl ____set_pepper____
    aes_256.set_values(pepper = pepper)

    #agl ____encrypt_data____
    encrypted = aes_256.encrypt(text, password)
    print(f"{c_colors.RED}Encrypted: {c_colors.WHITE}{encrypted}")

    #agl ____decrypt_data____
    decrypted = aes_256.decrypt(encrypted, password)
    print(f"{c_colors.GREEN}Decrypted: {c_colors.WHITE}{decrypted}")

    #agl ____print_pepper____
    print(f"{c_colors.YELLOW}PEPPER argument: {c_colors.WHITE}{aes_256.PEPPER}")
    print(f"{c_colors.YELLOW}PEPPER generated: {c_colors.WHITE}{pepper}")

    #agl ____test____
    assert text == decrypted
    assert aes_256.PEPPER == pepper