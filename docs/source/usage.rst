Usage
=====

.. _installation:

Installation
------------

To use EnergySystemModels, first install it using pip:

.. code-block:: console

   pip install energysystemmodels

Or in a virtual environment:

.. code-block:: console

   (.venv) $ pip install energysystemmodels

Updating
--------

To update EnergySystemModels to the latest version:

.. code-block:: console

   pip install --upgrade energysystemmodels

.. _quick_start:

Quick Start Guide
-----------------

First Example: Heat Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculating thermal losses through a composite wall:

.. code-block:: python

   from HeatTransfer import CompositeWall

   # Create a composite wall
   wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
   
   # Add layers (from outside to inside)
   wall.add_layer(thickness=0.20, material='Hollow blocks')
   wall.add_layer(thickness=0.05, material='Polystyrene')
   wall.add_layer(thickness=0.02, material='Plaster')
   
   # Calculate the transfer
   wall.calculate()
   
   # Display results
   print(f"Total resistance: {wall.R_total:.3f} m².K/W")
   print(f"Heat flux: {wall.Q:.2f} W")
   print(wall.df)

Second Example: Thermodynamic Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a fluid source:

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   # Create a Source object
   SOURCE = Source.Object()
   
   # Input data
   SOURCE.Ti_degC = 25
   SOURCE.Pi_bar = 1.01325
   SOURCE.fluid = "air"
   SOURCE.F_Sm3h = 3600  # Standard volumetric flow rate [Sm³/h]
   
   # Calculate the object
   SOURCE.calculate()
   
   # Display results
   print(SOURCE.df)

Third Example: Pinch Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thermal integration optimization:

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # Define thermal streams
   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],      # Initial temperatures [°C]
       'To': [50, 45, 250, 195],      # Final temperatures [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],   # Heat capacity flow rate [kW/K]
       'dTmin2': [5, 5, 5, 5],        # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   })

   # Analyze
   pinch = PinchAnalysis.Object(df)
   
   # Results
   print(f"Pinch Point: {pinch.T_pinch}°C")
   print(f"Minimum hot utility: {pinch.Qh_min} kW")
   print(f"Minimum cold utility: {pinch.Qc_min} kW")
   
   # Visualize
   pinch.plot_composites_curves()
   pinch.plot_GCC()

Fourth Example: Weather Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieve real-time weather data:

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import WeatherData

   # Initialize with your API key
   weather = WeatherData(api_key="YOUR_API_KEY")
   
   # Get data for a city
   data = weather.get_current_weather(city="Paris")
   
   print(f"Temperature: {data['temperature']}°C")
   print(f"Humidity: {data['humidity']}%")
   print(f"Description: {data['description']}")

Fifth Example: Air Handling Unit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simulate an AHU with fresh air:

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Connect import Air_connect

   # Create the first FA instance
   FA = FreshAir.Object()
   FA.RH = 50  # Relative humidity [%]
   FA.T = 20   # Temperature [°C]
   FA.F_m3h = 3000  # Volumetric flow rate [m³/h]
   
   # Perform calculations for FA
   FA.calculate()
   print(f"FA calculated: {FA.df}")
   
   # Create the second FA2 instance
   FA2 = FreshAir.Object()
   # Connect FA2's Inlet to FA's Outlet
   Air_connect(FA2.Inlet, FA.Outlet)
   # Perform calculations for FA2
   FA2.calculate()
   print(f"FA2 calculated: {FA2.df}")

Main Imports
------------

Here are the most commonly used imports:

.. code-block:: python

   # Heat transfer
   from HeatTransfer.CompositeWall import CompositeWall
   from HeatTransfer.PipeInsulation import PipeInsulation

   # Thermodynamic cycles
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Hydraulics
   from Hydraulic.StraightPipe import StraightPipe
   from Hydraulic.TA_Valve import TA_Valve

   # AHU
   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil
   from AHU.CoolingCoil import CoolingCoil
   from AHU.Humidifier import Humidifier

   # Energy analysis
   from PinchAnalysis import PinchAnalysis
   from IPMVP.IPMVP import IPMVP

   # Weather data
   from OpenWeatherMap.OpenWeatherMap import WeatherData
   from MeteoCiel.MeteoCiel import MeteoCiel

   # Solar production
   from PV.PV import PVSystem

   # Billing
   from Facture.TURPE import TURPE
   from CEE.CEE import CEE

Data Structure
--------------

Most modules return results in the form of:

- **pandas DataFrames**: For time series and result tables
- **Object attributes**: For individual values
- **Dictionaries**: For structured data

Example of accessing results:

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.F = 0.5
   source.calculate()

   # Access via attributes
   print(source.h_outlet)
   print(source.T_outlet)
   
   # Access via DataFrame
   print(source.df)
   print(source.df['h[J/kg]'])

Error Handling
--------------

EnergySystemModels modules raise explicit exceptions:

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   try:
       source = Source.Object()
       source.Pi_bar = 5.0
       source.fluid = "InvalidFluid"  # Unsupported fluid
       source.calculate()
   except ValueError as e:
       print(f"Error: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Required Dependencies
---------------------

EnergySystemModels requires the following libraries (installed automatically):

- **CoolProp**: Thermodynamic properties of fluids
- **pandas**: Tabular data manipulation
- **numpy**: Numerical calculations
- **matplotlib**: Graphical visualizations
- **scipy**: Scientific calculations
- **requests**: API requests (for OpenWeatherMap)
- **pvlib**: Photovoltaic calculations (optional)
- **PyQt5**: Graphical interfaces (optional)

Advanced Configuration
----------------------

For advanced users, you can configure:

**Calculation Precision**

.. code-block:: python

   import numpy as np
   np.set_printoptions(precision=4, suppress=True)

**Visualization Options**

.. code-block:: python

   import matplotlib.pyplot as plt
   
   plt.rcParams['figure.figsize'] = (12, 6)
   plt.rcParams['font.size'] = 12
   plt.rcParams['axes.grid'] = True

**Unit Management**

Default units are:

- Temperature: °C
- Pressure: bar
- Mass flow rate: kg/s
- Power: kW
- Energy: kWh

Next Steps
----------

Consult the following sections for detailed explanations:

- :ref:`heat_transfer` - Heat transfer calculations
- :ref:`thermodynamic_cycles` - Refrigeration cycle modeling
- :ref:`ahu_modules` - Air handling unit simulation
- :ref:`pinch_analysis` - Energy integration optimization

For complete API reference, see :doc:`api`
