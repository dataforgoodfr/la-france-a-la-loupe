import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import datetime

    import pandas as pd

    return datetime, pd


@app.cell
def _():
    # https://www.data.gouv.fr/dataservices/explore-api-v2-75
    API_URL = "https://data.education.gouv.fr/api/explore/v2.1/"
    return (API_URL,)


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
def _(datetime, df):
    df_2024 = df[df["annee"] == datetime.date(2024, 1, 1)]
    return (df_2024,)


if __name__ == "__main__":
    app.run()
