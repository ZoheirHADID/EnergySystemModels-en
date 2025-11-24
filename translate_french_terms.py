# -*- coding: utf-8 -*-
"""
Translation Script for EnergySystemModels Documentation
Translates French text to English in .rst files
"""

import os
import re
from pathlib import Path

# Translation dictionary for common terms
TRANSLATIONS = {
    # Titles and headers
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
    
    # Common phrases
    "L'image ci-dessous montre": "The image below shows",
    "Le code suivant montre": "The following code shows",
    "Le diagramme": "The diagram",
    "Les tableaux ci-dessous montrent": "The tables below show",
    "les résultats des calculs pour chaque composant": "the calculation results for each component",
    "de la CTA": "of the AHU",
    "points de fonctionnement": "operating points",
    "schéma de la CTA": "AHU schematic",
    
    # Technical terms
    "Température": "Temperature",
    "température": "temperature",
    "Pression": "Pressure",
    "pression": "pressure",
    "Débit": "Flow rate",
    "débit": "flow rate",
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
    
    # Units and parameters
    "d'entrée en degrés Celsius": "inlet in degrees Celsius",
    "d'entrée en bars": "inlet in bars",
    "volumétrique standard en mètres cubes par heure": "standard volumetric in cubic meters per hour",
    "volumétrique normal en mètres cubes par heure": "normal volumetric in cubic meters per hour",
    "volumétrique en mètres cubes par heure": "volumetric in cubic meters per hour",
    "massique en kilogrammes par heure": "mass in kilograms per hour",
    "massique en kilogrammes par seconde": "mass in kilograms per second",
    "d'entrée en Kelvin": "inlet in Kelvin",
    "de sortie en Kelvin": "outlet in Kelvin",
    
    # Section titles
    "Données Météorologiques": "Meteorological Data",
    "Données Météo": "Weather Data",
    "PV Solaire": "Solar PV",
    "Analyse de Pincement": "Pinch Analysis",
    
    # Other common terms
    "en fonction de": "as a function of",
    "permet de": "allows to",
    "permettent de": "allow to",
    "pour calculer": "to calculate",
    "utilise les équations suivantes": "uses the following equations",
    "sont automatiquement calculés": "are automatically calculated",
    "coordonnées GPS": "GPS coordinates",
    "la production": "the production",
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
