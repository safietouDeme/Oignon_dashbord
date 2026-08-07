"""
sensitivity.py
Analyse de sensibilité : fait varier un paramètre du modèle sur une plage
de valeurs, relance le solveur pour chaque valeur, et renvoie l'évolution
des principaux indicateurs (coût total, rupture totale, taux de couverture...).
"""

import numpy as np

from models.solver import solve_model

# Paramètres du modèle pouvant être explorés, avec un libellé lisible
SENSITIVITY_PARAMS = {
    "budget": "Budget (B)",
    "m_max": "Plafond d'achat/import mensuel (M_max)",
    "s_max": "Capacité de stock (S_max)",
    "lam": "Coût unitaire achat/import (λ)",
    "mu": "Coût unitaire de stockage (μ)",
    "alpha": "Taux de perte du stock (α)",
    # w (poids de la pénalité de rupture) n'est pas un paramètre réglable :
    # c'est le prix mensuel du marché, transmis fixe via base_params["w"].
}

# Mapping nom "sidebar" -> nom d'argument de solve_model
_ARG_NAME = {
    "budget": "B",
    "m_max": "M_max",
    "s_max": "S_max",
    "lam": "lam",
    "mu": "mu",
    "alpha": "alpha",
}


def run_sensitivity(param_key, values, base_params, demande, production):
    """
    param_key : une des clés de SENSITIVITY_PARAMS
    values    : liste des valeurs à tester pour ce paramètre
    base_params : dict avec les valeurs courantes de tous les paramètres
                  (clés : budget, m_max, s_max, lam, mu, alpha, w)
                  w est le tableau (fixe) des 12 prix mensuels du marché.
                  ATTENTION : alpha doit déjà être en fraction (0-1), pas en %.
    demande, production : listes de 12 valeurs (données exogènes)

    Retourne une liste de dicts, un par valeur testée.
    """

    arg_name = _ARG_NAME[param_key]
    resultats = []

    for v in values:

        kwargs = dict(
            demande=demande,
            production=production,
            lam=base_params["lam"],
            mu=base_params["mu"],
            alpha=base_params["alpha"],
            w=base_params["w"],
            M_max=base_params["m_max"],
            S_max=base_params["s_max"],
            B=base_params["budget"],
        )
        kwargs[arg_name] = v

        try:
            r = solve_model(**kwargs)
        except Exception as exc:  # sécurité : ne jamais faire planter l'UI
            r = {"success": False, "message": str(exc)}

        metrics = r.get("metrics", {})

        resultats.append({
            "value": v,
            "success": r.get("success", False),
            "cout_total": metrics.get("cout_total"),
            "cout_achat": metrics.get("cout_achat"),
            "cout_stockage": metrics.get("cout_stockage"),
            "rupture_totale": metrics.get("rupture_totale"),
            "taux_couverture": metrics.get("taux_couverture"),
        })

    return resultats


def make_value_range(current_value, n_points=7, span_ratio=0.5):
    """
    Construit une plage de `n_points` valeurs autour de `current_value`,
    de current_value*(1-span_ratio) à current_value*(1+span_ratio).
    """
    current_value = float(current_value)
    low = max(current_value * (1 - span_ratio), 0.0)
    high = current_value * (1 + span_ratio)
    if high <= low:
        high = low + 1.0
    return list(np.linspace(low, high, n_points))
