.. _ta_valve:

4.2. TA Balancing Valve (Tour & Andersson / IMI Hydronic)
==========================================================

**TA** balancing valves (Tour & Andersson / IMI Hydronic Engineering) are essential components in HVAC systems. They enable hydraulic balancing of circuits to ensure nominal flow rates and optimize energy performance of installations.

This Python class calculates pressure drops through different TA valve models using **official Kv data** from IMI TA manufacturer based on the number of opening turns.

.. image:: ../images/TAValve.png
   :alt: TA Valve
   :width: 800px
   :align: center

4.2.1. Introduction
-------------------

**TA** balancing valves (Tour & Andersson / IMI Hydronic Engineering) are essential components in heating, ventilation, and air conditioning (HVAC) systems. They enable hydraulic balancing of circuits to ensure nominal flow rates and optimize energy performance of installations.

4.2.2. Available TA Valve Types
--------------------------------

The ``TA_Valve`` class supports **over 120 references** of IMI TA balancing valves:

.. list-table:: **TA Valve Types and Available References**
   :header-rows: 1
   :widths: 25 20 55

   * - **Series**
     - **DN Range**
     - **Typical Application**
   * - **STAD**
     - DN10-50
     - Threaded secondary networks (PN 25)
   * - **STAV**
     - DN15-50
     - Economic Venturi secondary networks (PN 20)
   * - **TBV / TBV-C**
     - DN10-20
     - Terminal units: radiators, fan coil units (PN 20)
   * - **STAF**
     - DN20-400
     - Main networks cast iron flanged (PN 16/25)
   * - **STAF-SG**
     - DN65-400
     - Large GS cast iron high resistance networks (PN 16/25)
   * - **STAG**
     - DN65-300
     - Fast installation with Victaulic grooved fittings (PN 16)
   * - **STA**
     - DN15-150
     - Old installations (maintenance)
   * - **STAP / STAM**
     - DN15-100
     - ΔP regulators for dynamic balancing
   * - **MDFO**
     - DN20-900
     - Fixed measurement orifices (fixed Kv)

.. note::
   The ``dn`` parameter can be specified as a **string** (e.g., "DN65", "STAF-DN100") or an **integer** (e.g., 65).

4.2.3. Python Usage Examples
-----------------------------

**Complete Example: STAF-DN100 Valve for Main Network**

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    # Water source configuration
    SOURCE = Source.Object()
    SOURCE.Ti_degC = 25           # Inlet temperature: 25°C
    SOURCE.Pi_bar = 3.0           # Inlet pressure: 3 bar
    SOURCE.fluid = "Water"        # Fluid: water
    SOURCE.F_m3h = 70             # Flow rate: 70 m³/h
    SOURCE.calculate()

    # STAF-DN100 valve configuration
    vanne = TA_Valve.Object()
    vanne.dn = "STAF-DN100"       # Type: STAF-DN100 (cast iron flange, PN 16/25)
    vanne.nb_tours = 4.3          # Opening: 4.3 turns (auto interpolation)
    Fluid_connect(vanne.Inlet, SOURCE.Outlet) 
    vanne.calculate()

    # Display results
    print(vanne.df)
    print(f"Outlet pressure: {vanne.Outlet.P:.2f} Pa")
    print(f"Pressure drop: {vanne.delta_P:.2f} Pa")

**Simulation Results:**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 70.000
   * - Number of turns
     - 4.3
   * - Nominal diameter
     - STAF-DN100
   * - Interpolated Kv (m³/h)
     - ~81.4
   * - Pressure drop (Pa)
     - ~73500 (~0.74 bar)
   * - Inlet pressure (bar)
     - 3.0
   * - Outlet pressure (bar)
     - ~2.26

4.2.4. Calculation Model with Kv Coefficient
---------------------------------------------

**Kv Coefficient Principle**

The Kv coefficient represents the **water flow rate in m³/h** passing through the valve with a pressure drop of **1 bar** at 15-20°C. The higher the Kv, the more flow the valve allows for a given pressure drop.

**Calculation Equations**

**1. Volumetric flow rate from mass flow rate:**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Where:

- **Q**: Volumetric flow rate (m³/h)
- **ṁ**: Mass flow rate (kg/s)
- **ρ**: Fluid density (kg/m³)

**2. Pressure drop as a function of Kv:**

.. math::

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

Where:

- **ΔP**: Pressure drop (Pa)
- **Q**: Volumetric flow rate (m³/h)
- **Kv**: Flow coefficient for the given opening (m³/h)
- **10⁵**: Conversion factor (1 bar = 10⁵ Pa)

**Calculation Example:**

For Q = 70 m³/h and Kv = 81.4 m³/h:

.. math::

  \Delta P = \left(\frac{70}{81.4}\right)^2 \cdot 10^5 = (0.860)^2 \cdot 10^5 = 73960 \text{ Pa}

**3. Kv Interpolation:**

If the number of turns does not exactly match a tabulated value, **linear interpolation** is performed:

.. math::

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{turns} - n_{inf})}{(n_{sup} - n_{inf})}

**Interpolation Example:**

For a STAF-DN100 valve with 4.3 turns (between 4 turns and 4.5 turns):

- Kv(4 turns) = 66 m³/h
- Kv(4.5 turns) = 91.7 m³/h
- Interpolation: Kv(4.3) = 66 + (91.7-66) × (4.3-4)/(4.5-4) = 66 + 25.7 × 0.6 = 81.4 m³/h

**4. Conservation of Thermodynamic Properties:**

Through the valve (isenthalpic transformation):

- **Conserved mass flow rate:** :math:`\dot{m}_{outlet} = \dot{m}_{inlet}`
- **Conserved temperature:** :math:`T_{outlet} = T_{inlet}`
- **Reduced pressure:** :math:`P_{outlet} = P_{inlet} - \Delta P`

4.2.5. TA_Valve Class Parameters
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Parameter
     - Description
     - Unit
   * - **nb_tours**
     - Number of valve opening turns (0 for regulators/fixed orifices)
     - turns
   * - **dn**
     - Nominal diameter or valve reference (string or integer)
     - -
   * - **q**
     - Volumetric flow rate calculated from mass flow rate
     - m³/h
   * - **Kv**
     - Flow coefficient according to IMI TA tables (interpolated if necessary)
     - m³/h
   * - **delta_P**
     - Pressure drop across the valve
     - Pa
   * - **rho**
     - Fluid density (calculated via CoolProp)
     - kg/m³
   * - **Ti_degC**
     - Inlet temperature
     - °C
   * - **Pi_bar**
     - Inlet pressure
     - bar
   * - **F_m3h**
     - Volumetric flow rate
     - m³/h
   * - **F_kgs**
     - Mass flow rate
     - kg/s
   * - **Inlet**
     - Fluid inlet port
     - FluidPort
   * - **Outlet**
     - Fluid outlet port
     - FluidPort

.. note::
   Fluid thermodynamic properties (density, viscosity) are automatically calculated via **CoolProp** based on temperature and pressure.

4.2.6. Usage Recommendations
-----------------------------

**Valve Type Selection:**

1. **Main networks (> DN50)**: Prefer STAF, STAF-SG, or STAG
2. **Secondary networks (DN15-50)**: Use STAD or STAV
3. **Terminal units**: Choose TBV or TBV-C
4. **Automatic balancing**: Use STAP or STAM
5. **Measurement orifices**: MDFO for TA-Scope measurement

**Sizing:**

- Calculate the nominal circuit flow rate
- Select DN for a pressure drop between **3 and 15 kPa** at nominal flow
- Check the available adjustment range (number of turns)
- Allow margin for future adjustments

.. warning::
   - Do not exceed fluid temperature limits (typically -20°C to +120°C)
   - Respect nominal pressures PN 16/20/25 depending on models
   - Check fluid/material compatibility (glycol water, etc.)
   - For regulators (STAP, STAM, STAZ) and fixed orifices (MDFO), use **nb_tours = 0**

4.2.7. Data Sources and References
-----------------------------------

The Kv data used comes from **official IMI TA technical documentation**:

**Documentary Sources:**

- **STAD_PN25_FR_FR_low.pdf**: Kv tables for STAD DN10-50 valves
- **STAF_STAF-SG_EN_MAIN.pdf**: Kv tables for STAF and STAF-SG DN20-400 valves
- IMI Hydronic Engineering technical catalogs
- TA-Scope product sheets (MDFO, STAP, STAM)

**Certification and Compliance:**

- Kv values certified according to **EN 1267** (Industrial valves)
- Standards **PN 16**, **PN 20**, **PN 25** depending on models
- Compatible with **TA-Scope** and **TA-Surveyor** measurement systems

**Additional Documentation:**

- Official website: `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_
- Software: TA-Designer (hydraulic network sizing)
- Training: Hydraulic balancing and TA-Scope usage

4.2.8. Complete List of Available References
---------------------------------------------

**1. STAD - Threaded manual balancing valve PN 25 (DN 10-50)**

STAD-DN10, STAD-DN15, STAD-DN20, STAD-DN25, STAD-DN32, STAD-DN40, STAD-DN50

**2. STAV - Threaded Venturi balancing valve PN 20 (DN 15-50)**

STAV-DN15, STAV-DN20, STAV-DN25, STAV-DN32, STAV-DN40, STAV-DN50

**3. TBV - Terminal manual balancing valve (DN 15-20)**

TBV-DN15, TBV-DN20

**4. TBV-LF/NF - TBV variants with 1-10 position system (DN 15-20)**

TBV-LF-DN15, TBV-NF-DN15, TBV-NF-DN20

**5. TBV-C - Terminal balancing + TA-Scope control valve (DN 10-20)**

TBV-C-DN10, TBV-C-DN15, TBV-C-DN20

**6. STAF - Cast iron flanged balancing valve PN 16/25 (DN 20-400)**

STAF-DN20, STAF-DN25, STAF-DN32, STAF-DN40, STAF-DN50, STAF-DN65, 
STAF-DN80, STAF-DN100, STAF-DN125, STAF-DN150, STAF-DN200, STAF-DN250, 
STAF-DN300, STAF-DN350, STAF-DN400

**7. STAF-SG - STAF GS cast iron variant PN 16/25 (DN 65-400)**

STAF-SG-DN65, STAF-SG-DN80, STAF-SG-DN100, STAF-SG-DN125, STAF-SG-DN150, 
STAF-SG-DN200, STAF-SG-DN250, STAF-SG-DN300, STAF-SG-DN350, STAF-SG-DN400

**8. STAF-R - Balancing valve "return" version PN 16/25 (DN 65-200)**

STAF-R-DN65, STAF-R-DN80, STAF-R-DN100, STAF-R-DN125, STAF-R-DN150, 
STAF-R-DN200

**9. STAG - Grooved valve Victaulic type ends PN 16 (DN 65-300)**

STAG-DN65, STAG-DN80, STAG-DN100, STAG-DN125, STAG-DN150, STAG-DN200, 
STAG-DN250, STAG-DN300

**10. STA - Old TA balancing valve (DN 15-150) - Archive**

STA-DN15, STA-DN20, STA-DN25, STA-DN32, STA-DN40, STA-DN50, STA-DN65, 
STA-DN80, STA-DN100, STA-DN125, STA-DN150

**11. MDFO - Fixed measurement orifice (DN 20-900) - Fixed Kv**

MDFO-DN20, MDFO-DN25, MDFO-DN32, MDFO-DN40, MDFO-DN50, MDFO-DN65, 
MDFO-DN80, MDFO-DN100, MDFO-DN125, MDFO-DN150, MDFO-DN200, MDFO-DN250, 
MDFO-DN300, MDFO-DN350, MDFO-DN400, MDFO-DN450, MDFO-DN500, MDFO-DN600, 
MDFO-DN700, MDFO-DN800, MDFO-DN900

**12. STAP - Differential pressure regulator (DN 15-100) - Max Kv**

STAP-DN15, STAP-DN20, STAP-DN25, STAP-DN32, STAP-DN40, STAP-DN50, 
STAP-DN65, STAP-DN80, STAP-DN100

**13. STAM - ΔP regulator for loops and columns (DN 15-50) - Max Kv**

STAM-DN15, STAM-DN20, STAM-DN25, STAM-DN32, STAM-DN40, STAM-DN50

**14. STAZ / STAP-R - Legacy ΔP regulators for retrofits (DN 15-50) - Max Kv**

STAZ-DN15, STAZ-DN20, STAZ-DN25, STAZ-DN32, STAZ-DN40, STAZ-DN50
STAP-R-DN15, STAP-R-DN20, STAP-R-DN25, STAP-R-DN32, STAP-R-DN40, 
STAP-R-DN50

**TOTAL: 120+ valves and orifices available**
