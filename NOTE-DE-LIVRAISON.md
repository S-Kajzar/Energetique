# Note de livraison — Énergétique : cours et activités interactifs

## Construction reprise du dépôt « Chaîne fonctionnelle »

**Sources** : le chapitre « Énergétique » fourni en trois PDF de pages photographiées (cours : 10 pages ; exercices :
deux pages de QCM et d'exercices, plus une page d'exercices de dynamique). **Dépôt de référence, non modifié** :
« Chaîne fonctionnelle » (construction : générateur, gabarit, accueil, pastilles, cartes, cours, tests).

- **Gabarit** : `src/gabarit-exercice-interactif.html` est copié tel quel depuis le dépôt « Chaîne fonctionnelle »
  (fichier identique, vérifié octet par octet ; c'est lui-même la copie conforme du gabarit RDM). Comme dans ce dépôt,
  seules les entrées réservées au sujet du moteur applicatif sont remplacées, chaque remplacement étant vérifié :
  `CONSEIL_MIN` (lue dans `window.__CONSEIL_MIN__`), `DECOR` et `DR_NAMES` (vides : aucune activité n'a de document
  réponse à tracer), le texte de la fenêtre « Imprimer les DR », le libellé « Diagramme validé », devenu « Réponses
  validées ». Le correctif d'impression des tracés relevé dans le dépôt RDM est repris.
- **Générateur** (`src/generer.py`) : même organisation (rendu des questions, `prepare_exo`, parties pondérées par
  leur durée, documents dans le panneau latéral, aiguillage `?ex=…` exécuté avant les moteurs, accueil en cartes de
  même taille avec 3 à 5 mots-clés, pastilles Niveau 1 / Niveau 2, rubrique « Études de cas » annoncée « En cours
  d'édition »). Le contenu est réparti en modules : `commun.py`, `activites.py`, `cours_energetique.py`, `figures.py`.
- **Figures du cours et des énoncés** : les pages fournies sont des photographies du manuel (ombres, pages courbées,
  textes pâles). Les figures du cours et des énoncés sont **redessinées en SVG** (`src/figures.py`), pour être
  lisibles et, souvent, interactives.
- **Images de l'accueil et des pages d'activité** : ce sont **les figures du manuel**, et non des schémas redessinés.
  `outils/extraire_figures.py` les découpe dans les pages photographiées et les nettoie (division par l'éclairage de
  la photo : ombres et dégradés disparaissent, fond blanc ; niveaux ; couleurs ravivées) ; les figures découpées sont
  versionnées dans `src/images/originaux/`. `outils/preparer_images.py` en fait les vignettes des cartes (480 × 270,
  figure entière centrée sur fond blanc ; deux figures côte à côte pour l'activité 1.3) et le montage en tête de
  l'accueil (cabine d'ascenseur, roues dentées, frein à sabot, automobile). Correspondance : cours, le tremplin de
  l'ouverture du chapitre ; 1.1, le camion (fig. 11) ; 1.2, le palan en montée et en descente (fig. 16) ; 1.3,
  l'ascenseur et l'escalier (fig. 22 et 23) ; 1.4, les skieurs de l'ouverture du chapitre (les exercices 10 et 11
  n'ont pas de figure) ; 1.5, le wagonnet de levage (fig. 25) ; 2.1, le tire-bouchon (fig. 24) ; 2.2, l'amortisseur
  (fig. 26) ; 2.3, la même figure resserrée sur le ressort ; 2.4, fig. 27 ; 2.5, fig. 31 ; 2.6, fig. 32 ; 2.7,
  fig. 33 ; 2.8, le frein à disque industriel à deux garnitures (fig. 18) ; 2.9, fig. 34. Les deux cartes sans figure
  d'origine (formulaire, étude à venir) gardent un dessin. **Les PDF fournis ne sont pas versionnés** (photographies
  d'un manuel, 10 Mio) : `extraire_figures.py` les prend en arguments.
- **Mise en page** : le texte occupe **toute la largeur blanche** des sections, dans le cours comme dans les
  activités (énoncés, données, questions, corrections, consignes) : les limites de 72 à 80 caractères par ligne du
  gabarit sont levées par `generer.py` (le gabarit lui-même n'est pas modifié). Les encadrés de formules épousent
  leur contenu.
- **Numérotation** : « Activité 1.1… 1.5 » (Niveau 1) et « Activité 2.1… 2.9 » (Niveau 2) ; le premier chiffre est
  celui de la pastille. L'accueil a une seule rubrique d'activités.

## Pas de résolution graphique : un cours unique

L'énergétique se traite par le calcul : le site n'a **qu'un cours**, sans partie de résolution graphique ni atelier de
construction. Les quatre exercices d'abord traités par construction (9, 12, 23 et 26) sont des activités de calcul
comme les autres (voir plus bas). Le code de l'atelier de construction et du cours de résolution graphique reste
dans l'historique git (commit `4874c97`), s'il devait resservir dans un autre chapitre (cinématique graphique).

**Cours — Énergétique : travail, énergies, puissance** (`?ex=cours-energetique`). Tout le texte du chapitre est repris,
section par section (objectifs dans l'en-tête ; introduction et tremplin ; I notions d'énergie et de puissance ;
II travail d'une force, d'un couple, ressorts de torsion ; III énergie potentielle ; IV énergie cinétique en
translation, en rotation, en mouvement plan ; V puissance ; VI rendement ; VII théorèmes). Treize figures sont
redessinées (tremplin, palan et réservoir, travail élémentaire, rampe, couple, ressort de torsion, énergie
potentielle, volant, disque roulant, puissance d'une force, palan en montée et en descente, rendement, frein à
disque) ; les autres (trajectoires des figures 3 et 5, ressort, voiture, camion, élément de masse en rotation) cèdent
la place à un simulateur. Formules encadrées comme dans le manuel. Ajouts : neuf simulateurs (lever la même charge
plus ou moins vite, signe du travail selon l'angle, travail et puissance d'un moteur, **travail du ressort lu comme
l'aire sous la droite F(f)**, énergie cinétique d'un véhicule, volant d'inertie, rendement, tremplin où l'énergie se
conserve, levier), huit cartes « L'essentiel », un jeu (quelle forme d'énergie ?) et un quiz de 10 questions.

Le **principe du travail virtuel** est annoncé dans les objectifs du chapitre mais absent des pages fournies, qui
s'arrêtent à la loi de conservation de l'énergie (p. 250) : il est rédigé pour le site, à la fin de la section des
théorèmes (énoncé, formule encadrée, levier interactif : rapport des déplacements, rapport des efforts, égalité des
travaux), parce que l'exercice du tire-bouchon (activité 2.1) le demande.

**Formulaire** (`?ex=formulaire-energetique`) : la fiche DT1 (formules et unités, jusqu'au travail virtuel), ouverte
aussi dans le panneau de chaque activité.

## Les activités : une par exercice, les plus courts réunis par deux

| Activité | Exercices du manuel | Niveau | Parties | Questions | Points | Durée |
|---|---|---|---|---|---|---|
| 1.1 — QCM : travail et énergie cinétique | QCM 2, 3, 4 | 1 | 1 | 3 | 3 | 8 min |
| 1.2 — QCM : puissance d'une force, d'un couple | QCM 5, 6 | 1 | 1 | 2 | 2 | 6 min |
| 1.3 — Ascenseur et escalier roulant | 7 et 8 | 1 | 2 | 8 | 8 | 24 min |
| 1.4 — Remonte-pente et bateau | 10 et 11 | 1 | 2 | 9 | 9 | 25 min |
| 1.5 — Skip de chargement | 12 | 1 | 1 | 5 | 5 | 18 min |
| 2.1 — Tire-bouchon | 9 | 2 | 1 | 4 | 4 | 15 min |
| 2.2 — Amortisseur de fin de course | 13 | 2 | 1 | 5 | 5 | 20 min |
| 2.3 — Wagon sur une pente de 2 % | 14 (imprimé « 13 », second du nom) | 2 | 1 | 5 | 5 | 18 min |
| 2.4 — Freinage dans une pente | 15 | 2 | 1 | 5 | 5 | 15 min |
| 2.5 — Vérin de levage | 22 (imprimé « 16 ») | 2 | 1 | 6 | 6 | 22 min |
| 2.6 — Levage de balancier | 23 | 2 | 2 | 10 | 10 | 37 min |
| 2.7 — Frein à sabot | 24 | 2 | 1 | 8 | 8 | 22 min |
| 2.8 — Frein à deux sabots | 25 | 2 | 1 | 7 | 7 | 18 min |
| 2.9 — Roues dentées | 26 | 2 | 1 | 7 | 7 | 25 min |

- **Regroupements** (trois exercices au plus) : les QCM du manuel sont numérotés comme des exercices (2 à 6) ; ils
  forment deux activités, de trois et deux questions, par thème (énergie, puissance). Les exercices 7 et 8, puis 10 et
  11, les plus courts, sont réunis par deux, une partie chacun. Tous les autres ont leur propre activité.
- **Les quatre exercices autrefois construits, désormais calculés** : skip (12) — dénivellation par le sinus de
  l'inclinaison, énergie de levage, composante verticale de la vitesse, puissance du poids (négative), puissance du
  moteur ; tire-bouchon (9) — déplacements virtuels tirés de la géométrie du pantographe, puis principe du travail
  virtuel ; balancier (23) — vitesses d'un solide en rotation autour de A (ω = V<sub>B</sub>/AB, V<sub>G</sub> = ω·AG),
  effort de retenue par l'égalité des puissances, puis amortissement ; roues dentées (26) — même vitesse au contact
  des cercles primitifs (r<sub>A</sub>·ω<sub>A</sub> = r<sub>B</sub>·ω<sub>B</sub>), puis théorème de l'énergie
  cinétique.
- Chaque énoncé est découpé en questions intermédiaires notées (un point chacune), avec sa démarche corrigée
  (formule, application numérique, remarque). Toutes les valeurs attendues sont **recalculées** dans
  `src/activites.py` avec <i>g</i> = 9,81 m/s² ; tolérance de 2 % (une copie faite avec <i>g</i> = 10 passe) ; unités
  et multiples acceptés (W/kW, J/kJ, N/kN, m/mm, bar/MPa…), unité manquante ou fausse : demi-point.
- Document : DT1 (formulaire) dans toutes les activités.

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
  balancier, appliqué en G à 2 m de A (milieu de la longueur de 4 m) ; masse <i>P</i>/<i>g</i> ; balancier horizontal à
  l'instant étudié ; rotation petite pendant l'amortissement. Résultats : ω = 0,3 rad/s, <i>V</i><sub>G</sub> =
  0,6 m/s, <i>F</i><sub>s</sub> = 100 kN, <i>J</i><sub>A</sub> ≈ 27 391 kg·m², <i>F</i> ≈ 30,8 kN, <i>p</i> ≈ 81,6 bar.
- **Frein à sabot (24)** : le moment du frottement par rapport à l'articulation A est négligé (c'est ainsi que l'on
  retrouve 443 N) ; l'énoncé le dit.
- **Frein à deux sabots (25)** : « la puissance de freinage au début du mouvement à 400 tr/min » est lue comme une
  vitesse initiale de 400 tr/min, l'arrêt restant en 50 tours : <i>F</i> ≈ 1 064 N par levier, 18,7 kW.
- **Tire-bouchon (9)** : la géométrie du pantographe, illisible sur la photographie, est donnée dans l'énoncé (barres
  identiques articulées en leur milieu et à leurs extrémités, toutes au même angle φ avec l'axe ; biellettes du
  collier concourantes en un point fixe O) : <i>x</i><sub>D</sub> = 2·<i>a</i>·cos φ et <i>x</i><sub>H</sub> =
  6·<i>a</i>·cos φ, d'où un rapport des déplacements virtuels de 3 et <i>T</i> = 3·<i>F</i>, comme l'annonce le
  manuel. L'activité fixe <i>F</i> = 120 N et ajoute la course de la poignée (90 mm pour 30 mm de bouchon) et le
  travail fourni (10,8 J).
- Réponses du manuel retrouvées (et vérifiées par un test) : 10,48 kW et 218,46 kJ (7), 210 kN (11), 42,3 kJ et
  1,2 kW (12), 2,8 m/s (14), 205 m et 512,6 kJ (15), 6 880 N et 235 bar (22), 443 N (24), 16,3 tours et 50 N (26),
  <i>T</i> = 3·<i>F</i> (9).

## Points signalés sans modification

- Le niveau des pastilles (Niveau 1 : les QCM, 1.3, 1.4 et 1.5 ; Niveau 2 : les autres) est une proposition.
- Poids de la page : `index.html` ≈ 1,2 Mio, dont 295 Kio d'images (16 JPEG : vignettes et montage d'accueil).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 5 tests — configuration (14 activités, 84 cases, une ou deux parties
  chacune), réponse de référence juste pour chaque case, valeur hors tolérance refusée, unité manquante ou fausse à
  demi-point, multiples d'unité acceptés, saisies d'élève typiques (« 10486 W », « 81,8 % », « 160 kg.m^2 »,
  « 235 bars », « 16,3 tours »…), réponse du manuel incompatible refusée (0,178 m), signe exigé (travail du ressort,
  puissance du poids), QCM (seule la bonne combinaison de cases, parmi les 7 possibles), réponses du manuel retrouvées.
- `tests/navigateur.test.js` (Playwright, Chromium) : 10 parcours, tous réussis — accueil (quatre rubriques,
  17 cartes de même taille illustrées, mots-clés, aucune mention de résolution graphique ni de diplôme ou d'épreuve, téléphone) ; adresse
  inconnue ; cours (dix sections, simulateurs, signe du travail, aire du ressort, travail virtuel, tremplin, cartes,
  jeu, quiz 10/10) ; formulaire ; activité 1.3 en entraînement (20/20, demi-point d'unité) ; activité 2.7 en examen
  (rien avant la remise, remise en deux temps, 15/20) ; QCM 1.1 et 1.2 (20/20) ; 1.5 et 2.1 en entraînement (20/20) ;
  2.6 et 2.9 en examen (20/20) ; téléphone.
- Aucune erreur JavaScript, aucun identifiant en double, dans aucune page.
