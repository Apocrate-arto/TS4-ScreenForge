#  _______                                   _______                         
# |     __|.----.----.-----.-----.-----.    |    ___|.-----.----.-----.-----.
# |__     ||  __|   _|  -__|  -__|     |    |    ___||  _  |   _|  _  |  -__|
# |_______||____|__| |_____|_____|__|__|    |___|    |_____|__| |___  |_____|
#                                                               |_____|      

# Screen Forge TS4

Screen Forge est un outil open-source permettant de générer automatiquement des **loading screens personnalisés pour The Sims 4**.

---

## Fonctionnalités

- Génération automatique de loading screens (.package)
- Support multi-images (batch)
- Conversion automatique (JPG, PNG, WebP → PNG)
- Redimensionnement intelligent (1920x1080)
- Intégration de FFDec (ScaleForm GFX)
- Détection automatique de l’installation The Sims 4

---

## Utilisation

### 1. Préparer les images

Place tes images dans le dossier :

```text
entree/
```

---

### 2. Générer les loading screens

```bash
python screenforge.py build
```

Résultat :

```text
sortie/
```

---

### 3. Nettoyer

```bash
python screenforge.py clean
```

---

## Configuration obligatoire

Screen Forge ne fournit pas les fichiers du jeu.

Tu dois extraire toi-même les templates :

Voir : [docs/SETUP_TEMPLATES.md](docs/SETUP_TEMPLATES.md)

Ou tu peux utiliser l’assistant intégré :

```bash
python screenforge.py setup-templates
```

Fichiers attendus :

```text
templates/
├── loading_screen_template.package
└── transitionScreenMolecule.gfx
```

---

## Détection automatique du jeu

```bash
python screenforge.py detect
```

---

## Dépendances

* Python 3.10+
* ImageMagick (`convert`)
* FFDec (inclus dans `tools/ffdec/`)

---

## Licence

Screen Forge est distribué sous licence **GPL-3.0-or-later**.

---

## Composants tiers

Screen Forge inclut :

* **FFDec / JPEXS Free Flash Decompiler**

  * Licence : GPL-3.0-or-later
  * Dossier : `tools/ffdec/`

Voir [THIRD_PARTY.md](THIRD_PARTY.md)

---

## Avertissement

* Les fichiers The Sims 4 appartiennent à **Electronic Arts**
* Les templates ne sont pas distribués avec cet outil
* Tu dois utiliser tes propres fichiers du jeu

---

## Auteur

Apocrate_arto

---

## Contribution

Les contributions sont bienvenues !
