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

## Fonctionnalités

Le code du micro-logiciel est écrit en python 3.

Les packages disponibles pour traiter les requêtes et réponses de différents protcoles, ainsi que l'excellent support de python du linux, nous fournis un environnement parfait pour faire évoluer notre `InviseoBox`.

Actuellement la `InviseoBox` prend en charge 2 protocoles :
* HTTP(S)
* Modbus (RS-485)

Les futurs protocoles qui devront être pris en charge par ordre de priorité :
* LoRa
* KNX
* Les autres Modbus

## Utilisation de base

Dans l'idée, nos clients sont souvent amenés a créer un réseau dédié aux `InviseoPus` (capteurs) pour des raisons de sécurité et confidentialité.

La `InviseoBox` doit être préparée et configurée dans nos locaux **AVANT** l'installation chez le client.
Pour vérifier que tous est bon il suffit de rensigner la `InviseoBox` sur notre logiciel et d'y ajouter les `InviseoPus` (capteurs).
Le tout peut se faire via notre **interface d'administration** accessible uniquement avec le compte **super admin** contact@inviseo.fr

Pour installer la `InviseoBox` chez un client il suffit de brancher le cable réseau de type `RJ-45` de la `InviseoBox` dans la baie serveur de notre client. a défaut sur le routeur qui fournit le réseau aux `InviseoPus`.

Brancher ensuite l'alimentation.

Les `InviseoPus` ayant déjà été préparé avec le **SSID** et **mot de passe** du réseau le simple fait de les brancher suffira.

Il convient ensuite de vérifier chaque `InviseoPus` en tapant dans la barre d'adresse **l'adresse IP** de la `InviseoPus` afin de vérifier les retours et la présence de données.

Il convient, afin d'être exhaustif, de vérifier les logs de la `InviseoBox`.
Pour cela vous devez récupérer son IP avec `netdiscover` (pour linux) ou [advanced IP Scanner](./logiciels/Advanced_IP_Scanner_2.5.4594.1.exe) sur Windows 10/11.

## Installation Debian pour nouvelle InviseoBox
[Procedure installation Debian](./installation_debian_inviseobox_wyse.md)

## Procedure installation InviseoBox
[Procedure installation micro logiciel inviseobox](./installation.md)

## Configuration
[Configuration](./configuration.md)

## Consignes de développement
[Consignes de  developpement](./developpement.md)

## Dépannage & FAQ
[Depannage et FAQ](./depannage.md)

## Contributeurs
[Contributeurs](./contribution.md)