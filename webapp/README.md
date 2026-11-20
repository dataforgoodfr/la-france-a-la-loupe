# La France à la Loupe

> Application web du projet "La France à la Loupe"

## Guide de démarrage

Bienvenue sur l'application web "La France à la Loupe".

Ce projet est basé sur [Astro](https://astro.build/) et [React](https://react.dev/). Ce guide vous aidera à configurer votre environnement de développement et à démarrer l'application.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Node.js](https://nodejs.org/) (version 22 ou supérieure)
- [npm](https://www.npmjs.com/) (installé avec Node.js par défaut)

## Installation et IDE

Il est recommandé d'utiliser [VSCode](https://code.visualstudio.com/) pour ce projet. Vous etes evidement libre d'utiliser un autre éditeur mais vous devrez alors le configurer vous-même.

### Ouvrir le Workspace

Le dossier `webapp` contient l'application web et possède sa propre configuration VSCode spécifique, incluant les extensions recommandées et les paramètres adaptés.

Pour que ces paramètres et extensions spécifiques soient pris en compte, vous devez ouvrir le dossier `webapp` directement dans VSCode.

Si vous ouvrer le dossier racine du projet (`la-france-a-la-loupe`) dans VSCode, les paramètres spécifiques au dossier `webapp` ne seront pas appliqués automatiquement.

### Installer les dépendances

Pour installer les dépendances du projet, ouvrez un terminal dans le dossier `webapp` et exécutez la commande suivante:

```bash
npm install
```

### Lancer l'application

Une fois les dépendances installées, vous pourrez lancer l'application en exécutant la commande suivante dans le terminal :

```bash
npm run dev
```

L'application sera accessible à l'adresse indiquée dans le terminal (par défaut `http://localhost:4321`).

## Choix techniques

L'application "La France à la Loupe" utilise les technologies suivantes :

- [Astro](https://astro.build/) pour le framework web et la structure des pages
- [React](https://react.dev/) pour la création des composants
- [Oxfmt](https://oxc.rs/docs/guide/usage/formatter.html) pour le formatage du code
