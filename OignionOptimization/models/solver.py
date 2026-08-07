"""
solver.py
Implémentation du modèle d'optimisation de l'accessibilité de l'oignon.

Modèle (version confirmée) :

    min_{o_t, m_t, s_t}  f = sum_{t=1}^{12} [ w_t * max(0, d_t - o_t) + lambda*m_t + mu*s_t ]

    C1 : s_t = (1-alpha)*s_(t-1) + p_t + m_t - o_t
    C2 : 0 <= s_t <= S_max
    C3 : 0 <= m_t <= M_max
    C4 : sum_t (lambda*m_t + mu*s_t) <= B
    C5 : o_t >= 0, m_t >= 0, s_t >= 0

Variables de décision : o_t (quantité mise à disposition / vendue ce mois),
m_t (quantité achetée/importée ce mois, plafonnée par M_max), s_t (stock).

Paramètres (données d'entrée) :
    d_t     : demande mensuelle (donnée)
    p_t     : production locale exogène mensuelle (donnée)
    alpha   : taux de perte/déperdition du stock d'un mois sur l'autre
    lambda  : coût unitaire de m_t (achat/import)
    mu      : coût unitaire de s_t (détention de stock)
    w_t     : poids de la pénalité de rupture (peut varier par mois)
    S_max, M_max, B : capacités et budget

Hypothèse (non précisée dans l'énoncé) : stock initial s_0 = 0.
Si ce n'est pas le cas chez vous, changez `s0` ci-dessous ou exposez-le
comme paramètre dans la sidebar.
"""

import time

import cvxpy as cp
import numpy as np
import pandas as pd

MOIS = [
    "Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
    "Juil", "Août", "Sep", "Oct", "Nov", "Déc",
]


def _to_monthly_array(value, T=12):
    """Accepte un scalaire (appliqué aux 12 mois) ou une liste de 12 valeurs."""
    if np.isscalar(value):
        return np.full(T, float(value))
    arr = np.array(value, dtype=float)
    if arr.size != T:
        raise ValueError(f"Le paramètre doit contenir {T} valeurs (reçu {arr.size}).")
    return arr


def solve_model(
    demande,
    production,
    lam,
    mu,
    alpha,
    w,
    M_max,
    S_max,
    B,
    s0=0.0,
):
    """
    Résout le programme d'optimisation mensuel (12 mois) et renvoie un
    dictionnaire de résultats prêt à être exploité par le dashboard.
    """

    T = 12

    d = _to_monthly_array(demande, T)
    p = _to_monthly_array(production, T)
    w_arr = _to_monthly_array(w, T)

    lam = float(lam)
    mu = float(mu)
    alpha = float(alpha)
    M_max = float(M_max)
    S_max = float(S_max)
    B = float(B)
    s0 = float(s0)

    # ==========================================
    # Variables de décision
    # ==========================================

    o = cp.Variable(T, nonneg=True)   # quantité mise à disposition / vendue
    m = cp.Variable(T, nonneg=True)   # quantité achetée / importée
    s = cp.Variable(T, nonneg=True)   # stock

    contraintes = []

    for t in range(T):
        s_prev = s[t - 1] if t > 0 else s0  # s_0 = 0 par défaut

        # C1
        contraintes.append(
            s[t] == (1 - alpha) * s_prev + p[t] + m[t] - o[t]
        )

    # C2, C3
    contraintes += [s >= 0, s <= S_max]
    contraintes += [m >= 0, m <= M_max]

    # C4 : budget total
    contraintes.append(cp.sum(lam * m + mu * s) <= B)

    # C5 : o_t, m_t, s_t >= 0 déjà imposé via nonneg=True.

    # ==========================================
    # Fonction objectif
    # ==========================================

    shortfall = cp.pos(d - o)  # max(0, d_t - o_t), convexe

    objectif = cp.Minimize(
        cp.sum(cp.multiply(w_arr, shortfall)) + lam * cp.sum(m) + mu * cp.sum(s)
    )

    problem = cp.Problem(objectif, contraintes)

    debut = time.time()
    try:
        problem.solve(solver=cp.CLARABEL)
    except Exception:
        problem.solve()
    fin = time.time()

    if s.value is None or problem.status in ("infeasible", "unbounded"):
        return {
            "success": False,
            "status": problem.status,
            "message": (
                "Le problème est infaisable avec ces paramètres. "
                "Essayez d'augmenter le budget B, M_max ou S_max, "
                "ou de réduire le taux de perte alpha."
            ),
            "solve_time": round(fin - debut, 3),
        }

    o_val = np.array(o.value)
    m_val = np.array(m.value)
    s_val = np.array(s.value)
    shortfall_val = np.maximum(d - o_val, 0.0)

    cout_achat = np.round(lam * m_val, 2)
    cout_stockage = np.round(mu * s_val, 2)
    cout_rupture = np.round(w_arr * shortfall_val, 2)

    df = pd.DataFrame({
        "Mois": MOIS,
        "Demande (d_t)": np.round(d, 2),
        "Production locale (p_t)": np.round(p, 2),
        "Achat / import (m_t)": np.round(m_val, 2),
        "Stock (s_t)": np.round(s_val, 2),
        "Disponibilité (o_t)": np.round(o_val, 2),
        "Rupture": np.round(shortfall_val, 2),
        "Coût achat/import": cout_achat,
        "Coût stockage": cout_stockage,
        "Coût rupture": cout_rupture,
    })

    cout_achat_total = float(cout_achat.sum())
    cout_stockage_total = float(cout_stockage.sum())
    cout_rupture_total = float(cout_rupture.sum())

    return {
        "success": True,
        "data": df.to_dict("records"),
        "status": problem.status,
        "objective": round(float(problem.value), 2),
        "solve_time": round(fin - debut, 3),
        "message": None,
        "metrics": {
            "cout_total": round(float(problem.value), 2),
            "cout_achat": round(cout_achat_total, 2),
            "cout_stockage": round(cout_stockage_total, 2),
            "cout_rupture": round(cout_rupture_total, 2),
            "stock_max": round(float(df["Stock (s_t)"].max()), 2),
            "achat_total": round(float(df["Achat / import (m_t)"].sum()), 2),
            "production_totale": round(float(df["Production locale (p_t)"].sum()), 2),
            "demande_totale": round(float(df["Demande (d_t)"].sum()), 2),
            "rupture_totale": round(float(df["Rupture"].sum()), 2),
            "taux_couverture": round(
                100 * (1 - df["Rupture"].sum() / df["Demande (d_t)"].sum()), 2
            ),
        },
    }
