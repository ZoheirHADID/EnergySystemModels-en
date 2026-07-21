EnergySystemModels Documentation
=================================

Welcome to the EnergySystemModels library documentation!

**Developed by Zoheir HADID**

Objective and Approach
----------------------

This documentation presents the EnergySystemModels Python library,
conçue for faciliter les calculs et analyses liés à l'efficacité
energy. Elle combine des explications métier, des examples exécutables
et des pages de référence for passer rapidement d'un concept à son
implémentation Python.

Accès rapide
------------

Pour démarrer according to votre besoin :

1. :doc:`quickstart` for une prise en main rapide.
2. :doc:`usage` for le parcours fonctionnel complet.
3. :doc:`gui_tools` for l'interface graphique ``PyqtSimulator``.
4. :doc:`api` for les imports et entry points reals.

Prerequisites
-------------

Afin d'exploiter au mieux les models, il est recommandé d'avoir des bases en
Python et en thermique/energy. Les examples restent structurés de façon
progressive for être utilisables aussi en apprentissage.

Table of Contents
------------------

.. toctree::
   :maxdepth: 2
   :caption: General contents:

   usage
   quickstart
   contributing

.. toctree::
   :maxdepth: 2
   :caption: 1. Energy purchase and supply

   010-achat-energie/index

.. toctree::
   :maxdepth: 2
   :caption: 2. Utilities and energy production

   002-thermodynamic_cycles/index
   009-pv-solaire/index

.. toctree::
   :maxdepth: 2
   :caption: 3. Utility transport

   001-heat_transfer/index
   transfert_chaleur
   004-hydraulic/index
   005-aeraulic/index

.. toctree::
   :maxdepth: 2
   :caption: 4. Energy uses

   003-ahu_modules/index

.. toctree::
   :maxdepth: 2
   :caption: 5. Récupération de chaleur

   006-pinch_analysis/index

.. toctree::
   :maxdepth: 2
   :caption: 6. Financing and subsidies

   011-cee/index

.. toctree::
   :maxdepth: 2
   :caption: 7. Other

   007-ipmvp/index
   008-meteo/index
   gui_tools
   nomenclature
   api