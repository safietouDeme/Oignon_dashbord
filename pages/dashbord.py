import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.sidebar import Sidebar

dash.register_page(
    __name__,
    path="/dashboard",
    name="Dashboard",
)

layout = dbc.Container(

    [

        html.H1(
            "Dashboard de l'optimisation",
            className="page-title",
        ),

        html.Br(),

        dbc.Row(

            [

                dbc.Col(
                    Sidebar(),
                    lg=3,
                ),

                dbc.Col(

                    [

                        # KPI
                        html.Div(
                            id="kpi-container"
                        ),

                        html.Br(),

                        dbc.Row(

                            [

                                dbc.Col(

                                    dcc.Graph(
                                        id="price-chart",
                                        config={
                                            "displayModeBar": False
                                        },
                                    ),

                                    lg=6,

                                ),

                                dbc.Col(

                                    dcc.Graph(
                                        id="production-chart",
                                        config={
                                            "displayModeBar": False
                                        },
                                    ),

                                    lg=6,

                                ),

                            ]

                        ),

                        html.Br(),

                        dbc.Row(

                            [

                                dbc.Col(

                                    dcc.Graph(
                                        id="stock-chart",
                                        config={
                                            "displayModeBar": False
                                        },
                                    ),

                                    lg=6,

                                ),

                                dbc.Col(

                                    dcc.Graph(
                                        id="import-chart",
                                        config={
                                            "displayModeBar": False
                                        },
                                    ),

                                    lg=6,

                                ),

                            ]

                        ),

                        html.Br(),

                        dcc.Graph(

                            id="cost-chart",

                            config={
                                "displayModeBar": False
                            },

                        ),

                        html.Br(),

                        html.Div(
                            id="table-container"
                        ),

                    ],

                    lg=9,

                ),

            ]

        ),

    ],

    fluid=True,

    className="dashboard-page",

)