Introduction to the ESC Module
==============================

Le module ``CEE`` d'EnergySystemModels aide à estimer rapidement les
certificats d'économies d'energy associés à certaines opérations
standardisées. Il est particulièrement utile en phase d'avant-projet :
l'utilisateur peut comparer plusieurs actions, convertir les results en
MWh cumac et obtenir un ordre de grandeur de prime.

Le module expose une fonction principale :

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches

   print(list_fiches())

Les fiches **en vigueur** pilotées by le dispatcher (un example chacune dans
:doc:`module_cee`), rangées by secteur :

**Industrie**

* ``IND-UT-103`` : heat recovery on compresseur d'air.
* ``IND-UT-130`` : condenseur on effluents gazeux de chaudière vapeur.
* ``IND-UT-131`` : isolation de parois planes ou cylindriques industrielles.
* ``IND-UT-134`` : system de mesurage d'indicateurs de performance energy.
* ``IND-UT-135`` : freecooling by eau de refroidissement.

**Transport**

* ``TRA-EQ-101`` : unité de transport intermodal rail-route.
* ``TRA-EQ-107`` : unité de transport intermodal fluvial-route.

.. note::
   Les fiches ``IND-UT-136`` (systems moto-régulés, **abrogée** le 18/08/2025)
   et ``TRA-EQ-108`` (wagon d'autoroute ferroviaire, opération **close** au
   31/03/2020) sont supprimées : elles n'apparaissent plus in ``list_fiches()``
   et ``calcul_CEE`` les refuse (``ValueError``).

Example rapide : isolation industrielle
---------------------------------------

L'example suivant calcule les kWh cumac for l'isolation d'une paroi plane
industrielle fonctionnant en continu hors arrêt week-end.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   kwh_cumac = calcul_CEE(
       fiche="IND-UT-131",
       fonctionnement="3*8h_sansArrWE",
       Temperature=180,
       Geometry="plan",
       S=120,  # surface isolée [m2]
   )

   prix_mwh_cumac = 9.0
   prime_eur = kwh_cumac * prix_mwh_cumac / 1000

   print(f"Volume CEE : {kwh_cumac:,.0f} kWh cumac")
   print(f"Prime estimée : {prime_eur:,.0f} EUR")

Demander le détail du calcul
----------------------------

Pour construire un rapport utilisateur, il est préférable de demander les
détails. Le module retourne alors un dictionnaire with la fiche, le titre, les
MWh cumac, les kWh cumac et la valorisation interne.

.. code-block:: python

   details = calcul_CEE(
       fiche="IND-UT-135",
       return_details=True,
       fonctionnement="2*8h",
       Department=69,
       Supply_Temperature=16,
       puissance_nominale=200,
   )

   for cle, valeur in details.items():
       print(cle, ":", valeur)

Valorisation des CEE
--------------------

Le prix du MWh cumac dépend du marché, du type d'opération, du calendrier de
dépôt et des conditions contractuelles. Pour une première estimation, utilisez
une hypothèse explicite et conservez-la in le rapport.

.. math::

   \text{Prime CEE} = \text{kWh cumac} \times \frac{\text{Prix du MWh cumac}}{1000}

Example de lecture :

* volume obtenu : ``250 000 kWh cumac`` ;
* hypothèse de prix : ``9 EUR/MWh cumac`` ;
* prime estimée : ``250 000 x 9 / 1000 = 2 250 EUR``.

Bonnes pratiques
----------------

* Vérifier que la fiche existe with ``list_fiches()`` before d'automatiser une
  étude multi-sites.
* Garder les mêmes unités que le module : power en kW, surface en m2,
  temperature en degC, durée according to les chaînes attendues by la fiche.
* Demander ``return_details=True`` for tracer les results in un audit.
* Toujours valider l'éligibilité réglementaire et les pièces justificatives
  avec les fiches officielles before dépôt.

Références
----------

* Site officiel : https://www.ecologie.gouv.fr
* Registre des CEE : https://www.emmy.fr
* Fiches CEE : https://www.ecologie.gouv.fr/operations-standardisees-deconomies-denergie
