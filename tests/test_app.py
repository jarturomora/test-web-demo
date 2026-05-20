import tempfile
import unittest
from pathlib import Path

import app as web_app
from auth_service import AuthService


class TestAppRoutes(unittest.TestCase):
    def setUp(self) -> None:
        # Cada test usa su propia base de datos temporal para no compartir estado.
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "test_users.db"

        web_app.app.config["TESTING"] = True
        web_app.auth_service = AuthService(str(db_path))
        web_app.auth_service.init_db()
        self.client = web_app.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_get_login_page(self) -> None:
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Iniciar sesión", response.get_data(as_text=True))

    def test_get_register_page(self) -> None:
        response = self.client.get("/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Crear cuenta", response.get_data(as_text=True))

    def test_post_register_creates_new_user(self) -> None:
        response = self.client.post(
            "/register",
            data={
                "username": "ana",
                "email": "ana@example.com",
                "password": "micontra123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Registro completado", response.get_data(as_text=True))

    def test_post_login_authenticates_existing_user(self) -> None:
        # Preparamos el usuario para probar un login real.
        web_app.auth_service.create_user("ana", "ana@example.com", "micontra123")

        response = self.client.post(
            "/login",
            data={
                "username": "ana",
                "email": "ana@example.com",
                "password": "micontra123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Inicio de sesión correcto", response.get_data(as_text=True))

    def test_post_login_fails_when_user_does_not_exist(self) -> None:
        response = self.client.post(
            "/login",
            data={
                "username": "ana",
                "email": "ana@example.com",
                "password": "micontra123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("El usuario no existe", response.get_data(as_text=True))
