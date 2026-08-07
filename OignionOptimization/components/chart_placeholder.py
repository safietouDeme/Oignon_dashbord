from dash import html


def Chart(title):

    return html.Div(

        [

            html.H4(title),

            html.Div(

                "Graphique Plotly",

                className="chart-placeholder"

            )

        ],

        className="chart-card"

    )