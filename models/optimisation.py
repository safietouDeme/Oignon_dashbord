"""
optimisation.py
Interface entre Dash et le solveur (models/solver.py).
"""

from models.solver import solve_model


def optimize(
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
    Lance l'optimisation et retourne les résultats bruts du solveur.
    """

    return solve_model(
        demande=demande,
        production=production,
        lam=lam,
        mu=mu,
        alpha=alpha,
        w=w,
        M_max=M_max,
        S_max=S_max,
        B=B,
        s0=s0,
    )
