from dash import html
import dash_bootstrap_components as dbc


def KPI(icon, title, value, color):

    return dbc.Col(

        dbc.Card(

            dbc.CardBody(

                [

                    html.Div(

                        [

                            html.Div(icon, className="kpi-icon"),

                            html.Div(
                                [
                                    html.H4(value, className="kpi-value"),
                                    html.P(title, className="kpi-title"),
                                ]
                            ),

                        ],

                        className="kpi-content",

                    )

                ]

            ),

            className=f"kpi-card border-{color}",

        ),

        lg=3,
        md=6,
        sm=12,

    )


def KPICards(metrics):

    return dbc.Row(

        [

            KPI(
                "💰",
                "Coût total (objectif)",
                f"{metrics['cout_total']:,.0f} FCFA",
                "success",
            ),

            KPI(
                "📦",
                "Achat + stockage",
                f"{metrics['cout_achat'] + metrics['cout_stockage']:,.0f} FCFA",
                "primary",
            ),

            KPI(
                "⚠️",
                "Rupture totale",
                f"{metrics['rupture_totale']:,.0f} t",
                "danger",
            ),

            KPI(
                "✅",
                "Taux de couverture",
                f"{metrics['taux_couverture']:.1f} %",
                "warning",
            ),

        ],

        className="g-4",

    )
