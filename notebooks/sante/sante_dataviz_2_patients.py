import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Qui sont les patients ?
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'issue #122 liste cinq dimensions : zones rurales ou urbaines, zones favorisées ou défavorisées,
    taux d'emploi, maladies chroniques, espérance de vie.
    Je les répartis en deux familles :

    - **les données de santé**  : l'espérance de vie de la population, les maladies chroniques des soignés ;
    - **le contexte**, pour lire les écarts : la géographie, la pauvreté, l'emploi.

    ## Sources choisies

    - **Espérance de vie** : Insee, tableau DEP4 (état civil et estimations de population), par département.
      Mesurée sur l'ensemble des habitants.
    - **Maladies chroniques** : Assurance maladie, Data pathologies, par département, sexe et âge.
      Mesurée sur les patients pris en charge : une maladie non diagnostiquée ou non soignée n'y apparaît pas.
    - **Contexte** : à préciser (taux de pauvreté, revenu médian, taux d'emploi, grille de densité de l'Insee).


    ## À valider avec l'équipe

    - **le sujet** : l'état de santé des populations (espérance de vie, prévalence de maladies chroniques), le portrait des patients uniquement (âge, sexe, pathologies), ou les deux ?
    - **la lecture** : les disparités territoriales, qui semblent aller de soi avec une carte. Mais l'évolution dans le temps nous intéresse-t-elle ?
    - **le perimètre** : un seul angle (par ex croiser l'état de santé avec le taux de pauvreté), un portrait plus exhaustif avec les différentes données citées (ce qui impliquerait plusieurs cartes / de l'interactivité) ?

    ## Outils de visualisation

    Pour explorer :

    - **les moyennes groupées** : l'espérance de vie moyenne par classe de densité, ou par quintile de pauvreté, en barres ou en boîtes. Elles chiffrent l'écart ;
    - **le nuage de points**, un point par département (par exemple la pauvreté en abscisse, l'espérance de vie en ordonnée). Il montre la tendance et les exceptions.

    Pour la dataviz finale :

    - **les cartes côte à côte** : santé à gauche, contexte à droite. Simple et lisible, mais la comparaison se fait à l'œil ;
    - **la carte bivariée** : une seule carte, avec une palette 3 × 3 qui croise les deux variables. Elle montre directement les territoires « pauvres et en mauvaise santé », mais demande une légende un peu plus élaborée.
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Espérance de vie par département

    Source : Insee, tableau DEP4 (état civil et estimations de population), onglet 2025, données provisoires.
    """)


@app.cell
def _():
    import io

    import marimo as mo
    import polars as pl
    import requests

    return io, mo, pl, requests


@app.cell
def _(requests):
    url_dep4 = "https://www.insee.fr/fr/statistiques/fichier/8999023/4_Deces_mortalite_espvie_depreg.xlsx"
    contenu_dep4 = requests.get(url_dep4, timeout=30).content
    return (contenu_dep4,)


@app.cell
def _(contenu_dep4, io, pl):
    onglets_dep4 = pl.read_excel(
        io.BytesIO(contenu_dep4), sheet_id=0, has_header=False, raise_if_empty=False
    )
    list(onglets_dep4.keys())
    return (onglets_dep4,)


@app.cell
def _(onglets_dep4):
    onglets_dep4["2025"].head(15)


if __name__ == "__main__":
    app.run()
