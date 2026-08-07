from dash import dash_table


def ResultsTable(df):

    return dash_table.DataTable(

        id="results-table",

        data=df.to_dict("records"),

        columns=[

            {
                "name": col,
                "id": col
            }

            for col in df.columns

        ],

        page_size=12,

        style_table={

            "overflowX": "auto"

        },

        style_cell={

            "textAlign": "center",

            "padding": "10px",

            "fontFamily": "Segoe UI"

        },

        style_header={

            "fontWeight": "bold",

            "backgroundColor": "#2E7D32",

            "color": "white"

        }

    )