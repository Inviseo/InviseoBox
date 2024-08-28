# InviseoBox

## Aperçu

La `InviseoBox` est une des composante de la solution `Inviseo` avec le `Logiciel Inviseo` et la `InviseoPus`.

La `InviseoBox` est un client léger équipé d'un debian (latest) comme système d'exploitation sans interface graphique.
Configuré avec les utilitaires standard pour les systèmes debian et avec SSH, cette box branchée dans le réseau de nos clients, permet de réléver des informations de capteurs (`InviseopPus`).
Cette vient paramétrée avec un micro logiciel, le micro logiciel de la `InviseoBox`.
Ce micro logiciel est capable de communiquer avec les protocole modbus RS-485 (via une passerelle modbus) et le protocole http(s).

De manière récurente, la `InviseoBox` envoie vers l'url paramétrée, les données travaillées (moyenne, minimale, maximale, différence).

La `InviseoBox` est associé au compte du client (a un site précis) en utilisant un jeton d'authentification. Ainsi un site (bâtiment) peux avoir 0 ou plusieurs `InviseoBox` qui renvoie des données identifiées.

La pas de renvoie des donénes vers le serveur est parametrable de le docker-compose avec le parametre `interval`

## 🚀 Installation (Production)

Suivre la procédure d'installation d'un nouveau système pour la inviseobox [Procédure](./procedure_installation_inviseobox.md)

Il suffit d'exécuter les lignes de commande :

Connectez-vous au compte utilisateur inviseo sur la `inviseoBox`

```bash
# passer en root
su root
```

```bash
# installation de docker, sudo et git
apt-get install git docker docker-compose docker.io docker-clean docker-doc docker-registry sudo -y
# installer le user inviseo en sudo
sudo visudo
```

Entrer la ligne suivante dans le fichier a hauteur de la liste des utilisateurs :
`inviseo ALL=(ALL:ALL) ALL`

Taper ctrl + o et ctrl + x

Executer exit pourrevenir sur l'utilisateur inviseo

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

Modifiez le fichier `docker-compose.yml` pour ajouter les variables d'environnement suivantes, \<INVISEOBOX_TOKEN> et \<API_URL> (SURTOUT ne pas ajouter de / après l'URL. Vous pouvez faire comme l'exemple suivant : `https://domaine.com/api`).
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

- `token` : Token d'authentification de la InviseoBox, renvoyé par le serveur Inviseo lors de la création de la InviseoBox. Il est présent dans `workers.token`.
- `interval` : Délai en seconde entre chaque envoie de données vers le serveur Inviseo.
- `url` : URL de l'API Inviseo, sans le `/` à la fin.

### 📦 Fonctionnement et algorithimique

Tout d'abord, l'image watchtower permet de mettre à jour automatiquement l'image de la InviseoBox. Il est recommandé de la laisser dans le fichier `docker-compose.yml`. Cependant, le socket Docker doit être monté pour que Watchtower fonctionne correctement. Le chemin du socket Docker est par défaut `/var/run/docker.sock`, mais il peut être différent selon la configuration de votre système, donc il faut vérifier pour chaque installation.

Watchtower vérifie toutes les 5 secondes si une nouvelle version de l'image de la InviseoBox est disponible. Si c'est le cas, il télécharge la nouvelle image et redémarre le conteneur. Cette nouvelle image est téléchargée depuis le GitHub Container Registry (ghcr.io), elle même pushée depuis le GitHub Actions via l'action `macbre/push-to-ghcr`. Watchtower est configuré pour tirer la dernière image de la InviseoBox sur la branche `main` exclusivement.

La InviséoBox correctement configurée exécute un algorithme en boucle pour récupérer les données des appareils et les envoyer vers le serveur Inviseo.

Cet algorithme boucle :

- Instancier la base de données SQLite
- Récupérer les données des appareils (GET) : ``/api/workers/devices/data/token?=<TOKEN>`
- Pendant `<interval>` secondes :
  - Pour chaque appareil, pour chaque mesure :
    - Insérer les données relatives à l'appareil
    - Insérer les données relatives à la mesure
    - Insérer les données temporaires dans la base de données
- Aggréger les données en fonction de la configuration de la mesure
- Envoyer les données relatives à l'appareil et aux mesures (POST) : `/api/devices/status`
- Envoyer les données aggrégées vers le serveur Inviseo (POST) : `/api/fields/`

### 📝 Logs

Les logs sont accessibles grâce à la commande suivante :

```bash
sudo docker logs inviseobox
```

### Mise à jour (inviseoBox existante)

Pour mettre à jour le micro logiciel d'une inviseobox déjà en place suivez les étapes suivantes :

#### Down les containers

Il est très important d'arreter les containers sur la inviseoBox

Placez vous dans le dossier inviseobox 

```bash
cd inviseobox
```

et lancer la commande 

```bash
sudo docker-compose down
```

Le mot de passe par défaut de l'utilisateur inviseo est `inviseo`
Attention vous ne verrez pas de mot de passe se taper.

#### Supprimer le dossier inviseobox

Attention avant la suppression prenez soin de copier le fichier `docker-compose.yml` car la configuration du client est dedans.

```bash
cp docker-compose.yml ~/inviseo/docker-compose_save.yml
```

Supprimer le dossier `inviseobox` pour eviter les conflits

```bash
cd ..
cd ~/inviseo && sudo rm -rf inviseobox
```

#### Recloner le depot

Recloner le depot public

```bash
git clone https://github.com/inviseo/inviseobox/
```

#### Copier l'ancienne configuration

Executer commande

```bash
cp docker-compose_save.yml ~/inviseo/inviseobox/
cd inviseobox
```

N'oubliez pas de renommer le fichier comme avant

```bash
sudo mv docker-compose_save.yml docker-compose.yml
```

#### Redémarrer les containers

```bash
sudo docker-compose up -d
```

#### Vérification

Vérifier que tout c'est bien passé

```bash
sudo docker logs inviseobox
````

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
