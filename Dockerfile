# Dockerfile para el Chatbot Financiero 24/7
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Crear directorio para la base de datos si no existe
RUN mkdir -p /app/data

# Exponer el puerto 5000
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=web_app.py
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "web_app.py"]
