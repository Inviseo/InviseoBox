# Documentation installation `InviseoBox` (Dev/Prod/Mise a jour)

Cette documentation présente l'installation d'une `InviseoBox` pour :

* La production
* La mise a jour d'une ancienne `InviseoBox` (avant le service `watchtower` du docker-compose.yml)
* Le développement

## 🚀 Installation (Production)

Suivre la procédure d'installation d'un nouveau système pour la inviseobox [Procédure](./installation_debian_inviseobox_wyse.md)

Connecter vous sur la `InviseoBox` en SSH avec les identifiant attribués pour le compte inviseo

```bash
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

### Mise à jour (inviseoBox existante)

**Uniquement si le service `watchtower` est absent du docker-compose.yml**

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

### 📝 Logs

Les logs sont accessibles grâce à la commande suivante :

```bash
sudo docker logs inviseobox
```