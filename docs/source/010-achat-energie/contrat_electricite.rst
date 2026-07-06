.. _calcul_turpe:

10.1. Electricity Grid Cost Calculation
============================================================

10.1.1. TURPE
--------------------------------------------

Le prix payé annuellement for l’usage des réseaux publics de distribution (RPD) est la somme des composantes suivantes :

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Abréviation
     - Description
   * - **CG**
     - Annual management component
   * - **CC**
     - Annual metering component
   * - **CS**
     - Annual withdrawal component
   * - **CMDPS**
     - Monthly component for exceeding subscribed power
   * - **CACS**
     - Annual component for supplementary and backup supplies
   * - **CR**
     - Grouping component
   * - **CER**
     - Composante annuelle de l’energy réactive
   * - **CI**
     - Annual injection component

The general TURPE formula is therefore :

.. code-block:: text

   TURPE = CG + CC + CS + CMDPS + CACS + CR + CER + CI

**Component Details :**

- **CG** : Fixed contract management fees.
- **CC** : Fees related to meter provision and reading.
- **CS** : Frais liés à la quantité d’energy soutirée du réseau.
- **CMDPS** : Penalties for exceeding subscribed power.
- **CACS** : Fees for supplementary or backup supplies.
- **CR** : Fees for grouping multiple sites.
- **CER** : Frais liés à l’energy réactive consommée.
- **CI** : Frais for l’injection d’energy on le réseau.

.. admonition:: Guide d'utilisation du calcul TURPE

   Voici un example d'usage des fonctions to calculate le TURPE :

   .. code-block:: python

      from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

      # 1. Définition du contrat (caractéristiques de raccordement)
      contrat = input_Contrat(
          domaine_tension="BT < 36 kVA",
          PS_pointe=10,
          PS_HPH=10,
          PS_HCH=10,
          PS_HPB=10,
          PS_HCB=10,
          version_utilisation="CU4",
          pourcentage_ENR=0
      )

      # 2. Définition des tarifs unitaires (en €/kWh ou selon composante)
      tarif = input_Tarif(
          c_euro_kWh_pointe=0,
          c_euro_kWh_HPB=0,
          c_euro_kWh_HCB=0,
          c_euro_kWh_HPH=0,
          c_euro_kWh_HCH=0,
          c_euro_kwh_CSPE_TICFE=0.02250,
          c_euro_kWh_certif_capacite_pointe=0.0,
          c_euro_kWh_certif_capacite_HPH=0.0,
          c_euro_kWh_certif_capacite_HCH=0.0,
          c_euro_kWh_certif_capacite_HPB=0.0,
          c_euro_kWh_certif_capacite_HCB=0.0,
          c_euro_kWh_ENR=0,
          c_euro_kWh_ARENH=0
      )

      # 3. Création de la facture (consommations et dépassements)
      facture = input_Facture(
          start="2025-02-01",
          end="2025-02-28",
          heures_depassement=0,
          depassement_PS_HPB=10,
          kWh_pointe=0,
          kWh_HPH=10,
          kWh_HCH=10,
          kWh_HPB=10,
          kWh_HCB=10
      )

      # Création du calculateur TURPE
      turpe_calculator = TurpeCalculator(contrat, tarif, facture)

      # Calcul du TURPE
      turpe_calculator.calculate_turpe()

      # Affichage des résultats
      print(turpe_calculator.df_totaux)

   Output réelle (``df_totaux``, for ce contrat BT < 36 kVA / CU4 et 40 kWh
   consommés en février 2025) :

   .. code-block:: text

                            Ligne  Résultat Annuel
                       Fourniture             0.00
             Acheminement (TURPE)            12.27
           Taxes et contributions             2.43
                     = Total HTVA            15.58
                          TVA 20%             3.12
                      = Total TTC            18.70
              Coût HTVA (EUR/MWh)           389.50
      Coût distribution (EUR/MWh)           306.75
             Coût taxes (EUR/MWh)            60.75

   The parameters to fill in `input_Contrat`, `input_Tarif` and `input_Facture` are detailed in the tables below. Adapt them according to your consumption profile, your contract and the current tariffs.

**Table of Input Parameters for TURPE Calculation**

***Declare a Contract***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - domaine_tension
     - "BT < 36 kVA", "BT > 36 kVA", "HTA"
     - Connection voltage domain
   * - PS_pointe
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Subscribed power during peak period (according to voltage domain)
   * - PS_HPH
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Subscribed power during winter peak hours
   * - PS_HCH
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Subscribed power during winter off-peak hours
   * - PS_HPB
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Subscribed power during summer peak hours
   * - PS_HCB
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Subscribed power during summer off-peak hours
   * - version_usage
     - Voir tableau dédié ci-dessous
     - Tariff option according to voltage domain
   * - pourcentage_ENR
     - 0 à 100 (%)
     - Percentage of renewable energy injected or self-consumed

**Usage Versions by Voltage Domain**

***BT < 36 kVA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'usage
     - Description
   * - CU4
     - Contrat Unique 4 périodes (pointe, HPH, HCH, HPB, HCB)
   * - CU
     - Contrat Unique (tarification standard BT < 36 kVA)
   * - MU4
     - Multi-usage 4 périodes
   * - MU_DT
     - Multi-usage double tarif
   * - LU
     - Longue Usage
   * - CU4_ac
     - Single Contract 4 periods with collective self-production and/or backup supply
   * - MU_ac
     - Multi-use with collective self-production and/or backup supply

***BT > 36 kVA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'usage
     - Description
   * - CU
     - Contrat Unique (tarification standard BT > 36 kVA)
   * - LU
     - Longue Usage (tarification spécifique for usages prolongés)
   * - CU_ac
     - Single Contract with collective self-production and/or backup supply
   * - LU_ac
     - Longue Usage with autoproduction collective et/ou alimentation de secours

***HTA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'usage
     - Description
   * - CU_pf
     - SC Contract (Single Contract) with fixed peak
   * - CU_pm
     - SC Contract (Single Contract) with mobile peak
   * - LU_pf
     - Contrat LU (Longue Usage) with fixed peak
   * - LU_pm
     - Contrat LU (Longue Usage) with mobile peak

***Déclarer vos tarifs***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - c_euro_kWh_pointe
     -  ≥ 0 (€/kWh)
     - Unit price peak period
   * - c_euro_kWh_HPB
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures pleines été
   * - c_euro_kWh_HCB
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures creuses été
   * - c_euro_kWh_HPH
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures pleines hiver
   * - c_euro_kWh_HCH
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures creuses hiver
   * - c_euro_kwh_CSPE_TICFE
     -  ≥ 0 (€/kWh)
     - Accise on l'électricité (ex-CSPE / TICFE)
   * - c_euro_kWh_certif_capacite_pointe
     -  ≥ 0 (€/kWh)
     - Peak period capacity certificate
   * - c_euro_kWh_certif_capacite_HPH
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures pleines hiver
   * - c_euro_kWh_certif_capacite_HCH
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures creuses hiver
   * - c_euro_kWh_certif_capacite_HPB
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures pleines été
   * - c_euro_kWh_certif_capacite_HCB
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures creuses été
   * - c_euro_kWh_ENR
     -  ≥ 0 (€/kWh)
     - Tarif ENR (energy renouvelable)
   * - c_euro_kWh_ARENH
     -  ≥ 0 (€/kWh)
     - Tarif ARENH (Accès régulé à l'électricité nucléaire historique)

***Declare an Invoice***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - start, end
     - Date (YYYY-MM-DD)
     - Start and end of billing period
   * - heures_depassement
     - Entier ≥ 0
     - Number of hours exceeding subscribed power
   * - depassement_PS_HPB
     -  ≥ 0 (kW ou kVA)
     - Dépassement de power souscrite en HPB
   * - kWh_pointe
     -  ≥ 0
     - Consommation en période de pointe (kWh)
   * - kWh_HPH
     -  ≥ 0
     - Consommation en heures pleines hiver (kWh)
   * - kWh_HCH
     -  ≥ 0
     - Consommation en heures creuses hiver (kWh)
   * - kWh_HPB
     -  ≥ 0
     - Consommation en heures pleines été (kWh)
   * - kWh_HCB
     -  ≥ 0
     - Consommation en heures creuses été (kWh)

.. toctree::
   :maxdepth: 1
   :caption: TURPE Examples

   exemples/exemple_hta_cu_pf
   exemples/exemple_hta_cu_pm
   exemples/exemple_hta_lu_pf
   exemples/exemple_hta_lu_pm

   exemples/exemple_bt_m36_cu4
   exemples/exemple_bt_p36_cu
   


