# Screen Forge TS4
# Copyright (C) 2026 Apocrate_arto
# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import argparse
import shutil
import subprocess
import sys
import os

from services.service_package import ServicePackage


GFX_TYPE = 0x62ECC59A
IMAGE_ID = "119.png"

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
EXTENSIONS_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}

ROOT = Path(__file__).parent.resolve()
FFDEC = ROOT / "tools/ffdec/ffdec.sh"
TEMPLATE_PACKAGE = ROOT / "templates/loading_screen_template.package"
TEMPLATE_GFX = ROOT / "templates/transitionScreenMolecule.gfx"
CHEMINS_TS4_CANDIDATS = [
    Path.home() / ".wine/drive_c/Program Files (x86)/Origin Games/The Sims 4",
    Path.home() / ".steam/debian-installation/steamapps/common/The Sims 4",
    Path.home() / ".local/share/Steam/steamapps/common/The Sims 4",
    Path("C:/Program Files (x86)/Origin Games/The Sims 4"),
    Path("C:/Program Files/EA Games/The Sims 4"),
    Path("C:/Program Files (x86)/Steam/steamapps/common/The Sims 4"),
]

BUILD_DIR = ROOT / "build"
IMPORT_DIR = BUILD_DIR / "ffdec_import"
BUILD_GFX = BUILD_DIR / "transitionScreenMolecule.gfx"


def verifier_fichier(path: Path, label: str):
    if not path.exists():
        raise FileNotFoundError(f"{label} introuvable: {path}")


def nom_package(image: Path) -> str:
    return f"{image.stem}.package"


def generer_depuis_image(image: Path, sortie: Path):
    print(f"[Screen Forge] Image: {image.name}")

    if IMPORT_DIR.exists():
        shutil.rmtree(IMPORT_DIR)

    IMPORT_DIR.mkdir(parents=True, exist_ok=True)

    image_preparee = IMPORT_DIR / IMAGE_ID

    subprocess.run([
        "convert",
        str(image),
        "-auto-orient",
        "-colorspace", "sRGB",
        "-alpha", "set",
        "-resize", f"{TARGET_WIDTH}x{TARGET_HEIGHT}^",
        "-gravity", "center",
        "-extent", f"{TARGET_WIDTH}x{TARGET_HEIGHT}",
        "-strip",
        f"PNG32:{image_preparee}",
    ], check=True)

    subprocess.run([
        str(FFDEC),
        "-importImages",
        str(TEMPLATE_GFX),
        str(BUILD_GFX),
        str(IMPORT_DIR),
    ], check=True)

    package = ServicePackage(str(TEMPLATE_PACKAGE))
    package.lire_index()

    entree = trouver_gfx_dans_package(package)

    package.remplacer_ressource(entree, BUILD_GFX.read_bytes())
    package.sauvegarder(str(sortie))

    print(f"→ {sortie}")


def build(args):
    source = Path(args.image).resolve()
    output = Path(args.output).resolve()

    if source.name == "entree" and not source.exists():
        print("[Screen Forge] Création dossier entree/")
        source.mkdir()

    if output.name == "sortie":
        output.mkdir(exist_ok=True)

    if source.is_dir():
        images = [p for p in source.iterdir() if p.suffix.lower() in EXTENSIONS_IMAGES]

        if not images:
            print("[Screen Forge] Aucun fichier image valide dans entree/")
            return

    verifier_fichier(source, "Source")
    verifier_fichier(FFDEC, "FFDec")

    if not TEMPLATE_PACKAGE.exists() or not TEMPLATE_GFX.exists():
        raise FileNotFoundError(
            "Templates manquants.\n"
            "Lance : python screenforge.py setup-templates"
        )

    BUILD_DIR.mkdir(exist_ok=True)

    if source.is_file():
        if source.suffix.lower() not in EXTENSIONS_IMAGES:
            raise ValueError(f"Format non supporté: {source.suffix}")

        if output.suffix == ".package":
            sortie = output
        else:
            output.mkdir(parents=True, exist_ok=True)
            sortie = output / nom_package(source)

        generer_depuis_image(source, sortie)

    elif source.is_dir():
        output.mkdir(parents=True, exist_ok=True)

        images = [
            p for p in sorted(source.iterdir())
            if p.is_file() and p.suffix.lower() in EXTENSIONS_IMAGES
        ]

        if not images:
            raise ValueError(f"Aucune image supportée trouvée dans: {source}")

        for image in images:
            generer_depuis_image(image, output / nom_package(image))

        print(f"[Screen Forge] Batch terminé: {len(images)} package(s).")

    else:
        raise ValueError("Source invalide.")


def trouver_installations_ts4():
    installations = []

    for chemin in CHEMINS_TS4_CANDIDATS:
        chemin = chemin.expanduser()

        if chemin.exists() and (chemin / "Data").exists():
            installations.append(chemin)

    return installations


def setup_templates(args):
    installations = trouver_installations_ts4()

    if not installations:
        print("[Screen Forge] Aucune installation The Sims 4 détectée.")
        print("Lance manuellement Sims 4 Studio et suis docs/SETUP_TEMPLATES.md")
        return

    print("[Screen Forge] Installation TS4 détectée :")
    installation = installations[0]
    print(f"- {installation}")

    packages = trouver_packages_client(installation)

    if not packages:
        print("[Screen Forge] Aucun package client trouvé.")
        return

    print()
    print("[Screen Forge] Packages candidats :")
    for index, package in enumerate(packages[:20], start=1):
        print(f"{index}. {package}")

    print()
    print("Étapes à faire dans Sims 4 Studio :")
    print("1. Ouvre un des packages candidats ci-dessus")
    print("2. Va dans Warehouse")
    print("3. Cherche : transitionscreenmolecule")
    print("4. Exporte le ScaleForm GFX vers :")
    print(f"   {TEMPLATE_GFX}")
    print("5. Crée ou sauvegarde un package template vers :")
    print(f"   {TEMPLATE_PACKAGE}")
    print()
    print("Vérification attendue :")
    print("templates/")
    print("├── loading_screen_template.package")
    print("└── transitionScreenMolecule.gfx")


def trouver_packages_client(racine_ts4: Path):
    dossiers = [
        racine_ts4 / "Data" / "Client",
        racine_ts4 / "Delta",
    ]

    packages = []

    for dossier in dossiers:
        if dossier.exists():
            packages.extend(dossier.rglob("*.package"))

    return sorted(packages)


def detect(args):
    installations = trouver_installations_ts4()

    if not installations:
        print("[Screen Forge] Aucune installation The Sims 4 détectée.")
        print("Chemins testés :")
        for chemin in CHEMINS_TS4_CANDIDATS:
            print(f"- {chemin.expanduser()}")
        return

    print("[Screen Forge] Installation(s) détectée(s) :")

    for index, installation in enumerate(installations, start=1):
        print(f"{index}. {installation}")

        packages = trouver_packages_client(installation)
        print(f"   Packages trouvés : {len(packages)}")

        for package in packages[:10]:
            print(f"   - {package}")

        if len(packages) > 10:
            print("   - ...")


def trouver_gfx_dans_package(package: ServicePackage):
    gfx = [e for e in package.entrees if e.type_id == GFX_TYPE]

    if not gfx:
        raise ValueError("Aucune ressource ScaleForm GFX trouvée dans le template package.")

    if len(gfx) > 1:
        print("[Screen Forge] Plusieurs ressources GFX trouvées, utilisation de la première :")
        for e in gfx:
            print(f"- {e.type_id:08X}!{e.group_id:08X}!{e.instance_id:016X}")

    return gfx[0]


def clean(_args):
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    print("[Screen Forge] Build nettoyé.")


def main():
    parser = argparse.ArgumentParser(
        prog="screenforge",
        description="Générateur de loading screen pour The Sims 4."
    )

    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="Créer un ou plusieurs packages")
    build_cmd.add_argument(
        "image",
        nargs="?",
        default="entree",
        help="Image ou dossier (défaut: entree/)"
    )
    build_cmd.add_argument(
        "-o", "--output",
        default="sortie",
        help="Package de sortie ou dossier de sortie"
    )
    build_cmd.set_defaults(func=build)

    clean_cmd = sub.add_parser("clean", help="Supprimer les fichiers temporaires")
    clean_cmd.set_defaults(func=clean)
    detect_cmd = sub.add_parser("detect", help="Détecter l'installation The Sims 4")
    detect_cmd.set_defaults(func=detect)
    setup_cmd = sub.add_parser("setup-templates", help="Guider la création des templates")
    setup_cmd.set_defaults(func=setup_templates)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as erreur:
        print(f"[Screen Forge] ERREUR: {erreur}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
