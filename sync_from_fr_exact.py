# -*- coding: utf-8 -*-
"""Synchronize EnergySystemModels-en from EnergySystemModels-fr.

The French documentation is the structural source of truth. This script mirrors
the same docs/source tree into the English repository, translates textual files
with the local deterministic glossary, copies binary assets as-is, and removes
obsolete files from the English docs/source tree.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FR_ROOT = ROOT.parent / "EnergySystemModels-fr" / "docs" / "source"
EN_ROOT = ROOT / "docs" / "source"
REPORT = ROOT / "SYNCHRONIZATION_REPORT.md"

TEXT_SUFFIXES = {".rst", ".md", ".json", ".py"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf"}


def _load_existing_glossary() -> dict[str, str]:
    namespace: dict[str, object] = {}
    path = ROOT / "translate_french_terms.py"
    if not path.exists():
        return {}
    exec(path.read_text(encoding="utf-8"), namespace)
    return dict(namespace.get("TRANSLATIONS", {}))


GLOSSARY: dict[str, str] = {
    **_load_existing_glossary(),
    # Documentation structure
    "Documentation EnergySystemModels": "EnergySystemModels Documentation",
    "Bienvenue dans la documentation de la bibliothèque EnergySystemModels !": "Welcome to the EnergySystemModels library documentation!",
    "Objectif et approche": "Objective and Approach",
    "Prérequis": "Prerequisites",
    "Table des matières": "Table of Contents",
    "Sommaire général": "General contents",
    "Achat et fourniture d'énergie": "Energy purchase and supply",
    "Production d'utilités et d'énergie": "Utilities and energy production",
    "Transport des utilités": "Utility transport",
    "Usages énergétiques": "Energy uses",
    "Récupération de chaleur et chaleur fatale": "Heat recovery and waste heat",
    "Financement et subvention": "Financing and subsidies",
    "Autres": "Other",
    # API reference
    "Cette page récapitule les **points d'entrée réels** de la bibliothèque": "This page summarizes the library's **real entry points**",
    "chemins d'import valides": "valid import paths",
    "et renvoie vers le chapitre": "and links to the chapter",
    "détaillé de chaque module": "dedicated to each module",
    "où figurent des exemples exécutables avec leurs": "where executable examples with their",
    "sorties réelles": "real outputs are shown",
    "par exemple": "for example",
    "par example": "for example",
    " et :doc:": " and :doc:",
    "En local (dépôt), les modules s'importent **sans** préfixe": "Locally, in the repository, modules are imported **without** the prefix",
    "le nom d'import est celui du sous-paquet": "the import name is the subpackage name",
    "Transfert de chaleur": "Heat Transfer",
    "Chaque composant s'instancie via": "Each component is instantiated with",
    "puis": "then",
    "résultats dans": "results in",
    "et attributs comme": "and attributes such as",
    "Détails": "Details",
    "Cycles thermodynamiques": "Thermodynamic Cycles",
    "Les composants s'assemblent par": "Components are assembled with",
    "Hydraulique et aéraulique": "Hydraulics and Aeraulics",
    "Traitement d'air": "Air Handling",
    "Analyse Pinch": "Pinch Analysis",
    "avec colonnes": "with columns",
    "attributs réels": "real attributes",
    "Mesure & Vérification": "Measurement & Verification",
    "retourne un tuple de 9 éléments": "returns a 9-item tuple",
    "Météorologie": "Meteorology",
    "Photovoltaïque": "Photovoltaics",
    "Achat d'énergie": "Energy Purchasing",
    "Certificats d'Économies d'Énergie": "Energy Savings Certificates",
    "module de fonctions": "function module",
    "pas de classe": "no class",
    "points d'entrée": "entry points",
    "chemins d'import": "import paths",
    "chapitre détaillé": "detailed chapter",
    "sous-paquet": "subpackage",
    # GUI guide
    "Interfaces graphiques et outils visuels": "Graphical Interfaces and Visual Tools",
    "Vue d'ensemble": "Overview",
    "Installation et lancement": "Installation and Launch",
    "Interface PyqtSimulator": "PyqtSimulator Interface",
    "Convention des ports": "Port Convention",
    "Lecture d'un graphe": "Reading a Graph",
    "Graphes avec plusieurs sorties": "Graphs with Multiple Outputs",
    "Stockage et calcul pas-à-pas": "Storage and Step-by-Step Calculation",
    "Cycle d'évaluation": "Evaluation Cycle",
    "Créer un nouveau nœud": "Creating a New Node",
    "Exemple réel : nœud Réchauffeur": "Real Example: Heater Node",
    "Enregistrer le nœud dans la palette": "Registering the Node in the Palette",
    "Bonnes pratiques de développement": "Development Best Practices",
    "Résultats et figures dans la documentation": "Results and Figures in the Documentation",
    "Générer les schémas et plots": "Generating Diagrams and Plots",
    "Construire la documentation": "Building the Documentation",
    "Dépannage": "Troubleshooting",
    "Checklist pour finaliser un exemple": "Checklist for Finalizing an Example",
    "nœud": "node",
    "nœuds": "nodes",
    "Nœud": "Node",
    "Nœuds": "Nodes",
    "Réchauffeur": "Heater",
    "Diviseur": "Splitter",
    "Ballon de stockage": "Storage tank",
    "pas de temps": "time step",
    "multi-sorties": "multiple outputs",
    "sortie": "output",
    "Sortie": "Output",
    "entrée": "input",
    "Entrée": "Input",
    "débit": "flow rate",
    "Débit": "Flow rate",
    "fluide": "fluid",
    "Fluide": "Fluid",
    "pression": "pressure",
    "Pression": "Pressure",
    "enthalpie": "enthalpy",
    "Enthalpie": "Enthalpy",
    "température": "temperature",
    "Température": "Temperature",
    "puissance": "power",
    "Puissance": "Power",
    "chaleur fatale": "waste heat",
    "Chaleur fatale": "Waste Heat",
    "schéma": "diagram",
    "Schéma": "Diagram",
    "résultats": "results",
    "Résultats": "Results",
    "exemple": "example",
    "Exemple": "Example",
    "exemples": "examples",
    "Exemples": "Examples",
    "méthode": "method",
    "Méthode": "Method",
    "utilisation": "usage",
    "Utilisation": "Usage",
    "données": "data",
    "Données": "Data",
    "énergie": "energy",
    "Énergie": "Energy",
    "énergétique": "energy",
    "Énergétique": "Energy",
    "énergétiques": "energy",
    "Énergétiques": "Energy",
    "Paramètres possibles": "Possible Parameters",
    "Paramètres calculés": "Calculated Parameters",
    "Paramètres principaux": "Main Parameters",
    "Paramètres de configuration": "Configuration Parameters",
    "Paramètres de traitement": "Processing Parameters",
    "Paramètres": "Parameters",
    "Objectifs du chapitre": "Chapter Objectives",
    "Introduction au module IPMVP": "Introduction to the IPMVP Module",
    "Introduction au Module PV": "Introduction to the PV Module",
    "Introduction au Module CEE": "Introduction to the ESC Module",
    "Cette documentation présente la bibliothèque Python EnergySystemModels": "This documentation presents the EnergySystemModels Python library",
    "conçue pour faciliter les calculs et analyses liés à l'efficacité énergétique": "designed to facilitate calculations and analyses related to energy efficiency",
    "En proposant des modèles écrits en Python, vous pouvez facilement mettre en pratique les concepts d'efficacité énergétique": "By providing Python-written models, you can easily put energy efficiency concepts into practice",
    "Les outils de calcul peuvent également faciliter la compréhension et l'analyse de données complexes liées à l'efficacité énergétique": "The calculation tools can also facilitate understanding and analysis of complex data related to energy efficiency",
    "Afin de mieux comprendre les modèles d'efficacité énergétique présentés dans ce document et les outils de calcul en Python qui les accompagnent": "In order to better understand the energy efficiency models presented in this document and the accompanying Python calculation tools",
    "il est nécessaire d'avoir des connaissances préalables en programmation": "prior knowledge of programming is necessary",
    "en particulier dans le langage Python": "particularly in the Python language",
    "Cependant, les modèles sont présentés étape par étape": "However, the models are presented step by step",
    "de manière simple et accessible": "in a simple and accessible manner",
    "afin de faciliter leur appropriation par un large public": "to facilitate their adoption by a wide audience",
    "**Développée par Zoheir HADID**": "**Developed by Zoheir HADID**",
    "Cette documentation est organisée selon la **chaîne de valeur energy**": "This documentation is organized according to the **energy value chain**",
    "Cette documentation couvre l'ensemble des fonctionnalités d'EnergySystemModels selon la chaîne de valeur energy": "This documentation covers all EnergySystemModels features according to the energy value chain",
    "Cette page regroupe l'ensemble des symboles, paramètres et variables utilisés in la bibliothèque EnergySystemModels": "This page groups all symbols, parameters and variables used in the EnergySystemModels library",
    "Cette section aide l'utilisateur à qualifier, quantifier et valoriser les": "This section helps the user qualify, quantify and value",
    "Cette approche garde la figure synchronisée with l'example": "This approach keeps the figure synchronized with the example",
    "l'utilisateur lit": "the user reads",
    "Chaque fichier décrit": "Each file describes",
    "Chaque élément de la palette vient du registre": "Each palette item comes from the registry",
    "Chaque nouveau node important doit avoir un example in la documentation": "Each important new node must have an example in the documentation",
    "Chaque classe s'instancie with": "Each class is instantiated with",
    "Chaque composant retourne un DataFrame": "Each component returns a DataFrame",
    "Chaque scénario d'orientation est simulé": "Each orientation scenario is simulated",
    "Chaque opération produit une ligne de result": "Each operation produces one result row",
    "Chaque calculateur produit plusieurs DataFrames by section": "Each calculator produces several DataFrames by section",
    "Chaque calculateur produit désormais des **DataFrames auditables**": "Each calculator now produces **auditable DataFrames**",
    "Chaque ligne du": "Each row of the",
    "La TVA est désormais": "VAT is now",
    "on l'ensemble de la facture": "on the entire bill",
    "Cette modification": "This change",
    "Cette fonction effectue des requêtes HTTP to": "This function sends HTTP requests to",
    "accès réseau": "network access",
    "Le model": "The model",
    "Le modèle": "The model",
    "la bibliothèque": "the library",
    "bibliothèque": "library",
    "des systèmes énergétiques": "energy systems",
    "systems energy": "energy systems",
    "efficacité energy": "energy efficiency",
    "data complexes": "complex data",
    "models écrits": "models written",
    "conçue for faciliter": "designed to facilitate",
    "for la modélisation": "for modeling",
    "et l'analyse": "and analysis",
    "mettre en pratique": "put into practice",
    "peuvent également faciliter": "can also facilitate",
    "compréhension": "understanding",
    "analyse de": "analysis of",
    "Installez": "Install",
    "Installer": "Install",
    "via pip": "with pip",
    "est organisée en modules thématiques": "is organized into thematic modules",
    "tester et présenter": "test and present",
    "models energy": "energy models",
    "les models physiques": "the physical models",
    "installer aussi": "also install",
    "ajouter le dossier": "add the folder",
    "Les connexions échangent": "Connections exchange",
    "Cette convention rend": "This convention makes",
    "entre ces listes et les objets": "between these lists and the objects",
    "avec les figures réellement produites by": "with the figures actually produced by",
    "Figure produite by une method réelle": "Figure produced by a real method",
    "methods de plot": "plot methods",
    "et sauvegarde les figures": "and saves the figures",
    "générée en exécutant": "generated by running",
    "Output réelle": "Real output",
    "Résultats exportés vers": "Results exported to",
    "fiche d'opération standardisée": "standardized operation sheet",
    "réellement": "actually",
    "Le calcul CEE est traité in le chapitre dédié": "The ESC calculation is handled in the dedicated chapter",
    "le rapport agrège ensuite": "the report then aggregates",
    "Détail des composantes de facture": "Bill component details",
    "Répartition Fourniture TURPE Taxes": "Supply TURPE Taxes breakdown",
    "pour l'exemple": "for the example",
    "supérieur à": "greater than",
    "pointe fixe": "fixed peak",
    "pointe mobile": "mobile peak",
    "uniquement": "only",
    "avec conditions définies": "with defined conditions",
    "Prise d'air neuf": "Fresh air intake",
    "Introduction d'air extérieur": "Outdoor air introduction",
    "flow rate": "flow rate",
    "conditions": "conditions",
    "Cette classe Python calcule les pertes de charge à travers différents modèles de vannes TA en utilisant les **données Kv officielles** du fabricant IMI TA en fonction du nombre de tours d'ouverture.": "This Python class calculates pressure drops through different TA valve models using the manufacturer's **official IMI TA Kv data** as a function of the number of opening turns.",
    "Chaque classe s'instancie avec": "Each class is instantiated with",
    "Chaque face peut avoir": "Each face can have",
    "Le calcul CEE est traité dans le chapitre dédié": "The ESC calculation is handled in the dedicated chapter",
    "Cette fonction effectue des requêtes HTTP vers": "This function sends HTTP requests to",
    "Cette approche garde la figure synchronisée avec l'exemple": "This approach keeps the figure synchronized with the example",
    "Cette page présente un exemple par": "This page presents one example per",
    "Cette page regroupe l'ensemble des symboles, paramètres et variables utilisés dans la bibliothèque EnergySystemModels": "This page groups all symbols, parameters and variables used in the EnergySystemModels library",
    "Cette documentation est organisée selon la **chaîne de valeur énergétique**": "This documentation is organized according to the **energy value chain**",
    "Cette documentation couvre l'ensemble des fonctionnalités d'EnergySystemModels selon la chaîne de valeur énergétique": "This documentation covers all EnergySystemModels features according to the energy value chain",
    "du fournisseur jusqu'à l'usage final": "from supplier to end use",
    "tester et présenter des modèles énergétiques": "test and present energy models",
    "EnergySystemModels contient plusieurs briques visuelles pour construire": "EnergySystemModels contains several visual building blocks to build",
    "tester et prÃ©senter des modÃ¨les Ã©nergÃ©tiques": "test and present energy models",
    "Cette page sert de guide de": "This page serves as a working guide:",
    "travail : elle explique comment lancer le simulateur PyQt": "it explains how to launch the PyQt simulator",
    "comment lire un graphe": "how to read a graph",
    "comment ajouter un nouveau nÅ“ud": "how to add a new node",
    "comment documenter les rÃ©sultats": "how to document results",
    "avec les figures rÃ©ellement produites par la bibliothÃ¨que": "with the figures actually produced by the library",
    "Le simulateur graphique principal est": "The main graphical simulator is",
    "Il s'appuie sur le": "It relies on the",
    "moteur ``NodeEditor`` pour manipuler des nÅ“uds et des connexions": "``NodeEditor`` engine to manipulate nodes and connections",
    "puis appelle": "then calls",
    "les modÃ¨les physiques de la bibliothÃ¨que": "the library's physical models",
    "Architecture gÃ©nÃ©rale": "General architecture",
    "la fenÃªtre PyQt hÃ©berge une scÃ¨ne NodeEditor": "the PyQt window hosts a NodeEditor scene",
    "les nÅ“uds enregistrÃ©s appellent les modÃ¨les EnergySystemModels": "registered nodes call the EnergySystemModels models",
    "puis les valeurs sont affichÃ©es ou sauvegardÃ©es": "then values are displayed or saved",
    "Le principe d'utilisation est toujours le mÃªme": "The usage principle is always the same",
    "Cette page sert de guide": "This page serves as a guide",
    "Chaque nouveau nœud important doit avoir un exemple dans la documentation": "Each important new node must have an example in the documentation",
    "Chaque calculateur produit désormais des **DataFrames auditables**": "Each calculator now produces **auditable DataFrames**",
    "Chaque calculateur produit plusieurs DataFrames par section": "Each calculator produces several DataFrames per section",
    "Chaque opération produit une ligne de résultat": "Each operation produces one result row",
    "Les déperditions de chaleur à travers les parois de l'échangeur de chaleur à plaques peuvent être calculées en utilisant la classe PlateHeatTransfer.": "Heat losses through the plate heat exchanger walls can be calculated using the PlateHeatTransfer class.",
    "Cette classe permet de calculer les déperditions de chaleur à travers les parois horizontales et verticales de l'échangeur de chaleur à plaques.": "This class calculates heat losses through the horizontal and vertical walls of the plate heat exchanger.",
    "Les déperditions de chaleur à travers les parois horizontales et verticales peuvent être calculées en utilisant les paramètres suivants": "Heat losses through the horizontal and vertical walls can be calculated using the following parameters",
    "Répartition Fourniture TURPE Taxes": "Supply TURPE Taxes Breakdown",
    "Détail des composantes de facture": "Bill Component Details",
    "Exemples TURPE": "TURPE Examples",
    "supérieur à 36 kVA": "above 36 kVA",
    "Paramètres d'entrée": "Input Parameters",
    "Paramètres fixes": "Fixed Parameters",
    "Paramètres du bâtiment": "Building Parameters",
    "Photovoltaïque uniquement": "Photovoltaics only",
    "Certificats de capacité": "Capacity certificates",
    "Certificats de capacite": "Capacity certificates",
    "Guide pratique : Auditer une facture d'energie with Python": "Practical Guide: Auditing an Energy Bill with Python",
    "Ce guide explique comment utiliser les modeles": "This guide explains how to use the models",
    "de la bibliotheque": "from the library",
    "for **verifier et auditer**": "to **check and audit**",
    "une facture d'electricite": "an electricity bill",
    "de gaz": "gas",
    "que ce soit en France": "whether in France",
    "ou en Algerie": "or in Algeria",
    "Nouveaute": "New in",
    "desormais": "now",
    "qui detaillent": "which detail",
    "chaque ligne de calcul": "each calculation row",
    "with :": "with:",
    "la formule utilisee": "the formula used",
    "les entrees": "the inputs",
    "les coefficients et le resultat": "the coefficients and the result",
    "L'objectif est de pouvoir controler": "The goal is to be able to check",
    "chaque composante d'une facture": "each component of a bill",
    "Structure universelle d'une facture d'energie": "Universal Structure of an Energy Bill",
    "Cette": "This",
    "Chaque": "Each",
    "bibliotheque": "library",
    "parametres": "parameters",
    "chapitre": "chapter",
    "exemple": "example",
    "energie": "energy",
    "energetique": "energy",
    "energetiques": "energy",
    "Quelle que soit l’energy": "Whatever the energy type",
    "Facture dâ€™Ã©nergie (gaz et Ã©lectricitÃ©) : principes communs": "Energy bill (gas and electricity): common principles",
    "Quelle que soit lâ€™Ã©nergie (gaz ou Ã©lectricitÃ©) et quel que soit le pays, une facture dâ€™Ã©nergie repose sur des composantes communes, issues de contraintes techniques et rÃ©glementaires universelles.": "Whatever the energy type (gas or electricity) and whatever the country, an energy bill is based on common components derived from universal technical and regulatory constraints.",
    "Ã‰nergie mesurÃ©e et facturÃ©e": "Measured and billed energy",
    "Mesure rÃ©alisÃ©e par un compteur": "Measurement performed by a meter",
    "Ã‰lectricitÃ© : Ã©nergie mesurÃ©e en kWh": "Electricity: energy measured in kWh",
    "Gaz : volume mesurÃ© puis exprimÃ© dans une unitÃ© Ã©nergÃ©tique dÃ©finie par la rÃ©glementation nationale": "Gas: measured volume then expressed in an energy unit defined by national regulation",
    "Facturation basÃ©e sur": "Billing based on",
    "quantitÃ© mesurÃ©e": "measured quantity",
    "tarif unitaire": "unit tariff",
    "AccÃ¨s au rÃ©seau": "Network Access",
    "Utilisation des rÃ©seaux de transport et de distribution": "Use of transport and distribution networks",
    "Financement de lâ€™exploitation, de la maintenance et de la sÃ©curitÃ©": "Funding of operation, maintenance and safety",
    "CoÃ»t prÃ©sent sur toutes les factures, dÃ©taillÃ© ou intÃ©grÃ©": "Cost present on all bills, either detailed or integrated",
    "CapacitÃ© ou abonnement": "Capacity or Subscription",
    "Droit dâ€™accÃ¨s permanent Ã  lâ€™Ã©nergie": "Permanent right of access to energy",
    "Dimensionnement du rÃ©seau selon un besoin maximal potentiel": "Network sizing according to a potential maximum need",
    "Part fixe, partiellement ou totalement indÃ©pendante de la consommation": "Fixed share, partially or totally independent of consumption",
    "Taxes et contributions publiques": "Taxes and Public Contributions",
    "PrÃ©lÃ¨vements dÃ©cidÃ©s par lâ€™Ã‰tat": "Levies decided by the State",
    "Variables selon les pays et les politiques Ã©nergÃ©tiques": "Variable according to countries and energy policies",
    "Peuvent inclure fiscalitÃ© gÃ©nÃ©rale, subventions ou mÃ©canismes de solidaritÃ©": "May include general taxation, subsidies or solidarity mechanisms",
    "Principe universel": "Universal Principle",
    "Une facture dâ€™Ã©nergie rÃ©munÃ¨re toujours une Ã©nergie livrÃ©e, un rÃ©seau mobilisÃ© et un cadre public rÃ©gulÃ©, indÃ©pendamment du pays ou de lâ€™unitÃ© utilisÃ©e.": "An energy bill always remunerates delivered energy, a mobilized network and a regulated public framework, regardless of the country or unit used.",
    "une facture d’energy repose on des composantes communes": "an energy bill is based on common components",
    "issues de contraintes techniques et réglementaires universelles": "derived from universal technical and regulatory constraints",
    "Une facture d’energy rémunère toujours": "An energy bill always remunerates",
    "une energy livrée": "delivered energy",
    "un réseau mobilisé": "a mobilized network",
    "un cadre public régulé": "a regulated public framework",
    "indépendamment du pays ou de l’unité utilisée": "regardless of the country or unit used",
    "Le module": "The module",
    "Ce module": "This module",
    "La fonction": "The function",
    "La classe": "The class",
    "Le calcul": "The calculation",
    "La facture": "The bill",
    "Les figures ci-dessous sont les real outputs are shown de": "The figures below are the real outputs of",
    "Cascades détaillées by composante": "Detailed cascades by component",
    "Cascades detaillees par composante": "Detailed cascades by component",
    "dépendent de": "depend on",
    "dépend du": "depends on the",
    "dépend des": "depends on the",
    "est utilisée": "is used",
    "est utilisee": "is used",
    "est calculée": "is calculated",
    "est calculee": "is calculated",
    "est publiée": "is published",
    "est publie": "is published",
    "sont publiés": "are published",
    "sont publies": "are published",
    "stockés dans": "stored in",
    "stockes in": "stored in",
    "stockee dans": "stored in",
    "sélectionné automatiquement": "automatically selected",
    "selectionne automatiquement": "automatically selected",
    "en fonction de": "as a function of",
    "as a function of la": "as a function of the",
    "as a function of le": "as a function of the",
    "as a function of les": "as a function of the",
    "selon": "according to",
    "according to les": "according to the",
    "according to le": "according to the",
    "according to la": "according to the",
    "publiée par": "published by",
    "publie by": "published by",
    "by la CRE": "by the CRE",
    "to calculate les": "to calculate the",
    "permet d'accéder": "provides access",
    "permet de calculer": "calculates",
    "permet d'identifier": "identifies",
    "permet d'optimiser": "optimizes",
    "allows calculer": "calculates",
    "allows modéliser": "models",
    "allows mesurer": "measures",
    "allows déterminer": "determines",
    "allows chaîner": "chains",
    "permet": "allows",
    "récupère": "retrieves",
    "nécessite": "requires",
    "n'expose **que**": "exposes **only**",
    "modélise": "models",
    "modéliser": "model",
    "simule": "simulates",
    "calcule": "calculates",
    "calcule les": "calculates the",
    "optimise": "optimizes",
    "aide à estimer": "helps estimate",
    "expose une fonction principale": "exposes one main function",
    "retourne alors": "then returns",
    "Le prix du MWh cumac dépend": "The price of a cumac MWh depends",
    "détails": "details",
    "économies d'energy": "energy savings",
    "économies d'énergie": "energy savings",
    "économies potentielles": "potential savings",
    "certificats générés": "generated certificates",
    "fiches d'opérations standardisées": "standardized operation sheets",
    "fiches": "sheets",
    "en vigueur": "in force",
    "abrogée": "repealed",
    "moto-régulés": "motor-controlled",
    "chaleur du compresseur": "compressor heat",
    "est récupérée": "is recovered",
    "pour un usage": "for a use",
    "Le point Pinch": "The Pinch point",
    "est visible": "is visible",
    "se construit": "is built",
    "Le choix": "The choice",
    "est un compromis between": "is a trade-off between",
    "se calcule": "is calculated",
    "La source basse temperature": "The low-temperature source",
    "température": "temperature",
    "pression": "pressure",
    "perte de charge": "pressure drop",
    "pertes de charge": "pressure drops",
    "régime d'écoulement": "flow regime",
    "rugosité": "roughness",
    "paroi": "wall",
    "parois": "walls",
    "surface temperature": "surface temperature",
    "surface de l'isolant": "insulation surface",
    "tuyau": "pipe",
    "tuyau droit cylindrique": "straight cylindrical pipe",
    "mur multicouche": "multilayer wall",
    "corps parallélépipédique": "parallelepiped body",
    "boîte rectangulaire": "rectangular box",
    "environnement ambiant": "ambient environment",
    "à partir de": "from",
    "a partir de": "from",
    "peut être": "can be",
    "peuvent être": "can be",
    "reelles": "real",
    "réelles": "real",
    "réel": "real",
    "reel": "real",
    "réseau": "network",
    "reseau": "network",
    "fournisseur": "supplier",
    "consommation": "consumption",
    "consommations": "consumptions",
    "données": "data",
    "donnees": "data",
    "résultat": "result",
    "resultat": "result",
    "résultats": "results",
    "resultats": "results",
    "entrées": "inputs",
    "entrees": "inputs",
    "sortie": "output",
    "sorties": "outputs",
    "entrée": "input",
    "facturée": "billed",
    "facturee": "billed",
    "période": "period",
    "periode": "period",
    "calculée": "calculated",
    "calculee": "calculated",
    "utilisée": "used",
    "utilisee": "used",
    "formule utilisée": "formula used",
    "Equation utilisee": "Equation used",
    "part power": "power share",
    "part energy": "energy share",
    "sous-totaux": "subtotals",
    "montants": "amounts",
    "doivent correspondre": "must match",
    "relever": "read",
    "relevée": "read",
    "relevee": "read",
    "partagees": "shared",
    "ecart": "difference",
    "Ecart": "Difference",
    "Calcule": "Calculated",
    "Releve": "Read",
    "Methode": "Method",
    "Donnees": "Data",
    "Detail": "Detail",
    "Declarer": "Declare",
    "Resultats attendus": "Expected Results",
    "verification contre": "verification against",
    "facture reelle": "real bill",
    "fevrier": "February",
    "Ile-de-France": "Ile-de-France",
    "thenguage": "language",
    "Facture dâ€™energy (gaz et Ã©lectricitÃ©) : principes communs": "Energy bill (gas and electricity): common principles",
    "Quelle que soit lâ€™energy (gaz ou Ã©lectricitÃ©) et quel que soit le pays, une facture dâ€™energy repose on des composantes communes": "Whatever the energy type (gas or electricity) and whatever the country, an energy bill is based on common components",
    "Energy mesurÃ©e et billed": "Measured and billed energy",
    "Mesure rÃ©alisÃ©e by un compteur": "Measurement performed by a meter",
    "Ã‰lectricitÃ© : energy mesurÃ©e en kWh": "Electricity: energy measured in kWh",
    "Gaz : volume mesurÃ© then exprimÃ© in une unitÃ© energy dÃ©finie by the rÃ©glementation nationale": "Gas: measured volume then expressed in an energy unit defined by national regulation",
    "Facturation basÃ©e on": "Billing based on",
    "AccÃ¨s au network": "Network Access",
    "Usage des networkx de transport et de distribution": "Use of transport and distribution networks",
    "Financement de lâ€™exploitation, de la maintenance et de la sÃ©curitÃ©": "Funding of operation, maintenance and safety",
    "CoÃ»t prÃ©sent on toutes les factures, dÃ©taillÃ© ou intÃ©grÃ©": "Cost present on all bills, either detailed or integrated",
    "CapacitÃ© ou abonnement": "Capacity or Subscription",
    "Droit dâ€™accÃ¨s permanent Ã  lâ€™energy": "Permanent right of access to energy",
    "Dimensionnement du network according to un besoin maximal potentiel": "Network sizing according to a potential maximum need",
    "Part fixe, partiellement ou totalement indÃ©pendante de la consumption": "Fixed share, partially or totally independent of consumption",
    "PrÃ©lÃ¨vements dÃ©cidÃ©s by lâ€™Ã‰tat": "Levies decided by the State",
    "Variables according to les pays et les politiques energy": "Variable according to countries and energy policies",
    "Peuvent inclure fiscalitÃ© gÃ©nÃ©rale, subventions ou mÃ©canismes de solidaritÃ©": "May include general taxation, subsidies or solidarity mechanisms",
    "Une facture dâ€™energy rÃ©munÃ¨re toujours une energy livrÃ©e": "An energy bill always remunerates delivered energy",
    "et a regulated public framework": "and a regulated public framework",
    "comment lire un": "how to read a",
    "comment ajouter un nouveau node": "how to add a new node",
    "comment documenter les results": "how to document results",
    "avec les figures actually produites by the library": "with the figures actually produced by the library",
    "moteur ``NodeEditor`` for manipuler des nodes et des connexions": "``NodeEditor`` engine to manipulate nodes and connections",
    "les models physiques de the library": "the library's physical models",
    "Architecture du simulateur PyQt": "PyQt simulator architecture",
    "Architecture gÃ©nÃ©rale": "General architecture",
    "la fenÃªtre PyQt hÃ©berge une scÃ¨ne NodeEditor": "the PyQt window hosts a NodeEditor scene",
    "nodes enregistrÃ©s appellent les models EnergySystemModels": "registered nodes call the EnergySystemModels models",
    "then les valeurs": "then values",
    "sont affichÃ©es ou sauvegardÃ©es": "are displayed or saved",
    "Le principe d'usage est toujours le mÃªme": "The usage principle is always the same",
    "Facture d’energy (gaz et électricité) : principes communs": "Energy bill (gas and electricity): common principles",
    "Quelle que soit l’energy (gaz ou électricité) et quel que soit le pays, une facture d’energy repose on des composantes communes, derived from universal technical and regulatory constraints.": "Whatever the energy type (gas or electricity) and whatever the country, an energy bill is based on common components derived from universal technical and regulatory constraints.",
    "Energy mesurée et billed": "Measured and billed energy",
    "Mesure réalisée by un compteur": "Measurement performed by a meter",
    "Électricité : energy mesurée en kWh": "Electricity: energy measured in kWh",
    "Gaz : volume mesuré then exprimé in une unité energy définie by the réglementation nationale": "Gas: measured volume then expressed in an energy unit defined by national regulation",
    "Facturation basée on": "Billing based on",
    "Accès au network": "Network Access",
    "Usage des networkx de transport et de distribution": "Use of transport and distribution networks",
    "Financement de l’exploitation, de la maintenance et de la sécurité": "Funding of operation, maintenance and safety",
    "Coût présent on toutes les factures, détaillé ou intégré": "Cost present on all bills, either detailed or integrated",
    "Capacité ou abonnement": "Capacity or Subscription",
    "Droit d’accès permanent à l’energy": "Permanent right of access to energy",
    "Dimensionnement du network according to un besoin maximal potentiel": "Network sizing according to a potential maximum need",
    "Part fixe, partiellement ou totalement indépendante de la consumption": "Fixed share, partially or totally independent of consumption",
    "Prélèvements décidés by l’État": "Levies decided by the State",
    "Variables according to les pays et les politiques energy": "Variable according to countries and energy policies",
    "Peuvent inclure fiscalité générale, subventions ou mécanismes de solidarité": "May include general taxation, subsidies or solidarity mechanisms",
    "Une facture d’energy rémunère toujours une energy livrée": "An energy bill always remunerates delivered energy",
    "graphe": "graph",
    "comment ajouter un nouveau node et comment documenter les results": "how to add a new node and how to document results",
    "compresseur, échangeur, pompe": "compressor, exchanger, pump",
    "batterie, humidificateur, réchauffeur": "coil, humidifier, heater",
    "Architecture générale": "General architecture",
    "la fenêtre PyQt héberge une scène NodeEditor": "the PyQt window hosts a NodeEditor scene",
    "nodes enregistrés appellent les models EnergySystemModels": "registered nodes call the EnergySystemModels models",
    "sont affichées ou sauvegardées": "are displayed or saved",
    "Le principe d'usage est toujours le même": "The usage principle is always the same",
}


def _ordered_glossary() -> list[tuple[str, str]]:
    return sorted(GLOSSARY.items(), key=lambda item: len(item[0]), reverse=True)


def translate_plain_text(content: str) -> str:
    translated = content
    for french, english in _ordered_glossary():
        translated = translated.replace(french, english)
    return translated


def _is_adornment(line: str) -> bool:
    if line[:1].isspace():
        return False
    stripped = line.strip()
    return bool(stripped) and len(set(stripped)) == 1 and stripped[0] in "=-~^\"'`#*+"


def normalize_rst_underlines(content: str) -> str:
    lines = content.splitlines()
    for index in range(1, len(lines)):
        if _is_adornment(lines[index]) and lines[index - 1].strip():
            char = lines[index].strip()[0]
            indent = lines[index][: len(lines[index]) - len(lines[index].lstrip())]
            needed = max(len(lines[index - 1].strip()), len(lines[index].strip()))
            lines[index] = indent + char * needed
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def deduplicate_adjacent_paragraphs(content: str) -> str:
    parts = re.split(r"(\n\s*\n)", content)
    output: list[str] = []
    last_paragraph: str | None = None
    for index in range(0, len(parts), 2):
        paragraph = parts[index]
        separator = parts[index + 1] if index + 1 < len(parts) else ""
        normalized = " ".join(paragraph.split())
        if normalized and normalized == last_paragraph:
            continue
        output.append(paragraph)
        output.append(separator)
        if normalized:
            last_paragraph = normalized
    return "".join(output)


def polish_known_pages(relative_path: Path, content: str) -> str:
    """Polish high-visibility pages where phrase-by-phrase translation is weak."""
    rel = relative_path.as_posix()
    if rel == "010-achat-energie/index.rst":
        return """.. _achat-energie:

10. Energy Purchasing
======================

Energy bill (gas and electricity): common principles
----------------------------------------------------

Whatever the energy type (gas or electricity) and whatever the country, an
energy bill is based on common components derived from universal technical and
regulatory constraints.

1. Measured and billed energy
   * Measurement performed by a meter
   * Electricity: energy measured in kWh
   * Gas: measured volume, then expressed in an energy unit defined by national regulation (for example thermie, kWh, or an equivalent unit)
   * Billing based on: measured quantity x unit tariff

2. Network access
   * Use of transport and distribution networks
   * Funding of operation, maintenance and safety
   * Cost present on all bills, either detailed or integrated

3. Capacity or subscription
   * Permanent right of access to energy
   * Network sizing according to a potential maximum need
   * Fixed share, partially or totally independent of consumption

4. Taxes and public contributions
   * Levies decided by the State
   * Variable according to countries and energy policies
   * May include general taxation, subsidies or solidarity mechanisms

Universal principle
-------------------

An energy bill always remunerates delivered energy, a mobilized network and a
regulated public framework, regardless of the country or unit used.

.. toctree::
   :maxdepth: 2
   :caption: Energy Purchasing:

   contrat_electricite
   contrat_gaz
   guide_audit_facture

Examples
--------

.. toctree::
   :maxdepth: 1
   :caption: TURPE Examples

   exemples/exemple_hta_cu_pf
   exemples/exemple_hta_cu_pm
   exemples/exemple_hta_lu_pf
   exemples/exemple_hta_lu_pm
   exemples/exemple_bt_m36_cu4
   exemples/exemple_bt_p36_cu
"""
    if rel == "gui_tools.rst":
        original = content.splitlines()
        try:
            start = original.index("Installation and Launch")
        except ValueError:
            return content
        polished_intro = """.. _gui_tools:

Graphical Interfaces and Visual Tools
=======================================

EnergySystemModels contains several visual building blocks to build, test and
present energy models. This page is a working guide: it explains how to launch
the PyQt simulator, read a graph, add a new node and document results with the
figures actually produced by the library.

Overview
--------------

The main graphical simulator is ``PyqtSimulator``. It relies on the
``NodeEditor`` engine to manipulate nodes and connections, then calls the
library's physical models: compressor, exchanger, pump, coil, humidifier,
heater, etc.

.. figure:: images/gui_pyqtsimulator_architecture.svg
   :alt: PyQt simulator architecture
   :align: center

   General architecture: the PyQt window hosts a NodeEditor scene, registered
   nodes call EnergySystemModels models, then values are displayed or saved.

The usage principle is always the same:

1. Launch the interface.
2. Create a new scene.
3. Drag nodes from the palette.
4. Connect outputs to inputs.
5. Fill in the parameters.
6. Evaluate the graph or the output node.
7. Save the project in ``.json`` format.

"""
        return polished_intro + "\n".join(original[start:]) + "\n"
    return content


def _directive_name(stripped: str) -> str | None:
    match = re.match(r"\.\.\s+([A-Za-z0-9_-]+)::", stripped)
    return match.group(1).lower() if match else None


def _is_path_like(stripped: str) -> bool:
    if not stripped:
        return False
    if " " in stripped or "\t" in stripped:
        return False
    return any(token in stripped for token in ("/", "\\", ".", "_"))


def translate_rst(content: str, relative_path: Path | None = None) -> str:
    lines = content.splitlines(keepends=True)
    output: list[str] = []
    protect_indented_block: int | None = None
    protect_toctree: int | None = None

    for line in lines:
        raw = line.rstrip("\n")
        newline = "\n" if line.endswith("\n") else ""
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip())

        if protect_indented_block is not None:
            if stripped and indent <= protect_indented_block:
                protect_indented_block = None
            else:
                output.append(line)
                continue

        if protect_toctree is not None:
            if stripped and indent <= protect_toctree:
                protect_toctree = None
            else:
                option_match = re.match(r"(:(?:caption):\s*)(.*)", raw.lstrip())
                if option_match:
                    translated_option = option_match.group(1) + translate_plain_text(option_match.group(2))
                    output.append(raw[:indent] + translated_option + newline)
                else:
                    output.append(line)
                continue

        if not stripped or _is_adornment(raw):
            output.append(line)
            continue

        if stripped.startswith(".. "):
            directive = _directive_name(stripped)
            output.append(line)
            if directive in {"code-block", "math", "parsed-literal", "literalinclude", "raw"}:
                protect_indented_block = indent
            elif directive == "toctree":
                protect_toctree = indent
            continue

        if stripped.startswith(":") and indent > 0:
            option_match = re.match(r"(:(?:alt|caption):\s*)(.*)", raw.lstrip())
            if option_match:
                translated_option = option_match.group(1) + translate_plain_text(option_match.group(2))
                output.append(raw[:indent] + translated_option + newline)
            else:
                output.append(line)
            continue

        translated = translate_plain_text(raw.lstrip())
        # Keep Sphinx document targets stable. The English tree intentionally
        # mirrors French file names, so :doc:`exemple_...` must not become
        # :doc:`example_...`.
        doc_target_map = {
            "examples": "exemples",
            "example_": "exemple_",
            "method": "methode",
            "protocol": "protocole",
            "mathematical_models": "modeles_mathematiques",
            "cee_module": "module_cee",
            "achat-energy": "achat-energie",
        }

        def restore_doc_target(match: re.Match[str]) -> str:
            value = match.group(0)
            for english, french in doc_target_map.items():
                value = value.replace(english, french)
            value = value.replace("009-pv-solaire/usage", "009-pv-solaire/utilisation")
            return value

        translated = re.sub(r":doc:`([^`]+)`", restore_doc_target, translated)
        output.append(" " * indent + translated + newline)

    translated_content = normalize_rst_underlines(deduplicate_adjacent_paragraphs("".join(output)))
    if relative_path is not None:
        translated_content = polish_known_pages(relative_path, translated_content)
    return translated_content


def translate_json(content: str) -> str:
    data = json.loads(content)

    def visit(value):
        if isinstance(value, str):
            return translate_plain_text(value)
        if isinstance(value, list):
            return [visit(item) for item in value]
        if isinstance(value, dict):
            return {key: visit(item) for key, item in value.items()}
        return value

    return json.dumps(visit(data), ensure_ascii=False, indent=2) + "\n"


def translate_conf(content: str) -> str:
    content = content.replace("copyright = '2024-2025, Zoheir HAD