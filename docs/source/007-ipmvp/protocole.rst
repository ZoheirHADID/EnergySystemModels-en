Contexte IPMVP
==============

The module implémente l'Option C de l'IPMVP (analysis of bâtiment/site entier with model statistique).

Option C : Principe
-------------------

Utilise les compteurs généraux et construit un model de régression for établir la baseline :

.. math::

   E = a + b_1 \cdot \text{DJU}_{\text{chaud}} + b_2 \cdot \text{DJU}_{\text{froid}} + \epsilon

Économies calculateds :

.. math::

   \text{Économies} = E_{\text{baseline,ajustée}} - E_{\text{mesurée}}

Critères de validation (ASHRAE Guideline 14)
---------------------------------------------

* **R² ≥ 0.75**
* **CV(RMSE) ≤ 15%** (data mensuelles)
* **CV(RMSE) ≤ 30%** (data horaires)
