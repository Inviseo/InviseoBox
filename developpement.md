# Consignes pour le développement

## Commit

Chaque commit devront avoir un **message significatif et explicite**.

les commits avec un message comme "Mise a jour documentation", "Update files", "." seront rejeté pour a simple raison que nous ne pouvons pas bien suivre le déroulement du développement

Voici des exemples de messages acceptables : 
* "Ajout d'une section consignes de développement dans readme.md"
* "Correction du bug pour la mise a jour de la liste des appareils"
* "Amélioration des performance api.py : reduction de la complexité algorithmique"

Chaque commit devra correspondre a **une seule et unique issue**

Les commits sans issue associée seront rejetés
Les commits qui corrigent plusieurs issues en même temps seront aussi rejetés

## Pull Request (PR)

Chaque `Pull Request (PR)` est obligatoirement associée a une issue

Chaque `Pull Request` sont **obligatoirement** contienne a **au moins un** commit en rapport avec l'issue concernée

Chaque `Pull Request` ne peut contenir que des commit en rapport avec l'issue.

Chaque `Pull Request` créée sera validée et fusionnée par un responsable technique.
Si aucun responsable technique n'existe au dessus du propriétaire de la `Pull Request` elle pourra être fusionnée.

Les `Pull Requests` sur la branche `main` ne peut être fait qu'avec un reponsable technique car cette branche est automatiquement deployée sur les `InviseBox` installée chez nos clients. Elle ne peut donc souffrir d'aucun problème majeur.

## Tests

Pour chaque code produit, les `Tests Unitaires (TU)` doivent être créés et valides (Voir le travail en TDD).

Tout coude n'ayant pas de tests unitaire associés **et** valides seront rejeté

## Continious Integration (CI)

Il est strictement interdit de supprimer/désactiver la [CI](./.github/workflows/ci.yml)

Elle est notre garantie minimale que nous fesons bien le travail

## Continious Deployment (CD)

Vous ne devrez **jamais** supprimer/desactiver/modifier la [CD](./.github/workflows/cd.yml)

Elle nous garantie que le package docker de la `InviseoBox synchronisé` avec la branche git `main`.

## Branches

La branche `main` est celle dont le code est deployé en synchronisation sur tous les `InviseoBox`.
Aucun ajout/suppression/modification ne peut être fait sans vérirication, tests unitaires passés et validation avec un responsable

La branche `develop` est la branche dite `bêta` sur laquelle nous testons notre travail.