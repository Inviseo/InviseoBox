#!/bin/bash

# Vérifier que le script est exécuté avec un utilisateur qui a les droits sudo
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script avec les droits sudo."
    exit 1
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

# Si aucun paramètre n'est passé lors de l'appel du script
if [ -z "$1" ]; then
    # Si le fichier "worker_id.txt" n'existe pas
    if [ ! -f "worker_id.txt" ]; then
        echo "Le fichier worker_id.txt n'existe pas. Veuillez saisir le worker_id :"
        read worker_id
        echo "$worker_id" > worker_id.txt
    else
        # Sinon, récupérer le worker_id depuis le fichier
        worker_id=$(cat worker_id.txt)
    fi
else
    # Si un paramètre est passé, mettre à jour le fichier "worker_id.txt" ou le créer
    echo "$1" > worker_id.txt
    worker_id="$1"
fi

# Si le service n'existe pas, le créer
if [ ! -f /etc/systemd/system/inviseo.service ]; then
    echo "[Unit]
Description=Boucle permettant au worker (InviséoBox) de communiquer avec le serveur Inviséo puis d'envoyer les données à la plateforme
After=network.target

[Service]
User=root
WorkingDirectory=$dir
ExecStart=/usr/bin/bash $dir/inviseobox/install.sh

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/inviseo.service

    systemctl enable inviseo

    echo "Le service a été créé avec succès"
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


if [ ! -f .env ]; then
    echo "# Production
url_prod=\"https://client.inviseo.fr/api\"

# Development
url_dev=\"http://localhost:3000\"

# Authentification
email=\"hizaaknewton@gmail.com\"
password=\"amaurice\"
worker_id=\"$worker_id\"" > inviseobox/.env
    echo "Le fichier .env a été créé avec succès."
fi

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
