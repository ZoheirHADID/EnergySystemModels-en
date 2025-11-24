.. _nomenclature:

General Nomenclature
====================

This page compiles all symbols, parameters, and variables used in the EnergySystemModels library.

Heat Transfer (HeatTransfer)
-----------------------------

Geometry and Dimensions
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - L
     - Body length
     - m
     - ParallelepipedicBody
   * - W
     - Body width
     - m
     - ParallelepipedicBody
   * - H
     - Body height
     - m
     - ParallelepipedicBody
   * - A
     - Exchange surface area
     - m²
     - CompositeWall, ParallelepipedicBody
   * - thickness
     - Layer thickness
     - m
     - CompositeWall
   * - d_hyd
     - Hydraulic diameter
     - m
     - StraightPipe
   * - DN
     - Nominal diameter
     - mm
     - PipeInsulationAnalysis
   * - L_tube
     - Pipe length
     - m
     - PipeInsulationAnalysis

Temperatures
~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - T
     - General temperature
     - °C
     - All modules
   * - Ta
     - Ambient temperature
     - °C
     - ParallelepipedicBody
   * - Tamb
     - Ambient temperature
     - °C
     - PipeInsulationAnalysis
   * - Ti
     - Interior temperature
     - °C
     - CompositeWall
   * - Ti_degC
     - Inlet temperature
     - °C
     - Source, StraightPipe
   * - Te
     - Exterior temperature
     - °C
     - CompositeWall
   * - Tp
     - Wall temperature
     - °C
     - ParallelepipedicBody
   * - T_fluid
     - Fluid temperature
     - °C
     - PipeInsulationAnalysis

Transfer Coefficients
~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - he
     - External convection coefficient
     - W/m²·K
     - CompositeWall
   * - hi
     - Internal convection coefficient
     - W/m²·K
     - CompositeWall
   * - conductivity
     - Thermal conductivity
     - W/m·K
     - CompositeWall

Surface Properties
~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - emissivity
     - Surface emissivity
     - -
     - PipeInsulationAnalysis
   * - isolated
     - Face insulation indicator
     - True/False
     - ParallelepipedicBody
   * - faces_config
     - Faces configuration
     - dict
     - ParallelepipedicBody

Materials and Insulation
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 30

   * - Parameter
     - Description
     - Possible Values
   * - material (pipes)
     - Pipe material
     - 'steel', 'copper', 'PVC', 'PE', 'stainless_steel', 'cast_iron'
   * - material (walls)
     - Construction material
     - 'Béton' (Concrete), 'Brique' (Brick), 'Bois' (Wood), 'Acier' (Steel), 'Aluminium', 'Verre' (Glass), etc.
   * - insulation
     - Insulation type
     - 'laine_de_verre' (glass wool), 'laine_de_roche' (rock wool), 'polystyrène_expansé' (expanded polystyrene), 'polyuréthane' (polyurethane), etc.
   * - insulation_thickness
     - Insulation thickness
     - m

Thermodynamic Cycles
--------------------

Fluids and Refrigerants
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - fluid
     - Fluid/refrigerant name
     - String
     - Source, StraightPipe
   * - Ti_degC
     - Inlet temperature
     - °C
     - Source
   * - Pi_bar
     - Inlet pressure
     - bar
     - Source, StraightPipe

Available Fluids (CoolProp)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Natural fluids**: Water, Air, Nitrogen, Oxygen, CarbonDioxide, Hydrogen, Methane, Ethane, Propane, Butane, IsoButane, Pentane, IsoPentane, Hexane, Heptane, Octane, Nonane, Decane

**HFC refrigerants**: R134a, R125, R143a, R152a, R32, R245fa, R236fa, R227ea, R365mfc, R404A, R407C, R410A, R507A

**Natural refrigerants**: R717 (Ammonia), R744 (CO2), R290 (Propane), R600a (Isobutane), R1270 (Propylene)

**Others**: Benzene, Toluene, Acetone, Ethanol, Methanol, D4, D5, D6, MD2M, MD3M, MD4M, MDM, MM, Neopentane, Cyclohexane, p-Xylene, m-Xylene, o-Xylene

Flow Rates
~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - F
     - Mass flow rate
     - kg/s
     - Source
   * - F_kgs
     - Mass flow rate
     - kg/s
     - Source, StraightPipe
   * - F_kgh
     - Mass flow rate
     - kg/h
     - Source, StraightPipe
   * - F_m3s
     - Volumetric flow rate
     - m³/s
     - Source, StraightPipe
   * - F_m3h
     - Volumetric flow rate
     - m³/h
     - Source, StraightPipe, PipeInsulationAnalysis
   * - F_Sm3s
     - Standard volumetric flow rate (0°C, 1 atm)
     - Sm³/s
     - Source, StraightPipe
   * - F_Sm3h
     - Standard volumetric flow rate (0°C, 1 atm)
     - Sm³/h
     - Source, StraightPipe

Thermodynamic Properties
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - h
     - Specific enthalpy
     - J/kg (kJ/kg)
     - Source, FreshAir
   * - H_v
     - Vapor enthalpy
     - J/kg
     - Source
   * - H_l
     - Liquid enthalpy
     - J/kg
     - Source
   * - rho (ρ)
     - Density
     - kg/m³
     - Source, StraightPipe
   * - mu (η)
     - Dynamic viscosity
     - Pa·s
     - StraightPipe

Air Handling Units (AHU)
-------------------------

Air State
~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - T
     - Air temperature
     - °C
     - FreshAir, HeatingCoil, Humidifier
   * - RH
     - Relative humidity
     - %
     - FreshAir, HeatingCoil, Humidifier
   * - w
     - Absolute humidity
     - g/kg_dry_air
     - FreshAir, HeatingCoil, Humidifier
   * - h
     - Specific enthalpy
     - kJ/kg
     - FreshAir, HeatingCoil, Humidifier
   * - P
     - Atmospheric pressure
     - Pa
     - FreshAir, HeatingCoil, Humidifier
   * - Pv_sat
     - Saturation vapor pressure
     - Pa
     - FreshAir, HeatingCoil, Humidifier

Air Flow Rates
~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - F_m3h
     - Volumetric air flow rate
     - m³/h
     - FreshAir, HeatingCoil, Humidifier
   * - F
     - Moist air mass flow rate
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_dry
     - Dry air mass flow rate
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_water
     - Humidification water flow rate
     - kg/s
     - Humidifier

Treatment Parameters
~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - Q_th
     - Thermal power
     - kW
     - HeatingCoil
   * - To_target
     - Target outlet temperature
     - °C
     - HeatingCoil
   * - wo_target
     - Target outlet absolute humidity
     - g/kg_dry_air
     - Humidifier
   * - HumidType
     - Humidification type
     - String
     - Humidifier
   * - humidity
     - Ambient relative humidity
     - %
     - PipeInsulationAnalysis

Hydraulics
----------

Flow
~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - V
     - Flow velocity
     - m/s
     - StraightPipe
   * - Re
     - Reynolds number
     - -
     - StraightPipe
   * - f
     - Darcy friction factor
     - -
     - StraightPipe
   * - K
     - Absolute roughness
     - m
     - StraightPipe
   * - alpha (α)
     - Inclination angle
     - rad
     - StraightPipe

Pressure Losses
~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbol
     - Description
     - Unit
     - Module
   * - delta_P (ΔP)
     - Pressure loss
     - Pa
     - StraightPipe
   * - L
     - Pipe length
     - m
     - StraightPipe
   * - A
     - Pipe cross-section
     - m²
     - StraightPipe

Conventions
-----------

Units
~~~~~

- Temperatures: °C (unless otherwise stated)
- Pressures: Pa, bar (depending on context)
- Mass flow rates: kg/s, kg/h
- Volumetric flow rates: m³/s, m³/h, Sm³/s (standard: 0°C, 1 atm)
- Lengths: m, mm
- Areas: m²
- Powers: W, kW

Data Types
~~~~~~~~~~

- **String**: Character string (e.g., fluid name, material type)
- **Float**: Decimal number
- **Integer**: Whole number
- **Boolean**: True/False
- **Dict**: Python dictionary (key-value pairs)

Equation Nomenclature
~~~~~~~~~~~~~~~~~~~~~

- **Darcy-Weisbach**: :math:`\Delta P = f \cdot \frac{L}{d_{hyd}} \cdot \frac{\rho V^2}{2}`
- **Reynolds**: :math:`Re = \frac{\rho V d_{hyd}}{\mu}`
- **Colebrook-White**: :math:`\frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{K/d_{hyd}}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)`
- **Vapor quality**: :math:`x = \frac{H - H_l}{H_v - H_l}`
