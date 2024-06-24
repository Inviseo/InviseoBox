# InviseoBox

Un service léger et non-intrusif installé sur le client pour récupérer et envoyer des données vers le serveur Inviseo.

## 🚀 Installation (Production)

Suivre la procédure d'installation d'un nouveau système pour la inviseobox [Procédure](./procedure_installation_inviseobox.md)

Il suffit d'exécuter les lignes de commande :

```bash
# passer en root
su root
```

```bash
# installation de docker, sudo et git
apt-get install git docker docker-compose docker.io docker-clean docker-doc docker-registry docker sudo -y
# installer le user inviseo en sudo
sudo visudo
```

Entrer la ligne suivante dans le fichier a hauteur de la liste des utilisateurs : 
`inviseo ALL=(ALL:ALL) ALL`

Taper ctrl + o et ctrl + x

Executer exit

```bash
exit
```

Coller le depot de script `InviseoBoxScripts`

```bash
git clone https://github.com/Inviseo/inviseoBoxScripts.git
cd inviseoBoxScripts
sudo chmod a+x *
sudo ./switchSleepMode.sh # Répondre Yes
sudo ./switchGraphicalInterface.sh # Répondre No
```

```bash
cd /home/inviseo
git clone https://github.com/inviseo/inviseobox/ && cd inviseobox
```

Puis vous devrez modifier le fichier `docker-compose.yml` pour ajouter les variables d'environnement (voir ci-dessous).
```bash
nano docker-compose.yml
```

Enfin, exécutez la commande suivante :
```bash
sudo docker-compose up -d
```

Executer le démarrage automatique du service docker

```bash
sudo systemctl start docker
```

### 📝 Configuration

Modifiez le fichier `docker-compose.yml` pour ajouter les variables d'environnement suivantes, \<INVISEOBOX_TOKEN> et \<API_URL> (SURTOUT ne pas ajouter de / après l'URL. Vous pouvez faire comme l'exemple suivant : ``https://domaine.com/api``):

```yaml
version: "3"
services:
  inviseoboxbox:
    image: ghcr.io/inviseo/inviseobox:latest
    container_name: inviseobox
    privileged: true
    user: root
    restart: always
    pull_policy: always
    environment:
      - token=<INVISEOBOX_TOKEN>
      - interval=1800
      - url=<API_URL>

  watchtower:
    image: containrrr/watchtower:latest
    restart: always
    command: --interval 5 --debug  --cleanup inviseobox
```

### 📝 Logs

Les logs sont accessibles grâce à la commande suivante :

```bash
sudo docker logs inviseobox
```

## 🛠️ Installation (Développement)

Installer les dépendances :

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔌 Sortir de l'environnement virtuel

```bash
deactivate
```

### 💻 Environnement de développement

Pour utiliser Visual Studio Code, privilégiez l'utilisation de l'environnement virtuel pour que la coloration syntaxique et l'autocomplétion fonctionnent correctement.

```bash
source venv/bin/activate
code .
```

### ▶️ Pour exécuter le programme

Il est nécessaire d'activer l'environnement virtuel avant d'exécuter le programme. Si votre VSCode n'est pas configuré pour lancer le programme en sudo (ou autres), vous pouvez simplement exécuter le programme dans le terminal :

```bash
source venv/bin/activate
python main.py
```
