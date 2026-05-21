import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from auth_service import AuthService

# Resolvemos la ruta del proyecto para ubicar la base de datos SQLite.
BASE_DIR = Path(__file__).resolve().parent


def _resolve_db_path() -> Path:
    # Permite definir la ruta de la base de datos vía variable de entorno
    # (por ejemplo, /tmp/users.db en Render free para una demo).
    env_db_path = os.environ.get("APP_DB_PATH")
    if env_db_path:
        return Path(env_db_path)

    # En local mantenemos users.db junto al backend para simplicidad.
    return BASE_DIR / "users.db"


DB_PATH = _resolve_db_path()

# Creamos la app Flask y el servicio de autenticación.
app = Flask(__name__)
auth_service = AuthService(str(DB_PATH))
# Inicializa la tabla users si no existe aún.
auth_service.init_db()


@app.get("/")
def home() -> str:
    # Punto de entrada principal: redirige a la pantalla de login.
    return redirect(url_for("login"))


@app.get("/login")
def login() -> str:
    # Muestra solo el formulario de inicio de sesión.
    return render_template("index.html", message=None)


@app.post("/login")
def login_post() -> str:
    # Leemos los datos enviados por el formulario.
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    try:
        # En login exigimos que el usuario exista previamente.
        if not auth_service.user_exists(username, email):
            return render_template(
                "index.html",
                message="El usuario no existe. Primero regístrate en /register.",
            )

        if auth_service.authenticate_user(username, email, password):
            return render_template(
                "success.html",
                title="Inicio de sesión correcto",
                description="Usuario autenticado correctamente.",
                back_url="/login",
                back_label="Volver al login",
            )

        return render_template(
            "index.html",
            message="Credenciales inválidas. Revisa la contraseña.",
        )
    except ValueError as error:
        # Mostramos errores funcionales (validaciones, etc.).
        return render_template("index.html", message=str(error))


@app.get("/register")
def register() -> str:
    # Muestra solo el formulario de registro.
    return render_template("register.html", message=None)


@app.post("/register")
def register_post() -> str:
    # Leemos los datos enviados por el formulario.
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    try:
        # En registro exigimos que el usuario no exista ya.
        if auth_service.user_exists(username, email):
            return render_template(
                "register.html",
                message="Ese usuario ya existe. Inicia sesión en /login.",
            )

        auth_service.create_user(username, email, password)
        return render_template(
            "success.html",
            title="Registro completado",
            description="Usuario registrado y guardado en SQLite.",
            back_url="/login",
            back_label="Ir al login",
        )
    except ValueError as error:
        # Mostramos errores funcionales (validaciones, duplicados, etc.).
        return render_template("register.html", message=str(error))


if __name__ == "__main__":
    # debug=True es útil en desarrollo porque recarga cambios automáticamente.
    app.run(debug=True)
