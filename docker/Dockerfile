# Imagen base ligera de Python para reducir tamaño final del contenedor.
FROM python:3.12-slim

# Evita archivos .pyc y fuerza salida sin buffer para ver logs en tiempo real.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copiamos primero requirements para aprovechar caché de capas en builds futuros.
COPY requirements.txt /app/requirements.txt

# Instalamos dependencias del proyecto.
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiamos el resto del código fuente.
COPY . /app

# Puerto donde Flask escuchará dentro del contenedor.
EXPOSE 5000

# Variables para ejecutar la aplicación Flask.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Comando por defecto para entorno local dentro de Docker.
CMD ["flask", "run"]
