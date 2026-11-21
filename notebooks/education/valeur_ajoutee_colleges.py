import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analyse via **SQL** du jeu de données "Indicateurs de valeur ajoutée des collèges"
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Dans les paramètres du notebook, il est recommandé de choisir "SQL Output Type" = "Polars".
    En laissant "Default" le risque est de rencontrer des erreurs de connexion non fermées type :
    > Resource In Use Error: connection has an unfinished result from execute(); call complete() or abort(), or fetch until a fetch returns no rows, before other work on this connection, or use a separate connection from cursor()
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 - Import des packages utiles
    """)


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import requests

    return mo, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 - Récupération des données via l'API *data.education.gouv*

    Dans cet exemple, une condition est ajoutée, car l'API publique data.education.gouv limite les appels non loggés à 10 000 lignes.
    > if offset >= total or **offset >= 10000** or not results:<br>
    > &emsp;break
    """)


@app.cell
def _(pl, requests):
    url_ds_va_colleges = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-valeur-ajoutee-colleges/records/"

    def fetch_all(url, limit=100):
        """Récupère toutes les lignes à partir de l'API data.education.gouv (jusqu'à 10 000 pour rester sous le quota de l'API publique)"""
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
            if offset >= total or offset >= 10000 or not results:
                break

        print(f"Récupéré {len(all_rows)} / {total} enregistrements")
        return all_rows

    # Appel API et intégration des résultats dans une dataframe Polars
    records = fetch_all(url_ds_va_colleges)
    df = pl.DataFrame(records)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 - Lecture des données en SQL

    La dataframe créée à l'étape précédente est appelable comme une table en SQL.

    Le résultat de la requête est stocké par défaut dans une variable *_df*. Dans Marimo, les variables préfixées par "_" sont privées et ne sont pas accessibles depuis une autre cellule. Les deux requêtes suivantes peuvent donc avoir le même *output* sans que cela pose problème.
    """)


@app.cell
def _(mo):
    # Affiche un slider pour définir la valeur du limit appliqué à la requête SQL
    # Ca n'est pas très utile mais c'est l'occasion de présenter une fonctionnalité Marimo
    limit = mo.ui.slider(label="Limit SQL", start=10, stop=10000, step=10)
    return (limit,)


@app.cell(hide_code=True)
def _(df, limit, mo):
    _df = mo.sql(
        f"""
        -- Prévisualiser la table
        SELECT *
        FROM df
        LIMIT {limit.value}
        """
    )


@app.cell(hide_code=True)
def _(df, mo):
    _df = mo.sql(
        """
        -- Villes de Seine-Saint-Denis ayant les collèges avec la meilleure valeur-ajoutée moyenne
        SELECT commune, ROUND(AVG(va_du_taux_de_reussite_g), 2) AS moyenne_va
        FROM df
        WHERE code_departement = '93'
        GROUP BY commune
        ORDER BY AVG(va_du_taux_de_reussite_g) DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 - Transformations successives via SQL

    Ici, on utilise des variables globales pour passer une même table d'une cellule SQL à une autre.
    On peut reproduire les principales étapes du pipeline dbt de production
    """)


if __name__ == "__main__":
    app.run()
