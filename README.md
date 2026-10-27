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
assets_1/      — maquettes sources (EN, JPEG)
```

## Maquettes

Les écrans actifs sont dans `assets/screens/` en `.webp` (fond transparent ; originaux dans `assets/screens/source/`). Les anciennes maquettes PNG sont archivées dans `assets/screens/archive/`. La version EN du site (`en/index.html`) pointe vers `assets_1/`.

| Fichier screens/ | Fichier assets_1/ | Section |
| --- | --- | --- |
| `01_accueil.webp` | `Page d'acceuil.jpeg` | Hero |
| `02_explorer_activites.webp` | `Discover.jpeg` | Expérience — explorer |
| `03_detail_activite.webp` | `Manga night.jpeg` | Expérience — explorer |
| `07_mon_mood.webp` | `my mood.jpeg` | Expérience — moment pour soi |
| `09_tips_vibes.webp` | `Tips.jpeg` | Expérience — habitudes |
| `05_mon_crew.webp` | `my crew.jpeg` | Crew |

Tant qu'un fichier manque, un cadre en pointillés indique son nom.

## Éléments non fournis (non inventés)

- Logo : `assets/brand/` (icône SVG, version horizontale SVG, favicons PNG, `og-image.png`).
- Photographies : `assets/photos/` — Iwaria Inc et Muhammad-Taha Ibrahim, via Unsplash. Crédit affiché dans le pied de page.
- Section « Contribuer » : les boutons ouvrent un ticket sur `github.com/Charmel7/vibes/issues`. À remplacer par un formulaire ou une adresse officielle quand elle existe.
