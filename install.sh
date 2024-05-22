#!/bin/bash

# Vérifier que le script est exécuté les droits sudo
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

# Si le fichier n'a pas été lancé par systemd et qu'il n'a pas précisément 2 arguments, on quitte
if [ "$(ps -o comm= $PPID)" != systemd ]; then
    if [ "$#" -ne 2 ]; then
        echo "Usage: sudo bash install.sh <worker_id> <interval>"
        exit 1
    fi

    # Récupérer les arguments
    worker_id=$1
    interval=$2

    # Vérification de l'intégrité des arguments

    # worker_id doit être un MongoDB ObjectId
    if [[ ! "$worker_id" =~ ^[0-9a-fA-F]{24}$ ]]; then
        echo "L'identifiant du worker doit être un ObjectId valide."
        exit 1
    fi

    # interval doit être un entier positif
    if ! [[ "$interval" =~ ^[0-9]+$ ]]; then
        echo "L'intervalle doit être un entier positif."
        exit 1
    fi

    # interval doit être compris entre 60 et 1800
    if [ "$interval" -lt 60 ] || [ "$interval" -gt 1800 ]; then
        echo "L'intervalle doit être compris entre 60 et 1800."
        exit 1
    fi

    # Écrire les arguments dans un fichier
    echo "worker_id=\"$worker_id\"" > config.txt
    echo "interval=\"$interval\"" >> config.txt
fi

worker_id=$(grep worker_id config.txt | cut -d'=' -f2)
interval=$(grep interval config.txt | cut -d'=' -f2)

# Si le service n'existe pas, le créer
if [ ! -f /etc/systemd/system/inviseo.service ]; then
    echo "[Unit]
Description=Boucle permettant au worker (InviséoBox) de communiquer avec le serveur Inviséo puis d'envoyer les données à la plateforme
After=network.target

[Service]
User=root
Restart=always
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
    echo "url=\"https://client.inviseo.fr/api\"
email=\"vincent@inviseo.fr\"
password=\"runf86lq\"
worker_id=$worker_id
interval=$interval" > inviseobox/.env

    echo "Le fichier .env a été créé avec succès."
fi

cd inviseobox || {
    echo "Le dossier inviseobox n'existe pas."
    exit 1
}

# Créer un virtualenv
python -m venv venv

# Activer le virtualenv
# shellcheck source=/dev/null
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Si le script n'a pas été lancé par systemd, afficher un message et redémarrer la machine
if [ "$(ps -o comm= $PPID)" != systemd ]; then
    echo "
Installation terminée. Vous pourrez constater que la InvixéoBox est bien connectée via l'interface web :
https://client.inviseo.fr/

Un délai de 30 minutes est nécessaire pour que les données soient visibles sur la plateforme.
La machine va redémarrer automatiquement dans 5 secondes."
    for i in {5..1}; do
        echo -n "$i..."
        sleep 1
    done
    reboot
fi


# Lancer le worker
sudo python main.py