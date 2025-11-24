.. _calcul_turpe:

10.1. Electricity Grid Cost Calculation
============================================================

10.1.1. TURPE
--------------------------------------------

Le prix payé annuellement for l’utilisation des réseaux publics de distribution (RPD) est la somme des composantes suivantes :

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
     - Composante annuelle de l’énergie réactive
   * - **CI**
     - Annual injection component

The general TURPE formula is therefore :

.. code-block:: text

   TURPE = CG + CC + CS + CMDPS + CACS + CR + CER + CI

**Component Details :**

- **CG** : Fixed contract management fees.
- **CC** : Fees related to meter provision and reading.
- **CS** : Frais liés à la quantité d’énergie soutirée du réseau.
- **CMDPS** : Penalties for exceeding subscribed power.
- **CACS** : Fees for supplementary or backup supplies.
- **CR** : Fees for grouping multiple sites.
- **CER** : Frais liés à l’énergie réactive consommée.
- **CI** : Frais for l’injection d’énergie on le réseau.

.. admonition:: TURPE Calculation User Guide

   Here is an example of using the functions to calculate TURPE :

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

      # 2. Definition of unit tariffs (in €/kWh or by component)
      tarif = input_Tarif(
          c_euro_kWh_pointe=0,
          c_euro_kWh_HPB=0,
          c_euro_kWh_HCB=0,
          c_euro_kWh_HPH=0,
          c_euro_kWh_HCH=0,
          c_euro_kWh_TICFE=0.02250,
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

      # Calculationationation du TURPE
      turpe_calculator.calculate_turpe()

      # Affichage des résultats
      print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
      # print(f"Taxes et Contributions (€) : {turpe_calculator.euro_taxes_contrib}")

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
     - Power souscrite en période de pointe (selon domaine de tension)
   * - PS_HPH
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Power souscrite en heures pleines hiver
   * - PS_HCH
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Power souscrite en heures creuses hiver
   * - PS_HPB
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Power souscrite en heures pleines été
   * - PS_HCB
     - 0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV
     - Power souscrite en heures creuses été
   * - version_utilisation
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

   * - Version d'utilisation
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

   * - Version d'utilisation
     - Description
   * - CU
     - Contrat Unique (tarification standard BT > 36 kVA)
   * - LU
     - Long Use (specific pricing for extended use)
   * - CU_ac
     - Single Contract with collective self-production and/or backup supply
   * - LU_ac
     - Long Use with collective self-production and/or backup supply

***HTA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'utilisation
     - Description
   * - CU_pf
     - SC Contract (Single Contract) with fixed peak
   * - CU_pm
     - SC Contract (Single Contract) with mobile peak
   * - LU_pf
     - LU Contract (Long Use) with fixed peak
   * - LU_pm
     - LU Contract (Long Use) with mobile peak

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
   * - c_euro_kWh_TICFE
     -  ≥ 0 (€/kWh)
     - Tarif unitaire TCFE (taxe communale/foncière)
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
     - Tarif ENR (énergie renouvelable)
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
     - Dépassement de puissance souscrite en HPB
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
   :caption: Examples TURPE

   exemples/exemple_hta_cu_pf
   exemples/exemple_hta_cu_pm
   exemples/exemple_hta_lu_pf
   exemples/exemple_hta_lu_pm

   exemples/exemple_bt_m36_cu4
   exemples/exemple_bt_p36_cu
   


