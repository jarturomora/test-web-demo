# Aplicación Web Demo Pruebas

Sitio web en Python (Flask) con formularios separados de registro e inicio de sesion.

Cada formulario solicita:
- Nombre de usuario
- Correo
- Contrasena

Los datos se guardan en una base de datos SQLite (`users.db`) y la contrasena se almacena con hash PBKDF2.

## Endpoints

- `GET /login`: muestra el formulario de inicio de sesion.
- `POST /login`: autentica un usuario existente.
- `GET /register`: muestra el formulario de registro.
- `POST /register`: crea un nuevo usuario.

## Requisitos

- Python 3.10+
- Docker Desktop (o daemon Docker activo) para ejecutar opciones con Docker.

## Ejecutar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000/login` para iniciar sesion o `http://127.0.0.1:5000/register` para crear cuenta.

## Ejecutar con Docker (local)

### Opcion 1: Docker Compose (recomendado)

```bash
docker compose up --build
```

- Levanta el servicio web en `http://127.0.0.1:5000`.
- El codigo local se monta en el contenedor para ver cambios al instante.

Para detener:

```bash
docker compose down
```

### Servicio opcional de tests en Docker Compose

Ejecutar la suite dentro de contenedor:

```bash
docker compose --profile test run --rm test
```

- Este comando construye/usa la imagen y corre `pytest -q` dentro de Docker.
- El servicio `test` no se levanta en `docker compose up` normal.

### Opcion 2: Docker CLI

Construir imagen:

```bash
docker build -t test-web-demo:local .
```

Ejecutar contenedor:

```bash
docker run --rm -p 5000:5000 test-web-demo:local
```

## Ejecutar pruebas

```bash
pytest -q
```

Tambien puedes ejecutar pruebas en contenedor con el servicio opcional `test`.

## Estructura

- `app.py`: rutas web separadas para login y registro.
- `auth_service.py`: acceso a SQLite, hash de contrasenas y validaciones.
- `templates/`: vistas HTML.
- `tests/`: pruebas unitarias e integracion.
- `.github/workflows/python-ci.yml`: pipeline para GitHub Actions.
- `Dockerfile`: imagen para ejecutar la app en contenedor local.
- `docker-compose.yml`: orquestacion local del contenedor web y servicio opcional de tests.
