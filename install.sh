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

echo "Paramètre 1 (worker_id) : $1"
echo "Paramètre 2 (interval) : $2"

# Si le fichier "config.txt" n'existe pas
if [ ! -f "config.txt" ]; then
    echo "Le fichier config.txt n'existe pas."

    # Le premier paramètre est le worker_id. S'il n'est pas passé, demander à l'utilisateur de le saisir
    if [[ -z "$1" ]]; then
        echo "Le worker_id n'a pas été passé en paramètre."
        read -r -p "Veuillez saisir le worker_id : " worker_id
    else
        # Le worker_id doit être un identifiant MongoDB, soit une chaîne de 24 caractères, composée de chiffres et de lettres minuscules
        if ! [[ "$1" =~ ^[0-9a-f]{24}$ ]]; then
            echo "Le worker_id doit être un identifiant MongoDB valide."
            exit 1
        fi

        echo "Le worker_id ""$1"" a été enregistré dans le fichier config.txt."
        worker_id="$1"
    fi

    # Le deuxième paramètre est l'intervalle. S'il n'est pas passé, demander à l'utilisateur de le saisir
    if [[ -z "$2" ]]; then
        echo "L'intervalle n'a pas été passé en paramètre."
        read -r -p "Veuillez saisir l'intervalle (en secondes) entre chaque envoi de données (par défaut : 1800 secondes) : " interval
    else
        interval="$2"
    fi

    # Si $interval est vide, le définir à 1800
    if [[ -z "$interval" ]]; then
        interval=1800
    else
        # Vérifier que l'intervalle est un nombre
        if ! [[ "$interval" =~ ^[0-9]+$ ]]; then
            echo "L'intervalle doit être un nombre."
            exit 1
        fi

        # Vérifier que l'intervalle est supérieur à 0
        if [ "$interval" -le 0 ]; then
            echo "L'intervalle doit être supérieur à 0."
            exit 1
        fi
        
        echo "L'intervalle ""$interval"" a été enregistré dans le fichier config.txt."
    fi
    echo "worker_id=$1" > config.txt
    echo "interval=$2" > config.txt
    interval="$2"
else
    # Sinon, récupérer le worker_id et l'intervalle depuis le fichier
    worker_id=$(grep -oP 'worker_id=\K.*' config.txt)
    interval=$(grep -oP 'interval=\K.*' config.txt)

    # Vérifier que le worker_id est un identifiant MongoDB
    if ! [[ "$worker_id" =~ ^[0-9a-f]{24}$ ]]; then
        echo "Le worker_id doit être un identifiant MongoDB valide."
        exit 1
    fi

    # Vérifier que l'intervalle est un nombre
    if ! [[ "$interval" =~ ^[0-9]+$ ]]; then
        echo "L'intervalle doit être un nombre."
        exit 1
    fi

    # Vérifier que l'intervalle est supérieur à 0
    if [ "$interval" -le 0 ]; then
        echo "L'intervalle doit être supérieur à 0."
        exit 1
    fi

    echo "Le worker_id et l'intervalle ont été récupérés depuis le fichier config.txt."
    echo "worker_id : $worker_id"
    echo "interval : $interval"
fi


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

# Authentification
email=\"vincent@inviseo.fr\"
password=\"runf86lq\"
worker_id=\"$worker_id\"
interval=\"$interval\"
" > inviseobox/.env
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

echo "
Installation terminée. Vous pourrez constater que la InvixéoBox est bien connectée via l'interface web :
https://client.inviseo.fr/

Un délai de 30 minutes est nécessaire pour que les données soient visibles sur la plateforme.
Veuillez redémarrer la machine pour que le service soit démarré automatiquement :
CTRL + C
sudo reboot"

# Lancer le worker
sudo python main.py