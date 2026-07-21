API Reference
=============

This page summarizes the library's **real entry points**
(valid import paths with ``PYTHONPATH=src``) and links to the chapter
dedicated to each module, where executable examples with their
real outputs are shown.

.. note::
   Locally, in the repository, modules are imported **without** the prefix
   ``energysystemmodels.`` : the import name is the subpackage name, par
   example ``from ThermodynamicCycles.Compressor import Compressor``.

Heat Transfer — ``HeatTransfer``
---------------------------------------

.. code-block:: python

   from HeatTransfer import CompositeWall, ParallelepipedicBody
   from HeatTransfer import PipeInsulationAnalysis, PlateHeatTransfer

Each component is instantiated with ``.Object(...)`` then ``.calculate()`` ;
results in ``.df`` (and attributes such as ``R_total``, ``Q``, ``q_total``).
Details : :doc:`001-heat_transfer/index` and :doc:`transfert_chaleur`.

Thermodynamic Cycles — ``ThermodynamicCycles``
-------------------------------------------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Turbine import Turbine
   from ThermodynamicCycles.Chiller import Object as Chiller
   from ThermodynamicCycles.HEX import NUT_HEX, DTLM_HEX
   from ThermodynamicCycles.Combustion import NG_Heating_Value
   from ThermodynamicCycles.Connect import Fluid_connect

Components are assembled with ``Fluid_connect(aval.Inlet, amont.Outlet)``.
Details : :doc:`002-thermodynamic_cycles/index`.

Hydraulics and Aeraulics
-------------------------

.. code-block:: python

   from ThermodynamicCycles.Hydraulic import StraightPipe, TA_Valve
   from ThermodynamicCycles.Aeraulic import StraightPipe as AirDuct

Details : :doc:`004-hydraulic/index` and :doc:`005-aeraulic/index`.

Air Handling — ``AHU``
--------------------------

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Coil import HeatingCoil, CoolingCoil
   from AHU.Humidification import Humidifier
   from AHU.air_humide import air_humide
   from AHU.GenericAHU.AirRecyclingAHU import Object as AirRecyclingAHU
   from AHU.GenericAHU.AirRecoveryAHU import Object as AirRecoveryAHU

Details : :doc:`003-ahu_modules/index`.

Pinch Analysis — ``PinchAnalysis``
----------------------------------

.. code-block:: python

   from PinchAnalysis import PinchAnalysis

   pinch = PinchAnalysis.Object(df)   # df avec colonnes id, name, Ti, To, mCp, dTmin2
   pinch.Pinch_Temperature            # attributs réels : Heating_duty, Cooling_duty,
                                      # heat_recovery, df_hcc, df_ccc, df_combined

Details : :doc:`006-pinch_analysis/index`.

Measurement & Verification — ``IPMVP``
--------------------------------------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models   # retourne un tuple de 9 éléments

Details : :doc:`007-ipmvp/index`.

Meteorology
------------

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from MeteoCiel.DJU_costic import DJU_costic
   from OpenWeatherMap import OpenWeatherMap_call_location

Details : :doc:`008-meteo/index`.

Photovoltaics — ``PV``
-----------------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

Details : :doc:`009-pv-solaire/index`.

Energy Purchasing — ``Facture``
-------------------------------

.. code-block:: python

   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture
   from Facture.SONALGAZ_Elec import Sonalgaz_Elec
   from Facture.SONALGAZ_gaz import Sonalgaz_Gaz
   from Facture.ATR_Transport_Distribution import ATR_calculation

Details : :doc:`010-achat-energie/index`.

Energy Savings Certificates — ``CEE``
-------------------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches   # module de fonctions (pas de classe CEE)

Details : :doc:`011-cee/index`.
