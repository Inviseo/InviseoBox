# InviseoBox

Un service léger et non-intrusif installé sur le client pour récupérer et envoyer des données vers le serveur Inviseo.

## 🚀 Installation (Production)

Il suffit d'exécuter cette ligne de commande :

```bash
git clone https://github.com/inviseo/inviseobox/ && cd inviseobox
```

### 📝 Configuration

Modifiez le fichier `docker-compose.yml` pour ajouter les variables d'environnement suivantes :

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
docker logs inviseobox
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
