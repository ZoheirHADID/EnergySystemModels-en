.. _chiller:

Chiller (Refrigeration / Heat Pump)
====================================

The ``Chiller`` module models a complete refrigeration cycle: evaporator, compressor, desuperheater, condenser, expansion valve. In heat pump mode, condenser heat is valorized.

Example
-------

.. code-block:: python

    from ThermodynamicCycles.Chiller import Object as Chiller

    ch = Chiller(
        fluid='R134a',
        evap_params={'Ti_degC': 5, 'surchauff': 5, 'F': 1.0},
        comp_params={'Tcond_degC': 40, 'eta_is': 0.75, 'Tdischarge_target': 90},
        cond_params={'subcooling': 3}
    )
    ch.calculate_cycle()
    print(ch.df)
    ch.plot()

Methods
-------

* ``ch.calculate_cycle()`` — Compute full thermodynamic cycle
* ``ch.df`` — Summary DataFrame (EER, COP, pressures, temperatures)
* ``ch.print_results()`` — Print DataFrame for each component
* ``ch.plot()`` — T-S diagram of the cycle
