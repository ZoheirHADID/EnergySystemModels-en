=====
Usage
=====

.. _installation:

Installation
------------

To use EnergySystemModels, first install it using pip:

.. code-block:: console

   (.venv) $ pip install EnergySystemModels

Overview
--------

EnergySystemModels is a comprehensive Python library for modeling and analyzing energy systems.
This documentation is organized according to the **energy value chain**, from supplier to end use:

1. **Purchasing and Billing**: TURPE, CEE
2. **Data and Production**: Meteorology, Photovoltaics
3. **Transformation**: Thermodynamic Cycles
4. **Distribution**: Heat Transfer, Hydraulics, Air Distribution
5. **End Uses**: AHU, Pinch Analysis, IPMVP, RC Model

================================================================================
Section 1: Energy Purchasing and Billing
================================================================================

1.1. TURPE Module - Public Electricity Network Usage Tariff
------------------------------------------------------------

The TURPE module allows calculation of electricity transmission and distribution costs according to French regulated tariffs.

Main Classes
~~~~~~~~~~~~

**TURPEProfil**

Represents a TURPE tariff profile with its characteristics:

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil
   
   profil = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )

**TURPECalculateur**

Performs TURPE billing calculations:

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPECalculateur
   import pandas as pd
   
   # Prepare consumption data
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   calculateur = TURPECalculateur(profil)
   cout_total = calculateur.calculer_cout_annuel(consommation)
   print(f"Annual TURPE cost: {cout_total:.2f} €")

Complete Example: HTA Tariff Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Define HTA5 profile
   profil_hta5 = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )
   
   # Generate realistic load profile
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   base_load = 150.0
   variation = 50.0 * np.sin(2 * np.pi * np.arange(8760) / 24)
   consommation = pd.Series(base_load + variation, index=dates)
   
   # Calculate costs
   calculateur = TURPECalculateur(profil_hta5)
   
   # Total annual cost
   cout_total = calculateur.calculer_cout_annuel(consommation)
   
   # Cost breakdown by component
   details = calculateur.decomposition_couts(consommation)
   
   print(f"Total annual cost: {cout_total:.2f} €")
   print("\nBreakdown:")
   for composante, montant in details.items():
       print(f"  {composante}: {montant:.2f} €")

Example: Tariff Profile Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   
   # Profiles to compare
   profils = [
       TURPEProfil("HTA5", 250, "C5", "LU"),
       TURPEProfil("HTA5", 250, "C5", "MU"),
       TURPEProfil("BT>36", 100, "C5", "LU")
   ]
   
   # Same consumption profile
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   # Compare costs
   resultats = {}
   for profil in profils:
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       resultats[profil.nom] = cout
   
   print("Annual cost comparison:")
   for nom, cout in resultats.items():
       print(f"  {nom}: {cout:.2f} €")

Example: Subscribed Power Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Load profile with peaks
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series(100 + 50 * np.random.random(8760), index=dates)
   
   # Actual peak power
   puissance_pointe = consommation.max()
   print(f"Peak power: {puissance_pointe:.1f} kW")
   
   # Test different subscribed powers
   puissances_test = np.arange(
       puissance_pointe * 0.9, 
       puissance_pointe * 1.3, 
       10
   )
   
   resultats_optimisation = []
   for ps in puissances_test:
       profil = TURPEProfil("HTA5", ps, "C5", "LU")
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       depassements = calculateur.calculer_depassements(consommation)
       
       resultats_optimisation.append({
           'puissance_souscrite': ps,
           'cout_total': cout,
           'nb_depassements': depassements
       })
   
   # Find optimum
   df_optim = pd.DataFrame(resultats_optimisation)
   optimum = df_optim.loc[df_optim['cout_total'].idxmin()]
   
   print(f"\nOptimal subscribed power: {optimum['puissance_souscrite']:.1f} kW")
   print(f"Optimal annual cost: {optimum['cout_total']:.2f} €")

1.2. CEE Module - Energy Savings Certificates
----------------------------------------------

The CEE module allows calculation of energy savings and certificate volumes generated according to standardized operation sheets.

Sheet BAT-TH-116: Insulation of Attics or Roofs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_116 import IsolationCombles
   
   # Insulation project
   isolation = IsolationCombles(
       surface_m2=150,
       resistance_thermique_initiale=2.0,  # m².K/W
       resistance_thermique_finale=7.0,    # m².K/W
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calculate CEE
   kwh_cumac = isolation.calculer_kwh_cumac()
   montant_cee = isolation.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Savings: {kwh_cumac:,.0f} kWh cumac")
   print(f"CEE valuation: {montant_cee:.2f} €")

Sheet BAT-TH-104: Complete Windows or French Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_104 import FenetresPerformantes
   
   # Window replacement
   fenetres = FenetresPerformantes(
       nombre_fenetres=12,
       surface_moyenne_m2=1.5,
       uw_initial=2.8,  # W/m².K
       uw_final=1.3,    # W/m².K
       zone_climatique="H1",
       type_chauffage="electricite"
   )
   
   # Calculate CEE
   kwh_cumac = fenetres.calculer_kwh_cumac()
   print(f"Window savings: {kwh_cumac:,.0f} kWh cumac")

Sheet BAT-TH-127: Humidity-Controlled Single-Flow Mechanical Ventilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_127 import VMCHygroreglable
   
   # VMC installation
   vmc = VMCHygroreglable(
       surface_habitable_m2=120,
       type_vmc="hygroB",  # A or B
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calculate CEE
   kwh_cumac = vmc.calculer_kwh_cumac()
   print(f"VMC savings: {kwh_cumac:,.0f} kWh cumac")

Sheet BAT-TH-113: High-Performance Collective Boiler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_113 import ChaudiereCollective
   
   # Boiler replacement
   chaudiere = ChaudiereCollective(
       puissance_nominale_kW=500,
       efficacite_ancienne=0.75,
       efficacite_nouvelle=0.95,
       zone_climatique="H1",
       nombre_logements=50
   )
   
   # Calculate CEE
   kwh_cumac = chaudiere.calculer_kwh_cumac()
   montant = chaudiere.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Boiler savings: {kwh_cumac:,.0f} kWh cumac")
   print(f"CEE amount: {montant:.2f} €")

Sheet IND-UT-134: Heat Recovery on Chiller Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.IND_UT_134 import RecuperateurChaleurGroupeFroid
   
   # Recovery installation
   recuperateur = RecuperateurChaleurGroupeFroid(
       puissance_frigorifique_kW=300,
       cop_groupe_froid=3.0,
       taux_recuperation=0.65,
       heures_fonctionnement_annuelles=6000,
       secteur="tertiaire"
   )
   
   # Calculate CEE
   kwh_cumac = recuperateur.calculer_kwh_cumac()
   print(f"Recovery savings: {kwh_cumac:,.0f} kWh cumac")

Complete Example: Energy Renovation Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE import *
   
   # Define all project works
   operations_cee = {
       'isolation_combles': IsolationCombles(
           surface_m2=200,
           resistance_thermique_initiale=2.0,
           resistance_thermique_finale=8.0,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'fenetres': FenetresPerformantes(
           nombre_fenetres=15,
           surface_moyenne_m2=1.8,
           uw_initial=3.0,
           uw_final=1.2,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'vmc': VMCHygroreglable(
           surface_habitable_m2=150,
           type_vmc="hygroB",
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'chaudiere': ChaudiereCollective(
           puissance_nominale_kW=80,
           efficacite_ancienne=0.70,
           efficacite_nouvelle=0.95,
           zone_climatique="H1",
           nombre_logements=1
       )
   }
   
   # Calculate total CEE
   prix_kwh_cumac = 0.006  # €/kWh cumac
   total_kwh_cumac = 0
   total_montant = 0
   
   print("CEE operations detail:")
   print("-" * 70)
   
   for nom, operation in operations_cee.items():
       kwh = operation.calculer_kwh_cumac()
       montant = operation.calculer_montant_cee(prix_kwh_cumac)
       total_kwh_cumac += kwh
       total_montant += montant
       
       print(f"{nom:25s} : {kwh:>12,.0f} kWh cumac = {montant:>10,.2f} €")
   
   print("-" * 70)
   print(f"{'TOTAL':25s} : {total_kwh_cumac:>12,.0f} kWh cumac = {total_montant:>10,.2f} €")

================================================================================
Section 2: Data and Energy Production
================================================================================

2.1. Meteorological Data
-------------------------

2.1.1. OpenWeatherMap - Real-Time Weather Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenWeatherMap module provides access to current and forecast meteorological data.

.. code-block:: python

   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   
   # Initialize client
   api_key = "your_api_key"
   client = OpenWeatherMapClient(api_key)
   
   # Current weather data
   meteo_actuelle = client.get_current_weather(
       city="Paris",
       country="FR"
   )
   
   print(f"Temperature: {meteo_actuelle['temperature']}°C")
   print(f"Humidity: {meteo_actuelle['humidity']}%")
   print(f"Wind speed: {meteo_actuelle['wind_speed']} m/s")
   
   # 5-day forecast
   previsions = client.get_forecast(
       city="Paris",
       country="FR",
       days=5
   )
   
   for jour in previsions:
       print(f"{jour['date']}: {jour['temperature']}°C, {jour['description']}")

Example: Hourly Weather Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   import pandas as pd
   
   client = OpenWeatherMapClient(api_key="your_key")
   
   # Retrieve hourly forecast
   forecast = client.get_hourly_forecast(
       lat=48.8566,
       lon=2.3522,
       hours=48
   )
   
   # Convert to DataFrame
   df_meteo = pd.DataFrame(forecast)
   df_meteo['datetime'] = pd.to_datetime(df_meteo['timestamp'], unit='s')
   
   # Analysis
   temp_moyenne = df_meteo['temperature'].mean()
   temp_min = df_meteo['temperature'].min()
   temp_max = df_meteo['temperature'].max()
   
   print(f"Average temperature: {temp_moyenne:.1f}°C")
   print(f"Minimum temperature: {temp_min:.1f}°C")
   print(f"Maximum temperature: {temp_max:.1f}°C")

2.1.2. MeteoCiel - Historical Data and Degree Days
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MeteoCiel module provides access to historical data and calculates Unified Degree Days (UDD).

.. code-block:: python

   from energysystemmodels.MeteoCiel import MeteoCielClient
   
   # Initialize client
   client = MeteoCielClient()
   
   # Historical data
   historique = client.get_historical_data(
       station="Paris-Montsouris",
       date_debut="2024-01-01",
       date_fin="2024-12-31"
   )
   
   print(f"Number of days: {len(historique)}")

Calculating Unified Degree Days (UDD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.MeteoCiel import DJUCalculator
   import pandas as pd
   
   # Temperature data
   dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
   temperatures = pd.Series([5, 8, 10, 12, 15, 18, 20, 22, 25, 23] * 36, 
                           index=dates[:360])
   
   # Calculate UDD
   calculator = DJUCalculator(temperature_reference=18.0)
   
   # Heating UDD (UDD18)
   dju_chauffage = calculator.calculer_dju_chauffage(temperatures)
   
   # Cooling UDD (UDD21)
   calculator_clim = DJUCalculator(temperature_reference=21.0)
   dju_refroidissement = calculator_clim.calculer_dju_refroidissement(temperatures)
   
   print(f"Annual heating UDD: {dju_chauffage.sum():.0f}")
   print(f"Annual cooling UDD: {dju_refroidissement.sum():.0f}")

Example: Monthly UDD Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.MeteoCiel import DJUCalculator
   import pandas as pd
   
   # Simulate monthly average temperatures
   temperatures_mensuelles = pd.Series(
       [5, 6, 9, 12, 16, 19, 22, 21, 18, 13, 8, 5],
       index=pd.date_range('2024-01-01', periods=12, freq='MS')
   )
   
   calculator = DJUCalculator(temperature_reference=18.0)
   
   # Calculate monthly UDD
   dju_mensuels = calculator.calculer_dju_chauffage_mensuel(temperatures_mensuelles)
   
   print("Monthly heating UDD:")
   for mois, dju in dju_mensuels.items():
       print(f"  {mois}: {dju:.1f}")
   
   print(f"\nAnnual UDD: {dju_mensuels.sum():.0f}")

2.2. Solar Photovoltaic Production
-----------------------------------

The PV module uses pvlib to simulate photovoltaic production with high accuracy.

PV System Configuration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   
   # Define PV system
   pv_system = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,  # Due south
       inclinaison=30,   # degrees
       rendement=0.18,
       pertes_systeme=0.14
   )
   
   # Calculate annual production
   production_annuelle = pv_system.calculer_production_annuelle(annee=2024)
   
   print(f"Annual production: {production_annuelle:.0f} kWh")

Example: Hourly PV Production Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # PV system
   pv = PVSystem(
       latitude=43.6047,  # Toulouse
       longitude=1.4442,
       surface_m2=40,
       puissance_crete_kWc=6.5,
       orientation=180,
       inclinaison=35,
       rendement=0.19,
       pertes_systeme=0.12
   )
   
   # Hourly production over a year
   production_horaire = pv.calculer_production_horaire(
       date_debut='2024-01-01',
       date_fin='2024-12-31'
   )
   
   # Convert to DataFrame
   df_prod = pd.DataFrame({
       'datetime': production_horaire.index,
       'production_kW': production_horaire.values
   })
   
   # Statistics
   print(f"Total production: {df_prod['production_kW'].sum():.0f} kWh")
   print(f"Average production: {df_prod['production_kW'].mean():.2f} kW")
   print(f"Maximum power: {df_prod['production_kW'].max():.2f} kW")
   
   # Visualization
   df_prod_janvier = df_prod[df_prod['datetime'].dt.month == 1]
   plt.figure(figsize=(12, 6))
   plt.plot(df_prod_janvier['datetime'], df_prod_janvier['production_kW'])
   plt.title('PV Production - January 2024')
   plt.xlabel('Date')
   plt.ylabel('Power (kW)')
   plt.grid(True)
   plt.show()

Example: Orientation Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import numpy as np
   
   # Fixed parameters
   config_base = {
       'latitude': 48.8566,
       'longitude': 2.3522,
       'surface_m2': 30,
       'puissance_crete_kWc': 5.0,
       'rendement': 0.18,
       'pertes_systeme': 0.14
   }
   
   # Test different orientations and tilts
   orientations = np.arange(90, 270, 30)  # East to West
   inclinaisons = np.arange(0, 60, 10)
   
   resultats_optimisation = []
   
   for orient in orientations:
       for inclin in inclinaisons:
           pv = PVSystem(
               orientation=orient,
               inclinaison=inclin,
               **config_base
           )
           production = pv.calculer_production_annuelle(2024)
           
           resultats_optimisation.append({
               'orientation': orient,
               'inclinaison': inclin,
               'production_kWh': production
           })
   
   # Find optimum
   df_optim = pd.DataFrame(resultats_optimisation)
   optimum = df_optim.loc[df_optim['production_kWh'].idxmax()]
   
   print(f"Optimal configuration:")
   print(f"  Orientation: {optimum['orientation']:.0f}°")
   print(f"  Tilt: {optimum['inclinaison']:.0f}°")
   print(f"  Production: {optimum['production_kWh']:.0f} kWh/year")

Example: PV Production with Shading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem, ShadingProfile
   
   # Define shading profile
   ombrage = ShadingProfile()
   ombrage.add_obstacle(
       azimuth=180,      # Obstacle direction
       elevation=30,     # Angular height
       width=45          # Angular width
   )
   
   # PV system with shading
   pv = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,
       inclinaison=30,
       rendement=0.18,
       pertes_systeme=0.14,
       shading_profile=ombrage
   )
   
   # Compare with and without shading
   prod_avec_ombrage = pv.calculer_production_annuelle(2024)
   
   pv_sans_ombrage = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,
       inclinaison=30,
       rendement=0.18,
       pertes_systeme=0.14
   )
   prod_sans_ombrage = pv_sans_ombrage.calculer_production_annuelle(2024)
   
   perte_ombrage = (prod_sans_ombrage - prod_avec_ombrage) / prod_sans_ombrage * 100
   
   print(f"Production without shading: {prod_sans_ombrage:.0f} kWh")
   print(f"Production with shading: {prod_avec_ombrage:.0f} kWh")
   print(f"Loss due to shading: {perte_ombrage:.1f}%")

Example: PV Installation Sizing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import pandas as pd
   
   # Production target
   consommation_annuelle = 5000  # kWh
   taux_autoconsommation_vise = 0.70
   
   # Location
   lat, lon = 45.7640, 4.8357  # Lyon
   
   # Test different powers
   puissances_test = [3, 4, 5, 6, 7, 8, 9]  # kWc
   
   print(f"Annual consumption: {consommation_annuelle} kWh")
   print(f"Target self-consumption rate: {taux_autoconsommation_vise*100}%")
   print("\nSizing:")
   print("-" * 60)
   
   for puissance in puissances_test:
       surface = puissance / 0.18  # 18% efficiency
       
       pv = PVSystem(
           latitude=lat,
           longitude=lon,
           surface_m2=surface,
           puissance_crete_kWc=puissance,
           orientation=180,
           inclinaison=35,
           rendement=0.18,
           pertes_systeme=0.14
       )
       
       production = pv.calculer_production_annuelle(2024)
       taux_couverture = min(production / consommation_annuelle, 1.0)
       
       print(f"{puissance} kWc ({surface:.1f} m²) -> "
             f"Production: {production:.0f} kWh/year, "
             f"Coverage: {taux_couverture*100:.1f}%")

================================================================================
Section 3: Energy Transformation (Utilities)
================================================================================

3.1. Thermodynamic Cycles
--------------------------

The ThermodynamicCycles module allows modeling of refrigeration systems, heat pumps and thermodynamic cycles.

Basic Components
~~~~~~~~~~~~~~~~

**Source and Sink (Hot and Cold Sources)**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Source, Sink
   
   # Cold source (evaporator)
   source_froide = Source(
       temperature_K=273.15 + 5,  # 5°C
       debit_massique_kg_s=1.0
   )
   
   # Hot source (condenser)
   source_chaude = Sink(
       temperature_K=273.15 + 45,  # 45°C
       debit_massique_kg_s=1.0
   )

**Compressor**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Compressor
   
   compresseur = Compressor(
       rendement_isentropique=0.75,
       rendement_volumetrique=0.85,
       puissance_nominale_kW=10.0
   )

**Evaporator and Condenser**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Evaporator, Condenser
   
   evaporateur = Evaporator(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=6.0,
       coefficient_echange_W_m2K=1200,
       temperature_condensation_K=273.15 + 45
   )

**Expansion Valve**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import ExpansionValve
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.8
   )

Complete Example: Vapor Compression Refrigeration Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import (
       RefrigerationCycle, Source, Sink, Compressor, 
       Evaporator, Condenser, ExpansionValve
   )
   
   # Define components
   source_froide = Source(temperature_K=273.15 + 7, debit_massique_kg_s=0.5)
   source_chaude = Sink(temperature_K=273.15 + 40, debit_massique_kg_s=0.5)
   
   compresseur = Compressor(
       rendement_isentropique=0.70,
       rendement_volumetrique=0.80,
       puissance_nominale_kW=5.0
   )
   
   evaporateur = Evaporator(
       surface_echange_m2=4.0,
       coefficient_echange_W_m2K=800,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_condensation_K=273.15 + 42
   )
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.75
   )
   
   # Create cycle
   cycle = RefrigerationCycle(
       source=source_froide,
       sink=source_chaude,
       compressor=compresseur,
       evaporator=evaporateur,
       condenser=condenseur,
       expansion_valve=detendeur,
       refrigerant="R410A"
   )
   
   # Calculate performance
   resultats = cycle.calculate_performance()
   
   print(f"Cooling capacity: {resultats['cooling_capacity_kW']:.2f} kW")
   print(f"Power input: {resultats['power_input_kW']:.2f} kW")
   print(f"COP: {resultats['COP']:.2f}")
   print(f"EER: {resultats['EER']:.2f}")

Example: Air-Water Heat Pump
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import HeatPump
   
   # Heat pump configuration
   pac = HeatPump(
       type_source="air",
       type_sink="eau",
       puissance_thermique_nominale_kW=12,
       temperature_source_K=273.15 + 7,
       temperature_sink_K=273.15 + 35,
       refrigerant="R32",
       rendement_compresseur=0.75
   )
   
   # Nominal performance
   perf_nominale = pac.calculate_performance()
   
   print(f"Heating capacity: {perf_nominale['heating_capacity_kW']:.2f} kW")
   print(f"Electrical power: {perf_nominale['power_input_kW']:.2f} kW")
   print(f"COP: {perf_nominale['COP']:.2f}")
   
   # Performance according to outdoor temperature
   temperatures_ext = [-7, -2, 2, 7, 12]
   
   print("\nPerformance by outdoor temperature:")
   for t_ext in temperatures_ext:
       pac.set_source_temperature(273.15 + t_ext)
       perf = pac.calculate_performance()
       print(f"  {t_ext:3.0f}°C : COP = {perf['COP']:.2f}, "
             f"Power = {perf['heating_capacity_kW']:.2f} kW")

================================================================================
Section 4: Energy Distribution
================================================================================

4.1. Heat Transfer
------------------

4.1.1. CompositeWall - Multilayer Wall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CompositeWall module allows calculation of heat transfers through multilayer walls.

.. image:: _static/001_heat_transfer_composite_wall.png
   :alt: Composite wall diagram
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.HeatTransfer import CompositeWall, Layer
   
   # Define wall layers
   couche_interieure = Layer(
       nom="Plaster",
       epaisseur_m=0.013,
       conductivite_W_mK=0.35
   )
   
   couche_isolation = Layer(
       nom="Glass wool",
       epaisseur_m=0.20,
       conductivite_W_mK=0.04
   )
   
   couche_exterieure = Layer(
       nom="Brick",
       epaisseur_m=0.10,
       conductivite_W_mK=0.80
   )
   
   # Create composite wall
   paroi = CompositeWall(
       surface_m2=15.0,
       layers=[couche_interieure, couche_isolation, couche_exterieure],
       h_int=7.7,  # Internal exchange coefficient W/m²K
       h_ext=25.0  # External exchange coefficient W/m²K
   )
   
   # Calculate thermal resistance
   R_totale = paroi.resistance_thermique_totale()
   U = paroi.coefficient_transmission_thermique()
   
   print(f"Total thermal resistance: {R_totale:.3f} m².K/W")
   print(f"U coefficient: {U:.3f} W/m².K")
   
   # Heat flux for a temperature difference
   T_int = 20  # °C
   T_ext = -5  # °C
   flux_thermique = paroi.calculer_flux_thermique(T_int, T_ext)
   
   print(f"Heat flux: {flux_thermique:.2f} W")
   print(f"Heat losses: {flux_thermique/1000:.2f} kW")

4.1.2. PlateHeatTransfer - Plate Heat Exchanger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/PlateHeatTransfer.png
   :alt: Plate heat exchanger
   :align: center
   :width: 500px

.. code-block:: python

   from energysystemmodels.HeatTransfer import PlateHeatExchanger
   
   # Plate heat exchanger
   echangeur = PlateHeatExchanger(
       nombre_plaques=30,
       surface_echange_par_plaque_m2=0.35,
       epaisseur_plaque_mm=0.6,
       espacement_plaques_mm=3.0,
       materiau="acier_inox"
   )
   
   # Inlet conditions
   # Hot circuit
   T_chaud_entree = 80  # °C
   debit_chaud = 2.0    # kg/s
   
   # Cold circuit
   T_froid_entree = 15  # °C
   debit_froid = 1.8    # kg/s
   
   # Calculate efficiency and outlet temperatures
   resultats = echangeur.calculate_performance(
       T_hot_in=T_chaud_entree,
       T_cold_in=T_froid_entree,
       m_dot_hot=debit_chaud,
       m_dot_cold=debit_froid
   )
   
   print(f"Efficiency: {resultats['efficacite']:.1%}")
   print(f"Hot circuit outlet temperature: {resultats['T_hot_out']:.1f}°C")
   print(f"Cold circuit outlet temperature: {resultats['T_cold_out']:.1f}°C")
   print(f"Exchanged power: {resultats['puissance_kW']:.2f} kW")
   print(f"Hot circuit pressure drop: {resultats['delta_P_hot_Pa']:.0f} Pa")
   print(f"Cold circuit pressure drop: {resultats['delta_P_cold_Pa']:.0f} Pa")

4.1.3. PipeInsulation - Pipe Insulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.HeatTransfer import PipeInsulation
   
   # Insulated pipe
   tuyau = PipeInsulation(
       diametre_interieur_mm=50,
       diametre_exterieur_mm=60,
       epaisseur_isolation_mm=30,
       longueur_m=50,
       conductivite_tuyau_W_mK=50,      # Steel
       conductivite_isolation_W_mK=0.04, # Mineral wool
       temperature_fluide_C=80,
       temperature_ambiante_C=20
   )
   
   # Calculate heat losses
   pertes = tuyau.calculer_pertes_thermiques()
   
   print(f"Linear heat losses: {pertes['pertes_lineiques_W_m']:.2f} W/m")
   print(f"Total heat losses: {pertes['pertes_totales_W']:.2f} W")
   print(f"Total heat losses: {pertes['pertes_totales_W']/1000:.2f} kW")
   
   # Outer surface temperature
   T_surface = tuyau.temperature_surface_exterieure()
   print(f"Outer surface temperature: {T_surface:.1f}°C")

Example: Insulation Thickness Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.HeatTransfer import PipeInsulation
   import numpy as np
   
   # Fixed parameters
   diametre_tuyau = 100  # mm
   longueur = 100        # m
   T_fluide = 90         # °C
   T_ambient = 20        # °C
   heures_fonctionnement = 6000  # h/year
   cout_energie = 0.10   # €/kWh
   
   # Test different insulation thicknesses
   epaisseurs_test = np.arange(10, 100, 10)  # mm
   
   print("Insulation thickness optimization:")
   print("-" * 80)
   print(f"{'Thickness (mm)':<15} {'Losses (kW)':<15} {'Annual cost (€)':<20}")
   print("-" * 80)
   
   for epaisseur in epaisseurs_test:
       tuyau = PipeInsulation(
           diametre_interieur_mm=diametre_tuyau,
           diametre_exterieur_mm=diametre_tuyau + 5,
           epaisseur_isolation_mm=epaisseur,
           longueur_m=longueur,
           conductivite_tuyau_W_mK=50,
           conductivite_isolation_W_mK=0.035,
           temperature_fluide_C=T_fluide,
           temperature_ambiante_C=T_ambient
       )
       
       pertes = tuyau.calculer_pertes_thermiques()
       pertes_kW = pertes['pertes_totales_W'] / 1000
       energie_annuelle_kWh = pertes_kW * heures_fonctionnement
       cout_annuel = energie_annuelle_kWh * cout_energie
       
       print(f"{epaisseur:<15.0f} {pertes_kW:<15.3f} {cout_annuel:<20.2f}")

4.2. Hydraulics
---------------

4.2.1. StraightPipe - Straight Pipe and Pressure Losses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_hydraulic_straight_pipe.png
   :alt: Straight pipe diagram
   :align: center
   :width: 500px

.. code-block:: python

   from energysystemmodels.Hydraulic import StraightPipe
   
   # Define pipe
   tuyau = StraightPipe(
       longueur_m=100,
       diametre_mm=50,
       rugosite_mm=0.05,  # New steel
       materiau="acier"
   )
   
   # Fluid: water at 20°C
   debit_m3_h = 10.0
   
   # Calculate pressure losses
   resultats = tuyau.calculer_pertes_charge(
       debit_m3_h=debit_m3_h,
       temperature_C=20
   )
   
   print(f"Flow rate: {debit_m3_h} m³/h")
   print(f"Velocity: {resultats['vitesse_m_s']:.2f} m/s")
   print(f"Reynolds number: {resultats['reynolds']:.0f}")
   print(f"Regime: {resultats['regime']}")
   print(f"Linear pressure losses: {resultats['pertes_lineaires_Pa']:.1f} Pa")
   print(f"Linear pressure losses: {resultats['pertes_lineaires_Pa']/100:.1f} mWC")

Network Curve
~~~~~~~~~~~~~

.. image:: _static/004_hydraulic_straight_pipe_courbe_reseau.png
   :alt: Hydraulic network curve
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.Hydraulic import StraightPipe
   import numpy as np
   import matplotlib.pyplot as plt
   
   tuyau = StraightPipe(
       longueur_m=150,
       diametre_mm=65,
       rugosite_mm=0.05,
       materiau="acier"
   )
   
   # Calculate network curve
   debits = np.linspace(0.1, 30, 50)  # m³/h
   pertes = []
   
   for debit in debits:
       resultats = tuyau.calculer_pertes_charge(debit, 20)
       pertes.append(resultats['pertes_lineaires_Pa'] / 100)  # Convert to mWC
   
   # Plot curve
   plt.figure(figsize=(10, 6))
   plt.plot(debits, pertes, linewidth=2)
   plt.xlabel('Flow rate (m³/h)')
   plt.ylabel('Pressure loss (mWC)')
   plt.title('Hydraulic network curve')
   plt.grid(True, alpha=0.3)
   plt.show()

4.2.2. TA_Valve - Hydraulic Balancing Valve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_TA_valve.png
   :alt: TA valve
   :align: center
   :width: 400px

.. code-block:: python

   from energysystemmodels.Hydraulic import TA_Valve
   
   # TA valve DN50
   vanne = TA_Valve(
       dn=50,
       kvs=25.0,  # Kvs coefficient
       position=3  # Setting position (1-7)
   )
   
   # Calculate Kv at this position
   kv = vanne.get_kv_at_position(position=3)
   print(f"Kv at position 3: {kv:.2f}")
   
   # Desired flow rate
   debit_souhaite = 5.0  # m³/h
   
   # Calculate pressure drop
   delta_P = vanne.calculer_perte_charge(debit_m3_h=debit_souhaite)
   print(f"Pressure drop for {debit_souhaite} m³/h: {delta_P:.1f} Pa")
   print(f"Pressure drop: {delta_P/100:.2f} mWC")
   
   # Find position for given flow rate and pressure drop
   delta_P_disponible = 5000  # Pa
   position_requise = vanne.trouver_position_pour_debit(
       debit_m3_h=debit_souhaite,
       delta_P_Pa=delta_P_disponible
   )
   print(f"Recommended position: {position_requise}")

Valve Characteristic Curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_TA_valve-courbe-reseau.png
   :alt: TA valve characteristic curve
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.Hydraulic import TA_Valve
   import numpy as np
   import matplotlib.pyplot as plt
   
   vanne = TA_Valve(dn=50, kvs=25.0)
   
   # Plot curves for different positions
   debits = np.linspace(0.5, 15, 50)
   
   plt.figure(figsize=(10, 6))
   
   for position in range(1, 8):
       pertes = []
       vanne.position = position
       
       for debit in debits:
           delta_P = vanne.calculer_perte_charge(debit)
           pertes.append(delta_P / 100)  # In mWC
       
       plt.plot(debits, pertes, label=f'Position {position}', linewidth=2)
   
   plt.xlabel('Flow rate (m³/h)')
   plt.ylabel('Pressure drop (mWC)')
   plt.title('Characteristic curves - TA valve DN50')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.show()

4.3. Air Duct Networks
-----------------------

4.3.1. AirDuct - Air Ducts and Aeraulic Pressure Losses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct
   
   # Rectangular duct
   gaine = AirDuct(
       type_section="rectangulaire",
       largeur_mm=400,
       hauteur_mm=200,
       longueur_m=50,
       rugosite_mm=0.1,  # Galvanized steel
       materiau="acier_galvanise"
   )
   
   # Air flow rate
   debit_air = 3000  # m³/h
   temperature = 20   # °C
   
   # Calculate pressure losses
   resultats = gaine.calculer_pertes_charge(
       debit_m3_h=debit_air,
       temperature_C=temperature
   )
   
   print(f"Flow rate: {debit_air} m³/h")
   print(f"Velocity: {resultats['vitesse_m_s']:.2f} m/s")
   print(f"Hydraulic diameter: {resultats['diametre_hydraulique_mm']:.1f} mm")
   print(f"Linear pressure losses: {resultats['pertes_lineaires_Pa']:.2f} Pa")
   print(f"Total pressure losses: {resultats['pertes_totales_Pa']:.2f} Pa")

Circular Duct
~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct
   
   # Circular duct
   gaine_circ = AirDuct(
       type_section="circulaire",
       diametre_mm=315,
       longueur_m=30,
       rugosite_mm=0.05,
       materiau="acier_galvanise"
   )
   
   # Calculate for different flow rates
   debits_test = [1000, 2000, 3000, 4000]
   
   print("Circular duct Ø315 mm performance:")
   print("-" * 70)
   print(f"{'Flow rate (m³/h)':<15} {'Velocity (m/s)':<15} {'ΔP (Pa)':<15}")
   print("-" * 70)
   
   for debit in debits_test:
       res = gaine_circ.calculer_pertes_charge(debit, 20)
       print(f"{debit:<15.0f} {res['vitesse_m_s']:<15.2f} {res['pertes_lineaires_Pa']:<15.2f}")

Aeraulic Singularities
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct, Singularity
   
   gaine = AirDuct(
       type_section="circulaire",
       diametre_mm=250,
       longueur_m=20,
       materiau="acier_galvanise"
   )
   
   # Add singularities
   coude_90 = Singularity(type="coude_90", coefficient_perte=0.9)
   te_divergent = Singularity(type="te_divergent", coefficient_perte=1.3)
   registre = Singularity(type="registre", coefficient_perte=0.5)
   
   gaine.add_singularity(coude_90)
   gaine.add_singularity(te_divergent)
   gaine.add_singularity(registre)
   
   # Calculate total losses
   debit = 2500  # m³/h
   resultats = gaine.calculer_pertes_charge_totales(debit, 20)
   
   print(f"Linear losses: {resultats['pertes_lineaires_Pa']:.1f} Pa")
   print(f"Singular losses: {resultats['pertes_singulieres_Pa']:.1f} Pa")
   print(f"Total losses: {resultats['pertes_totales_Pa']:.1f} Pa")

================================================================================
Section 5: End Uses of Energy
================================================================================

5.1. AHU Module - Air Handling Units (AHU)
-------------------------------------------

The AHU module allows modeling of air handling units with their different components.

5.1.1. FreshAir - Fresh Air and Recirculated Air Mixing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/003_ahu_fresh_air.png
   :alt: Fresh air mixing diagram
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.AHU import FreshAir
   
   # Mixing configuration
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=3000,
       debit_air_recycle_m3_h=7000,
       temperature_ext_C=5,
       humidite_ext_pct=80,
       temperature_reprise_C=22,
       humidite_reprise_pct=45
   )
   
   # Calculate mixture state
   etat_melange = fresh_air.calculer_etat_melange()
   
   print(f"Mixture temperature: {etat_melange['temperature_C']:.1f}°C")
   print(f"Relative humidity: {etat_melange['humidite_relative_pct']:.1f}%")
   print(f"Absolute humidity: {etat_melange['humidite_absolue_g_kg']:.2f} g/kg")
   print(f"Enthalpy: {etat_melange['enthalpie_kJ_kg']:.2f} kJ/kg")

Psychrometric Chart
~~~~~~~~~~~~~~~~~~~

.. image:: _static/003_ahu_fresh_air_figure1.png
   :alt: Psychrometric chart
   :align: center
   :width: 700px

.. code-block:: python

   from energysystemmodels.AHU import FreshAir
   import matplotlib.pyplot as plt
   
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=3000,
       debit_air_recycle_m3_h=7000,
       temperature_ext_C=5,
       humidite_ext_pct=80,
       temperature_reprise_C=22,
       humidite_reprise_pct=45
   )
   
   # Plot psychrometric chart
   fig = fresh_air.plot_psychrometric_chart()
   plt.show()

5.1.2. HeatingCoil - Heating Coil
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import HeatingCoil
   
   # Hot water heating coil
   batterie = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=50,
       temperature_entree_eau_C=80,
       temperature_sortie_eau_C=60,
       efficacite=0.85
   )
   
   # Air to heat
   debit_air = 10000  # m³/h
   T_air_entree = 10  # °C
   
   # Calculate heating
   resultats = batterie.calculer_chauffage(
       debit_air_m3_h=debit_air,
       temperature_air_entree_C=T_air_entree
   )
   
   print(f"Heating power: {resultats['puissance_kW']:.2f} kW")
   print(f"Air outlet temperature: {resultats['temperature_air_sortie_C']:.1f}°C")
   print(f"Water flow rate: {resultats['debit_eau_m3_h']:.2f} m³/h")

Example: Heating Coil Sizing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import HeatingCoil
   
   # Design conditions
   debit_air = 15000       # m³/h
   T_air_entree = 5        # °C
   T_air_sortie_voulue = 18  # °C
   T_eau_aller = 80        # °C
   T_eau_retour = 60       # °C
   
   # Calculate required power
   rho_air = 1.2  # kg/m³
   cp_air = 1.005  # kJ/kg.K
   
   debit_massique_air = debit_air / 3600 * rho_air  # kg/s
   puissance_requise = debit_massique_air * cp_air * (T_air_sortie_voulue - T_air_entree)
   
   print(f"Required power: {puissance_requise:.2f} kW")
   
   # Create coil with this power
   batterie = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=puissance_requise,
       temperature_entree_eau_C=T_eau_aller,
       temperature_sortie_eau_C=T_eau_retour,
       efficacite=0.90
   )
   
   # Verify performance
   resultats = batterie.calculer_chauffage(debit_air, T_air_entree)
   print(f"Air outlet temperature obtained: {resultats['temperature_air_sortie_C']:.1f}°C")

5.1.3. Humidifier - Humidifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import Humidifier
   
   # Steam humidifier
   humidificateur = Humidifier(
       type_humidificateur="vapeur",
       capacite_kg_h=30,
       efficacite=0.95
   )
   
   # Air to humidify
   debit_air = 10000  # m³/h
   T_air = 20         # °C
   HR_entree = 30     # %
   HR_souhaitee = 50  # %
   
   # Calculate humidification
   resultats = humidificateur.calculer_humidification(
       debit_air_m3_h=debit_air,
       temperature_C=T_air,
       humidite_relative_entree_pct=HR_entree,
       humidite_relative_sortie_pct=HR_souhaitee
   )
   
   print(f"Required steam flow rate: {resultats['debit_vapeur_kg_h']:.2f} kg/h")
   print(f"Power consumed: {resultats['puissance_kW']:.2f} kW")
   print(f"Inlet absolute humidity: {resultats['humidite_abs_entree_g_kg']:.2f} g/kg")
   print(f"Outlet absolute humidity: {resultats['humidite_abs_sortie_g_kg']:.2f} g/kg")

Complete Example: Complete AHU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import FreshAir, HeatingCoil, CoolingCoil, Humidifier, Fan
   
   # Winter outdoor conditions
   T_ext = 5      # °C
   HR_ext = 80    # %
   
   # Indoor conditions
   T_reprise = 22  # °C
   HR_reprise = 45  # %
   
   # Supply setpoint
   T_soufflage = 18  # °C
   HR_soufflage = 50  # %
   
   # Flow rates
   debit_air_neuf = 3000    # m³/h
   debit_air_recycle = 7000  # m³/h
   debit_total = debit_air_neuf + debit_air_recycle
   
   print("=== WINTER AHU SIMULATION ===\n")
   
   # 1. Fresh air / recirculated air mixing
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=debit_air_neuf,
       debit_air_recycle_m3_h=debit_air_recycle,
       temperature_ext_C=T_ext,
       humidite_ext_pct=HR_ext,
       temperature_reprise_C=T_reprise,
       humidite_reprise_pct=HR_reprise
   )
   
   etat_melange = fresh_air.calculer_etat_melange()
   print(f"1. After mixing:")
   print(f"   T = {etat_melange['temperature_C']:.1f}°C")
   print(f"   RH = {etat_melange['humidite_relative_pct']:.1f}%\n")
   
   # 2. Heating
   batterie_chaude = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=80,
       temperature_entree_eau_C=80,
       temperature_sortie_eau_C=60,
       efficacite=0.90
   )
   
   resultats_chauffage = batterie_chaude.calculer_chauffage(
       debit_air_m3_h=debit_total,
       temperature_air_entree_C=etat_melange['temperature_C']
   )
   
   print(f"2. After heating coil:")
   print(f"   T = {resultats_chauffage['temperature_air_sortie_C']:.1f}°C")
   print(f"   Power = {resultats_chauffage['puissance_kW']:.2f} kW\n")
   
   # 3. Humidification
   humidificateur = Humidifier(
       type_humidificateur="vapeur",
       capacite_kg_h=50,
       efficacite=0.95
   )
   
   # Calculate RH after heating (approximation)
   HR_apres_chauffage = etat_melange['humidite_relative_pct'] * \
                        etat_melange['temperature_C'] / \
                        resultats_chauffage['temperature_air_sortie_C']
   
   resultats_humidif = humidificateur.calculer_humidification(
       debit_air_m3_h=debit_total,
       temperature_C=resultats_chauffage['temperature_air_sortie_C'],
       humidite_relative_entree_pct=HR_apres_chauffage,
       humidite_relative_sortie_pct=HR_soufflage
   )
   
   print(f"3. After humidification:")
   print(f"   RH = {HR_soufflage}%")
   print(f"   Steam = {resultats_humidif['debit_vapeur_kg_h']:.2f} kg/h")
   print(f"   Power = {resultats_humidif['puissance_kW']:.2f} kW\n")
   
   # 4. Fan
   ventilateur = Fan(
       type_ventilateur="centrifuge",
       debit_nominal_m3_h=debit_total,
       pression_statique_Pa=800,
       rendement=0.75
   )
   
   puissance_ventilateur = ventilateur.calculer_puissance()
   
   print(f"4. Fan:")
   print(f"   Power = {puissance_ventilateur:.2f} kW\n")
   
   # Total energy balance
   print("=== ENERGY BALANCE ===")
   puissance_totale = (resultats_chauffage['puissance_kW'] + 
                       resultats_humidif['puissance_kW'] + 
                       puissance_ventilateur)
   print(f"Total AHU power: {puissance_totale:.2f} kW")

5.2. PinchAnalysis Module - Pinch Analysis
-------------------------------------------

Pinch analysis allows optimization of heat exchanger networks and minimizing energy consumption.

Example: Simple Pinch Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   
   # Define hot streams
   hot_streams = [
       Stream(name="H1", T_in=180, T_out=60, heat_flow=300),  # kW
       Stream(name="H2", T_in=150, T_out=40, heat_flow=200)
   ]
   
   # Define cold streams
   cold_streams = [
       Stream(name="C1", T_in=20, T_out=135, heat_flow=250),
       Stream(name="C2", T_in=80, T_out=140, heat_flow=150)
   ]
   
   # Create Pinch analysis
   pinch = PinchAnalysis(
       hot_streams=hot_streams,
       cold_streams=cold_streams,
       delta_T_min=10  # Minimum pinch 10°C
   )
   
   # Calculate results
   resultats = pinch.analyze()
   
   print(f"Pinch temperature: {resultats['pinch_temperature']}°C")
   print(f"Minimum heating requirement: {resultats['hot_utility_min']:.0f} kW")
   print(f"Minimum cooling requirement: {resultats['cold_utility_min']:.0f} kW")
   print(f"Possible heat recovery: {resultats['heat_recovery']:.0f} kW")
   print(f"Potential savings: {resultats['energy_savings_pct']:.1f}%")

Composite Curves
~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt
   
   # Use previous analysis
   fig = pinch.plot_composite_curves()
   plt.show()

Complete Example: Industrial Process Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   
   # Industrial process with 4 hot streams and 3 cold streams
   hot_streams = [
       Stream(name="Reactor outlet", T_in=220, T_out=40, heat_flow=500),
       Stream(name="Distillation", T_in=180, T_out=60, heat_flow=400),
       Stream(name="Product cooling", T_in=150, T_out=80, heat_flow=300),
       Stream(name="Exhaust gases", T_in=350, T_out=120, heat_flow=250)
   ]
   
   cold_streams = [
       Stream(name="Feed preheating", T_in=20, T_out=180, heat_flow=450),
       Stream(name="Reboiler", T_in=140, T_out=145, heat_flow=350),
       Stream(name="Process water", T_in=15, T_out=90, heat_flow=200)
   ]
   
   # Analysis with different pinches
   delta_T_values = [5, 10, 15, 20]
   
   print("Pinch sensitivity analysis:")
   print("-" * 80)
   print(f"{'ΔTmin (°C)':<12} {'Heating (kW)':<18} {'Cooling (kW)':<18} {'Recovery (%)':<15}")
   print("-" * 80)
   
   for delta_T in delta_T_values:
       pinch = PinchAnalysis(hot_streams, cold_streams, delta_T_min=delta_T)
       resultats = pinch.analyze()
       
       print(f"{delta_T:<12.0f} {resultats['hot_utility_min']:<18.0f} "
             f"{resultats['cold_utility_min']:<18.0f} "
             f"{resultats['energy_savings_pct']:<15.1f}")
   
   # Detailed analysis with ΔTmin = 10°C
   print("\n=== Optimal configuration (ΔTmin = 10°C) ===")
   pinch_optimal = PinchAnalysis(hot_streams, cold_streams, delta_T_min=10)
   resultats_optimal = pinch_optimal.analyze()
   
   print(f"\nEnergy balance:")
   print(f"  Available heat: {resultats_optimal['total_hot_available']:.0f} kW")
   print(f"  Required heat: {resultats_optimal['total_cold_required']:.0f} kW")
   print(f"  Internal recovery: {resultats_optimal['heat_recovery']:.0f} kW")
   print(f"  Required hot utility: {resultats_optimal['hot_utility_min']:.0f} kW")
   print(f"  Required cold utility: {resultats_optimal['cold_utility_min']:.0f} kW")
   
   # Plot composite curves
   fig = pinch_optimal.plot_composite_curves()
   plt.show()

5.3. IPMVP Module - International Performance Measurement and Verification Protocol
------------------------------------------------------------------------------------

The IPMVP module allows measurement and verification of energy savings according to the international protocol.

5.3.1. Daily Regression Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   import numpy as np
   
   # Generate baseline reference data
   dates_baseline = pd.date_range('2023-01-01', '2023-12-31', freq='D')
   temperatures = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates_baseline)) / 365)
   
   # Consumption correlated to temperature
   consommation_baseline = 1000 + 50 * (20 - temperatures) * (temperatures < 20)
   
   df_baseline = pd.DataFrame({
       'date': dates_baseline,
       'temperature': temperatures,
       'consommation_kWh': consommation_baseline
   })
   
   # Create IPMVP model
   model = IPMVPModel(periode_baseline=df_baseline)
   
   # Train model
   model.fit(variable_independante='temperature', variable_dependante='consommation_kWh')
   
   print(f"Model R²: {model.r_squared:.3f}")
   print(f"RMSE: {model.rmse:.2f} kWh")

Calculating Savings
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Reporting period data (after works)
   dates_reporting = pd.date_range('2024-01-01', '2024-12-31', freq='D')
   temperatures_reporting = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates_reporting)) / 365)
   
   # Actual consumption after works (20% reduction)
   consommation_reporting = (1000 + 50 * (20 - temperatures_reporting) * 
                              (temperatures_reporting < 20)) * 0.80
   
   df_reporting = pd.DataFrame({
       'date': dates_reporting,
       'temperature': temperatures_reporting,
       'consommation_kWh': consommation_reporting
   })
   
   # Calculate savings
   economies = model.calculer_economies(df_reporting)
   
   print(f"\n=== IPMVP RESULTS ===")
   print(f"Adjusted baseline consumption: {economies['baseline_ajustee_kWh']:.0f} kWh")
   print(f"Actual consumption: {economies['consommation_reelle_kWh']:.0f} kWh")
   print(f"Savings achieved: {economies['economies_kWh']:.0f} kWh")
   print(f"Savings rate: {economies['taux_economie_pct']:.1f}%")
   print(f"Uncertainty: ±{economies['incertitude_pct']:.1f}%")

5.3.2. Weekly Model
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   
   # Weekly data
   dates_hebdo = pd.date_range('2023-01-01', '2023-12-31', freq='W')
   
   df_hebdo_baseline = pd.DataFrame({
       'semaine': range(len(dates_hebdo)),
       'temperature_moy': 15 + 8 * np.sin(2 * np.pi * np.arange(len(dates_hebdo)) / 52),
       'production_unite': 1000 + 200 * np.random.random(len(dates_hebdo)),
       'consommation_kWh': 7000 + np.random.normal(0, 500, len(dates_hebdo))
   })
   
   # Multi-variable model
   model_hebdo = IPMVPModel(periode_baseline=df_hebdo_baseline)
   model_hebdo.fit(
       variables_independantes=['temperature_moy', 'production_unite'],
       variable_dependante='consommation_kWh'
   )
   
   print(f"Weekly model R²: {model_hebdo.r_squared:.3f}")

5.3.3. Monthly Model
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   
   # Monthly consumption data
   mois = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
   
   df_mensuel = pd.DataFrame({
       'mois': mois,
       'dju_chauffage': [450, 380, 310, 180, 80, 20, 0, 0, 50, 150, 280, 400],
       'consommation_gaz_kWh': [45000, 38000, 31000, 18000, 8000, 2000, 
                                 0, 0, 5000, 15000, 28000, 40000]
   })
   
   # Monthly model
   model_mensuel = IPMVPModel(periode_baseline=df_mensuel)
   model_mensuel.fit(
       variable_independante='dju_chauffage',
       variable_dependante='consommation_gaz_kWh'
   )
   
   print(f"\nMonthly model:")
   print(f"R²: {model_mensuel.r_squared:.3f}")
   print(f"UDD coefficient: {model_mensuel.coefficients['dju_chauffage']:.2f} kWh/UDD")

Complete IPMVP Report
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPReport
   
   # Generate complete report
   rapport = IPMVPReport(
       model=model,
       periode_baseline=df_baseline,
       periode_reporting=df_reporting,
       description_projet="Building envelope insulation and HVAC optimization",
       cout_travaux=150000,
       cout_energie=0.10  # €/kWh
   )
   
   # Generate report
   rapport.generer_rapport(fichier='rapport_ipmvp.pdf')
   
   # Display summary
   print(rapport.get_summary())

5.4. Building RC Model
-----------------------

The RC (Resistance-Capacity) model allows simulation of the dynamic thermal behavior of a building.

Simple RC Model (1R1C)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.BuildingModel import RC_Model
   
   # Building parameters
   modele_rc = RC_Model(
       resistance_thermique=0.01,  # K/W
       capacite_thermique=50e6,     # J/K
       surface_vitree_m2=30,
       orientation_vitrage=180,     # South
       apports_internes_W=500
   )
   
   # Initial conditions
   T_interieure_initiale = 20  # °C
   
   # 24-hour simulation
   import numpy as np
   
   heures = np.arange(0, 24, 1)
   temperatures_ext = 10 + 5 * np.sin(2 * np.pi * (heures - 6) / 24)
   
   temperatures_int = []
   T_int = T_interieure_initiale
   
   for h, T_ext in zip(heures, temperatures_ext):
       T_int = modele_rc.simuler_pas_de_temps(
           T_interieure=T_int,
           T_exterieure=T_ext,
           rayonnement_solaire_W_m2=max(0, 500 * np.sin(np.pi * (h - 6) / 12)),
           dt_seconds=3600
       )
       temperatures_int.append(T_int)
   
   # Display
   import matplotlib.pyplot as plt
   
   plt.figure(figsize=(12, 6))
   plt.plot(heures, temperatures_ext, label='Outdoor T°', linewidth=2)
   plt.plot(heures, temperatures_int, label='Indoor T°', linewidth=2)
   plt.xlabel('Hour')
   plt.ylabel('Temperature (°C)')
   plt.title('RC 1R1C Model - Temperature Evolution')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.show()

Advanced RC Model (2R2C)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.BuildingModel import RC_Model_Advanced
   
   # 2R2C model with heavy and light inertia
   modele_2r2c = RC_Model_Advanced(
       R_envelope=0.005,      # K/W - Envelope resistance
       R_internal=0.003,      # K/W - Internal resistance
       C_light=10e6,          # J/K - Light capacity (air)
       C_heavy=100e6,         # J/K - Heavy capacity (structure)
       surface_vitree_m2=40,
       apports_internes_W=800
   )
   
   # Simulation with heating
   T_consigne = 20  # °C
   
   resultats_simulation = modele_2r2c.simuler_periode(
       T_ext_serie=temperatures_ext,
       T_consigne=T_consigne,
       puissance_chauffage_max_W=5000,
       dt_seconds=3600
   )
   
   print(f"Heating consumption: {resultats_simulation['energie_chauffage_kWh']:.1f} kWh")
   print(f"Average temperature: {np.mean(resultats_simulation['temperatures_int']):.1f}°C")

================================================================================
Section 6: Detailed Modules - Complete Reference
================================================================================

For detailed documentation of each module, consult the following pages:

.. toctree::
   :maxdepth: 2
   :caption: Available modules
   
   modules/turpe
   modules/cee
   modules/openweathermap
   modules/meteociel
   modules/pv
   modules/thermodynamic_cycles
   modules/heat_transfer
   modules/hydraulic
   modules/ahu
   modules/pinch_analysis
   modules/ipmvp
   modules/building_model

================================================================================
Section 7: Advanced Concepts
================================================================================

7.1. Error and Exception Handling
----------------------------------

.. code-block:: python

   from energysystemmodels.exceptions import (
       EnergySystemError,
       ConfigurationError,
       CalculationError,
       DataError
   )
   
   try:
       pv_system = PVSystem(
           latitude=48.8566,
           longitude=2.3522,
           puissance_crete_kWc=-5.0  # Error: negative value
       )
   except ConfigurationError as e:
       print(f"Configuration error: {e}")
   
   try:
       production = pv_system.calculer_production_annuelle(2024)
   except CalculationError as e:
       print(f"Calculation error: {e}")

7.2. External API Connections
------------------------------

.. code-block:: python

   from energysystemmodels.utils import APIConnector
   
   # Configure proxy if necessary
   connector = APIConnector(
       proxy_url="http://proxy.entreprise.com:8080",
       timeout=30
   )
   
   # Use with OpenWeatherMap
   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   
   client = OpenWeatherMapClient(
       api_key="your_key",
       connector=connector
   )

7.3. Data Visualization and Export
-----------------------------------

.. code-block:: python

   from energysystemmodels.visualization import EnergyPlotter
   import pandas as pd
   
   # Consumption data
   dates = pd.date_range('2024-01-01', periods=365, freq='D')
   consommation = pd.Series(
       1000 + 500 * np.sin(2 * np.pi * np.arange(365) / 365),
       index=dates
   )
   
   # Create visualizer
   plotter = EnergyPlotter()
   
   # Consumption chart
   fig = plotter.plot_consumption_profile(
       data=consommation,
       title="Annual consumption profile",
       xlabel="Date",
       ylabel="Consumption (kWh)"
   )
   
   # Export in different formats
   plotter.export(fig, 'consommation.png', format='png', dpi=300)
   plotter.export(fig, 'consommation.pdf', format='pdf')
   plotter.export(fig, 'consommation.svg', format='svg')

7.4. Parallelized Calculations for Large Simulations
-----------------------------------------------------

.. code-block:: python

   from energysystemmodels.utils import ParallelCalculator
   import numpy as np
   
   # Simulation of many configurations
   def simuler_configuration(params):
       orientation, inclinaison = params
       pv = PVSystem(
           latitude=48.8566,
           longitude=2.3522,
           surface_m2=30,
           puissance_crete_kWc=5.0,
           orientation=orientation,
           inclinaison=inclinaison,
           rendement=0.18
       )
       return pv.calculer_production_annuelle(2024)
   
   # Generate all combinations
   orientations = np.arange(0, 360, 15)
   inclinaisons = np.arange(0, 90, 10)
   configurations = [(o, i) for o in orientations for i in inclinaisons]
   
   # Calculate in parallel
   calculator = ParallelCalculator(n_jobs=-1)  # All cores
   resultats = calculator.map(simuler_configuration, configurations)
   
   print(f"Calculated {len(resultats)} configurations in parallel")

================================================================================
Section 8: Imports and Dependencies
================================================================================

Essential Imports
-----------------

.. code-block:: python

   # Base modules
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # EnergySystemModels modules by domain
   
   # Billing and finance
   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   from energysystemmodels.CEE import *
   
   # Meteorological data
   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   from energysystemmodels.MeteoCiel import MeteoCielClient, DJUCalculator
   
   # Energy production
   from energysystemmodels.PV import PVSystem, ShadingProfile
   
   # Thermodynamics
   from energysystemmodels.ThermodynamicCycles import (
       RefrigerationCycle, HeatPump, Source, Sink,
       Compressor, Evaporator, Condenser, ExpansionValve
   )
   
   # Heat transfer
   from energysystemmodels.HeatTransfer import (
       CompositeWall, Layer, PlateHeatExchanger, PipeInsulation
   )
   
   # Hydraulics and aeraulics
   from energysystemmodels.Hydraulic import (
       StraightPipe, TA_Valve, AirDuct, Singularity
   )
   
   # AHU and air treatment
   from energysystemmodels.AHU import (
       FreshAir, HeatingCoil, CoolingCoil, Humidifier, Fan
   )
   
   # Analysis and optimization
   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   from energysystemmodels.IPMVP import IPMVPModel, IPMVPReport
   
   # Building modeling
   from energysystemmodels.BuildingModel import RC_Model, RC_Model_Advanced
   
   # Utilities
   from energysystemmodels.utils import (
       APIConnector, ParallelCalculator
   )
   from energysystemmodels.visualization import EnergyPlotter
   from energysystemmodels.exceptions import (
       EnergySystemError, ConfigurationError, 
       CalculationError, DataError
   )

External Dependencies
---------------------

The EnergySystemModels package requires the following dependencies:

.. code-block:: text

   numpy>=1.20.0
   pandas>=1.3.0
   matplotlib>=3.4.0
   scipy>=1.7.0
   pvlib>=0.9.0
   CoolProp>=6.4.0
   requests>=2.26.0
   psychrolib>=2.5.0

Complete installation with all dependencies:

.. code-block:: console

   $ pip install EnergySystemModels[all]

Minimal installation:

.. code-block:: console

   $ pip install EnergySystemModels

Installation for specific modules:

.. code-block:: console

   $ pip install EnergySystemModels[pv]        # Photovoltaics only
   $ pip install EnergySystemModels[hvac]      # HVAC only
   $ pip install EnergySystemModels[analysis]  # Analysis only

================================================================================
Conclusion
================================================================================

This documentation covers all EnergySystemModels functionalities according to the energy value chain:

1. **Purchasing and Billing**: TURPE, CEE
2. **Data and Production**: Weather, PV
3. **Transformation**: Thermodynamic cycles
4. **Distribution**: Heat transfer, Hydraulics, Aeraulics
5. **End Uses**: AHU, Pinch, IPMVP, RC Model

For more information, consult:

- Complete documentation: https://energysystemmodels.readthedocs.io
- Source code: https://github.com/your-repo/EnergySystemModels
- Examples: https://github.com/your-repo/EnergySystemModels/tree/main/examples
- Issues: https://github.com/your-repo/EnergySystemModels/issues

Support and Contribution
-------------------------

For any questions or contributions:

- Email: support@energysystemmodels.com
- Forum: https://forum.energysystemmodels.com
- Slack: https://energysystemmodels.slack.com

================================================================================
License
================================================================================

EnergySystemModels is distributed under the MIT license.

Copyright (c) 2024 EnergySystemModels Contributors

For full license details, see the LICENSE file in the source repository.
