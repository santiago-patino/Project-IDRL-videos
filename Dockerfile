# Base image
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias del sistema y Python
#RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Crear y activar un entorno virtual
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Crear un entorno virtual de Python en la raíz y configurarlo en el PATH
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instalar dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exponer los puertos para los servidores Flask
EXPOSE 5000 5001

# Copiar el script de inicio para ejecutar los dos servidores
COPY start_servers.sh /start_servers.sh
RUN chmod +x /start_servers.sh

# Comando por defecto: ejecutar el script de inicio
CMD ["/start_servers.sh"]