import requests
import os
import json
import jwt
from magma_database import config
from datetime import datetime, timezone, timedelta
from typing import Self
from .encryptor import Encryptor


class MagmaAuth:
    url_login = 'https://magma.esdm.go.id/api/login'
    url_validate_token = 'https://magma.esdm.go.id/api/status'
    database_location = config['DATABASE_LOCATION']

    def __init__(self) -> None:
        self.expired_at = None
        self.success = False
        self.encryptor: Encryptor = Encryptor()
        self._token: str | None = None
        self._token_file_location = os.path.join(self.database_location, '.token')
        self._credential_location = os.path.join(self.database_location, '.credential')

    @property
    def token(self) -> str | None:
        return self.encryptor.hybrid_decrypt()

    @token.setter
    def token(self, token: str) -> None:
        # Also set encrypted_package property
        self.encryptor.text = token
        self._token: str = self.encryptor.hybrid_encrypt()

    def decode(self, token: str = None) -> dict:
        """Decode token

        Args:
            token (str): Token to decode

        Returns:
            dict: Decoded token
        """
        if token is None and self.token is None:
            raise Exception('Token is missing')
        decoded = jwt.decode(self.token, options={"verify_signature": False})

        return {
            'issued_at': datetime.fromtimestamp(decoded['iat'], timezone.utc),
            'expired_at': datetime.fromtimestamp(decoded['exp'], timezone.utc),
            'roles': decoded['roles']
        }

    def validate_token(self, token) -> bool:
        headers = {'Authorization': 'Bearer ' + token}

        try:
            response = requests.request("GET", self.url_validate_token, headers=headers).json()
            self.expired_at = datetime.fromtimestamp(response['exp'], timezone.utc)
        except Exception as e:
            print(f'Error validating token: {e}')
            return False

        if 'code' in response:
            if response['code'] == 419:
                return False

        self.success = True

        return True

    def load_token(self) -> tuple[bool, str | None]:
        """Load token from file

        Returns:
            token exists (bool)
            token (str)
        """
        if not os.path.exists(self._token_file_location):
            print('Token not found. Please login first.')
            return False, None

        try:
            with open(self._token_file_location, 'r') as f:
                self.encryptor.encrypted_package = json.loads(f.read())

            token = self.encryptor.hybrid_decrypt()
            decoded = self.decode(token)

            now = datetime.now(timezone.utc)
            self.expired_at = decoded['expired_at']

            # Remove expired token
            if bool(now > self.expired_at):
                try:
                    os.remove(self._token_file_location)
                except Exception as e:
                    raise Exception(f'Error deleting {self._token_file_location}: {e}')
                return False, None

            return True, token
        except Exception as e:
            print(f'Error loading token: {e}')
            return False, None

    def _login(self, payload: str, ttl: int = 1, verbose: bool = False) -> Self:
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.request("POST", self.url_login,
                                        headers=headers, data=payload).json()
            if verbose:
                print(f'Login response: {response}')

            if not response['success']:
                raise ValueError(f'Wrong username or password.')

            self.token = response['token']
            self.success = bool(response['success'])
            self.expired_at = datetime.now() + timedelta(days=ttl)

            with open(self._token_file_location, "w") as f:
                f.write(json.dumps(self.encryptor.encrypted_package))

            if verbose:
                print(f'Login successful. Token saved to {self._token_file_location}')

            self.save(payload, verbose)

            return self
        except Exception as e:
            raise ConnectionError(f'Error login with username and password: {e}')

    def login(self, username: str, password: str, ttl: int = 1,
              use_token: bool = True, verbose: bool = False) -> Self:
        """Login MAGMA Indonesia using username and password.

        Args:
            username (str): username
            password (str): password
            ttl (int, optional): Time to live token in day. Defaults to 1.
            use_token (bool, optional): Use saved token. Default True.
            verbose (bool, optional): Print token to console. Defaults to False.

        Returns:
            Self
        """
        if use_token:
            token_exists, token = self.load_token()
            if token_exists and use_token:
                if verbose:
                    print('Login using token')
                self.token = token
                self.success = True

                return self

        # Logging in
        payload = json.dumps({
            "username": username,
            "password": password,
            "ttl": ttl
        })

        return self._login(payload, ttl, verbose)

    def _load(self) -> tuple[bool, dict | None]:
        """Load credential from file

        Returns:
            success (bool), payload (dict)
        """
        if not os.path.exists(self._credential_location):
            print('Credential not found. Please login first.')
            return False, None

        encryptor = Encryptor()
        with open(self._credential_location, 'r') as f:
            encryptor.encrypted_package = json.loads(f.read())

        payload = json.loads(encryptor.hybrid_decrypt())
        return True, payload

    def save(self, payload: str, verbose: bool = False) -> None:
        """Save username and password credential to file

        Args:
            payload (str): Consist of username and password.
            verbose (bool, optional): Print token to console. Defaults to False.
        """
        encryptor = Encryptor()
        encryptor.text = payload
        encrypted_payload = encryptor.hybrid_encrypt()
        credential_location = self._credential_location

        with open(credential_location, "w") as f:
            f.write(encrypted_payload)

        if verbose:
            print(f'Saving credential to {credential_location}')

        return None

    def auto(self, ttl: int = 1) -> None:
        """Login automatically using saved credential.
        Make sure you already have logged in once before.

        Args:
            ttl (int, optional): Time to live token in day. Defaults to 1.
        """
        success, payload = self._load()

        if success:
            self._login(json.dumps(payload), ttl)
            print('Successfully logged in using saved credential.')


auth = MagmaAuth()
