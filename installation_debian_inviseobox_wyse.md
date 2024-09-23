# Préparation `Base OS` pour la inviseBox

## Installer Debian `latest`

Debian est l'OS basé sur `GNU/Linux` que nous utilisons pour les inviseoBox.
Chaque nouvelle inviseoBox doit être formaté et réinstallé avec un nouveau système [Debian latest](https://www.debian.org/download)

Télécharger l'image `ISO`.

Préparer une clé bootable (prévoyez une clé USB d'une capacité comprise en 8 et 16GO).

Pour créer une clé bootable il existe plusieurs moyens.
Une facon simple est d'utiliser une interface graphique portable et cross platforme comme [BalenaEtcher](https://etcher.balena.io/)

Une fois la clé bootable prête, munissez-vous d'un dell wyse (aujourd'hui nous les utilisons).

Brancher ecran, clavier, souris et alimentation.

Lancer le dell wyse en appuyant sur le bouton d'alimentation.

Marteler la touche `supp` sur clavier pour lancer le `BIOS`.

Le mot de passe du `BIOS` pour ces appareils est `Fireport`

Activer le `BOOT USB`.

Insérer votre clé et redémarrer.

Continuer à appuyer sur `supp` et rendez vous dans le `Boot Order`.

Placer votre clé au sommet de la liste et taper `F10`.

Le Wyse redémarre et devrait booter sur votre clé.

L'installateur Debian va se lancer.

Choissiez la langue et configuration `Français`

Comme nom de machine entrer `inviseobox` Si plusieurs son présente réespecter la nomenclature suivante `inviseobox` + {{numéro d'instance de la box}}
Exemple : `inviseobox1`, `inviseobox2`

Pour l'utilisateur `root` mettre le mot de passe `root`
Pour l'utilisateur suivant choissez `inviseo` avec comme mot de passe `inviseo`

Ne forcer pas `UEFI`

Utiliser le disque entier

Choissez le disque principal commençant par `sda`

Mettre tout sur une seule partition

Valider et terminer les changements.

laisser l'installation se faire.

Choissier le dépôt `deb.debian.org`

Laisser le mandataire vide

accepter les demandes d'envoie de statistiques.

Laisser uniquement cocher `serveur SSH` et `utilitaires usuels du système`

Laisser `Grub` s'installer sur le disque `sda`

Laisser l'installation se faire.

## Configurer le démarrage automatique

Vous rendre dans le BIOS (SUPP au démarrage et mot de passe `Fireport`).

Rendez-vous dans l'onglet `Advanced`

trouver l'option ` Power Loss Recovery Option` et choissiez la valeur `Always On`

Plus bas, sur la partie `AUTO Power-On` ouvrer le menu

Sur l'option de ce menu, mettre `SET AUTO Power-On` sur `Enabled` ainsi que tous les jours de la semaine.

Faites `F10' pour sauvegarder.


## Test Auto Power-On

Une fois l'auto power-on configuré faite le test suivant : 
- éteignez le Wyse
- Débrancher l'aimentation pour simuler une panne de courant
- Rebrancher l'aimentation
=> Le wyse devrait démarrer.

## Installation de l'utilisateur sudo inviseo

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

Executez les commandes suivantes pour désactiver lamise en veille et l'hybernation

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo systemctl set-default multi-user.target
```