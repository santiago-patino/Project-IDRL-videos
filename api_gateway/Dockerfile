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

# Copia el script wait-for-it.sh al contenedor
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Expone el puerto en el que la aplicación Flask está corriendo
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["sh", "-c", "wait-for-it flask_db:5432 --timeout=30 && cd api_gateway && flask run --host=0.0.0.0 --port=5000"]
#CMD ["sh", "-c", "cd api_gateway && flask run --host=0.0.0.0 --port=5000"]