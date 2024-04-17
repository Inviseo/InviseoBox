#!/bin/bash

if [ -z "$1" ]; then
    echo "Veuillez spécifier le worker_id en paramètre."
    exit 1
fi

if [ ! -f .env ]; then
    echo "# Production
url_prod=\"https://inviseo.fr/api\"

# Development
url_dev=\"http://192.168.3.23:3000/api\"

# Authentification
email=\"hizaaknewton@gmail.com\"
password=\"amaurice\"
worker_id=\"$1\"" > .env
    echo "Le fichier .env a été créé avec succès."
else
    echo "Le fichier .env existe déjà."
fi

# Fonction pour vérifier la connectivité Internet
check_internet() {
    while true; do
        if ping -c 1 github.com &> /dev/null; then
            echo "Connexion Internet établie."
            break
        else
            echo "En attente de connexion Internet..."
            sleep 5
        fi
    done
}

# dir = répertoire actuel
dir=$(pwd)


# Si le service n'existe pas, le créer
if [ ! -f /etc/systemd/system/inviseo.service ]; then
    echo "[Unit]
Description=Boucle permettant au worker (InviséoBox) de communiquer avec le serveur Inviséo puis d'envoyer les données à la plateforme
After=network.target

[Service]
User=root
WorkingDirectory=$dir
ExecStart=/usr/bin/bash $dir/install.sh

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/inviseo.service

    systemctl enable inviseo
    # Ne pas démarrer le service ici, il sera démarré après l'installation
else
    echo "Le service existe déjà"
fi

# Supprimer le dossier inviseobox s'il existe
rm -rf inviseobox

# Attendre que la connexion Internet soit établie
check_internet

# Cloner le dépôt
git clone "https://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@github.com/inviseo/inviseobox" || {
    echo "Échec du clonage du dépôt GitHub. Vérifiez votre connexion Internet et réessayez."
    exit 1
}

# Copier le fichier .env dans le dossier inviseobox
cp .env inviseobox/

cd inviseobox || {
    echo "Le dossier inviseobox n'existe pas."
    exit 1
}

# Créer un virtualenv
python -m venv venv

# Activer le virtualenv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le worker
sudo python main.py

echo "Installation terminée"
