# Énergétique : cours et activités interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même issu du dépôt « Résistance des matériaux ») : une
page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages depuis
`index.html`. Le contenu vient du chapitre « Énergétique » fourni (cours et pages d'exercices), scindé en une
**approche analytique** et une **résolution graphique**. L'accueil mène à :

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées à mots-clés : les cours (pastilles Niveau 1 / Niveau 2), le formulaire, les activités en deux rubriques (approche analytique, résolution graphique), l'atelier libre, les études de cas |
| `?ex=cours-analytique` | Cours 1 — Énergétique : approche analytique (Niveau 1) : énergie et puissance, travail d'une force et d'un couple, énergies potentielle et cinétique, puissance, rendement, théorèmes ; figures redessinées, simulateurs, cartes, jeu, quiz |
| `?ex=cours-graphique` | Cours 2 — Énergétique : résolution graphique (Niveau 2) : échelles, travail = aire, produit scalaire par projection, répartition linéaire des vitesses, équiprojectivité, CIR, puissances virtuelles, atelier de construction et planche libre, quiz |
| `?ex=formulaire-energetique` | formulaire d'énergétique et fiche des méthodes graphiques (les documents DT1 et DT2 des activités) |
| `?ex=qcm-travail-energie`, `?ex=qcm-puissance` | Activités A1 et A2 — QCM (Niveau 1) |
| `?ex=ascenseur-escalier`, `?ex=remonte-pente-bateau` | Activités A3 et A4 — deux exercices courts réunis, une partie chacun (Niveau 1) |
| `?ex=amortisseur`, `?ex=wagon-pente`, `?ex=freinage-pente`, `?ex=verin-levage`, `?ex=frein-sabot`, `?ex=frein-deux-sabots` | Activités A5 à A10 — un exercice chacune (Niveau 2) |
| `?ex=skip-chargement` | Activité G1 — projections sur planche, puis énergie et puissance (Niveau 1) |
| `?ex=roues-dentees`, `?ex=balancier`, `?ex=tire-bouchon` | Activités G2 à G4 — vitesses construites (répartition linéaire, triangle des vitesses, CIR), puis bilan énergétique (Niveau 2) |

Chaque activité propose le mode entraînement ou le mode examen, avec sa note pondérée par la durée de ses parties.
Correspondance avec les exercices du manuel, corrections apportées et décisions :
[`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

## L'atelier de construction

Les activités de résolution graphique se font sur des **planches** à l'échelle (`src/construction.py`) : outils
point, segment, droite, vecteur, compas, report de longueur, perpendiculaire, parallèle, projeté, mesure à l'échelle,
nom d'un point ; aimantation aux points, extrémités, intersections et lignes ; annuler, rétablir, gomme, zoom, plein
écran. Une question de construction est une question à plusieurs cases du gabarit, dont les cases sont masquées : la
planche y écrit ce qu'elle relève sur le tracé (norme et direction d'un vecteur, écart d'un point nommé à sa position
attendue) et le moteur du gabarit les corrige comme les autres cases. La correction se superpose ensuite en rouge.

**Ajouter une activité** : décrire ses parties dans `src/activites.py` (blocs `Q` pour une saisie, `QCM` pour des
propositions, `CG` pour une construction sur une planche décrite par `construction.planche(…)`), puis l'ajouter à
`ACTIVITES` avec sa rubrique (`"analytique"` ou `"graphique"`) ; la carte apparaît d'elle-même sur l'accueil. Une
étude de cas : même chose avec `"etude": True` (elle remplace l'annonce « En cours d'édition »).

## Régénérer les pages

Les pages sont produites par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui des dépôts RDM et « Chaîne fonctionnelle », recopié sans modification de son style ni de ses moteurs) et du
contenu décrit dans `src/`.

```sh
python3 src/generer.py       # écrit index.html
python3 outils/reponses.py   # seulement si les activités changent : réécrit tests/reponses.js
```

## Tester

```sh
node --test tests/correction.test.js                          # moteur de correction : 100 cases, unités, QCM, relevés des planches
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, entraînement, examen, QCM, constructions au clic
```

`tests/reponses.js` contient une saisie juste pour chaque case et la construction juste de chaque planche ; les
parcours navigateur vérifient qu'une copie entièrement juste donne 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris des dépôts RDM et « Chaîne fonctionnelle » |
| `src/generer.py` | rendu des questions, accueil, éléments communs des cours, aiguillage et assemblage |
| `src/commun.py` | écriture des nombres et des calculs, unités et correcteurs numériques, blocs des parties |
| `src/activites.py` | les 14 activités (énoncés, valeurs recalculées, démarches), les planches de G1 à G4, les documents DT1 et DT2 |
| `src/construction.py` | atelier de construction : dessin des planches en millimètres, moteur JavaScript des outils, style |
| `src/cours_analytique.py` | cours 1 : texte du chapitre, figures, simulateurs, quiz |
| `src/cours_graphique.py` | cours 2 : méthodes graphiques, démonstrations interactives, planche libre, quiz |
| `src/figures.py` | figures redessinées en SVG : illustration de l'accueil, vignettes des cartes, figures des énoncés |
| `outils/reponses.py` | écrit `tests/reponses.js` à partir des activités |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
