import dash
from dash import html

from components.hero import Hero
from components.cards import InfoCards
from components.workflow import Workflow
from components.footer import Footer

dash.register_page(
    __name__,
    path="/",
    name="Accueil"
)

layout = html.Div(

    [

        Hero(),

        InfoCards(),

        Workflow(),

        Footer(),

    ],

    className="page"

)