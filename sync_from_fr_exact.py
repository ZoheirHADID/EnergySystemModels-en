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


def _directive_name(stripped: str) -> str | None:
    match = re.match(r"\.\.\s+([A-Za-z0-9_-]+)::", stripped)
    return match.group(1).lower() if match else None


def _is_path_like(stripped: str) -> bool:
    if not stripped:
        return False
    if " " in stripped or "\t" in stripped:
        return False
    return any(token in stripped for token in ("/", "\\", ".", "_"))


def translate_rst(content: str) -> str:
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
        }

        def restore_doc_target(match: re.Match[str]) -> str:
            value = match.group(0)
            for english, french in doc_target_map.items():
                value = value.replace(english, french)
            value = value.replace("009-pv-solaire/usage", "009-pv-solaire/utilisation")
            return value

        translated = re.sub(r":doc:`([^`]+)`", restore_doc_target, translated)
        output.append(" " * indent + translated + newline)

    return normalize_rst_underlines("".join(output))


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
    content = content.replace("copyright = '2024-2025, Zoheir HADID'", "copyright = '2024-2025, Zoheir HADID'")
    if "language =" not in content:
        content = content.replace("templates_path = ['_templates']\n", "templates_path = ['_templates']\nlanguage = 'en'\n")
    else:
        content = re.sub(r"language\s*=\s*['\"].*?['\"]", "language = 'en'", content)
    return content


def render_file(src: Path, dest: Path) -> str:
    suffix = src.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        text = src.read_text(encoding="utf-8")
        if src.name == "conf.py":
            output = translate_conf(text)
        elif suffix == ".json":
            output = translate_json(text)
        elif suffix == ".rst":
            output = translate_rst(text)
        else:
            output = translate_plain_text(text)
        dest.parent.mkdir(parents=True, exist_ok=True)
        previous = dest.read_text(encoding="utf-8") if dest.exists() else None
        dest.write_text(output, encoding="utf-8")
        return "updated" if previous != output else "unchanged"

    dest.parent.mkdir(parents=True, exist_ok=True)
    previous = dest.read_bytes() if dest.exists() else None
    data = src.read_bytes()
    dest.write_bytes(data)
    return "updated" if previous != data else "unchanged"


def iter_source_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def main() -> None:
    if not FR_ROOT.exists():
        raise SystemExit(f"French source tree not found: {FR_ROOT}")
    EN_ROOT.mkdir(parents=True, exist_ok=True)

    fr_files = iter_source_files(FR_ROOT)
    expected = {path.relative_to(FR_ROOT) for path in fr_files}
    existing = {path.relative_to(EN_ROOT) for path in iter_source_files(EN_ROOT)}

    created: list[str] = []
    updated: list[str] = []
    unchanged: list[str] = []
    removed: list[str] = []

    for src in fr_files:
        rel = src.relative_to(FR_ROOT)
        dest = EN_ROOT / rel
        existed = dest.exists()
        state = render_file(src, dest)
        if not existed:
            created.append(str(rel))
        elif state == "updated":
            updated.append(str(rel))
        else:
            unchanged.append(str(rel))

    for rel in sorted(existing - expected):
        target = EN_ROOT / rel
        target.unlink()
        removed.append(str(rel))

    for directory in sorted((path for path in EN_ROOT.rglob("*") if path.is_dir()), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass

    report = [
        "# EnergySystemModels EN Synchronization Report",
        "",
        "Source of truth: `EnergySystemModels-fr/docs/source`.",
        "Destination: `EnergySystemModels-en/docs/source`.",
        "",
        f"- Created: {len(created)}",
        f"- Updated: {len(updated)}",
        f"- Unchanged: {len(unchanged)}",
        f"- Removed obsolete files: {len(removed)}",
        "",
        "## Created",
        *[f"- `{item}`" for item in created],
        "",
        "## Updated",
        *[f"- `{item}`" for item in updated],
        "",
        "## Removed",
        *[f"- `{item}`" for item in removed],
        "",
        "## Notes",
        "- Binary assets are copied exactly from the French documentation.",
        "- Text files are translated with the deterministic local glossary.",
        "- File names and toctree paths intentionally match the French source tree.",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Created: {len(created)}")
    print(f"Updated: {len(updated)}")
    print(f"Unchanged: {len(unchanged)}")
    print(f"Removed obsolete files: {len(removed)}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
