# -*- coding: utf-8 -*-
"""Activités tirées des exercices du chapitre « Énergétique » (pages d'exercices fournies, numéros du manuel dans
NOTE-DE-LIVRAISON.md). Une activité par exercice ; les plus courts sont réunis par deux (une partie chacun).

Deux rubriques :
  - approche analytique : QCM et exercices de calcul (activités A1 à A10) ;
  - résolution graphique : les exercices où une vitesse (ou une longueur) se construit à l'échelle avant le bilan
    énergétique (activités G1 à G4), sur les planches de l'atelier de construction (src/construction.py).

Toutes les valeurs attendues sont recalculées ici (g = 9,81 m/s²), avec les mêmes formules que les démarches."""
import math

import construction as cg
import figures as fg
from commun import CG, G, HTML, Q, QBAR, QCM, donnees, eq, fr, frac, num, sig, vec

PI = math.pi
H_NUM = "Saisis la valeur <strong>avec son unité</strong> (elle vaut la moitié du point) ; tolérance de 2 %."
H_LU = "Valeur lue sur ta construction, <strong>avec son unité</strong> ; tolérance de 4 % (précision du tracé)."
H_SANS = "Nombre sans unité ; tolérance de 2 %."


def tr_min(N):
    return N * PI / 30


# ============================================================ documents (panneau latéral)
FORMULAIRE_HTML = f"""<div class="doc-text">
<h3>Travail</h3>
<table class="t"><tbody>
<tr><td>Force constante, déplacement rectiligne <i>AB</i></td><td><i>W</i> = {vec('F')}·{vec('AB')} = <i>F</i>·<i>AB</i>·cos θ</td><td><i>W</i> en J ; <i>F</i> en N ; <i>AB</i> en m</td></tr>
<tr><td>Poids, dénivellation <i>h</i></td><td><i>W</i> = ± <i>P</i>·<i>h</i> = ± <i>m</i>·<i>g</i>·<i>h</i></td><td>+ en descente (moteur), − en montée (résistant)</td></tr>
<tr><td>Couple constant, rotation d'angle θ</td><td><i>W</i> = <i>C</i>·θ</td><td><i>C</i> en N·m ; θ en rad (1 tour = 2π rad)</td></tr>
<tr><td>Ressort de traction-compression</td><td><i>W</i> = {frac('<i>k</i>', '2')}·(<i>f</i><sub>2</sub>² − <i>f</i><sub>1</sub>²)</td><td><i>k</i> en N/m ; <i>f</i> flèche en m</td></tr>
<tr><td>Ressort de torsion</td><td><i>C</i> = <i>k</i>·α ; <i>W</i> = {frac('1', '2')}·<i>k</i>·α²</td><td><i>k</i> en N·m/rad ; α en rad</td></tr>
</tbody></table>
<h3>Énergies</h3>
<table class="t"><tbody>
<tr><td>Potentielle de pesanteur</td><td><i>E</i><sub>p</sub> = <i>m</i>·<i>g</i>·<i>z</i></td><td><i>z</i> altitude en m ; <i>g</i> = 9,81 m/s²</td></tr>
<tr><td>Potentielle élastique</td><td><i>E</i><sub>p</sub> = {frac('1', '2')}·<i>k</i>·<i>f</i>²</td><td><i>f</i> déformation du ressort</td></tr>
<tr><td>Cinétique, translation</td><td><i>E</i><sub>c</sub> = {frac('1', '2')}·<i>m</i>·<i>V</i>²</td><td><i>V</i> en m/s</td></tr>
<tr><td>Cinétique, rotation d'axe fixe</td><td><i>E</i><sub>c</sub> = {frac('1', '2')}·<i>J</i>·ω²</td><td><i>J</i> en kg·m² ; ω en rad/s</td></tr>
<tr><td>Cinétique, mouvement plan</td><td><i>E</i><sub>c</sub> = {frac('1', '2')}·<i>m</i>·<i>V</i><sub>G</sub>² + {frac('1', '2')}·<i>J</i><sub>G</sub>·ω²</td><td><i>V</i><sub>G</sub> vitesse du centre de gravité</td></tr>
</tbody></table>
<h3>Moments d'inertie usuels</h3>
<table class="t"><tbody>
<tr><td>Rayon de giration <i>k</i></td><td><i>J</i> = <i>m</i>·<i>k</i>²</td><td></td></tr>
<tr><td>Cylindre plein (disque, volant) de rayon <i>R</i></td><td><i>J</i> = <i>m</i>·<i>R</i>²/2</td><td>axe de révolution</td></tr>
<tr><td>Parallélépipède <i>a</i> × <i>b</i> × <i>c</i></td><td><i>J</i><sub>G</sub> = <i>m</i>·(<i>a</i>² + <i>b</i>²)/12</td><td>axe passant par <i>G</i>, parallèle à <i>c</i></td></tr>
<tr><td>Théorème de Huygens</td><td><i>J</i><sub>A</sub> = <i>J</i><sub>G</sub> + <i>m</i>·<i>AG</i>²</td><td>axes parallèles, distants de <i>AG</i></td></tr>
</tbody></table>
<h3>Puissance et rendement</h3>
<table class="t"><tbody>
<tr><td>Puissance moyenne</td><td><i>P</i><sub>m</sub> = Δ<i>W</i> / Δ<i>t</i></td><td>W (watt) = J/s ; 1 cv = 736 W</td></tr>
<tr><td>Force</td><td><i>P</i> = {vec('F')}·{vec('V')} = <i>F</i>·<i>V</i>·cos θ</td><td>&gt; 0 motrice ; &lt; 0 résistante</td></tr>
<tr><td>Couple</td><td><i>P</i> = <i>C</i>·ω</td><td>ω = π·<i>N</i>/30 (<i>N</i> en tr/min)</td></tr>
<tr><td>Rendement</td><td>η = <i>W</i><sub>restituée</sub> / <i>W</i><sub>fournie</sub> = <i>P</i><sub>utile</sub> / <i>P</i><sub>absorbée</sub> ≤ 1</td><td>sans unité</td></tr>
</tbody></table>
<h3>Théorèmes</h3>
<table class="t"><tbody>
<tr><td>Énergie cinétique (solide isolé)</td><td><i>E</i><sub>c2</sub> − <i>E</i><sub>c1</sub> = Σ <i>W</i>(<i>F</i><sub>ext</sub>)<sub>1→2</sub></td><td>travaux des actions extérieures</td></tr>
<tr><td>Énergie-puissance</td><td>d<i>E</i><sub>c</sub>/d<i>t</i> = Σ <i>P</i>(<i>F</i><sub>ext</sub>)</td><td>ensemble de solides : ajouter les actions mutuelles</td></tr>
<tr><td>Conservation de l'énergie</td><td><i>E</i><sub>c1</sub> + <i>E</i><sub>p1</sub> = <i>E</i><sub>c2</sub> + <i>E</i><sub>p2</sub></td><td>système isolé, sans frottement</td></tr>
<tr><td>Puissances virtuelles (équilibre, liaisons parfaites)</td><td>Σ <i>P</i> = 0 pour tout mouvement possible</td><td><i>F</i><sub>e</sub>·<i>V</i><sub>e</sub> = <i>F</i><sub>s</sub>·<i>V</i><sub>s</sub></td></tr>
</tbody></table>
<h3>Frottement</h3>
<p>Effort tangentiel <i>T</i> = <i>f</i>·<i>N</i> (<i>f</i> = μ coefficient de frottement, <i>N</i> effort presseur).</p>
</div>"""

METHODES_HTML = f"""<div class="doc-text">
<h3>Échelles</h3>
<p>Une planche est dessinée à l'échelle : « 1 mm ↔ 0,1 m » veut dire qu'un millimètre de la planche représente
0,1 m de la réalité. Chaque grandeur vectorielle a son échelle (longueurs, vitesses, efforts). L'outil
<b>Mesurer</b> convertit une longueur tracée avec toutes les échelles de la planche ; un vecteur tracé affiche
directement sa valeur à l'échelle des vitesses.</p>
<h3>Projeter un vecteur (produit scalaire)</h3>
<p>{vec('F')}·{vec('V')} = <i>F</i>·<i>V</i>·cos θ = <i>F</i> × (projection de {vec('V')} sur la direction de {vec('F')}).
Construction : tracer la droite qui porte {vec('F')}, puis le <b>projeté</b> de l'extrémité de {vec('V')} sur cette droite.
Le travail du poids ne dépend que de la dénivellation <i>h</i>, projection verticale du déplacement.</p>
<h3>Solide en rotation autour d'un axe fixe O : répartition linéaire</h3>
<p>Chaque point M a une vitesse perpendiculaire à OM, de norme <i>V</i><sub>M</sub> = ω·OM : les extrémités des
vecteurs vitesses des points d'un même rayon sont alignées avec O (<b>triangle des vitesses</b>). Pour un point M
qui n'est pas sur le rayon du vecteur connu, on le ramène sur ce rayon au compas (cercle de centre O passant par
M), on lit la norme dans le triangle, puis on la reporte en M, perpendiculairement à OM.</p>
<h3>Équiprojectivité</h3>
<p>Pour deux points A et B d'un même solide, les vitesses ont la même projection sur la droite (AB) :
{vec('V')}<sub>A</sub>·{vec('AB')} = {vec('V')}<sub>B</sub>·{vec('AB')}. Si la direction de {vec('V')}<sub>B</sub> est connue :
projeter l'extrémité de {vec('V')}<sub>A</sub> sur (AB), reporter cette projection à partir de B (outil Report), tracer
la perpendiculaire à (AB) en ce point : elle coupe la direction de {vec('V')}<sub>B</sub> à l'extrémité de {vec('V')}<sub>B</sub>.</p>
<h3>Centre instantané de rotation (CIR)</h3>
<p>À un instant donné, un solide en mouvement plan tourne autour de son CIR I : chaque vitesse est perpendiculaire
à IM et proportionnelle à IM. I est à l'intersection des perpendiculaires aux directions de deux vitesses. Une
roue qui roule sans glisser a son CIR au point de contact.</p>
<h3>Roulement sans glissement, engrenages</h3>
<p>Au point de contact I de deux roues (ou des cercles primitifs de deux roues dentées), les deux roues ont la même
vitesse : ω<sub>A</sub>·<i>r</i><sub>A</sub> = ω<sub>B</sub>·<i>r</i><sub>B</sub>.</p>
<h3>Puissances virtuelles</h3>
<p>Un mécanisme en équilibre, à liaisons parfaites : pour tout mouvement possible (réel ou virtuel), la somme des
puissances des efforts extérieurs est nulle. Avec un effort d'entrée et un effort de sortie :
<i>F</i><sub>e</sub>·<i>V</i><sub>e</sub> = <i>F</i><sub>s</sub>·<i>V</i><sub>s</sub>, soit
<i>F</i><sub>s</sub> / <i>F</i><sub>e</sub> = <i>V</i><sub>e</sub> / <i>V</i><sub>s</sub> : le rapport des efforts est l'inverse du rapport des
vitesses, que l'on construit graphiquement.</p>
<h3>Outils de l'atelier</h3>
<ul><li><b>Point</b>, <b>Segment</b>, <b>Droite</b>, <b>Vecteur</b> (origine puis extrémité), <b>Compas</b> (centre puis point),
<b>Report</b> (longueur à reporter, puis centre).</li>
<li><b>Perpendiculaire</b> et <b>Parallèle</b> : la ligne de référence, puis le point de passage ; <b>Projeté</b> : le point, puis la ligne.</li>
<li><b>Aimantation</b> : un clic près d'un point, d'une extrémité, d'une intersection ou d'une ligne s'y accroche (repère jaune).</li>
<li><b>Nommer</b> un point placé (I1, H…) : la planche relève les points par leur nom.</li>
<li><b>Gomme</b>, <b>Annuler</b>, <b>Rétablir</b> ; <b>zoom</b> et <b>plein écran</b> pour les constructions fines.</li></ul>
</div>"""

DOCS = [
    ("DT1", "Formulaire d'énergétique", "Dossier technique", True, FORMULAIRE_HTML),
    ("DT2", "Méthodes graphiques et atelier", "Dossier technique", True, METHODES_HTML),
]


def page_formulaire(A):
    """Page « Formulaire d'énergétique » (?ex=formulaire-energetique) : les deux documents, en pleine page."""
    return (A.course_head("Formulaire", "", "Formulaire d'énergétique",
                          "Les formules du cours, avec leurs unités, et les méthodes de résolution graphique. Les mêmes "
                          "fiches s'ouvrent dans les activités (documents DT1 et DT2).") +
            '<div class="cours">' +
            A.course_nav([("f-formules", "Formules"), ("f-methodes", "Méthodes graphiques")]) +
            A.course_section(1, "f-formules", "Formules et unités", FORMULAIRE_HTML) +
            A.course_section(2, "f-methodes", "Méthodes graphiques et atelier de construction", METHODES_HTML) +
            '<div class="cours-foot"><a class="btn" href="?ex=cours-analytique">Cours 1 : approche analytique</a>'
            '<a class="btn" href="?ex=cours-graphique">Cours 2 : résolution graphique</a>'
            '<a class="btn ghost" href="?">Retour à l\'accueil</a></div></div>')


# ============================================================ consignes
CONSIGNES_QCM = """<p class="only-training"><strong>Mode entraînement.</strong> Coche ta ou tes réponses puis clique sur « Valider » : une réponse validée est définitive, sa correction et son explication s'affichent aussitôt.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Réponds à tout le questionnaire sans correction ni note : tes choix restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections et la note.</p>
    <p><strong>Une ou plusieurs réponses.</strong> Chaque question peut avoir plusieurs propositions justes : il faut les cocher toutes, et seulement elles, pour obtenir le point.</p>
    <p>Le formulaire (DT1) s'ouvre avec l'onglet sur le bord droit.</p>"""

CONSIGNES_CALCUL = """<p class="only-training"><strong>Mode entraînement.</strong> Réponds dans chaque champ puis clique sur « Valider » : une réponse validée est définitive et sa démarche corrigée s'affiche aussitôt.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Compose tout le sujet sans correction ni note : tes réponses restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections, les notes par partie et la note globale.</p>
    <p><strong>Les unités sont notées.</strong> Saisis la valeur et son unité (par exemple <span class="calc">10,5 kW</span> ou <span class="calc">10 500 W</span>) : une valeur juste sans unité, ou avec une unité fausse, ne rapporte qu'un demi-point. Tolérance : 2 % (calculs faits avec g = 9,81 m/s²).</p>
    <p>Le formulaire (DT1) s'ouvre avec l'onglet sur le bord droit, ou avec les boutons des en-têtes de question.</p>
    <p><strong>Barème pondéré par la durée conseillée</strong> : chaque partie est notée sur 20, puis pèse au prorata de son temps.</p>"""

CONSIGNES_GRAPHIQUE = """<p class="only-training"><strong>Mode entraînement.</strong> Construis sur la planche, puis clique sur « Valider la construction » : la planche se verrouille et la correction se superpose en rouge à ton tracé. Les questions de calcul se valident une à une.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Construis et réponds sans correction : tout reste modifiable jusqu'au bouton « J'ai fini, je fais corriger ma copie », qui verrouille les planches et dévoile les corrections.</p>
    <p><strong>L'atelier de construction.</strong> Les outils de la barre tracent des points, droites, perpendiculaires, parallèles, projetés, cercles et vecteurs ; tout s'aimante aux points, aux intersections et aux lignes (repère jaune). Un vecteur tracé affiche sa valeur à l'échelle des vitesses ; l'outil Mesurer convertit une longueur avec les échelles de la planche. Annuler, Gomme, zoom et plein écran aident aux constructions fines. Méthodes : document DT2.</p>
    <p><strong>Ce qui est noté sur la planche</strong> est indiqué sous elle (« relevé de ta construction ») : la norme et la direction des vecteurs tracés depuis les points demandés, la position des points que tu nommes (outil Nommer). Chaque relevé vaut un point ; tolérance de 4 % sur une norme, de 3° sur une direction, de 2 mm sur un point.</p>
    <p><strong>Les unités sont notées</strong> dans les questions de calcul : une valeur juste sans unité ne rapporte qu'un demi-point.</p>
    <p><strong>Barème pondéré par la durée conseillée</strong> : chaque partie est notée sur 20, puis pèse au prorata de son temps.</p>"""


def partie(title, minutes, intro, blocks):
    return {"title": title, "minutes": minutes, "intro": intro, "blocks": blocks}


def fig(f, caption, alt, maxw=520):
    return fg.figure(f(), caption, alt, maxw)


def lot(*items):
    return " ; ".join(items)


# ============================================================ A1, A2 — QCM
A1 = [partie("Travail d'un couple, énergie cinétique", 8, [
    "<p>Coche la ou les propositions justes. Notations : <i>C</i> couple (N·m), θ angle (rad), <i>W</i> travail (J), "
    "<i>m</i> masse (kg), <i>V</i> vitesse (m/s), <i>J</i> moment d'inertie (kg·m²), ω vitesse angulaire (rad/s).</p>"], [
    QCM("Le travail d'un couple constant <i>C</i> qui se déplace de l'angle θ<sub>1</sub> à l'angle θ<sub>2</sub> est :",
        ["<i>W</i> = <i>C</i> · (θ<sub>2</sub> − θ<sub>1</sub>)", "<i>W</i> = <i>C</i> · (θ<sub>1</sub> − θ<sub>2</sub>)",
         f"<i>W</i> = {vec('C')} · (θ<sub>2</sub> − θ<sub>1</sub>)"], "a",
        "<p>Le travail d'un couple constant est le produit du couple par l'angle balayé : <i>W</i> = <i>C</i>·Δθ, avec "
        "Δθ = θ<sub>2</sub> − θ<sub>1</sub> (positif quand le couple tourne dans le sens du mouvement : il est moteur). La "
        "proposition b donne le signe opposé ; la proposition c multiplie un vecteur par un nombre : le résultat serait un "
        "vecteur, pas une énergie.</p>"),
    QCM("L'énergie cinétique d'un solide de masse <i>m</i> en translation rectiligne à la vitesse <i>V</i> est :",
        ["<i>E</i><sub>c</sub> = <i>T</i> = ½ <i>m</i> <i>V</i>", "2 <i>E</i><sub>c</sub> = 2 <i>T</i> = <i>m</i> <i>V</i>²",
         "<i>E</i><sub>c</sub> = <i>T</i> = ½ <i>m</i> <i>V</i>²"], "bc",
        "<p><i>E</i><sub>c</sub> = ½·<i>m</i>·<i>V</i>² (c) ; la proposition b est la même relation multipliée par 2 : elle "
        "est juste aussi. La proposition a oublie le carré de la vitesse : elle n'est pas homogène à une énergie "
        "(kg·m/s au lieu de kg·m²/s², c'est-à-dire J).</p>"),
    QCM("L'énergie cinétique d'un solide de masse <i>m</i> en rotation autour d'un axe fixe, à la vitesse angulaire ω, "
        "de moment d'inertie <i>J</i> par rapport à cet axe, est :",
        ["<i>E</i><sub>c</sub> = <i>T</i> = ½ <i>m</i> <i>J</i> ω", "<i>E</i><sub>c</sub> = <i>T</i> = ½ <i>m</i> ω²",
         "<i>E</i><sub>c</sub> = <i>T</i> = ½ <i>J</i> ω²"], "c",
        "<p>En rotation, le moment d'inertie <i>J</i> joue le rôle de la masse et la vitesse angulaire ω celui de la "
        "vitesse : <i>E</i><sub>c</sub> = ½·<i>J</i>·ω². Les propositions a et b ne sont pas homogènes à une énergie.</p>"),
])]

A2 = [partie("Puissance d'une force, puissance d'un couple", 6, [
    "<p>Coche la ou les propositions justes.</p>"], [
    QCM(f"La puissance <i>P</i> (en W) développée par une force {vec('F')} (en N) dont le point d'application se déplace "
        f"à la vitesse {vec('V')} (en m/s) est :",
        ["<i>P</i> = <i>F</i> · <i>V</i>", f"<i>P</i> = {vec('F')} · {vec('V')}", f"<i>P</i> = {vec('V')} · {vec('F')}"],
        "bc",
        f"<p>La puissance est le produit scalaire de la force par la vitesse : <i>P</i> = {vec('F')}·{vec('V')} = "
        "<i>F</i>·<i>V</i>·cos θ, et le produit scalaire est commutatif (b et c). <i>P</i> = <i>F</i>·<i>V</i> (produit "
        "des normes) n'est juste que si la force et la vitesse ont la même direction et le même sens (θ = 0) : ce n'est "
        "pas la définition générale.</p>"),
    QCM("La puissance <i>P</i> (en W) développée par un couple <i>C</i> (en N·m) tournant à la vitesse angulaire ω (en "
        "rad/s) est :", ["<i>P</i> = <i>C</i> · ω", f"<i>P</i> = {vec('C')} · {vec('ω')}", f"<i>P</i> = {vec('ω')} · {vec('C')}"],
        "abc",
        f"<p><i>P</i> = <i>C</i>·ω. Le couple et la vitesse angulaire sont portés par le même axe, l'axe de rotation : le "
        f"produit scalaire {vec('C')}·{vec('ω')} = {vec('ω')}·{vec('C')} se réduit au produit de leurs valeurs "
        "algébriques <i>C</i>·ω. Les trois écritures sont justes, alors qu'à la question précédente la force et la vitesse "
        "n'ont pas, en général, la même direction.</p>"),
])]

# ============================================================ A3 — ascenseur et escalier roulant
m, V, f, h = 850, 1.2, 400, 25
P_asc = m * G
T_asc = P_asc + f
Pw_asc = T_asc * V
t_asc = h / V
W_asc = T_asc * h
W1_esc = 600 * 5
Pu_esc = 36 * W1_esc / 60
eta_esc = Pu_esc / 2200
A3 = [
    partie("La cabine d'ascenseur", 14, [
        '<div class="cours-split"><div>'
        "<p>Une cabine d'ascenseur monte du sous-sol au dernier étage, 25 m plus haut, à la vitesse constante de "
        "1,2 m/s. Calculer le travail et la puissance de levage.</p>" +
        donnees("masse de l'ensemble (cabine et passagers) : <i>m</i> = 850 kg",
                "vitesse de levage, supposée constante : <i>V</i> = 1,2 m/s",
                "frottements sur les glissières : <i>f</i> = 40 daN = 400 N",
                "hauteur entre le sous-sol et le dernier étage : <i>h</i> = 25 m", "<i>g</i> = 9,81 m/s²") +
        "</div>" + fig(fg.fig_ascenseur, "Figure 1 — Cabine d'ascenseur.", "Cabine d'ascenseur entre deux glissières, "
                       "tirée par un câble, vitesse 1,2 m/s vers le haut", 380) + "</div>"], [
        QBAR(["DT1"]),
        Q("Calcule le poids <i>P</i> de l'ensemble.", H_NUM, num(P_asc, "N"), f"<i>P</i> = <i>m</i>·<i>g</i> = {fr(P_asc, 1)} N",
          eq(f"<i>P</i> = <i>m</i>·<i>g</i> = 850 × 9,81 = {fr(P_asc, 1)} N")),
        Q("Calcule l'effort de traction <i>T</i> du câble pendant la montée.", H_NUM, num(T_asc, "N"),
          f"<i>T</i> = {fr(T_asc, 1)} N",
          "<p>La vitesse est constante : l'énergie cinétique ne varie pas, la somme des travaux est nulle et le câble "
          "compense exactement le poids et les frottements.</p>" + eq(f"<i>T</i> = <i>P</i> + <i>f</i> = {fr(P_asc, 1)} + 400 = {fr(T_asc, 1)} N")),
        Q("Calcule la puissance de levage <i>P</i><sub>L</sub> fournie par le câble.", H_NUM, num(Pw_asc / 1000, "kW"),
          f"<i>P</i><sub>L</sub> = {fr(Pw_asc, 0)} W ≈ {fr(Pw_asc / 1000, 2)} kW",
          eq(f"<i>P</i><sub>L</sub> = <i>T</i>·<i>V</i> = {fr(T_asc, 1)} × 1,2 = {fr(Pw_asc, 0)} W ≈ {fr(Pw_asc / 1000, 2)} kW")),
        Q("Calcule la durée <i>t</i> de la montée.", H_NUM, num(t_asc, "s"), f"<i>t</i> = {fr(t_asc, 2)} s",
          eq(f"<i>t</i> = <i>h</i> / <i>V</i> = 25 / 1,2 = {fr(t_asc, 2)} s")),
        Q("Calcule le travail <i>W</i> fourni par le câble pendant la montée.", H_NUM, num(W_asc / 1000, "kJ"),
          f"<i>W</i> = {fr(W_asc, 0)} J ≈ {fr(W_asc / 1000, 2)} kJ",
          eq(f"<i>W</i> = <i>T</i>·<i>h</i> = {fr(T_asc, 1)} × 25 = {fr(W_asc, 0)} J ≈ {fr(W_asc / 1000, 2)} kJ") +
          "<p>Vérification : <i>W</i> = <i>P</i><sub>L</sub>·<i>t</i> = " + f"{fr(Pw_asc, 0)} × {fr(t_asc, 2)} ≈ {fr(W_asc, 0)} J : "
          "la puissance est le débit d'énergie.</p>"),
    ]),
    partie("L'escalier roulant", 10, [
        '<div class="cours-split"><div>'
        "<p>Un escalier roulant de magasin transporte 36 personnes par minute entre le premier et le deuxième étage. "
        "Le moteur délivre en permanence une puissance de 2,2 kW. Déterminer le rendement du système.</p>" +
        donnees("différence de niveau : <i>h</i> = 5 m ; inclinaison : 30°",
                "poids moyen d'une personne : 60 daN = 600 N", "débit : 36 personnes par minute",
                "puissance délivrée par le moteur : 2,2 kW") +
        "</div>" + fig(fg.fig_escalier, "Figure 2 — Escalier roulant.", "Escalier roulant incliné à 30°, dénivellation "
                       "5 m, une personne transportée", 420) + "</div>"], [
        Q("Calcule le travail <i>W</i><sub>1</sub> nécessaire pour élever une personne d'un étage.", H_NUM,
          num(W1_esc, "J"), "<i>W</i><sub>1</sub> = 3 000 J",
          "<p>Le travail du poids ne dépend que de la dénivellation : l'inclinaison de 30° (et donc la longueur de "
          "l'escalier) n'intervient pas.</p>" + eq("<i>W</i><sub>1</sub> = <i>P</i>·<i>h</i> = 600 × 5 = 3 000 J")),
        Q("Calcule la puissance utile <i>P</i><sub>u</sub> nécessaire pour élever les 36 personnes par minute.", H_NUM,
          num(Pu_esc, "W"), "<i>P</i><sub>u</sub> = 1 800 W",
          eq(f"<i>P</i><sub>u</sub> = {frac('36 × 3 000', '60')} = 1 800 W")),
        Q("Calcule le rendement η du système.", H_SANS + " (0,8 ou 80 %, par exemple)",
          num(eta_esc, None, rel=0.01, alt=(eta_esc * 100,)), f"η ≈ {fr(eta_esc, 3)} (soit {fr(eta_esc * 100, 1)} %)",
          eq(f"η = {frac('<i>P</i><sub>u</sub>', '<i>P</i><sub>moteur</sub>')} = {frac('1 800', '2 200')} ≈ {fr(eta_esc, 3)}") +
          "<p>Le reste (400 W) est perdu en frottements et en chaleur.</p>"),
    ]),
]

# ============================================================ A4 — remonte-pente et bateau
t_rp = 1800 / 2
n_rp = 1200 * t_rp / 3600
Pu_rp = 1200 * 70 * G * 600 / 3600
Pa_rp = Pu_rp / 0.7
Pi_rp = 3 * Pa_rp
v_b = 15 * 0.5144
Pt_b = 5500 * 736
Pu_b = 0.4 * Pt_b
R_b = Pu_b / v_b
A4 = [
    partie("Le remonte-pente", 16, [
        '<div class="cours-split"><div>'
        "<p>Un remonte-pente de station de ski tire 1 200 skieurs par heure à la vitesse de 120 m par minute. "
        "Déterminer la puissance moyenne du moteur nécessaire au transport des skieurs.</p>" +
        donnees("masse moyenne d'un skieur : 70 kg", "longueur de la pente : 1 800 m ; dénivellation : 600 m (pente de 33 %)",
                "vitesse : 120 m/min = 2 m/s", "rendement de l'installation : 0,7",
                "surcharge admise de 200 % : le moteur doit pouvoir fournir <b>trois fois</b> la puissance nécessaire en "
                "service normal (100 % + 200 %)") +
        "</div>" + fig(fg.fig_remonte, "Figure 1 — Remonte-pente.", "Pente de 1 800 m de long et 600 m de dénivellation, "
                       "skieurs tirés par un câble", 440) + "</div>"], [
        QBAR(["DT1"]),
        Q("Calcule la durée <i>t</i> de la montée d'un skieur.", H_NUM, num(t_rp, "s"), "<i>t</i> = 900 s (15 min)",
          eq("<i>V</i> = 120 m/min = 2 m/s ; <i>t</i> = 1 800 / 2 = 900 s")),
        Q("Combien de skieurs sont, à chaque instant, sur la pente ?", "Un nombre entier.", num(n_rp, None, abs_=0.5),
          "300 skieurs", eq(f"<i>n</i> = 1 200 skieurs/h × {frac('900 s', '3 600 s')} = 300 skieurs") +
          "<p>Il part un skieur toutes les 3 s : ils sont espacés de 6 m sur 1 800 m de câble.</p>"),
        Q("Calcule la puissance utile moyenne <i>P</i><sub>u</sub> nécessaire pour élever les skieurs.", H_NUM,
          num(Pu_rp / 1000, "kW"), f"<i>P</i><sub>u</sub> ≈ {fr(Pu_rp / 1000, 1)} kW",
          "<p>En une heure, 1 200 skieurs sont élevés de 600 m :</p>" +
          eq(f"<i>P</i><sub>u</sub> = {frac('1 200 × 70 × 9,81 × 600', '3 600')} = {fr(Pu_rp, 0)} W ≈ {fr(Pu_rp / 1000, 1)} kW") +
          "<p>Autre calcul : 300 skieurs montent chacun à la vitesse verticale 2 × 600/1 800 ≈ 0,667 m/s : "
          f"<i>P</i><sub>u</sub> = 300 × 70 × 9,81 × 0,667 ≈ {fr(Pu_rp / 1000, 1)} kW.</p>"),
        Q("Calcule la puissance <i>P</i><sub>a</sub> absorbée par l'installation en service normal.", H_NUM,
          num(Pa_rp / 1000, "kW"), f"<i>P</i><sub>a</sub> ≈ {fr(Pa_rp / 1000, 1)} kW",
          eq(f"<i>P</i><sub>a</sub> = {frac('<i>P</i><sub>u</sub>', 'η')} = {frac(fr(Pu_rp / 1000, 2), '0,7')} ≈ {fr(Pa_rp / 1000, 1)} kW")),
        Q("Calcule la puissance du moteur à installer, compte tenu de la surcharge de 200 %.", H_NUM,
          num(Pi_rp / 1000, "kW"), f"<i>P</i> ≈ {fr(Pi_rp / 1000, 0)} kW",
          eq(f"<i>P</i> = 3 × <i>P</i><sub>a</sub> = 3 × {fr(Pa_rp / 1000, 1)} ≈ {fr(Pi_rp / 1000, 0)} kW")),
    ]),
    partie("Le bateau", 9, [
        '<div class="cours-split"><div>'
        "<p>Un bateau se déplace à la vitesse de 15 nœuds ; sa turbine développe une puissance de 5 500 cv. Calculer "
        "la résistance à l'avancement du bateau.</p>" +
        donnees("1 nœud = 0,5144 m/s", "1 cv = 736 W", "rendement de l'ensemble turbine + hélice : 0,4") +
        "</div>" + fig(fg.fig_bateau, "Figure 2 — Bateau.", "Bateau à la vitesse V, résistance à l'avancement R", 400) +
        "</div>"], [
        Q("Convertis la vitesse du bateau en m/s.", H_NUM, num(v_b, "m/s"), f"<i>V</i> = {fr(v_b, 3)} m/s",
          eq(f"<i>V</i> = 15 × 0,5144 = {fr(v_b, 3)} m/s")),
        Q("Calcule la puissance de la turbine en kW.", H_NUM, num(Pt_b / 1000, "kW"), f"{fr(Pt_b / 1000, 0)} kW",
          eq(f"<i>P</i><sub>t</sub> = 5 500 × 736 = {fr(Pt_b, 0)} W = {fr(Pt_b / 1000, 0)} kW")),
        Q("Calcule la puissance utile <i>P</i><sub>u</sub>, qui fait avancer le bateau.", H_NUM, num(Pu_b / 1000, "kW"),
          f"<i>P</i><sub>u</sub> ≈ {fr(Pu_b / 1000, 0)} kW",
          eq(f"<i>P</i><sub>u</sub> = η·<i>P</i><sub>t</sub> = 0,4 × {fr(Pt_b / 1000, 0)} ≈ {fr(Pu_b / 1000, 0)} kW")),
        Q("Calcule la résistance à l'avancement <i>R</i> du bateau.", H_NUM, num(R_b / 1000, "kN"),
          f"<i>R</i> ≈ {fr(R_b / 1000, 0)} kN",
          "<p>À vitesse constante, la poussée de l'hélice équilibre la résistance <i>R</i> : <i>P</i><sub>u</sub> = <i>R</i>·<i>V</i>.</p>" +
          eq(f"<i>R</i> = {frac('<i>P</i><sub>u</sub>', '<i>V</i>')} = {frac(fr(Pu_b, 0), fr(v_b, 3))} ≈ {fr(R_b, 0)} N ≈ {fr(R_b / 1000, 0)} kN")),
    ]),
]

# ============================================================ A5 — amortisseur de fin de course
m5, V5, c5, a5 = 300, 2.0, 0.1, math.radians(10)
Ec5 = 0.5 * m5 * V5 ** 2
Wp5 = m5 * G * c5 * math.sin(a5)
Wr5 = -(Ec5 + Wp5)
K5 = 2 * (Ec5 + Wp5) / c5 ** 2
F5 = K5 * c5
A5 = [partie("L'amortisseur de fin de course", 20, [
    '<div class="cours-split"><div>'
    "<p>Le wagonnet descend un rail incliné et arrive en fin de course sur un amortisseur, assimilé à un ressort de "
    "raideur <i>K</i>. Il s'arrête au bout de la course d'amortissement. Déterminer la raideur du ressort et l'effort "
    "exercé en fin de course (frottements négligés).</p>" +
    donnees("masse du wagonnet : <i>m</i> = 300 kg", "vitesse à l'arrivée sur l'amortisseur : <i>V</i> = 2 m/s",
            "course d'amortissement : <i>c</i> = 100 mm", "pente du rail : 10°") +
    "</div>" + fig(fg.fig_amortisseur, "Figure 1 — Amortisseur de fin de course.", "Wagonnet descendant un rail incliné "
                   "de 10° vers un amortisseur à ressort", 460) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule l'énergie cinétique <i>E</i><sub>c</sub> du wagonnet à l'arrivée sur l'amortisseur.", H_NUM,
      num(Ec5, "J"), "<i>E</i><sub>c</sub> = 600 J", eq("<i>E</i><sub>c</sub> = ½·<i>m</i>·<i>V</i>² = ½ × 300 × 2² = 600 J")),
    Q("Calcule le travail <i>W</i><sub>P</sub> du poids pendant la course d'amortissement.", H_NUM, num(Wp5, "J"),
      f"<i>W</i><sub>P</sub> ≈ {fr(Wp5, 1)} J",
      "<p>Le wagonnet descend de <i>c</i>·sin 10° pendant la compression : le poids est moteur.</p>" +
      eq(f"<i>W</i><sub>P</sub> = <i>m</i>·<i>g</i>·<i>c</i>·sin 10° = 300 × 9,81 × 0,1 × {fr(math.sin(a5), 4)} ≈ {fr(Wp5, 1)} J")),
    Q("Applique le théorème de l'énergie cinétique : calcule le travail <i>W</i><sub>R</sub> du ressort, avec son signe.",
      H_NUM, num(Wr5, "J"), f"<i>W</i><sub>R</sub> ≈ {fr(Wr5, 1)} J",
      eq("<i>E</i><sub>c2</sub> − <i>E</i><sub>c1</sub> = <i>W</i><sub>P</sub> + <i>W</i><sub>R</sub> (la réaction du rail, "
         "perpendiculaire au déplacement, ne travaille pas)",
         f"0 − 600 = {fr(Wp5, 1)} + <i>W</i><sub>R</sub> ⇒ <i>W</i><sub>R</sub> = {fr(Wr5, 1)} J") +
      "<p>Le travail du ressort est résistant : il absorbe l'énergie cinétique et le travail du poids.</p>"),
    Q("Calcule la raideur <i>K</i> du ressort.", H_NUM, num(K5 / 1000, "kN/m"), f"<i>K</i> ≈ {fr(K5 / 1000, 1)} kN/m",
      eq(f"½·<i>K</i>·<i>c</i>² = {fr(-Wr5, 1)} J ⇒ <i>K</i> = {frac('2 × ' + fr(-Wr5, 1), '0,1²')} ≈ {fr(K5, 0)} N/m ≈ {fr(K5 / 1000, 1)} kN/m")),
    Q("Calcule l'effort <i>F</i> exercé par le ressort en fin de course.", H_NUM, num(F5 / 1000, "kN"),
      f"<i>F</i> ≈ {fr(F5, 0)} N ≈ {fr(F5 / 1000, 1)} kN",
      eq(f"<i>F</i> = <i>K</i>·<i>c</i> = {fr(K5, 0)} × 0,1 ≈ {fr(F5, 0)} N")),
])]

# ============================================================ A6 — wagon sur une pente de 2 %
a6 = math.atan(0.02)
h6 = 20 * math.sin(a6)
V6 = math.sqrt(2 * G * h6)
Ec6 = m5 * G * h6
K6 = 10_000e3
F6p = m5 * G * math.sin(a6)
x6 = (F6p + math.sqrt(F6p ** 2 + 2 * K6 * Ec6)) / K6
Fm6 = K6 * x6
A6 = [partie("Le wagon sur une pente de 2 %", 18, [
    '<div class="cours-split"><div>'
    "<p>On reprend le wagonnet de 300 kg de l'activité A5. Il descend maintenant une pente de 2 %, départ arrêté, sur "
    "une longueur de rail de 20 m, puis rencontre l'amortisseur. Déterminer la vitesse du wagon au moment du contact et "
    "la course de compression du ressort (frottements négligés).</p>" +
    donnees("masse : <i>m</i> = 300 kg", "pente : 2 % (tan α = 0,02)", "longueur parcourue avant le contact : 20 m, départ arrêté",
            "raideur du ressort : <i>K</i> = 10 000 kN/m") +
    "</div>" + fig(fg.fig_wagon_pente, "Figure 1 — Wagon descendant une pente de 2 %.", "Wagonnet sur un rail en légère "
                   "pente, amortisseur en bas", 460) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule la dénivellation <i>h</i> parcourue avant le contact.", H_NUM, num(h6, "m"), f"<i>h</i> ≈ {fr(h6, 3)} m",
      eq(f"α = arctan 0,02 ≈ {fr(math.degrees(a6), 2)}° ; <i>h</i> = 20 × sin α ≈ {fr(h6, 3)} m") +
      "<p>Pour une pente faible, sin α ≈ tan α : <i>h</i> ≈ 20 × 0,02 = 0,4 m.</p>"),
    Q("Calcule la vitesse <i>V</i> du wagon au moment du contact.", H_NUM, num(V6, "m/s"), f"<i>V</i> ≈ {fr(V6, 2)} m/s",
      "<p>Conservation de l'énergie (pas de frottement) : l'énergie potentielle perdue devient énergie cinétique.</p>" +
      eq(f"½·<i>m</i>·<i>V</i>² = <i>m</i>·<i>g</i>·<i>h</i> ⇒ <i>V</i> = √(2·<i>g</i>·<i>h</i>) = √(2 × 9,81 × {fr(h6, 3)}) ≈ {fr(V6, 2)} m/s")),
    Q("Calcule l'énergie cinétique <i>E</i><sub>c</sub> du wagon au moment du contact.", H_NUM, num(Ec6, "J"),
      f"<i>E</i><sub>c</sub> ≈ {fr(Ec6, 0)} J", eq(f"<i>E</i><sub>c</sub> = <i>m</i>·<i>g</i>·<i>h</i> = 300 × 9,81 × {fr(h6, 3)} ≈ {fr(Ec6, 0)} J")),
    Q("Calcule la course de compression <i>x</i> du ressort.", "Saisis la valeur avec son unité (mm ou m) ; tolérance de 2 %.",
      num(x6 * 1000, "mm"), f"<i>x</i> ≈ {fr(x6 * 1000, 1)} mm",
      "<p>Théorème de l'énergie cinétique entre le contact et l'arrêt : le poids travaille encore (le wagon descend de "
      "<i>x</i>·sin α), le ressort absorbe tout.</p>" +
      eq(f"0 − <i>E</i><sub>c</sub> = <i>m</i>·<i>g</i>·<i>x</i>·sin α − ½·<i>K</i>·<i>x</i>²",
         f"½ × 10<sup>7</sup> × <i>x</i>² − {fr(F6p, 1)}·<i>x</i> − {fr(Ec6, 0)} = 0 ⇒ <i>x</i> ≈ {fr(x6, 4)} m ≈ {fr(x6 * 1000, 1)} mm") +
      f"<p>Le terme du poids ({fr(F6p * x6, 1)} J) est négligeable : <i>x</i> ≈ √(2·<i>E</i><sub>c</sub>/<i>K</i>) donne la même valeur.</p>"),
    Q("Calcule l'effort maximal <i>F</i> exercé par le ressort.", H_NUM, num(Fm6 / 1000, "kN"),
      f"<i>F</i> ≈ {fr(Fm6 / 1000, 0)} kN",
      eq(f"<i>F</i> = <i>K</i>·<i>x</i> = 10<sup>7</sup> × {fr(x6, 4)} ≈ {fr(Fm6, 0)} N ≈ {fr(Fm6 / 1000, 0)} kN") +
      "<p>Un ressort très raide arrête le wagon sur une course courte, mais au prix d'un effort considérable (plus de "
      "50 fois le poids du wagon) : comparer avec l'amortisseur de l'activité A5.</p>"),
])]

# ============================================================ A7 — freinage dans une pente
m7, V7, F7 = 1000, 90 / 3.6, 2500
a7 = math.atan(0.10)
Ec7 = 0.5 * m7 * V7 ** 2
Pp7 = m7 * G * math.sin(a7)
x7 = Ec7 / (F7 - Pp7)
W7 = F7 * x7
A7 = [partie("Le freinage dans une pente", 15, [
    '<div class="cours-split"><div>'
    "<p>Une automobile descend une pente de 10 %. Les freins sont actionnés et exercent un effort résultant de "
    "freinage constant, parallèle à la pente. Déterminer la distance parcourue avant l'arrêt et l'énergie dissipée par "
    "le freinage.</p>" +
    donnees("masse : <i>m</i> = 1 000 kg", "pente : 10 % (tan α = 0,10)", "vitesse initiale : 90 km/h",
            "effort de freinage : <i>F</i> = 2 500 N") +
    "</div>" + fig(fg.fig_auto, "Figure 1 — Freinage dans une pente.", "Automobile descendant une pente de 10 % à "
                   "90 km/h, distance d'arrêt x", 460) + "</div>"], [
    QBAR(["DT1"]),
    Q("Convertis la vitesse initiale en m/s.", H_NUM, num(V7, "m/s"), "<i>V</i><sub>0</sub> = 25 m/s",
      eq("<i>V</i><sub>0</sub> = 90 / 3,6 = 25 m/s")),
    Q("Calcule l'énergie cinétique initiale <i>E</i><sub>c0</sub>.", H_NUM, num(Ec7 / 1000, "kJ"),
      f"<i>E</i><sub>c0</sub> = {fr(Ec7 / 1000, 1)} kJ", eq(f"<i>E</i><sub>c0</sub> = ½ × 1 000 × 25² = {fr(Ec7, 0)} J")),
    Q("Calcule la composante du poids parallèle à la pente.", H_NUM, num(Pp7, "N"), f"≈ {fr(Pp7, 0)} N",
      eq(f"α = arctan 0,10 ≈ {fr(math.degrees(a7), 2)}° ; <i>m</i>·<i>g</i>·sin α = 1 000 × 9,81 × {fr(math.sin(a7), 4)} ≈ {fr(Pp7, 0)} N")),
    Q("Calcule la distance <i>x</i> parcourue avant l'arrêt.", H_NUM, num(x7, "m"), f"<i>x</i> ≈ {fr(x7, 0)} m",
      "<p>Théorème de l'énergie cinétique : le poids est moteur (descente), le freinage résistant.</p>" +
      eq(f"0 − <i>E</i><sub>c0</sub> = <i>m</i>·<i>g</i>·sin α·<i>x</i> − <i>F</i>·<i>x</i>",
         f"<i>x</i> = {frac('<i>E</i><sub>c0</sub>', '<i>F</i> − <i>m</i>·<i>g</i>·sin α')} = "
         f"{frac(fr(Ec7, 0), '2 500 − ' + fr(Pp7, 0))} ≈ {fr(x7, 1)} m")),
    Q("Calcule l'énergie <i>W</i> dissipée par le freinage.", H_NUM, num(W7 / 1000, "kJ"), f"<i>W</i> ≈ {fr(W7 / 1000, 1)} kJ",
      eq(f"<i>W</i> = <i>F</i>·<i>x</i> = 2 500 × {fr(x7, 1)} ≈ {fr(W7, 0)} J ≈ {fr(W7 / 1000, 1)} kJ") +
      "<p>Les freins dissipent l'énergie cinétique initiale et l'énergie potentielle perdue pendant le freinage "
      f"({fr(Pp7 * x7 / 1000, 1)} kJ) : elles finissent en chaleur.</p>"),
])]

# ============================================================ A8 — vérin de levage
P8, V8, L8 = 30000, 0.3, 0.02
m8 = P8 / G
Ec8 = 0.5 * m8 * V8 ** 2
F8 = Ec8 / L8
Ft8 = P8 + F8
S8 = PI / 4 * (60 ** 2 - 40 ** 2)
p8 = Ft8 / S8  # MPa
A8 = [partie("Le vérin de levage", 22, [
    '<div class="cours-split"><div>'
    "<p>Le vérin de levage travaille uniquement en tirant ; le côté fond est relié à l'atmosphère. L'ensemble descend "
    "sous l'effet de la charge, à vitesse constante. L'alimentation est assurée par une pompe hydraulique à débit fixe, "
    "avec régulation à la descente. L'arrêt de la charge, en fin de course de sortie de tige, est obtenu par une valve "
    "de décélération qui travaille sur la course <i>L</i>.</p>"
    "<p>On appelle <i>F</i> l'effort de décélération : l'effort que la tige exerce <b>en plus</b> de celui qui retient "
    "la charge en descente uniforme. Il est supposé constant sur la course <i>L</i>. Déterminer <i>F</i>, puis la "
    "pression interne maximale dans le vérin.</p>" +
    donnees("charge : <i>P</i> = 3 000 daN = 30 000 N", "vitesse de descente : <i>V</i> = 0,3 m/s",
            "course de décélération : <i>L</i> = 20 mm", "diamètre de la tige : 40 mm ; diamètre de l'alésage : 60 mm") +
    "</div>" + fig(fg.fig_verin, "Figure 1 — Vérin de levage.", "Vérin vertical suspendu, tige vers le bas portant "
                   "une charge de 3 000 daN qui descend à 0,3 m/s", 360) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule la masse <i>m</i> de la charge.", H_NUM, num(m8, "kg"), f"<i>m</i> ≈ {fr(m8, 0)} kg",
      eq(f"<i>m</i> = <i>P</i> / <i>g</i> = 30 000 / 9,81 ≈ {fr(m8, 0)} kg")),
    Q("Calcule l'énergie cinétique <i>E</i><sub>c</sub> de la charge pendant la descente.", H_NUM, num(Ec8, "J"),
      f"<i>E</i><sub>c</sub> ≈ {fr(Ec8, 1)} J", eq(f"<i>E</i><sub>c</sub> = ½ × {fr(m8, 1)} × 0,3² ≈ {fr(Ec8, 1)} J")),
    Q("Calcule l'effort de décélération <i>F</i>.", H_NUM, num(F8, "N"), f"<i>F</i> ≈ {fr(F8, 0)} N",
      "<p>Théorème de l'énergie cinétique sur la course <i>L</i> : le poids est moteur, la tige résistante, avec "
      "l'effort <i>P</i> + <i>F</i>.</p>" +
      eq("0 − <i>E</i><sub>c</sub> = <i>P</i>·<i>L</i> − (<i>P</i> + <i>F</i>)·<i>L</i> ⇒ <i>F</i>·<i>L</i> = <i>E</i><sub>c</sub>",
         f"<i>F</i> = {frac(fr(Ec8, 1), '0,02')} ≈ {fr(F8, 0)} N")),
    Q("Calcule l'effort total <i>F</i><sub>t</sub> exercé par l'huile sur le piston en fin de course.", H_NUM,
      num(Ft8 / 1000, "kN"), f"<i>F</i><sub>t</sub> ≈ {fr(Ft8, 0)} N",
      eq(f"<i>F</i><sub>t</sub> = <i>P</i> + <i>F</i> = 30 000 + {fr(F8, 0)} ≈ {fr(Ft8, 0)} N")),
    Q("Calcule la section annulaire <i>S</i> sur laquelle agit l'huile (côté tige).", H_NUM, num(S8, "mm²"),
      f"<i>S</i> ≈ {fr(S8, 0)} mm²",
      "<p>Le vérin travaille en tirant : l'huile pousse sur la couronne du piston, entre l'alésage et la tige.</p>" +
      eq(f"<i>S</i> = {frac('π', '4')} × (60² − 40²) = {frac('π', '4')} × 2 000 ≈ {fr(S8, 0)} mm²")),
    Q("Calcule la pression maximale <i>p</i> dans le vérin, en bar.", H_NUM, num(p8 * 10, "bar"),
      f"<i>p</i> ≈ {fr(p8 * 10, 0)} bar ({fr(p8, 1)} MPa)",
      eq(f"<i>p</i> = {frac('<i>F</i><sub>t</sub>', '<i>S</i>')} = {frac(fr(Ft8, 0) + ' N', fr(S8, 0) + ' mm²')} ≈ "
         f"{fr(p8, 2)} N/mm² = {fr(p8, 2)} MPa ≈ {fr(p8 * 10, 0)} bar")),
])]

# ============================================================ A9, A10 — freins à sabot(s)
J9 = 1000 * 0.4 ** 2
w9 = tr_min(200)
Ec9 = 0.5 * J9 * w9 ** 2
th9 = 50 * 2 * PI
C9 = Ec9 / th9
T9 = C9 / 0.36
N9 = T9 / 0.3
F9 = N9 * 600 / 1400
A9 = [partie("Le frein à sabot", 22, [
    '<div class="cours-split"><div>'
    "<p>On souhaite arrêter le tambour en 50 tours avec le frein à sabot schématisé ci-contre. Quel effort <i>F</i> "
    "faut-il exercer sur le levier ?</p>" +
    donnees("vitesse initiale du tambour : 200 tr/min",
            "masse du tambour et du dispositif en rotation : 1 000 kg ; rayon de giration : 400 mm",
            "rayon du tambour : <i>r</i> = 360 mm ; frottement sabot/tambour : <i>f</i> = μ = 0,3",
            "levier articulé en A : le sabot appuie à 600 mm de A, l'effort <i>F</i> s'exerce à 600 + 800 = 1 400 mm de A",
            "on néglige le moment, par rapport à A, de l'effort de frottement sur le sabot") +
    "</div>" + fig(fg.fig_frein_sabot, "Figure 1 — Frein à sabot.", "Levier articulé en A, sabot appuyé sur le "
                   "tambour, effort F à l'extrémité du levier", 460) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule le moment d'inertie <i>J</i> du dispositif en rotation.", H_NUM, num(J9, "kg·m²"),
      "<i>J</i> = 160 kg·m²", eq("<i>J</i> = <i>m</i>·<i>k</i>² = 1 000 × 0,4² = 160 kg·m²")),
    Q("Calcule la vitesse angulaire initiale ω<sub>0</sub>.", H_NUM, num(w9, "rad/s"), f"ω<sub>0</sub> ≈ {fr(w9, 2)} rad/s",
      eq(f"ω<sub>0</sub> = {frac('π·<i>N</i>', '30')} = {frac('π × 200', '30')} ≈ {fr(w9, 2)} rad/s")),
    Q("Calcule l'énergie cinétique initiale <i>E</i><sub>c0</sub>.", H_NUM, num(Ec9 / 1000, "kJ"),
      f"<i>E</i><sub>c0</sub> ≈ {fr(Ec9, 0)} J", eq(f"<i>E</i><sub>c0</sub> = ½ × 160 × {fr(w9, 2)}² ≈ {fr(Ec9, 0)} J")),
    Q("Calcule l'angle θ balayé par le tambour pendant le freinage, en radians.", H_NUM, num(th9, "rad"),
      f"θ ≈ {fr(th9, 1)} rad", eq(f"θ = 50 × 2π = 100π ≈ {fr(th9, 1)} rad")),
    Q("Calcule le couple de freinage <i>C</i>, supposé constant.", H_NUM, num(C9, "N·m"), f"<i>C</i> ≈ {fr(C9, 1)} N·m",
      "<p>Théorème de l'énergie cinétique : seul le couple de freinage travaille (le poids et les actions des paliers "
      "passent par l'axe).</p>" +
      eq(f"0 − <i>E</i><sub>c0</sub> = −<i>C</i>·θ ⇒ <i>C</i> = {frac(fr(Ec9, 0), fr(th9, 1))} ≈ {fr(C9, 1)} N·m")),
    Q("Calcule l'effort tangentiel <i>T</i> du sabot sur le tambour.", H_NUM, num(T9, "N"), f"<i>T</i> ≈ {fr(T9, 0)} N",
      eq(f"<i>C</i> = <i>T</i>·<i>r</i> ⇒ <i>T</i> = {frac(fr(C9, 1), '0,36')} ≈ {fr(T9, 0)} N")),
    Q("Calcule l'effort presseur <i>N</i> du sabot sur le tambour.", H_NUM, num(N9, "N"), f"<i>N</i> ≈ {fr(N9, 0)} N",
      eq(f"<i>T</i> = <i>f</i>·<i>N</i> ⇒ <i>N</i> = {frac(fr(T9, 0), '0,3')} ≈ {fr(N9, 0)} N")),
    Q("Calcule l'effort <i>F</i> à exercer sur le levier.", H_NUM, num(F9, "N"), f"<i>F</i> ≈ {fr(F9, 0)} N",
      "<p>Équilibre du levier : moments par rapport à A (le moment du frottement est négligé).</p>" +
      eq(f"<i>F</i> × 1 400 = <i>N</i> × 600 ⇒ <i>F</i> = {fr(N9, 0)} × {frac('600', '1 400')} ≈ {fr(F9, 0)} N")),
])]

w10 = tr_min(400)
Ec10 = 0.5 * J9 * w10 ** 2
C10 = Ec10 / th9
T10 = C10 / (2 * 0.36)
N10 = T10 / 0.25
F10 = N10 * 600 / 1400
P10 = C10 * w10
A10 = [partie("Le frein à deux sabots", 18, [
    '<div class="cours-split"><div>'
    "<p>On reprend le tambour de l'activité A9, freiné cette fois par deux sabots identiques disposés "
    "symétriquement, chacun au bout d'un levier identique à celui de l'activité A9. Le tambour tourne à 400 tr/min au "
    "début du freinage et doit s'arrêter en 50 tours. Déterminer l'effort <i>F</i> sur chaque levier et la puissance "
    "de freinage au début du mouvement.</p>" +
    donnees("moment d'inertie du tambour : <i>J</i> = 160 kg·m² ; rayon : <i>r</i> = 360 mm",
            "frottement sabot/tambour : <i>f</i> = μ = 0,25",
            "chaque levier : sabot à 600 mm de l'articulation, effort <i>F</i> à 1 400 mm",
            "vitesse au début du freinage : 400 tr/min ; arrêt en 50 tours") +
    "</div>" + fig(lambda: fg.fig_frein_sabot(True), "Figure 1 — Frein à deux sabots.", "Tambour serré par deux sabots "
                   "symétriques portés par deux leviers", 420) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule la vitesse angulaire initiale ω<sub>0</sub>.", H_NUM, num(w10, "rad/s"), f"ω<sub>0</sub> ≈ {fr(w10, 2)} rad/s",
      eq(f"ω<sub>0</sub> = π × 400 / 30 ≈ {fr(w10, 2)} rad/s")),
    Q("Calcule l'énergie cinétique initiale <i>E</i><sub>c0</sub>.", H_NUM, num(Ec10 / 1000, "kJ"),
      f"<i>E</i><sub>c0</sub> ≈ {fr(Ec10 / 1000, 1)} kJ",
      eq(f"<i>E</i><sub>c0</sub> = ½ × 160 × {fr(w10, 2)}² ≈ {fr(Ec10, 0)} J") +
      "<p>Deux fois plus vite : quatre fois plus d'énergie qu'à 200 tr/min.</p>"),
    Q("Calcule le couple de freinage total <i>C</i>.", H_NUM, num(C10, "N·m"), f"<i>C</i> ≈ {fr(C10, 1)} N·m",
      eq(f"<i>C</i> = {frac('<i>E</i><sub>c0</sub>', 'θ')} = {frac(fr(Ec10, 0), fr(th9, 1))} ≈ {fr(C10, 1)} N·m")),
    Q("Calcule l'effort tangentiel <i>T</i> exercé par <b>chaque</b> sabot.", H_NUM, num(T10, "N"),
      f"<i>T</i> ≈ {fr(T10, 0)} N",
      "<p>Les deux sabots se partagent le couple : <i>C</i> = 2·<i>T</i>·<i>r</i>.</p>" +
      eq(f"<i>T</i> = {frac(fr(C10, 1), '2 × 0,36')} ≈ {fr(T10, 0)} N")),
    Q("Calcule l'effort presseur <i>N</i> de chaque sabot.", H_NUM, num(N10, "N"), f"<i>N</i> ≈ {fr(N10, 0)} N",
      eq(f"<i>N</i> = {frac('<i>T</i>', '<i>f</i>')} = {frac(fr(T10, 0), '0,25')} ≈ {fr(N10, 0)} N")),
    Q("Calcule l'effort <i>F</i> à exercer sur chaque levier.", H_NUM, num(F10, "N"), f"<i>F</i> ≈ {fr(F10, 0)} N",
      eq(f"<i>F</i> = <i>N</i> × {frac('600', '1 400')} ≈ {fr(F10, 0)} N")),
    Q("Calcule la puissance de freinage au début du mouvement.", H_NUM, num(P10 / 1000, "kW"),
      f"<i>P</i> ≈ {fr(P10 / 1000, 1)} kW",
      eq(f"<i>P</i> = <i>C</i>·ω<sub>0</sub> = {fr(C10, 1)} × {fr(w10, 2)} ≈ {fr(P10, 0)} W ≈ {fr(P10 / 1000, 1)} kW") +
      "<p>La puissance de freinage diminue ensuite avec la vitesse : elle est nulle à l'arrêt.</p>"),
])]


# ============================================================ planches de construction (millimètres)
def deg(v):
    return cg.angle(v)


# ---------- G1 — skip de chargement : projections
def planche_skip():
    a = math.radians(70)
    O = (40.0, 165.0)
    d = (math.cos(a), -math.sin(a))
    nrm = (math.sin(a), math.cos(a))
    Tp = cg.add(O, cg.mul(d, 150))
    Gp = cg.add(cg.add(O, cg.mul(d, 75)), cg.mul(nrm, 14))
    Vt = cg.add(Gp, cg.mul(d, 60))
    Pt = (Gp[0], Gp[1] + 60)
    sol_a, sol_b = (8.0, 165.0), (200.0, 165.0)
    rail2 = (cg.add(O, cg.mul(nrm, 4)), cg.add(Tp, cg.mul(nrm, 4)))
    fond = (cg.sol(sol_a, sol_b) + cg.ligne(O, Tp, "rail") + cg.ligne(*rail2, "fin") +
            cg.poly([cg.add(Gp, cg.add(cg.mul(d, -9), cg.mul(nrm, -8))), cg.add(Gp, cg.add(cg.mul(d, 9), cg.mul(nrm, -8))),
                     cg.add(Gp, cg.add(cg.mul(d, 11), cg.mul(nrm, 9))), cg.add(Gp, cg.add(cg.mul(d, -11), cg.mul(nrm, 9)))],
                    "mb", True) +
            cg.arc_angle(O, 14, 0, 70, "70°") + cg.point(O, "O", (-3, 5)) + cg.point(Tp, "T", (3, -1)) +
            cg.point(Gp, "G", (3, 4)) + cg.fleche(Gp, Vt) + cg.nom_vecteur((Vt[0] + 5, Vt[1] + 4), "V", "", ancre="start") +
            cg.fleche(Gp, Pt) + cg.nom_vecteur((Pt[0] + 3, Pt[1] - 3), "P", "", ancre="start") +
            cg.texte((120, 20), "rail de guidage incliné à 70°", "tc", "start") +
            cg.texte((120, 26), "V = 0,3 m/s ; P = 300 daN", "tc", "start"))
    Vv = 0.3 * math.sin(a)
    tipv = (Gp[0], Gp[1] - Vv / 0.005)
    H = (O[0], Tp[1])
    corr = (cg.ligne((Gp[0], 4), (Gp[0], 164), "axe") + cg.ligne(Vt, tipv, "fin") + cg.fleche(Gp, tipv) +
            cg.nom_vecteur((Gp[0] - 3, tipv[1] + 18), "V", "v", ancre="end") +
            cg.ligne((O[0], 4), (O[0], 164), "axe") + cg.ligne(Tp, H, "fin") + cg.point(H, "H", (-3, -1)) +
            cg.cote(O, H, f"h ≈ {fr(150 * math.sin(a) * 0.1, 1)} m", 12))
    return cg.planche(
        "skip", 205, 178, fond, points={"O": O, "T": Tp, "G": Gp},
        lignes=[{"a": sol_a, "b": sol_b, "inf": True, "nom": "sol"}, {"a": O, "b": Tp, "nom": "rail"}],
        vecteurs=[{"a": Gp, "b": Vt, "nom": "V"}, {"a": Gp, "b": Pt, "nom": "P"}],
        echelles={"L": (0.1, "m", 1), "V": (0.005, "m/s", 3), "F": (50, "N", 0)},
        attendus=[{"type": "vnorme", "en": "G"}, {"type": "vangle", "en": "G", "ref": 90},
                  {"type": "point", "nom": "H", "x": H[0], "y": H[1]}],
        corr=corr, aria="Rail incliné à 70° de O à T, wagonnet en G, vitesse V le long du rail et poids P vertical",
        legende="Le sol est horizontal ; la verticale lui est perpendiculaire."), Vv, 150 * math.sin(a) * 0.1, \
        [{"t": "vec", "a": Gp, "b": tipv}, {"t": "pt", "p": H, "nom": "H"}]


PL_SKIP, VV1, H1, _sol = planche_skip()
PL_SKIP["solution"] = _sol
W1 = 3000 * H1
Pp1 = -3000 * VV1
Pm1 = -Pp1 / 0.7
G1 = [
    partie("Projections : vitesse verticale et dénivellation", 16, [
        '<div class="cours-split"><div>'
        "<p>Un skip de chargement effectue le levage d'un wagonnet le long d'un rail incliné de 70° par rapport à "
        "l'horizontale. Le poids de l'ensemble est de 300 daN, la distance parcourue sur le rail est de 15 m, la vitesse "
        "du wagonnet est de 0,3 m/s.</p><p>La puissance du poids est le produit scalaire " + vec("P") + "·" + vec("V") +
        " : seule compte la composante verticale de la vitesse. De même, le travail du poids ne dépend que de la "
        "dénivellation. On construit ces deux projections sur la planche, à l'échelle.</p></div>" +
        fig(fg.fig_skip, "Figure 1 — Wagonnet de levage.", "Wagonnet sur un rail incliné à 70°, poids 300 daN, vitesse "
            "0,3 m/s, 15 m de rail", 360) + "</div>"], [
        QBAR(["DT2"], "sur la planche"),
        CG("Sur la planche : trace la verticale passant par G, projette l'extrémité de " + vec("V") + " sur cette "
           "verticale et trace depuis G le vecteur " + vec("V") + "<sub>v</sub>, composante verticale de la vitesse. "
           "Construis ensuite le projeté H du point T sur la verticale passant par O, et nomme-le H.",
           "Outils : Perpendiculaire (au sol, passant par G puis par O), Projeté, Vecteur, Nommer.",
           PL_SKIP,
           [("Vecteur tracé en G : norme", num(VV1, None, rel=0.04), f"{fr(VV1, 3)} m/s"),
            ("Vecteur tracé en G : direction", num(90, None, abs_=3), "verticale, vers le haut (90°)"),
            ("Point H, projeté de T sur la verticale de O", num(0, None, abs_=2), "H à la verticale de O, au niveau de T")],
           "<p>Le produit scalaire se construit par projection orthogonale : la composante verticale de " + vec("V") +
           " a pour norme <i>V</i>·cos 20° = <i>V</i>·sin 70° = 0,3 × 0,940 ≈ " + fr(VV1, 3) + " m/s, soit " +
           fr(VV1 / 0.005, 1) + " mm à l'échelle. La dénivellation est la projection verticale de OT : <i>h</i> = 15 × sin 70° "
           "≈ " + fr(H1, 2) + " m.</p>"),
        Q("Lis la composante verticale <i>V</i><sub>v</sub> de la vitesse du wagonnet.", H_LU, num(VV1, "m/s", rel=0.04),
          f"<i>V</i><sub>v</sub> ≈ {fr(VV1, 3)} m/s",
          eq(f"<i>V</i><sub>v</sub> = <i>V</i>·sin 70° = 0,3 × {fr(math.sin(math.radians(70)), 3)} ≈ {fr(VV1, 3)} m/s")),
        Q("Lis la dénivellation <i>h</i> = OH parcourue par le wagonnet.", H_LU, num(H1, "m", rel=0.03),
          f"<i>h</i> ≈ {fr(H1, 2)} m",
          "<p>Outil Mesurer entre O et H : la longueur lue est convertie avec l'échelle des longueurs (1 mm ↔ 0,1 m).</p>" +
          eq(f"<i>h</i> = 15 × sin 70° ≈ {fr(H1, 2)} m")),
    ]),
    partie("Énergie et puissance du levage", 10, [
        "<p>On utilise les grandeurs construites dans la partie 1. Le rendement de l'appareil est de 0,7.</p>"], [
        QBAR(["DT1", "DT2"]),
        Q("Calcule l'énergie <i>W</i> dépensée pour le levage (travail contre le poids).", H_NUM,
          num(W1 / 1000, "kJ", rel=0.03), f"<i>W</i> ≈ {fr(W1 / 1000, 1)} kJ",
          eq(f"<i>W</i> = <i>P</i>·<i>h</i> = 3 000 × {fr(H1, 2)} ≈ {fr(W1, 0)} J ≈ {fr(W1 / 1000, 1)} kJ")),
        Q("Calcule la puissance développée par le poids, avec son signe.", H_NUM, num(Pp1, "W", rel=0.04),
          f"{vec('P')}·{vec('V')} ≈ {fr(Pp1, 0)} W",
          eq(f"{vec('P')}·{vec('V')} = −<i>P</i>·<i>V</i><sub>v</sub> = −3 000 × {fr(VV1, 3)} ≈ {fr(Pp1, 0)} W") +
          "<p>Le poids est opposé à la composante verticale de la vitesse : sa puissance est négative (résistante).</p>"),
        Q("Calcule la puissance du moteur à adopter.", H_NUM, num(Pm1 / 1000, "kW", rel=0.04),
          f"<i>P</i><sub>m</sub> ≈ {fr(Pm1 / 1000, 2)} kW",
          eq(f"<i>P</i><sub>m</sub> = {frac(fr(-Pp1, 0), '0,7')} ≈ {fr(Pm1, 0)} W ≈ {fr(Pm1 / 1000, 2)} kW")),
    ]),
]


# ---------- G2 — roues dentées : répartition linéaire et roulement sans glissement
def planche_roues():
    e = 0.004  # 1 mm ↔ 4 mm
    A = (55.0, 112.0)
    rA, rB = 0.150 / e, 0.375 / e
    I = (A[0] + rA, A[1])
    B = (I[0] + rB, A[1])
    M = (A[0] + 0.075 / e, A[1])
    Nn = (B[0] - 0.300 / e, A[1])
    wA = tr_min(900)
    wB = wA * 0.150 / 0.375
    kv = 0.2
    VM = wA * 0.075
    VI = wA * 0.150
    VN = wB * 0.300
    tM = (M[0], M[1] - VM / kv)
    tI = (I[0], I[1] - VI / kv)
    tN = (Nn[0], Nn[1] - VN / kv)
    fond = (cg.cercle(A, rA, "mf") + cg.cercle(B, rB, "mf") + cg.ligne((A[0] - 12, A[1]), (B[0] + 12, B[1]), "axe") +
            cg.articulation(A) + cg.articulation(B) + cg.point(A, "A", (-3, 6)) + cg.point(B, "B", (3, 6)) +
            cg.point(I, "I", (2, 6)) + cg.point(M, "M", (-2, 6)) + cg.point(Nn, "N", (2, 6)) +
            cg.fleche(M, tM) + cg.nom_vecteur((M[0] - 3, tM[1] + 10), "V", "M", ancre="end") +
            cg.texte((A[0] - 30, A[1] - rA - 6), "roue A (r = 150 mm)", "tc", "start") +
            cg.texte((B[0] - 20, B[1] - rB - 4), "roue B (r = 375 mm)", "tc", "start") +
            cg.texte((8, 200), "AM = 75 mm ; BN = 300 mm (rayon de giration de B)", "tc", "start"))
    corr = (cg.ligne(A, cg.add(A, cg.mul(cg.sub(tI, A), 1.12)), "axe") + cg.ligne((I[0], I[1]), (I[0], tI[1] - 6), "fin") +
            cg.fleche(I, tI) + cg.nom_vecteur((I[0] + 3, tI[1] + 8), "V", "I", ancre="start") +
            cg.ligne(B, cg.add(B, cg.mul(cg.sub(tI, B), 1.08)), "axe") + cg.ligne((Nn[0], Nn[1]), (Nn[0], tN[1] - 6), "fin") +
            cg.fleche(Nn, tN) + cg.nom_vecteur((Nn[0] + 3, tN[1] + 8), "V", "N", ancre="start"))
    cfg = cg.planche(
        "roues", 290, 210, fond, points={"A": A, "B": B, "I": I, "M": M, "N": Nn},
        lignes=[{"a": A, "b": B, "nom": "ligne des centres"}], vecteurs=[{"a": M, "b": tM, "nom": "VM"}],
        cercles=[{"c": A, "r": rA}, {"c": B, "r": rB}],
        echelles={"L": (e, "m", 3), "V": (kv, "m/s", 1)},
        attendus=[{"type": "vnorme", "en": "I"}, {"type": "vangle", "en": "I", "ref": 90},
                  {"type": "vnorme", "en": "N"}, {"type": "vangle", "en": "N", "ref": 90}],
        corr=corr, aria="Deux roues dentées tangentes en I, de centres A et B ; vitesse du point M de la roue A donnée",
        legende="Cercles primitifs des deux roues ; la roue A tourne à 900 tr/min à l'instant considéré.")
    cfg["solution"] = [{"t": "vec", "a": I, "b": tI}, {"t": "vec", "a": Nn, "b": tN}]
    return cfg, VI, VN, wB


PL_ROUES, VI2, VN2, WB2 = planche_roues()
JA2, JB2 = 4 * 0.12 ** 2, 12 * 0.3 ** 2
wA2 = tr_min(900)
Ec2 = 0.5 * JA2 * wA2 ** 2 + 0.5 * JB2 * WB2 ** 2
thA2 = Ec2 / 10
tours2 = thA2 / (2 * PI)
EcB2 = 0.5 * JB2 * WB2 ** 2
Ft2 = EcB2 / (0.375 * thA2 * 0.4)
G2 = [
    partie("Vitesses au contact des deux roues", 15, [
        '<div class="cours-split"><div>'
        "<p>Une roue dentée A transmet son mouvement à une roue B. Les cercles primitifs roulent sans glisser l'un sur "
        "l'autre au point I. À l'instant étudié, la roue A tourne à 900 tr/min : la vitesse du point M de la roue A "
        "est tracée sur la planche.</p>" +
        donnees("roue A : rayon primitif <i>r</i><sub>A</sub> = 150 mm", "roue B : rayon primitif <i>r</i><sub>B</sub> = 375 mm",
                "M : point de la roue A à 75 mm de son axe ; N : point de la roue B à 300 mm de son axe") +
        "</div>" + fig(fg.fig_roues, "Figure 1 — Roues dentées.", "Roue dentée A entraînée par un couple CA, engrenant "
                       "avec une roue B plus grande", 380) + "</div>"], [
        QBAR(["DT2"], "sur la planche"),
        CG("Sur la planche : construis la vitesse " + vec("V") + "<sub>I</sub> du point I de la roue A (répartition "
           "linéaire des vitesses sur la roue A), puis, la roue B ayant la même vitesse en I, la vitesse " + vec("V") +
           "<sub>N</sub> du point N de la roue B.",
           "Outils : Droite (du centre par l'extrémité d'une vitesse), Perpendiculaire, Vecteur.",
           PL_ROUES,
           [("Vecteur tracé en I : norme", num(VI2, None, rel=0.04), f"{fr(VI2, 2)} m/s"),
            ("Vecteur tracé en I : direction", num(90, None, abs_=3), "perpendiculaire à AB, vers le haut (90°)"),
            ("Vecteur tracé en N : norme", num(VN2, None, rel=0.04), f"{fr(VN2, 2)} m/s"),
            ("Vecteur tracé en N : direction", num(90, None, abs_=3), "perpendiculaire à AB, vers le haut (90°)")],
           "<p>Roue A en rotation autour de A : les extrémités des vitesses des points du rayon AI sont alignées avec A. "
           "La droite issue de A passant par l'extrémité de " + vec("V") + "<sub>M</sub> coupe la perpendiculaire à AB "
           "en I à l'extrémité de " + vec("V") + f"<sub>I</sub> : <i>V</i><sub>I</sub> = 2·<i>V</i><sub>M</sub> ≈ {fr(VI2, 2)} m/s "
           "(I est deux fois plus loin de A que M).</p><p>Roulement sans glissement : la roue B a la même vitesse en I. "
           "La droite issue de B passant par l'extrémité de " + vec("V") + "<sub>I</sub> donne " + vec("V") +
           f"<sub>N</sub> : <i>V</i><sub>N</sub> = <i>V</i><sub>I</sub> × 300/375 ≈ {fr(VN2, 2)} m/s.</p>"),
        Q("Lis la vitesse <i>V</i><sub>I</sub> du point de contact.", H_LU, num(VI2, "m/s", rel=0.04),
          f"<i>V</i><sub>I</sub> ≈ {fr(VI2, 1)} m/s",
          eq(f"<i>V</i><sub>I</sub> = ω<sub>A</sub>·<i>r</i><sub>A</sub> = {fr(wA2, 2)} × 0,15 ≈ {fr(VI2, 2)} m/s")),
        Q("Déduis-en la vitesse angulaire ω<sub>B</sub> de la roue B.", H_LU, num(WB2, "rad/s", rel=0.04),
          f"ω<sub>B</sub> ≈ {fr(WB2, 1)} rad/s",
          eq(f"ω<sub>B</sub> = {frac('<i>V</i><sub>I</sub>', '<i>r</i><sub>B</sub>')} = {frac(fr(VI2, 2), '0,375')} ≈ {fr(WB2, 1)} rad/s (soit 360 tr/min)")),
        Q("Calcule le rapport ω<sub>B</sub> / ω<sub>A</sub>.", H_SANS, num(0.4, None, rel=0.03), "0,4",
          eq(f"{frac('ω<sub>B</sub>', 'ω<sub>A</sub>')} = {frac('<i>r</i><sub>A</sub>', '<i>r</i><sub>B</sub>')} = {frac('150', '375')} = 0,4")),
    ]),
    partie("Mise en vitesse : théorème de l'énergie cinétique", 20, [
        "<p>L'ensemble est à l'arrêt lorsqu'un couple constant <i>C</i><sub>A</sub> = 10 N·m est appliqué à la roue A. "
        "Les frottements sont négligés. On cherche le nombre de tours de la roue A avant qu'elle n'atteigne 900 tr/min, "
        "puis l'effort tangentiel entre les deux roues.</p>" +
        donnees("roue A : masse 4 kg, rayon de giration 120 mm", "roue B : masse 12 kg, rayon de giration 300 mm",
                "couple moteur appliqué à A : <i>C</i><sub>A</sub> = 10 N·m")], [
        QBAR(["DT1"]),
        Q("Calcule le moment d'inertie <i>J</i><sub>A</sub> de la roue A.", H_NUM, num(JA2, "kg·m²"),
          f"<i>J</i><sub>A</sub> = {fr(JA2, 4)} kg·m²", eq("<i>J</i><sub>A</sub> = <i>m</i>·<i>k</i>² = 4 × 0,12² = 0,0576 kg·m²")),
        Q("Calcule le moment d'inertie <i>J</i><sub>B</sub> de la roue B.", H_NUM, num(JB2, "kg·m²"),
          f"<i>J</i><sub>B</sub> = {fr(JB2, 2)} kg·m²", eq("<i>J</i><sub>B</sub> = 12 × 0,3² = 1,08 kg·m²")),
        Q("Calcule l'énergie cinétique de l'ensemble quand A tourne à 900 tr/min.", H_NUM, num(Ec2, "J"),
          f"<i>E</i><sub>c</sub> ≈ {fr(Ec2, 0)} J",
          eq(f"<i>E</i><sub>c</sub> = ½·<i>J</i><sub>A</sub>·ω<sub>A</sub>² + ½·<i>J</i><sub>B</sub>·ω<sub>B</sub>² = "
             f"½ × 0,0576 × {fr(wA2, 2)}² + ½ × 1,08 × {fr(WB2, 2)}² ≈ {fr(Ec2, 0)} J") +
          f"<p>La grande roue, plus lente, emporte pourtant les trois quarts de l'énergie ({fr(EcB2, 0)} J).</p>"),
        Q("Combien de tours la roue A fait-elle avant d'atteindre 900 tr/min ?", H_NUM, num(tours2, "tours"),
          f"≈ {fr(tours2, 1)} tours",
          "<p>Théorème de l'énergie cinétique appliqué à l'ensemble des deux roues : seul le couple <i>C</i><sub>A</sub> "
          "travaille (les actions mutuelles des dentures se compensent, sans frottement).</p>" +
          eq(f"<i>E</i><sub>c</sub> − 0 = <i>C</i><sub>A</sub>·θ<sub>A</sub> ⇒ θ<sub>A</sub> = {frac(fr(Ec2, 0), '10')} ≈ {fr(thA2, 1)} rad ≈ {fr(tours2, 1)} tours")),
        Q("Calcule l'effort tangentiel <i>F</i><sub>T</sub> exercé entre les deux roues.", H_NUM, num(Ft2, "N"),
          f"<i>F</i><sub>T</sub> ≈ {fr(Ft2, 0)} N",
          "<p>Théorème appliqué à la roue B seule : l'effort tangentiel de A sur B, au rayon <i>r</i><sub>B</sub>, est "
          "le seul effort qui travaille.</p>" +
          eq(f"θ<sub>B</sub> = 0,4 × θ<sub>A</sub> ≈ {fr(thA2 * 0.4, 2)} rad ; "
             f"<i>F</i><sub>T</sub>·<i>r</i><sub>B</sub>·θ<sub>B</sub> = ½·<i>J</i><sub>B</sub>·ω<sub>B</sub>²",
             f"<i>F</i><sub>T</sub> = {frac(fr(EcB2, 1), '0,375 × ' + fr(thA2 * 0.4, 2))} ≈ {fr(Ft2, 0)} N")),
    ]),
]


# ---------- G3 — levage de balancier : rotation autour d'un axe fixe
def planche_balancier():
    e = 0.02  # 1 mm ↔ 20 mm
    A = (25.0, 92.0)
    B = (A[0] + 1 / e, A[1])
    Gp = (A[0] + 2 / e, A[1])
    E = (A[0] + 4 / e, A[1])
    kv = 0.01
    tB = (B[0], B[1] + 0.3 / kv)
    tG = (Gp[0], Gp[1] + 0.6 / kv)
    h2 = 0.35 / e
    fond = (cg.poly([(A[0], A[1] - h2), (E[0], E[1] - h2), (E[0], E[1] + h2), (A[0], A[1] + h2)], "mf", True) +
            cg.ligne((A[0] - 6, A[1]), (E[0] + 8, E[1]), "axe") + cg.pivot_fixe(A) +
            cg.poly([(B[0] - 7, 8), (B[0] + 7, 8), (B[0] + 7, 46), (B[0] - 7, 46)], "mb", True) +
            cg.ligne((B[0], 46), (B[0], A[1] - h2), "m") + cg.articulation(B) +
            cg.point(A, "A", (-4, -3)) + cg.point(B, "B", (3, -3)) + cg.point(Gp, "G", (3, -3)) + cg.point(E, "E", (3, -3)) +
            cg.fleche(B, tB) + cg.nom_vecteur((B[0] + 3, tB[1] - 4), "V", "B", ancre="start") +
            cg.texte((B[0] + 10, 20), "vérin (tige articulée en B)", "tc", "start") +
            cg.cote(A, B, "1 m", -24) + cg.cote(B, Gp, "1 m", -24) + cg.cote(Gp, E, "2 m", -24))
    corr = (cg.ligne(A, cg.add(A, cg.mul(cg.sub(tG, A), 1.15)), "axe") + cg.ligne(Gp, (Gp[0], tG[1] + 6), "fin") +
            cg.fleche(Gp, tG) + cg.nom_vecteur((Gp[0] + 3, tG[1] - 4), "V", "G", ancre="start"))
    cfg = cg.planche(
        "balancier", 245, 170, fond, points={"A": A, "B": B, "G": Gp, "E": E},
        lignes=[{"a": A, "b": E, "nom": "balancier"}], vecteurs=[{"a": B, "b": tB, "nom": "VB"}],
        echelles={"L": (e, "m", 2), "V": (kv, "m/s", 2)},
        attendus=[{"type": "vnorme", "en": "G"}, {"type": "vangle", "en": "G", "ref": -90}],
        corr=corr, aria="Balancier horizontal articulé en A, tige de vérin en B, centre de gravité G, extrémité E",
        legende="Le balancier est horizontal à l'instant étudié ; il tourne autour de A.")
    cfg["solution"] = [{"t": "vec", "a": Gp, "b": tG}]
    return cfg


PL_BAL = planche_balancier()
m3 = 50000 / G
JG3 = m3 * (4 ** 2 + 0.7 ** 2) / 12
JA3 = JG3 + m3 * 2 ** 2
w3 = 0.3
Ec3 = 0.5 * JA3 * w3 ** 2
Wp3 = 50000 * 2 * 0.04
Fs3 = 50000 * 2
F3 = (Ec3 + Wp3) / 0.04 - Fs3
S3 = PI / 4 * (200 ** 2 - 140 ** 2)
p3 = (Fs3 + F3) / S3
G3 = [
    partie("Vitesses du balancier", 15, [
        '<div class="cours-split"><div>'
        "<p>Le dispositif de levage de l'activité A8 manœuvre maintenant un balancier, articulé en A sur le bâti. La "
        "tige du vérin, articulée en B, descend à la vitesse de 0,3 m/s ; le balancier tourne autour de A. Son poids, "
        "5 000 daN, s'applique en son centre de gravité G.</p>" +
        donnees("AB = 1 m ; AG = 2 m ; longueur du balancier AE = 4 m",
                "vitesse de la tige en B : <i>V</i><sub>B</sub> = 0,3 m/s, verticale, vers le bas") +
        "</div>" + fig(fg.fig_balancier, "Figure 1 — Levage de balancier.", "Vérin vertical relié en B à un balancier "
                       "horizontal articulé en A, poids de 5 000 daN", 380) + "</div>"], [
        QBAR(["DT2"], "sur la planche"),
        CG("Sur la planche : construis la vitesse " + vec("V") + "<sub>G</sub> du centre de gravité G du balancier "
           "(triangle des vitesses).", "Outils : Droite (de A par l'extrémité de " + vec("V") + "<sub>B</sub>), "
           "Perpendiculaire, Vecteur.", PL_BAL,
           [("Vecteur tracé en G : norme", num(0.6, None, rel=0.04), "0,60 m/s"),
            ("Vecteur tracé en G : direction", num(-90, None, abs_=3), "verticale, vers le bas (−90°)")],
           "<p>Le balancier tourne autour de A : les extrémités des vitesses des points de AE sont alignées avec A. La "
           "droite issue de A passant par l'extrémité de " + vec("V") + "<sub>B</sub> coupe la verticale de G à "
           "l'extrémité de " + vec("V") + "<sub>G</sub> : AG = 2·AB, donc <i>V</i><sub>G</sub> = 2·<i>V</i><sub>B</sub> = 0,6 m/s.</p>"),
        Q("Lis la vitesse <i>V</i><sub>G</sub> du centre de gravité.", H_LU, num(0.6, "m/s", rel=0.04),
          "<i>V</i><sub>G</sub> = 0,6 m/s", eq("<i>V</i><sub>G</sub> = <i>V</i><sub>B</sub> × AG/AB = 0,3 × 2 = 0,6 m/s")),
        Q("Calcule la vitesse angulaire ω du balancier.", H_NUM, num(0.3, "rad/s"), "ω = 0,3 rad/s",
          eq("ω = <i>V</i><sub>B</sub> / AB = 0,3 / 1 = 0,3 rad/s")),
        Q("La descente est uniforme : calcule l'effort <i>F</i><sub>s</sub> de la tige qui retient le balancier.",
          "Avec son unité ; tolérance de 2 %. Pense aux puissances : à vitesse constante, leur somme est nulle.",
          num(Fs3 / 1000, "kN"), f"<i>F</i><sub>s</sub> = {fr(Fs3 / 1000, 0)} kN",
          "<p>Énergie cinétique constante : la somme des puissances est nulle. Le poids (moteur) et la tige (résistante) "
          "ont des puissances opposées.</p>" +
          eq("<i>F</i><sub>s</sub>·<i>V</i><sub>B</sub> = <i>P</i>·<i>V</i><sub>G</sub> ⇒ "
             f"<i>F</i><sub>s</sub> = 50 000 × {frac('0,6', '0,3')} = {fr(Fs3, 0)} N") +
          "<p>Le rapport des efforts est l'inverse du rapport des vitesses, lu sur la construction.</p>"),
    ]),
    partie("Amortissement en fin de course", 25, [
        "<p>L'arrêt est obtenu, comme dans l'activité A8, par une valve de décélération, ici sur une course de tige "
        "<i>L</i> = 40 mm. Le balancier est assimilé à un parallélépipède de 4 × 0,7 × 0,7 m. Le vérin travaille en "
        "tirant ; l'effort de décélération <i>F</i> s'ajoute à l'effort <i>F</i><sub>s</sub> de la descente uniforme. "
        "La rotation pendant l'amortissement est petite : on assimile les déplacements de B et de G à des arcs.</p>" +
        donnees("poids du balancier : 5 000 daN = 50 000 N, en G (AG = 2 m)", "course d'amortissement : <i>L</i> = 40 mm",
                "diamètre de la tige : 140 mm ; diamètre de l'alésage : 200 mm")], [
        QBAR(["DT1"]),
        Q("Calcule la masse <i>m</i> du balancier.", H_NUM, num(m3, "kg"), f"<i>m</i> ≈ {fr(m3, 0)} kg",
          eq(f"<i>m</i> = 50 000 / 9,81 ≈ {fr(m3, 0)} kg")),
        Q("Calcule le moment d'inertie <i>J</i><sub>A</sub> du balancier par rapport à son axe de rotation A.", H_NUM,
          num(JA3, "kg·m²"), f"<i>J</i><sub>A</sub> ≈ {fr(JA3, 0)} kg·m²",
          eq(f"<i>J</i><sub>G</sub> = <i>m</i>·{frac('<i>a</i>² + <i>b</i>²', '12')} = {fr(m3, 0)} × {frac('4² + 0,7²', '12')} ≈ {fr(JG3, 0)} kg·m²",
             f"<i>J</i><sub>A</sub> = <i>J</i><sub>G</sub> + <i>m</i>·AG² = {fr(JG3, 0)} + {fr(m3, 0)} × 2² ≈ {fr(JA3, 0)} kg·m²")),
        Q("Calcule l'énergie cinétique <i>E</i><sub>c</sub> du balancier pendant la descente uniforme.", H_NUM,
          num(Ec3, "J"), f"<i>E</i><sub>c</sub> ≈ {fr(Ec3, 0)} J",
          eq(f"<i>E</i><sub>c</sub> = ½·<i>J</i><sub>A</sub>·ω² = ½ × {fr(JA3, 0)} × 0,3² ≈ {fr(Ec3, 0)} J")),
        Q("Calcule le travail <i>W</i><sub>P</sub> du poids pendant l'amortissement.", H_NUM, num(Wp3, "J"),
          "<i>W</i><sub>P</sub> = 4 000 J",
          "<p>B descend de 40 mm : le balancier tourne de Δθ = 0,04 / 1 = 0,04 rad et G descend de 2 × 0,04 = 0,08 m "
          "(la répartition linéaire vaut aussi pour les déplacements).</p>" +
          eq("<i>W</i><sub>P</sub> = <i>P</i> × 0,08 = 50 000 × 0,08 = 4 000 J")),
        Q("Calcule l'effort de décélération <i>F</i>, supposé constant.", H_NUM, num(F3 / 1000, "kN"),
          f"<i>F</i> ≈ {fr(F3 / 1000, 1)} kN",
          eq("0 − <i>E</i><sub>c</sub> = <i>W</i><sub>P</sub> − (<i>F</i><sub>s</sub> + <i>F</i>)·<i>L</i>",
             f"<i>F</i><sub>s</sub> + <i>F</i> = {frac(fr(Ec3, 0) + ' + 4 000', '0,04')} ≈ {fr(Fs3 + F3, 0)} N ⇒ "
             f"<i>F</i> ≈ {fr(Fs3 + F3, 0)} − 100 000 ≈ {fr(F3, 0)} N") +
          "<p>Le travail du poids pendant l'amortissement est compensé par <i>F</i><sub>s</sub>·<i>L</i> : "
          "l'effort supplémentaire <i>F</i> n'absorbe que l'énergie cinétique, <i>F</i> = <i>E</i><sub>c</sub> / <i>L</i>.</p>"),
        Q("Calcule la section annulaire <i>S</i> du vérin.", H_NUM, num(S3, "mm²"), f"<i>S</i> ≈ {fr(S3, 0)} mm²",
          eq(f"<i>S</i> = {frac('π', '4')} × (200² − 140²) ≈ {fr(S3, 0)} mm²")),
        Q("Calcule la pression maximale <i>p</i> dans le vérin, en bar.", H_NUM, num(p3 * 10, "bar"),
          f"<i>p</i> ≈ {fr(p3 * 10, 1)} bar",
          eq(f"<i>p</i> = {frac(fr(Fs3 + F3, 0) + ' N', fr(S3, 0) + ' mm²')} ≈ {fr(p3, 2)} MPa ≈ {fr(p3 * 10, 1)} bar")),
    ]),
]


# ---------- G4 — tire-bouchon : centres instantanés de rotation et puissances virtuelles
def planche_tirebouchon():
    x0, y0, u, yv, c = 30.0, 112.0, 16.0, 16.0, 7.0
    x1 = u * (yv - c) / yv
    P = {"C1": (x0, y0 - c), "C2": (x0, y0 + c)}
    xs = [x0 + x1 + k * u for k in range(6)]
    P.update({"P1": (xs[0], y0 - yv), "Q1": (xs[0], y0 + yv), "D": (xs[1], y0), "P2": (xs[2], y0 - yv),
              "Q2": (xs[2], y0 + yv), "E": (xs[3], y0), "P3": (xs[4], y0 - yv), "Q3": (xs[4], y0 + yv), "H": (xs[5], y0)})
    Ah = (P["H"][0] + 22, y0)
    kv = 1.0  # 1 mm ↔ 1 mm/s
    VD = (15.0, 0.0)
    # barre P1-D-Q2 : I1 sur (C1P1) et sur la verticale de D
    I1 = cg.inter(P["C1"], cg.sub(P["P1"], P["C1"]), P["D"], (0, 1))
    w1 = -VD[0] / (P["D"][1] - I1[1])  # V_M = w·perp(M − I), perp(a) = (−a_y, a_x)

    def vit(w, Ic, M):
        return (w * -(M[1] - Ic[1]), w * (M[0] - Ic[0]))
    VQ2 = vit(w1, I1, P["Q2"])
    I2 = cg.inter(I1, cg.sub(P["Q2"], I1), P["E"], (0, 1))
    w2 = VQ2[0] / -(P["Q2"][1] - I2[1])
    VP3 = vit(w2, I2, P["P3"])
    I3 = cg.inter(I2, cg.sub(P["P3"], I2), P["H"], (0, 1))
    w3_ = VP3[0] / -(P["P3"][1] - I3[1])
    VH = vit(w3_, I3, P["H"])
    tip = lambda M, Vv: cg.add(M, Vv)
    fond = cg.poly([(6, y0 - 4), (x0 - 4, y0 - 4), (x0 - 4, y0 + 4), (6, y0 + 4)], "mb", True)
    fond += cg.poly([(x0 - 6, y0 - c - 6), (x0 + 3, y0 - c - 6), (x0 + 3, y0 + c + 6), (x0 - 6, y0 + c + 6)], "mf", True)
    fond += cg.ligne((x0 - 6, y0 - 4), (P["D"][0], y0 - 1.5), "fin") + cg.ligne((x0 - 6, y0 + 4), (P["D"][0], y0 + 1.5), "fin")
    for a, b in [("C1", "P1"), ("C2", "Q1"), ("P1", "Q2"), ("Q1", "P2"), ("P2", "Q3"), ("Q2", "P3"), ("P3", "H"), ("Q3", "H")]:
        fond += cg.ligne(P[a], P[b], "m")
    fond += cg.ligne(P["H"], Ah, "m") + cg.ligne((Ah[0], y0 - 14), (Ah[0], y0 + 14), "m")
    fond += cg.ligne((4, y0), (Ah[0] + 70, y0), "axe")
    for k, pos in [("C1", (-3, -2)), ("C2", (-3, 6)), ("P1", (-1, -3)), ("Q1", (-1, 6)), ("D", (1.5, -3)),
                   ("P2", (0, -3)), ("Q2", (0, 6)), ("E", (1.5, -3)), ("P3", (0, -3)), ("Q3", (0, 6)), ("H", (1.5, -3))]:
        fond += cg.articulation(P[k], 1.1) + cg.point(P[k], k, pos)
    fond += cg.point(Ah, "A", (2, -3))
    fond += cg.fleche(P["D"], tip(P["D"], VD)) + cg.nom_vecteur((P["D"][0] + 6, y0 + 7), "V", "D", ancre="start")
    fond += cg.texte((6, y0 - 9), "vis", "tc", "start") + cg.texte((4, y0 + c + 14), "collier (fixe)", "tc", "start")
    fond += cg.texte((Ah[0] + 4, y0 + 22), "poignée", "tc", "start")

    def tri(Ic, M, Vv):  # correction : rayon IM, vitesse perpendiculaire
        return cg.ligne(Ic, M, "fin") + cg.fleche(M, tip(M, Vv))
    corr = (cg.ligne(P["C1"], I1, "axe") + cg.ligne((P["D"][0], 4), (P["D"][0], 206), "axe") + cg.point(I1, "I1", (2, -2)) +
            cg.ligne(I1, I2, "axe") + cg.ligne((P["E"][0], 4), (P["E"][0], 206), "axe") + cg.point(I2, "I2", (2, 4)) +
            cg.ligne(I2, I3, "axe") + cg.ligne((P["H"][0], 4), (P["H"][0], 206), "axe") + cg.point(I3, "I3", (2, -2)) +
            tri(I1, P["Q2"], VQ2) + tri(I2, P["P3"], VP3) + tri(I3, P["H"], VH) +
            cg.nom_vecteur((P["Q2"][0] + 8, P["Q2"][1] + 8), "V", "Q2", ancre="start") +
            cg.nom_vecteur((P["P3"][0] + 10, P["P3"][1] - 12), "V", "P3", ancre="start") +
            cg.nom_vecteur((P["H"][0] + 30, y0 + 8), "V", "H", ancre="start"))
    pts = dict(P)
    pts["A"] = Ah
    cfg = cg.planche(
        "tirebouchon", 230, 210, fond, points=pts,
        lignes=[{"a": P[a], "b": P[b], "nom": a + b} for a, b in
                [("C1", "P1"), ("C2", "Q1"), ("P1", "Q2"), ("Q1", "P2"), ("P2", "Q3"), ("Q2", "P3"), ("P3", "H"), ("Q3", "H")]] +
               [{"a": (4, y0), "b": (Ah[0] + 70, y0), "inf": True, "nom": "axe"}],
        vecteurs=[{"a": P["D"], "b": tip(P["D"], VD), "nom": "VD"}],
        echelles={"L": (1, "mm", 0), "V": (kv, "mm/s", 0)},
        attendus=[{"type": "point", "nom": "I1", "x": I1[0], "y": I1[1]}, {"type": "vnorme", "en": "Q2"},
                  {"type": "point", "nom": "I2", "x": I2[0], "y": I2[1]}, {"type": "vnorme", "en": "P3"},
                  {"type": "point", "nom": "I3", "x": I3[0], "y": I3[1]}, {"type": "vnorme", "en": "H"},
                  {"type": "vangle", "en": "H", "ref": 0}],
        corr=corr, aria="Pantographe du tire-bouchon : collier fixe C1 C2, barres articulées, croisements D et E sur l'axe, "
                        "poignée articulée en H",
        legende="Par symétrie, les articulations D, E et H, sur l'axe, se déplacent le long de l'axe.")
    cfg["solution"] = [{"t": "pt", "p": I1, "nom": "I1"}, {"t": "pt", "p": I2, "nom": "I2"}, {"t": "pt", "p": I3, "nom": "I3"},
                       {"t": "vec", "a": P["Q2"], "b": tip(P["Q2"], VQ2)}, {"t": "vec", "a": P["P3"], "b": tip(P["P3"], VP3)},
                       {"t": "vec", "a": P["H"], "b": tip(P["H"], VH)}]
    return cfg, I1, I2, I3, cg.norme(VQ2), cg.norme(VP3), cg.norme(VH)


PL_TB, I1g, I2g, I3g, VQ2g, VP3g, VHg = planche_tirebouchon()
F4 = 120
G4 = [
    partie("Vitesses du pantographe : centres instantanés de rotation", 28, [
        '<div class="cours-split"><div>'
        "<p>Un tire-bouchon est réalisé à partir d'un système de barres articulées (pivots) entre elles et d'une tige "
        "filetée articulée en D sur les barres. Le collier repose sur la bouteille : il est fixe. L'opérateur tire sur "
        "la poignée (effort " + vec("F") + " en A) ; le bouchon retient la tige (effort " + vec("T") + ").</p>"
        "<p>On donne une vitesse (virtuelle) de D, " + vec("V") + "<sub>D</sub> = 15 mm/s, et l'on cherche celle de la "
        "poignée, de proche en proche, avec le centre instantané de rotation de chaque barre.</p>"
        "<ol><li>Barre P1DQ2 : P1 tourne autour de C1 (biellette C1P1), D se déplace sur l'axe. Construis son CIR, "
        "nomme-le I1, puis la vitesse de Q2.</li>"
        "<li>Barre Q2EP3 : construis son CIR (nomme-le I2), puis la vitesse de P3.</li>"
        "<li>Biellette P3H : construis son CIR (nomme-le I3), puis la vitesse de H.</li></ol></div>" +
        fig(fg.fig_tirebouchon, "Figure 1 — Tire-bouchon.", "Pantographe de barres articulées entre le collier posé sur la "
            "bouteille et la poignée A ; tige filetée articulée en D", 420) + "</div>"], [
        QBAR(["DT2"], "sur la planche"),
        CG("Sur la planche : construis les CIR I1, I2, I3 (nomme-les) et les vitesses " + vec("V") + "<sub>Q2</sub>, " +
           vec("V") + "<sub>P3</sub> et " + vec("V") + "<sub>H</sub>.",
           "Un CIR est à l'intersection des perpendiculaires aux vitesses (ici : une droite déjà tracée, et la "
           "perpendiculaire à l'axe). Les normes se transportent au compas (triangle des vitesses, document DT2).",
           PL_TB,
           [("Point I1 (CIR de la barre P1DQ2)", num(0, None, abs_=2), "sur la verticale de D, sur la droite C1P1"),
            ("Vecteur tracé en Q2 : norme", num(VQ2g, None, rel=0.04), f"{fr(VQ2g, 1)} mm/s"),
            ("Point I2 (CIR de la barre Q2EP3)", num(0, None, abs_=2), "sur la verticale de E, sur la droite I1Q2"),
            ("Vecteur tracé en P3 : norme", num(VP3g, None, rel=0.04), f"{fr(VP3g, 1)} mm/s"),
            ("Point I3 (CIR de la biellette P3H)", num(0, None, abs_=2), "sur la verticale de H, sur la droite I2P3"),
            ("Vecteur tracé en H : norme", num(VHg, None, rel=0.04), f"{fr(VHg, 1)} mm/s"),
            ("Vecteur tracé en H : direction", num(0, None, abs_=3), "horizontale, vers la poignée (0°)")],
           "<p><b>Barre P1DQ2.</b> P1 décrit un cercle de centre C1 : sa vitesse est perpendiculaire à C1P1, et le CIR "
           "I1 est sur la droite (C1P1). D reste sur l'axe : I1 est aussi sur la perpendiculaire à l'axe en D. "
           "<i>V</i><sub>Q2</sub> = <i>V</i><sub>D</sub> × I1Q2 / I1D ≈ " + fr(VQ2g, 1) + " mm/s, perpendiculaire à I1Q2.</p>"
           "<p><b>Barre Q2EP3.</b> La vitesse de Q2 est perpendiculaire à I1Q2 : I2 est sur la droite (I1Q2), et sur la "
           "perpendiculaire à l'axe en E. <i>V</i><sub>P3</sub> = <i>V</i><sub>Q2</sub> × I2P3 / I2Q2 ≈ " + fr(VP3g, 1) +
           " mm/s.</p><p><b>Biellette P3H.</b> I3 est sur la droite (I2P3) et sur la perpendiculaire à l'axe en H : "
           "<i>V</i><sub>H</sub> = <i>V</i><sub>P3</sub> × I3H / I3P3 ≈ " + fr(VHg, 1) + " mm/s = 3·<i>V</i><sub>D</sub>.</p>"
           "<p>Pour transporter une norme dans la rotation autour d'un CIR : cercle de centre I passant par le point "
           "cherché (Compas), qui le ramène sur le rayon de la vitesse connue ; droite de I par l'extrémité de cette "
           "vitesse ; la perpendiculaire au rayon donne la norme, que l'on reporte (outil Report).</p>"),
        Q("Lis la vitesse <i>V</i><sub>H</sub> de l'articulation H.", H_LU, num(VHg, "mm/s", rel=0.04),
          f"<i>V</i><sub>H</sub> ≈ {fr(VHg, 0)} mm/s",
          f"<p>Lecture de la construction : <i>V</i><sub>H</sub> ≈ {fr(VHg, 1)} mm/s.</p>"),
    ]),
    partie("Principe des puissances virtuelles", 10, [
        "<p>La poignée est en translation le long de l'axe : <i>V</i><sub>A</sub> = <i>V</i><sub>H</sub>. Les liaisons "
        "sont supposées parfaites et le tire-bouchon en équilibre sous l'action de " + vec("F") + " (opérateur) et de " +
        vec("T") + " (bouchon) ; le collier, fixe, ne travaille pas.</p>" + donnees("effort de l'opérateur : <i>F</i> = 120 N")], [
        QBAR(["DT1", "DT2"]),
        Q("Calcule le rapport <i>V</i><sub>A</sub> / <i>V</i><sub>D</sub>.", "Nombre sans unité, déduit de ta construction ; "
          "tolérance de 4 %.", num(VHg / 15, None, rel=0.04), "3",
          eq(f"{frac('<i>V</i><sub>A</sub>', '<i>V</i><sub>D</sub>')} = {frac(fr(VHg, 1), '15')} = 3")),
        Q("Applique le principe des puissances virtuelles : calcule l'effort <i>T</i> du bouchon.", H_NUM,
          num(F4 * VHg / 15, "N", rel=0.04), f"<i>T</i> = 3·<i>F</i> = {fr(3 * F4, 0)} N",
          "<p>Pour le mouvement virtuel construit, la somme des puissances des efforts extérieurs est nulle :</p>" +
          eq("<i>F</i>·<i>V</i><sub>A</sub> − <i>T</i>·<i>V</i><sub>D</sub> = 0 ⇒ "
             f"<i>T</i> = <i>F</i> × {frac('<i>V</i><sub>A</sub>', '<i>V</i><sub>D</sub>')} = 120 × 3 = {fr(3 * F4, 0)} N") +
          "<p>On retrouve <i>T</i> = 3·<i>F</i> : le pantographe multiplie l'effort par trois, au prix d'une course "
          "trois fois plus longue à la poignée.</p>"),
    ]),
]


# ============================================================ définitions des activités (accueil et configuration)
# image de chaque activité (accueil et page de l'activité) : la figure du manuel, src/images/carte-*.jpg
# (outils/extraire_figures.py, puis outils/preparer_images.py) ; texte alternatif et légende
IMAGES_ACT = {
    "A1": ("Camion de 14 000 kg roulant à 108 km/h", "Énergie cinétique d'un camion (figure du cours)."),
    "A2": ("Palan levant puis descendant une charge : poids et vitesse du centre de gravité",
           "Puissance développée par le poids d'une charge (figure du cours)."),
    "A3": ("Cabine d'ascenseur entre ses glissières ; escalier roulant incliné à 30°",
           "Les deux systèmes : la cabine d'ascenseur et l'escalier roulant."),
    "A4": ("Skieurs en vol au-dessus du tremplin", "Les skieurs que tire le remonte-pente (figure du cours)."),
    "A5": ("Wagonnet de 300 kg arrivant à 2 m/s sur un amortisseur à ressort, rail incliné de 10°",
           "Amortisseur de fin de course."),
    "A6": ("Amortisseur à ressort en bout de rail, course de 100 mm", "L'amortisseur à ressort."),
    "A7": ("Automobile descendant une pente à 90 km/h, distance d'arrêt x", "Freinage dans une pente."),
    "A8": ("Vérin de levage suspendu, charge de 3 000 daN descendant à 0,3 m/s", "Vérin de levage."),
    "A9": ("Frein à sabot : levier articulé en A, sabot appuyé sur le tambour, effort F", "Frein à sabot."),
    "A10": ("Frein à disque industriel : deux garnitures serrent le tambour de part et d'autre",
            "Freinage par deux garnitures symétriques (figure du cours)."),
    "G1": ("Wagonnet guidé sur un rail incliné à 70°, vitesse 0,3 m/s, poids 300 daN", "Wagonnet de levage."),
    "G2": ("Roue dentée A entraînée par un couple, engrenant avec la roue B", "Roues dentées."),
    "G3": ("Vérin relié en B à un balancier articulé en A, poids de 5 000 daN", "Levage de balancier."),
    "G4": ("Tire-bouchon à pantographe posé sur la bouteille, effort F sur la poignée", "Tire-bouchon."),
}


def act(key, prefix, tag, level, rub, title, parts, docs, consignes, mots, sub):
    n = tag.split()[-1]
    alt, legende = IMAGES_ACT[n]
    return {"key": key, "prefix": prefix, "tag": tag, "level": level, "rubrique": rub, "title": title, "parts": parts,
            "docs": docs, "consignes": consignes, "image": "carte-" + n.lower(), "valt": alt, "legende": legende,
            "mots": mots, "sub": sub}


ACTIVITES = [
    act("qcm-travail-energie", "a", "Activité A1", "Niveau 1", "analytique", "QCM : travail et énergie cinétique", A1,
        ["DT1"], CONSIGNES_QCM, ["Couple", "Translation", "Rotation"],
        "Trois questions à propositions : travail d'un couple, énergie cinétique en translation et en rotation."),
    act("qcm-puissance", "b", "Activité A2", "Niveau 1", "analytique", "QCM : puissance d'une force, d'un couple", A2,
        ["DT1"], CONSIGNES_QCM, ["Produit scalaire", "Force", "Couple"],
        "Deux questions à propositions : puissance d'une force (produit scalaire) et puissance d'un couple."),
    act("ascenseur-escalier", "c", "Activité A3", "Niveau 1", "analytique", "Ascenseur et escalier roulant", A3, ["DT1"],
        CONSIGNES_CALCUL, ["Travail", "Puissance", "Rendement"],
        "Deux levages de personnes : travail et puissance d'une cabine d'ascenseur, rendement d'un escalier roulant."),
    act("remonte-pente-bateau", "d", "Activité A4", "Niveau 1", "analytique", "Remonte-pente et bateau", A4, ["DT1"],
        CONSIGNES_CALCUL, ["Puissance moyenne", "Rendement", "Résistance"],
        "Puissance moyenne et rendement : le moteur d'un remonte-pente, la résistance à l'avancement d'un bateau."),
    act("amortisseur", "e", "Activité A5", "Niveau 2", "analytique", "Amortisseur de fin de course", A5, ["DT1"],
        CONSIGNES_CALCUL, ["Énergie cinétique", "Ressort", "Théorème"],
        "Un wagonnet freiné par un ressort : théorème de l'énergie cinétique, raideur et effort en fin de course."),
    act("wagon-pente", "f", "Activité A6", "Niveau 2", "analytique", "Wagon sur une pente de 2 %", A6, ["DT1"],
        CONSIGNES_CALCUL, ["Conservation", "Ressort", "Course"],
        "Conservation de l'énergie : la vitesse au contact de l'amortisseur, puis la course de compression du ressort."),
    act("freinage-pente", "g", "Activité A7", "Niveau 2", "analytique", "Freinage dans une pente", A7, ["DT1"],
        CONSIGNES_CALCUL, ["Distance d'arrêt", "Pente", "Énergie dissipée"],
        "Une automobile freine en descente : distance d'arrêt et énergie dissipée par le freinage."),
    act("verin-levage", "h", "Activité A8", "Niveau 2", "analytique", "Vérin de levage", A8, ["DT1"],
        CONSIGNES_CALCUL, ["Décélération", "Effort", "Pression"],
        "Arrêt d'une charge en fin de course : effort de décélération et pression maximale dans le vérin."),
    act("frein-sabot", "i", "Activité A9", "Niveau 2", "analytique", "Frein à sabot", A9, ["DT1"],
        CONSIGNES_CALCUL, ["Moment d'inertie", "Couple de freinage", "Levier"],
        "Arrêter un tambour en 50 tours : couple de freinage, effort presseur et effort sur le levier."),
    act("frein-deux-sabots", "j", "Activité A10", "Niveau 2", "analytique", "Frein à deux sabots", A10, ["DT1"],
        CONSIGNES_CALCUL, ["Deux sabots", "Effort", "Puissance de freinage"],
        "Le même tambour, freiné par deux sabots depuis 400 tr/min : efforts sur les leviers et puissance de freinage."),
    act("skip-chargement", "k", "Activité G1", "Niveau 1", "graphique", "Skip de chargement", G1, ["DT1", "DT2"],
        CONSIGNES_GRAPHIQUE, ["Projection", "Puissance du poids", "Échelles"],
        "Projeter pour calculer : composante verticale de la vitesse, dénivellation, puis énergie et puissance de levage."),
    act("roues-dentees", "l", "Activité G2", "Niveau 2", "graphique", "Roues dentées", G2, ["DT1", "DT2"],
        CONSIGNES_GRAPHIQUE, ["Répartition linéaire", "Roulement", "Mise en vitesse"],
        "Vitesses construites au contact de deux roues dentées, puis mise en vitesse par le théorème de l'énergie cinétique."),
    act("balancier", "m", "Activité G3", "Niveau 2", "graphique", "Levage de balancier", G3, ["DT1", "DT2"],
        CONSIGNES_GRAPHIQUE, ["Triangle des vitesses", "Huygens", "Pression"],
        "Un balancier manœuvré par un vérin : triangle des vitesses, puis amortissement en fin de course."),
    act("tire-bouchon", "n", "Activité G4", "Niveau 2", "graphique", "Tire-bouchon", G4, ["DT1", "DT2"],
        CONSIGNES_GRAPHIQUE, ["CIR", "Puissances virtuelles", "Pantographe"],
        "Un pantographe de barres articulées : vitesses par les centres instantanés de rotation, puis T = 3·F."),
]
