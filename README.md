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
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo systemctl set-default multi-user.target
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

Modifiez le fichier `docker-compose.yml` pour ajouter les variables d'environnement suivantes, \<INVISEOBOX_TOKEN> et \<API_URL> (SURTOUT ne pas ajouter de / après l'URL. Vous pouvez faire comme l'exemple suivant : ``https://domaine.com/api``).
`interval` est la valeur en seconde de délai entre chaque envoie vers le serveur distant. Il ne peut être négatif ou égal à zéro.

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
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

### 📦 Variables d'environnement

- `token` : Token d'authentification de la InviseoBox, renvoyé par le serveur Inviseo lors de la création de la InviseoBox. Il est présent dans ``workers.token``.
- `interval` : Délai en seconde entre chaque envoie de données vers le serveur Inviseo.
- `url` : URL de l'API Inviseo, sans le `/` à la fin.

### 📦 Algorithimique

Cet algorithme boucle :
- Instancier la base de données SQLite
- Récupérer les données des appareils (GET) : ``/api/workers/devices/data/token?=<TOKEN>`
- Pendant `<interval>` secondes :
  - Pour chaque appareil, pour chaque mesure :
    - Insérer les données relatives à l'appareil
    - Insérer les données relatives à la mesure
    - Insérer les données temporaires dans la base de données
- Aggréger les données en fonction de la configuration de la mesure
- Envoyer les données relatives à l'appareil et aux mesures (POST) : ``/api/devices/status``
- Envoyer les données aggrégées vers le serveur Inviseo (POST) : ``/api/fields/``

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
