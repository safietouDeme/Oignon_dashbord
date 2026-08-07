from dash import Input, Output, State, callback, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from models.sensitivity import run_sensitivity, make_value_range, SENSITIVITY_PARAMS
from data.reference_data import DEMANDE, PRODUCTION, PRIX_MARCHE_ONION


# ============================================================
# 1. Interprétation automatique + recommandations
# ============================================================

@callback(
    Output("interpretation-container", "children"),
    Input("optimization-store", "data"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)
def update_interpretation(store_data, pathname):

    # On ne met à jour que quand on est réellement sur la page Analyse,
    # pour éviter d'essayer d'écrire dans des composants qui n'existent
    # pas sur les autres pages.
    if pathname != "/analyse":
        raise PreventUpdate

    if not store_data:
        placeholder = dbc.Alert(
            "Lancez d'abord une optimisation dans le Dashboard pour "
            "voir apparaître cette analyse ici.",
            color="secondary",
        )
        return placeholder

    metrics = store_data["metrics"]
    params = store_data["params"]
    data = store_data["data"]

    # ---------------------------
    # Interprétation
    # ---------------------------

    mois_rupture = [row["Mois"] for row in data if row["Rupture"] > 0]

    lignes = [
        html.Li(
            f"Coût total optimal : {metrics['cout_total']:,.0f} FCFA "
            f"(achat/import : {metrics['cout_achat']:,.0f}, "
            f"stockage : {metrics['cout_stockage']:,.0f}, "
            f"rupture : {metrics['cout_rupture']:,.0f})."
        ),
        html.Li(
            f"Taux de couverture de la demande : "
            f"{metrics['taux_couverture']:.1f} %."
        ),
    ]

    if mois_rupture:
        lignes.append(
            html.Li(
                f"Rupture d'approvisionnement sur {len(mois_rupture)} mois : "
                f"{', '.join(mois_rupture)} "
                f"(total {metrics['rupture_totale']:.0f} t)."
            )
        )
    else:
        lignes.append(html.Li("Aucune rupture d'approvisionnement sur l'année."))

    lignes.append(
        html.Li(
            f"Stock maximal atteint : {metrics['stock_max']:.0f} t "
            f"(capacité S_max = {params['s_max']:.0f} t)."
        )
    )

    lignes.append(
        html.Li(f"Achat/import total sur l'année : {metrics['achat_total']:.0f} t.")
    )

    interpretation = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Ce que montrent ces résultats"),
                html.Ul(lignes),
            ]
        )
    )

    return interpretation


# ============================================================
# 2. Analyse de sensibilité
# ============================================================

# Valeurs par défaut si aucune optimisation n'a encore été lancée
_DEFAULT_BASE_PARAMS = {
    "lam": 15,
    "mu": 25,
    "alpha": 0.05,
    "w": list(PRIX_MARCHE_ONION),
    "m_max": 800,
    "s_max": 1500,
    "budget": 200000,
}

# Libellés utilisés dans les phrases de recommandation
_PARAM_NOMS = {
    "budget": "le budget total B",
    "m_max": "le plafond mensuel d'achat/import M_max",
    "s_max": "la capacité de stock S_max",
    "lam": "le coût unitaire d'achat/import λ",
    "mu": "le coût unitaire de stockage μ",
    "alpha": "le taux de perte du stock α",
}


def _fmt_valeur(param_key, v):
    if param_key == "alpha":
        return f"{v * 100:.1f} %"
    if param_key == "budget":
        return f"{v:,.0f} FCFA"
    if param_key in ("lam", "mu"):
        return f"{v:,.0f} FCFA/t"
    return f"{v:,.0f} t"


def _build_sensitivity_recommendation(param_key, results):
    """
    Construit une recommandation ciblée sur le paramètre choisi dans
    l'analyse de sensibilité, du type :
    "Pour éviter la rupture, le budget doit être au moins égal à X."
    """

    label = SENSITIVITY_PARAMS[param_key]
    nom = _PARAM_NOMS.get(param_key, label)

    valides = [r for r in results if r.get("success") and r.get("rupture_totale") is not None]

    if not valides:
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H5(f"Recommandation — {label}"),
                    html.P(
                        "Impossible de calculer une recommandation : "
                        "toutes les simulations testées ont échoué "
                        "(problème infaisable)."
                    ),
                ]
            )
        )

    valeurs = [r["value"] for r in valides]
    ruptures = [r["rupture_totale"] for r in valides]

    # Cas où le paramètre n'a quasiment aucun effet sur la rupture dans
    # la plage testée (contrainte non active) : éviter un message
    # directionnel trompeur, et l'indiquer clairement.
    etendue_rupture = max(ruptures) - min(ruptures)
    seuil_negligeable = max(1.0, 0.01 * max(ruptures + [1.0]))

    if etendue_rupture < seuil_negligeable:
        if max(ruptures) <= 1e-6:
            phrase = (
                f"Sur toute la plage testée, la demande est déjà "
                f"entièrement couverte quelle que soit la valeur de {nom} : "
                "ce paramètre n'est pas le facteur limitant actuellement."
            )
        else:
            phrase = (
                f"Faire varier {nom} sur la plage testée ne change quasiment "
                f"pas la rupture totale (environ {ruptures[0]:.0f} t dans "
                "tous les cas) : ce n'est probablement pas ce paramètre qui "
                "limite la couverture de la demande actuellement — "
                "essayez plutôt un autre paramètre (budget, capacité de "
                "stock, plafond d'achat/import)."
            )

        return dbc.Card(
            dbc.CardBody(
                [
                    html.H5(f"Recommandation — {label}"),
                    html.P(phrase),
                ]
            )
        )

    # Une augmentation du paramètre réduit-elle la rupture (cas de B,
    # M_max, S_max) ou l'augmente-t-elle (cas de lambda, mu, alpha) ?
    hausse_reduit_rupture = ruptures[0] >= ruptures[-1]

    seuil_zero = [i for i, r in enumerate(ruptures) if r <= 1e-6]

    def _interpole(i0, i1):
        v0, v1 = valeurs[i0], valeurs[i1]
        r0, r1 = ruptures[i0], ruptures[i1]
        if r1 == r0:
            return v1
        return v0 + (0 - r0) * (v1 - v0) / (r1 - r0)

    if hausse_reduit_rupture:
        if seuil_zero:
            idx = min(seuil_zero)
            seuil = (
                _interpole(idx - 1, idx)
                if idx > 0 and ruptures[idx - 1] > 0
                else valeurs[idx]
            )
            phrase = (
                f"Pour éviter la rupture, {nom} doit être au moins égal "
                f"à {_fmt_valeur(param_key, seuil)}."
            )
        else:
            phrase = (
                f"Même à la valeur la plus élevée testée "
                f"({_fmt_valeur(param_key, valeurs[-1])}), une rupture "
                f"subsiste ({ruptures[-1]:.0f} t) : il faut augmenter "
                f"{nom} au-delà de cette valeur pour l'éliminer."
            )
    else:
        if seuil_zero:
            idx = max(seuil_zero)
            seuil = (
                _interpole(idx, idx + 1)
                if idx < len(valeurs) - 1 and ruptures[idx + 1] > 0
                else valeurs[idx]
            )
            phrase = (
                f"Pour éviter la rupture, {nom} ne doit pas dépasser "
                f"{_fmt_valeur(param_key, seuil)}."
            )
        else:
            phrase = (
                f"Même à la valeur la plus basse testée "
                f"({_fmt_valeur(param_key, valeurs[0])}), une rupture "
                f"subsiste ({ruptures[0]:.0f} t) : il faut réduire {nom} "
                f"en dessous de cette valeur pour l'éliminer."
            )

    if all(r <= 1e-6 for r in ruptures):
        phrase += (
            " Sur toute la plage testée, la demande est déjà entièrement "
            "couverte : ce paramètre n'est actuellement pas contraignant."
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(f"Recommandation — {label}"),
                html.P(phrase),
            ]
        )
    )


@callback(
    Output("sensitivity-chart", "figure"),
    Output("recommendations-container", "children"),
    Input("run-sensitivity", "n_clicks"),
    State("sensitivity-param", "value"),
    State("sensitivity-points", "value"),
    State("optimization-store", "data"),
    prevent_initial_call=True,
)
def update_sensitivity(n_clicks, param_key, n_points, store_data):

    if store_data:
        p = store_data["params"]
        base_params = {
            "lam": p["lam"],
            "mu": p["mu"],
            "alpha": p["alpha"] / 100.0,  # stocké en % dans la sidebar
            "w": p.get("w", list(PRIX_MARCHE_ONION)),
            "m_max": p["m_max"],
            "s_max": p["s_max"],
            "budget": p["budget"],
        }
    else:
        base_params = dict(_DEFAULT_BASE_PARAMS)

    n_points = int(n_points) if n_points else 7
    current_value = base_params[param_key]
    values = make_value_range(current_value, n_points=n_points)

    results = run_sensitivity(param_key, values, base_params, DEMANDE, PRODUCTION)

    x = [r["value"] for r in results]
    if param_key == "alpha":
        x = [v * 100 for v in x]  # affichage en %

    rupture = [r["rupture_totale"] for r in results]

    label = SENSITIVITY_PARAMS[param_key]
    if param_key == "alpha":
        label += " (%)"

    # Le graphique n'affiche que la rupture totale (demandé par
    # l'utilisateur), plus besoin d'axe secondaire pour le coût total.
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=rupture,
            name="Rupture totale",
            mode="lines+markers",
            line={"color": "#c0392b"},
        )
    )

    fig.update_layout(
        title=f"Sensibilité de la rupture totale au paramètre : {label}",
        xaxis={"title": label},
        yaxis={"title": "Rupture totale (t)"},
        legend={"orientation": "h"},
    )

    recommendation = _build_sensitivity_recommendation(param_key, results)

    return fig, recommendation
