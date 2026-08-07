from dash import html
import dash_bootstrap_components as dbc


def Hero():
    return html.Section(

        className="hero-section",

        children=[

            # Overlay sombre
            html.Div(className="hero-overlay"),

            dbc.Container(

                [

                    html.Div(

                        [

                            html.Div(
                                "APPLICATION D'AIDE À LA DÉCISION",
                                className="hero-badge"
                            ),

                            html.H1(
                                [
                                    "Optimisation de l'accessibilité",
                                    html.Br(),
                                    "de l'oignon au Sénégal"
                                ],
                                className="hero-title"
                            ),

                            html.P(
                                """
                                Une plateforme interactive permettant de simuler,
                                visualiser et analyser les stratégies optimales
                                de production, stockage et importation afin de
                                stabiliser les prix de l'oignon.
                                """,
                                className="hero-description"
                            ),

                            html.Div(

                                [

                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-bar-chart-line-fill me-2"),
                                            "Découvrir le Dashboard"
                                        ],
                                        href="/dashboard",
                                        className="hero-btn"
                                    ),

                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-book-half me-2"),
                                            "Présentation du modèle"
                                        ],
                                        href="#model",
                                        outline=True,
                                        className="hero-btn-outline"
                                    )

                                ],

                                className="hero-buttons"

                            ),

                            html.Div(

                                [

                                    html.Div(

                                        [

                                            html.H2("12"),

                                            html.P("Mois étudiés")

                                        ],

                                        className="hero-stat"

                                    ),

                                    html.Div(

                                        [

                                            html.H2("3"),

                                            html.P("Variables de décision")

                                        ],

                                        className="hero-stat"

                                    ),

                                    html.Div(

                                        [

                                            html.H2("100%"),

                                            html.P("Interactif")

                                        ],

                                        className="hero-stat"

                                    )

                                ],

                                className="hero-stats"

                            )

                        ],

                        className="hero-content"

                    )

                ],

                fluid=True,

                className="hero-container"

            )

        ]

    )