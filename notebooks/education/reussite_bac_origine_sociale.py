import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Présentation du notebook

    Analyse du jeu de données "Réussite au baccalauréat selon l’origine sociale" disponible sur https://data.education.gouv.fr/explore/assets/fr-en-reussite-au-baccalaureat-origine-sociale/

    Conclusion rapide : il nous manque des données de l'INSEE sur la part de chaque catégorie socio-professionnelle dans la population française pour faire une analyse pertinente
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1- Import des packages utiles
    """)


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import polars as pl
    import requests

    return alt, mo, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 - Téléchargement des données

    ### Option 1 - récupération des données via l'API

    La difficulté est que l'API publique de education.data.gouv limite les appels à 10 000 lignes, il n'est donc possible de passer au-delà qu'en passant un token de login (pas développé). Passer par l'API a peu d'intérêt si on utilise pas les paramètres de requêtage qu'elle propose.
    """)


@app.cell
def _(requests):
    # Fonction pour l'appel API
    def fetch_all(url, limit=100, stop_at=0):
        """Récupère les données paginées depuis une API ODS (data.education.gouv).

        Args:
            url: URL de l'endpoint /records.
            limit: Taille de page (max 100 pour cette API).
            stop_at: Plafond d'enregistrements à récupérer (0 = sans limite).
                     Utile pour respecter le quota de l'API publique.
        """
        all_rows = []
        offset = 0
        total = None

        while True:
            resp = requests.get(
                url,
                params={"lang": "fr", "limit": limit, "offset": offset},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()

            total = data["total_count"]
            results = data["results"]
            all_rows.extend(results)

            offset += limit

            # Troncature si stop_at est atteint
            if stop_at > 0 and len(all_rows) >= stop_at:
                all_rows = all_rows[:stop_at]
                break

            if offset >= total or not results:
                break

        print(f"Récupéré {len(all_rows)} / {total} enregistrements")
        return all_rows

    # URL de l'API
    # url_api_reussite_bac = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-reussite-au-baccalaureat-origine-sociale/records/"
    # Appel API
    # records = fetch_all(url_api_reussite_bac)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Option 2 - Téléchargement du fichier Parquet

    On télécharge obligatoirement l'ensemble des données sans possibilité de filtrer.
    """)


@app.cell
def _(requests):
    # URL du fichier parquet
    url_parquet_reussite_bac = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-reussite-au-baccalaureat-origine-sociale/exports/parquet/?lang=fr&timezone=Europe%2FParis"

    def fetch_file(url):
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    # Récupération des données
    parquet_file = fetch_file(url_parquet_reussite_bac)
    return (parquet_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Selon l'option choisie, on créée la dataframe Polars à partir d'une des deux sources
    """)


@app.cell
def _(parquet_file, pl):
    ## Option 1 - API
    # df = pl.DataFrame(records)
    ## Option 2 - Fichier Parquet
    df = pl.read_parquet(parquet_file)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 - Statistiques et visualisation interactive des données
    """)


@app.cell
def _(df):
    # Description statistique du jeu de données avec la méthode describe() de Polars
    df.describe()


@app.cell
def _(df, mo):
    # Affichage dans l'explorateur de table Marimo
    mo.ui.table(df)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 - Graphique exploratoire
    """)


@app.cell
def _(df, mo):
    # Graphique exploratoire : widget de filtrage par origine sociale
    social_filter = mo.ui.multiselect(
        options=df["origine_sociale"].unique().sort().to_list(),
        value=df["origine_sociale"].unique().sort().to_list(),
        label="Origine sociale",
    )
    return (social_filter,)


@app.cell
def _(alt, df, mo, pl, social_filter):
    # Filtrage réactif
    df_filtered = df.filter(pl.col("origine_sociale").is_in(social_filter.value))

    # Définition du graphique en ligne
    chart = (
        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("annee:O", title="Année"),
            y=alt.Y(
                "nombre_d_admis_au_baccalaureat_general:Q", title="Nb admis bac Gén"
            ),
            color=alt.Color(
                "origine_sociale:N",
                title="Catégorie",
                legend=alt.Legend(orient="bottom"),
            ),
            tooltip=[
                "annee",
                "origine_sociale",
                "nombre_d_admis_au_baccalaureat_general",
            ],
        )
        .properties(
            width=600,
            height=350,
            title="Évolution du nombre d'admis par origine sociale",
        )
    )

    # Affichage du graphique exploratoire et du filtre dynamique
    mo.vstack([social_filter, chart])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 - Analyse de test sur le cas des agriculteurs
    """)


@app.cell
def _(alt, df, pl):
    # Analyse du cas des agriculteurs
    category = "Agriculteurs exploitants"
    df_filtered_2 = df.filter(pl.col("origine_sociale") == category)

    # Définition du graphique pour les agriculteurs uniquement
    chart_2 = (
        alt.Chart(df_filtered_2)
        .mark_line(point=True)
        .encode(
            x=alt.X("annee:O", title="Année"),
            y=alt.Y(
                "nombre_d_admis_au_baccalaureat_general:Q", title="Nb admis bac Gén"
            ),
            tooltip=["annee", "nombre_d_admis_au_baccalaureat_general"],
        )
        .properties(
            width=600, height=350, title=f"Évolution du nombre d'admis - {category}"
        )
    )
    return category, chart_2


@app.cell
def _(category, chart_2, mo):
    # Affichage dans une cellule markdown
    mo.md(f"""
    ## Evolution du nombre de bachelier.ères dont les parents sont {category} depuis 1997

    {mo.as_html(chart_2)}

    On constate la baisse du nombre de bacheliers dont les parents sont agriculteurs depuis 1997. Mais est-ce que ce n'est lié au fait qu'il y a moins d'agriculteurs dans la population ? Il faudrait croiser avec les données de l'INSEE pour appliquer une correction en fonction de la part dans la population générale
    """)


if __name__ == "__main__":
    app.run()
