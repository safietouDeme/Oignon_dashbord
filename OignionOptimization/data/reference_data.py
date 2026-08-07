"""
reference_data.py
Données mensuelles de référence utilisées par le dashboard et l'analyse
de sensibilité. À remplacer par vos vraies données si vous en disposez
(CSV, base de données, etc.).
"""

DEMANDE = [
    1400, 1450, 1500, 1550, 1600, 1650,
    1700, 1750, 1700, 1600, 1500, 1450,
]

PRODUCTION = [
    900, 1200, 1500, 1800, 2000, 2200,
    1800, 1500, 1300, 1100, 900, 800,
]

# Prix mensuels de l'oignon observés sur le marché (FCFA/t), utilisés
# comme poids w_t de la pénalité de rupture : plus l'oignon est cher
# un mois donné, plus une rupture ce mois-là est pénalisée. Le prix
# suit un profil saisonnier inverse de la production (prix bas
# pendant la récolte, prix haut en période de soudure).
PRIX_MARCHE_ONION = [
    260, 240, 210, 170, 140, 130,
    150, 190, 230, 260, 280, 270,
]
