.. _nomenclature:

Nomenclature générale
=====================

This page groups all symbols, parameters and variables used in the EnergySystemModels library.

Transfer thermique (HeatTransfer)
----------------------------------

Géométrie et dimensions
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - L
     - Length du corps
     - m
     - ParallelepipedicBody
   * - W
     - Largeur du corps
     - m
     - ParallelepipedicBody
   * - H
     - Height du corps
     - m
     - ParallelepipedicBody
   * - A
     - Surface d'échange
     - m²
     - CompositeWall, ParallelepipedicBody
   * - thickness
     - Épaisseur d'une couche
     - m
     - CompositeWall
   * - d_hyd
     - Diameter hydraulique
     - m
     - StraightPipe
   * - DN
     - Diameter nominal
     - mm
     - PipeInsulationAnalysis
   * - L_tube
     - Length du tuyau
     - m
     - PipeInsulationAnalysis

Temperatures
~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - T
     - Temperature générale
     - °C
     - Tous modules
   * - Ta
     - Temperature ambiante
     - °C
     - ParallelepipedicBody
   * - Tamb
     - Temperature ambiante
     - °C
     - PipeInsulationAnalysis
   * - Ti
     - Temperature intérieure
     - °C
     - CompositeWall
   * - Ti_degC
     - Temperature d'input
     - °C
     - Source, StraightPipe
   * - Te
     - Temperature extérieure
     - °C
     - CompositeWall
   * - Tp
     - Temperature de paroi
     - °C
     - ParallelepipedicBody
   * - T_fluid
     - Temperature of the fluid
     - °C
     - PipeInsulationAnalysis

Coefficients de transfert
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - he
     - Coefficient de convection externe
     - W/m²·K
     - CompositeWall
   * - hi
     - Coefficient de convection interne
     - W/m²·K
     - CompositeWall
   * - conductivity
     - Conductivité thermique
     - W/m·K
     - CompositeWall

Properties de surface
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - emissivity
     - Émissivité of the surface
     - -
     - PipeInsulationAnalysis
   * - isolated
     - Indicateur d'isolation (face)
     - True/False
     - ParallelepipedicBody
   * - faces_config
     - Configuration des faces
     - dict
     - ParallelepipedicBody

Matériaux et isolation
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 30

   * - Paramètre
     - Description
     - Valeurs possibles
   * - material (tuyaux)
     - Matériau du tuyau
     - 'steel', 'copper', 'PVC', 'PE', 'stainless_steel', 'cast_iron'
   * - material (murs)
     - Matériau de construction
     - 'Béton', 'Brique', 'Bois', 'Acier', 'Aluminium', 'Verre', etc.
   * - insulation
     - Type d'isolant
     - 'laine_de_verre', 'laine_de_roche', 'polystyrène_expansé', 'polyuréthane', etc.
   * - insulation_thickness
     - Épaisseur d'isolant
     - m

Thermodynamic Cycles
-----------------------

Fluids et frigorigènes
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - fluid
     - Nom of the fluid/frigorigène
     - String
     - Source, StraightPipe
   * - Ti_degC
     - Temperature d'input
     - °C
     - Source
   * - Pi_bar
     - Pressure d'input
     - bar
     - Source, StraightPipe

Fluids disponibles (CoolProp)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fluids naturels** : Water, Air, Nitrogen, Oxygen, CarbonDioxide, Hydrogen, Methane, Ethane, Propane, Butane, IsoButane, Pentane, IsoPentane, Hexane, Heptane, Octane, Nonane, Decane

**Frigorigènes HFC** : R134a, R125, R143a, R152a, R32, R245fa, R236fa, R227ea, R365mfc, R404A, R407C, R410A, R507A

**Frigorigènes naturels** : R717 (Ammonia), R744 (CO2), R290 (Propane), R600a (Isobutane), R1270 (Propylene)

**Other** : Benzene, Toluene, Acetone, Ethanol, Methanol, D4, D5, D6, MD2M, MD3M, MD4M, MDM, MM, Neopentane, Cyclohexane, p-Xylene, m-Xylene, o-Xylene

Flow rates
~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - F
     - Flow rate massique
     - kg/s
     - Source
   * - F_kgs
     - Flow rate massique
     - kg/s
     - Source, StraightPipe
   * - F_kgh
     - Flow rate massique
     - kg/h
     - Source, StraightPipe
   * - F_m3s
     - Flow rate volumique
     - m³/s
     - Source, StraightPipe
   * - F_m3h
     - Flow rate volumique
     - m³/h
     - Source, StraightPipe, PipeInsulationAnalysis
   * - F_Sm3s
     - Flow rate volumique standard (0°C, 1 atm)
     - Sm³/s
     - Source, StraightPipe
   * - F_Sm3h
     - Flow rate volumique standard (0°C, 1 atm)
     - Sm³/h
     - Source, StraightPipe

Properties thermodynamiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - h
     - Enthalpy spécifique
     - J/kg (kJ/kg)
     - Source, FreshAir
   * - H_v
     - Enthalpy de la vapeur
     - J/kg
     - Source
   * - H_l
     - Enthalpy du liquide
     - J/kg
     - Source
   * - rho (ρ)
     - Density
     - kg/m³
     - Source, StraightPipe
   * - mu (η)
     - Viscosity dynamique
     - Pa·s
     - StraightPipe

Air Handling (AHU)
----------------------

État de l'air
~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - T
     - Temperature de l'air
     - °C
     - FreshAir, HeatingCoil, Humidifier
   * - RH
     - Humidité relative
     - %
     - FreshAir, HeatingCoil, Humidifier
   * - w
     - Humidité absolue
     - g/kg_air_sec
     - FreshAir, HeatingCoil, Humidifier
   * - h
     - Enthalpy spécifique
     - kJ/kg
     - FreshAir, HeatingCoil, Humidifier
   * - P
     - Pressure atmosphérique
     - Pa
     - FreshAir, HeatingCoil, Humidifier
   * - Pv_sat
     - Pressure de vapeur saturante
     - Pa
     - FreshAir, HeatingCoil, Humidifier

Flow rates d'air
~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - F_m3h
     - Flow rate volumique d'air
     - m³/h
     - FreshAir, HeatingCoil, Humidifier
   * - F
     - Flow rate massique d'air humide
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_dry
     - Flow rate massique d'air sec
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_water
     - Flow rate d'eau d'humidification
     - kg/s
     - Humidifier

Processing Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - Q_th
     - Power thermique
     - kW
     - HeatingCoil
   * - To_target
     - Temperature de output cible
     - °C
     - HeatingCoil
   * - wo_target
     - Humidité absolue de output cible
     - g/kg_air_sec
     - Humidifier
   * - HumidType
     - Type d'humidification
     - String
     - Humidifier
   * - humidity
     - Humidité relative ambiante
     - %
     - PipeInsulationAnalysis

Hydraulique
-----------

Écoulement
~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - V
     - Speed d'écoulement
     - m/s
     - StraightPipe
   * - Re
     - Number Reynolds number
     - -
     - StraightPipe
   * - f
     - Facteur de friction (Darcy)
     - -
     - StraightPipe
   * - K
     - Roughness absolue
     - m
     - StraightPipe
   * - alpha (α)
     - Angle d'inclinaison
     - rad
     - StraightPipe

Losss de charge
~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - delta_P (ΔP)
     - Loss de pressure
     - Pa
     - StraightPipe
   * - L
     - Length de tuyau
     - m
     - StraightPipe
   * - A
     - Section du tube
     - m²
     - StraightPipe

Conventions
-----------

Unités
~~~~~~

- Temperatures : °C (sauf indication contraire)
- Pressures : Pa, bar (selon contexte)
- Flow rates massiques : kg/s, kg/h
- Flow rates volumiques : m³/s, m³/h, Sm³/s (standard : 0°C, 1 atm)
- Lengths : m, mm
- Surfaces : m²
- Powers : W, kW

Types de data
~~~~~~~~~~~~~~~~

- **String** : Chaîne de caractères (ex: nom de fluid, type de matériau)
- **Float** : Number décimal
- **Integer** : Number entier
- **Boolean** : True/False
- **Dict** : Dictionnaire Python (paires clé-valeur)

Nomenclature des équations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Darcy-Weisbach** : :math:`\Delta P = f \cdot \frac{L}{d_{hyd}} \cdot \frac{\rho V^2}{2}`
- **Reynolds** : :math:`Re = \frac{\rho V d_{hyd}}{\mu}`
- **Colebrook-White** : :math:`\frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{K/d_{hyd}}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)`
- **Titre vapeur** : :math:`x = \frac{H - H_l}{H_v - H_l}`
