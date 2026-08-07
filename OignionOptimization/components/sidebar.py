from dash import html, dcc
import dash_bootstrap_components as dbc


def _param_input(label, id_, value, min_=0, step=1):
    return html.Div(
        [
            html.Label(label, className="param-label"),
            dbc.Input(
                id=id_,
                type="number",
                value=value,
                min=min_,
                step=step,
            ),
        ],
        className="param-row",
    )


def Sidebar():

    return html.Div(

        [

            html.H3("Paramètres", className="sidebar-title"),

            html.Hr(),

            html.H6("Coûts", className="sidebar-section"),

            _param_input(
                "λ — coût unitaire d'achat/import (m_t) (FCFA/t)",
                "lambda-cost", 200, min_=0, step=1,
            ),

            _param_input(
                "μ — coût unitaire de stockage (s_t) (FCFA/t/mois)",
                "mu-cost", 150, min_=0, step=1,
            ),

            html.Small(
                "La pénalité de rupture w_t n'est pas un paramètre "
                "réglable : elle correspond directement au prix mensuel "
                "de l'oignon observé sur le marché (voir courbe « Prix "
                "marché » du Dashboard), et varie donc chaque mois.",
                className="text-muted d-block mb-2",
            ),

            html.Br(),

            html.H6("Stock", className="sidebar-section"),

            _param_input(
                "α — taux de perte du stock (%)",
                "alpha-taux", 5, min_=0, step=1,
            ),

            _param_input(
                "S_max — capacité maximale de stock (t)",
                "s-max", 1500, min_=0, step=50,
            ),

            html.Br(),

            html.H6("Achat / import", className="sidebar-section"),

            _param_input(
                "M_max — plafond mensuel d'achat/import (t)",
                "m-max", 800, min_=0, step=50,
            ),

            html.Br(),

            html.H6("Budget", className="sidebar-section"),

            _param_input(
                "B — budget total (achat + stockage) (FCFA)",
                "budget", 500000, min_=0, step=1000,
            ),

            html.Br(),
            html.Br(),

            # =====================================
            # Bouton
            # =====================================

            dbc.Button(
                [
                    html.I(className="bi bi-play-fill me-2"),
                    "Lancer l'optimisation",
                ],
                id="run-model",
                color="success",
                className="w-100",
                size="lg",
                n_clicks=0,
            ),

            html.Br(),
            html.Br(),

            # =====================================
            # Message
            # =====================================

            dbc.Alert(
                "En attente d'une optimisation...",
                id="optimization-status",
                color="secondary",
                is_open=True,
            ),

            html.Br(),

            # =====================================
            # Informations solveur
            # =====================================

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H5("Informations"),

                        html.Hr(),

                        html.P(
                            [
                                html.Strong("Solveur : "),
                                html.Span(id="solver-name", children="CLARABEL"),
                            ]
                        ),

                        html.P(
                            [
                                html.Strong("Statut : "),
                                html.Span(id="solver-status", children="-"),
                            ]
                        ),

                        html.P(
                            [
                                html.Strong("Temps : "),
                                html.Span(id="solve-time", children="-"),
                            ]
                        ),

                        html.P(
                            [
                                html.Strong("Fonction objectif : "),
                                html.Span(id="objective-value", children="-"),
                            ]
                        ),

                    ]

                )

            ),

        ],

        className="sidebar",

    )
