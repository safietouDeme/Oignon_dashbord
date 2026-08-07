import numpy as np


def compute_metrics(df):

    cout_total = (
        df["Cout_stockage"].sum()
        + df["Cout_importation"].sum()
    )

    import_total = df["Importation"].sum()

    stock_max = df["Stock"].max()

    reduction_prix = (
        (
            df["Prix_initial"].mean()
            - df["Prix_optimal"].mean()
        )
        / df["Prix_initial"].mean()
    ) * 100

    satisfaction = (
        np.minimum(
            df["Disponibilite"],
            df["Demande"]
        ).sum()
        / df["Demande"].sum()
    ) * 100

    return {

        "cout_total": cout_total,

        "import_total": import_total,

        "stock_max": stock_max,

        "reduction_prix": reduction_prix,

        "satisfaction": satisfaction

    }