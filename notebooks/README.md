# Notebooks dédiés aux analyses exploratoires

Pour l'analyse exploratoire sur les différentes thématiques, nous avons prévu l'utilisation de notebooks [Marimo](https://marimo.io/). Par rapport à Jupyter, ils sont réactifs et exécutables comme des scripts Python.

## Installation

Marimo et ses dépendances s'installent automatiquement avec le reste du projet via uv.
```bash
uv sync
```

## Dépendances

Pour ne pas pousser Marimo et ses dépendances en production, si vous avez besoin d'ajouter une dépendance liée à votre notebook, ajoutez-la uniquement sur le groupe dev :
```bash
uv add --dev pandas matplotlib
```

## Démarrer Marimo et créer un notebook

Pour créer/ouvrir un notebook dans une thématique :
```bash
uv run marimo edit notebooks/[thématique]/[nom_notebook].py
```

Autrement vous pouvez ouvrir Marimo et utiliser son explorateur :
```bash
uv run marimo edit
```

## Notebook de démonstration

Dans ce notebook, vous trouverez un exemple d'analyse très basique à partir d'un jeu de données.
```bash
uv run marimo edit notebooks/education/reussite_bac_origine_sociale.py
```
