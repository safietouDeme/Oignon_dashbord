import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from models.sensitivity import SENSITIVITY_PARAMS

dash.register_page(
    __name__,
    path="/analyse",
    name="Analyse",
)

layout = dbc.Container(

    [

        html.H1(
            "Analyse et conclusion",
            className="page-title",
        ),

        html.Hr(),

        # =====================================
        # 1. Interprétation automatique
        # =====================================

        html.H4("Interprétation des derniers résultats"),

        html.Div(
            id="interpretation-container",
            children=dbc.Alert(
                "Lancez d'abord une optimisation dans le Dashboard pour "
                "voir apparaître l'interprétation ici.",
                color="secondary",
            ),
        ),

        html.Br(),

        # =====================================
        # 2. Analyse de sensibilité
        # =====================================

        html.H4("Analyse de sensibilité"),

        html.P(
            "Faites varier un paramètre du modèle autour de sa valeur "
            "actuelle (celle utilisée lors du dernier lancement du "
            "Dashboard) et observez son effet sur la rupture totale. "
            "Une recommandation ciblée sur ce paramètre s'affichera "
            "ensuite ci-dessous."
        ),

        dbc.Row(

            [

                dbc.Col(
                    [
                        html.Label("Paramètre à faire varier"),
                        dcc.Dropdown(
                            id="sensitivity-param",
                            options=[
                                {"label": label, "value": key}
                                for key, label in SENSITIVITY_PARAMS.items()
                            ],
                            value="budget",
                            clearable=False,
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.Label("Nombre de points testés"),
                        dbc.Input(
                            id="sensitivity-points",
                            type="number",
                            value=7,
                            min=3,
                            max=15,
                            step=1,
                        ),
                    ],
                    lg=3,
                ),

                dbc.Col(
                    [
                        html.Br(),
                        dbc.Button(
                            "Lancer l'analyse de sensibilité",
                            id="run-sensitivity",
                            color="primary",
                            className="w-100",
                            n_clicks=0,
                        ),
                    ],
                    lg=3,
                ),

            ],

            className="g-3",

        ),

        html.Br(),

        dcc.Loading(
            dcc.Graph(
                id="sensitivity-chart",
                config={"displayModeBar": False},
            ),
        ),

        html.Br(),

        # =====================================
        # 3. Recommandations
        # =====================================

        html.H4("Recommandations"),

        html.Div(
            id="recommendations-container",
            children=dbc.Alert(
                "Choisissez un paramètre ci-dessus puis lancez l'analyse "
                "de sensibilité pour voir apparaître une recommandation "
                "ciblée sur ce paramètre.",
                color="secondary",
            ),
        ),

    ],

    fluid=True,

    className="page",

)
