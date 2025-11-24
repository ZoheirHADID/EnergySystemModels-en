# -*- coding: utf-8 -*-
"""
Translation Script for EnergySystemModels Documentation
Translates French text to English in .rst files
"""

import os
import re
from pathlib import Path

# Translation dictionary for common terms - Extended version
TRANSLATIONS = {
    # Titles and headers
    "Analyse de l'": "Analysis of ",
    "Analyse de l'pipe insulation": "Pipe Insulation Analysis",
    "Example de simulation de l'pipe insulation": "Pipe insulation simulation example",
    "Example de AHU Frais": "Fresh Air AHU Example",
    "Le modèle d'pipe insulation": "The pipe insulation model",
    "IPMVP - Mesure et Vérification": "IPMVP - Measurement and Verification",
    "Structure des données d'entrée": "Input Data Structure",
    "Calcul du coût du réseau électrique": "Electricity Grid Cost Calculation",
    "Résultats": "Results",
    "Résultat": "Result",
    "Exemple": "Example",
    "Exemples": "Examples",
    "Introduction": "Introduction",
    "Utilisation": "Usage",
    "Nomenclature": "Nomenclature",
    "Modèle Mathématique": "Mathematical Model",
    "Explication des équations utilisées": "Explanation of Equations Used",
    "Résumé des équations utilisées pour le calcul": "Summary of Equations Used for Calculation",
    "Calcul des propriétés de l'air ambiant": "Calculation of Ambient Air Properties",
    "Calcul des heat loss": "Heat Loss Calculation",
    "Calcul des temperatures": "Temperature Calculation",
    
    # Long phrases first (before shorter ones)
    "L'image ci-dessous montre l'évolution des déperditions et de la temperature de surface de l'isolant as a function of l'insulation thickness": "The image below shows the evolution of heat loss and insulation surface temperature as a function of insulation thickness",
    "The image below shows un exemple de insulated pipe avec les simulation parameters": "The image below shows an example of an insulated pipe with simulation parameters",
    "Le modèle utilise les propriétés thermophysiques des matériaux et des fluides to calculate les heat loss et la temperature de surface de l'isolant. Voici un résumé des équations utilisées": "The model uses the thermophysical properties of materials and fluids to calculate heat loss and insulation surface temperature. Here is a summary of the equations used",
    "Ces équations allow to déterminer les heat loss à travers l'isolant et la temperature de surface de l'isolant as a function ofs simulation parameters": "These equations allow us to determine heat loss through the insulation and the insulation surface temperature as a function of simulation parameters",
    "Ces équations allow to déterminer la distribution de temperature à travers le mur composite et le flux thermique total traversant le mur": "These equations allow us to determine the temperature distribution across the composite wall and the total heat flux through the wall",
    "Les temperatures aux interfaces des couches sont ensuite calculées en utilisant le flux thermique et les résistances thermiques": "The temperatures at layer interfaces are then calculated using heat flux and thermal resistances",
    "Le module IPMVP d'EnergySystemModels allows to quantifier les économies d'énergie selon le protocole IPMVP (Option C) en créant des modèles de baseline basés sur des régressions polynomiales": "The IPMVP module of EnergySystemModels allows quantifying energy savings according to the IPMVP protocol (Option C) by creating baseline models based on polynomial regressions",
    "Le module compare la consommation énergétique avant (baseline) et après un projet d'efficacité énergétique, en ajustant pour les variables indépendantes (météo, production, occupation)": "The module compares energy consumption before (baseline) and after an energy efficiency project, adjusting for independent variables (weather, production, occupation)",
    "Le module nécessite": "The module requires",
    "Le prix payé annuellement pour l'utilisation des réseaux publics de distribution (RPD) est la somme des composantes suivantes": "The annual price paid for the use of public distribution networks (PDN) is the sum of the following components",
    "La formule générale du TURPE est donc": "The general TURPE formula is therefore",
    "Détail des composantes": "Component Details",
    "Guide d'utilisation du calcul TURPE": "TURPE Calculation User Guide",
    "Voici un exemple d'utilisation des fonctions to calculate le TURPE": "Here is an example of using the functions to calculate TURPE",
    "Les paramètres à renseigner dans `input_Contrat`, `input_Tarif` et `input_Facture` sont détaillés dans les tableaux ci-dessous. Adaptez-les selon votre profil de consommation, votre contrat et les tarifs en vigueur": "The parameters to fill in `input_Contrat`, `input_Tarif` and `input_Facture` are detailed in the tables below. Adapt them according to your consumption profile, your contract and the current tariffs",
    "Tableau des paramètres d'entrée pour le calcul TURPE": "Table of Input Parameters for TURPE Calculation",
    "Versions d'utilisation selon le domaine de tension": "Usage Versions by Voltage Domain",
    "Déclarer un contrat": "Declare a Contract",
    "Déclarer une facture": "Declare an Invoice",
    "Début et fin de la période de facturation": "Start and end of billing period",
    "Nombre d'heures de dépassement de puissance souscrite": "Number of hours exceeding subscribed power",
    "L'image ci-dessous montre": "The image below shows",
    "Le code suivant montre": "The following code shows",
    "Le diagramme": "The diagram",
    "Les tableaux ci-dessous montrent": "The tables below show",
    "les résultats des calculs pour chaque composant": "the calculation results for each component",
    "de la CTA": "of the AHU",
    "points de fonctionnement": "operating points",
    "schéma de la CTA": "AHU schematic",
    
    # Specific technical phrases
    "volumétrique en mètres cubes par seconde": "volumetric in cubic meters per second",
    "volumétrique standard en mètres cubes par seconde": "standard volumetric in cubic meters per second",
    "massique à l'entrée en kilogrammes par seconde": "mass flow at inlet in kilograms per second",
    "à l'entrée en joules par kilogramme": "at inlet in joules per kilogram",
    "à la sortie en joules par kilogramme": "at outlet in joules per kilogram",
    "du tube en mètres carrés": "of the tube in square meters",
    "d'écoulement en mètres par seconde": "flow in meters per second",
    "de Reynolds": "Reynolds number",
    "de pressure en pascals": "pressure in pascals",
    "à l'entrée en pascals": "at inlet in pascals",
    "en watts": "in watts",
    "du fluide": "of the fluid",
    "en kilogrammes par mètre cube": "in kilograms per cubic meter",
    "de la surface": "of the surface",
    "hydraulique en mètres": "hydraulic in meters",
    "en mètres": "in meters",
    "d'inclinaison du tube en radians": "of tube inclination in radians",
    "du tuyau en mètres": "of the pipe in meters",
    "de pressure en mètres": "pressure in meters",
    "dynamique du fluide": "fluid dynamic viscosity",
    "de pressure due aux frottements": "pressure loss due to friction",
    "de pressure entre l'entrée et la sortie": "pressure difference between inlet and outlet",
    "en joules par kilogramme": "in joules per kilogram",
    "de dilatation thermique": "thermal expansion coefficient",
    "à la temperature de référence de 20°C": "at reference temperature of 20°C",
    "de Rayleigh": "Rayleigh number",
    "de Nusselt": "Nusselt number",
    "de transfert de chaleur moyen": "average heat transfer coefficient",
    "de chaleur convectif": "convective heat transfer",
    "de chaleur radiatif": "radiative heat transfer",
    "de la paroi interne": "of the inner wall",
    "de la paroi externe": "of the outer wall",
    "de surface de l'isolant": "of insulation surface",
    
    # Materials
    "Laine de verre": "Glass wool",
    "Mousse de polyuréthane": "Polyurethane foam",
    
    # Technical terms
    "Température": "Temperature",
    "température": "temperature",
    "Pression": "Pressure",
    "pression": "pressure",
    "Pressure": "Pressure",
    "Perte": "Loss",
    "Puissance": "Power",
    "Qualité": "Quality",
    "Section": "Section",
    "Vitesse": "Speed",
    "Nombre": "Number",
    "Densité": "Density",
    "Rugosité": "Roughness",
    "Diamètre": "Diameter",
    "Longueur": "Length",
    "Angle": "Angle",
    "Hauteur": "Height",
    "Viscosité": "Viscosity",
    "Différence": "Difference",
    "Enthalpie": "Enthalpy",
    "Coefficient": "Coefficient",
    "Transfert": "Transfer",
    "Propriétés": "Properties",
    "Résistance thermique de convection interne": "Internal convection thermal resistance",
    "Résistance thermique de conduction à travers l'isolant": "Conduction thermal resistance through insulation",
    "Résistance thermique de convection externe": "External convection thermal resistance",
    "Débit": "Flow rate",
    "débit": "flow rate",
    "Flow rate": "Flow rate",
    "Déperditions thermiques": "Heat loss",
    "déperditions thermiques": "heat loss",
    "Épaisseur de l'isolant": "Insulation thickness",
    "épaisseur de l'isolant": "insulation thickness",
    "Température de surface": "Surface temperature",
    "température de surface": "surface temperature",
    "Tracé des résultats": "Plot results",
    "résistance thermique": "thermal resistance",
    "isolation des tuyaux": "pipe insulation",
    "perte de charge linéaire": "linear pressure drop",
    "conduit d'eau": "water pipe",
    "tuyau isolé": "insulated pipe",
    "paramètres de simulation": "simulation parameters",
    
    # Code strings
    "Épaisseur de l'isolant (m)": "Insulation thickness (m)",
    "Effet de l'épaisseur de l'isolant sur les heat loss et la temperature de surface": "Effect of insulation thickness on heat loss and surface temperature",
    "nous avons déjà géré l'étiquette x avec ax1": "we already handled the x label with ax1",
    "Humidité Absolue de l'Air Frais  g/kg_as": "Absolute Humidity of Fresh Air  g/kg_as",
    "Pressure de Vapeur Saturée de l'Air Frais   Pa": "Saturated Vapor Pressure of Fresh Air   Pa",
    "Temperature de Bulbe Humide de l'Air Frais  °C": "Wet Bulb Temperature of Fresh Air  °C",
    "Enthalpie Spécifique de l'Air Frais  KJ/Kg_as": "Specific Enthalpy of Fresh Air  KJ/Kg_as",
    "Enthalpie Spécifique de la Batterie de Chauffage KJ/Kg_as": "Specific Enthalpy of Heating Coil KJ/Kg_as",
    "Puissance Thermique de la Batterie de Chauffage  kW": "Thermal Power of Heating Coil  kW",
    "Humidité Relative de la Batterie de Chauffage %": "Relative Humidity of Heating Coil %",
    "Flow rate Massique de Vapeur de l'Humidificateur Kg/s": "Mass Flow Rate of Humidifier Steam Kg/s",
    "Flow rate Massique d'Air Sec de l'Humidificateur Kg/s": "Dry Air Mass Flow Rate of Humidifier Kg/s",
    "R² (qualité du modèle)": "R² (model quality)",
    
    # Contract terms
    "Domaine de tension du raccordement": "Connection voltage domain",
    "Puissance souscrite en période de pointe (selon domaine de tension)": "Subscribed power during peak period (according to voltage domain)",
    "Puissance souscrite en heures pleines hiver": "Subscribed power during winter peak hours",
    "Puissance souscrite en heures creuses hiver": "Subscribed power during winter off-peak hours",
    "Puissance souscrite en heures pleines été": "Subscribed power during summer peak hours",
    "Puissance souscrite en heures creuses été": "Subscribed power during summer off-peak hours",
    "Option tarifaire selon le domaine de tension": "Tariff option according to voltage domain",
    "Pourcentage d'énergie renouvelable injectée ou autoconsommée": "Percentage of renewable energy injected or self-consumed",
    "Contrat Unique 4 périodes avec autoproduction collective et/ou alimentation de secours": "Single Contract 4 periods with collective self-production and/or backup supply",
    "Multi-usage avec autoproduction collective et/ou alimentation de secours": "Multi-use with collective self-production and/or backup supply",
    "Longue Usage (tarification spécifique pour usages prolongés)": "Long Use (specific pricing for extended use)",
    "Contrat Unique avec autoproduction collective et/ou alimentation de secours": "Single Contract with collective self-production and/or backup supply",
    "Longue Usage avec autoproduction collective et/ou alimentation de secours": "Long Use with collective self-production and/or backup supply",
    "Contrat CU (Contrat Unique) avec pointe fixe": "SC Contract (Single Contract) with fixed peak",
    "Contrat CU (Contrat Unique) avec pointe mobile": "SC Contract (Single Contract) with mobile peak",
    "Contrat LU (Longue Usage) avec pointe fixe": "LU Contract (Long Use) with fixed peak",
    "Contrat LU (Longue Usage) avec pointe mobile": "LU Contract (Long Use) with mobile peak",
    "Tarif unitaire période de pointe": "Unit price peak period",
    "Certificat capacité période de pointe": "Peak period capacity certificate",
    "Composante annuelle de gestion": "Annual management component",
    "Composante annuelle de comptage": "Annual metering component",
    "Composante annuelle de soutirage": "Annual withdrawal component",
    "Composante mensuelle des dépassements de puissance souscrite": "Monthly component for exceeding subscribed power",
    "Composante annuelle des alimentations complémentaires et de secours": "Annual component for supplementary and backup supplies",
    "Composante de regroupement": "Grouping component",
    "Composante annuelle de l'énergie réactive": "Annual reactive energy component",
    "Composante annuelle des injections": "Annual injection component",
    "Frais fixes de gestion du contrat": "Fixed contract management fees",
    "Frais liés à la mise à disposition et à la relève du compteur": "Fees related to meter provision and reading",
    "Frais liés à la quantité d'énergie soutirée du réseau": "Fees related to the amount of energy withdrawn from the grid",
    "Pénalités en cas de dépassement de la puissance souscrite": "Penalties for exceeding subscribed power",
    "Frais pour les alimentations complémentaires ou de secours": "Fees for supplementary or backup supplies",
    "Frais de regroupement de plusieurs sites": "Fees for grouping multiple sites",
    "Frais pour l'injection d'énergie sur le réseau": "Fees for energy injection into the grid",
    
    # IPMVP terms
    "Série temporelle de la consommation énergétique (kWh)": "Time series of energy consumption (kWh)",
    "DataFrame des variables indépendantes (DJU, production, etc.)": "DataFrame of independent variables (HDD, production, etc.)",
    "Périodes": "Periods",
    "Dates de début/fin des périodes baseline et reporting": "Start/end dates of baseline and reporting periods",
    
    # Code comments
    "# Exemple d'utilisation": "# Usage example",
    "# module de calcul": "# calculation module",
    "# Composant": "# Component",
    "# composant": "# component",
    "# connexion entre les composants": "# connection between components",
    "# options d'affichage": "# display options",
    "# par défaut": "# default",
    "# Créer": "# Create",
    "# Récupérer": "# Retrieve",
    "# Calculate": "# Calculate",
    "# Calcul": "# Calculation",
    "# Accéder aux résultats": "# Access results",
    
    # Section titles
    "Données Météorologiques": "Meteorological Data",
    "Données Météo": "Weather Data",
    "PV Solaire": "Solar PV",
    "Analyse de Pincement": "Pinch Analysis",
    
    # Other common terms
    "en fonction de": "as a function of",
    "permet de": "allows",
    "permettent de": "allow",
    "pour calculer": "to calculate",
    "utilise les équations suivantes": "uses the following equations",
    "uses the following equations to calculate": "uses the following equations to calculate",
    "sont automatiquement calculés": "are automatically calculated",
    "coordonnées GPS": "GPS coordinates",
    "la production": "the production",
    "selon le protocole": "according to the protocol",
    
    # Additional French terms in code/comments
    "# Simulation de l'effet de l'insulation thickness sur les heat loss": "# Simulation of insulation thickness effect on heat loss",
    "Effet de l'épaisseur de l'isolant sur les heat loss et la temperature de surface": "Effect of insulation thickness on heat loss and surface temperature",
    "Les DJU are automatically calculated par le module": "HDDs are automatically calculated by the module",
    "Le prix des CEE varie selon l'offre et la demande": "The CEE price varies according to supply and demand",
    "# Calculationation CEE pour une opération d'isolation": "# CEE calculation for an insulation operation",
    "# Pompe à chaleur air/eau": "# Air/water heat pump",
    "# Récupération chaleur fatale": "# Waste heat recovery",
    "# Calculationation pour chaque opération": "# Calculation for each operation",
    "- **CI** : Frais pour l'injection d'énergie sur le réseau.": "- **CI**: Fees for energy injection into the grid.",
    "# 2. Définition des tarifs unitaires (en €/kWh ou selon composante)": "# 2. Definition of unit tariffs (in €/kWh or by component)",
    "1. Créer un compte sur": "1. Create an account on",
    "# Récupération pour une ville": "# Retrieval for a city",
    "# Liste pour stocker les données": "# List to store data",
    "* Utiliser MeteoCiel pour données historiques": "* Use MeteoCiel for historical data",
    "# Retrieve données météo historiques depuis MeteoCiel": "# Retrieve historical weather data from MeteoCiel",
    "# Trouver codes sur": "# Find codes on",
    "# Nécessite clé API OpenWeatherMap (gratuite sur openweathermap.org)": "# Requires OpenWeatherMap API key (free on openweathermap.org)",
    "# Create un système PV avec paramètres géographiques": "# Create a PV system with geographic parameters",
    "# Retrieve les données modules/onduleurs depuis PVGIS": "# Retrieve module/inverter data from PVGIS",
    "# DataFrame avec production horaire": "# DataFrame with hourly production",
    "# Create un DataFrame avec les flux thermiques": "# Create a DataFrame with heat flows",
    "# dTmin2 : ΔTmin/2 pour chaque flux [K]": "# dTmin2: ΔTmin/2 for each flow [K]",
    "# integration : inclure le flux dans l'analyse": "# integration: include the flow in the analysis",
    "# Flux avec temperatures décalées": "# Flows with shifted temperatures",
    'print("\\nHeat Exchanger Network de chaleur :")': 'print("\\nHeat Exchanger Network:")',
    " échange avec ": " exchanges with ",
    " chauffé par utilité chaude": " heated by hot utility",
    " refroidi par utilité froide": " cooled by cold utility",
    "* Le condenseur peut récupérer une partie de sa chaleur": "* The condenser can recover part of its heat",
    "Vapeur chauffe le Rebouilleur": "Steam heats the Reboiler",
    "au lieu de": "instead of",
    "sans intégration": "without integration",
    "* **BAR-TH-104** : Pompe à chaleur de type air/eau ou eau/eau (résidentiel)": "* **BAR-TH-104**: Air/water or water/water heat pump (residential)",
    "0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA": "0 to 36 (kW) for LV < 36 kVA; >36 to ~250 (kW) for LV > 36 kVA; generally >250 kW for MV",
    "Par GPS coordinates": "By GPS coordinates",
    "Par nom de ville": "By city name",
    "selon l'offre et la demande": "according to supply and demand",
    " pour ": " for ",
    " avec ": " with ",
    " sans ": " without ",
    " dans ": " in ",
    " sur ": " on ",
    " sous ": " under ",
    " entre ": " between ",
    " depuis ": " from ",
    " vers ": " to ",
    " par ": " by ",
    " selon ": " according to ",
    " durant ": " during ",
    " pendant ": " during ",
    " après ": " after ",
    " avant ": " before ",
    "voici": "here is",
    "de type": "type",
    
    # Additional specific terms
    "# Modèle AHU (Air frais + Batterie de chauffage + Humidificateur)": "# AHU Model (Fresh Air + Heating Coil + Humidifier)",
    "#Récupération des données entrées by l'utilisateur": "#Retrieval of data entered by the user",
    "# Fin du Modèle AHU": "# End of AHU Model",
    "# Retrieve les données météo annuelles": "# Retrieve annual weather data",
    "# Calculationationation économique (exemple autoconsommation 40%)": "# Economic calculation (example 40% self-consumption)",
    "# Données courbes composites": "# Composite curve data",
    "Données": "Data",
    "Dans un procédé complexe, on dispose de plusieurs niveaux d'utilités": "In a complex process, there are several utility levels",
    "# Après avoir créé l'objet PinchAnalysis": "# After creating the PinchAnalysis object",
    "Sauvegarde des données": "Data Backup",
    "1. **Validation des données**": "1. **Data Validation**",
    "# 1. Récupérer les données météo historiques": "# 1. Retrieve historical weather data",
    "# 2. Fusionner with vos données de consommation": "# 2. Merge with your consumption data",
    "# 4. Créer le modèle IPMVP Option C": "# 4. Create the IPMVP Option C model",
    "# degree=2 : modèle polynomial de degré 2": "# degree=2: polynomial model of degree 2",
    "# Données période baseline": "# Baseline period data",
    "# Données période reporting": "# Reporting period data",
    "# Ajustement du modèle baseline": "# Baseline model fit",
    "Le module ``PinchAnalysis`` optimise la récupération de chaleur between flux chauds et froids": "The ``PinchAnalysis`` module optimizes heat recovery between hot and cold streams",
    "récupération de chaleur": "heat recovery",
    "flux chauds et froids": "hot and cold streams",
    "données": "data",
    "système": "system",
    "exemple": "example",
    "résultat": "result",
    "modèle": "model",
}

def translate_file(file_path):
    """Translate a single .rst file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply translations
    for french, english in TRANSLATIONS.items():
        content = content.replace(french, english)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Translated: {file_path}")
        return True
    else:
        print(f"  - No changes: {file_path}")
        return False

def main():
    """Main translation function"""
    docs_path = Path("A:/OneDrive/_Github_/EnergySystemModels-en/docs/source")
    
    # Find all .rst files
    rst_files = list(docs_path.rglob("*.rst"))
    
    print(f"Found {len(rst_files)} .rst files to process")
    print("=" * 60)
    
    translated_count = 0
    
    for rst_file in rst_files:
        if translate_file(rst_file):
            translated_count += 1
    
    print("=" * 60)
    print(f"\nTranslation complete!")
    print(f"Files translated: {translated_count}/{len(rst_files)}")

if __name__ == "__main__":
    main()
