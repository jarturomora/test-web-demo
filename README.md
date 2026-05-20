# Aplicación Web Demo Pruebas

Sitio web en Python (Flask) con formularios separados de registro e inicio de sesión.

Cada formulario solicita:

- Nombre de usuario
- Correo
- Contraseña

Los datos se guardan en una base de datos SQLite (`users.db`) y la contraseña se almacena con hash PBKDF2.

## Endpoints

- `GET /login`: muestra el formulario de inicio de sesión.
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

Abre `http://127.0.0.1:5000/login` para iniciar sesión o `http://127.0.0.1:5000/register` para crear cuenta.

## Ejecutar con Docker (local)

### Opción 1: Docker Compose (recomendado)

```bash
docker compose up --build
```

- Levanta el servicio web en `http://127.0.0.1:5000`.
- El código local se monta en el contenedor para ver cambios al instante.

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

### Opción 2: Docker CLI

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

También puedes ejecutar pruebas en contenedor con el servicio opcional `test`.

## Despliegue en PythonAnywhere (gratis)

Este proyecto está preparado para desplegarse en PythonAnywhere usando su hosting WSGI.
El workflow de GitHub Actions se usa para validar tests antes de publicar cambios.

### Requisitos en PythonAnywhere

- Cuenta en PythonAnywhere.
- Un entorno virtual con Python 3.10+.
- El proyecto clonado en tu home de PythonAnywhere.

### Pasos de configuración

1. En PythonAnywhere, abre una consola Bash y clona el repositorio:

```bash
git clone <TU_REPO_GIT>
cd test-web-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

1. Crea una nueva Web App en el panel de PythonAnywhere:

- Tipo: `Manual configuration`
- Versión de Python: 3.10+ (la que tengas disponible)

1. En la pestaña `Web`, configura el archivo WSGI:

- Puedes usar la plantilla de `pythonanywhere_wsgi.py` incluida en este repo.
- Ajusta `PROJECT_HOME` a tu ruta real, por ejemplo:
  - `/home/tu_usuario/test-web-demo`

1. Configura el entorno virtual en la pestaña `Web`:

- Ruta ejemplo: `/home/tu_usuario/test-web-demo/.venv`

1. Recarga la app desde el botón `Reload` y prueba:

- `https://tu_usuario.pythonanywhere.com/login`
- `https://tu_usuario.pythonanywhere.com/register`

### SQLite en PythonAnywhere

- SQLite se guarda de forma persistente en tu home.
- La variable `APP_DB_PATH` puede apuntar a:
  - `/home/tu_usuario/test-web-demo/users.db`
- Si no defines `APP_DB_PATH`, por defecto se usa `users.db` en la raíz del proyecto.

### Flujo recomendado con GitHub Actions

1. Haz push a GitHub.
2. GitHub Actions ejecuta tests automáticamente.
3. Si todo pasa, en PythonAnywhere haces `git pull` y `Reload`.

## Estructura

- `app.py`: rutas web separadas para login y registro.
- `auth_service.py`: acceso a SQLite, hash de contraseñas y validaciones.
- `templates/`: vistas HTML.
- `tests/`: pruebas unitarias e integración.
- `.github/workflows/python-ci.yml`: pipeline para GitHub Actions.
- `Dockerfile`: imagen para ejecutar la app en contenedor local.
- `docker-compose.yml`: orquestación local del contenedor web y servicio opcional de tests.
- `pythonanywhere_wsgi.py`: plantilla WSGI para desplegar en PythonAnywhere.

## Convención de textos (español)

Para mantener coherencia en interfaz, comentarios y documentación:

1. Usar tildes y eñes correctas: sesión, contraseña, configuración, útil, automático, raíz, código.
2. En preguntas, usar signos de apertura y cierre: ¿...?
3. Mantener tono claro y didáctico en comentarios técnicos.
4. En mensajes al usuario, priorizar frases cortas y directas.
5. Si se cambia un texto visible en UI, actualizar también las pruebas que validan ese literal.
