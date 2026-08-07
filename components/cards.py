from dash import html
import dash_bootstrap_components as dbc


def InfoCards():

    cards = [

        {
            "icon": "bi bi-globe-africa",
            "title": "Contexte",
            "text": """
            L'oignon est un produit agricole stratégique au Sénégal.
            Les fortes fluctuations de prix au cours de l'année
            affectent aussi bien les producteurs que les consommateurs.
            """
        },

        {
            "icon": "bi bi-bullseye",
            "title": "Objectif",
            "text": """
            Déterminer une stratégie optimale de production,
            stockage et importation permettant de stabiliser
            les prix tout au long de l'année.
            """
        },

        {
            "icon": "bi bi-cpu",
            "title": "Méthodologie",
            "text": """
            Utilisation d'un modèle d'optimisation convexe
            résolu sous Python (CVXPY) avec visualisation
            interactive sous Dash.
            """
        }

    ]

    return html.Section(

        className="info-section",

        children=[

            dbc.Container(

                [

                    html.Div(

                        [

                            html.H2(
                                "Pourquoi cette étude ?",
                                className="section-title"
                            ),

                            html.P(
                                """
                                Cette plateforme constitue un outil d'aide
                                à la décision permettant d'analyser différents
                                scénarios de gestion de l'oignon au Sénégal.
                                """,
                                className="section-description"
                            )

                        ],

                        className="section-header"

                    ),

                    dbc.Row(

                        [

                            dbc.Col(

                                dbc.Card(

                                    dbc.CardBody(

                                        [

                                            html.Div(

                                                html.I(
                                                    className=card["icon"]
                                                ),

                                                className="card-icon"

                                            ),

                                            html.H4(
                                                card["title"],
                                                className="card-title"
                                            ),

                                            html.P(
                                                card["text"],
                                                className="card-text"
                                            ),

                                            html.A(

                                                "En savoir plus",

                                                href="#",

                                                className="card-link"

                                            )

                                        ]

                                    ),

                                    className="info-card"

                                ),

                                lg=4,
                                md=6,
                                sm=12

                            )

                            for card in cards

                        ],

                        className="g-4"

                    )

                ]

            )

        ]

    )