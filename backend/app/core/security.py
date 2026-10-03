from pwdlib import PasswordHash

# Argon2: algoritmo recomendado para guardar contraseñas (lento a propósito para frenar ataques)
_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return _password_hash.verify(password, hashed_password)
