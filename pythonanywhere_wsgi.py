"""Plantilla WSGI para desplegar esta app Flask en PythonAnywhere.

Uso:
1) Copia este contenido en el archivo WSGI que te crea PythonAnywhere.
2) Ajusta PROJECT_HOME a tu ruta real en /home/<usuario>/...
3) Recarga la web app desde el panel de PythonAnywhere.
"""

import os
import sys
from pathlib import Path

# Ruta al directorio del proyecto en PythonAnywhere.
PROJECT_HOME = Path("/home/tu_usuario/test-web-demo")

if str(PROJECT_HOME) not in sys.path:
    sys.path.insert(0, str(PROJECT_HOME))

# Ruta persistente para SQLite en el home del usuario.
os.environ.setdefault("APP_DB_PATH", str(PROJECT_HOME / "users.db"))

from app import app as application
