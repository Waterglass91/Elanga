# The Elanga Experience

Concept éditorial indépendant autour du parcours d'Anthony Elanga. Non affilié à Anthony Elanga, à ses clubs ni à ses partenaires tant qu'aucune autorisation n'a été donnée.

Cahier des charges : [`ELANGA_DESIGN_BRIEF.md`](ELANGA_DESIGN_BRIEF.md) · Audit : [`docs/M0-AUDIT.md`](docs/M0-AUDIT.md) · À valider : [`docs/EDITORIAL-CHECKLIST.md`](docs/EDITORIAL-CHECKLIST.md)

## Pages

| Page | Contenu |
|---|---|
| `index.html` | Experience : intro signature, hero, Statement, Motion, Journey (4 étapes), Person, Next chapter |
| `journey.html` | Les 7 chapitres en format documentaire, rail de navigation, Milestones |
| `person.html` | Racines, Mindset, Style, Héritage, Ambitions |
| `motion.html` | Le film, Stills, Moments clés datés |

## Structure

```
css/tokens.css        couleurs, typographies, espacements, durées (brief)
css/base.css          reset, grille, utilitaires
css/experience.css    intro, en-tête, menu, hero, fenêtre du film
css/home.css          sections de l'accueil, révélations
css/pages.css         Journey, Person, Motion
js/signature.js       moteur d'écriture de la signature
js/main.js            comportements partagés par toutes les pages
data/signature.js     géométrie de la signature + tracés du stylo
fonts/                Anton, Inter (OFL, auto-hébergées)
media/                vidéo, photos N&B, variantes WebP du hero
tools/build_pages.py  génère les 4 pages HTML (en-tête, menu, pied de page communs)
tools/skeleton.py     calcule les tracés du stylo à partir de la signature
tools/build_signature_data.py  produit data/signature.js
```

Le contenu des pages se modifie dans `tools/build_pages.py`, puis :

```
python3 tools/build_pages.py
```

## Aperçu local

```
python3 -m http.server 8000
# http://localhost:8000/
```

Aucune dépendance, aucun build obligatoire. Tous les chemins sont relatifs : compatible GitHub Pages sous `/Elanga/`.

## Design system

Obsidian `#090A0C` · Carbon `#202228` · Bone `#F2F0EA` · Titanium `#ACB2BA` · Volt `#B8FF36` (≈ 5 %)
Anton (titres), Inter (texte), signature manuscrite (logo).
