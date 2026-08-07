import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# ============================
# Création de l'application
# ============================

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    ],
)

server = app.server

# ============================
# Barre de navigation
# ============================

navbar = dbc.Navbar(

    dbc.Container(

        [

            dbc.NavbarBrand(

                [

                    html.I(className="fas fa-seedling me-2"),

                    "Optimisation de l'accessibilité de l'oignon"

                ],

                className="fw-bold fs-4",

            ),

            dbc.Nav(

                [

                    dbc.NavLink(

                        [

                            html.I(className="fas fa-house me-2"),

                            "Accueil"

                        ],

                        href="/",

                        active="exact",

                    ),

                    dbc.NavLink(

                        [

                            html.I(className="fas fa-chart-column me-2"),

                            "Dashboard"

                        ],

                        href="/dashboard",

                        active="exact",

                    ),

                    dbc.NavLink(

                        [

                            html.I(className="fas fa-lightbulb me-2"),

                            "Analyse"

                        ],

                        href="/analyse",

                        active="exact",

                    ),

                ],

                pills=True,

            ),

        ],

        fluid=True,

    ),

    color="white",

    dark=False,

    className="navbar-custom shadow-sm",

)

# ============================
# Layout principal
# ============================

app.layout = html.Div(

    [

        navbar,

        # Permet de savoir sur quelle page on se trouve (utilisé par la
        # page Analyse pour se rafraîchir à chaque visite)
        dcc.Location(id="url", refresh=False),

        # Store global : conserve les derniers résultats d'optimisation
        # (persiste entre les pages, contrairement à un dcc.Store placé
        # dans le layout d'une seule page)
        dcc.Store(id="optimization-store", storage_type="memory"),

        html.Div(

            dash.page_container,

            className="page-content",

        ),

    ]

)

# ============================
# Import des callbacks
# (IMPORTANT : toujours après
# la création de app.layout)
# ============================

import callbacks.dashbord_callbacks
import callbacks.analyse_callbacks

# ============================
# Lancement de l'application
# ============================

if __name__ == "__main__":

    app.run(debug=True)