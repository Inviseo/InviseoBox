# InviseoBox
Un service léger et non-intrusif installé le client pour récupérer et envoyer les données vers le serveur Inviseo

## Installation (Production)

Il suffit normalement d'exécuter cette ligne de commande :

```bash
curl -sSL https://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@raw.githubusercontent.com/inviseo/inviseobox/main/install.sh | sudo bash -s <worder-id>
```

En précisant le `<worder-id>` de la box à installer.

## Installation (Développement)

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
sudo systemctl enable inviseo
sudo systemctl daemon-reload
sudo systemctl start inviseo
```

# Un script d'installation pour automatiser l'installation

# RESTE A FAIRE

- [ ] Réaliser les tests (unitaire, d'intégration, de bout en bout)
- [ ] Gestion des logs
- [ ] Permettre un script pour pull automatiquement le code