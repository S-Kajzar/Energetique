# Note de livraison — Énergétique : cours et activités interactifs

## Construction reprise du dépôt « Chaîne fonctionnelle »

**Sources** : le chapitre « Énergétique » fourni en trois PDF de pages photographiées (cours : 10 pages ; exercices :
deux pages de QCM et d'exercices, plus une page d'exercices de dynamique). **Dépôt de référence, non modifié** :
« Chaîne fonctionnelle » (construction : générateur, gabarit, accueil, pastilles, cartes, cours, tests).

- **Gabarit** : `src/gabarit-exercice-interactif.html` est copié tel quel depuis le dépôt « Chaîne fonctionnelle »
  (fichier identique, vérifié octet par octet ; c'est lui-même la copie conforme du gabarit RDM). Comme dans ce dépôt,
  seules les entrées réservées au sujet du moteur applicatif sont remplacées, chaque remplacement étant vérifié :
  `CONSEIL_MIN` (lue dans `window.__CONSEIL_MIN__`), `DECOR` et `DR_NAMES` (vides : les tracés se font dans l'atelier
  de construction), le texte de la fenêtre « Imprimer les DR », le libellé « Diagramme validé », devenu « Réponses
  validées ». Le correctif d'impression des tracés relevé dans le dépôt RDM est repris.
- **Générateur** (`src/generer.py`) : même organisation (rendu des questions, `prepare_exo`, parties pondérées par
  leur durée, documents dans le panneau latéral, aiguillage `?ex=…` exécuté avant les moteurs, accueil en cartes de
  même taille avec 3 à 5 mots-clés, pastilles Niveau 1 / Niveau 2, rubrique « Études de cas » annoncée « En cours
  d'édition »). Le contenu est réparti en modules : `commun.py`, `activites.py`, `construction.py`,
  `cours_analytique.py`, `cours_graphique.py`, `figures.py`.
- **Figures des cours et des énoncés** : les pages fournies sont des photographies du manuel (ombres, pages courbées,
  textes pâles). Les figures des cours et des énoncés sont **redessinées en SVG** (`src/figures.py`, et les planches
  dans `src/activites.py`), pour être lisibles et, souvent, interactives.
- **Images de l'accueil et des pages d'activité** : ce sont **les figures du manuel**, et non plus des schémas
  redessinés. `outils/extraire_figures.py` les découpe dans les pages photographiées et les nettoie (division par
  l'éclairage de la photo : ombres et dégradés disparaissent, fond blanc ; niveaux ; couleurs ravivées) ; les figures
  découpées sont versionnées dans `src/images/originaux/`. `outils/preparer_images.py` en fait les vignettes des
  cartes (480 × 270, figure entière centrée sur fond blanc ; deux figures côte à côte pour A3) et le montage en tête de
  l'accueil (cabine d'ascenseur, roues dentées, frein à sabot, automobile). Correspondance : cours 1, le tremplin de
  l'ouverture du chapitre ; cours 2, le disque qui roule sans glisser (fig. 14) ; A1, le camion (fig. 11) ; A2, le
  palan en montée et en descente (fig. 16) ; A3, l'ascenseur et l'escalier (fig. 22 et 23) ; A4, les skieurs de
  l'ouverture du chapitre (les exercices 10 et 11 n'ont pas de figure) ; A5, l'amortisseur (fig. 26) ; A6, la même
  figure resserrée sur le ressort ; A7, fig. 27 ; A8, fig. 31 ; A9, fig. 33 ; A10, le frein à disque industriel à deux
  garnitures (fig. 18) ; G1 à G4, fig. 25, 34, 32 et 24. Les trois cartes sans figure d'origine (formulaire, atelier
  libre, étude à venir) gardent un dessin. **Les PDF fournis ne sont pas versionnés** (photographies d'un manuel,
  10 Mio) : `extraire_figures.py` les prend en arguments.
- **Mise en page** : le texte occupe **toute la largeur blanche** des sections, dans les cours comme dans les
  activités (énoncés, données, questions, corrections, consignes) : les limites de 72 à 80 caractères par ligne du
  gabarit sont levées par `generer.py` (le gabarit lui-même n'est pas modifié). Les encadrés de formules épousent
  leur contenu.
- **Numérotation** : « Activité A1… A10 » (approche analytique) et « Activité G1… G4 » (résolution graphique) ; la
  pastille donne le niveau. L'accueil a deux rubriques d'activités, plus une carte « Atelier de construction libre ».

## Un cours scindé en deux : approche analytique et résolution graphique

**Cours 1 — approche analytique** (`?ex=cours-analytique`, Niveau 1). Tout le texte du chapitre est repris, section
par section (objectifs dans l'en-tête ; introduction et tremplin ; I notions d'énergie et de puissance ; II travail
d'une force, d'un couple, ressorts de torsion ; III énergie potentielle ; IV énergie cinétique en translation, en
rotation, en mouvement plan ; V puissance ; VI rendement ; VII théorèmes). Treize figures sont redessinées (tremplin,
palan et réservoir, travail élémentaire, rampe, couple, ressort de torsion, énergie potentielle, volant, disque
roulant, puissance d'une force, palan en montée et en descente, rendement, frein à disque) ; les autres (trajectoires
des figures 3 et 5, ressort, voiture, camion, élément de masse en rotation) cèdent la place à un simulateur ou au
cours 2. Formules encadrées comme dans le manuel. Ajouts : simulateurs (lever la même charge plus ou moins vite, signe du travail selon
l'angle, travail et puissance d'un moteur, énergie cinétique d'un véhicule, volant d'inertie, rendement, tremplin où
l'énergie se conserve), huit cartes « L'essentiel », un jeu (quelle forme d'énergie ?) et un quiz de 10 questions.

**Cours 2 — résolution graphique** (`?ex=cours-graphique`, Niveau 2). Le chapitre pose les outils graphiques sans les
développer : le travail d'une force variable comme aire (figure du ressort), le produit scalaire par projection
(« F cos θ », travail du poids ne dépendant que de la dénivellation), les vitesses d'un solide en rotation et le
disque qui roule sans glisser (CIR au contact). Le cours 2 les rassemble en méthodes de construction et **ajoute ce dont
les activités graphiques ont besoin** : échelles, répartition linéaire et triangle des vitesses, équiprojectivité,
centre instantané de rotation, et le **principe des puissances virtuelles** (annoncé dans les objectifs du chapitre —
« principe du travail virtuel » — mais absent des pages fournies, qui s'arrêtent à la loi de conservation de
l'énergie, p. 250 : cette section est rédigée pour le site). Démonstrations interactives : aire sous la droite du
ressort, puissance par projection, triangle des vitesses, bielle-manivelle (équiprojectivité et CIR), disque roulant,
levier ; présentation de l'atelier et **planche libre** (bielle-manivelle, non notée, correction à afficher) ; quiz de
8 questions.

**Formulaire** (`?ex=formulaire-energetique`) : les fiches DT1 (formules et unités) et DT2 (méthodes graphiques et
outils de l'atelier), ouvertes aussi dans le panneau des activités.

## L'atelier de construction graphique

Les exercices de cinématique graphique demandent un environnement de construction : il est fait pour être cohérent
avec le gabarit (même barre d'outils, mêmes couleurs, mêmes modes, même notation, même impression).

- **Planche** : un dessin SVG coté en millimètres, à l'échelle, avec ses échelles affichées (longueurs, vitesses,
  efforts), ses points nommés et les vecteurs donnés.
- **Outils** : Point, Segment, Droite, Vecteur (sa valeur s'affiche à l'échelle des vitesses pendant le tracé), Compas,
  Report (une longueur, puis le centre), Perpendiculaire, Parallèle, Projeté, Mesurer (longueur convertie avec toutes
  les échelles), Nommer ; Gomme, Annuler, Rétablir, Tout effacer (en deux temps) ; zoom de 100 à 400 %, Déplacer,
  plein écran (Échap en sort). **Aimantation** aux points, extrémités, intersections (droites, segments, cercles) et
  lignes, avec un repère jaune : rien n'est tracé à main levée, une construction juste donne un résultat exact.
- **Notation** (même principe que les étiquettes du dépôt « Chaîne fonctionnelle ») : une question de construction
  est une question à plusieurs cases du gabarit (« fast-q »), aux cases masquées. La planche y écrit, à chaque tracé,
  ce qu'elle relève : norme d'un vecteur tracé depuis un point demandé (tolérance 4 %), sa direction (3°), écart entre
  un point nommé (I1, H…) et sa position attendue (2 mm). Le relevé est affiché sous la planche, sans dire s'il est
  juste. Le moteur du gabarit corrige ces cases comme les autres : entraînement (bouton « Valider la construction »),
  examen (rien avant la remise), note pondérée, récapitulatif. Une fois la question corrigée, la planche se verrouille
  et la **correction se superpose en rouge** (case à cocher pour la masquer) ; elle s'imprime avec la copie, jamais
  avant la remise.
- Les questions de calcul qui suivent une construction demandent les valeurs **lues** sur la planche (tolérance 4 %).

## Les activités : une par exercice, les plus courts réunis par deux

| Activité | Exercices du manuel | Rubrique, niveau | Parties | Questions | Points | Durée |
|---|---|---|---|---|---|---|
| A1 — QCM : travail et énergie cinétique | QCM 2, 3, 4 | analytique, 1 | 1 | 3 | 3 | 8 min |
| A2 — QCM : puissance d'une force, d'un couple | QCM 5, 6 | analytique, 1 | 1 | 2 | 2 | 6 min |
| A3 — Ascenseur et escalier roulant | 7 et 8 | analytique, 1 | 2 | 8 | 8 | 24 min |
| A4 — Remonte-pente et bateau | 10 et 11 | analytique, 1 | 2 | 9 | 9 | 25 min |
| A5 — Amortisseur de fin de course | 13 | analytique, 2 | 1 | 5 | 5 | 20 min |
| A6 — Wagon sur une pente de 2 % | 14 (imprimé « 13 », second du nom) | analytique, 2 | 1 | 5 | 5 | 18 min |
| A7 — Freinage dans une pente | 15 | analytique, 2 | 1 | 5 | 5 | 15 min |
| A8 — Vérin de levage | 22 (imprimé « 16 ») | analytique, 2 | 1 | 6 | 6 | 22 min |
| A9 — Frein à sabot | 24 | analytique, 2 | 1 | 8 | 8 | 22 min |
| A10 — Frein à deux sabots | 25 | analytique, 2 | 1 | 7 | 7 | 18 min |
| G1 — Skip de chargement | 12 | graphique, 1 | 2 | 6 | 8 | 26 min |
| G2 — Roues dentées | 26 | graphique, 2 | 2 | 9 | 12 | 35 min |
| G3 — Levage de balancier | 23 | graphique, 2 | 2 | 11 | 12 | 40 min |
| G4 — Tire-bouchon | 9 | graphique, 2 | 2 | 4 | 10 | 38 min |

- **Regroupements** (trois exercices au plus) : les QCM du manuel sont numérotés comme des exercices (2 à 6) ; ils
  forment deux activités, de trois et deux questions, par thème (énergie, puissance). Les exercices 7 et 8, puis 10 et
  11, les plus courts, sont réunis par deux, une partie chacun. Tous les autres ont leur propre activité.
- **Rubrique graphique** : les exercices où une vitesse ou une longueur se construit avant le bilan. Skip (12) :
  projections (composante verticale de la vitesse, dénivellation). Roues dentées (26) : répartition linéaire sur la
  roue A, même vitesse au contact, répartition sur la roue B. Balancier (23) : triangle des vitesses autour de A, puis
  effort de la tige par les puissances (<i>F</i>·<i>V</i><sub>B</sub> = <i>P</i>·<i>V</i><sub>G</sub>). Tire-bouchon (9) :
  centres instantanés de rotation de proche en proche (I1, I2, I3), puis principe des puissances virtuelles, comme le
  demande l'énoncé (« en utilisant le principe des travaux virtuels… montrer que T = 3F »).
- Chaque énoncé est découpé en questions intermédiaires notées (un point chacune), avec sa démarche corrigée
  (formule, application numérique, remarque). Toutes les valeurs attendues sont **recalculées** dans
  `src/activites.py` avec <i>g</i> = 9,81 m/s² ; tolérance de 2 % sur un calcul (une copie faite avec <i>g</i> = 10 passe),
  4 % sur une lecture graphique ; unités et multiples acceptés (W/kW, J/kJ, N/kN, m/mm, bar/MPa…), unité manquante
  ou fausse : demi-point.
- Documents : DT1 (formulaire) dans toutes les activités, DT2 (méthodes graphiques et atelier) dans les activités G.

## Corrections apportées au manuel et décisions — à vérifier par l'enseignant

**Cours**
- **Palan, puissance du poids (p. 248)** : le manuel écrit −5 000 W en montée et 5 000 W en descente ; avec
  <i>P</i> = 10 000 N et <i>V</i> = 0,1 m/s, on trouve **∓ 1 000 W**. Corrigé dans le cours.
- **Freinage du tambour (p. 250)** : « réalisé en 6 secondes pendant 3 tours » est incohérent (une décélération
  uniforme de 20 rad/s à l'arrêt en 6 s fait 9,5 tours) ; la durée n'intervient pas dans le calcul : elle est retirée.
  « 20 rad/s (≈ 200 tr/min) » devient « ≈ 190 tr/min ».
- **Puissance d'un torseur** : le texte du manuel est illisible sur la photographie ; il est rétabli sous sa forme
  usuelle (comoment, <i>P</i> = R·V<sub>A</sub> + M<sub>A</sub>·ω, indépendant du point choisi).
- Renvois à d'autres chapitres du manuel (« chapitre 13 », « voir chapitre moment d'inertie ») retirés ; figures
  renumérotées.

**Exercices**
- **QCM** : le corrigé n'est pas fourni ; réponses établies : 2 → a ; 3 → **b et c** (b est la même relation
  multipliée par 2) ; 4 → c ; 5 → **b et c** (P = F·V n'est juste que si force et vitesse sont colinéaires) ;
  6 → **a, b et c** (couple et vitesse angulaire portés par le même axe). Les propositions sont des cases à cocher et
  toutes les bonnes réponses sont exigées. La question 1 du QCM n'est pas dans les pages fournies.
- **Exercices 16 à 21** : page absente des documents fournis (la page « exo 2 » commence à l'exercice numéroté 16,
  qui est en fait le 22 : l'exercice 23 y renvoie). Deux exercices sont imprimés « 13 » : le second est le 14.
- **Remonte-pente (10)** : la réponse du manuel (1 110 kW) n'a pu être retrouvée avec les données. Décision : la
  « surcharge de 200 % » est explicitée dans l'énoncé (le moteur doit pouvoir fournir trois fois la puissance de
  service), d'où 137,3 kW utiles, 196,2 kW absorbés, **588,6 kW** à installer.
- **Skip (12)** : la réponse « P = −1,2 kW » mêle la puissance du poids (négative, −846 W) et celle du moteur
  (+1,21 kW avec η = 0,7) ; l'activité demande les deux, séparément.
- **Amortisseur (13)** : pas de réponse dans le manuel ; le rail descend vers l'amortisseur (figure), le poids
  travaille pendant la compression : <i>K</i> ≈ 130,2 kN/m, <i>F</i> ≈ 13,0 kN.
- **Wagon sur une pente de 2 % (14)** : la vitesse au contact (2,8 m/s) est juste, mais la course annoncée (0,178 m)
  est incompatible avec <i>K</i> = 10 000 kN/m et la masse de 300 kg (elle supposerait <i>K</i> ≈ 74 kN/m). L'énoncé est
  gardé ; la course juste est **15,3 mm** (effort de 153 kN), et la démarche souligne la raideur excessive. À
  confirmer : si la raideur voulue était différente, ne changer que la donnée dans `src/activites.py`.
- **Vérin (22)** : « l'effort F de décélération » est l'effort **supplémentaire** à celui qui retient la charge en
  descente uniforme (c'est ainsi que l'on retrouve 6 880 N et 235 bar) ; l'énoncé le précise.
- **Balancier (23)** : pas de réponse dans le manuel. Hypothèses écrites dans l'énoncé : les 5 000 daN sont le poids du
  balancier, appliqué en G à 2 m de A (milieu de la longueur de 4 m) ; masse <i>P</i>/<i>g</i> ; rotation petite pendant
  l'amortissement. Résultats : <i>J</i><sub>A</sub> ≈ 27 391 kg·m², <i>F</i> ≈ 30,8 kN, <i>p</i> ≈ 81,6 bar.
- **Frein à sabot (24)** : le moment du frottement par rapport à l'articulation A est négligé (c'est ainsi que l'on
  retrouve 443 N) ; l'énoncé le dit.
- **Frein à deux sabots (25)** : « la puissance de freinage au début du mouvement à 400 tr/min » est lue comme une
  vitesse initiale de 400 tr/min, l'arrêt restant en 50 tours : <i>F</i> ≈ 1 064 N par levier, 18,7 kW.
- **Tire-bouchon (9)** : la géométrie du pantographe est redessinée (barres à 45°, biellettes du collier parallèles aux
  barres, comme sur la figure) ; avec une vitesse virtuelle de D de 15 mm/s, la construction donne 45 mm/s à la
  poignée : <i>T</i> = 3·<i>F</i>, comme l'annonce le manuel ; l'activité fixe <i>F</i> = 120 N.
- Réponses du manuel retrouvées (et vérifiées par un test) : 10,48 kW et 218,46 kJ (7), 210 kN (11), 42,3 kJ (12),
  2,8 m/s (14), 205 m et 512,6 kJ (15), 6 880 N et 235 bar (22), 443 N (24), 16,3 tours et 50 N (26).

## Points signalés sans modification

- Le niveau des pastilles (Niveau 1 : QCM, A3, A4, G1 ; Niveau 2 : les autres) est une proposition.
- Poids de la page : `index.html` ≈ 1,4 Mio, dont 310 Kio d'images (17 JPEG : vignettes et montage d'accueil).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 6 tests — configuration (14 activités, 100 cases, une ou deux parties
  chacune), réponse de référence juste pour chaque case, valeur hors tolérance refusée, unité manquante ou fausse à
  demi-point, multiples d'unité acceptés, saisies d'élève typiques (« 10486 W », « 81,8 % », « 160 kg.m^2 »,
  « 235 bars »…), réponse du manuel incompatible refusée (0,178 m), QCM (seule la bonne combinaison de cases, parmi les
  7 possibles), relevés des planches (valeur attendue juste, hors tolérance faux), réponses du manuel retrouvées.
- `tests/navigateur.test.js` (Playwright, Chromium) : 13 parcours, tous réussis — accueil (rubriques, 19 cartes de même
  taille illustrées, mots-clés, téléphone, aucune mention de diplôme ou d'épreuve) ; adresse inconnue ; cours 1
  (simulateurs, signe du travail, exemples du manuel, tremplin, cartes, jeu, quiz 10/10) ; cours 2 (démonstrations,
  planche libre : tracer, annuler, rétablir, afficher la correction) ; formulaire ; activité en entraînement (20/20,
  demi-point d'unité) ; activité en examen (rien avant la remise, remise en deux temps, 15/20) ; QCM (20/20, réponse
  incomplète) ; **G1 construite au clic** (perpendiculaires, projetés, vecteur, nom, mesure : 3/3, planche verrouillée,
  correction superposée, 20/20) ; G4 (7/7, 20/20) ; outils de l'atelier (report, gomme, noms uniques, point mal placé
  refusé, zoom, plein écran) ; G2 et G3 en examen (correction et verrouillage à la remise, 20/20) ; téléphone.
- Aucune erreur JavaScript, aucun identifiant en double, dans aucune page.
