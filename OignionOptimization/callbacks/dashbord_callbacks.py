from dash import Input, Output, State, callback, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from models.optimisation import optimize
from components.kpi_cards import KPICards
from components.results_table import ResultsTable
from data.reference_data import DEMANDE, PRODUCTION, PRIX_MARCHE_ONION


def _empty_figure(message):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        showarrow=False,
        font={"size": 16},
    )
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
    )
    return fig


@callback(
    Output("kpi-container", "children"),
    Output("price-chart", "figure"),
    Output("production-chart", "figure"),
    Output("stock-chart", "figure"),
    Output("import-chart", "figure"),
    Output("cost-chart", "figure"),
    Output("table-container", "children"),
    Output("optimization-status", "children"),
    Output("optimization-status", "color"),
    Output("solver-status", "children"),
    Output("solve-time", "children"),
    Output("objective-value", "children"),
    Output("optimization-store", "data"),

    Input("run-model", "n_clicks"),

    State("lambda-cost", "value"),
    State("mu-cost", "value"),
    State("alpha-taux", "value"),
    State("m-max", "value"),
    State("s-max", "value"),
    State("budget", "value"),

    prevent_initial_call=True,
)
def run_optimization(
    n_clicks,
    lam,
    mu,
    alpha,
    m_max,
    s_max,
    budget,
):

    # ===============================
    # Résolution du modèle
    # ===============================

    # w_t = prix_marche_t : la pénalité de rupture n'est pas un paramètre
    # réglable, elle correspond directement au prix mensuel de l'oignon
    # observé sur le marché, et varie donc chaque mois.
    w_mensuel = list(PRIX_MARCHE_ONION)

    results = optimize(
        demande=DEMANDE,
        production=PRODUCTION,
        lam=lam,
        mu=mu,
        alpha=alpha / 100.0,
        w=w_mensuel,
        M_max=m_max,
        S_max=s_max,
        B=budget,
    )

    # ===============================
    # Cas d'échec (infaisable, etc.)
    # ===============================

    if not results.get("success", False):
        empty = _empty_figure("Aucun résultat — voir le message ci-contre")
        return (
            html.Div(),
            empty, empty, empty, empty, empty,
            html.Div(),
            results.get("message", "Optimisation impossible avec ces paramètres."),
            "danger",
            results.get("status", "-"),
            f'{results.get("solve_time", "-")} s',
            "-",
            None,  # optimization-store : pas de résultats exploitables
        )

    df = pd.DataFrame(results["data"])

    # ===============================
    # KPI
    # ===============================

    kpis = KPICards(results["metrics"])

    # ===============================
    # Graphique : rupture (demande vs disponibilité)
    # ===============================

    fig_price = px.line(
        df,
        x="Mois",
        y=["Demande (d_t)", "Disponibilité (o_t)"],
        markers=True,
        title="Demande vs Disponibilité (rupture éventuelle)",
    )

    fig_price.add_trace(
        go.Scatter(
            x=df["Mois"],
            y=w_mensuel,
            name="Prix marché (w_t)",
            mode="lines+markers",
            line={"dash": "dot", "color": "#c0392b"},
            yaxis="y2",
        )
    )

    fig_price.update_layout(
        yaxis2={
            "title": "Prix marché w_t (FCFA/t)",
            "overlaying": "y",
            "side": "right",
        },
    )

    # ===============================
    # Production / Achat-import / Demande
    # ===============================

    fig_prod = px.bar(
        df,
        x="Mois",
        y=["Production locale (p_t)", "Achat / import (m_t)", "Demande (d_t)"],
        barmode="group",
        title="Production locale vs Achat/import vs Demande",
    )

    # ===============================
    # Stock
    # ===============================

    fig_stock = px.area(
        df,
        x="Mois",
        y="Stock (s_t)",
        title="Évolution du stock (s_t)",
    )

    # ===============================
    # Achat / import
    # ===============================

    fig_import = px.bar(
        df,
        x="Mois",
        y="Achat / import (m_t)",
        title="Achats / importations optimales (m_t)",
    )

    # ===============================
    # Coûts
    # ===============================

    fig_cost = px.bar(
        df,
        x="Mois",
        y=["Coût achat/import", "Coût stockage", "Coût rupture"],
        barmode="stack",
        title="Répartition des coûts",
    )

    # ===============================
    # Tableau
    # ===============================

    table = ResultsTable(df)

    # ===============================
    # Store (pour la page Analyse)
    # ===============================

    store_data = {
        "params": {
            "lam": lam,
            "mu": mu,
            "alpha": alpha,
            "w": w_mensuel,
            "m_max": m_max,
            "s_max": s_max,
            "budget": budget,
        },
        "metrics": results["metrics"],
        "data": results["data"],
        "objective": results["objective"],
    }

    # ===============================
    # Retour
    # ===============================

    return (
        kpis,
        fig_price,
        fig_prod,
        fig_stock,
        fig_import,
        fig_cost,
        table,
        "Optimisation terminée avec succès",
        "success",
        results["status"],
        f'{results["solve_time"]} s',
        f'{results["objective"]:,.0f} FCFA',
        store_data,
    )
