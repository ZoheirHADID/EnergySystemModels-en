IPMVP — Example de Mesure et Vérification (Option C)
====================================================

La fonction ``Mathematical_Models`` ajuste un model de régression on une
**période de référence** (baseline) then quantifie les économies on une
**période de suivi** (reporting). Elle **returns a 9-item tuple**
(il n'existe pas d'objet ``model`` with des attributs ``.r2`` / ``.plot_*``).

Signature et valeurs de retour
------------------------------

.. code-block:: python

   y_pred, df, conformite, table_incertitude, \
   y_pred_report, df_report, conformite_report, table_incertitude_report, \
   df_savings = Mathematical_Models(
       y, X,
       start_baseline_period, end_baseline_period,
       start_reporting_period, end_reporting_period,
       print_report=False,      # True -> génère un rapport .docx (via docx_report)
       seuil_z_scores=8,        # seuil d'exclusion des points aberrants (défaut 8)
       degree=1,                # degré du modèle polynomial
       site="****",
   )

Les 9 éléments : ``y_pred`` (prédiction baseline), ``df`` (data + prédiction),
``conformite`` (indicateurs IPMVP + verdict), ``table_incertitude`` (incertitude
baseline), les 4 équivalents for la période de reporting, et ``df_savings``
(économies ANTE-POST / POST-ANTE).

Example complet
---------------

.. code-block:: python

   import pandas as pd
   from datetime import datetime
   from IPMVP.IPMVP import Mathematical_Models

   # Données mensuelles livrées avec le paquet : consommation + DJU
   df = pd.read_excel("src/IPMVP/IPMVP_input.xlsx")
   df["Mois"] = pd.to_datetime(df["Mois"])
   df = df.set_index("Mois")

   X = df[["DJU"]]                              # variable(s) explicative(s)
   y = df["Consommation (kWh) - Relevé"]        # consommation mesurée

   res = Mathematical_Models(
       y, X,
       datetime(2016, 9, 1), datetime(2021, 5, 1),    # baseline
       datetime(2021, 10, 1), datetime(2022, 10, 1),  # reporting
       degree=1, seuil_z_scores=3, site="exemple_site",
   )
   y_pred, df_bl, conformite, table_inc, *_rep, df_savings = res

   print(conformite)
   print(df_savings)

Output réelle
-------------

**Conformité du model baseline** (``conformite``) :

.. code-block:: text

                  valeur  conformité IPMVP
   r2               0.81              True
   cv_remse         0.53             False
   stat_t_const    -4.80             False
   stat_t_DJU      13.60              True

Le model explique 81 % de la variance (``r2`` = 0,81) et la variable DJU est
significative (``stat_t_DJU``), mais le ``cv_remse`` (0,53) dépasse le seuil
IPMVP — indiquant une dispersion résiduelle à améliorer (variables explicatives
supplémentaires, granularité, etc.).

**Économies** (``df_savings``) :

.. code-block:: text

                              ANTE-POST    POST-ANTE
   Relevé de consommation    3914387.73  19655625.79
   Prédiction                4624795.55  16156026.80
   pourcentage d'économie>0       18.15        17.80

L'approche **ANTE-POST** (référence ajustée − mesuré) donne **18,15 %**
d'économie on la période de suivi.

**Incertitude** (``table_incertitude``) : ``precision_relative`` ≈ 0,69,
``Erreur type (rmse)`` ≈ 236 260, for un niveau de confiance de 80 %.

.. note::
   Pour un rapport détaillé (graphiques d'ajustement, résidus, économies
   cumulées), appeler with ``print_report=True`` : un document **.docx** est
   généré via ``docx_report`` (dépend de ``python-docx``). Il n'y a pas de
   methods ``plot_*`` on un objet model.
