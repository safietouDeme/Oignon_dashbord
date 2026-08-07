from dash import html
import dash_bootstrap_components as dbc


def Workflow():

    return html.Section(

        id="model",

        className="workflow-section",

        children=[

            dbc.Container(

                [

                    html.Div(

                        [

                            html.H2(
                                "Comment fonctionne le modèle d'optimisation ?",
                                className="section-title"
                            ),

                            html.P(
                                """
                                Le modèle combine les données de production, les besoins
                                du marché et les coûts logistiques afin de déterminer
                                une stratégie optimale de stockage et d'importation.
                                """,
                                className="section-description"
                            )

                        ],

                        className="section-header"

                    ),

                    html.Div(

                        [

                            # Ligne 1
                            html.Div(

                                [

                                    workflow_card(
                                        "bi bi-flower1",
                                        "Production locale",
                                        "Quantités produites chaque mois."
                                    ),

                                    workflow_card(
                                        "bi bi-cart",
                                        "Demande nationale",
                                        "Besoins mensuels du marché."
                                    ),

                                ],

                                className="workflow-row"

                            ),

                            html.Div(className="workflow-arrow-down"),

                            workflow_card_large(

                                "bi bi-box-seam",

                                "Disponibilité mensuelle",

                                """
                                Offre disponible = Production locale nette
                                + Stock disponible
                                + Importations
                                """

                            ),

                            html.Div(className="workflow-arrow-down"),

                            workflow_card_large(

                                "bi bi-sliders",

                                "Décision optimale",

                                """
                                Le modèle détermine :

                                • la quantité à stocker

                                • la quantité à importer

                                afin de minimiser les coûts.
                                """

                            ),

                            html.Div(className="workflow-arrow-down"),

                            workflow_card_large(

                                "bi bi-cpu",

                                "Optimisation Convexe",

                                """
                                Fonction objectif :

                                Minimiser

                                Coût de stockage
                                +
                                Coût d'importation

                                sous contraintes.
                                """

                            ),

                            html.Div(className="workflow-arrow-down"),

                            workflow_card_large(

                                "bi bi-graph-up-arrow",

                                "Résultat",

                                """
                                Satisfaction complète
                                de la demande nationale
                                tout en réduisant
                                les fluctuations
                                saisonnières des prix.
                                """

                            )

                        ],

                        className="workflow-grid"

                    )

                ]

            )

        ]

    )


def workflow_card(icon, title, text):

    return html.Div(

        [

            html.Div(

                html.I(className=icon),

                className="workflow-icon"

            ),

            html.H4(title),

            html.P(text)

        ],

        className="workflow-card"

    )


def workflow_card_large(icon, title, text):

    return html.Div(

        [

            html.Div(

                html.I(className=icon),

                className="workflow-icon"

            ),

            html.H3(title),

            html.P(text)

        ],

        className="workflow-card workflow-large"

    )