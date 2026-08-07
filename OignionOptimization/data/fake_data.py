import pandas as pd
import numpy as np


def get_fake_data():

    np.random.seed(42)

    mois = [
        "Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
        "Juil", "Août", "Sep", "Oct", "Nov", "Déc"
    ]

    # Production locale (forte pendant la saison)
    production = np.array(
        [650, 900, 1300, 1700, 1800, 1600,
         1200, 850, 600, 450, 500, 550]
    )

    # Demande nationale
    demande = np.array(
        [950, 920, 940, 980, 1000, 1030,
         1020, 1010, 990, 980, 960, 950]
    )

    # Importations simulées
    #importation = np.maximum(
       # demande - production,
        #100
    #)

     # IMPORTATION simulé
    importation = np.array(
        [120, 180, 420, 760, 1050, 980,
         700, 430, 210, 130, 110, 100]
    )

    # Stock simulé
    stock = np.array(
        [120, 180, 420, 760, 1050, 980,
         700, 430, 210, 130, 110, 100]
    )

    # Disponibilité
    disponibilite = production + importation + stock

    # Prix observés
    prix_initial = np.array(
        [520, 510, 470, 390, 340, 330,
         350, 390, 460, 520, 550, 540]
    )

    # Prix après optimisation
    prix_optimal = np.array(
        [470, 465, 450, 420, 390, 385,
         390, 410, 440, 455, 465, 470]
    )

    cout_stock = stock * 20

    cout_import = importation * 110

    df = pd.DataFrame({

        "Mois": mois,

        "Production": production,

        "Demande": demande,

        "Importation": importation,

        "Stock": stock,

        "Disponibilite": disponibilite,

        "Prix_initial": prix_initial,

        "Prix_optimal": prix_optimal,

        "Cout_stockage": cout_stock,

        "Cout_importation": cout_import

    })

    return df