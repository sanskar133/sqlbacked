import os
from cryptography.fernet import Fernet

SECURE_ENV_KEY = "xVf6_IWpSgUAcMBojJ66s6RglN9msT4Wi3xNyF2uJ8M="


def decrypt_envvar(encrypted_value, key=None):
    def decrypt_envvar_internal(encrypted_value, key, mode):
        encrypted_value = encrypted_value.strip()
        if encrypted_value and mode == "prod":
            cipher_suite = Fernet(key)
            decrypted_value = cipher_suite.decrypt(encrypted_value).decode()
            return decrypted_value
        return encrypted_value

    if key is None:
        # from settings import env

        return decrypt_envvar_internal(
            encrypted_value, SECURE_ENV_KEY, os.getenv("MODE")
        )
    else:
        return decrypt_envvar_internal(encrypted_value, key, "prod")
