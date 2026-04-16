PV Module Usage
================

Complete Example
----------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(
       latitude=45.764, longitude=4.8357,
       name='Lyon Factory', altitude=200,
       timezone='Europe/Paris',
       azimut=180, inclinaison=20
   )

   pv.retrieve_module_inverter_data(
       module_name='Canadian_Solar_CS5P_220M___2009_',
       inverter_name='ABB__MICRO_0_25_I_OUTD_US_208__208V_',
       temperature_model='open_rack_glass_glass'
   )

   pv.calculate_solar_parameters()
   print(pv.df)

Parameters
----------

* **latitude/longitude** : GPS coordinates
* **altitude** : Meters above sea level
* **azimut** : Panel orientation (0=North, 180=South)
* **inclinaison** : Tilt angle from horizontal
* **module_name** : PV module (Sandia database, 500+ modules)
* **inverter_name** : Inverter (CEC database, 1000+ inverters)
* **temperature_model** : Thermal model (open_rack_glass_glass, etc.)

Available Methods
-----------------

* ``pv.df`` — System summary (module, area, production, productivity)
* ``pv.summary()`` — Technical + economic summary (Payback, ROI, IRR)
* ``pv.plot(nb_modules)`` — Hourly production + monthly profile
* ``pv.to_excel(filename, nb_modules)`` — Excel export (hourly, monthly, summary)
* ``SolarSystem.orientation_study(...)`` — Compare orientations/tilts
* ``SolarSystem.plot_orientation_study(df, df_monthly)`` — Monthly profiles chart
