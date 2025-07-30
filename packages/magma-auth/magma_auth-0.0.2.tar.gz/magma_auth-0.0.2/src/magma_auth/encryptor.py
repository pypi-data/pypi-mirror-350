from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import json


class Encryptor:
    def __init__(self):

        ssh_dir = os.path.join(os.path.expanduser('~'), '.ssh')
        os.makedirs(ssh_dir, exist_ok=True)

        self.private_key_path = os.path.join(ssh_dir, 'private_key.pem')
        self.public_key_path = os.path.join(ssh_dir, 'public_key.pem')

        self.private_key, self.public_key = self.load_or_generate_keys()
        self.AES_KEY = os.urandom(32)
        self._text = None
        self._encrypted_package = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def encrypted_package(self):
        return self._encrypted_package

    @encrypted_package.setter
    def encrypted_package(self, encrypted_package):
        self._encrypted_package = encrypted_package

    def generate_rsa_keys(self):
        """Generate RSA public and private key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt_with_aes(self):
        """Encrypt data using AES-GCM"""
        data = self.text
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.AES_KEY), modes.GCM(iv))
        encryptor = cipher.encryptor()

        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')

        ciphertext = encryptor.update(data) + encryptor.finalize()

        return iv, ciphertext, encryptor.tag

    def decrypt_with_aes(self, iv, ciphertext, tag):
        """Decrypt data using AES-GCM"""
        cipher = Cipher(algorithms.AES(self.AES_KEY), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        return plaintext.decode('utf-8')

    def hybrid_encrypt(self) -> str:
        """
        Hybrid encryption: Use AES for data, RSA for AES key
        Returns a dictionary with all encrypted components
        """
        # Encrypt the data with AES
        iv, ciphertext, tag = self.encrypt_with_aes()

        # Encrypt the AES key with RSA
        encrypted_aes_key = self.public_key.encrypt(
            self.AES_KEY,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Package everything together
        encrypted_package = {
            'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8')
        }

        self.encrypted_package = encrypted_package

        # Return as JSON string for easy storage/transmission
        return json.dumps(encrypted_package)

    def hybrid_decrypt(self) -> str:
        """
        Hybrid decryption: Decrypt AES key with RSA, then decrypt data with AES
        """
        # Parse the JSON package
        encrypted_package = json.loads(json.dumps(self.encrypted_package))

        # Decode base64 components
        encrypted_aes_key = base64.b64decode(encrypted_package['encrypted_aes_key'])
        iv = base64.b64decode(encrypted_package['iv'])
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        tag = base64.b64decode(encrypted_package['tag'])

        # Decrypt the AES key with RSA
        self.AES_KEY = self.private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        plaintext = self.decrypt_with_aes(iv, ciphertext, tag)

        return plaintext

    def save_keys(self, private_key, public_key):
        """Save keys to PEM files"""
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(self.private_key_path, 'wb') as f:
            f.write(private_pem)

        # Save public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(self.public_key_path, 'wb') as f:
            f.write(public_pem)

    def load_keys(self):
        """Load keys from PEM files"""
        with open(self.private_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        # Load public key
        with open(self.public_key_path, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())

        return private_key, public_key

    def load_or_generate_keys(self):
        if os.path.isfile(self.private_key_path) and os.path.isfile(self.public_key_path):
            return self.load_keys()

        private_key, public_key = self.generate_rsa_keys()
        self.save_keys(private_key, public_key)
        return private_key, public_key
