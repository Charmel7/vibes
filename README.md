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

Les écrans actifs sont dans `assets/screens/` en `.webp` (fond transparent ; originaux dans `assets/screens/source/`). Les anciennes maquettes PNG sont archivées dans `assets/screens/archive/`. Les deux versions du site utilisent aussi les visuels de `assets_1/` :

| Fichier assets_1/ | Section |
| --- | --- |
| `page_accueil.png` | Hero |
| `derrière_l'écran.jpeg` | Constat — dehors |
| `Discover.jpeg` | Approche — découvrir |
| `equip yourself.jpeg` | Approche — s'outiller |
| `anchor.jpeg` | Approche — ancrer |

Les autres maquettes de `assets_1/` illustrent l'expérience de l'application.

## Éléments non fournis (non inventés)

- Logo : `assets/brand/` (icône SVG, version horizontale SVG, favicons PNG, `og-image.png`).
- Photographies : `assets/photos/` — Iwaria Inc et Muhammad-Taha Ibrahim, via Unsplash. Crédit affiché dans le pied de page.
- Section « Contribuer » : les boutons ouvrent un ticket sur `github.com/Charmel7/vibes/issues`. À remplacer par un formulaire ou une adresse officielle quand elle existe.
