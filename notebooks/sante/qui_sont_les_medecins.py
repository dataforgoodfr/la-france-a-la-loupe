import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return mo, pl


@app.cell
def _(mo, pl):
    chemin_lake = mo.notebook_dir() / "../../data/dev/lake/sante"
    effectifs = pl.read_parquet(
        f"{chemin_lake}/medecins_rpps_2012_2026_effectifs/*.parquet"
    )
    # effectifs  # à décommenter pour afficher toute la table
    return (effectifs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Structure de la table `effectifs`
    """)


@app.cell
def _(effectifs, mo):
    mo.vstack(
        [
            mo.md(
                f"**Dimensions** : {effectifs.height:,} lignes × {effectifs.width} colonnes"
            ),
            mo.md("**Colonnes et types**"),
            mo.ui.table(
                [
                    {"colonne": nom, "type": str(type_)}
                    for nom, type_ in effectifs.schema.items()
                ],
                page_size=25,
                selection=None,
            ),
            mo.md("**10 premières lignes**"),
            effectifs.head(10),
        ]
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Contenu et complétude des colonnes
    """)


@app.cell
def _(effectifs, pl):
    effectifs.describe().with_columns(pl.col(pl.Float64).round(1))


@app.cell
def _(effectifs, pl):
    effectifs.select(pl.all().n_unique())


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Unicité
    """)


@app.cell
def _(effectifs, mo):
    cle = [
        "territoire",
        "region",
        "departement",
        "specialites_agregees",
        "specialites",
        "exercice",
        "tranche_age",
        "sexe",
    ]
    mo.md(f"""
    - Lignes entièrement en double : **{effectifs.is_duplicated().sum()}**
    - Combinaisons de découpage en double : **{effectifs.select(cle).is_duplicated().sum()}**
    """)
    return (cle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Cohérence des totaux
    """)


@app.cell
def _(cle, effectifs, mo, pl):
    autres_cols = [c for c in cle if c != "sexe"]
    totaux_sexe = effectifs.filter(pl.col("sexe") == "0-Ensemble").select(
        autres_cols + ["effectif_2026"]
    )
    sommes_sexe = (
        effectifs.filter(pl.col("sexe") != "0-Ensemble")
        .group_by(autres_cols)
        .agg(pl.col("effectif_2026").sum().alias("somme_hommes_femmes"))
    )
    comparaison_sexe = totaux_sexe.join(sommes_sexe, on=autres_cols)
    ecarts_sexe = comparaison_sexe.filter(
        pl.col("effectif_2026") != pl.col("somme_hommes_femmes")
    )
    mo.md(f"""
    - Combinaisons comparées : **{comparaison_sexe.height:,}**
    - Écarts entre total ensemble et somme hommes + femmes : **{ecarts_sexe.height}**
    """)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Fiche d'identité des colonnes

    Pour chaque colonne : nombre de valeurs, min, max et liste des valeurs (si 20 ou moins)
    """)


@app.cell
def _(effectifs, mo, pl):
    mo.ui.table(
        [
            {
                "colonne": c,
                "nb de valeurs": effectifs[c].n_unique(),
                "min": str(effectifs[c].min()),
                "max": str(effectifs[c].max()),
                "valeurs": ", ".join(effectifs[c].unique().sort())
                if effectifs[c].dtype == pl.String and effectifs[c].n_unique() <= 20
                else "",
            }
            for c in effectifs.columns
        ],
        page_size=25,
        selection=None,
    )


if __name__ == "__main__":
    app.run()
