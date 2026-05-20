import tempfile
import unittest
from pathlib import Path

from auth_service import AuthService


class TestAuthServiceInitialization(unittest.TestCase):
    def setUp(self) -> None:
        # Entorno temporal aislado por test.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_users.db"
        self.service = AuthService(str(self.db_path))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_init_db_creates_users_table(self) -> None:
        # Debe crear la tabla users en SQLite.
        self.service.init_db()

        with self.service.get_connection() as connection:
            row = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            ).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "users")


class TestAuthServiceMethods(unittest.TestCase):
    def setUp(self) -> None:
        # Inicializamos DB limpia para cada prueba de métodos.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_users.db"
        self.service = AuthService(str(self.db_path))
        self.service.init_db()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_create_user_stores_user(self) -> None:
        # Verifica inserción y lectura posterior.
        user_id = self.service.create_user("ana", "ana@example.com", "micontra123")

        self.assertGreater(user_id, 0)
        user = self.service.get_user_by_username_and_email("ana", "ana@example.com")
        self.assertIsNotNone(user)

    def test_create_user_rejects_duplicate_username_or_email(self) -> None:
        # El esquema aplica UNIQUE y el servicio traduce a ValueError.
        self.service.create_user("ana", "ana@example.com", "micontra123")

        with self.assertRaises(ValueError):
            self.service.create_user("ana", "ana2@example.com", "micontra123")

        with self.assertRaises(ValueError):
            self.service.create_user("ana2", "ana@example.com", "micontra123")

    def test_authenticate_user_returns_true_for_valid_credentials(self) -> None:
        # Happy path de autenticación.
        self.service.create_user("ana", "ana@example.com", "micontra123")

        is_valid = self.service.authenticate_user("ana", "ana@example.com", "micontra123")

        self.assertTrue(is_valid)

    def test_authenticate_user_returns_false_for_invalid_password(self) -> None:
        # Mismo usuario pero password incorrecta.
        self.service.create_user("ana", "ana@example.com", "micontra123")

        is_valid = self.service.authenticate_user("ana", "ana@example.com", "incorrecta")

        self.assertFalse(is_valid)

    def test_create_user_validates_required_fields(self) -> None:
        # Casos de validación de entradas obligatorias.
        with self.assertRaises(ValueError):
            self.service.create_user("", "ana@example.com", "micontra123")

        with self.assertRaises(ValueError):
            self.service.create_user("ana", "correo-invalido", "micontra123")

        with self.assertRaises(ValueError):
            self.service.create_user("ana", "ana@example.com", "123")
