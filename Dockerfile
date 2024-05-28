# Utilisez une image de base Python slim
FROM python:3.9-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /inviseobox

# Copiez les fichiers de l'hôte vers le conteneur
COPY . /inviseobox

# echo "url=\"https://client.inviseo.fr/api\"  > inviseobox/.env
# Installez les dépendances de l'application
RUN apt update -y && apt upgrade -y  && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "src/main.py"]