#!/usr/bin/env python3
"""Génère en/index.html à partir de index.html (la version française est la source).

Usage : python3 tools/make_en.py
Chaque chaîne française doit exister dans index.html : si une phrase est modifiée
côté français, le script s'arrête et indique laquelle mettre à jour ici.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, urlencode, quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "en" / "index.html"

# (français, anglais). Appliqué du plus long au plus court.
T = [
    # --- <head> ---
    ('<html lang="fr">', '<html lang="en">'),
    ('<title>VIBES · Makes lives happen</title>',
     '<title>VIBES · Makes lives happen</title>'),
    ("VIBES est une initiative étudiante pour le bien-être sur les campus : retrouver des jeunes qui partagent tes passions, prendre soin de toi et construire des habitudes qui te font du bien.",
     "VIBES is a student-led initiative for well-being on campus: find young people who share your passions, take care of yourself and build habits that do you good."),
    ('content="fr_FR"', 'content="en_US"'),
    ('<meta property="og:title" content="VIBES · Makes lives happen">',
     '<meta property="og:title" content="VIBES · Makes lives happen">'),
    ("Le bien-être étudiant autrement : découvrir, s'outiller, ancrer de bonnes habitudes.",
     "Student well-being, differently: discover, equip yourself, anchor good habits."),

    # --- navigation ---
    ('aria-label="VIBES, retour en haut de page"', 'aria-label="VIBES, back to top"'),
    ('aria-label="Navigation principale"', 'aria-label="Main navigation"'),
    ('aria-label="Ouvrir le menu" data-label-open="Ouvrir le menu" data-label-close="Fermer le menu"',
     'aria-label="Open menu" data-label-open="Open menu" data-label-close="Close menu"'),
    ('>Aller au contenu<', '>Skip to content<'),
    ('<a href="#constat">Vision</a>\n      <a href="#intentions">Approche</a>\n      <a href="#experience">Expérience</a>\n      <a href="#engagements">Engagements</a>',
     '<a href="#constat">Vision</a>\n      <a href="#intentions">Approach</a>\n      <a href="#experience">Experience</a>\n      <a href="#engagements">Commitments</a>'),
    ('<a class="lang" href="en/" hreflang="en" lang="en" title="Read this page in English"><b>FR</b> | EN</a>',
     '<a class="lang" href="../" hreflang="fr" lang="fr" title="Lire cette page en français">FR | <b>EN</b></a>'),
    ('href="#contribuer">Contribuer</a>\n    </nav>', 'href="#contribuer">Contribute</a>\n    </nav>'),

    # --- hero ---
    ("VIBES · Le bien-être étudiant autrement", "VIBES · Student well-being, differently"),
    ('Makes <span class="hl">lives</span> happen.', 'Makes <span class="hl">lives</span> happen.'),
    ("Et si ton téléphone t'aidait à vivre davantage, plutôt qu'à rester connecté toute la journée ?",
     "What if your phone helped you live more, instead of keeping you connected all day?"),
    ("VIBES t'aide à retrouver des jeunes qui partagent tes passions, à prendre soin de toi et à construire des habitudes qui te font du bien.",
     "VIBES helps you find young people who share your passions, take care of yourself and build habits that do you good."),
    ('Découvrir VIBES <span', 'Discover VIBES <span'),
    ('>Notre vision</a>', '>Our vision</a>'),
    ("En cours de conception : l'application n'est pas encore disponible au téléchargement. Envie de donner un coup de main ? <a href=\"#contribuer\">Contribuer</a>",
     "In design: the app is not available to download yet. Want to lend a hand? <a href=\"#contribuer\">Contribute</a>"),
    ("Maquette de l'écran d'accueil de VIBES : petite Étincelle du jour, activités de la semaine et accès à l'aide",
     "Mockup of the VIBES home screen: today's small Spark, this week's activities and access to help"),
    ("Maquette à ajouter : ", "Mockup to add: "),

    # --- bandeau des passions ---
    ("Des passions pour tous : football, musique, photo, animés, chorale, randonnée urbaine, jeux de société, cinéma, lecture, révision collective",
     "Passions for everyone: football, music, photography, anime, choir, urban hiking, board games, cinema, reading, group study"),
    ("</svg>Musique</li>", "</svg>Music</li>"),
    ("</svg>Photo</li>", "</svg>Photography</li>"),
    ("</svg>Animés</li>", "</svg>Anime</li>"),
    ("</svg>Chorale</li>", "</svg>Choir</li>"),
    ("</svg>Randonnée urbaine</li>", "</svg>Urban hiking</li>"),
    ("</svg>Jeux de société</li>", "</svg>Board games</li>"),
    ("</svg>Cinéma</li>", "</svg>Cinema</li>"),
    ("</svg>Lecture</li>", "</svg>Reading</li>"),
    ("</svg>Révision collective</li>", "</svg>Group study</li>"),

    # --- constat ---
    ('>Le constat<', '>The situation<'),
    ("Toujours connectés. Et si nous nous retrouvions davantage ?", "Always connected. What if we met up more?"),
    ("Entre les cours, les écrans et les journées qui se ressemblent, il n'est pas toujours facile de rencontrer de nouvelles personnes, de trouver des activités qui nous correspondent ou de prendre du temps pour soi.",
     "Between classes, screens and days that all look alike, it isn't always easy to meet new people, find activities that suit us or take time for ourselves."),
    ("Pourtant, une passion partagée, une activité improvisée ou une petite habitude peuvent ouvrir la porte à de nouvelles expériences.",
     "Yet a shared passion, an impromptu activity or a small habit can open the door to new experiences."),
    ("C'est de cette idée qu'est né VIBES.", "That's the idea VIBES was born from."),
    ("<figcaption>Dans l'écran</figcaption>", "<figcaption>On the screen</figcaption>"),
    ("<figcaption>Dehors</figcaption>", "<figcaption>Outside</figcaption>"),
    ("Illustration : une personne seule devant un écran plein de notifications",
     "Illustration: a person alone in front of a screen full of notifications"),

    # --- quatre couches ---
    ("Pourquoi VIBES existe", "Why VIBES exists"),
    ("Derrière l'écran, quatre choses qui s'additionnent.", "Behind the screen, four things that add up."),
    ("Ce n'est pas un manque de volonté. C'est ce que nous observons autour de nous, sur le campus.",
     "It's not a lack of willpower. It's what we see around us, on campus."),
    ("<h3>L'attraction</h3>", "<h3>Attraction</h3>"),
    ("Le scroll est conçu pour retenir. Y rester ne dit rien de ta volonté.",
     "Scrolling is designed to hold you. Staying says nothing about your willpower."),
    ("<h3>Le vide</h3>", "<h3>The void</h3>"),
    ("Quand on pose le téléphone, on ne sait pas toujours quoi faire d'aussi bien, ni avec qui.",
     "When you put the phone down, you don't always know what to do that's as good, or with whom."),
    ("<h3>Le silence</h3>", "<h3>The silence</h3>"),
    ("On sait souvent de quoi on a besoin. Il manque un endroit pour se l'avouer sans être jugé.",
     "We often know what we need. What's missing is a place to admit it without being judged."),
    ("<h3>L'invisible</h3>", "<h3>The invisible</h3>"),
    ("Des outils de bien-être existent, mais beaucoup d'étudiants ne les connaissent pas, ou ne s'y reconnaissent pas.",
     "Well-being tools exist, but many students don't know about them, or don't see themselves in them."),

    # --- trois intentions ---
    (">L'approche<", ">The approach<"),
    ("Trois gestes. Une autre façon de vivre le campus.", "Three gestures. Another way to live campus life."),
    ("<h3>Découvrir</h3>", "<h3>Discover</h3>"),
    ("Retrouve des jeunes qui partagent tes passions. Explore les activités, découvre les clubs et trouve des occasions de faire le premier pas.",
     "Meet young people who share your passions. Explore activities, discover clubs and find chances to take the first step."),
    ("<h3>S'outiller</h3>", "<h3>Equip yourself</h3>"),
    ("Prends un moment pour toi, mets des mots sur ton humeur et découvre des conseils simples pour mieux prendre soin de toi.",
     "Take a moment for yourself, put words on your mood and discover simple tips to take better care of yourself."),
    ("<h3>Ancrer</h3>", "<h3>Anchor</h3>"),
    ("Transforme les petites intentions en habitudes. Essaie de nouvelles activités, relève de petites Étincelles et avance à ton rythme.",
     "Turn small intentions into habits. Try new activities, take on small Étincelles (Sparks) and move at your own pace."),
    ("Pas besoin de tout changer. Parfois, une petite action suffit pour commencer.",
     "No need to change everything. Sometimes one small action is enough to get started."),

    # --- cinq dimensions ---
    ("Le bien-être, en cinq dimensions", "Well-being, in five dimensions"),
    ("Prendre soin de soi, c'est aussi vivre pleinement.", "Taking care of yourself also means living fully."),
    ("Le bien-être ne se résume pas à un seul aspect de notre vie. Il se construit à travers nos relations, notre corps, nos émotions, notre esprit et notre quotidien.",
     "Well-being isn't just one part of our life. It is built through our relationships, our body, our emotions, our mind and our daily life."),
    ("<h3>Le lien social</h3>", "<h3>Social connection</h3>"),
    ("Créer des liens, partager ses passions et trouver sa place.", "Building bonds, sharing passions and finding your place."),
    ("<h3>Le bien-être physique</h3>", "<h3>Physical well-being</h3>"),
    ("Bouger, marcher et retrouver le plaisir des activités accessibles.", "Moving, walking and rediscovering the joy of accessible activities."),
    ("<h3>L'équilibre émotionnel</h3>", "<h3>Emotional balance</h3>"),
    ("Mieux comprendre ce que l'on ressent et savoir vers qui se tourner lorsqu'on en a besoin.",
     "Understanding what you feel and knowing who to turn to when you need to."),
    ("<h3>Le bien-être mental</h3>", "<h3>Mental well-being</h3>"),
    ("Prendre du recul, souffler, apprendre et créer.", "Stepping back, taking a breath, learning and creating."),
    ("<h3>L'alimentation</h3>", "<h3>Food</h3>"),
    ("Découvrir des repères simples pour mieux prendre soin de soi au quotidien.",
     "Discovering simple guidelines to take better care of yourself every day."),

    # --- expérience ---
    (">L'expérience<", ">The experience<"),
    ("Pensé pour les vrais moments de la vie étudiante.", "Made for the real moments of student life."),
    ("De la découverte d'une activité au petit moment que l'on s'accorde pour soi, VIBES veut rendre les premiers pas plus simples.",
     "From discovering an activity to the little moment you give yourself, VIBES wants to make first steps easier."),
    ("<h3>Explorer les activités</h3>", "<h3>Explore activities</h3>"),
    ("Trouve des occasions de jouer, de créer, de bouger ou de partager une passion avec d'autres étudiants.",
     "Find chances to play, create, move or share a passion with other students."),
    ("Exemples de catégories d'activités", "Examples of activity categories"),
    ("</svg>Détente</li>", "</svg>Relaxation</li>"),
    ("</svg>Solidarité</li>", "</svg>Solidarity</li>"),
    ("Maquette de l'écran Découvrir : activités du campus filtrables par jour, gratuité ou proximité",
     "Mockup of the Discover screen: campus activities filterable by day, free or nearby"),
    ("Maquette du détail d'une activité : soirée anime au campus, informations pratiques et bouton Je participe",
     "Mockup of an activity page: anime night on campus, practical information and an I'm in button"),
    ("<h3>Prendre un moment pour soi</h3>", "<h3>Take a moment for yourself</h3>"),
    ("Avec Mon Mood et My Safe Place, découvre un espace personnel pour exprimer ton ressenti et trouver des pistes adaptées à tes besoins.",
     "With Mon Mood and My Safe Place, discover a personal space to express how you feel and find ideas that fit your needs."),
    ("Facultatif, privé, sans score et sans diagnostic.", "Optional, private, no score and no diagnosis."),
    ("Maquette de Mon Mood : choix de ressenti du jour, avec la mention que l'humeur n'est pas un score",
     "Mockup of Mon Mood: choose how you feel today, with a note that mood is not a score"),
    ("<h3>Faire durer les bonnes habitudes</h3>", "<h3>Make good habits last</h3>"),
    ("Grâce aux Étincelles, aux conseils et aux rappels doux, avance à ton rythme, sans pression ni compétition.",
     "With Étincelles (Sparks), tips and gentle reminders, move at your own pace, with no pressure and no competition."),
    ("Des Étincelles, par exemple :", "Étincelles (Sparks), for example:"),
    ("Exemples d'Étincelles envisagées", "Examples of planned Étincelles"),
    ("</svg>Une marche</li>", "</svg>A walk</li>"),
    ("</svg>Un message à un camarade</li>", "</svg>A message to a classmate</li>"),
    ("</svg>Une pause sans écran</li>", "</svg>A screen-free break</li>"),
    ("</svg>Un repas équilibré</li>", "</svg>A balanced meal</li>"),
    ("Maquette des Tips VIBES : petits conseils partagés par des jeunes, classés par thème",
     "Mockup of Tips VIBES: small tips shared by young people, sorted by theme"),
    ("La technologie ouvre la porte. Les expériences se vivent dehors.",
     "Technology opens the door. Experiences are lived outside."),

    # --- heures vécues ---
    ("Ce qui nous distingue", "What sets us apart"),
    ("On ne cherche pas à te garder dans l'application.", "We're not trying to keep you in the app."),
    ("Beaucoup d'applications se mesurent au temps qu'on y passe. VIBES se mesure à celui qu'on y passe <strong>en moins</strong>.",
     "Many apps are measured by the time you spend in them. VIBES is measured by the time you spend in it <strong>less</strong>."),
    ("Notre indicateur central : les <strong>heures vécues</strong>. Ce sont les heures réelles de match, de marche, de répétition de chorale ou de création que VIBES a aidé à déclencher.",
     "Our central indicator: <strong>lived hours</strong>. These are the real hours of matches, walks, choir rehearsals or creating that VIBES helped trigger."),
    ("Le temps passé dans l'application est suivi comme un signal d'alerte, pas comme un objectif.",
     "Time spent in the app is tracked as a warning signal, not as a goal."),
    ("Indicateur en cours de définition. Aucun résultat n'est avancé à ce stade.",
     "Indicator still being defined. No result is claimed at this stage."),

    # --- crew ---
    (">Le Crew<", ">The Crew<"),
    ("Le premier pas est plus simple quand on n'est pas seul.", "The first step is easier when you're not alone."),
    ("Un match, une marche, une séance de musique ou une nouvelle activité : parfois, il suffit de trouver quelques personnes avec qui partager le moment.",
     "A match, a walk, a music session or a new activity: sometimes all it takes is finding a few people to share the moment with."),
    ("Avec le Crew, VIBES veut faciliter l'organisation des participations et aider chacun à aborder une première expérience collective plus sereinement.",
     "With the Crew, VIBES wants to make it easier to organise who's coming and help everyone approach a first group experience more calmly."),
    ("Des passions en commun. Des expériences à vivre.", "Shared passions. Experiences to live."),
    ("Tu repères une activité qui te parle.", "You spot an activity that speaks to you."),
    ("Tu rejoins un petit groupe pour t'organiser.", "You join a small group to get organised."),
    ("Vous vous retrouvez sur place, pour de vrai.", "You meet up in person, for real."),
    ("Prévu : un chat réservé aux inscrits de l'activité, sans messages privés. Le Crew sert à participer, pas à remplacer la vraie vie.",
     "Planned: a chat reserved for people signed up to the activity, with no private messages. The Crew is for taking part, not for replacing real life."),
    ("Maquette de l'écran Mon Crew : petits groupes autour d'activités du campus",
     "Mockup of the Mon Crew screen: small groups around campus activities"),

    # --- pensé pour ici ---
    ("Pensé pour ici", "Made for here"),
    ("Fait pour le quotidien des étudiants du Bénin.", "Made for the daily life of students in Benin."),
    ("Peu de données mobiles, un budget serré, des trajets parfois longs : on y pense dès la conception. <span class=\"pill\">Prévu dans la conception</span>",
     "Little mobile data, a tight budget, sometimes long commutes: we think about it from the start. <span class=\"pill\">Planned in the design</span>"),
    ("<h3>Une application légère</h3>", "<h3>A lightweight app</h3>"),
    ("Une application web, pensée pour les petits forfaits de données et les téléphones plus anciens.",
     "A web app, designed for small data plans and older phones."),
    ("<h3>Tout savoir avant d'y aller</h3>", "<h3>Know before you go</h3>"),
    ("Le coût réel, la distance et la durée affichés avant de s'engager.", "Real cost, distance and duration shown before you commit."),
    ("<h3>Le gratuit d'abord</h3>", "<h3>Free first</h3>"),
    ("Des activités gratuites mises en avant, pour que le budget ne bloque pas l'envie.",
     "Free activities highlighted, so that budget doesn't get in the way of wanting to go."),
    ("<h3>Dans nos mots</h3>", "<h3>In our own words</h3>"),
    ("Le français d'abord, des conseils écrits par des jeunes béninois. Les langues locales sont à l'étude.",
     "French first, with tips written by young Beninese people. Local languages are being studied."),
    ("<h3>Pour les débutants</h3>", "<h3>For beginners</h3>"),
    ("Des activités ouvertes à tous les niveaux, avec des informations d'accessibilité.",
     "Activities open to all levels, with accessibility information."),

    # --- engagements ---
    (">Nos engagements<", ">Our commitments<"),
    ("Ton bien-être. Ton rythme. Tes choix.", "Your well-being. Your pace. Your choices."),
    ("<h3>Respect de la vie privée</h3>", "<h3>Respect for your privacy</h3>"),
    ("Ce que tu partages dans ton espace personnel reste privé selon les règles prévues par VIBES.",
     "What you share in your personal space stays private, according to the rules set by VIBES."),
    ("<h3>La liberté de choisir</h3>", "<h3>Freedom to choose</h3>"),
    ("Tu choisis les activités auxquelles tu souhaites participer et ce que tu veux partager.",
     "You choose which activities you want to join and what you want to share."),
    ("<h3>Pas de pression</h3>", "<h3>No pressure</h3>"),
    ("Pas de compétition sur ton bien-être, pas de culpabilisation lorsque tu prends une pause.",
     "No competition over your well-being, no guilt when you take a break."),
    ("<h3>Des activités encadrées</h3>", "<h3>Supervised activities</h3>"),
    ("Les événements seront soumis à une validation et les organisateurs devront respecter les règles de sécurité prévues par le projet.",
     "Events will be checked before publication, and organisers will have to follow the safety rules set by the project."),
    ("<h3>Une aide facile à trouver</h3>", "<h3>Help that's easy to find</h3>"),
    ("Un accès « Besoin d'aide ? » est prévu sur les écrans, pour t'orienter vers une personne ou un service fiable.",
     "A “Need help?” access is planned on the screens, to point you to a trusted person or service."),
    ("<h3>Une limite claire</h3>", "<h3>A clear limit</h3>"),
    ("VIBES est une initiative de prévention et de bien-être. Ce n'est ni un service de soins, ni un outil de diagnostic, ni un conseil médical ou psychologique.",
     "VIBES is a prevention and well-being initiative. It is not a care service, a diagnostic tool, or medical or psychological advice."),

    # --- état du projet ---
    ("En toute transparence", "In full transparency"),
    ("Où en est VIBES ?</h2>", "Where is VIBES at?</h2>"),
    ("VIBES est un projet étudiant en construction. Voici ce qui existe, ce qui avance et ce qui est envisagé.",
     "VIBES is a student project under construction. Here is what exists, what is moving and what is envisioned."),
    ("Déjà là</h3>", "Already here</h3>"),
    ("<li>Un dossier de conception du projet</li>", "<li>A project design document</li>"),
    ("<li>Un Design System</li>", "<li>A Design System</li>"),
    ("<li>10 écrans de maquette</li>", "<li>10 mockup screens</li>"),
    ("En cours</h3>", "In progress</h3>"),
    ("<li>La construction d'un premier MVP web léger</li>", "<li>Building a first lightweight web MVP</li>"),
    ("<li>Un premier questionnaire auprès de 10 étudiants (échantillon trop petit pour conclure)</li>",
     "<li>A first questionnaire with 10 students (too small a sample to conclude)</li>"),
    ("<li>La conception avec les étudiants : entretiens et tests de maquettes</li>",
     "<li>Designing with students: interviews and mockup tests</li>"),
    ("Envisagé</h3>", "Envisioned</h3>"),
    ("<li>Un pilote sur campus</li>", "<li>A pilot on campus</li>"),
    ("<li>Des enquêtes dans d'autres écoles et universités</li>", "<li>Surveys in other schools and universities</li>"),
    ("<li>Des pistes avec des lieux et des associations. Aucun partenariat n'est annoncé à ce stade.</li>",
     "<li>Leads with venues and associations. No partnership is announced at this stage.</li>"),

    # --- contribuer ---
    ('<p class="eyebrow eyebrow--purple">Contribuer</p>', '<p class="eyebrow eyebrow--purple">Contribute</p>'),
    ("VIBES se construit avec toi.", "VIBES is built with you."),
    ("Le projet est en cours de conception, et c'est maintenant que ton avis compte le plus. Choisis ce qui te ressemble.",
     "The project is being designed, and right now your opinion matters most. Pick what suits you."),
    ("<h3>Écrire des Tips</h3>", "<h3>Write Tips</h3>"),
    ("Rejoins des jeunes pour rédiger des conseils courts, dans nos mots et avec notre culture.",
     "Join young people to write short tips, in our own words and with our culture."),
    ("<h3>Tester et donner ton avis</h3>", "<h3>Test and give your feedback</h3>"),
    ("Entretiens, essais de maquettes : dis-nous ce qui te parle et ce qui ne te parle pas.",
     "Interviews, mockup tests: tell us what speaks to you and what doesn't."),
    ("<h3>Proposer une activité ou un club</h3>", "<h3>Suggest an activity or a club</h3>"),
    ("Match, karaoké, marche, atelier : fais-toi connaître comme organisateur ou organisatrice. Chaque événement sera validé avant publication.",
     "Match, karaoke, walk, workshop: make yourself known as an organiser. Every event will be checked before publication."),
    ("<h3>Devenir ambassadeur ou ambassadrice</h3>", "<h3>Become an ambassador</h3>"),
    ("Fais connaître VIBES autour de toi et aide à lancer les premières activités sur ton campus.",
     "Spread the word about VIBES and help launch the first activities on your campus."),
    ("<h3>Relire les contenus santé</h3>", "<h3>Review health content</h3>"),
    ("Étudiant·e en fin de formation de santé ou professionnel·le : aide-nous à vérifier les conseils avant leur publication.",
     "Final-year health student or professional: help us check the tips before they are published."),
    ("<h3>Lieux, clubs et associations</h3>", "<h3>Venues, clubs and associations</h3>"),
    ("Tu animes un lieu ou une association ? Parlons de ce que nous pourrions faire ensemble.",
     "Do you run a venue or an association? Let's talk about what we could do together."),
    ("Je me propose <span", "I'd like to help <span"),
    (", écrire des Tips (s'ouvre dans un nouvel onglet)", ", write Tips (opens in a new tab)"),
    (", tester et donner mon avis (s'ouvre dans un nouvel onglet)", ", test and give feedback (opens in a new tab)"),
    (", proposer une activité ou un club (s'ouvre dans un nouvel onglet)", ", suggest an activity or a club (opens in a new tab)"),
    (", devenir ambassadeur ou ambassadrice (s'ouvre dans un nouvel onglet)", ", become an ambassador (opens in a new tab)"),
    (", relire les contenus santé (s'ouvre dans un nouvel onglet)", ", review health content (opens in a new tab)"),
    (", lieux, clubs et associations (s'ouvre dans un nouvel onglet)", ", venues, clubs and associations (opens in a new tab)"),
    ("J'ai une autre idée <span", "I have another idea <span"),
    (" (s'ouvre dans un nouvel onglet)</span>", " (opens in a new tab)</span>"),
    ("Les messages passent par GitHub et sont publics : n'y mets ni numéro de téléphone ni adresse e-mail. Pour écrire en privé : <a href=\"mailto:prosperaffoukou@outlook.com\">prosperaffoukou@outlook.com</a>.",
     "Messages go through GitHub and are public: don't put a phone number or an e-mail address in them. To write privately: <a href=\"mailto:prosperaffoukou@outlook.com\">prosperaffoukou@outlook.com</a>."),

    # --- FAQ ---
    ("Questions fréquentes", "Frequently asked questions"),
    ("On te répond simplement.", "Simple answers."),
    ("<summary>VIBES est-il déjà disponible ?</summary>", "<summary>Is VIBES available yet?</summary>"),
    ("Pas encore. Le projet est en cours de conception : les maquettes existent, mais l'application n'est pas encore téléchargeable.",
     "Not yet. The project is being designed: the mockups exist, but the app can't be downloaded yet."),
    ("<summary>VIBES, est-ce un service médical ?</summary>", "<summary>Is VIBES a medical service?</summary>"),
    ("Non. C'est une initiative de prévention et de bien-être. VIBES ne pose pas de diagnostic, ne donne pas de score, et t'oriente vers une personne ou un service fiable si cela te dépasse.",
     "No. It's a prevention and well-being initiative. VIBES makes no diagnosis, gives no score, and points you to a trusted person or service if it's too much."),
    ("<summary>Ce que j'écris reste-t-il privé ?</summary>", "<summary>Does what I write stay private?</summary>"),
    ("Ce que tu écris dans My Safe Place est privé, selon les règles prévues par VIBES. Les réponses sur ton ressenti sont facultatives.",
     "What you write in My Safe Place is private, according to the rules set by VIBES. Answers about how you feel are optional."),
    ("<summary>C'est quoi, le Crew ?</summary>", "<summary>What is the Crew?</summary>"),
    ("Un petit groupe qui se forme autour d'une activité, pour s'organiser et confirmer les présences. L'idée : ne pas avoir à venir seul·e la première fois.",
     "A small group that forms around an activity, to get organised and confirm who's coming. The idea: not having to show up alone the first time."),
    ("<summary>VIBES est-il un réseau social ou une application de rencontres ?</summary>",
     "<summary>Is VIBES a social network or a dating app?</summary>"),
    ("Non. Pas de fil public, pas de likes, pas de classements. Les activités sont publiques et se vivent en petits groupes.",
     "No. No public feed, no likes, no rankings. Activities are public and are lived in small groups."),
    ("<summary>Faut-il beaucoup de données mobiles ?</summary>", "<summary>Does it need a lot of mobile data?</summary>"),
    ("L'objectif est une application web légère, pensée pour les petits forfaits et les téléphones plus anciens.",
     "The goal is a lightweight web app, designed for small data plans and older phones."),
    ("<summary>Qui est derrière VIBES ?</summary>", "<summary>Who is behind VIBES?</summary>"),
    ("Une équipe de trois étudiants de l'UNSTIM, à Abomey, au Bénin : Charmel Prosper Affoukou (Team Lead), Laurinda Adéyinka Adanlao et Judicaël Karol Doboevi. Les contenus de l'application sont écrits avec des jeunes, et les contenus de santé seront relus avant publication.",
     "A team of three UNSTIM students in Abomey, Benin: Charmel Prosper Affoukou (Team Lead), Laurinda Adéyinka Adanlao and Judicaël Karol Doboevi. The app's content is written with young people, and health content will be reviewed before publication."),

    # --- CTA final ---
    ("Et si la prochaine bonne chose commençait ici ?", "What if the next good thing started here?"),
    ("Une passion à découvrir. Une activité à essayer. Une habitude à construire.",
     "A passion to discover. An activity to try. A habit to build."),
    ("VIBES veut aider les étudiants à faire davantage de place à ce qui leur fait du bien.",
     "VIBES wants to help students make more room for what does them good."),
    ("Découvrir notre vision <span", "Discover our vision <span"),
    ('href="#contribuer">Contribuer</a>\n        </div>', 'href="#contribuer">Contribute</a>\n        </div>'),

    # --- photos ---
    ("Étudiantes qui rient ensemble sur un terrain de sport", "Students laughing together on a sports court"),
    ("Quatre étudiants assis sur des marches avec des ordinateurs portables, l'un d'eux prend un selfie",
     "Four students sitting on steps with laptops, one of them taking a selfie"),
    ("Cinq mains qui forment une étoile vers le ciel", "Five hands forming a star against the sky"),
    ("Photos&nbsp;: Iwaria Inc et Muhammad-Taha Ibrahim, via Unsplash.", "Photos: Iwaria Inc and Muhammad-Taha Ibrahim, via Unsplash."),
    ("Équipe&nbsp;: Charmel Prosper Affoukou, Laurinda Adéyinka Adanlao, Judicaël Karol Doboevi.", "Team: Charmel Prosper Affoukou, Laurinda Adéyinka Adanlao, Judicaël Karol Doboevi."),

    # --- footer ---
    ("Makes lives happen.</p>", "Makes lives happen.</p>"),
    ("Projet étudiant, UNSTIM, Abomey (Bénin). En cours de conception.",
     "Student project, UNSTIM, Abomey (Benin). In design."),
    ('aria-label="Pied de page"', 'aria-label="Footer"'),
    ('<a href="#intentions">Approche</a>\n      <a href="#experience">Expérience</a>\n      <a href="#engagements">Engagements</a>\n      <a href="#etat">Où en est VIBES ?</a>\n      <a href="#equipe">L\'équipe</a>\n      <a href="#contribuer">Contribuer</a>\n      <a href="#faq">Questions</a>',
     '<a href="#intentions">Approach</a>\n      <a href="#experience">Experience</a>\n      <a href="#engagements">Commitments</a>\n      <a href="#etat">Where is VIBES at?</a>\n      <a href="#equipe">The team</a>\n      <a href="#contribuer">Contribute</a>\n      <a href="#faq">Questions</a>'),
    # --- section équipe ---
    ('<p class="eyebrow eyebrow--blue">L\'équipe</p>', '<p class="eyebrow eyebrow--blue">The team</p>'),
    ('<h2>Ceux qui construisent VIBES.</h2>', '<h2>The people building VIBES.</h2>'),
    ('<p class="section__intro">Un projet étudiant porté par trois personnes de l\'<abbr title="Université Nationale des Sciences, Technologies, Ingénierie et Mathématiques d\'Abomey">UNSTIM</abbr>, au Bénin.</p>', '<p class="section__intro">A student project carried by three people from <abbr title="National University of Sciences, Technology, Engineering and Mathematics of Abomey">UNSTIM</abbr>, in Benin.</p>'),
    ('<p class="team__school"><abbr title="Université Nationale des Sciences, Technologies, Ingénierie et Mathématiques d\'Abomey">UNSTIM</abbr> · Abomey, Bénin</p>', '<p class="team__school"><abbr title="National University of Sciences, Technology, Engineering and Mathematics of Abomey">UNSTIM</abbr> · Abomey, Benin</p>'),
    ('<p class="team__role">ML Engineer en formation &amp; Développeuse Front-end</p>', '<p class="team__role">ML Engineer in training &amp; Front-end Developer</p>'),
    ('alt="Photo de Charmel Prosper Affoukou"', 'alt="Photo of Charmel Prosper Affoukou"'),
    ('alt="Photo de Laurinda Adéyinka Adanlao"', 'alt="Photo of Laurinda Adéyinka Adanlao"'),
    ('alt="Photo de Judicaël Karol Doboevi"', 'alt="Photo of Judicaël Karol Doboevi"'),
    # --- refonte : nouvelles chaînes ---
    ("Une application pensée <strong>par des jeunes, pour des jeunes</strong> : retrouver des jeunes qui partagent tes passions, prendre soin de toi et construire des habitudes qui te font du bien.",
     "An app designed <strong>by young people, for young people</strong>: find young people who share your passions, take care of yourself and build habits that do you good."),
    (">Rencontrer l'équipe</a>", ">Meet the team</a>"),
    ("Ce que les adultes comprennent mal", "What adults often misunderstand"),
    ("On y voit un manque de volonté. Nous observons surtout un manque d'alternatives et de personnes vers qui se tourner : quand les écrans isolent, il devient aussi plus difficile de trouver une écoute réelle, par exemple face au harcèlement ou à un problème de santé. C'est pourquoi VIBES prévoit des contacts de confiance et des lignes d'aide gratuites, à un clic.",
     "They see a lack of willpower. We mostly observe a lack of alternatives and of people to turn to: when screens isolate, it also becomes harder to find a real listening ear, for example in cases of harassment or a health problem. That is why VIBES plans trusted contacts and free helplines, one tap away."),
    ("Premier questionnaire (10 étudiants, 4 écoles) : 5 sur 10 trouvent leur temps d'écran trop long, 4 sur 10 disent ne pas avoir avec qui sortir. L'échantillon est trop petit pour conclure : c'est un premier signal.",
     "First questionnaire (10 students, 4 schools): 5 in 10 find their screen time too long, 4 in 10 say they have no one to go out with. The sample is too small to conclude: it is a first signal."),
    ("<strong>Cinq dimensions du bien-être :</strong> le lien social · le bien-être physique · l'équilibre émotionnel · le bien-être mental · l'alimentation.",
     "<strong>Five dimensions of well-being:</strong> social connection · physical well-being · emotional balance · mental well-being · food."),
    ("Filtre par jour, gratuité ou distance.", "Filter by day, free or distance."),
    ("Le détail d'une activité", "An activity in detail"),
    ("Les infos pratiques d'abord : lieu public, gratuit, tous niveaux.", "Practical info first: public venue, free, all levels."),
    ("Un petit groupe autour d'une activité, pour ne pas venir seul·e.", "A small group around an activity, so you do not have to come alone."),
    ("Mon Mood : facultatif, privé, sans score ni diagnostic.", "Mon Mood: optional, private, no score, no diagnosis."),
    ("Les Tips VIBES", "VIBES Tips"),
    ("Des conseils courts écrits par des jeunes ; le contenu santé sera relu.", "Short tips written by young people; health content will be reviewed."),
    ("Ces maquettes ont été générées avec des outils d'IA, faute de designer pour l'instant. Elles sont en anglais, sujettes à modification, et montrent la direction : l'application sera d'abord en français.",
     "These mockups were generated with AI tools, as we have no designer yet. They are in English, subject to change, and show the direction: the app will be French first."),
    ("Une écoute réelle, à un clic", "Real listening, one tap away"),
    ("Quand l'isolement s'installe, trouver une vraie écoute devient plus difficile (harcèlement, santé). Un accès « Besoin d'aide ? » est prévu sur les écrans, vers des contacts de confiance et des lignes d'aide gratuites, dont la liste est en cours de vérification.",
     "When isolation sets in, finding real listening gets harder (harassment, health). A \"Need help?\" access is planned on the screens, pointing to trusted contacts and free helplines, whose list is still being verified."),
    ("Fait pour le quotidien des étudiants du Bénin", "Made for the daily life of students in Benin"),
    ("10 écrans de maquette (générés avec des outils d'IA)", "10 mockup screens (generated with AI tools)"),
    ("Calendrier visé", "Target timeline"),
    ("Nov. – déc. 2026", "Nov. – Dec. 2026"), ("Janv. – mars 2027", "Jan. – Mar. 2027"), ("Avr. – sept. 2027", "Apr. – Sep. 2027"),
    ("Oct. – nov. 2027", "Oct. – Nov. 2027"), ("Déc. 2027 – janv. 2028", "Dec. 2027 – Jan. 2028"),
    ("<span>Écouter</span>", "<span>Listen</span>"), ("<span>Construire</span>", "<span>Build</span>"), ("<span>Préparer</span>", "<span>Prepare</span>"),
    ("<span>Pilote</span>", "<span>Pilot</span>"), ("<span>Partager</span>", "<span>Share</span>"),
    ("Enquête auprès de 30 étudiants ou plus, tests des maquettes.", "Survey of 30 or more students, mockup tests."),
    ("Premier MVP web avec 20 à 30 testeurs sur le campus.", "First web MVP with 20 to 30 testers on campus."),
    ("Enquêtes élargies, ambassadeurs, relecture santé.", "Wider surveys, ambassadors, health review."),
    ("4 à 6 semaines supervisées, en période de cours.", "4 to 6 supervised weeks, during term."),
    ("Un rapport d'apprentissage ouvert.", "An open learning report."),
    ("Dates indicatives. Les étapes dépendant d'un financement démarrent à l'arrivée des fonds.", "Indicative dates. Steps that depend on funding start when funds arrive."),
    ("Un projet étudiant, par des jeunes, pour des jeunes, porté par trois personnes de l'<abbr title=\"Université Nationale des Sciences, Technologies, Ingénierie et Mathématiques d'Abomey\">UNSTIM</abbr>, au Bénin.",
     "A student project, by young people, for young people, carried by three people from <abbr title=\"National University of Sciences, Technology, Engineering and Mathematics of Abomey\">UNSTIM</abbr>, in Benin."),
    ("Data &amp; Systèmes", "Data &amp; Systems"),
    ("Tester, donner ton avis, devenir ambassadeur", "Test, give feedback, become an ambassador"),
    ("Entretiens, essais de maquettes, premières activités sur ton campus : dis-nous ce qui te parle et ce qui ne te parle pas.",
     "Interviews, mockup tests, first activities on your campus: tell us what speaks to you and what does not."),
    ("Proposer une activité, un club ou un lieu", "Suggest an activity, a club or a venue"),
    ("Match, karaoké, marche, atelier : fais-toi connaître comme organisateur, organisatrice, association ou lieu. Chaque événement sera validé avant publication.",
     "Match, karaoke, walk, workshop: make yourself known as an organiser, association or venue. Every event will be validated before publication."),
    ("Découvrir des activités et rencontrer des jeunes qui partagent tes passions", "Discover activities and meet young people who share your passions"),
    ("Un étudiant prend un moment pour lui sur son téléphone", "A student takes a moment for himself on his phone"),
    ("Ancrer de bonnes habitudes et avancer à son rythme", "Anchoring good habits and moving at your own pace"),
    ('Makes lives<br>happen.', 'Makes lives<br>happen.'),
]

# Tickets GitHub pré-remplis : titre français -> (titre, corps) anglais.
ISSUE_SIGNOFF = "(This page is public: don't share a phone number or an e-mail.)"
ISSUES = {
    "Contribution : écrire des Tips": ("Contribution: write Tips",
        "Hi! I'd like to contribute to VIBES by writing Tips.\n\nWhat I'm offering: \n\nMy field / school: \n\n" + ISSUE_SIGNOFF),
    "Contribution : tester et donner mon avis": ("Contribution: test and give feedback",
        "Hi! I'd like to test VIBES and give my feedback.\n\nWhat I'm offering: \n\nMy field / school: \n\n" + ISSUE_SIGNOFF),
    "Contribution : proposer une activité ou un club": ("Contribution: suggest an activity or a club",
        "Hi! I'd like to suggest an activity or a club on VIBES.\n\nThe activity or club: \n\nMy field / school: \n\n" + ISSUE_SIGNOFF),
    "Contribution : devenir ambassadeur ou ambassadrice": ("Contribution: become an ambassador",
        "Hi! I'd like to become a VIBES ambassador.\n\nMy campus: \n\nMy field: \n\n" + ISSUE_SIGNOFF),
    "Contribution : relire les contenus santé": ("Contribution: review health content",
        "Hi! I'd like to review VIBES health content.\n\nMy profile (training / job): \n\n" + ISSUE_SIGNOFF),
    "Contribution : lieu, club ou association": ("Contribution: venue, club or association",
        "Hi! I represent a venue, a club or an association and I'd like to talk.\n\nName: \n\nWhat we could do together: \n\n" + ISSUE_SIGNOFF),
    "Une idée pour VIBES": ("An idea for VIBES",
        "Hi! I have an idea for VIBES:\n\n" + ISSUE_SIGNOFF),
}


def fail(msg):
    sys.exit("ERREUR : " + msg)


def translate_issue(m):
    url = m.group(0)
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query, keep_blank_values=True))
    title = q.get("title", "")
    if title not in ISSUES:
        fail("ticket GitHub non traduit : %r" % title)
    t, b = ISSUES[title]
    return "%s://%s%s?title=%s&body=%s" % (parts.scheme, parts.netloc, parts.path, quote(t, safe=""), quote(b, safe="'!"))


OBSOLETE = []


def main():
    s = SRC.read_text(encoding="utf-8")

    s = re.sub(r"https://github\.com/Charmel7/vibes/issues/new\?[^\"]+", translate_issue, s)

    for fr, en in sorted(T, key=lambda p: -len(p[0])):
        if fr not in s:
            OBSOLETE.append(fr[:70])
            continue
        s = s.replace(fr, en)

    # chemins relatifs depuis /en/
    s = s.replace('href="styles.css"', 'href="../styles.css"').replace('src="main.js"', 'src="../main.js"')
    s = s.replace('src="assets/', 'src="../assets/').replace('src="assets_1/', 'src="../assets_1/')
    s = s.replace('href="favicon.svg"', 'href="../favicon.svg"').replace('href="assets/brand/', 'href="../assets/brand/')

    if OBSOLETE:
        print("Entrées de traduction devenues inutiles : %d (ex. %r)" % (len(OBSOLETE), OBSOLETE[0]))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(s, encoding="utf-8")
    print("OK :", OUT.relative_to(ROOT), "(%d octets)" % len(s.encode("utf-8")))


if __name__ == "__main__":
    main()
