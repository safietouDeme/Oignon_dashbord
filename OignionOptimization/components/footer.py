from dash import html
import dash_bootstrap_components as dbc


def Footer():

    return html.Footer(

        className="footer",

        children=[

            dbc.Container(

                [

                    dbc.Row(

                        [

                            dbc.Col(

                                [

                                    html.H4(
                                        "OnionOpt",
                                        className="footer-title"
                                    ),

                                    html.P(

                                        """
                                        Plateforme interactive d'aide à la décision
                                        basée sur l'optimisation pour améliorer la
                                        disponibilité de l'oignon au Sénégal.
                                        """,

                                        className="footer-text"

                                    )

                                ],

                                lg=5

                            ),

                            dbc.Col(

                                [

                                    html.H5("Navigation"),

                                    html.Ul(

                                        [

                                            html.Li(html.A("Accueil",
                                                           href="/")),

                                            html.Li(html.A("Dashboard",
                                                           href="/dashboard")),

                                            html.Li(html.A("Analyse",
                                                           href="/analyse"))

                                        ],

                                        className="footer-links"

                                    )

                                ],

                                lg=3

                            ),

                            dbc.Col(

                                [

                                    html.H5("Projet"),

                                    html.P(

                                        "ENSAE Dakar",

                                        className="footer-text"

                                    ),

                                    html.P(

                                        "Optimisation convexe",

                                        className="footer-text"

                                    ),

                                    html.P(

                                        "Python • Dash • CVXPY",

                                        className="footer-text"

                                    )

                                ],

                                lg=4

                            )

                        ],

                        className="gy-4"

                    ),

                    html.Hr(className="footer-line"),

                    html.Div(

                        [

                            html.P(

                                "© 2026 OnionOpt • Tous droits réservés",

                                className="copyright"

                            )

                        ],

                        className="footer-bottom"

                    )

                ]

            )

        ]

    )