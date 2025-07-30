import abc
import json
import random
import string
import typing
from threading import Lock

import keyring
from cryptography.fernet import Fernet


class ISecretsManager(abc.ABC):
    @abc.abstractmethod
    def get_secret(self, *, secret_name: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def store_secret(self, *, secret_name_prefix: str, secret_value: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_secret(self, *, secret_name: str) -> None:
        raise NotImplementedError


class FileSecretsManager(ISecretsManager):
    _KEYRING_IDENTIFIERS = ("statql", "secrets_file_keyring")

    def __init__(self, *, secrets_file_path: str):
        self._secrets_file_path = secrets_file_path
        self._lock = Lock()
        self._secrets: typing.Dict[str, str] | None = None

    def get_secret(self, *, secret_name: str) -> str:
        with self._lock:
            if self._secrets is None:
                self._secrets = self._load_secrets()

            if secret_name not in self._secrets:
                raise LookupError(f"Secret not found: {secret_name}")

            return self._secrets[secret_name]

    def store_secret(self, *, secret_name_prefix: str, secret_value: str) -> str:
        with self._lock:
            if self._secrets is None:
                self._secrets = self._load_secrets()

            suffix = "".join(random.choices(string.ascii_letters + string.digits, k=10))
            secret_name = f"{secret_name_prefix}-{suffix}"

            self._secrets[secret_name] = secret_value
            self._save_secrets(secrets=self._secrets)

            return secret_name

    def delete_secret(self, *, secret_name: str) -> None:
        with self._lock:
            if self._secrets is None:
                self._secrets = self._load_secrets()

            if secret_name not in self._secrets:
                raise LookupError(f"Secret not found: {secret_name}")

            self._secrets.pop(secret_name)
            self._save_secrets(secrets=self._secrets)

    def _load_secrets(self) -> typing.Dict[str, str]:
        secrets_file_key = self._get_secrets_file_key()

        try:
            with open(self._secrets_file_path, "rb") as f:
                encrypted_data = f.read()
                plaintext = Fernet(secrets_file_key).decrypt(encrypted_data).decode(encoding="utf-8")
                return json.loads(plaintext)

        except FileNotFoundError:
            return {}

    def _save_secrets(self, *, secrets: typing.Dict[str, str]) -> None:
        secrets_file_key = self._get_secrets_file_key()

        with open(self._secrets_file_path, "wb") as f:
            plaintext = json.dumps(secrets)
            encrypted_data = Fernet(secrets_file_key).encrypt(plaintext.encode(encoding="utf-8"))
            f.write(encrypted_data)

    @classmethod
    def _get_secrets_file_key(cls) -> bytes:
        keyring_service, keyring_username = cls._KEYRING_IDENTIFIERS

        secrets_file_key = keyring.get_password(keyring_service, keyring_username)

        if secrets_file_key is None:
            secrets_file_key = Fernet.generate_key().decode()
            keyring.set_password(keyring_service, keyring_username, secrets_file_key)

        return secrets_file_key.encode(encoding="utf-8")
