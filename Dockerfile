# Imagen base con los binarios de Python basada en debian
FROM python:3.7-slim-buster
# Carpeta raiz en la que vamos a meter los ficheros
WORKDIR /app
# Ejecución de comandos
RUN pip3 install pymongo pyTelegramBotAPI
# Copia ficheros en la imagen del contenedor
COPY ./src/ .
# Comandos que se ejecutan al arrancar el contenedor"
CMD [ "python3", "index.py"]