import plotly.graph_objects as go


GREEN = "#2E7D32"
LIGHT_GREEN = "#66BB6A"
RED = "#D32F2F"
ORANGE = "#F9A825"
BLUE = "#1976D2"
PURPLE = "#6A1B9A"


def update_layout(fig, title):

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            font=dict(size=22)
        ),

        template="plotly_white",

        paper_bgcolor="white",

        plot_bgcolor="white",

        hovermode="x unified",

        height=380,

        margin=dict(
            l=30,
            r=20,
            t=60,
            b=20
        ),

        legend=dict(
            orientation="h",
            y=1.10
        ),

        font=dict(
            family="Segoe UI"
        )

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False

    )

    fig.update_yaxes(

        gridcolor="#ECECEC"

    )

    return fig


def price_chart(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Mois"],

            y=df["Prix_initial"],

            mode="lines+markers",

            name="Avant optimisation",

            line=dict(color=RED, width=4),

            marker=dict(size=8)

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Mois"],

            y=df["Prix_optimal"],

            mode="lines+markers",

            name="Après optimisation",

            line=dict(color=GREEN, width=4),

            marker=dict(size=8)

        )

    )

    return update_layout(fig, "Évolution des prix")
def production_chart(df):

    fig = go.Figure()

    fig.add_bar(

        x=df["Mois"],

        y=df["Production"],

        name="Production",

        marker_color=GREEN

    )

    fig.add_bar(

        x=df["Mois"],

        y=df["Importation"],

        name="Importations",

        marker_color=ORANGE

    )

    fig.add_scatter(

        x=df["Mois"],

        y=df["Demande"],

        mode="lines+markers",

        name="Demande",

        line=dict(color=BLUE, width=4)

    )

    fig.update_layout(

        barmode="group"

    )

    return update_layout(fig, "Production - Importations - Demande")
def stock_chart(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Mois"],

            y=df["Stock"],

            fill="tozeroy",

            mode="lines+markers",

            line=dict(color=PURPLE, width=4),

            marker=dict(size=8),

            name="Stock"

        )

    )

    return update_layout(fig, "Évolution du stock")
def import_chart(df):

    fig = go.Figure()

    fig.add_bar(

        x=df["Mois"],

        y=df["Importation"],

        marker_color=ORANGE,

        name="Importation"

    )

    return update_layout(fig, "Importations optimales")