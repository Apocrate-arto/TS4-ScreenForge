# Template configuration (required)

Screen Forge TS4 does not provide the template files for legal reasons.

You must extract them yourself from your own The Sims 4 installation.

---

## Step 1 — Find the game files

Typical locations:

- Linux (Wine/Steam/EA App):
  ~/.wine/drive_c/Program Files (x86)/Origin Games/The Sims 4/
  ~/.steam/debian-installation/steamapps/common/The Sims 4

- Windows:
  C:\Program Files (x86)\Origin Games\The Sims 4\

---

## Step 2 — Find the file containing the loading screen

Look in:

```text
Data/Client/
```

Typical files:

```text
FullBuild0.package
FullBuild1.package
ClientFullBuild*.package
```

---

## Step 3 — Extract with Sims 4 Studio

1. Open Sims 4 Studio
2. Menu: Tools → Extract Tuning / Extract Package
3. Open a `FullBuild*.package` file
4. Go to the **Warehouse** tab
5. Search for:

```text
ScaleFormGFXResource
```

---

## Step 4 — Identify the correct GFX

Look for a name similar to:

```text
transitionscreenmolecule
```

Then note the key:

```text
Type:     62ECC59A
Group:    00000000
Instance: XXXXXXXX
```

---

## Step 5 — Export the GFX

In Sims 4 Studio:

```text
Right-click → Export to file
```

Save it as:

```text
templates/transitionScreenMolecule.gfx
```

---

## Step 6 — Create the template package

Still in Sims 4 Studio:

```text
File → New → Package
```

Import the GFX:

```text
Import → select the .gfx file
```

Then save it as:

```text
templates/loading_screen_template.package
```

---

## Verification

Expected structure:

```text
templates/
├── loading_screen_template.package
└── transitionScreenMolecule.gfx
```

---

## You can now use Screen Forge

```bash
python screenforge.py build
```

---

## Important notes

* Do not share these files publicly
* They belong to EA / The Sims 4
* Screen Forge only works with your own copies
