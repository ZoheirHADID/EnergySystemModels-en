Heat Transfer
====================

The image below shows an example of convective and radiative heat transfer through an uninsulated plate heat exchanger with a wall temperature of 60°C and an ambient temperature of 25°C:

.. image:: images/PlateHeatTransfer.png
   :alt: Plate Heat Transfer
   :width: 300px
   :align: center

Heat losses through the walls of the plate heat exchanger can be calculated using the PlateHeatTransfer class. This class allows calculating heat losses through horizontal and vertical walls of the plate heat exchanger. Heat losses through horizontal and vertical walls can be calculated using the following parameters:

.. code-block:: python

    from EnergySystemModels.TransferChaleur import PlateHeatTransfer

    # Wall temperature in °C
    Tp = 60
    # Ambient temperature in °C
    Ta = 25
    # Length in meters
    L = 0.6
    # Width in meters
    W = 0.8
    # Height in meters
    H = 1.5

    # Calculationationate heat transfer for the upper horizontal wall
    haut = PlateHeatTransfer.Object(
        orientation='horizontal_up',
        Tp=Tp,  # Wall temperature in °C
        Ta=Ta,  # Ambient temperature in °C
        W=W,    # Width in meters
        L=L     # Length in meters
    ).calculate()

    # Calculationationate heat transfer for the lower horizontal wall
    bas = PlateHeatTransfer.Object(
        orientation='horizontal_down',
        Tp=Tp,  # Wall temperature in °C
        Ta=Ta,  # Ambient temperature in °C
        W=W,    # Width in meters
        L=L     # Length in meters
    ).calculate()

    # Calculationationate heat transfer for the first vertical wall
    vertical1 = PlateHeatTransfer.Object(
        orientation='vertical',
        Tp=Tp,  # Wall temperature in °C
        Ta=Ta,  # Ambient temperature in °C
        W=W,    # Width in meters
        H=H     # Height in meters
    ).calculate() * 2

    # Calculationationate heat transfer for the second vertical wall
    vertical2 = PlateHeatTransfer.Object(
        orientation='vertical',
        Tp=Tp,  # Wall temperature in °C
        Ta=Ta,  # Ambient temperature in °C
        W=L,    # Width in meters
        H=H     # Height in meters
    ).calculate() * 2

    # Calculationationate total heat transfer
    total = haut + bas + vertical1 + vertical2
    print(f"{round(total, 0)} W = {round(haut, 0)} W + {round(bas, 0)} W + {round(vertical1, 0)} W + {round(vertical2, 0)} W")

Result: 
1957.0 W = 191.0 W + 190.0 W + 900.0 W + 675.0 W

Explanation of the Equations Used
-----------------------------------

The `PlateHeatTransfer` class uses different equations to calculate heat losses depending on the orientation of the plate (horizontal or vertical). Here are the main equations used:

### Calculationationated Parameters

- **Film temperature (Tf)**: Average temperature between the wall and ambient air.
.. math::

  Tf = \frac{Tp + Ta}{2}

- **Kinematic viscosity (v)**: 
.. math::

  v = \frac{\mu}{\rho_{ref}}

- **Density at film temperature (ρ)**:
.. math::

  \rho = \rho_{ref} \left(1 - \beta (Tf - 20)\right)

- **Thermal diffusivity (a)**:
.. math::

  a = \frac{k}{\rho \cdot Cp}

- **Prandtl number (Pr)**:
.. math::

  Pr = \frac{v}{a}

- **Grashof number (Gr)**:
.. math::

  Gr = \frac{g \cdot \beta \cdot (Tp - Ta) \cdot \left(\frac{W \cdot L}{2W + 2L}\right)^3}{v^2}

- **Rayleigh number (Ra)**:
.. math::

  Ra = Gr \cdot Pr

### Horizontal Plate Facing Downward

- **Nusselt number (Nu)**:
.. math::

  Nu = 0.27 \cdot Ra^{0.25} \quad \text{if} \quad 10^4 < Ra < 10^7

.. math::

  Nu = 0.54 \cdot Ra^{0.25} \quad \text{if} \quad Ra \geq 10^7

- **Heat transfer coefficient (h)**:
.. math::

  h = \frac{Nu \cdot k}{\frac{W \cdot L}{2W + 2L}}

### Horizontal Plate Facing Upward

- **Nusselt number (Nu)**:
.. math::

  Nu = 0.15 \cdot Ra^{0.33}

### Vertical Plate

- **Nusselt number (Nu)**:
.. math::

  Nu = \left(0.68 + \frac{0.67 \cdot Ra^{1/4}}{\left(1 + \left(\frac{0.492}{Pr}\right)^{9/16}\right)^{4/9}}\right)^2 \quad \text{if} \quad Ra < 10^9

.. math::

  Nu = \left(0.825 + \frac{0.387 \cdot Ra^{1/6}}{\left(1 + \left(\frac{0.492}{Pr}\right)^{9/16}\right)^{8/27}}\right)^2 \quad \text{if} \quad Ra \geq 10^9

### Convective Heat Transfer (q_conv)

.. math::

  q_{conv} = h \cdot W \cdot L \cdot (Tp - Ta)

### Radiative Heat Transfer (q_rad)

.. math::

  q_{rad} = \sigma \cdot W \cdot L \cdot e \cdot \left((Tp + 273.15)^4 - (Ta + 273.15)^4\right)

### Total Heat Transfer (q_total)

.. math::

  q_{total} = q_{conv} + q_{rad}
