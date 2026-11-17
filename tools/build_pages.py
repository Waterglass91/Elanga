"""Generate the site's HTML pages (shared header, menu, footer and film dialog).

    python3 tools/build_pages.py

Pages written at the repository root: index.html, journey.html, person.html, motion.html.
Edit page content here, then run the script; the HTML files are the published output.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARROW = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5"/></svg>'
IMG = {  # file: (width, height)
    'photo-01.jpg': (640, 800), 'photo-02.jpg': (688, 860), 'photo-04.jpg': (688, 860),
    'photo-05.jpg': (632, 790), 'photo-06.jpg': (654, 817), 'photo-07.jpg': (627, 783),
    'bw-56.jpg': (720, 900), 'bw-portrait.jpg': (720, 900), 'poster.jpg': (720, 900),
}


def img(name, alt, eager=False):
    w, h = IMG[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    webp = name.rsplit('.', 1)[0] + '.webp'
    return (f'<picture><source type="image/webp" srcset="media/{webp}">'
            f'<img src="media/{name}" width="{w}" height="{h}" alt="{alt}" {load}></picture>')


def fig(name, alt, caption, cls='fig portrait'):
    return f'<figure class="{cls}"><div class="frame">{img(name, alt)}</div><figcaption>{caption}</figcaption></figure>'


def lines(*parts):
    return ''.join(f'<span class="ln"><span>{p}</span></span>' for p in parts)


# ------------------------------------------------------------------ shared chrome
def head(title, desc, css, intro=False, body_class=''):
    intro_js = ("var seen = null; try { seen = localStorage.getItem('elanga:intro-v2'); } catch (e) {}\n"
                "    if (!seen && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) d.classList.add('intro-on');") if intro else ''
    links = '\n'.join(f'<link rel="stylesheet" href="css/{c}.css">' for c in ['tokens', 'base', 'experience', 'home'] + css)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#090A0C">
<link rel="preload" href="fonts/anton-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
{links}
<script>
  (function () {{
    var d = document.documentElement; d.classList.add('js');
    {intro_js}
  }})();
</script>
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Aller au contenu</a>
'''


INTRO = '''
<!-- ===== 01 Arrival : intro ===== -->
<div class="intro" id="intro" aria-hidden="true">
  <div class="intro-stack">
    <div class="intro-sig"></div>
    <div class="intro-brand"></div>
  </div>
  <button class="intro-skip" id="intro-skip" type="button">Passer l'intro</button>
</div>
'''

PAGES = [('index.html', 'Experience'), ('journey.html', 'The Journey'), ('person.html', 'The Person'), ('motion.html', 'The Motion'), ('partnerships.html', 'Partnerships')]


def chrome(current):
    def cur(f):
        return ' aria-current="page"' if f == current else ''
    nav = ''.join(f'\n      <a href="{f}"{cur(f)}>{label.replace("The ", "")}</a>' for f, label in PAGES[1:])
    menu = ''.join(f'\n      <li><a href="{f}"{cur(f)}>{label}</a></li>' for f, label in PAGES)
    return f'''
<!-- ===== Header ===== -->
<header class="site-header">
  <a class="brand" href="index.html" aria-label="Anthony Elanga, accueil">
    <img src="assets/signature-blanc.svg" width="1978" height="660" alt="">
  </a>
  <div class="header-actions">
    <nav class="header-nav" aria-label="Navigation principale">{nav}
    </nav>
    <button class="header-film" type="button" data-open-film>Le film</button>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu">
      <span class="label">Menu</span><span class="bars" aria-hidden="true"></span>
    </button>
  </div>
  <div class="progress" aria-hidden="true"></div>
</header>

<!-- ===== Menu overlay ===== -->
<nav class="menu" id="menu" aria-label="Menu" inert>
  <div class="wrap">
    <ul>{menu}
    </ul>
    <p class="menu-foot">Concept éditorial indépendant. Always forward.</p>
  </div>
</nav>
'''


def footer(replay, scripts=''):
    extra = '<button type="button" data-replay-intro>Revoir l\'intro</button>' if replay else '<a href="index.html">Accueil</a>'
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 · Concept éditorial indépendant, non affilié à Anthony Elanga, à ses clubs ni à ses partenaires.</span>
    {extra}
  </div>
</footer>

<!-- ===== Film dialog ===== -->
<dialog class="film-dialog" id="film" aria-labelledby="film-title">
  <div class="film-inner">
    <div class="film-head">
      <h2 id="film-title">Le film · Manchester United, 2014 – 2023</h2>
      <button class="film-close" type="button" aria-label="Fermer le film">
        <svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13"/></svg>
      </button>
    </div>
    <div class="film-screen">
      <video data-src="media/elanga-manchester.mp4" poster="media/poster.jpg" controls playsinline loop preload="none"></video>
      <p class="film-error" hidden>La vidéo n'a pas pu être chargée.</p>
    </div>
    <div class="film-foot">
      <span class="meta">Lecture sans son par défaut</span>
      <button class="sound-btn" type="button" aria-pressed="false"><span>Activer le son</span></button>
    </div>
  </div>
</dialog>

<div class="grain" aria-hidden="true"></div>

<script src="data/signature.js"></script>{scripts}
<script src="js/signature.js"></script>
<script src="js/main.js"></script>
</body>
</html>
'''


def next_card(href, kicker, title):
    return f'<a class="next-card" href="{href}"><span><span class="meta">{kicker}</span><strong>{title}</strong></span><span class="go">{ARROW}</span></a>'


# ------------------------------------------------------------------ HOME
def stop(year, place, what, name, ch):
    w, h = IMG[name]
    return f'''        <li class="stop"><a href="journey.html#chapitre-{ch}" data-preview="media/{name}">
          <img class="thumb" src="media/{name}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">
          <span class="yr">{year}</span><span class="place">{place}</span><span class="what">{what}</span><span class="go">{ARROW}</span>
        </a></li>
'''


HOME = f'''
<main id="main">
  <!-- ===== Hero ===== -->
  <section class="hero" id="top" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="kicker">Beyond speed.</p>
      <h1 class="hero-name display" id="hero-title">
        <span class="line"><span>Anthony</span></span>
        <span class="line"><span>Elanga.</span></span>
      </h1>
      <p class="hero-lede">Ailier international suédois, formé à Manchester United. Une trajectoire qui part de Malmö et mène aux plus grandes scènes d'Europe.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="journey.html">Découvrir le parcours</a>
        <button class="btn btn-ghost" type="button" data-open-film>
          <span class="play" aria-hidden="true"><svg viewBox="0 0 12 14"><path d="M0 0l12 7-12 7z"/></svg></span>
          Regarder le film
        </button>
      </div>
    </div>
    <figure class="hero-media">
      <picture>
        <source type="image/webp" srcset="media/hero-portrait-420.webp 420w, media/hero-portrait-632.webp 632w" sizes="(max-width: 900px) 100vw, 50vw">
        <img src="media/hero-portrait-632.jpg" srcset="media/hero-portrait-420.jpg 420w, media/hero-portrait-632.jpg 632w"
             sizes="(max-width: 900px) 100vw, 50vw" width="632" height="790" fetchpriority="high"
             alt="Anthony Elanga, mains croisées sur la poitrine, regard de côté">
      </picture>
      <figcaption class="meta">Newcastle United</figcaption>
    </figure>
    <a class="scroll-cue meta" href="#statement"><span class="rail" aria-hidden="true"></span>Défiler</a>
  </section>

  <!-- ===== 02 Statement ===== -->
  <section class="statement" id="statement" aria-labelledby="statement-title">
    <div class="wrap">
      <p class="section-label">Philosophie</p>
      <h2 class="display reveal" id="statement-title">{lines('Speed is a gift.', 'Progress is', 'a choice.')}</h2>
      <div class="statement-body">
        <p class="fade">Sa vitesse lui a ouvert des portes. Le travail les a gardées ouvertes : des séances de musculation à l'aube avant les déplacements européens, des choix de carrière assumés, des saisons à se reconstruire. L'ambition, chez lui, se mesure à ce qu'il refuse de laisser stagner.</p>
      </div>
    </div>
  </section>

  <!-- ===== 03 Motion ===== -->
  <section class="motion" id="motion" aria-labelledby="motion-title">
    <div class="wrap motion-grid">
      <div class="motion-stage">
        <div class="screen">
          <img src="media/poster.jpg" width="720" height="900" alt="" loading="lazy" decoding="async">
          <video data-src="media/elanga-manchester.mp4" muted loop playsinline preload="none" aria-label="Extraits de matchs avec Manchester United, sans son"></video>
        </div>
        <div class="bar">
          <span class="meta">Manchester United, 2014 – 2023 · sans son</span>
          <button class="link-btn" type="button" data-open-film>Voir le film avec le son</button>
        </div>
      </div>
      <div class="motion-text">
        <div class="motion-track" aria-hidden="true"><span></span></div>
        <p class="section-label">The Motion</p>
        <h2 class="display reveal" id="motion-title">{lines('Pace.', 'Precision.', 'Instinct.')}</h2>
        <p>Trois qualités qui reviennent à chaque étape de son parcours.</p>
        <article class="beat fade">
          <span class="k">01 · Pace</span>
          <h3 class="display">Attaquer l'espace</h3>
          <p>Sa vitesse est devenue une arme : attaquer la profondeur, multiplier les courses, peser sur chaque transition offensive.</p>
        </article>
        <article class="beat fade">
          <span class="k">02 · Precision</span>
          <h3 class="display">Le dernier geste</h3>
          <p>Accélérer ne suffit pas. Il faut choisir la bonne passe au bon moment : c'est le palier qu'il a franchi à Nottingham Forest.</p>
        </article>
        <article class="beat fade">
          <span class="k">03 · Instinct</span>
          <h3 class="display">Les grands soirs</h3>
          <p>Le Metropolitano à 19 ans, le Camp Nou avec Newcastle, la Coupe du monde avec la Suède : des matchs où tout se décide en un instant.</p>
          <p><a class="link-btn" href="motion.html">Explorer The Motion</a></p>
        </article>
      </div>
    </div>
  </section>

  <!-- ===== 04 Journey ===== -->
  <section class="journey" id="journey" aria-labelledby="journey-title">
    <div class="preview" aria-hidden="true"><img alt=""></div>
    <div class="wrap">
      <div class="journey-top">
        <div>
          <p class="section-label">The Journey</p>
          <h2 class="display reveal" id="journey-title">{lines('Four cities.', 'One direction.')}</h2>
        </div>
        <a class="link-btn" href="journey.html">Lire les 7 chapitres</a>
      </div>
      <ul class="stops">
{stop('2014 – 2023', 'Manchester', "L'académie, les débuts en Premier League, un but en Ligue des champions à 19 ans.", 'bw-56.jpg', 3)}{stop('2023 – 2025', 'Nottingham', "Du temps de jeu, de la confiance, et Forest qui retrouve l'Europe.", 'photo-04.jpg', 4)}{stop('2025 –', 'Newcastle', 'Changer de dimension et répondre présent lors des grandes soirées.', 'photo-05.jpg', 5)}{stop('2022 –', 'Sweden', "Le choix de la Suède, jusqu'à la Coupe du monde 2026.", 'photo-06.jpg', 6)}      </ul>
    </div>
  </section>

  <!-- ===== 05 Person ===== -->
  <section class="person" id="person" aria-labelledby="person-title">
    <div class="wrap">
      <div class="person-head">
        <div>
          <p class="section-label">The Person</p>
          <h2 class="display reveal" id="person-title">{lines('The man', 'behind the pace.')}</h2>
        </div>
        <p class="fade">Des racines, une façon de penser, un style et une ambition. L'homme derrière l'ailier. <a href="person.html">Lire The Person</a></p>
      </div>
      <div class="spread">
        <figure class="fig-a fade">
          {img('photo-01.jpg', 'Anthony Elanga sous le maillot de la Suède')}
          <figcaption>Avec la Suède. Photo © Corbis via Getty Images</figcaption>
        </figure>
        <article class="trait t-roots fade">
          <h3 class="display">Racines</h3>
          <p>Né à Malmö en 2002, fils de Joseph Elanga, ancien international camerounais. En héritage : le respect, le travail, l'humilité et la constance.</p>
        </article>
        <article class="trait t-mind fade">
          <h3 class="display">Mindset</h3>
          <p>Ne pas rester prisonnier de ses erreurs, ni s'attarder sur ses réussites. Il lit et étudie les méthodes des meilleurs sportifs.</p>
        </article>
        <article class="trait t-style fade">
          <h3 class="display">Style</h3>
          <p>Direct, précis, sans effet inutile : une manière d'être qui ressemble à son jeu.</p>
        </article>
        <article class="trait t-amb fade">
          <h3 class="display">Ambitions</h3>
          <p>Gagner en régularité et franchir le cap qui sépare un bon joueur d'un joueur d'élite. À 24 ans, son histoire est encore en train de s'écrire.</p>
        </article>
        <figure class="fig-b fade">
          {img('photo-07.jpg', "Anthony Elanga à l'entraînement, soulevé de terre en plein air")}
          <figcaption>Préparation</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <!-- ===== 06 Next chapter ===== -->
  <section class="next" id="next" aria-labelledby="next-title">
    <div class="wrap">
      <h2 class="display reveal" id="next-title">{lines('Not the finish line.', 'Just the beginning.')}</h2>
      <div class="next-sig" data-signature="closing"></div>
      <div class="next-foot">
        <p class="kicker">Always forward.</p>
        <nav class="next-links" aria-label="Liens de fin de page">
          <a href="journey.html">The Journey</a>
          <a href="person.html">The Person</a>
          <a href="motion.html">The Motion</a>
          <a href="partnerships.html">Partnerships</a>
          <a href="#top">Retour en haut</a>
        </nav>
      </div>
    </div>
  </section>
</main>
'''

# ------------------------------------------------------------------ JOURNEY
CHAPTERS = [
    dict(n='01', years='2002 – 2014', short='Malmö', title='Malmö, les racines', image='photo-01.jpg',
         alt='Anthony Elanga sous le maillot de la Suède', caption='Avec la Suède. Photo © Corbis via Getty Images',
         lede="Avant la vitesse, il y a un environnement : une famille où le football de haut niveau est un métier.",
         body=["Anthony David Junior Elanga naît le 27 avril 2002 à Hyllie, un quartier de Malmö. Son père, Joseph Elanga, ancien défenseur international camerounais, a disputé la Coupe du monde 1998 en France et joué au Malmö FF. Avec sa mère, Daniella, il lui transmet le respect, le travail, l'humilité et la constance.",
               "La famille vit à Malmö puis à Borås. Anthony découvre le football dans les structures suédoises, à l'IF Elfsborg puis au Malmö FF. Très tôt, il se distingue par sa vitesse et son explosivité, mais il cherche surtout à comprendre comment progresser : il observe les professionnels et étudie Thierry Henry, l'un de ses modèles.",
               "Enfant, il croise même Zlatan Ibrahimović, alors coéquipier de son père à Malmö."],
         moment="En 1998, son père disputait la Coupe du monde avec le Cameroun."),
    dict(n='02', years='2014 – 2020', short='Angleterre', title='Une nouvelle vie', image='photo-02.jpg',
         alt='Anthony Elanga en pleine course, ballon au pied, avec la Suède', caption='En mouvement, avec la Suède',
         lede="À douze ans, un nouveau pays, une nouvelle langue, et une porte qui s'ouvre : l'académie de Manchester United.",
         body=["Sa famille s'installe dans la région de Manchester. Il joue d'abord au Hattersley FC, un club local, où ses performances attirent vite l'attention. Manchester United le repère et l'intègre à son académie.",
               "Il y progresse catégorie après catégorie : la technique, le physique, l'art d'exploiter sa vitesse. Ses éducateurs retiennent autant son sérieux et son comportement que son talent.",
               "En 2019-2020, dans une saison interrompue par la pandémie, il marque sept buts en neuf matchs de championnat chez les moins de 18 ans et reçoit le Jimmy Murphy Young Player of the Year."],
         moment="Le meilleur jeune joueur de l'académie, saison 2019-2020."),
    dict(n='03', years='2021 – 2023', short='Manchester United', title='Le très haut niveau', image='bw-56.jpg',
         alt='Anthony Elanga de dos, maillot Elanga 56', caption='Manchester United',
         lede="Des débuts en Premier League, un soir européen à 19 ans, puis le choix difficile de partir.",
         body=["Le 11 mai 2021, Ole Gunnar Solskjær lui offre sa première apparition en équipe première, face à Leicester City. Le 23 mai, il marque son premier but en Premier League contre Wolverhampton.",
               "Une blessure à l'épaule début 2021 aurait pu le freiner ; il en profite pour se renforcer. Lors de déplacements européens avec les équipes de jeunes, il lui arrive d'être en salle de musculation dès quatre heures du matin avant de prendre l'avion.",
               "L'arrivée de Ralf Rangnick lui donne du temps de jeu. En février 2022, au Metropolitano, il entre en jeu et égalise face à l'Atlético de Madrid en huitième de finale de Ligue des champions. Un mois plus tard, il connaît sa première sélection avec la Suède. Avec l'arrivée d'Erik ten Hag et le renforcement offensif de l'effectif, ses occasions se raréfient : en 2023, il choisit de partir pour jouer."],
         moment="19 ans, un huitième de finale de Ligue des champions, un but."),
    dict(n='04', years='2023 – 2025', short='Nottingham Forest', title="L'envol", image='photo-04.jpg',
         alt='Anthony Elanga sous les projecteurs du City Ground, maillot de Nottingham Forest', caption='City Ground, Nottingham Forest',
         lede="Du temps de jeu, de la confiance, et un ailier qui devient une menace permanente.",
         body=["Le 25 juillet 2023, il rejoint Nottingham Forest pour un transfert estimé à 15 millions de livres. Dès sa première saison, il inscrit cinq buts et délivre neuf passes décisives en championnat.",
               "En 2024-2025, il franchit un palier : présent sur les 38 matchs de Premier League, six buts, onze passes décisives. Le 1er février 2025, il délivre trois passes décisives dans la victoire 7-0 contre Brighton. Le 1er avril, il marque contre Manchester United, son ancien club, au bout d'une course impressionnante.",
               "Forest termine septième et retrouve une qualification européenne après trois décennies d'absence."],
         moment="Le jeune espoir est devenu l'un des ailiers les plus rapides d'Angleterre."),
    dict(n='05', years='2025 – 2026', short='Newcastle United', title='Changer de dimension', image='photo-05.jpg',
         alt='Anthony Elanga, mains croisées sur la poitrine, maillot de Newcastle United', caption='Newcastle United',
         lede="Un transfert majeur, de nouvelles attentes, et l'apprentissage de la pression.",
         body=["Le 11 juillet 2025, il rejoint Newcastle United, entraîné par Eddie Howe, pour un transfert estimé à 55 millions de livres. Il ne s'agit plus de mériter sa place, mais de justifier un investissement et de faire basculer les grands matchs.",
               "Sa première saison est contrastée. Mais il répond présent lors des grandes soirées : un but contre Manchester City en demi-finale retour de la Coupe de la Ligue en février 2026, puis un doublé au Camp Nou contre le FC Barcelone en Ligue des champions en mars.",
               "En décembre 2025, il devient père d'une petite fille, Blair."],
         moment="Apprendre à vivre avec la pression, sans perdre confiance."),
    dict(n='06', years='2022 – 2026', short='Suède', title='Deux générations', image='photo-06.jpg',
         alt="Anthony Elanga célèbre un but avec la Suède, main à l'oreille", caption='Avec la Suède',
         lede="Né en Suède d'un père camerounais, formé en Angleterre : il choisit la Suède.",
         body=["Il honore sa première sélection en mars 2022, à 19 ans. La Suède échoue à se qualifier pour la Coupe du monde au Qatar.",
               "En mars 2026, il marque contre la Pologne en finale des barrages et contribue à envoyer son pays à la Coupe du monde. En Amérique du Nord, il débute contre la Tunisie, marque contre les Pays-Bas puis contre le Japon lors du dernier match de groupe. Après ce but, il aperçoit sa fille soulevée dans les tribunes, et doit détourner le regard pour ne pas pleurer.",
               "La Suède est éliminée par la France en seizièmes de finale."],
         moment="Vingt-huit ans après son père, sa première Coupe du monde."),
    dict(n='07', years='2026 –', short='Next', title="Devenir l'élite", image='photo-07.jpg',
         alt="Anthony Elanga à l'entraînement, soulevé de terre en plein air", caption='Préparation',
         lede="Une leçon retenue : ne pas rester prisonnier de ses erreurs, ni s'attarder sur ses réussites.",
         body=["À l'été 2026, il revient sur sa première année à Newcastle avec du recul. Sa philosophie : progresser chaque jour et se concentrer sur ce qui se maîtrise.",
               "Pour lui, ce qui sépare un bon joueur d'un joueur d'élite tient aussi au mental : réagir aux difficultés, prendre les bonnes décisions, garder confiance. Il lit et étudie les meilleurs sportifs pour comprendre leurs méthodes.",
               "Pour la saison 2026-2027, il porte le numéro 19, dont il garde la signification pour lui."],
         moment="À 24 ans, son histoire est encore en train de s'écrire."),
]

MILESTONES = [('2002', 'Naissance à Malmö, en Suède'), ('2014', 'Installation en Angleterre, puis académie de Manchester United'),
              ('2020', "Meilleur jeune joueur de l'académie de Manchester United"), ('2021', 'Débuts professionnels et premier but en Premier League'),
              ('2022', "But contre l'Atlético de Madrid et première sélection suédoise"), ('2023', 'Transfert à Nottingham Forest'),
              ('2025', 'Saison à 17 contributions décisives en championnat, puis Newcastle United'),
              ('2026', 'Doublé au Camp Nou, première Coupe du monde, numéro 19')]


def chapter(i, c):
    alt = ' alt' if i % 2 else ''
    body = ''.join(f'<p>{p}</p>' for p in c['body'])
    return f'''      <article class="chapter{alt}" id="chapitre-{i + 1}" aria-labelledby="ch{i + 1}-title">
        <div class="ch-top"><span class="ch-n" aria-hidden="true">{c['n']}</span><span class="ch-years">Chapitre {i + 1} · {c['years']}</span></div>
        <h2 class="display" id="ch{i + 1}-title">{c['title']}</h2>
        <p class="ch-lede">{c['lede']}</p>
        <div class="ch-body">
          <div class="ch-text">{body}<p class="moment">{c['moment']}</p></div>
          {fig(c['image'], c['alt'], c['caption'])}
        </div>
      </article>
'''


rail = ''.join(f'<li><a href="#chapitre-{i + 1}"><span class="n">{c["n"]}</span><span class="t">{c["short"]}</span><span class="y">{c["years"]}</span></a></li>' for i, c in enumerate(CHAPTERS))
credits = ''.join(f'<li><span class="y">{y}</span><span class="t">{t}</span></li>' for y, t in MILESTONES)

JOURNEY = f'''
<main id="main" class="page">
  <div class="wrap">
    <header class="page-head">
      <p class="section-label">The Journey</p>
      <h1 class="display reveal">{lines('De Malmö', 'au monde.')}</h1>
      <p class="page-lede">Sept chapitres, de Hyllie à Newcastle, en passant par Manchester, Nottingham et la Coupe du monde.</p>
    </header>
    <div class="jr">
      <nav class="rail" aria-label="Chapitres"><ol>{rail}</ol></nav>
      <div class="chapters">
{''.join(chapter(i, c) for i, c in enumerate(CHAPTERS))}      </div>
    </div>
  </div>

  <section class="credits-sec" aria-labelledby="credits-title">
    <div class="wrap grid">
      <h2 class="display" id="credits-title">Milestones</h2>
      <ol class="credits">{credits}</ol>
    </div>
  </section>

  <div class="wrap next-pages">
    {next_card('person.html', 'Continuer', 'The Person')}
    {next_card('motion.html', 'Continuer', 'The Motion')}
  </div>
</main>
'''

# ------------------------------------------------------------------ PERSON
PERSON = f'''
<main id="main" class="page">
  <div class="wrap">
    <div class="p-hero">
      <header class="page-head">
        <p class="section-label">The Person</p>
        <h1 class="display reveal">{lines('The man', 'behind the pace.')}</h1>
        <p class="page-lede">Des racines, une façon de penser, un style et un héritage. Le portrait de l'homme derrière l'ailier.</p>
      </header>
      {fig('bw-portrait.jpg', 'Anthony Elanga, doigt sur les lèvres, après un but', 'Manchester United')}
    </div>

    <section class="p-sec" id="racines" aria-labelledby="p1">
      <div class="p-head"><p class="section-label">01</p><h2 class="display" id="p1">Racines</h2></div>
      <div class="p-text fade">
        <p>Anthony grandit à Malmö, dans une famille où le football de haut niveau est un métier. Son père, Joseph Elanga, ancien défenseur international camerounais, a disputé la Coupe du monde 1998 et joué au Malmö FF.</p>
        <p>Sa mère, Daniella, et son père lui transmettent des valeurs auxquelles il reste attaché : le respect, le travail, l'humilité et la constance. Enfant, il observe les professionnels, étudie Thierry Henry et croise même Zlatan Ibrahimović, coéquipier de son père.</p>
        <p class="moment">Un enfant de Malmö qui voit de près ce qu'exige le haut niveau.</p>
      </div>
      {fig('photo-01.jpg', 'Anthony Elanga sous le maillot de la Suède', 'Avec la Suède. Photo © Corbis via Getty Images')}
    </section>

    <section class="p-sec" id="mindset" aria-labelledby="p2">
      <div class="p-head"><p class="section-label">02</p><h2 class="display" id="p2">Mindset</h2></div>
      <div class="p-text fade">
        <p>À l'été 2026, il résume ce qu'il a appris : ne pas rester prisonnier de ses erreurs, ni s'attarder sur ses réussites. Progresser chaque jour et se concentrer sur ce qui peut être maîtrisé.</p>
        <p>Il insiste sur le mental : la différence entre un bon joueur et un joueur d'élite tient à la capacité de réagir aux difficultés, de prendre les bonnes décisions et de garder confiance. Il lit et étudie les meilleurs sportifs pour comprendre leurs méthodes.</p>
        <p class="moment">Des séances à quatre heures du matin avant les déplacements européens, à 18 ans.</p>
      </div>
      {fig('photo-07.jpg', "Anthony Elanga à l'entraînement, soulevé de terre en plein air", 'Préparation')}
    </section>

    <section class="p-sec" id="style" aria-labelledby="p3">
      <div class="p-head"><p class="section-label">03</p><h2 class="display" id="p3">Style</h2></div>
      <div class="p-text fade">
        <p>Direct, précis, sans effet inutile : une manière d'être qui ressemble à son jeu.</p>
        <p>Ce chapitre accueillera une série lifestyle et studio, réalisée avec son accord.</p>
      </div>
      <div class="style-panel" role="note"><strong>Lifestyle<br>&amp; studio</strong><span>Série photo à produire. Aucun visuel n'est affiché tant qu'il n'est pas validé.</span></div>
    </section>

    <section class="p-sec wide" id="heritage" aria-labelledby="p4">
      <div class="p-head"><p class="section-label">04</p><h2 class="display" id="p4">Héritage</h2></div>
      <div class="p-text fade">
        <p>Né en Suède d'un père camerounais, formé en Angleterre, il choisit la Suède. En 2026, vingt-huit ans après son père, il dispute à son tour une Coupe du monde.</p>
        <p>En décembre 2025, il devient père d'une petite fille, Blair. Pendant la Coupe du monde, après son but contre le Japon, il l'aperçoit soulevée dans les tribunes.</p>
        <div class="gen" aria-label="Deux générations en Coupe du monde">
          <div><b>1998</b><span>Joseph Elanga · Cameroun</span></div>
          <div><b>2026</b><span>Anthony Elanga · Suède</span></div>
        </div>
      </div>
    </section>

    <section class="p-sec wide" id="ambitions" aria-labelledby="p5">
      <div class="p-head"><p class="section-label">05</p><h2 class="display" id="p5">Ambitions</h2></div>
      <div class="p-text fade">
        <p>Gagner en régularité. Franchir le cap qui sépare un bon joueur d'un joueur d'élite. Pour la saison 2026-2027, il porte le numéro 19, dont il garde la signification pour lui.</p>
        <p class="moment">À 24 ans, il sait que son histoire est encore en train de s'écrire.</p>
      </div>
    </section>

    <div class="next-pages">
      {next_card('journey.html', 'Le parcours', 'The Journey')}
      {next_card('motion.html', 'Les images', 'The Motion')}
    </div>
  </div>
</main>
'''

# ------------------------------------------------------------------ MOTION
MOMENTS = [('23 mai 2021', 'Premier but en Premier League', 'Manchester United contre Wolverhampton'),
           ('Février 2022', 'Le Metropolitano', "But égalisateur contre l'Atlético de Madrid, huitième de finale de Ligue des champions"),
           ('1er avril 2025', "Face à son ancien club", 'But avec Nottingham Forest contre Manchester United'),
           ('Février 2026', 'Demi-finale de Coupe de la Ligue', 'But avec Newcastle contre Manchester City'),
           ('Mars 2026', 'Doublé au Camp Nou', 'Newcastle contre le FC Barcelone, Ligue des champions'),
           ('Mars 2026', 'Finale des barrages', 'But contre la Pologne, qualification de la Suède pour la Coupe du monde'),
           ('Été 2026', 'Coupe du monde', 'Buts contre les Pays-Bas et le Japon')]
moments = ''.join(f'<li><time>{d}</time><strong>{t}</strong><span class="ctx">{c}</span><span class="st">Vidéo sous licence à venir</span></li>' for d, t, c in MOMENTS)

MOTION = f'''
<main id="main" class="page">
  <div class="wrap">
    <header class="page-head">
      <p class="section-label">The Motion</p>
      <h1 class="display reveal">{lines('Pace. Precision.', 'Instinct.')}</h1>
      <p class="page-lede">Le mouvement en images : un film, des instants figés, et les grands soirs de sa carrière.</p>
    </header>

    <section class="feature" aria-labelledby="film-feature">
      <div class="player">
        <div class="screen">
          <video id="feature-video" data-src="media/elanga-manchester.mp4" poster="media/poster.jpg" controls playsinline preload="none" aria-describedby="film-desc"></video>
          <p class="film-error" hidden>La vidéo n'a pas pu être chargée.</p>
        </div>
      </div>
      <div class="feature-info">
        <p class="section-label">Le film</p>
        <h2 class="display" id="film-feature">Manchester United, 2014 – 2023</h2>
        <dl>
          <dt>Durée</dt><dd>2 min 10</dd>
          <dt>Son</dt><dd>Coupé par défaut</dd>
          <dt>Droits</dt><dd>À confirmer</dd>
        </dl>
        <p id="film-desc">Les années Manchester United en images : l'académie, les débuts en équipe première et les premiers soirs européens.</p>
        <div class="actions">
          <button class="btn btn-primary" type="button" id="feature-play">Lancer le film</button>
          <button class="sound-btn" type="button" id="feature-sound" aria-pressed="false"><span>Activer le son</span></button>
        </div>
      </div>
    </section>
  </div>

  <section class="stills" aria-labelledby="stills-title">
    <div class="wrap">
      <p class="section-label">Stills</p>
      <h2 class="display reveal" id="stills-title">{lines('Frozen speed.')}</h2>
      <div class="stills-grid">
        {fig('photo-02.jpg', 'Anthony Elanga en pleine course, ballon au pied, avec la Suède', 'En mouvement, avec la Suède')}
        {fig('bw-56.jpg', 'Anthony Elanga de dos, maillot Elanga 56', 'Manchester United')}
        {fig('photo-06.jpg', "Anthony Elanga célèbre un but avec la Suède, main à l'oreille", 'Avec la Suède')}
        {fig('bw-portrait.jpg', 'Anthony Elanga, doigt sur les lèvres, après un but', 'Manchester United')}
        {fig('photo-04.jpg', 'Anthony Elanga sous les projecteurs du City Ground', 'City Ground, Nottingham Forest')}
      </div>
    </div>
  </section>

  <section class="moments" aria-labelledby="moments-title">
    <div class="wrap">
      <p class="section-label">Moments</p>
      <h2 class="display reveal" id="moments-title">{lines('The big nights.')}</h2>
      <ol class="moment-list">{moments}</ol>
      <p class="sources meta">Source : portrait biographique fourni (novembre 2026), à vérifier avant publication. Les extraits vidéo seront ajoutés une fois les droits obtenus.</p>
    </div>
  </section>

  <div class="wrap next-pages">
    {next_card('journey.html', 'Le parcours', 'The Journey')}
    {next_card('person.html', "L'homme", 'The Person')}
  </div>
</main>
'''

# ------------------------------------------------------------------ PARTNERSHIPS
TODO = '<span class="todo">À valider</span>'


def slot(label, note):
    return f'<div class="slot"><span class="slot-label">{label}</span><span class="slot-value" aria-label="Donnée non renseignée">—</span><span class="slot-note">{note}</span></div>'


def field(fid, label, kind='text', required=True, extra=''):
    req = ' required aria-required="true"' if required else ''
    star = '' if not required else ' <span aria-hidden="true">*</span>'
    if kind == 'textarea':
        ctrl = f'<textarea id="{fid}" name="{fid}" rows="5"{req} aria-describedby="{fid}-err"{extra}></textarea>'
    elif kind == 'select':
        ctrl = (f'<select id="{fid}" name="{fid}"{req} aria-describedby="{fid}-err"><option value="">Choisir…</option>'
                '<option>Partenariat de marque</option><option>Campagne ou contenu</option><option>Événement ou apparition</option>'
                '<option>Presse ou interview</option><option>Autre</option></select>')
    else:
        ctrl = f'<input id="{fid}" name="{fid}" type="{kind}"{req} aria-describedby="{fid}-err"{extra}>'
    return f'<div class="field"><label for="{fid}">{label}{star}</label>{ctrl}<span class="err" id="{fid}-err"></span></div>'


PARTNERS = f"""
<main id="main" class="page">
  <div class="wrap">
    <header class="page-head">
      <p class="section-label">Partnerships</p>
      <h1 class="display reveal">{lines('Built to', 'move forward.')}</h1>
      <p class="page-lede">Un athlète international qui construit sa propre marque, à la croisée de la performance, du mouvement et de l'élégance.</p>
      <p class="demo-note" role="note">Page de démonstration. Les chiffres, formats et contacts seront complétés et validés avec Anthony Elanga ou ses représentants avant toute publication.</p>
    </header>

    <section class="pt-sec" aria-labelledby="pt-pillars">
      <div class="pt-head"><p class="section-label">Positionnement</p><h2 class="display" id="pt-pillars">Three pillars</h2></div>
      <div class="pillars3">
        <article class="pillar fade"><span class="k">01</span><h3 class="display">Luxury</h3><p>Précision, retenue, exigence du détail. Une image sobre et maîtrisée, loin du bruit.</p></article>
        <article class="pillar fade"><span class="k">02</span><h3 class="display">Motion</h3><p>Vitesse, agilité, impact. Le mouvement comme langage, sur le terrain et en dehors.</p></article>
        <article class="pillar fade"><span class="k">03</span><h3 class="display">Identity</h3><p>Des racines à Malmö, une famille de footballeurs, un parcours entre trois pays.</p></article>
      </div>
    </section>

    <section class="pt-sec" aria-labelledby="pt-facts">
      <div class="pt-head"><p class="section-label">Repères</p><h2 class="display" id="pt-facts">At a glance</h2></div>
      <div class="facts">
        <div class="fact-row"><span class="slot-label">Poste</span><span>Ailier</span></div>
        <div class="fact-row"><span class="slot-label">Sélection</span><span>Suède, depuis mars 2022</span></div>
        <div class="fact-row"><span class="slot-label">Clubs</span><span>Manchester United, Nottingham Forest, Newcastle United</span></div>
        <div class="fact-row"><span class="slot-label">Grandes compétitions</span><span>Premier League, Ligue des champions, Coupe du monde 2026</span></div>
      </div>
      <p class="meta pt-src">Source : portrait biographique fourni (novembre 2026), à vérifier.</p>
      <h3 class="pt-sub">Audience et chiffres {TODO}</h3>
      <div class="slots">
        {slot('Audience réseaux sociaux', 'À fournir par le management, avec date et source')}
        {slot('Engagement moyen', 'Donnée certifiée requise')}
        {slot('Répartition par pays', 'Donnée certifiée requise')}
        {slot('Couverture médias', 'Revue de presse à constituer')}
      </div>
      <p class="meta pt-src">Aucun chiffre n'est affiché tant qu'il n'est pas sourcé, daté et vérifié.</p>
    </section>

    <section class="pt-sec" aria-labelledby="pt-formats">
      <div class="pt-head"><p class="section-label">Collaborations</p><h2 class="display" id="pt-formats">Formats {TODO}</h2></div>
      <ol class="formats">
        <li class="fade"><strong class="display">Ambassadeur</strong><p>Partenariat de marque sur la durée, construit autour des trois piliers.</p></li>
        <li class="fade"><strong class="display">Campagnes</strong><p>Contenus éditoriaux, photo et vidéo, dans la direction artistique The Elanga Experience.</p></li>
        <li class="fade"><strong class="display">Événements</strong><p>Apparitions, lancements, rencontres, selon le calendrier sportif.</p></li>
        <li class="fade"><strong class="display">Communauté</strong><p>Projets liés à la jeunesse et au football de formation, à définir.</p></li>
      </ol>
      <p class="meta pt-src">Références de partenaires : aucune n'est affichée sans autorisation écrite. Aucun logo de marque n'est utilisé.</p>
    </section>

    <section class="pt-sec kit-sec" aria-labelledby="pt-kit">
      <div class="pt-head"><p class="section-label">Media kit</p><h2 class="display" id="pt-kit">Media kit</h2></div>
      <div class="kit">
        <div class="kit-cover" aria-hidden="true"><img class="kit-sig" src="assets/signature-blanc.svg" width="1978" height="660" alt=""><strong>Media kit</strong><span>2026 – 2027</span></div>
        <div class="kit-body">
          <p>Le media kit réunira tout ce qu'une marque ou un média doit savoir, dans un seul document.</p>
          <ul class="kit-list">
            <li>Biographie courte et longue, validées</li>
            <li>Sélection de photos HD sous licence</li>
            <li>Chiffres d'audience certifiés et datés</li>
            <li>Formats de collaboration et conditions</li>
            <li>Contact du management</li>
          </ul>
          <button class="btn btn-primary" type="button" disabled aria-describedby="kit-state">Télécharger le media kit (PDF)</button>
          <p class="meta" id="kit-state">En préparation : disponible après validation du contenu.</p>
        </div>
      </div>
    </section>

    <section class="pt-sec" id="contact" aria-labelledby="pt-contact">
      <div class="pt-head"><p class="section-label">Contact</p><h2 class="display" id="pt-contact">Work together</h2>
        <p class="pt-lede">Le contact du management sera ajouté après validation. En attendant, ce formulaire montre le parcours prévu : il n'envoie rien.</p></div>
      <form class="pt-form" data-demo-form novalidate>
        {field('nom', 'Nom', extra=' autocomplete="name"')}
        {field('organisation', 'Organisation', extra=' autocomplete="organization"')}
        {field('email', 'E-mail', 'email', extra=' autocomplete="email"')}
        {field('projet', 'Type de projet', 'select')}
        {field('message', 'Message', 'textarea')}
        <div class="form-foot">
          <button class="btn btn-primary" type="submit">Envoyer la demande</button>
          <p class="meta">Formulaire de démonstration · aucune donnée n'est transmise ni conservée.</p>
        </div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </section>

    <div class="next-pages">
      {next_card('journey.html', 'Le parcours', 'The Journey')}
      {next_card('index.html', "Retour à", 'Experience')}
    </div>
  </div>
</main>
"""

DESC_SUFFIX = ' Concept éditorial indépendant.'
pages = {
    'index.html': head("Anthony Elanga — The Elanga Experience (concept éditorial)",
                       "The Elanga Experience : concept éditorial indépendant autour du parcours d'Anthony Elanga, de Malmö aux plus grandes scènes d'Europe.",
                       [], intro=True, body_class='page-home') + INTRO + chrome('index.html') + HOME + footer(True, '\n<script src="data/brand.js"></script>'),
    'journey.html': head('The Journey — Anthony Elanga (concept éditorial)',
                         "Le parcours d'Anthony Elanga en sept chapitres, de Malmö à la Coupe du monde 2026." + DESC_SUFFIX,
                         ['pages'], body_class='page-journey') + chrome('journey.html') + JOURNEY + footer(False),
    'person.html': head('The Person — Anthony Elanga (concept éditorial)',
                        "Racines, mindset, style et héritage : l'homme derrière l'ailier." + DESC_SUFFIX,
                        ['pages'], body_class='page-person') + chrome('person.html') + PERSON + footer(False),
    'partnerships.html': head('Partnerships — Anthony Elanga (concept éditorial)',
                              'Positionnement, formats de collaboration et media kit (démonstration).' + DESC_SUFFIX,
                              ['pages'], body_class='page-partners') + chrome('partnerships.html') + PARTNERS + footer(False),
    'motion.html': head('The Motion — Anthony Elanga (concept éditorial)',
                        'Le film, les images et les grands soirs de la carrière d\'Anthony Elanga.' + DESC_SUFFIX,
                        ['pages'], body_class='page-motion') + chrome('motion.html') + MOTION + footer(False),
}
for name, html in pages.items():
    (ROOT / name).write_text(html)
    print(f'{name}: {len(html):,} octets')
