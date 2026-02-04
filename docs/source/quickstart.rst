.. _quickstart:

Quick Start Guide
=================

This guide allows you to start using EnergySystemModels in just a few minutes.

Installation
------------

Install the library via pip:

.. code-block:: console

   pip install energysystemmodels

Or in a virtual environment:

.. code-block:: console

   (.venv) $ pip install energysystemmodels

Usage Principle
---------------

EnergySystemModels follows a simple and consistent object-oriented programming model:

1. **Create an object** representing an energy component
2. **Define input parameters** (temperatures, pressures, flow rates, etc.)
3. **Call the calculate() method** to perform calculations
4. **Access results** via object attributes or DataFrame

Simple Example
~~~~~~~~~~~~~~

Here is a minimal example to illustrate the principle:

.. code-block:: python

   from HeatTransfer import CompositeWall

   # 1. Create the object
   wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
   
   # 2. Define the structure (add layers)
   wall.add_layer(thickness=0.20, material='Hollow blocks')
   wall.add_layer(thickness=0.05, material='Polystyrene')
   wall.add_layer(thickness=0.02, material='Plaster')
   
   # 3. Calculate
   wall.calculate()
   
   # 4. Access results
   print(f"Thermal resistance: {wall.R_total:.3f} m².K/W")
   print(f"Heat flux: {wall.Q:.2f} W")
   print(wall.df)  # DataFrame with all results

Available Modules
-----------------

The library is organized into thematic modules:

**Heat Transfer**
  Thermal calculations for walls, pipes, heat exchangers

**Thermodynamic Cycles**
  Modeling of refrigeration cycles, heat pumps, compressors

**Air Handling Units (AHU)**
  Complete AHU simulation with coils, humidification, heat recovery

**Hydraulics**
  Pressure drop calculations, pump and valve sizing

**Energy Analysis**
  Pinch Analysis, IPMVP, thermal integration optimization

**Weather Data**
  Retrieval of real-time or historical climate data

**Solar Production**
  Photovoltaic production simulation

**Billing**
  TURPE calculation, energy savings certificates (CEE)

Units and Conventions
---------------------

Default units are:

- **Temperature**: °C
- **Pressure**: bar
- **Mass flow rate**: kg/s
- **Volumetric flow rate**: m³/h
- **Power**: kW
- **Energy**: kWh

Results Structure
-----------------

Results are accessible in two ways:

**Via object attributes:**

.. code-block:: python

   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.calculate()
   
   print(source.h_outlet)  # Direct access to enthalpy
   print(source.T_outlet)  # Direct access to temperature

**Via a pandas DataFrame:**

.. code-block:: python

   print(source.df)  # Complete results table
   print(source.df['h[J/kg]'])  # Access to a specific column

Going Further
-------------

Consult the detailed sections of the documentation:

- :doc:`usage` - Complete user guide with examples
- :doc:`api` - Detailed API reference for all modules
- :doc:`001-heat_transfer/index` - Heat Transfer
- :doc:`002-thermodynamic_cycles/index` - Thermodynamic Cycles
- :doc:`003-ahu_modules/index` - Air Handling Units
- :doc:`006-pinch_analysis/index` - Pinch Analysis

Resources
---------

- **Online documentation**: https://energysystemmodels-en.readthedocs.io/
- **Source code**: https://github.com/ZoheirHADID/EnergySystemModels
- **PyPI**: https://pypi.org/project/energysystemmodels/
- **Support**: https://github.com/ZoheirHADID/EnergySystemModels/issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall

   # Create a wall
   wall = CompositeWall.Object()
   
   # Add layers (thickness [m], conductivity [W/m.K])
   wall.add_layer(0.02, 0.25)  # Interior plaster
   wall.add_layer(0.15, 0.04)  # Glass wool insulation
   wall.add_layer(0.20, 1.40)  # Concrete block
   wall.add_layer(0.01, 0.80)  # Exterior rendering
   
   # Boundary conditions
   wall.T_interior = 20   # °C
   wall.T_exterior = -5   # °C
   wall.h_interior = 8    # W/m².K
   wall.h_exterior = 25   # W/m².K
   
   # Calculate
   wall.calculate()
   
   # Results
   print(f"U-value: {wall.U:.3f} W/m².K")
   print(f"Heat flux: {wall.heat_flux:.2f} W/m²")
   print(f"Total thermal resistance: {wall.R_total:.3f} m².K/W")

**Expected result:**

.. code-block:: text

   U-value: 0.246 W/m².K
   Heat flux: 6.15 W/m²
   Total thermal resistance: 4.065 m².K/W

Example 2: Refrigerant Fluid Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   # Create an R134a source
   source = Source.Object()
   source.Pi_bar = 5.0       # Pressure [bar]
   source.Ti_C = 20          # Temperature [°C]
   source.fluid = "R134a"    # Fluid
   source.F = 0.5            # Flow rate [kg/s]
   
   # Calculate
   source.calculate()
   
   # Display results
   print(f"Enthalpy: {source.h_outlet:.2f} J/kg")
   print(f"Entropy: {source.s_outlet:.2f} J/kg.K")
   print(f"Density: {source.rho:.2f} kg/m³")
   print(f"Fluid state: {source.quality}")
   
   # Complete DataFrame
   print("\nDetailed results:")
   print(source.df)

**Expected result:**

.. code-block:: text

   Enthalpy: 426543.21 J/kg
   Entropy: 1745.32 J/kg.K
   Density: 27.45 kg/m³
   Fluid state: superheated vapor

Example 3: Size a Heating Coil
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil

   # Define outdoor air
   air_ext = FreshAir.Object()
   air_ext.T_C = -5          # Outdoor temperature [°C]
   air_ext.RH = 0.80         # Relative humidity
   air_ext.F_dry = 1.0       # Dry air flow rate [kg/s]
   air_ext.calculate()
   
   print(f"Outdoor air: {air_ext.T_C}°C, {air_ext.RH*100}% RH")
   print(f"Enthalpy: {air_ext.h:.2f} kJ/kg")
   
   # Size the heating coil
   coil = HeatingCoil.Object()
   coil.inlet_air = air_ext
   coil.outlet_T_C = 18  # Supply setpoint [°C]
   coil.calculate()
   
   # Results
   print(f"\nHeating coil:")
   print(f"Required power: {coil.Q_th:.2f} kW")
   print(f"Outlet temperature: {coil.outlet_T_C}°C")
   print(f"Outlet humidity: {coil.outlet_RH*100:.1f}%")

**Expected result:**

.. code-block:: text

   Outdoor air: -5°C, 80.0% RH
   Enthalpy: -2.45 kJ/kg
   
   Heating coil:
   Required power: 23.50 kW
   Outlet temperature: 18°C
   Outlet humidity: 12.3%

Example 4: Optimization with Pinch Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt

   # Define thermal streams of a process
   # 2 hot streams to cool, 2 cold streams to heat
   df = pd.DataFrame({
       'name': ['Hot stream 1', 'Hot stream 2', 'Cold stream 1', 'Cold stream 2'],
       'Ti': [200, 125, 50, 45],          # Initial temperature [°C]
       'To': [50, 45, 250, 195],          # Final temperature [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],       # Heat capacity flow rate [kW/K]
       'dTmin2': [5, 5, 5, 5],            # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   })

   # Analyze
   pinch = PinchAnalysis.Object(df)
   
   # Key results
   print("=== PINCH ANALYSIS ===")
   print(f"Pinch Point: {pinch.T_pinch}°C")
   print(f"Minimum hot utility: {pinch.Qh_min} kW")
   print(f"Minimum cold utility: {pinch.Qc_min} kW")
   print(f"Potential recovery: {pinch.Q_recovered} kW")
   
   # Visualizations
   fig, axes = plt.subplots(1, 2, figsize=(14, 5))
   
   # Composite curves
   pinch.plot_composites_curves(ax=axes[0])
   axes[0].set_title('Composite Curves')
   
   # Grand Composite Curve
   pinch.plot_GCC(ax=axes[1])
   axes[1].set_title('Grand Composite Curve')
   
   plt.tight_layout()
   plt.savefig('pinch_analysis.png', dpi=300)
   plt.show()

**Expected result:**

.. code-block:: text

   === PINCH ANALYSIS ===
   Pinch Point: 120°C
   Minimum hot utility: 300 kW
   Minimum cold utility: 50 kW
   Potential recovery: 650 kW

Example 5: Retrieve Weather Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import WeatherData
   import pandas as pd

   # Initialize with your API key
   # (get it for free at https://openweathermap.org/api)
   weather = WeatherData(api_key="YOUR_API_KEY")
   
   # Current data
   paris = weather.get_current_weather(city="Paris")
   
   print("=== PARIS WEATHER ===")
   print(f"Temperature: {paris['temperature']}°C")
   print(f"Humidity: {paris['humidity']}%")
   print(f"Pressure: {paris['pressure']} hPa")
   print(f"Wind: {paris['wind_speed']} m/s")
   print(f"Description: {paris['description']}")
   
   # 5-day forecast
   forecast = weather.get_forecast(city="Paris", days=5)
   
   # Convert to DataFrame for analysis
   df_forecast = pd.DataFrame(forecast)
   print("\nForecast:")
   print(df_forecast[['datetime', 'temperature', 'humidity']])

Example 6: Pipe Pressure Drop Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from Hydraulic.StraightPipe import StraightPipe

   # Define the pipe
   pipe = StraightPipe.Object()
   pipe.D = 0.05             # Diameter [m]
   pipe.L = 100              # Length [m]
   pipe.flow_rate = 0.002    # Flow rate [m³/s]
   pipe.fluid = "Water"
   pipe.T = 60               # Temperature [°C]
   pipe.roughness = 0.00005  # Roughness [m] (new steel)
   
   # Calculate
   pipe.calculate()
   
   # Results
   print(f"Flow velocity: {pipe.velocity:.2f} m/s")
   print(f"Reynolds number: {pipe.Reynolds:.0f}")
   print(f"Flow regime: {pipe.regime}")
   print(f"Friction coefficient: {pipe.f:.4f}")
   print(f"Pressure drop: {pipe.pressure_drop:.2f} Pa")
   print(f"Pressure drop: {pipe.pressure_drop/1000:.2f} kPa")

**Expected result:**

.. code-block:: text

   Flow velocity: 1.02 m/s
   Reynolds number: 64523
   Flow regime: turbulent
   Friction coefficient: 0.0223
   Pressure drop: 2345.67 Pa
   Pressure drop: 2.35 kPa

Example 7: Balancing Valve
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from Hydraulic.TA_Valve import TA_Valve

   # Select an IMI TA valve
   valve = TA_Valve.Object()
   valve.model = "TA-COMPACT-P"
   valve.DN = 20                # Nominal diameter [mm]
   valve.flow_rate = 0.0005     # Flow rate [m³/s] = 1.8 m³/h
   valve.opening = 3.0          # Number of turns open
   
   # Calculate
   valve.calculate()
   
   # Results
   print(f"Model: {valve.model} DN{valve.DN}")
   print(f"Kv at {valve.opening} turns: {valve.Kv:.2f} m³/h")
   print(f"Flow rate: {valve.flow_rate * 3600:.2f} m³/h")
   print(f"Pressure drop: {valve.pressure_drop:.0f} Pa")
   print(f"Pressure drop: {valve.pressure_drop/100:.2f} mbar")

Integrated Use Cases
--------------------

Case 1: Building Energy Audit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall
   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil
   import pandas as pd

   # 1. Envelope losses
   south_facade = CompositeWall.Object()
   south_facade.add_layer(0.02, 0.25)   # Plaster
   south_facade.add_layer(0.10, 0.04)   # Insulation
   south_facade.add_layer(0.20, 0.80)   # Concrete
   south_facade.T_interior = 20
   south_facade.T_exterior = -5
   south_facade.h_interior = 8
   south_facade.h_exterior = 25
   south_facade.calculate()
   
   facade_area = 100  # m²
   facade_losses = south_facade.heat_flux * facade_area / 1000  # kW
   
   # 2. Ventilation losses
   air = FreshAir.Object()
   air.T_C = -5
   air.RH = 0.80
   air.F_dry = 0.5  # kg/s (approx. 1500 m³/h)
   air.calculate()
   
   heating = HeatingCoil.Object()
   heating.inlet_air = air
   heating.outlet_T_C = 20
   heating.calculate()
   
   ventilation_losses = heating.Q_th  # kW
   
   # 3. Total balance
   total_losses = facade_losses + ventilation_losses
   
   print("=== THERMAL BALANCE ===")
   print(f"Facade losses: {facade_losses:.2f} kW")
   print(f"Ventilation losses: {ventilation_losses:.2f} kW")
   print(f"Total losses: {total_losses:.2f} kW")
   
   # 4. Annual cost (estimate)
   heating_hours = 2500  # h/year (HDD base)
   energy_price = 0.10   # €/kWh
   annual_cost = total_losses * heating_hours * energy_price
   
   print(f"\nAnnual heating cost: {annual_cost:.0f} €/year")

Case 2: Heat Pump Sizing
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Evaporator (heat source from outdoor air)
   evap_inlet = Source.Object()
   evap_inlet.fluid = "R32"
   evap_inlet.Pi_bar = 3.5      # Evaporation pressure
   evap_inlet.quality = 1.0     # Saturated vapor at evaporator outlet
   evap_inlet.F = 0.15          # Flow rate [kg/s]
   evap_inlet.calculate()
   
   # Compressor
   compressor = Compressor.Object()
   compressor.inlet_source = evap_inlet
   compressor.Po_bar = 18.0     # Condensation pressure
   compressor.eta_isentropic = 0.70
   compressor.eta_volumetric = 0.85
   compressor.calculate()
   
   # Results
   print("=== R32 HEAT PUMP ===")
   print(f"Fluid: {evap_inlet.fluid}")
   print(f"Evaporation pressure: {evap_inlet.Pi_bar} bar")
   print(f"Condensation pressure: {compressor.Po_bar} bar")
   print(f"\nCompressor:")
   print(f"Power consumption: {compressor.W_compressor:.2f} kW")
   print(f"Discharge temperature: {compressor.outlet_T:.1f}°C")
   print(f"\nPerformance:")
   print(f"Thermal power: {compressor.Q_condenser:.2f} kW")
   print(f"COP: {compressor.COP:.2f}")

Case 3: Industrial Plant Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt

   # Industrial process with 6 streams
   df_process = pd.DataFrame({
       'name': [
           'Distillation - Condenser',
           'Distillation - Reboiler', 
           'Reactor - Cooling',
           'Feed - Preheating',
           'Drying - Heating',
           'Product - Cooling'
       ],
       'Ti': [95, 120, 180, 25, 50, 150],
       'To': [40, 160, 60, 90, 120, 45],
       'mCp': [8.0, 10.0, 5.0, 6.0, 4.0, 3.5],
       'dTmin2': [5, 5, 5, 5, 5, 5],
       'integration': [True, True, True, True, True, True]
   })

   # Pinch Analysis
   pinch = PinchAnalysis.Object(df_process)
   
   print("=== INDUSTRIAL OPTIMIZATION ===")
   print(f"Current needs (without integration):")
   print(f"  Hot utility: {pinch.total_heating_required:.0f} kW")
   print(f"  Cold utility: {pinch.total_cooling_required:.0f} kW")
   print(f"\nAfter optimal integration:")
   print(f"  Minimum hot utility: {pinch.Qh_min:.0f} kW")
   print(f"  Minimum cold utility: {pinch.Qc_min:.0f} kW")
   print(f"\nSavings:")
   heating_saving = pinch.total_heating_required - pinch.Qh_min
   cooling_saving = pinch.total_cooling_required - pinch.Qc_min
   print(f"  Heating reduction: {heating_saving:.0f} kW ({heating_saving/pinch.total_heating_required*100:.1f}%)")
   print(f"  Cooling reduction: {cooling_saving:.0f} kW ({cooling_saving/pinch.total_cooling_required*100:.1f}%)")
   
   # Financial estimate
   steam_price = 0.04  # €/kWh
   chilled_water_price = 0.02  # €/kWh
   operating_hours = 7500  # h/year
   
   annual_savings = (heating_saving * steam_price + 
                     cooling_saving * chilled_water_price) * operating_hours
   
   print(f"\nEstimated annual savings: {annual_savings/1000:.0f} k€/year")
   
   # Visualize
   pinch.plot_composites_curves()
   plt.savefig('industrial_optimization.png', dpi=300)
   plt.show()

Next Steps
----------

Now that you've mastered the basics, explore:

1. **Complete module documentation**: :doc:`index`
2. **Detailed API reference**: :doc:`api`
3. **Advanced examples** in each thematic section
4. **Jupyter Notebook** available in the GitHub repository

Additional Resources
--------------------

- **Online documentation**: https://energysystemmodels-en.readthedocs.io/
- **Source code**: https://github.com/ZoheirHADID/EnergySystemModels
- **PyPI**: https://pypi.org/project/energysystemmodels/
- **Issues and support**: https://github.com/ZoheirHADID/EnergySystemModels/issues

Need Help?
----------

If you encounter difficulties:

1. Check the examples in the section corresponding to your need
2. Verify the units of your data (°C, bar, kg/s, kW)
3. Consult the API reference for available parameters
4. Open an issue on GitHub with a minimal reproducible example

Best Practices
--------------

✅ **Do:**

- Validate units before calculations
- Check temperature ranges supported by CoolProp
- Use pandas DataFrames for time series
- Save results to Excel/CSV files

❌ **Don't:**

- Mix units (°C and K, bar and Pa)
- Use temperatures outside limits (-273°C to 2000°C depending on fluids)
- Ignore convergence warnings
- Modify objects after calculation without recalculating
