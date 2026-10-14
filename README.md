# Énergétique : cours et activités interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même issu du dépôt « Résistance des matériaux ») : une
page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages depuis
`index.html`. Le contenu vient du chapitre « Énergétique » fourni (cours et pages d'exercices). L'accueil mène à :

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées par les figures du manuel, à mots-clés : le cours, le formulaire, les activités (pastilles Niveau 1 / Niveau 2), les études de cas |
| `?ex=cours-energetique` | Cours — Énergétique : travail, énergies, puissance : énergie et puissance, travail d'une force et d'un couple, énergies potentielle et cinétique, puissance, rendement, théorèmes, principe du travail virtuel ; figures redessinées, simulateurs, cartes, jeu, quiz |
| `?ex=formulaire-energetique` | formulaire d'énergétique (le document DT1 des activités) |
| `?ex=qcm-travail-energie`, `?ex=qcm-puissance` | Activités 1.1 et 1.2 — QCM (Niveau 1) |
| `?ex=ascenseur-escalier`, `?ex=remonte-pente-bateau` | Activités 1.3 et 1.4 — deux exercices courts réunis, une partie chacun (Niveau 1) |
| `?ex=skip-chargement` | Activité 1.5 — skip de chargement (Niveau 1) |
| `?ex=tire-bouchon`, `?ex=amortisseur`, `?ex=wagon-pente`, `?ex=freinage-pente`, `?ex=verin-levage`, `?ex=balancier`, `?ex=frein-sabot`, `?ex=frein-deux-sabots`, `?ex=roues-dentees` | Activités 2.1 à 2.9 — un exercice chacune (Niveau 2) |

Chaque activité propose le mode entraînement ou le mode examen, avec sa note pondérée par la durée de ses parties.
Correspondance avec les exercices du manuel, corrections apportées et décisions :
[`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

**Ajouter une activité** : décrire ses parties dans `src/activites.py` (blocs `Q` pour une saisie, `QCM` pour des
propositions), puis l'ajouter à `ACTIVITES` avec `act(…)` (adresse, préfixe des cases, numéro « 1.x » ou « 2.x » qui
donne le niveau, titre, mots-clés, sous-titre) et sa vignette dans `outils/preparer_images.py` ; la carte apparaît
d'elle-même sur l'accueil. Une étude de cas : même chose avec `"etude": True` (elle remplace l'annonce « En cours
d'édition »).

## Régénérer les pages

Les pages sont produites par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui des dépôts RDM et « Chaîne fonctionnelle », recopié sans modification de son style ni de ses moteurs) et du
contenu décrit dans `src/`.

```sh
python3 outils/extraire_figures.py cours.pdf exercices.pdf exo2.pdf  # seulement pour redécouper les figures du manuel
python3 outils/preparer_images.py   # seulement si src/images/originaux change : vignettes et montage d'accueil
python3 src/generer.py              # écrit index.html
python3 outils/reponses.py          # seulement si les activités changent : réécrit tests/reponses.js
```

## Tester

```sh
node --test tests/correction.test.js                          # moteur de correction : 84 cases, unités, QCM
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, formulaire, entraînement, examen, QCM
```

`tests/reponses.js` contient une saisie juste pour chaque case ; les parcours navigateur vérifient qu'une copie
entièrement juste donne 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris des dépôts RDM et « Chaîne fonctionnelle » |
| `src/generer.py` | rendu des questions, accueil, éléments communs du cours, aiguillage et assemblage |
| `src/commun.py` | écriture des nombres et des calculs, unités et correcteurs numériques, blocs des parties |
| `src/activites.py` | les 14 activités (énoncés, valeurs recalculées, démarches), le formulaire DT1 |
| `src/cours_energetique.py` | le cours : texte du chapitre, figures, simulateurs, cartes, jeu, quiz |
| `src/figures.py` | figures redessinées en SVG : figures des énoncés, vignettes des cartes sans figure d'origine |
| `src/images/originaux/` | figures du manuel découpées dans les pages photographiées et nettoyées |
| `src/images/` | vignettes des cartes (`carte-*.jpg`) et montage de l'accueil (`accueil.jpg`), intégrés en data URI |
| `outils/extraire_figures.py` | découpe et nettoyage des figures du manuel (à partir des PDF fournis) |
| `outils/preparer_images.py` | vignettes des cartes et montage de l'accueil |
| `outils/reponses.py` | écrit `tests/reponses.js` à partir des activités |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
