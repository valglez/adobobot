# Imagen base con los binarios de Python basada en debian
FROM python:3.8-slim-buster
# Carpeta raiz en la que vamos a meter los ficheros
WORKDIR /app
# Ejecución de comandos
RUN pip3 install pyTelegramBotAPI mysql-connector-python
# Copia ficheros en la imagen del contenedor
COPY adobobot.py .
# Comandos que se ejecutan al arrancar al container
CMD [ "python3", "adobobot.py"]