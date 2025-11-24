Parallelepiped Body
===================

Usage
-----

.. image:: ../images/001_heat_transfer_parallelepiped.png
   :alt: Plate Heat Transfer
   :width: 400px
   :align: center

.. code-block:: python

  from HeatTransfer import ParallelepipedicBody

  # Define the thermal configuration for each face
  thermal_measurements = {
      'top': {'Tp': 60.0, 'isolated': False},
      'bottom': {'Tp': 60.0, 'isolated': False},
      'front': {'Tp': 60.0, 'isolated': False},
      'back': {'Tp': 60.0, 'isolated': False},
      'left': {'Tp': 60.0, 'isolated': False},
      'right': {'Tp': 60.0, 'isolated': False}
  }

  # Create the object
  objet = ParallelepipedicBody.Object(
      L=0.6,  # Length [m]
      W=0.8,  # Width [m]
      H=1.5,  # Height [m]
      Ta=25,  # Ambient temperature [°C]
      faces_config=thermal_measurements
  )
  
  # Calculationationationationate heat transfers
  objet.calculate()

  # Display results
  print(f"Total transfer: {objet.get_total_heat_transfer():.2f} W")
  print(objet.df)

Results ::

  Total transfer: 1956.56 W
       Face        Orientation  Surface (m²) Tp (°C)  Ta (°C) ΔT (°C) Isolated  Heat Transfer (W)  Heat Flux (W/m²)
  0     top    Horizontal (up)          0.48    60.0       25    35.0    False             191.19            398.31
  1  bottom  Horizontal (down)          0.48    60.0       25    35.0    False             189.98            395.80
  2   front           Vertical          1.20    60.0       25    35.0    False             450.11            375.09
  3    back           Vertical          1.20    60.0       25    35.0    False             450.11            375.09
  4    left           Vertical          0.90    60.0       25    35.0    False             337.58            375.09
  5   right           Vertical          0.90    60.0       25    35.0    False             337.58            375.09
  6   TOTAL                  -          5.16       -       25       -        -            1956.56            379.18

The calculation returns:

- **Total heat transfer**: Sum of losses from all faces [W]
- **Detailed DataFrame**: For each face (top, bottom, front, back, left, right)
  
  - Surface area [m²]
  - Wall temperature [°C]
  - Convection coefficient [W/m²·K]
  - Convection transfer [W]
  - Radiation transfer [W]
  - Total transfer per face [W]

Possible Parameters
-------------------

**Face configuration** (``faces_config`` dictionary):

Each face can have:

- ``'Tp'``: Wall temperature [°C]
- ``'isolated'``: ``True`` or ``False`` (insulated face or not)

**Available faces**: ``'top'``, ``'bottom'``, ``'front'``, ``'back'``, ``'left'``, ``'right'``

Model Explanation
-----------------

This model calculates the heat transfer from a parallelepiped body (rectangular box) to the ambient environment.

The calculation takes into account:

1. **Natural convection**: Heat exchange between the surface and ambient air
2. **Radiation**: Heat emission by radiation to the environment

For each face, the model:

- Calculates the exchange surface area
- Determines the convection coefficient according to orientation (horizontal/vertical)
- Calculates convection and radiation fluxes
- Sums contributions to obtain the total transfer
