.. _ng_heating_value:

NG Heating Value (HHV/LHV — ISO 6976)
=======================================

The ``NG_Heating_Value`` module computes natural gas thermodynamic properties from molar composition according to **ISO 6976**: HHV (PCS), LHV (PCI), density, Wobbe index, Cp, compressibility factor Z.

Example
-------

.. code-block:: python

    from ThermodynamicCycles.Combustion.NG_Heating_Value import NG_Heating_Value

    gas = NG_Heating_Value([
        NG_Heating_Value.GasComponent("CH4", 0.9489),
        NG_Heating_Value.GasComponent("C2H6", 0.01235),
        NG_Heating_Value.GasComponent("C3H8", 0.00935),
        NG_Heating_Value.GasComponent("n-C4H10", 0.00614),
        NG_Heating_Value.GasComponent("N2", 0.00839),
        NG_Heating_Value.GasComponent("CO2", 0.01269),
    ])
    print(gas.df)
