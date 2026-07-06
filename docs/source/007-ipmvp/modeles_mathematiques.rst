Usage du module IPMVP
===========================

Le module ``IPMVP`` construit un model de **baseline** (régression) et calcule
les économies d'energy according to l'**Option C** (mesure au niveau du site). La
fonction principale ``Mathematical_Models`` **retourne un tuple de 9 éléments** ;
il n'existe pas d'objet ``model`` with des attributs ``.r2`` ou des methods
``plot_*`` (voir :doc:`exemples` for un example exécutable complet).

Signature
---------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models

   res = Mathematical_Models(
       y, X,
       start_baseline_period, end_baseline_period,
       start_reporting_period, end_reporting_period,
       print_report=False,
       seuil_z_scores=8,
       degree=1,
       site="****",
   )
   (y_pred, df, conformite, table_incertitude,
    y_pred_report, df_report, conformite_report,
    table_incertitude_report, df_savings) = res

Paramètres
----------

* **y** : consommation energy (``Series`` indexée by le temps) ;
* **X** : variable(s) explicative(s) (``DataFrame``, ex. ``[["DJU"]]``) ;
* **start/end_baseline_period** : période de référence (``datetime``) ;
* **start/end_reporting_period** : période de suivi (``datetime``) ;
* **degree** : degré du polynôme (1=linéaire, 2=quadratique, 3=cubique) ;
* **print_report** : si ``True``, génère un rapport ``.docx`` (via ``docx_report``) ;
* **seuil_z_scores** : seuil d'exclusion des points aberrants (**défaut 8**).

Valeurs de retour
-----------------

* ``y_pred`` : consommation prédite on la baseline ;
* ``df`` : data baseline + colonne de prédiction (colonne ``"ANTE-POST"``) ;
* ``conformite`` : ``DataFrame`` des indicateurs (``r2``, ``cv_remse``,
  ``stat_t_*``) with la colonne ``conformité IPMVP`` (booléens) ;
* ``table_incertitude`` : incertitude baseline (``precision_relative``, ``rmse``…) ;
* ``y_pred_report``, ``df_report``, ``conformite_report``,
  ``table_incertitude_report`` : équivalents for la période de suivi ;
* ``df_savings`` : économies **ANTE-POST** / **POST-ANTE** (relevé, prédiction,
  pourcentage d'économie).

Critères de validation (ASHRAE Guideline 14)
--------------------------------------------

**R² (coefficient de détermination)** :

.. math::

   R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y}_i)^2}
   \qquad\text{seuil usuel } R^2 \ge 0.75

**CV(RMSE)** — coefficient de variation du RMSE :

.. math::

   \text{CV(RMSE)} = \frac{1}{\bar{y}} \sqrt{\frac{\sum (y_i - \hat{y}_i)^2}{n - p}}

Seuils de référence ASHRAE : ≤ 15 % (mensuel) / ≤ 30 % (horaire).

.. note::
   Ces indicateurs sont fournis in le ``DataFrame`` ``conformite`` retourné,
   avec le verdict ``conformité IPMVP``. Le seuil ``cv_remse`` **codé in le
   module** est unique (0,2 = 20 %), without distinction mensuel/horaire.

Détection des valeurs aberrantes
--------------------------------

Le module utilise la method du **z-score** :

.. math::

   z_i = \frac{y_i - \bar{y}}{\sigma_y}

Les points with :math:`|z|` > ``seuil_z_scores`` (**défaut 8**) sont exclus.

Variables explicatives (X)
--------------------------

Le plus souvent, ``X`` contient les **degrés-jours unifiés (DJU)**. Le module
calcule les DJU by la method COSTIC (voir :doc:`../008-meteo/degres_jours`) ;
on peut aussi ajouter d'autres variables according to le contexte :

.. code-block:: python

   # Bâtiment thermiquement sensible
   X = df[["DJU"]]
   # Site industriel : ajouter des inducteurs de production
   X = df[["DJU", "tonnes_produites", "heures_fonctionnement"]]

Granularité temporelle
----------------------

``Mathematical_Models`` s'applique à des data horaires, journalières ou
mensuelles. Les data **mensuelles** offrent le meilleur compromis
précision/simplicité for la plupart des projets M&V.

.. code-block:: python

   df_monthly = df.resample("MS").sum()   # agrégation mensuelle
   X = df_monthly[["DJU"]]
   y = df_monthly["consommation_kWh"]

Références
----------

* IPMVP Volume I (2012), Efficiency Valuation Organization (EVO) ;
* ASHRAE Guideline 14 : Measurement of Energy, Demand, and Water Savings ;
* ISO 50015 : Systèmes de management de l'energy — Mesure et vérification.
