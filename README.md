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

## Despliegue en Render (free tier)

Este proyecto está preparado para desplegarse en Render desde GitHub Actions.

### Requisitos en Render

- Cuenta en Render (free tier).
- Repositorio conectado a Render.

### Paso 1: crear servicio web en Render

1. En Render, pulsa `New +` y selecciona `Blueprint`.
2. Conecta tu repositorio y selecciona este proyecto.
3. Render detectará `render.yaml` y creará el servicio `test-web-demo`.

### Paso 2: configurar Deploy Hook para GitHub Actions

1. Abre tu servicio en Render y entra en `Settings`.
2. Copia la `Deploy Hook URL`.
3. En GitHub, abre `Settings > Secrets and variables > Actions`.
4. Crea el secret `RENDER_DEPLOY_HOOK_URL` con esa URL.

### Paso 3: despliegue automático

1. Haz push a `main`.
2. GitHub Actions ejecuta tests.
3. Si pasan, el workflow dispara el Deploy Hook y Render publica la nueva versión.

### Nota importante sobre SQLite en Render free

- En Render free, la base se guardará en `/tmp/users.db`.
- Ese almacenamiento es efímero y puede perderse entre reinicios o deploys.
- Para esta demo educativa es válido, pero no para producción.

## Estructura

- `app.py`: rutas web separadas para login y registro.
- `auth_service.py`: acceso a SQLite, hash de contraseñas y validaciones.
- `templates/`: vistas HTML.
- `tests/`: pruebas unitarias e integración.
- `.github/workflows/python-ci.yml`: pipeline para GitHub Actions.
- `Dockerfile`: imagen para ejecutar la app en contenedor local.
- `docker-compose.yml`: orquestación local del contenedor web y servicio opcional de tests.
- `render.yaml`: configuración de despliegue en Render free.

## Convención de textos (español)

Para mantener coherencia en interfaz, comentarios y documentación:

1. Usar tildes y eñes correctas: sesión, contraseña, configuración, útil, automático, raíz, código.
2. En preguntas, usar signos de apertura y cierre: ¿...?
3. Mantener tono claro y didáctico en comentarios técnicos.
4. En mensajes al usuario, priorizar frases cortas y directas.
5. Si se cambia un texto visible en UI, actualizar también las pruebas que validan ese literal.
