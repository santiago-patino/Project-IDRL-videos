#!/bin/bash

# Activar el entorno virtual
source /venv/bin/activate

# Iniciar el servidor Flask para api_gateway en el puerto 5000
echo "Iniciando api_gateway en el puerto 5000..."
cd api_gateway || exit
flask run --host=0.0.0.0 --port=5000 &

# Iniciar el servidor Flask para tasks en el puerto 5001
echo "Iniciando tasks en el puerto 5001..."
cd ../tasks || exit
flask run --host=0.0.0.0 --port=5001 &

# Esperar a que ambos procesos finalicen
wait