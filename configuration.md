# 📝 Configuration

Cette documentation décrit la stack Docker qui est mise en place avec ses variables d'environnements et ses services.

## Docker-compose.yml : la stack Docker

### Service inviseobox

 Ce service exécute l'image Docker ghcr.io/inviseo/inviseobox:latest, qui est le micro logiciel `InviseoBox`.
 
 Il fonctionne avec des `privilèges root`, se redémarre **toujours** en cas de problème, et **vérifie** régulièrement les mises à jour de l'image. 
 Il utilise des **variables d'environnement** pour spécifier un jeton d'authentification (token), l'intervalle de temps pour une opération (interval), et l'URL de l'API cible (url).

### Service watchtower

 Ce service utilise l'image `containrrr/watchtower:latest` pour **surveiller** et mettre à jour **automatiquement** le conteneur `inviseobox` toutes les **5 secondes**.
 Il supprime les anciennes images après la mise à jour. 
 Il a accès au socket Docker via le volume monté /var/run/docker.sock, ce qui lui permet de gérer d'autres conteneurs.

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