"""
Script pour synchroniser et traduire automatiquement les articles
de EnergySystemModels-fr vers EnergySystemModels-en
"""

import os
import shutil
from pathlib import Path

# Chemins de base
FR_PATH = Path(r"A:\OneDrive\_Github_\EnergySystemModels-fr\docs\source")
EN_PATH = Path(r"A:\OneDrive\_Github_\EnergySystemModels-en\docs\source")

# Mapping des fichiers à traduire (FR -> EN)
# Format: "chemin/fichier_fr.rst": "chemin/fichier_en.rst"
TRANSLATIONS_NEEDED = {
    # 006-pinch_analysis
    "006-pinch_analysis/introduction.rst": "006-pinch_analysis/introduction.rst",
    "006-pinch_analysis/methode.rst": "006-pinch_analysis/method.rst",
    "006-pinch_analysis/exemples.rst": "006-pinch_analysis/examples.rst",
    
    # 007-ipmvp
    "007-ipmvp/index.rst": "007-ipmvp/index.rst",
    "007-ipmvp/introduction.rst": "007-ipmvp/introduction.rst",
    "007-ipmvp/protocole.rst": "007-ipmvp/protocol.rst",
    "007-ipmvp/modeles_mathematiques.rst": "007-ipmvp/mathematical_models.rst",
    "007-ipmvp/exemples.rst": "007-ipmvp/examples.rst",
    
    # 008-meteo
    "008-meteo/index.rst": "008-meteo/index.rst",
    "008-meteo/degres_jours.rst": "008-meteo/degree_days.rst",
    "008-meteo/meteociel.rst": "008-meteo/meteociel.rst",
    "008-meteo/openweathermap.rst": "008-meteo/openweathermap.rst",
    
    # 009-pv-solaire
    "009-pv-solaire/index.rst": "009-pv-solaire/index.rst",
    "009-pv-solaire/introduction.rst": "009-pv-solaire/introduction.rst",
    "009-pv-solaire/utilisation.rst": "009-pv-solaire/usage.rst",
    "009-pv-solaire/exemples.rst": "009-pv-solaire/examples.rst",
    
    # 011-cee
    "011-cee/index.rst": "011-cee/index.rst",
    "011-cee/introduction.rst": "011-cee/introduction.rst",
    "011-cee/module_cee.rst": "011-cee/cee_module.rst",
}

# Dictionnaire de traduction des termes courants
TERM_TRANSLATIONS = {
    # Titres et sections
    "Utilisation": "Usage",
    "Exemple": "Example",
    "Exemples": "Examples",
    "Introduction": "Introduction",
    "Méthode": "Method",
    "Méthodes disponibles": "Available Methods",
    "Protocole": "Protocol",
    "Modèles mathématiques": "Mathematical Models",
    "Module": "Module",
    
    # Termes techniques
    "Analyse de pincement": "Pinch Analysis",
    "Analyse Pinch": "Pinch Analysis",
    "Courbes composites": "Composite Curves",
    "Grande courbe composite": "Grand Composite Curve",
    "Réseau d'échangeurs": "Heat Exchanger Network",
    "Point Pinch": "Pinch Point",
    "Utilité chaude": "Hot Utility",
    "Utilité froide": "Cold Utility",
    "Flux chauds": "Hot Streams",
    "Flux froids": "Cold Streams",
    "Température": "Temperature",
    "Pression": "Pressure",
    "Débit": "Flow Rate",
    "Chaleur": "Heat",
    "Énergie": "Energy",
    "Puissance": "Power",
    
    # Instructions
    "Créer l'objet": "Create the object",
    "Afficher les résultats": "Display results",
    "Calculer": "Calculate",
    "Visualiser": "Visualize",
    
    # DataFrames
    "DataFrame requis": "Required DataFrame",
    "Résultats": "Results",
    "DataFrames de résultats": "Result DataFrames",
    "Attributs calculés": "Calculated Attributes",
    
    # Unités
    "[°C]": "[°C]",
    "[kW]": "[kW]",
    "[kW/K]": "[kW/K]",
    "[K]": "[K]",
    "[m]": "[m]",
    "[kg/s]": "[kg/s]",
    
    # Commentaires
    "Température initiale": "Initial temperature",
    "Température finale": "Final temperature",
    "Débit capacité": "Capacity flow rate",
    "ΔTmin": "ΔTmin",
}

def translate_content(content):
    """
    Traduit le contenu du français vers l'anglais
    en utilisant le dictionnaire de traductions
    """
    translated = content
    
    for fr_term, en_term in TERM_TRANSLATIONS.items():
        translated = translated.replace(fr_term, en_term)
    
    return translated

def sync_missing_files():
    """
    Synchronise les fichiers manquants de FR vers EN
    """
    print("=" * 60)
    print("Synchronisation des fichiers FR → EN")
    print("=" * 60)
    
    for fr_file, en_file in TRANSLATIONS_NEEDED.items():
        fr_path = FR_PATH / fr_file
        en_path = EN_PATH / en_file
        
        if not fr_path.exists():
            print(f"⚠️  Fichier FR introuvable: {fr_file}")
            continue
        
        if en_path.exists():
            print(f"✓  Existe déjà: {en_file}")
            continue
        
        # Créer le dossier de destination si nécessaire
        en_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Lire le contenu français
        with open(fr_path, 'r', encoding='utf-8') as f:
            fr_content = f.read()
        
        # Traduire le contenu
        en_content = translate_content(fr_content)
        
        # Écrire le fichier anglais
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(en_content)
        
        print(f"✓  Créé et traduit: {en_file}")
    
    print("\n" + "=" * 60)
    print("Synchronisation terminée")
    print("=" * 60)

def list_missing_files():
    """
    Liste tous les fichiers présents en FR mais absents en EN
    """
    print("\n" + "=" * 60)
    print("Fichiers manquants en EN")
    print("=" * 60)
    
    missing_count = 0
    
    for fr_file, en_file in TRANSLATIONS_NEEDED.items():
        en_path = EN_PATH / en_file
        if not en_path.exists():
            print(f"❌ {en_file}")
            missing_count += 1
    
    print(f"\nTotal: {missing_count} fichiers manquants")
    print("=" * 60)

if __name__ == "__main__":
    print("\n🔄 Début de la synchronisation des documentations")
    print(f"Source (FR): {FR_PATH}")
    print(f"Destination (EN): {EN_PATH}\n")
    
    # Lister les fichiers manquants
    list_missing_files()
    
    # Demander confirmation
    response = input("\nVoulez-vous procéder à la synchronisation? (o/n): ")
    
    if response.lower() == 'o':
        sync_missing_files()
        print("\n✅ Synchronisation complète!")
    else:
        print("\n❌ Synchronisation annulée")
