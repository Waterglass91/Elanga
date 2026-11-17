# THE ELANGA EXPERIENCE — Design & Development Brief
Version 1.0 — 17 November 2026
Repository: https://github.com/Waterglass91/Elanga
Live: https://waterglass91.github.io/Elanga/

## Mission
Transform the current Anthony Elanga storytelling website into a premium, distinctive, cinematic personal-brand experience blending luxury editorial design, football performance, and human storytelling. Present as an independent concept/demo until Anthony Elanga or his representatives authorize any official representation.

## Collaboration contract
- ChatGPT: creative direction, UX and visual QA. Claude Code: implementation and technical QA. GitHub: shared source of truth.
- Never push or merge directly to `main` without explicit approval. Work on a branch named `redesign/elanga-experience` and open a pull request. Keep current GitHub Pages site functioning.
- First audit the existing repository, inventory assets/code/third-party dependencies, and provide an implementation plan. Do not start major changes until the audit has been summarized.
- Prefer incremental commits per milestone and reproducible preview instructions. Show screenshots of desktop and mobile when possible.

## Current repository facts
- Public repository `Waterglass91/Elanga`, default branch `main`.
- `index.html` contains HTML, CSS and JavaScript in one file; no `package.json` was found in the repository root when checked.
- Existing intro writes an SVG signature by stroke masking. Preserve SVG geometry and spirit of the animation.
- Existing homepage includes hero with framed video, Beyond the Game, seven Journey chapters, The Man, milestones, closing/contact.
- Existing typography: Bebas Neue and Inter; palette obsidian `#0B0B0D`, graphite `#202329`, ivory `#F4F1EB`, steel `#A8ADB7`, gold `#C6A773`.
- `README.md` identifies photo-rights verification, missing The Man photos, nonfunctional EN/SV selector and missing partnership contact as outstanding tasks.

## Brand strategy
- Core brand: ELANGA. Brand philosophy: ALWAYS FORWARD. Campaign line: BEYOND SPEED.
- Three pillars: Luxury (precision, elegant restraint), Motion (speed, agility, impact), Identity (roots, mindset, journey).
- Desired feeling: modern international sports icon, not generic fan site or conventional player CV.
- This is an editorial concept; do not attribute invented quotes or unverified facts to the player.

## Design system
- Background / Obsidian: `#090A0C`; Carbon surface: `#202228`; Bone: `#F2F0EA`; Titanium muted text/details: `#ACB2BA`; Volt accent: `#B8FF36`.
- Use restrained Volt (approximately 5% of visible elements), primarily for interactive states, progress indicators, fine rules and emphasis. Avoid loud neon gradients and gratuitous glow effects.
- Primary display: Anton or another high-quality condensed display face, with font licensing verified. Body: Manrope or Inter; preserve the existing custom SVG signature as a personal mark.
- Desktop: 12-column grid, content max-width ~1440px, elegant rhythm and generous whitespace. Large editorial typography; clear contrast and hierarchy.
- Desktop hero display: responsive ~90–160px as visual conditions allow; mobile ~44–72px; avoid cropping important letterforms. Responsive designs at 360, 390, 768, 1024, 1440 and 1920px.
- Imagery: authoritative dramatic athlete portrait, fast-motion sport, archival journey and refined lifestyle studio photography. Do not substitute stock photos as if they depict Elanga.

## Information architecture
1. EXPERIENCE — immersive homepage / brand statement.
2. THE JOURNEY — documentary-style timeline with seven detailed chapters.
3. THE PERSON — roots, mindset, style, legacy; avoid unverified personal claims and image placeholders that look like final assets.
4. THE MOTION — authenticated/licensed videos and football moments, filters only where enough media exists.
5. PARTNERSHIPS — commercial positioning, verified metrics if available, authorized collaboration references, media kit and approved management contact.

## Homepage storyboards
### 01 — Arrival
Short optional animated SVG signature (ideally <3s), then full-bleed athlete photography/video. Oversized `ANTHONY / ELANGA.` behind or alongside subject, clear `BEYOND SPEED.` kicker, subtle vertical motion and optional scroll cue. Do not autoplay sound. Visible Skip intro. Remember completion for repeat visitors only where suitable. Maintain a readable fallback if video fails.
### 02 — Statement
Abrupt visual shift from dark to bone-colored background. Giant editorial copy: `SPEED IS A GIFT. / PROGRESS IS A CHOICE.` (creative copy, not player quotation). Short paragraph about ambition and discipline. Scroll reveals should be elegant, legible and reversible.
### 03 — Motion
Immersive video/motion gallery highlighting pace, precision and instinct. Thin Volt line tracks narrative progress. Any statistics must be sourced, dated and verified.
### 04 — Journey
Four homepage teaser milestones (Manchester, Nottingham, Newcastle, Sweden), leading to seven existing chapters. Hover image preview for pointer devices and tap card for touch devices. Preserve chronological accuracy.
### 05 — Person
High-end magazine treatment with roots, mindset, style and ambitions. Use approved imagery and captions; mark missing assets in the editorial checklist rather than faking them.
### 06 — Next Chapter
Closing `NOT THE FINISH LINE. / JUST THE BEGINNING.` and `ALWAYS FORWARD.`; clean links and footer; meaningful contact only when approved.

## Interactions
- Signature stroke reveal, subtle image zoom 105% to 100%, editorial text-mask reveals, progress line, elegant menu overlay, restrained hover states.
- Respect `prefers-reduced-motion`, no scroll hijacking, no blocking animations, transitions generally 300–700ms.
- Real navigation with keyboard support, focus indicators, accessible name for icon buttons, Escape closes overlays, visible captions/subtitles for videos, mute by default.
- Mobile: performance-first, simple transitions, no hover-only features, high-quality menu and responsive type.

## Engineering
- Inspect existing project before choosing stack. Current site is vanilla single-file HTML/CSS/JS; do not introduce React/Vite without a clear, practical reason and an explicit migration plan.
- Prefer maintainable component/section separation and reusable design tokens, while preserving compatibility with GitHub Pages deployment under the `/Elanga/` subpath (avoid broken root-relative assets).
- Optimize video (poster, preload strategy, mute, compression) and photos (responsive `srcset`, modern formats, dimensions, lazy load below fold). Prevent cumulative layout shift.
- Verify accessibility to WCAG 2.2 AA where feasible; good contrast, semantic headings, keyboard navigation and reduced motion.
- Keep the existing content while carefully shortening homepage excerpts. Avoid inventing career records, endorsements, social reach or official status.
- Verify licensing/rights for all player portraits, match footage, logos and third-party images. Flag missing rights for the owner.
- Use real EN/SV switch only after both full translations exist; otherwise remove/disable misleading controls and document remaining work.
- No false contact details and no fictitious brand partnership logos.

## Implementation milestones and acceptance criteria
### M0 — Audit & foundation
Deliver repository inventory, page inventory, asset/right audit, planned file structure, dependencies and risk summary. Branch created. No main changes.
### M1 — Brand system & hero
Implement design tokens, fonts, navigation, brief intro and cinematic full-bleed hero. Verify screenshot at desktop/mobile, CTA, visual contrast, skip intro and fallback. Present for approval.
### M2 — Home narrative
Build statement, motion, journey teasers, person and closing. Preserve existing story data; accessible motion; responsive.
### M3 — Detail pages
Journey, Person and Motion; appropriate content structure and graceful handling of incomplete assets.
### M4 — Partnerships & QA
Commercial page and media-kit shell with placeholder content clearly labeled for approval; links and forms tested, license and accessibility checklist, responsive/performance report.

## Mandatory delivery format for each milestone
- What was changed (file list), why, and notable creative choices.
- Preview URL or local preview instructions; desktop and mobile screenshots if available.
- Known gaps, unresolved decisions, licensing issues, test results.
- Git branch and PR/commit link; **do not merge to main without approval**.

## Definition of success
Within three seconds of the main hero, a visitor recognizes a premium international athlete brand. Navigation feels deliberate and quick, hero works on mobile, the seven-chapter narrative is preserved, and the site is commercially credible without unsupported claims.
