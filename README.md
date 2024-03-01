# InviseoBox
Un service léger et non-intrusif installé le client pour récupérer et envoyer les données vers le serveur Inviseo

## Installation

Installer les dépendances :
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Sortir de l'environnement virtuel
```bash
deactivate
```

## Environnement de développement

Pour utiliser Visual Studio Code, privilégier l'utilisation de l'environnement virtuel pour que la coloration syntaxique et l'autocomplétion fonctionnent correctement.
```bash
source venv/bin/activate
code .
```

### Pour exécuter le programme

Il est nécessaire d'activer l'environnement virtuel avant d'exécuter le programme. Si votre VSCode n'est pas configuré lancer le programme en sudo (ou autres), vous pouvez juste exécuter le programme dans le terminal :

```bash
source venv/bin/activate
python main.py
```

## Installation en environnement de production

Un fichier `inviseo.service` est fourni pour installer le service sur un système Linux. Il a été prévu que ce dépôt soit cloné dans le dossier `/home/user/inviseo-box` et que le service soit lancé par l'utilisateur `user`.

Les commandes suivantes permettent d'installer le service :
```bash
sudo cp inviseo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable inviseo
sudo systemctl start inviseo
```

IMPORTANT :
Le fichier `main.py` doit être exécuté avec `sudo` pour pouvoir accéder aux ports série. Pour éviter de devoir taper le mot de passe à chaque démarrage (ce qui serait problématique pour un service, sur une machine distante), il est possible désactiver le mot de passe pour la commande `sudo` pour l'utilisateur `user` en ajoutant la ligne suivante à la fin du fichier `/etc/sudoers` :

```
user ALL=(ALL) NOPASSWD: /usr/bin/python3 /home/user/inviseo-box/main.py
```