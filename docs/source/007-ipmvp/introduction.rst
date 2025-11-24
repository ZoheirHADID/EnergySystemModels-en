Introduction au module IPMVP
==============================

Objectif
--------

The IPMVP module of EnergySystemModels allows quantifying energy savings according to the IPMVP protocol (Option C) by creating baseline models based on polynomial regressions.

Principe
--------

The module compares energy consumption before (baseline) and after an energy efficiency project, adjusting for independent variables (weather, production, occupation).

.. math::

   \text{Économies} = \text{Baseline}_{\text{ajustée}} - \text{Consommation}_{\text{mesurée}}

Input Data Structure
-------------------------------

The module requires :

* **y** : Time series of energy consumption (kWh)
* **X** : DataFrame of independent variables (HDD, production, etc.)
* **Periods** : Start/end dates of baseline and reporting periods
