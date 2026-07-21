Usage du module IPMVP
===========================

The module ``IPMVP`` construit un model de **baseline** (régression) et calculates
les energy savings according to l'**Option C** (mesure au niveau du site). La
fonction principale ``Mathematical_Models`` **returns a 9-item tuple** ;
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
       imposed_intercept=None,
       niveau_confiance=0.8,
   )
   (y_pred, df, conformite, table_incertitude,
    y_pred_report, df_report, conformite_report,
    table_incertitude_report, df_savings) = res

Parameters
----------

* **y** : consumption energy (``Series`` indexée by le temps) ;
* **X** : variable(s) explicative(s) (``DataFrame``, ex. ``[["DJU"]]``) ;
* **start/end_baseline_period** : period de référence (``datetime``) ;
* **start/end_reporting_period** : period de suivi (``datetime``) ;
* **degree** : degré du polynôme (1=linéaire, 2=quadratique, 3=cubique) ;
* **print_report** : si ``True``, génère un rapport ``.docx`` (via ``docx_report``) ;
* **seuil_z_scores** : seuil d'exclusion des points aberrants (**défaut 8**) ;
* **imposed_intercept** : impose la constante du model. ``None`` (défaut) =
  constante estimée librement ; ``0`` = régression by l'origine ; toute autre
  valeur = « talon » de consumption imposé. Les pentes sont alors ajustées sur
  le résidu :math:`y - b_0`, then l'ordonnée est fixée à :math:`b_0` ;
* **niveau_confiance** : niveau de confiance du calcul d'incertitude
  (**défaut 0,8**). Pilote la statistique de Student et donc la
  ``precision_absolue`` / ``precision_relative`` de ``table_incertitude``.

Valeurs de retour
-----------------

* ``y_pred`` : consumption prédite on la baseline (``DataFrame``) ;
* ``df`` : coefficients et indicateurs du model baseline, en colonne
  ``"ANTE-POST"`` (lignes ``coef_const``, ``coef_DJU``…, ``r2``, ``rmse``,
  ``cv_rmse``, ``ddof``, ``serr_*``, ``stat_t_*``) ;
* ``conformite`` : ``DataFrame`` des indicateurs (``r2``, ``cv_remse``,
  ``stat_t_*``) with la colonne ``conformité IPMVP`` (booléens) ;
* ``table_incertitude`` : incertitude baseline (``gamma``, ``niveau_confiance``,
  ``stat_t_normale``, ``Erreur type (rmse)``, ``precision_absolue +/-``,
  ``precision_relative``) ;
* ``y_pred_report``, ``df_report``, ``conformite_report``,
  ``table_incertitude_report`` : équivalents for la period de suivi
  (colonne ``"POST-ANTE"``) ;
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

The module utilise la method du **z-score** :

.. math::

   z_i = \frac{y_i - \bar{y}}{\sigma_y}

Les points with:math:`|z|` > ``seuil_z_scores`` (**défaut 8**) sont exclus.

Variables explicatives (X)
--------------------------

Le plus souvent, ``X`` contient les **degrés-jours unifiés (DJU)**. The module
calculates the DJU by la method COSTIC (voir :doc:`../008-meteo/degres_jours`) ;
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

Incertitude propagée des économies
----------------------------------

The function ``incertitude_savings`` propage l'erreur-type du model de
référence (``rmse``, ``ddof``, moyenne de consumption) on une durée de
contrat et une period de reporting, according to the protocol IPMVP :

.. code-block:: python

   from IPMVP.IPMVP import incertitude_savings

   inc = incertitude_savings(
       rmse, ddof, moyenne,
       gain_pct=0.18,            # économie mensuelle attendue
       duree_contrat_mois=60,
       duree_reporting_mois=12,
       niveau_confiance=0.8,     # défaut 0,8
   )

Formule (identique au calcul Excel M&V) :

.. math::

   t = t_{\text{Student}}\!\left(\tfrac{1+\text{conf}}{2},\; ddof\right)
   \qquad
   \text{prec}_{\text{abs}}(m) = t \cdot rmse \cdot \sqrt{m}

où :math:`m` est le nombre de mois. The function est **pure** (aucun effet de
bord) et retourne un ``dict`` contenant les clés ``contrat`` et ``reporting``
(chacune : ``mois``, ``economie_kwh``, ``precision_absolue_kwh``,
``precision_relative``). Voir :doc:`exemples` for une output realle.

Références
----------

* IPMVP Volume I (2012), Efficiency Valuation Organization (EVO) ;
* ASHRAE Guideline 14 : Measurement of Energy, Demand, and Water Savings ;
* ISO 50015 : Systèmes de management de l'energy — Mesure et vérification.
