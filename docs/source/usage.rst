=====
Usage
=====

.. _installation:

Installation
------------

Pour utiliser EnergySystemModels, installez-le d'abord en utilisant pip :

.. code-block:: console

   (.venv) $ pip install EnergySystemModels

Overview
--------------

EnergySystemModels est une library Python complète for la modélisation and analysis energy systems.
This documentation is organized according to the **energy value chain**, from supplier to end use :

1. **Achat et Facturation** : TURPE, CEE
2. **Data et Production** : Meteorology, Photovoltaics
3. **Transformation** : Thermodynamic Cycles
4. **Distribution** : Heat Transfer, Hydraulique, Aéraulique
5. **Usages finaux** : CTA, Pinch Analysis, IPMVP, Modèle RC

.. toctree::
   :maxdepth: 2
   :caption: Sections du guide

   usage/section-1-achat-facturation
   usage/section-2-donnees-production
   usage/section-3-transformation
   usage/section-4-distribution
   usage/section-5-usages-finaux
   usage/section-6-financement-subvention
   usage/section-6-autres
