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

## Despliegue automático a Render desde CI

El workflow de GitHub Actions ahora tiene dos jobs:

- test: ejecuta pytest
- deploy_render: solo corre si test pasa y el evento es push a main

Configura estos secrets en GitHub (Settings > Secrets and variables > Actions):

- RENDER_DEPLOY_HOOK_URL

Nota importante:

- En Render, SQLite se guarda en un disco persistente montado en `/var/data`.
- La app usa `APP_DB_PATH=/var/data/users.db` para mantener datos entre reinicios.

## Estructura para Render

- `render.yaml`: blueprint del servicio web con disco persistente.

Para conectar el repositorio con Render puedes usar `render.yaml` (Blueprint) o configurar el servicio manualmente en el panel.

## Cómo configurar Render paso a paso

### Opción A: usando Blueprint (`render.yaml`)

1. En Render, pulsa `New +` y luego `Blueprint`.
2. Conecta tu repositorio de GitHub y selecciona este proyecto.
3. Render detectará `render.yaml` y mostrará el servicio a crear.
4. Confirma el plan, nombre del servicio y despliega.
5. Cuando termine, abre la URL publica y prueba `/login` y `/register`.

### Opción B: configuración manual en el panel

1. En Render, crea un `Web Service` desde tu repositorio.
2. Define `Environment` como `Python`.
3. Configura:

   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. En `Environment Variables`, agrega:

   - `APP_DB_PATH=/var/data/users.db`

5. En `Disks`, crea un disco persistente:

   - Mount Path: `/var/data`
   - Size: `1 GB` (o superior si lo necesitas)

6. Guarda cambios y lanza el deploy.

### Activar deploy automático desde GitHub Actions

1. En el servicio de Render, entra a `Settings`.
2. Copia la `Deploy Hook URL`.
3. En GitHub, abre `Settings > Secrets and variables > Actions`.
4. Crea el secret `RENDER_DEPLOY_HOOK_URL` con esa URL.
5. Haz push a `main`: CI correrá tests y, si pasan, disparará deploy en Render.

## Estructura

- `app.py`: rutas web separadas para login y registro.
- `auth_service.py`: acceso a SQLite, hash de contraseñas y validaciones.
- `templates/`: vistas HTML.
- `tests/`: pruebas unitarias e integración.
- `.github/workflows/python-ci.yml`: pipeline para GitHub Actions.
- `Dockerfile`: imagen para ejecutar la app en contenedor local.
- `docker-compose.yml`: orquestación local del contenedor web y servicio opcional de tests.
- `render.yaml`: configuración de despliegue en Render con disco persistente.

## Convención de textos (español)

Para mantener coherencia en interfaz, comentarios y documentación:

1. Usar tildes y eñes correctas: sesión, contraseña, configuración, útil, automático, raíz, código.
2. En preguntas, usar signos de apertura y cierre: ¿...?
3. Mantener tono claro y didáctico en comentarios técnicos.
4. En mensajes al usuario, priorizar frases cortas y directas.
5. Si se cambia un texto visible en UI, actualizar también las pruebas que validan ese literal.
