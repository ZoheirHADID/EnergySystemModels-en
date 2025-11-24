.. _exemple_ahu_frais:

Fresh Air AHU Example
====================

.. code-block:: python

    # =============================================================================
    # Modèle AHU (Air frais + Batterie de chauffage + Humidificateur)
    # =============================================================================

    #module de calcul des prop d'air humide
    from AHU import FreshAir
    #Composant Batterie de chauffage
    from AHU import HeatingCoil
    #composant Humidificateur (vapeur ou adiabatique)
    from AHU.Humidification import Humidifier
    # connection between components
    from AHU.Connect import Air_connect

    ##########Création des Objets
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()

    #Récupération des données entrées by l'utilisateur
    AN.F_m3h=3000 #m3/h
    AN.T=14 #°C
    AN.RH_FreshAir=71 # %
    BC.To_target=15 #°C
    HMD.wo_target=8 #g/Kg air sec

    #calculer les propriétés d'air neuf; !important
    AN.calculate()

    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()

    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.HumidType="vapeur" #par défaut : Humidificateur adiabatique
    HMD.calculate()

    #enregistrer les résultats du module d'air neuf
    print("Absolute Humidity of Fresh Air  g/kg_as",round(AN.w,1))
    print("Saturated Vapor Pressure of Fresh Air   Pa",round(AN.Pvsat,0))
    print("Wet Bulb Temperature of Fresh Air  °C",round(AN.T_hum,1))
    print("Enthalpy Spécifique de l'Air Frais  KJ/Kg_as",round(AN.h,3))

    #enregistrer les résultats de la Batterie de préchauffage
    print("Enthalpy Spécifique de la Batterie de Chauffage KJ/Kg_as",round(BC.ho,1))
    print("Power Thermique de la Batterie de Chauffage  kW",round(BC.Qth,1))
    print("Relative Humidity of Heating Coil %",round(BC.RH_out,1))
    print("Mass Flow Rate of Humidifier Steam Kg/s",round(HMD.F_water,3))  
    print("Dry Air Mass Flow Rate of Humidifier Kg/s",round(HMD.F_dry,3)) 

    # =============================================================================
    # Fin du Modèle AHU
    # =============================================================================