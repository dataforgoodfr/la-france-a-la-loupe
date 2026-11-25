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
    L'objectif de cet exemple est de montrer qu'il est possible de faire l'extraction, l'analyse et le traitement des données en utilisant uniquement les fonctions spécifique SQL de DuckDB et l'interface graphique de Marimo.

    ⚠️ Dans les paramètres du notebook, il est recommandé de choisir "SQL Output Type" = "Polars".
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

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 - Lecture des données en SQL

    DuckDB permet de lire des fichiers Parquet en SQL depuis une URL. Pas besoin de les télécharger et de les stocker dans une *dataframe*.

    Le résultat de la requête est stocké par défaut dans une variable *_df*. Dans Marimo, les variables préfixées par "_" sont privées et ne sont pas accessibles depuis une autre cellule. Les deux requêtes suivantes peuvent donc avoir le même *output* sans que cela pose problème.

    L'inconvénient, c'est qu'on "télécharge" le fichier Parquet à chaque requête SQL.
    """)


@app.cell
def _():
    # URL du fichier parquet
    url_parquet_va_colleges = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-valeur-ajoutee-colleges/exports/parquet/?lang=fr&timezone=Europe%2FParis"
    return (url_parquet_va_colleges,)


@app.cell
def _(mo):
    # Affiche un slider pour définir la valeur du limit appliqué à la requête SQL
    # Ca n'est pas très utile mais c'est l'occasion de présenter une fonctionnalité Marimo
    limit = mo.ui.slider(label="Limit SQL", start=10, stop=10000, step=10)
    mo.md(f"Valeur du LIMIT de la requête SQL : {limit}")
    return (limit,)


@app.cell(hide_code=True)
def _(limit, mo, url_parquet_va_colleges):
    _df = mo.sql(
        f"""
        -- Prévisualiser la table (en utilisant une variable Python)
        SELECT *
        FROM read_parquet('{url_parquet_va_colleges}')
        LIMIT {limit.value}
        """
    )


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        """
        -- Villes de Seine-Saint-Denis ayant les collèges avec la meilleure valeur-ajoutée moyenne
        -- Sans utiliser la variable Python, en intégrant l'URL directement dans la requête
        -- Avec la fonction visualize de Marimo, on peut faire un graphique très facilement à partir des données, on peut ensuite récupérer le code Python pour afficher le graphique dans une cellule (penser à importer altair)
        SELECT commune, ROUND(AVG(va_du_taux_de_reussite_g), 2) AS moyenne_va
        FROM read_parquet('https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-valeur-ajoutee-colleges/exports/parquet/?lang=fr&timezone=Europe%2FParis')
        WHERE code_departement = '93'
        GROUP BY commune
        ORDER BY AVG(va_du_taux_de_reussite_g) DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 - Transformations successives via SQL

    Ici, on utilise des variables d'*output* globales pour passer une table d'une cellule SQL à une autre. On stocke les données en mémoire plutôt que de repartir du fichier Parquet en ligne à chaque fois.

    Dans cet exemple on reproduit les principales étapes du pipeline dbt de production.

    Pour mémoire :
    >**staging**
    >
    >Les models staging n'appliquent que des changements légers sur la donnée :
    >
    > - renommage
    > - typing
    > - conversion (centimes en euros par ex)
    > - catégories (bucket, booléens)
    >
    >A ce niveau, pas de joins ou d'agrégations.
    >
    >**intermediate**
    >
    >Avec les models intermediate on fait les premières jointures. On change au besoin la granularité (communes->departements).
    >
    >**mart**
    >
    >Les marts sont dans la couche qui sert le front. Les données doivent être dénormalisées, prêtes à être utilisées.
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Staging
    """)


@app.cell
def _(mo, url_parquet_va_colleges):
    staging = mo.sql(
        f"""
        /* Transformations de base extraction de l'année depuis session
           conversion des codes de la colonne secteur
           sélection des colonnes à conserver */
        select
            strftime("session", '%Y') as annee,
            uai,
            case
            	when secteur = 'PR' then 'Privé'
            	when secteur = 'PU' then 'Public'
            	else secteur
            end as secteur,
            taux_de_reussite_g,
            va_du_taux_de_reussite_g
        from read_parquet('{url_parquet_va_colleges}')
        """
    )
    return (staging,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intermediate
    """)


@app.cell(hide_code=True)
def _(mo):
    ref_etab = mo.sql(
        """
        -- Téléchargement du référentiel des établissement et stockage sous la forme d'une table
        -- La colonne "position" qui contient les données géospatiales est affichée comme un binaire
        select *
        from read_parquet('https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-cites_scolaires/exports/parquet/?lang=fr&timezone=Europe%2FParis')
        """
    )
    return (ref_etab,)


@app.cell
def _(mo, ref_etab, staging):
    intermediate = mo.sql(
        """
        -- Chargement de l'extension duckdb permettant de manipuler des données de localisation
        install spatial;
        load spatial;

        -- Jointure avec le référentiel des établissements
        -- Extraction des coordonnées spatiales sous la forme x / y
        select
            a.*,
            b.code_commune, -- code INSEE
            b.appellation_officielle, -- nom de l'établissement en casse riche
            st_x(b.position::GEOMETRY) as x,
            st_y(b.position::GEOMETRY) as y
        from staging a
        left join ref_etab b on a.uai = b.uai
        """
    )
    return (intermediate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Mart
    """)


@app.cell
def _(intermediate, mo):
    _mart = mo.sql(
        """
        -- Sélection des données pour faire une carte comparative de la valeur-ajoutée des Collège pour l'année 2025
        select
            annee,
            code_commune,
            appellation_officielle,
            secteur,
            taux_de_reussite_g,
            va_du_taux_de_reussite_g,
            x,
            y
        from intermediate
        where va_du_taux_de_reussite_g is not null
        and annee = '2025'
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reste plus qu'à faire une carte !
    """)


if __name__ == "__main__":
    app.run()
