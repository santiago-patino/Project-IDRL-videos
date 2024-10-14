# api_gateway/Dockerfile
FROM python:3.9-slim

# # Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el requirements.txt desde la raíz del proyecto
COPY requirements.txt ./

# Instala las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación desde el directorio api_gateway
COPY . .

# Expone el puerto en el que la aplicación Flask está corriendo
EXPOSE 5001

# Comando para ejecutar la aplicación Flask
CMD ["sh", "-c", "cd tasks && flask run --host=0.0.0.0 --port=5001"]