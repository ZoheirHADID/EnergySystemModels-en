.. _ng_boiler_efficiency:

NG Boiler Efficiency (EN12952-15)
==================================

The ``NG_Boiler_Efficiency`` module computes natural gas boiler efficiency using the **indirect method** (heat losses calculation) according to EN12952-15 (water tube) and EN12953-11 (fire tube). Uses CoolProp for accurate flue gas enthalpies.

Features
--------

* LHV and HHV efficiency by indirect method
* Losses: flue gas (sensible), CO, radiation, condensation
* Water side (``Inlet``/``Outlet`` FluidPort) — temperature setpoint
* Flue gas port (``FG_Outlet``) with composition, enthalpy, dew point
* Automatic NG flow adaptation to water heating demand

Example 1: Fixed NG flow
-------------------------

.. code-block:: python

    from ThermodynamicCycles.Combustion.NG_Boiler_Efficiency_EN1295X import (
        NG_Boiler_Efficiency
    )

    boiler = NG_Boiler_Efficiency(
        gas_composition={'CH4': 0.9489, 'C2H6': 0.01235, 'C3H8': 0.00935,
            'n-C4H10': 0.00614, 'N2': 0.00839, 'CO2': 0.01269},
        ng_flow_Nm3h=2000,
        flue_gas_temperature_C=180, O2_measured=0.035,
        boiler_type='water_tube', design_useful_heat_kW=22000,
    )
    boiler.calculate()
    print(boiler.df)

Example 2: Economizer sizing via FlueGasPort
----------------------------------------------

.. code-block:: python

    fg = boiler.FG_Outlet
    print(fg.df)

    # Sensible heat recovery: flue gas 180C -> 80C
    h_in = fg.enthalpy_at(180)
    h_out = fg.enthalpy_at(80)
    Q_eco = (h_in - h_out) * fg.F_Nm3h
    print(f"Economizer gain: {Q_eco:.0f} kW")

    # Condensation recovery: flue gas -> 50C
    Q_cond, kg_cond = fg.condensation_heat(50)
    print(f"Condensation: {Q_cond * fg.F_Nm3h:.0f} kW, {kg_cond * fg.F_Nm3h:.0f} kg/h")
