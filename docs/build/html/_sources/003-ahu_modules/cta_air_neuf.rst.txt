.. _cta_air_neuf:

CTA d'air neuf
==============

Usage
-----------

.. image:: ../images/003_ahu_fresh_air.png
   :alt: AHU Fresh Air
   :width: 600px
   :align: center

.. code-block:: python

    from AHU import FreshAir, HeatingCoil
    from AHU.Humidification import Humidifier
    from AHU.Connect import Air_connect
    from AHU.air_humide import PsychrometricChart

    # Air neuf
    AN = FreshAir.Object()
    AN.F_m3h = 3000
    AN.T = 5
    AN.RH = 80
    AN.calculate()

    # Batterie de chauffage
    BC = HeatingCoil.Object()
    BC.To_target = 20
    Air_connect(BC.Inlet, AN.Outlet)
    BC.calculate()

    # Humidificateur
    HMD = Humidifier.Object()
    HMD.wo_target = 8
    Air_connect(HMD.Inlet, BC.Outlet)
    HMD.HumidType = "vapeur"
    HMD.calculate()

    # Diagramme psychrométrique
    chart = PsychrometricChart.Object(figsize=(12, 4))
    chart.set_title('CTA batterie chaude & Humidificateur vapeur')
    
    custom_points = [
        {'h': BC.Inlet.h, 'w': BC.Inlet.w},
        {'h': BC.Outlet.h, 'w': BC.Outlet.w},
        {'h': HMD.Outlet.h, 'w': HMD.Outlet.w}
    ]
    chart.add_points(custom_points)
    chart.show(draw_arrows=True)

**Diagramme psychrométrique** :

.. image:: ../images/003_ahu_fresh_air_figure1.png
   :alt: Diagramme psychrométrique
   :width: 600px
   :align: center

**Results numériques** :

- **Air neuf (AN)** : T=5°C, RH=80%, F=1.053 kg/s, w=4.314 g/kg_sec, h=15.8 kJ/kg
- **Batterie chauffage (BC)** : T_output=20°C, RH=29.8%, Q_th=15.9 kW
- **Humidificateur (HMD)** : T_output=20.6°C, RH=53.1%, w_output=8 g/kg_sec, F_eau=0.0039 kg/s

Each component returns a DataFrame (``df``) with les details complets.

Possible Parameters
--------------------

**FreshAir (Air neuf)** :

- ``F_m3h`` : Flow rate volumique [m³/h]
- ``T`` : Temperature [°C]
- ``RH`` : Humidité relative [%]
- ``P`` : Pressure atmosphérique [Pa] (défaut: 101325)

**HeatingCoil (Batterie de chauffage)** :

- ``To_target`` : Temperature de output cible [°C]
- ``Inlet`` : Connecté via ``Air_connect()``
- Calculated automatiquement ``Q_th`` (power thermique) [kW]

**Humidifier** :

- ``wo_target`` : Humidité absolue de output cible [g/kg_air_sec]
- ``HumidType`` : Type d'humidification
  
  - ``"adiabatique"`` (défaut) : Humidification by évaporation d'eau
  - ``"vapeur"`` : Injection de vapeur

- ``Inlet`` : Connecté via ``Air_connect()``
- Calculated automatiquement ``F_water`` (flow rate d'eau) [kg/s] et ``Q_th`` [kW]

**PsychrometricChart** :

- ``figsize`` : Dimensions du graphique (largeur, hauteur)
- ``set_title()`` : Définir le titre du diagramme
- ``add_points()`` : Liste de points with coordata ``{'h': enthalpy, 'w': humidité}``
- ``show(draw_arrows=True)`` : Afficher with flèches de transformation

Explication du model
----------------------

Ce model simulates une Centrale de Traitement d'Air (CTA) simple composée de trois éléments en série :

1. **Fresh air intake** : Outdoor air introduction with defined conditions (T, RH, flow rate)
2. **Batterie de chauffage** : Réchauffage de l'air à temperature constante d'humidité absolue
3. **Humidificateur** : Ajout d'humidité by injection de vapeur ou évaporation adiabatique

The module utilise les propriétés de l'air humide to calculate :

- Les transformations on le diagramme psychrométrique (h, w)
- Les powers thermiques nécessaires
- Les flow rates de fluids (air sec, air humide, eau d'humidification)

The function ``Air_connect()`` allows chaîner les composants en connectant la output d'un composant à l'input du suivant.

**Transformations psychrométriques** :

- **Chauffage** : Ligne horizontale (w constant) to la droite (T augmente)
- **Humidification vapeur** : Ligne quasi-horizontale (T légèrement augmente)
- **Humidification adiabatique** : Ligne isoenthalpique (h constant)
