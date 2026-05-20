import hashlib
import hmac
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class User:
    # Modelo de datos simple para transportar información del usuario.
    id: int
    username: str
    email: str
    password_hash: str
    password_salt: str
    created_at: str


class AuthService:
    def __init__(self, db_path: str) -> None:
        # Ruta al archivo SQLite que usaremos como persistencia.
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        # Context manager para abrir/cerrar conexión de forma segura.
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    def init_db(self) -> None:
        # Crea la tabla si no existe; permite arrancar el proyecto sin SQL manual.
        with self.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def create_user(self, username: str, email: str, password: str) -> int:
        # Validamos formato mínimo antes de interactuar con la base de datos.
        self._validate_inputs(username, email, password)

        # Generamos salt aleatoria por usuario para robustecer el hash.
        password_salt = os.urandom(16)
        password_hash = self._hash_password(password, password_salt)
        # Guardamos fecha en UTC para evitar ambigüedades horarias.
        created_at = datetime.now(timezone.utc).isoformat()

        try:
            with self.get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (username, email, password_hash, password_salt, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (username.strip(), email.strip().lower(), password_hash, password_salt.hex(), created_at),
                )
                connection.commit()
                return int(cursor.lastrowid)
        except sqlite3.IntegrityError as error:
            # UNIQUE en username/email termina aquí y se traduce a error de dominio.
            raise ValueError("Username or email already exists") from error

    def authenticate_user(self, username: str, email: str, password: str) -> bool:
        # Buscamos por username + email para validar identidad.
        user = self.get_user_by_username_and_email(username, email)
        if user is None:
            return False

        # Comparamos hash esperado vs hash calculado con compare_digest.
        return self._verify_password(password, user.password_salt, user.password_hash)

    def user_exists(self, username: str, email: str) -> bool:
        # Helper de conveniencia para simplificar las rutas web.
        return self.get_user_by_username_and_email(username, email) is not None

    def get_user_by_username_and_email(self, username: str, email: str) -> Optional[User]:
        # Normalizamos email a minúsculas para mantener consistencia.
        with self.get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, username, email, password_hash, password_salt, created_at
                FROM users
                WHERE username = ? AND email = ?
                """,
                (username.strip(), email.strip().lower()),
            ).fetchone()

        if row is None:
            return None

        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            password_salt=row["password_salt"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        # PBKDF2 con SHA-256 y 100000 iteraciones: equilibrio entre seguridad y coste.
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex()

    def _verify_password(self, password: str, salt_hex: str, expected_hash: str) -> bool:
        # Recalcula hash con la misma salt y compara en tiempo constante.
        calculated_hash = self._hash_password(password, bytes.fromhex(salt_hex))
        return hmac.compare_digest(calculated_hash, expected_hash)

    @staticmethod
    def _validate_inputs(username: str, email: str, password: str) -> None:
        # Reglas mínimas de validación de negocio.
        if not username or not username.strip():
            raise ValueError("Username is required")
        if not email or "@" not in email:
            raise ValueError("Valid email is required")
        if not password or len(password) < 8:
            raise ValueError("Password must have at least 8 characters")
