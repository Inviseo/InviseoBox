# InviseoBox

Un service léger et non-intrusif installé sur le client pour récupérer et envoyer des données vers le serveur Inviseo.

## 🚀 Installation (Production)

Il suffit d'exécuter cette ligne de commande :

```bash
curl -H "Authorization: token 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" https://raw.githubusercontent.com/inviseo/inviseobox/main/install.sh -o install.sh && sudo bash install.sh <worder-id> <interval>
```

En précisant le `<worder-id>` de la box à installer, obtenu lors de la création de la box sur le serveur Inviseo, et l'`<interval>` de temps en secondes entre chaque envoi de données.

### 📝 Logs

Les logs sont stockés dans ``./inviseobox.log``.
Pour les consulter, vous pouvez utiliser la commande suivante :

```bash
tail -f inviseobox.log
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
