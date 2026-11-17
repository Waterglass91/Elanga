# M0 — Audit et plan de développement

Branche : `redesign/elanga-experience` · Base : `main` @ `462b673` · Date : 17 novembre 2026
Référence : `ELANGA_DESIGN_BRIEF.md` v1.0

---

## 1. Inventaire du dépôt

| Élément | État actuel |
|---|---|
| `index.html` | 717 lignes, 181 Ko. HTML, CSS et JS dans un seul fichier. Aucun build, aucun `package.json`. |
| Signature | Géométrie SVG d'origine + 74 tracés de masque (squelette calculé par `tools/skeleton.py`). Le tracé est **dupliqué deux fois** dans la page (intro + clôture) : environ 140 Ko sur 181. |
| `media/elanga-manchester.mp4` | 15,8 Mo, H.264 720×900 (portrait 4:5), 2 min 10, audio AAC. Pas de sous-titres. |
| Photos | 9 JPEG N&B entre 627 et 720 px de large (95 à 199 Ko). Pas de `srcset`, pas de WebP/AVIF, pas de `width`/`height` déclarés. |
| `assets/` | Signature vectorielle d'origine, noir et blanc. |
| Dépendances tierces | Google Fonts uniquement (Bebas Neue, Inter), appelé depuis fonts.googleapis.com. |
| Chemins | Tous relatifs (`media/…`) : compatibles avec le sous-chemin `/Elanga/`. |

## 2. Inventaire des sections (page unique)

1. Intro : signature animée (≈ 3,6 s), « Entrer », « Passer l'intro »
2. Film : « ALWAYS FORWARD. » + vidéo encadrée, **son activé au clic sur Entrer**
3. Beyond the game : manifeste + portrait N&B
4. The journey : 7 chapitres avec photo
5. The man : 4 blocs, **photos manquantes (emplacements visibles)**
6. Milestones : 8 dates
7. Clôture : signature réécrite, contact « à définir »
8. Footer, « Revoir l'intro »

## 3. Écarts entre l'existant et le brief

| Sujet | Existant | Brief | Action |
|---|---|---|---|
| Palette | Obsidian #0B0B0D, or #C6A773 | #090A0C, Carbon #202228, Bone #F2F0EA, Titanium #ACB2BA, **Volt #B8FF36** | Remplacer par des tokens CSS |
| Titres | Bebas Neue | Anton (ou condensée équivalente) | Anton (licence OFL, libre) |
| Texte | Inter | Manrope ou Inter | Garder Inter |
| Intro | ≈ 3,6 s | < 3 s, mémorisée pour les visites suivantes | Accélérer, `localStorage` |
| Son vidéo | Activé à l'entrée | **Muet par défaut** | ⚠️ décision à prendre (voir §6) |
| Hero | Titre + vidéo encadrée | Plein écran, `ANTHONY / ELANGA.`, `BEYOND SPEED.` | Refonte M1 |
| Statut | Titre « Site officiel » | Concept indépendant tant que non autorisé | Mention discrète + titre corrigé |
| Langues | Sélecteur FR/EN/SV inactif | Pas de contrôle trompeur | Retirer jusqu'aux traductions |
| The man | Emplacements « Photo à venir » | Pas de faux visuels | Liste éditoriale au lieu d'emplacements |
| Contact | « à définir » | Seulement si approuvé | Masquer ou libellé clair |
| Polices | Google Fonts externe | Licences vérifiées | Auto-hébergement des woff2 (RGPD, performance) |

## 4. Audit des droits (à vérifier par le propriétaire)

| Fichier | Source | Statut |
|---|---|---|
| `photo-01.jpg` | Getty Images (© Corbis via Getty Images) | ❌ Licence requise |
| `photo-02, 04, 05, 06, 07` | Captures de publications Instagram | ❌ Photographe et droits à identifier |
| `bw-56`, `bw-portrait`, `poster` | Images extraites de la vidéo | ❌ Dépend des droits de la vidéo |
| `elanga-manchester.mp4` | Vidéo publiée sur Instagram (images de Manchester United) | ❌ Droits club / auteur à vérifier |
| Signature | Fournie par le client | ✅ À confirmer par écrit |

**Qualité** : toutes les photos font moins de 720 px de large. Elles suffisent pour un format portrait dans une colonne, mais **pas pour un plein écran** sur ordinateur (flou visible au-delà d'environ 800 px). Le hero plein écran demandé nécessite au moins un visuel HD (≥ 2400 px de large).

## 5. Faits à faire valider

Repris du portrait biographique fourni, non vérifiés de façon indépendante : transferts (montants « estimés »), statistiques Forest 2024-2025, doublé au Camp Nou, buts en Coupe du monde 2026, naissance de sa fille, numéro 19. Mention « passionné de mode » : information client, non sourcée publiquement.

## 6. Décisions à prendre avant M1

1. **Son de la vidéo** : le brief impose « muet par défaut » ; tu avais demandé le son automatique. Proposition : muet par défaut + gros bouton « Son » bien visible.
2. **Hero plein écran** : avec les visuels actuels, je propose un hero en **diptyque** (photo N&B pleine hauteur sur une moitié, typographie sur l'autre) qui reste net. Le vrai plein écran viendra avec un visuel HD.
3. **Titre derrière le sujet** : tu avais trouvé moche le texte coupé derrière la vidéo. Proposition : `ANTHONY / ELANGA.` **à côté** du sujet, jamais masqué.
4. **Mention de statut** : « Concept éditorial indépendant » en pied de page et dans le titre de la page.

## 7. Structure de fichiers prévue

Toujours en HTML/CSS/JS sans framework (pas de raison concrète d'introduire React/Vite).

```
index.html                 accueil (Experience)
journey.html               M3 : les 7 chapitres complets
person.html                M3
motion.html                M3
partnerships.html          M4
css/tokens.css             couleurs, typo, espacements, durées
css/base.css               reset, grille 12 colonnes, utilitaires
css/sections/*.css         un fichier par section
js/signature.js            moteur d'écriture (données du tracé chargées une seule fois)
js/main.js                 navigation, menu, progression, vidéo, révélations
data/signature.json        géométrie + tracés de masque (sortis du HTML)
data/journey.json          contenu des 7 chapitres (une seule source)
fonts/                     Anton, Inter (woff2, auto-hébergés)
media/                     images en plusieurs tailles (AVIF/WebP/JPEG) + vidéo + poster + sous-titres .vtt
```

## 8. Jalons

| Jalon | Contenu | Validation |
|---|---|---|
| **M1** | Tokens, polices, navigation + menu plein écran, intro < 3 s mémorisée, hero cinématographique, repli si la vidéo échoue | Captures 360 / 390 / 768 / 1024 / 1440 / 1920 px |
| M2 | Statement (bascule vers fond Bone), Motion, 4 teasers Journey, Person, Next Chapter | Captures + test clavier et mouvement réduit |
| M3 | Pages Journey, Person, Motion | Idem |
| M4 | Partenariats, media kit (contenus marqués « à valider »), QA accessibilité / performance / licences | Rapport complet |

Chaque jalon : commits dédiés sur la branche, captures ordinateur et mobile, aperçu privé. Pull request vers `main` seulement à la fin, après validation. **Aucune modification de `main`.**

## 9. Aperçu local

```
git checkout redesign/elanga-experience
python3 -m http.server 8000
# ouvrir http://localhost:8000/
```
