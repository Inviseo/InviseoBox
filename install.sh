#!/bin/bash

# Vérifier que le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]
then
    echo "Ce script doit être exécuté en tant que root"
    exit
fi

# Vérifier que le système est basé sur Debian
if [ ! -f /etc/debian_version ]
then
    echo "Ce script est conçu pour les systèmes basés sur Debian"
    exit
fi

# Supprimer le dossier InviseoBox s'il existe
if [ -d InviseoBox ]
then
    rm -rf InviseoBox
fi

# Vérifier que git est installé
if [ ! command -v git &> /dev/null ]
then
    echo "Git n'est pas installé"
    exit
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]
then
    echo "Le fichier .env n'existe pas."
    exit
fi

# Récupérer le token github
GITHUB_PAT=$(grep -oP 'github_pat = "\K[^"]+' .env)

# Cloner le dépôt
if [ ! git clone "https://$github_pat@github.com/Inviseo/InviseoBox" ]
then
    echo "Erreur lors du clonage du dépôt"
    exit
fi

cd InviseoBox

# Vérifier si python3 est installé
if [ ! command -v python3 &> /dev/null ]
then
    echo "Python3 n'est pas installé"
    exit
fi

# Créer un virtualenv
python3 -m venv venv

# Activer le virtualenv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancez le fichier main.py
python main.py