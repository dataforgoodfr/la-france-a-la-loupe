import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import datetime

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return datetime, mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    API du ministère de l'éducation nationale
    """)


@app.cell
def _():
    # https://www.data.gouv.fr/dataservices/explore-api-v2-75
    API_URL = "https://data.education.gouv.fr/api/explore/v2.1/"
    return (API_URL,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Fonction pour extraire en parquet de la donnée à partir d'un dataset_id
    """)


@app.cell
def _(API_URL, pd):
    def get_dataset_parquet(dataset_id: str):
        url = API_URL + f"catalog/datasets/{dataset_id}/exports/parquet"
        try:
            df = pd.read_parquet(url)
            return df
        except pd.errors.Pandas4Warning:
            print("There was an error")

    return (get_dataset_parquet,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On récupère le dataset de la propotion de bachier
    """)


@app.cell
def _():
    # https://data.education.gouv.fr/explore/assets/fr-en-proportion-de-bacheliers-dans-une-generation/
    DATASET_ID = "fr-en-proportion-de-bacheliers-dans-une-generation"
    return (DATASET_ID,)


@app.cell
def _(DATASET_ID, get_dataset_parquet):
    df = get_dataset_parquet(DATASET_ID)
    return (df,)


@app.cell
def _(df):
    df.info()


@app.cell
def _(df):
    df.head()


@app.cell
def _(df):
    df["caracteristique"].unique()


@app.cell
def _(df):
    df[df["caracteristique"] == "données provisoires"]


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Filtrage par colonne
        - On veut le pourcentage par génération
        - On prend uniquement les données définitives (sinon il y a des doublons de séries ex. pour l'année 1971 il y aura deux fois le bac général, ...)
    """)


@app.cell
def _(df):
    COLS = ["annee", "pourcentage_de_bacheliers_dans_une_generation", "serie"]
    df2 = df[df["caracteristique"] == "données définitives"][COLS]
    return (df2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vue global: Tous baccalauréats
    """)


@app.cell
def _(df2):
    df2.sort_values(by=["annee"], inplace=True)


@app.cell
def _(df2):
    y_tous = df2[df2["serie"] == "Tous baccalauréats"][
        ["annee", "pourcentage_de_bacheliers_dans_une_generation"]
    ]

    y_gen = df2[df2["serie"] == "Bac général"][
        ["annee", "pourcentage_de_bacheliers_dans_une_generation"]
    ]

    y_techno = df2[df2["serie"] == "Bac technologique"][
        ["annee", "pourcentage_de_bacheliers_dans_une_generation"]
    ]

    y_pro = df2[df2["serie"] == "Bac professionnel"][
        ["annee", "pourcentage_de_bacheliers_dans_une_generation"]
    ]
    return y_gen, y_pro, y_techno, y_tous


@app.cell
def _(df2):
    type(df2["annee"])


@app.cell
def _(plt, y_gen, y_pro, y_techno, y_tous):
    plt.title("Proportion de tous les bachelers au cours des années")
    plt.plot(
        y_tous["annee"],
        y_tous["pourcentage_de_bacheliers_dans_une_generation"],
        label="Tous baccalauréats",
    )
    plt.plot(
        y_gen["annee"],
        y_gen["pourcentage_de_bacheliers_dans_une_generation"],
        label="Gen",
    )
    plt.plot(
        y_techno["annee"],
        y_techno["pourcentage_de_bacheliers_dans_une_generation"],
        label="Techno",
    )
    plt.plot(
        y_pro["annee"],
        y_pro["pourcentage_de_bacheliers_dans_une_generation"],
        label="Pro",
    )
    plt.legend()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A expliquer:

    - Pique en 2010 des bac pro => Possible réforme de Sarko sur pour envoyer ceux qui abandonne la seconde et après la 3ème en bac pro: https://www.letudiant.fr/educpros/actualite/bilan-du-quinquennat-sarkozy-un-bac-pro-en-trois-ans-bien-installe.html

    - Croissance à partir de 1990 des bac gen

    - Explosion du nombre de bachelier en 1997 => Pourrait correspondre à la période de baby-boom en france (pas sûre): https://fr.wikipedia.org/wiki/Baby-boom#/media/Fichier:Taux_de_natalit%C3%A9_en_France_de_1901_%C3%A0_2016.svg

    - Petit pique du bac techno en 1992 => Réforme avec la création de filière STI, STT (https://fr.wikipedia.org/wiki/Baccalaur%C3%A9at_technologique#1992%E2%80%932007)
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On observe bien une inflation des diplômes au fil des années
    Depuis 2010 on a une très grosse montée des diplomés et ça ne fait que de croître.

    On peut se poser comme question:
    - Par région comment ça se passe ? La variation de bachelier par région
    - Combien travail après le BAC
    - Combien entre à l'université et combien en sont diplomé. Regarder la répartition bachelier gen, tech, pro
    - Combien vont en BTS/DUT ou formation professionnalisante et combien en sont diplomé. Regarder la répartition bachelier gen, tech, pro
    - Est-ce qu'il y a suffisemment de place pour acceuillir ses étudiants ?
    - La direction que prends les étudiants en fonction du cursus d'étude sup
    - Pourquoi les élèves veulent faire des études longues
    - Regarder le CAP
    - Regarder le VAE (diplôme obtenu après une expérience pro)
    - L'algorithme est-il une solution pour gérer l'augmentation des élèves et les limites sturcturelles ?
    - Comment cette inflation fait baisser la valeur des diplomes et aussi créer des privilièges ?
    - Quels sont les nouveaux critères ?
    """)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
