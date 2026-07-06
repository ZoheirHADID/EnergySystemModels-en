.. _fluid_source:

Fluid Source
============

Usage
-----------

.. code-block:: python

    from ThermodynamicCycles.Source import Source

    # Créer un objet Source
    SOURCE = Source.Object()

    # Paramètres d'entrée
    SOURCE.Pi_bar = 1.01325
    SOURCE.Ti_degC = 25          # température d'entrée obligatoire
    SOURCE.fluid = "air"
    SOURCE.F = 1                 # débit massique [kg/s]

    # Calcul
    SOURCE.calculate()

    # Résultats
    print(SOURCE.df)

Output réelle (``SOURCE.df``) :

.. code-block:: text

                                Source
    Timestamp      2026-07-04 23:33:33
    fluid                          air
    Ti_degC                       25.0
    Pi_bar                        1.01
    F_Sm3h                      2937.5
    F_Nm3h                 2784.081453
    F_m3h                       3039.7
    F_kgh                         3600
    F_kgs                            1
    F_m3s                        0.844
    F_Sm3s                       0.816
    self.Outlet.h        424436.043917

Le DataFrame contient : la temperature d'input ``Ti_degC`` [°C], la pressure
``Pi_bar`` [bar], les flow rates déclinés en Sm³/h, Nm³/h, m³/h, kg/h, kg/s, m³/s,
Sm³/s, et l'enthalpy de output ``Outlet.h`` [J/kg].

.. note::
   ``SOURCE.Ti_degC`` est **obligatoire** : without elle, ``calculate()`` lève une
   ``TypeError`` (temperature à ``None``).

Possible Parameters
--------------------

**Fluids disponibles in CoolProp**

**Fluids purs courants :**

- ``'Water'`` - Eau
- ``'Air'`` - Air
- ``'Ammonia'`` (ou ``'NH3'``) - Ammoniac
- ``'CO2'`` (ou ``'CarbonDioxide'``) - Dioxyde de carbone
- ``'Nitrogen'`` (ou ``'N2'``) - Azote
- ``'Oxygen'`` (ou ``'O2'``) - Oxygène
- ``'Hydrogen'`` (ou ``'H2'``) - Hydrogène
- ``'Methane'`` - Méthane
- ``'Propane'`` - Propane
- ``'n-Butane'`` - n-Butane
- ``'IsoButane'`` - Isobutane

**Frigorigènes HFC :**

- ``'R134a'`` - 1,1,1,2-Tétrafluoroéthane
- ``'R32'`` - Difluorométhane
- ``'R125'`` - Pentafluoroéthane
- ``'R143a'`` - 1,1,1-Trifluoroéthane
- ``'R152a'`` - 1,1-Difluoroéthane
- ``'R404A'`` - Mélange (R125/143a/134a)
- ``'R407C'`` - Mélange (R32/125/134a)
- ``'R410A'`` - Mélange (R32/125)
- ``'R507A'`` - Mélange (R125/143a)

**Frigorigènes naturels et autres :**

- ``'R290'`` (ou ``'Propane'``) - Propane
- ``'R600a'`` (ou ``'IsoButane'``) - Isobutane
- ``'R717'`` (ou ``'Ammonia'``) - Ammoniac
- ``'R744'`` (ou ``'CO2'``) - Dioxyde de carbone
- ``'R1234yf'`` - 2,3,3,3-Tétrafluoropropène
- ``'R1234ze(E)'`` - trans-1,3,3,3-Tétrafluoropropène

**Fluids industriels :**

- ``'Toluene'`` - Toluène
- ``'Ethanol'`` - Éthanol
- ``'Acetone'`` - Acétone
- ``'Methanol'`` - Méthanol

.. note::
   Pour la liste complète des fluids disponibles, consultez la documentation officielle de CoolProp : http://www.coolprop.org/fluid_properties/PurePseudoPure.html

**Types de flow rates disponibles** :

- ``F`` : Flow rate massique [kg/s]
- ``F_kgh`` : Flow rate massique [kg/h]
- ``F_Sm3s`` / ``F_Sm3h`` : Flow rate volumique standard [Sm³/s] / [Sm³/h]
- ``F_Nm3s`` / ``F_Nm3h`` : Flow rate volumique normal [Nm³/s] / [Nm³/h]
- ``F_m3s`` / ``F_m3h`` : Flow rate volumique aux conditions d'input [m³/s] / [m³/h]

Explication du model
----------------------

The model Fluid Source calcule le flow rate massique as a function of diverses conditions d'input et des propriétés of the fluid. The model utilise the library CoolProp for déterminer les propriétés of the fluid et effectue les calculs suivants :

1. Convertir les flow rates volumiques en flow rates massiques en utilisant la densité of the fluid.
2. Calculer l'enthalpy de output et déterminer la qualité of the fluid (liquide, vapeur, diphasique ou supercritique).
3. Mettre à jour les propriétés de output et générer un DataFrame with les results.

Les principales équations utilisées in le model sont :

- Flow rate massique à partir de mètres cubes standards by heure (Sm³/h) :

  .. math::
    \dot{m} = \frac{F_{Sm3h}}{3600} \cdot \rho(P_{std}, T_{std})

- Flow rate massique à partir de mètres cubes normaux by heure (Nm³/h) :

  .. math::
    \dot{m} = \frac{F_{Nm3h}}{3600} \cdot \rho(P_{std}, T_{norm})

- Flow rate massique à partir de mètres cubes by seconde (m³/s) :

  .. math::
    \dot{m} = F_{m3s} \cdot \rho(P_{in}, T_{in})

- Enthalpy de output :

  .. math::
    h_{out} = \text{PropsSI}('H', 'P', P_{out}, 'T', T_{in}, \text{fluid})

- Quality of the fluid :

  .. math::
    Q = 1 - \frac{H_v - h_{out}}{H_v - H_l}

où :

- :math:`\rho` est la densité of the fluid,
- :math:`P_{std}` et :math:`T_{std}` sont la pressure et la temperature standards,
- :math:`P_{norm}` et :math:`T_{norm}` sont la pressure et la temperature normales,
- :math:`P_{in}` et :math:`T_{in}` sont la pressure et la temperature d'input,
- :math:`H_v` et :math:`H_l` sont les enthalpys de la vapeur et du liquide à la pressure d'input.
