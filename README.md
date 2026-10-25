# VIBES — landing page

Page statique (HTML, CSS, JS sans dépendance, police Inter via Google Fonts).
Illustrations (autocollants, personnages, icônes) : SVG intégrés dans `index.html`, aux couleurs de la palette VIBES.
Tokens issus de `vibes_design_system_v1.md`.

## Langues

- Français : `index.html` (source, à modifier en premier).
- Anglais : `en/index.html`, **généré** depuis le français. Ne pas le modifier à la main.

Après chaque modification du texte français :

```
python3 tools/make_en.py
```

Le script s'arrête et indique la phrase à mettre à jour dans `tools/make_en.py` si un texte français a changé.
Les noms du projet (Mon Mood, My Safe Place, Tips VIBES, Étincelles, Crew, Souvenirs) restent en français, avec « Sparks » en explication à la première mention.
Les captures d'écran de l'application restent en français : elles sont à traduire côté maquettes.

## Lancer en local

```
python3 -m http.server 8000
```

Puis ouvrir http://localhost:8000.

## Maquettes à ajouter

Les écrans ne sont pas recréés : la page utilise tes PNG du Drive, tels quels.
Les écrans actuels (générés, en anglais) sont dans `assets/screens/` en `.jpg`. Les anciens sont dans `assets/screens/archive/`. Correspondance :

| Fichier | Section |
| --- | --- |
| `01_accueil.jpg` | Hero |
| `02_explorer_activites.jpg` | Expérience, explorer |
| `03_detail_activite.jpg` | Expérience, explorer |
| `07_mon_mood.jpg` | Expérience, moment pour soi |
| `09_tips_vibes.jpg` | Expérience, habitudes |
| `05_mon_crew.jpg` | Crew |

Tant qu'un fichier manque, un cadre en pointillés indique son nom.

## Éléments non fournis (non inventés)

- Logo : redessiné en vectoriel dans `assets/brand/` (icône, version verticale, version horizontale, favicons, `og-image.png`). Mot en Poppins Bold converti en tracés.
- Photographies : trois photos Unsplash (Iwaria Inc, Muhammad-Taha Ibrahim) dans `assets/photos/`, versions web optimisées. Les originaux sont dans `assets/photos/source/`. Crédit affiché dans le pied de page.
- Section « Contribuer » : les boutons ouvrent un nouveau ticket sur `github.com/Charmel7/vibes/issues` (public). À remplacer par un formulaire ou une adresse officielle quand elle existe.
- Contact : adresse e-mail de l'équipe (landing, PDF). Pas de réseaux sociaux, pages légales, lien de téléchargement ou d'inscription.
