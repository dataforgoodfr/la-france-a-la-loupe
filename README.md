# La France à la loupe

Une collaboration Data For Good et The Conversation.

## Guide de démarrage

Ce guide explique comment récupérer le projet en local et contribuer au code.
Note : vous aurez besoin d'utiliser le terminal.

## Prérequis

Vous aurez besoin des outils suivants :

- Git : https://git-scm.com/install/
- VS Code (ou un autre éditeur de code) : https://code.visualstudio.com/
- python >= 3.12
- uv
- geoparquet-io
- just
- pre-commit
- tox

## Installation des prérequis

- Télécharger et installer Python :

[Installation de Python](https://www.python.org/downloads/)

- Ce projet utilise [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances Python :

[Installation de uv](https://docs.astral.sh/uv/getting-started/installation/)

- Si vous venez d'installer `uv`, mettre à jour la variable `PATH` dans un terminal :

```bash
uv tool update-shell
```

Puis fermer et redémarrer votre terminal.

- Pour installer geoparquet-io, just, pre-commit et tox :

```bash
uv tool install geoparquet-io
uv tool install just
uv tool install pre-commit
uv tool install tox
```

### Installer le projet en local

Attention : la commande `git clone` crée un sous-dossier qui contiendra le projet.
Le code n'est donc pas copié dans le dossier courant mais dans le sous-dossier.

- Ouvrir un terminal (e.g. PowerShell, terminal VS Code).

- Se déplacer vers le dossier de votre choix où cloner le projet:

```bash
cd path/to/folder
```

- Dans GitHub, ouvrir la page du projet, cliquer sur le bouton code et copier l'URL HTTPS.

- Dans le terminal, cloner le projet:

```bash
git clone https://github.com/dataforgoodfr/la-france-a-la-loupe.git
```

- Rentrer dans le dossier du projet :

```bash
cd la-france-a-la-loupe
```

- Installer les scripts pre-commit :

```bash
pre-commit install
```

- La commande suivante installe la version de Python adéquate, crée un environnement virtuel et installe les dépendances du projet.

```bash
uv sync
```

- A l'usage, si vous utilisez VS Code, l'environnement virtuel sera automatiquement activé lorsque vous ouvrirez le projet.
Sinon, il suffit de l'activer manuellement avec la commande suivante :

```bash
source .venv/bin/activate
```

Ou alors, utiliser la commande `uv run ...` (au lieu de `python ...`) pour lancer un script Python.
Par exemple :

```bash
uv run pipelines/run.py run build_database
```

### Créer une nouvelle branche Git

- Ouvrir un terminal et mettre à jour la branche main :

```bash
git checkout main
git pull
```

- Créer un nouvelle branche pour traiter votre issue :

```bash
git branch ma-branche
git checkout ma-branche
```

Note : choisir un nom de branche en rapport avec votre issue, à la place de `ma-branche`.

### Modifier le code et enregister les modifications (git commit)

- Faire les changement nécessaires.

- Avant de faire le commit, exécuter la commande suivante pour appliquer les règles de formatage du projet :

```bash
uv run ruff format
```

- S'il y a eu des erreurs, lister les fichiers corrigés :

```bash
git status
```

- Ajouter les fichiers modifiés :

```bash
git add nom_fichier.py
```

Ou ajouter tous les fichiers :

```bash
git add .
```

- Créer un commit avec une description des changements claire :

```bash
git commit -m "Issue #123 : Description des modifications"
```

Attention : lors du premier commit de cette branche, penser à noter le numéro de l'issue dans la description.

- Envoyer les modifications sur GitHub:

```bash
git push -u origin ma-branche
```

Note : utiliser le vrai nom de votre branche, à la place de `ma-branche`.
Note : la partie `-u origin ma-branche` n'est nécessaire que lors du premier push de la branche.

Si vous utilisez VS Code, les opérations Git peuvent être réalisées depuis l'onglet Source Control:

- Vérifier la branche active
- Ajouter les fichiers modifiés au stage en cliquant sur +
- Renseigner un message décrivant les modifications
- Cliquer sur Commit
- Cliquer sur Push ou Sync Changes pour envoyer les modifications sur GitHub

### Créer une pull request

- Dans GitHub, créer une pull request à partir de votre branche
- Vérifier que l'issue associée est bien référencée
- Vérifier que les checks automatiques sont passés et qu'une review valide votre code avant de faire un merge

### Résoudre des conflits

Parfois il y a des conflits dûs à des changements dans la branche main.

- Ouvrir un terminal et mettre à jour la branche main :

```bash
git checkout main
git pull
```

- Mettre à jour votre branche avec les changements de la branche main :

```bash
git checkout ma-branche
git merge main
```

Note : utiliser le vrai nom de votre branche, à la place de `ma-branche`.

- Pour voir les fichiers qui contiennent des conflits :

```bash
git status
```

- Ouvrir les fichiers concernés et faire les changement nécessaires.

- Ajouter les fichiers modifiés :

```bash
git add nom_fichier.py
```

- Créer un commit (pas besoin de description) :

```bash
git commit
```

- Vérifier qu'il n'y a plus de conflits :

```bash
git status
```

- Envoyer les modifications sur GitHub:

```bash
git push
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

```bash
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
