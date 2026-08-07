# Oignion Optimization — Corrections apportées

## 1. Bug bloquant : `cvxpy` manquant

Votre `venv` d'origine ne contenait **pas `cvxpy`**, alors que
`models/solver.py` en dépend directement. L'application plantait donc
dès le démarrage (`ModuleNotFoundError: No module named 'cvxpy'`).

**Correctif** : `cvxpy` a été ajouté à `requirements.txt`.

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py
```

(L'ancien dossier `venv/` n'est pas renvoyé dans ce zip : trop lourd et
spécifique à votre machine. Le recréer avec `requirements.txt` prend
2 minutes.)

## 2. Le solveur implémente maintenant le bon modèle

Le modèle final confirmé est :

```
min_{o_t, m_t, s_t}  f = Σ_{t=1}^{12} [ w_t·max(0, d_t - o_t) + λ·m_t + μ·s_t ]

C1 : s_t = (1-α)·s_(t-1) + p_t + m_t - o_t
C2 : 0 ≤ s_t ≤ S_max
C3 : 0 ≤ m_t ≤ M_max
C4 : Σ_t (λ·m_t + μ·s_t) ≤ B
C5 : o_t ≥ 0, m_t ≥ 0, s_t ≥ 0
```

Implémenté fidèlement dans `models/solver.py` avec CVXPY :

- **Variables de décision** : `o_t` (quantité mise à disposition /
  vendue), `m_t` (quantité achetée/importée, plafonnée par `M_max`),
  `s_t` (stock, plafonné par `S_max`).
- **Paramètres (données)** : `d_t` (demande), `p_t` (production locale
  exogène), `α` (taux de perte du stock), `λ`, `μ` (coûts), `w_t`
  (poids de la pénalité de rupture), `B` (budget).
- **Hypothèse non précisée par l'énoncé** : stock initial `s_0 = 0`
  (paramètre `s0` dans `solve_model()`, modifiable si besoin).
- La pénalité de rupture `max(0, d_t - o_t)` est modélisée via
  `cp.pos(...)`, qui est convexe donc compatible CVXPY.

## 3. Sidebar et dashboard mis à jour

- `components/sidebar.py` : champs alignés sur le modèle — λ, μ, w,
  α, `S_max`, `M_max`, `B`.
- `components/kpi_cards.py` : coût total, coût achat+stockage,
  rupture totale, taux de couverture.
- `callbacks/dashbord_callbacks.py` : appelle le nouveau solveur avec
  les données `DEMANDE` (d_t) et `PRODUCTION` (p_t, exogène) définies
  en tête de fichier — à remplacer par vos vraies données si vous en
  avez (CSV, base de données, etc.).
- Gestion propre d'un problème infaisable : message d'erreur affiché
  au lieu de faire planter l'app.

## 4. Démarrer l'application

```bash
pip install -r requirements.txt
python app.py
```

Puis ouvrez `http://127.0.0.1:8050`, allez sur **Dashboard**, réglez
les paramètres dans la sidebar, et cliquez sur **Lancer
l'optimisation**.

## 5. Page "Analyse" (nouveau)

La page `/analyse` était un simple placeholder ; elle est maintenant
fonctionnelle et contient :

1. **Interprétation automatique** des derniers résultats du Dashboard
   (coût, mois en rupture, utilisation du stock...).
2. **Analyse de sensibilité** (`models/sensitivity.py`) : fait varier un
   paramètre choisi (Budget, M_max, S_max, λ, μ, α, w) autour de sa
   valeur actuelle et trace l'effet sur le coût total et la rupture.
3. **Recommandations** générées par des règles simples (quelle
   contrainte est saturée : budget, capacité de stock, plafond
   d'achat...).

Pour que cela fonctionne, les derniers paramètres et résultats du
Dashboard sont maintenant sauvegardés dans un `dcc.Store` global
(`optimization-store`, défini dans `app.py` pour persister entre les
pages). **Il faut donc lancer une optimisation dans le Dashboard avant
que la page Analyse affiche quelque chose.**

## 6. Pour aller plus loin

- Remplacer `DEMANDE` / `PRODUCTION` (dans
  `callbacks/dashbord_callbacks.py`) par vos données réelles.
- Si `w_t`, `p_t` ou `α` doivent varier par mois plutôt qu'être
  constants, vous pouvez déjà passer des listes de 12 valeurs à
  `solve_model()` (la fonction `_to_monthly_array` accepte scalaire
  ou liste) — il suffit d'ajouter les champs correspondants dans la
  sidebar.
