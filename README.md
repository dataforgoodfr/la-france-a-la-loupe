# La France à la loupe

Une collaboration Data For Good et The Conversation.

## Guide de démarrage

Ce guide explique comment récupérer le projet en local et contribuer au code.

### Installer les outils

Installer les outils suivants:
- Git: https://git-scm.com/downloads
- VS Code (recommandé mais pas obligatoire): https://code.visualstudio.com/
- Pour les prérequis, voir la section installation ci-dessous (python, uv)

### Installer le projet en local
- Ouvrir un terminal (e.g. PowerShell, terminal VS Code)
- Se déplacer vers le dossier où cloner le projet:

```bash
cd path/to/folder
```

- Dans GitHub, ouvrir la page du projet, cliquer sur le bouton code et copier l'URL HTTPS
- Cloner le projet:

```bash
git clone URL_PROJET
```

### Créer et récupérer une branche Git

- Dans GitHub, créer une nouvelle branche dans l'issue sur laquelle vous travaillez.
- Dans le terminal, récupérer les branches:

```bash
git fetch origin
```

- Basculer sur la nouvelle branche:

```bash
git switch nom-branche
```

- Pour vérifier la branche active

```bash
git branch --show-current
```

### Modifier le code et enregister les modifications

- Faire les changement nécessaires
- Avant de faire le commit, exécuter la commande suivante pour appliquer les règles de formatage du projet:

```bash
uv run ruff format
```

- Pour ajouter les fichiers modifiés:

```bash
git add nom_fichier.py
```

ou pour tous les fichiers:

```bash
git add .
```

- Créer un commit avec une description des changements claire:

```bash
git commit -m "Description des modifications"
```

- Envoyer les modifications sur GitHub:

```bash
git push
```

Si vous utilisez VS Code, les opérations Git peuvent être réalisées depuis l'onglet Source Control:
- Vérifier la branche active
- Ajouter les fichiers modifiés au stage en cliquant sur +
- Renseigner un message décrivant les modifications
- Cliquer sur Commit
- Cliquer sur Push ou Sync Changes pour envoyer les modifications sur GitHub

### Créer une pull request

- Dans GitHub, créer une pull request depuis la branche créée
- Vérifier que l'issue associée est bien référencée
- Vérifier que les check automatiques sont passés avant de demander un merge

## Prérequis

- python >= 3.12
- uv
- just
- pre-commit
- tox

## Installation

- [Installation de Python](#installation-de-python)

Ce projet utilise [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances Python. Il est préréquis pour l'installation de ce projet.

Si vous venez d'installer `uv`, mettez à jour la variable `PATH` :

```bash
uv tool update-shell
```

Puis fermez et redémarrez votre terminal.

Pour installer just, pre-commit et tox :

```bash
uv tool install just
uv tool install pre-commit
uv tool install tox
```

Installation des scripts pre-commit :

```
pre-commit install
```

Une fois installé, il suffit de lancer la commande suivante pour installer la version de Python adéquate, créer un environnement virtuel et installer les dépendances du projet.

```bash
uv sync
```

A l'usage, si vous utilisez VSCode, l'environnement virtuel sera automatiquement activé lorsque vous ouvrirez le projet. Sinon, il suffit de l'activer manuellement avec la commande suivante :

```bash
source .venv/bin/activate
```

Ou alors, utilisez la commande `uv run ...` (au lieu de `python ...`) pour lancer un script Python. Par exemple :

```bash
uv run pipelines/run.py run build_database
```

## Lancer les precommit-hook localement

[Installer les precommit](https://pre-commit.com/)

```bash
pre-commit run --all-files
```

## Utiliser Tox pour tester votre code

```bash
tox -vv
```

## Utiliser l'application web

Pour lancer le serveur web :

```bash
just webapp
```

Ouvrir [http://localhost:3000/](http://localhost:3000/)

## Utiliser le serveur S3

Démarrer le serveur

```bash
docker-compose up -d
```

Vérifier l'état du serveur

```
docker exec garage /garage status
```

Stopper le serveur

```bash
docker-compose up -d
```

Voir les logs du serveur

```bash
docker logs garage
```

Attention. En cas d'erreur de permission, il y a deux solutions possibles :

1. créer un group `docker` et y ajouter son compte (recommandé)
   voir [Linux post-installation steps for Docker Engine | Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
2. utiliser `sudo`
