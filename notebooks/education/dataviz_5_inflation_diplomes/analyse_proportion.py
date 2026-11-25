import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import datetime
    import pandas as pd
    import marimo as mo
    import matplotlib.pyplot as plt

    return datetime, mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    API du ministère de l'éducation nationale
    """)
    return


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
    return


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
    return


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
    return


@app.cell
def _(datetime, df):
    df_2024 = df[df["annee"] == datetime.date(2024, 1, 1)]
    return


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    df["caracteristique"].unique()
    return


@app.cell
def _(df):
    df[df["caracteristique"] == "données provisoires"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Filtrage par colonne
        - On veut le pourcentage par génération
        - On prend uniquement les données définitives (sinon il y a des doublons de séries ex. pour l'année 1971 il y aura deux fois le bac général, ...)
    """)
    return


@app.cell
def _(df):
    COLS = ["annee", "pourcentage_de_bacheliers_dans_une_generation", "serie"]
    df2 = df[df["caracteristique"] == "données définitives"][COLS]
    return (df2,)


@app.cell
def _(df2):
    df2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vue global: Tous baccalauréats
    """)
    return


@app.cell
def _(df2):
    df3 = df2[df2["serie"] == "Tous baccalauréats"].sort_values(by=["annee"])
    return


@app.cell
def _(df2):
    df2.sort_values(by=["annee"], inplace=True)
    return


@app.cell
def _(df2):
    y_tous = df2[df2["serie"] == "Tous baccalauréats"]["pourcentage_de_bacheliers_dans_une_generation"]

    y_gen = df2[df2["serie"] == "Bac général"]["pourcentage_de_bacheliers_dans_une_generation"]

    y_techno = df2[df2["serie"] == "Bac technologique"]["pourcentage_de_bacheliers_dans_une_generation"]

    y_pro = df2[df2["serie"] == "Bac professionnel"]["pourcentage_de_bacheliers_dans_une_generation"]
    return y_gen, y_pro, y_techno, y_tous


@app.cell
def _(df):
    x = df["annee"].unique()
    return (x,)


@app.cell
def _(y_gen, y_pro, y_techno, y_tous):
    print(len(y_tous), len(y_gen), len(y_techno), len(y_pro))
    return


@app.cell
def _(df, plt, x, y_tous):
    plt.title("Proportion de tous les bachelers au cours des années")
    plt.plot(x, y_tous, label="Tous baccalauréats")
    plt.plot()
    plt.plot(df)
    plt.legend()
    return


@app.cell
def _(df2):
    df2.plot(x="annee", y=["pourcentage_de_bacheliers_dans_une_generation"] )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
