# Configuration des templates (obligatoire)

Screen Forge TS4 ne fournit pas les fichiers templates pour des raisons légales.

Vous devez les extraire vous-même depuis votre installation de The Sims 4.

---

## Étape 1 — Trouver les fichiers du jeu

Localisation typique :

- Linux (Wine/Steam/EA App) :
  ~/.wine/drive_c/Program Files (x86)/Origin Games/The Sims 4/
  ~/.steam/debian-installation/steamapps/common/The Sims 4

- Windows :
  C:\Program Files (x86)\Origin Games\The Sims 4\

---

## Étape 2 — Trouver le fichier contenant le loading screen

Recherchez dans :

```text
Data/Client/
```

Fichiers typiques :

```text
FullBuild0.package
FullBuild1.package
ClientFullBuild*.package
```

---

## Étape 3 — Extraire avec Sims 4 Studio

1. Ouvrir Sims 4 Studio
2. Menu : Tools → Extract Tuning / Extract Package
3. Ouvrir un fichier `FullBuild*.package`
4. Aller dans l’onglet **Warehouse**
5. Rechercher :

```text
ScaleFormGFXResource
```

---

## Étape 4 — Identifier le bon GFX

Chercher un nom similaire à :

```text
transitionscreenmolecule
```

Puis récupérer la clé :

```text
Type:     62ECC59A
Group:    00000000
Instance: XXXXXXXX
```

---

## Étape 5 — Exporter le GFX

Dans Sims 4 Studio :

```text
Click droit → Export to file
```

Sauvegarder :

```text
templates/transitionScreenMolecule.gfx
```

---

## Étape 6 — Créer le template package

Toujours dans Sims 4 Studio :

```text
File → New → Package
```

Importer le GFX :

```text
Import → sélectionner le fichier .gfx
```

Puis sauvegarder :

```text
templates/loading_screen_template.package
```

---

## Vérification

Structure attendue :

```text
templates/
├── loading_screen_template.package
└── transitionScreenMolecule.gfx
```

---

## Vous pouvez maintenant utiliser Screen Forge

```bash
python screenforge.py build
```

---

## Notes importantes

* Ne partagez pas ces fichiers publiquement
* Ils appartiennent à EA / The Sims 4
* Screen Forge fonctionne uniquement avec vos propres copies
