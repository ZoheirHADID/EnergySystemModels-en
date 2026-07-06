.. _turbine:

Turbine
=======

Le module ``Turbine`` modélise une détente. Comme le compresseur, l'état d'input
provient d'un composant amont **connecté via** ``Fluid_connect(TURB.Inlet, amont.Outlet)`` ;
la pressure d'échappement est fixée by ``LP`` (en Pa, défaut 1 bar).

Parameters
----------

.. list-table::
   :header-rows: 1

   * - Attribut
     - Description
     - Unité
   * - ``Inlet``
     - Port d'input (rempli by ``Fluid_connect`` from l'amont)
     - —
   * - ``LP``
     - Pressure d'échappement (basse pressure)
     - Pa
   * - ``IsenEff``
     - Rendement isentropique (défaut 0,7)
     - —

Example
-------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Turbine import Turbine
    from ThermodynamicCycles.Connect import Fluid_connect

    # État d'entrée : gaz chaud sous pression fourni par une Source
    SOURCE = Source.Object()
    SOURCE.Pi_bar = 8
    SOURCE.Ti_degC = 400
    SOURCE.fluid = "air"
    SOURCE.F = 1                 # kg/s
    SOURCE.calculate()

    # Turbine alimentée par la Source
    TURBINE = Turbine.Object()
    Fluid_connect(TURBINE.Inlet, SOURCE.Outlet)
    TURBINE.LP = 1.01325 * 100000     # pression d'échappement en Pa (~1 atm)
    TURBINE.calculate()

    print(TURBINE.df)

Output réelle (``TURBINE.df``) :

.. code-block:: text

                    Turbine
    Fluid               air
    IsenEff             0.7
    Inlet.P (bar)       8.0
    LP (bar)           1.01
    F (kg/s)              1
    To (C)           195.83
    Ho (J/kg)      597537.4
    So (J/kg.K)     4339.17
    Q_turb (W)     213456.9

Principaux results : temperature d'échappement ``To`` ≈ 195,8 °C et power
récupérée ``Q_turb`` ≈ 213,5 kW for une détente de 8 bar / 400 °C à ~1 atm.

.. note::
   La turbine ne définit pas ``Pi_bar``/``Ti_degC``/``F`` : ces grandeurs
   viennent du port ``Inlet`` connecté à l'amont. Sans ``Fluid_connect``,
   ``calculate()`` lève une erreur.
