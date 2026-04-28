#  _______                                   _______                         
# |     __|.----.----.-----.-----.-----.    |    ___|.-----.----.-----.-----.
# |__     ||  __|   _|  -__|  -__|     |    |    ___||  _  |   _|  _  |  -__|
# |_______||____|__| |_____|_____|__|__|    |___|    |_____|__| |___  |_____|
#                                                               |_____|      

# Screen Forge TS4

Screen Forge is an open-source tool for automatically generating **custom loading screens for The Sims 4**.

---

## Features

* Automatic generation of loading screens (.package)
* Multi-image support (batch processing)
* Automatic conversion (JPG, PNG, WebP → PNG)
* Smart resizing (1920×1080)
* FFDec integration (ScaleForm GFX)
* Automatic detection of the The Sims 4 installation

---

## Usage

### 1. Prepare the images

Place your images in the following folder:

```text
entree/
```

---

### 2. Generate loading screens

```bash
python screenforge.py build
```

Output:

```text
sortie/
```

---

### 3. Clean up

```bash
python screenforge.py clean
```

---

## Required Configuration

Screen Forge does not provide game files.

You must extract the templates yourself:

See: [docs/SETUP_TEMPLATES.md](docs/SETUP_TEMPLATES.md)

Expected files:

```text
templates/
├── loading_screen_template.package
└── transitionScreenMolecule.gfx
```

---

## Automatic Game Detection

```bash
python screenforge.py detect
```

---

## Dependencies

* Python 3.10+
* ImageMagick (`convert`)
* FFDec (included in `tools/ffdec/`)

---

## Licence

Screen Forge is distributed under the **GPL-3.0-or-later** licence.

---

## Third-Party Components

Screen Forge includes:

* **FFDec / JPEXS Free Flash Decompiler**

  * Licence: GPL-3.0-or-later
  * Directory: `tools/ffdec/`

See [THIRD_PARTY.md](THIRD_PARTY.md)

---

## Disclaimer

* Files from The Sims 4 belong to **Electronic Arts**
* Templates are not distributed with this tool
* You must use your own game files

---

## Author

Apocrate_arto

---

## Contribution

Contributions are welcome!

