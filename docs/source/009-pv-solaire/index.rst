.. _pv_solaire:

The module ``PV.ProductionElectriquePV.SolarSystem`` simulates the production
photovoltaïque d'un site from sa localisation, en s'appuyant sur
``pvlib-python`` et la météo horaire PVGIS. Each fonctionnalité de la classe
est illustrée ci-dessous by un example.

Créer un system et calculatesr the production
=============================================

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(
       latitude=45.764, longitude=4.8357,
       name='Usine Lyon', altitude=200,
       timezone='Europe/Paris',
       azimut=180,       # 0=Nord, 90=Est, 180=Sud, 270=Ouest
       inclinaison=20,   # degrés par rapport à l'horizontale
   )

   pv.retrieve_module_inverter_data(
       module_name='Canadian_Solar_CS5P_220M___2009_',
       inverter_name='ABB__MICRO_0_25_I_OUTD_US_208__208V_',
       temperature_model='open_rack_glass_glass',
   )

   pv.calculate_solar_parameters()   # télécharge la météo PVGIS automatiquement
   print(pv.df)

Output ``pv.df`` (météo PVGIS, un module) :

.. code-block:: text

                               SolarSystem
   Site                          Usine Lyon
   Module    Canadian_Solar_CS5P_220M___2009_
   Surface module (m2)                 1.701
   Puissance STC (Wc)                  219.7
   Onduleur  ABB__MICRO_0_25_I_OUTD_US_208__208V_
   Production / module (kWh/an)        306.9
   Productivite (kWh/kWc/an)            1397

* **latitude / longitude / altitude** : position du site ;
* **azimut** : orientation (0°=Nord, 180°=Sud) ;
* **inclinaison** : angle by rapport à l'horizontale ;
* **module_name** : module PV (base Sandia, 500+ références) ;
* **inverter_name** : onduleur (base CEC, 1000+ références) ;
* **temperature_model** : model thermique (``open_rack_glass_glass``,
  ``close_mount_glass_glass``…).

Synthèse technique et économique — ``pv.summary()``
===================================================

.. code-block:: python

   print(pv.summary(
       nb_modules=455, module_wc=220,
       capex_eur_m2=155,
       opex_eur_m2=2,
       tarif_elec_eur_mwh=120,
       duree_vie=25,
   ))

Renvoie une synthèse for l'ensemble du champ : power installée, surface,
production annuelle, then les indicateurs économiques (CAPEX, OPEX, temps de
retour, ROI, TRI) calculés froms hypothèses passées en argument.

Graphique de production — ``pv.plot()``
=======================================

.. code-block:: python

   pv.plot(nb_modules=455)

Affiche the production AC horaire (nulle la nuit, maximale en milieu de journée)
et le profil mensuel du champ.

Export Excel — ``pv.to_excel()``
================================

.. code-block:: python

   pv.to_excel('production_lyon.xlsx', nb_modules=455)

Génère un classeur à trois onglets : **Horaire** (8760 lignes), **Mensuel**
(12 lignes) et **Synthèse**.

Étude d'orientation — ``SolarSystem.orientation_study()``
===============================================================

Method de classe qui simulates et compare plusieurs orientations / inclinaisons
pour un même site :

.. code-block:: python

   scenarios = [
       {'nom': 'Sud 35', 'azimut': 180, 'inclinaison': 35},
       {'nom': 'Sud 10', 'azimut': 180, 'inclinaison': 10},
       {'nom': 'SE 30',  'azimut': 135, 'inclinaison': 30},
       {'nom': 'Est 85', 'azimut': 90,  'inclinaison': 85},
   ]

   df, df_monthly = SolarSystem.orientation_study(
       latitude=45.764, longitude=4.8357,
       name='Lyon', altitude=200, timezone='Europe/Paris',
       scenarios=scenarios,
   )
   print(df)                                             # production annuelle par scénario
   SolarSystem.plot_orientation_study(df, df_monthly, name='Lyon')   # profils mensuels
