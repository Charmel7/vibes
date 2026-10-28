# VIBES — landing page

Page statique (HTML, CSS, JS sans dépendance, polices Inter et Syne via Google Fonts).
Illustrations (autocollants, icônes) : SVG intégrés dans `index.html`, aux couleurs de la palette VIBES.

## Équipe

| Nom | Rôle |
| --- | --- |
| **Affoukou Dossou Ossan Prosper Charmel** | Team Lead · System Thinker & Data Scientist |
| **ADANLAO Adéyinka Laurinda** | ML Engineer en formation & Développeuse Front-end |
| **Judicaël Karol DOBOEVI** | Business Development & Product Marketing Manager |

UNSTIM, Abomey, Bénin.

## Langues

- Français : `index.html` (source, à modifier en premier).
- Anglais : `en/index.html`.

## Lancer en local

```
python3 -m http.server 8000
```

Puis ouvrir http://localhost:8000.

## Structure des assets

```
assets/
  brand/       — logo, favicons, og-image
  photos/      — photos Unsplash (Iwaria Inc, Muhammad-Taha Ibrahim)
  screens/     — maquettes JPG actives (EN)
  screens/archive/ — anciennes maquettes PNG (FR)
  team/        — photos de l'équipe (charmel.jpg, laurinda.jpg, judicael.jpg)
assets_1/      — maquettes et visuels sources du site
```

## Maquettes

Les 5 écrans de la galerie sont dans `assets/screens/` en `.webp` (fond transparent), détourés à partir des JPEG de `assets_1/` (les JPEG restent les sources). Les anciennes versions sont dans `assets/screens/source/` et `archive/`. Les autres visuels de `assets_1/` :

| Fichier assets_1/ | Section |
| --- | --- |
| `page_accueil.png` | Hero |
| `derrière_l'écran.jpeg` | Constat — dehors |
| `Discover.jpeg` | Approche — découvrir |
| `equip yourself.jpeg` | Approche — s'outiller |
| `anchor.jpeg` | Approche — ancrer |

Les maquettes sont générées avec des outils d'IA (mention sur le site et dans le dossier de candidature).

## Branche `refonte`

Version raccourcie du site (9 sections au lieu de 15). Pour la prévisualiser : Settings → Pages → Branch `refonte`. À fusionner dans `main` après validation, puis remettre Pages sur `main`.

## Éléments non fournis (non inventés)

- Logo : `assets/brand/` (icône SVG, version horizontale SVG, favicons PNG, `og-image.png`).
- Photographies : `assets/photos/` — Iwaria Inc et Muhammad-Taha Ibrahim, via Unsplash. Crédit affiché dans le pied de page.
- Section « Contribuer » : les boutons ouvrent un ticket sur `github.com/Charmel7/vibes/issues`. À remplacer par un formulaire ou une adresse officielle quand elle existe.
