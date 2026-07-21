Contexte et théorie IPMVP
=========================

Objectif
--------

The module ``IPMVP`` quantifie les energy savings according to the protocol IPMVP
**Option C** (mesure au niveau du site) : il ajuste un model de régression sur
une period de référence, then compare la baseline **ajustée** à la
consumption mesurée on la period de suivi.

.. math::

   \text{Économies} = E_{\text{baseline, ajustée}} - E_{\text{mesurée}}

Option C — model de baseline
-----------------------------

La baseline est un model de régression on les variables indépendantes
(DJU, production, occupation…) :

.. math::

   E = a + b_1 \cdot \text{DJU}_{\text{chaud}} + b_2 \cdot \text{DJU}_{\text{froid}} + \epsilon

Data d'input : ``y`` (consumption, ``Series`` temporelle en kWh), ``X``
(variables indépendantes, ``DataFrame``) et les dates de début/fin des periods
de référence et de suivi.

Critères de validation (ASHRAE Guideline 14)
--------------------------------------------

* **R² ≥ 0,75**
* **CV(RMSE) ≤ 15 %** (data mensuelles) / **≤ 30 %** (data horaires)

The module applique un seuil ``cv_remse`` unique de **0,20** et vérifie la
significativité des coefficients via la statistique de Student. Details et
formules in :doc:`modeles_mathematiques`.
