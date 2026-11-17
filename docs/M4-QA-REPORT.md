# M4 — Partnerships et rapport qualité

Branche : `redesign/elanga-experience` · Date : 17 novembre 2026 · Outil : `tools/qa.py` (Playwright + axe-core 4)

## 1. Ce qui a été livré

| Fichier | Rôle |
|---|---|
| `partnerships.html` | Positionnement (3 piliers), repères, audience (emplacements vides étiquetés), formats, media kit, formulaire de démonstration |
| `css/pages.css` | Styles Partnerships, formulaire, media kit |
| `js/main.js` | Validation du formulaire, messages d'erreur accessibles, aucun envoi |
| `media/*.webp` | Versions WebP de toutes les photos (−33 % de poids) |
| `tools/qa.py` | Tests automatisés reproductibles |

Contenus marqués « À valider » : audience et chiffres, formats de collaboration, media kit, contact. Aucun chiffre, logo de marque, référence de partenaire ni adresse de contact n'est inventé.

## 2. Liens et ressources

205 liens et ressources vérifiés sur les 5 pages (pages, ancres `#chapitre-1` à `7`, images, `srcset`, vidéo, polices, scripts) : **0 lien cassé**, 0 dépendance externe (polices auto-hébergées).

## 3. Formulaire (démonstration)

| Test | Résultat |
|---|---|
| Envoi vide | « 5 champs à corriger. », focus sur le premier champ, `aria-invalid` posé |
| E-mail invalide | Message « Indiquez une adresse e-mail valide… », focus sur le champ |
| Envoi valide | Message de statut annoncé (`role="status"`), **aucune requête réseau** |
| Bouton media kit | Désactivé, état expliqué (`aria-describedby`) |

## 4. Accessibilité (WCAG 2.2 AA)

axe-core, règles `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`, sur les 5 pages × ordinateur (1440 px) et mobile (390 px) : **0 violation**.

Vérifié en plus : lien d'évitement « Aller au contenu », ordre de tabulation logique, focus visible (contour Volt 2 px), menu plein écran fermable par Échap avec le reste de la page rendu inerte, fenêtre du film en `<dialog>` modal, vidéos muettes par défaut, `prefers-reduced-motion` respecté (intro, révélations, zoom, aperçus désactivés), page lisible sans JavaScript.

Reste à faire : sous-titres de la vidéo si elle contient des paroles ; test avec un lecteur d'écran réel (VoiceOver, NVDA).

## 5. Performances

Mesures locales (sans latence réseau), intro déjà vue, Chromium.

| Page | Poids initial | dont images | LCP | CLS |
|---|---|---|---|---|
| Accueil (ordinateur) | 292 Ko | 132 Ko | 0,16 s | 0 |
| Accueil (mobile) | 252 Ko | 92 Ko | 0,14 s | 0 |
| Journey | 498 Ko | 270 Ko | 0,15 s | 0 |
| Person | 497 Ko | 277 Ko | 0,18 s | 0 |
| Motion | 709 Ko | 540 Ko | 0,16 s | 0 |
| Partnerships | 235 Ko | 64 Ko | 0,13 s | 0 |

La vidéo (15,8 Mo) n'est jamais chargée au démarrage : uniquement à l'ouverture du film ou à l'approche de la section Motion. Images hors écran en `loading="lazy"`, dimensions déclarées (CLS = 0), polices préchargées en `font-display: swap`.

Pistes : version 720p et 480p de la vidéo, AVIF pour les photos, photos HD une fois fournies (à servir en `srcset` multi-tailles).

## 6. Responsive

5 pages × 6 largeurs (360, 390, 768, 1024, 1440, 1920 px) : 30 captures, **aucun débordement horizontal**, aucune erreur JavaScript.

## 7. Droits et licences

Voir `docs/EDITORIAL-CHECKLIST.md`. En résumé : **aucun visuel n'a de droits confirmés** (Getty pour la photo 01, publications Instagram pour les autres, images de Manchester United dans la vidéo). Les polices Anton et Inter sont sous licence SIL OFL (fichiers de licence dans `fonts/`). La signature est fournie par le client : à confirmer par écrit.

## 8. Avant fusion dans `main`

1. Validation visuelle des 5 pages
2. Décision sur la mise en ligne publique tant que les droits ne sont pas réglés
3. Ouverture de la pull request `redesign/elanga-experience` → `main`
