# -*- coding: utf-8 -*-
"""Activités tirées des exercices du chapitre « Énergétique » (pages d'exercices fournies, numéros du manuel dans
NOTE-DE-LIVRAISON.md). Une activité par exercice ; les plus courts sont réunis par deux (une partie chacun).
Numérotation sur le modèle du dépôt « Chaîne fonctionnelle » : le premier chiffre donne le niveau (1.1… puis 2.1…).

Toutes les valeurs attendues sont recalculées ici (g = 9,81 m/s²), avec les mêmes formules que les démarches."""
import math

import figures as fg
from commun import G, HTML, Q, QBAR, QCM, donnees, eq, fr, frac, num, sig, vec

PI = math.pi
H_NUM = "Saisis la valeur <strong>avec son unité</strong> (elle vaut la moitié du point) ; tolérance de 2 %."
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
<tr><td>Travail virtuel (équilibre, liaisons parfaites)</td><td>Σ δ<i>W</i> = 0 pour tout déplacement virtuel compatible avec les liaisons</td><td><i>F</i><sub>e</sub>·δ<i>x</i><sub>e</sub> = <i>F</i><sub>s</sub>·δ<i>x</i><sub>s</sub></td></tr>
</tbody></table>
<h3>Frottement</h3>
<p>Effort tangentiel <i>T</i> = <i>f</i>·<i>N</i> (<i>f</i> = μ coefficient de frottement, <i>N</i> effort presseur).</p>
</div>"""

DOCS = [
    ("DT1", "Formulaire d'énergétique", "Dossier technique", True, FORMULAIRE_HTML),
]


def page_formulaire(A):
    """Page « Formulaire d'énergétique » (?ex=formulaire-energetique) : le document DT1, en pleine page."""
    return (A.course_head("Formulaire", "", "Formulaire d'énergétique",
                          "Les formules du cours, avec leurs unités. La même fiche s'ouvre dans les activités "
                          "(document DT1).") +
            '<div class="cours">' + A.course_section(1, "f-formules", "Formules et unités", FORMULAIRE_HTML) +
            '<div class="cours-foot"><a class="btn" href="?ex=cours-energetique">Le cours</a>'
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
    "<p>On reprend le wagonnet de 300 kg de l'activité 2.2. Il descend maintenant une pente de 2 %, départ arrêté, sur "
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
      "50 fois le poids du wagon) : comparer avec l'amortisseur de l'activité 2.2.</p>"),
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
    "<p>On reprend le tambour de l'activité 2.7, freiné cette fois par deux sabots identiques disposés "
    "symétriquement, chacun au bout d'un levier identique à celui de l'activité 2.7. Le tambour tourne à 400 tr/min au "
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


# ============================================================ skip de chargement
a70 = math.radians(70)
H1 = 15 * math.sin(a70)
W1 = 3000 * H1
VV1 = 0.3 * math.sin(a70)
Pp1 = -3000 * VV1
Pm1 = -Pp1 / 0.7
t1 = 15 / 0.3
SKIP = [partie("Le skip de chargement", 18, [
    '<div class="cours-split"><div>'
    "<p>Un skip de chargement effectue le levage d'un wagonnet le long d'un rail incliné. Déterminer l'énergie dépensée "
    "pour le levage, puis la puissance du moteur à adopter.</p>" +
    donnees("poids de l'ensemble : <i>P</i> = 300 daN = 3 000 N", "distance parcourue sur le rail : 15 m",
            "inclinaison du rail : 70° par rapport à l'horizontale", "vitesse du wagonnet : <i>V</i> = 0,3 m/s",
            "rendement de l'appareil : η = 0,7") +
    "</div>" + fig(fg.fig_skip, "Figure 1 — Wagonnet de levage.", "Wagonnet sur un rail incliné à 70°, poids 300 daN, "
                   "vitesse 0,3 m/s, 15 m de rail", 360) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule la dénivellation <i>h</i> franchie par le wagonnet.", H_NUM, num(H1, "m"), f"<i>h</i> ≈ {fr(H1, 2)} m",
      eq(f"<i>h</i> = 15 × sin 70° = 15 × {fr(math.sin(a70), 3)} ≈ {fr(H1, 2)} m")),
    Q("Calcule l'énergie <i>W</i> dépensée pour le levage.", H_NUM, num(W1 / 1000, "kJ"), f"<i>W</i> ≈ {fr(W1 / 1000, 1)} kJ",
      "<p>Le travail du poids ne dépend que de la dénivellation : il faut fournir au moins <i>P</i>·<i>h</i>.</p>" +
      eq(f"<i>W</i> = <i>P</i>·<i>h</i> = 3 000 × {fr(H1, 2)} ≈ {fr(W1, 0)} J ≈ {fr(W1 / 1000, 1)} kJ")),
    Q("Calcule la composante verticale <i>V</i><sub>v</sub> de la vitesse du wagonnet.", H_NUM, num(VV1, "m/s"),
      f"<i>V</i><sub>v</sub> ≈ {fr(VV1, 3)} m/s",
      "<p>La vitesse est portée par le rail, incliné de 70° sur l'horizontale : sa projection sur la verticale vaut "
      "<i>V</i>·sin 70° (ou <i>V</i>·cos 20°, 20° étant l'angle entre le rail et la verticale).</p>" +
      eq(f"<i>V</i><sub>v</sub> = 0,3 × sin 70° ≈ {fr(VV1, 3)} m/s")),
    Q("Calcule la puissance développée par le poids, avec son signe.", H_NUM, num(Pp1, "W"),
      f"{vec('P')}·{vec('V')} ≈ {fr(Pp1, 0)} W",
      eq(f"{vec('P')}·{vec('V')} = <i>P</i>·<i>V</i>·cos(90° + 70°) = −<i>P</i>·<i>V</i><sub>v</sub> = −3 000 × {fr(VV1, 3)} ≈ {fr(Pp1, 0)} W") +
      "<p>Le poids s'oppose à la montée : sa puissance est négative (résistante). Vérification : <i>W</i> / <i>t</i> = "
      f"{fr(W1, 0)} / {fr(t1, 0)} s ≈ {fr(-Pp1, 0)} W.</p>"),
    Q("Calcule la puissance du moteur à adopter.", H_NUM, num(Pm1 / 1000, "kW"), f"<i>P</i><sub>m</sub> ≈ {fr(Pm1 / 1000, 2)} kW",
      eq(f"<i>P</i><sub>m</sub> = {frac(fr(-Pp1, 0), '0,7')} ≈ {fr(Pm1, 0)} W ≈ {fr(Pm1 / 1000, 2)} kW")),
])]

# ============================================================ roues dentées
JA2, JB2 = 4 * 0.12 ** 2, 12 * 0.3 ** 2
wA2 = tr_min(900)
WB2 = wA2 * 0.150 / 0.375
Ec2 = 0.5 * JA2 * wA2 ** 2 + 0.5 * JB2 * WB2 ** 2
EcB2 = 0.5 * JB2 * WB2 ** 2
thA2 = Ec2 / 10
tours2 = thA2 / (2 * PI)
Ft2 = EcB2 / (0.375 * thA2 * 0.4)
ROUES = [partie("La mise en vitesse de deux roues dentées", 25, [
    '<div class="cours-split"><div>'
    "<p>Une roue dentée A transmet son mouvement à une roue B. L'ensemble est à l'arrêt lorsqu'un couple constant "
    "<i>C</i><sub>A</sub> est appliqué à la roue A ; les frottements sont négligés. Quel nombre de tours fait la roue A "
    "avant d'atteindre la vitesse de 900 tr/min ? Quel est l'effort tangentiel exercé entre les deux roues ?</p>" +
    donnees("roue A : masse 4 kg, rayon de giration 120 mm, rayon primitif <i>r</i><sub>A</sub> = 150 mm",
            "roue B : masse 12 kg, rayon de giration 300 mm, rayon primitif <i>r</i><sub>B</sub> = 375 mm",
            "couple moteur appliqué à A : <i>C</i><sub>A</sub> = 10 N·m ; vitesse finale de A : 900 tr/min") +
    "</div>" + fig(fg.fig_roues, "Figure 1 — Roues dentées.", "Roue dentée A entraînée par un couple CA, engrenant avec "
                   "une roue B plus grande", 380) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule la vitesse angulaire finale ω<sub>A</sub> de la roue A.", H_NUM, num(wA2, "rad/s"),
      f"ω<sub>A</sub> ≈ {fr(wA2, 2)} rad/s", eq(f"ω<sub>A</sub> = {frac('π × 900', '30')} ≈ {fr(wA2, 2)} rad/s")),
    Q("Calcule la vitesse angulaire finale ω<sub>B</sub> de la roue B.", H_NUM, num(WB2, "rad/s"),
      f"ω<sub>B</sub> ≈ {fr(WB2, 2)} rad/s",
      "<p>Les cercles primitifs roulent sans glisser : au point de contact, les deux roues ont la même vitesse.</p>" +
      eq(f"<i>r</i><sub>A</sub>·ω<sub>A</sub> = <i>r</i><sub>B</sub>·ω<sub>B</sub> ⇒ ω<sub>B</sub> = {fr(wA2, 2)} × "
         f"{frac('150', '375')} ≈ {fr(WB2, 2)} rad/s (360 tr/min)")),
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
])]

# ============================================================ levage de balancier
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
BALANCIER = [
    partie("Vitesses du balancier et effort de retenue", 12, [
        '<div class="cours-split"><div>'
        "<p>Le dispositif de levage de l'activité 2.5 manœuvre maintenant un balancier, articulé en A sur le bâti. La "
        "tige du vérin, articulée en B, descend à la vitesse de 0,3 m/s ; le balancier, horizontal à l'instant étudié, "
        "tourne autour de A. Son poids, 5 000 daN, s'applique en son centre de gravité G.</p>" +
        donnees("AB = 1 m ; AG = 2 m ; longueur du balancier : 4 m",
                "vitesse de la tige en B : <i>V</i><sub>B</sub> = 0,3 m/s, verticale, vers le bas") +
        "</div>" + fig(fg.fig_balancier, "Figure 1 — Levage de balancier.", "Vérin vertical relié en B à un balancier "
                       "horizontal articulé en A, poids de 5 000 daN", 380) + "</div>"], [
        QBAR(["DT1"]),
        Q("Calcule la vitesse angulaire ω du balancier.", H_NUM, num(0.3, "rad/s"), "ω = 0,3 rad/s",
          eq("ω = <i>V</i><sub>B</sub> / AB = 0,3 / 1 = 0,3 rad/s")),
        Q("Calcule la vitesse <i>V</i><sub>G</sub> du centre de gravité G.", H_NUM, num(0.6, "m/s"),
          "<i>V</i><sub>G</sub> = 0,6 m/s", eq("<i>V</i><sub>G</sub> = ω·AG = 0,3 × 2 = 0,6 m/s")),
        Q("La descente est uniforme : calcule l'effort <i>F</i><sub>s</sub> de la tige qui retient le balancier.",
          H_NUM, num(Fs3 / 1000, "kN"), f"<i>F</i><sub>s</sub> = {fr(Fs3 / 1000, 0)} kN",
          "<p>Énergie cinétique constante : la somme des puissances des efforts extérieurs est nulle. Le poids (moteur) "
          "et la tige (résistante) ont des puissances opposées ; l'action de l'articulation A ne travaille pas.</p>" +
          eq("<i>F</i><sub>s</sub>·<i>V</i><sub>B</sub> = <i>P</i>·<i>V</i><sub>G</sub> ⇒ "
             f"<i>F</i><sub>s</sub> = 50 000 × {frac('0,6', '0,3')} = {fr(Fs3, 0)} N") +
          "<p>On retrouve l'équilibre des moments en A : <i>F</i><sub>s</sub> × 1 = <i>P</i> × 2.</p>"),
    ]),
    partie("Amortissement en fin de course", 25, [
        "<p>L'arrêt est obtenu, comme dans l'activité 2.5, par une valve de décélération, ici sur une course de tige "
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
          "<p>B descend de 40 mm : le balancier tourne de Δθ = 0,04 / 1 = 0,04 rad et G, deux fois plus loin de A, "
          "descend de 2 × 0,04 = 0,08 m.</p>" + eq("<i>W</i><sub>P</sub> = <i>P</i> × 0,08 = 50 000 × 0,08 = 4 000 J")),
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

# ============================================================ tire-bouchon : principe du travail virtuel
F4 = 120
TIREBOUCHON = [partie("Le tire-bouchon : principe du travail virtuel", 15, [
    '<div class="cours-split"><div>'
    "<p>Un tire-bouchon est réalisé à partir d'un système de barres articulées (pivots) entre elles et d'une tige "
    "filetée articulée en D sur les barres. " + vec("F") + " schématise l'action de l'opérateur sur la poignée, en A ; "
    + vec("B") + " (non représentée) celle de la bouteille sur le collier ; " + vec("T") + " celle du bouchon sur la "
    "tige. En utilisant le principe des travaux virtuels, déterminer la valeur de <i>T</i> en fonction de <i>F</i>.</p>"
    "<p><b>Géométrie du pantographe.</b> Les barres, identiques, sont articulées en leur milieu et à leurs extrémités ; "
    "elles font toutes le même angle φ avec l'axe. Les biellettes du collier, prolongées, se coupent sur l'axe en un "
    "point fixe O. Les articulations D, E et H, sur l'axe, sont alors à des distances de O égales à</p>" +
    eq("<i>x</i><sub>D</sub> = 2·<i>a</i>·cos φ ; <i>x</i><sub>E</sub> = 4·<i>a</i>·cos φ ; <i>x</i><sub>H</sub> = 6·<i>a</i>·cos φ") +
    "<p>où <i>a</i> est la demi-longueur d'une barre. La poignée, solidaire de H, se déplace comme H.</p>" +
    donnees("effort de l'opérateur : <i>F</i> = 120 N", "liaisons supposées parfaites ; tire-bouchon en équilibre") +
    "</div>" + fig(fg.fig_tirebouchon, "Figure 1 — Tire-bouchon.", "Pantographe de barres articulées entre le collier "
                   "posé sur la bouteille et la poignée A ; tige filetée articulée en D", 420) + "</div>"], [
    QBAR(["DT1"]),
    Q("Calcule le rapport δ<i>x</i><sub>A</sub> / δ<i>x</i><sub>D</sub> des déplacements virtuels de la poignée et de la tige.",
      H_SANS, num(3, None), "3",
      "<p>Pour une petite variation δφ de l'angle des barres, toutes les distances varient avec cos φ :</p>" +
      eq("δ<i>x</i><sub>D</sub> = −2·<i>a</i>·sin φ·δφ ; δ<i>x</i><sub>A</sub> = δ<i>x</i><sub>H</sub> = −6·<i>a</i>·sin φ·δφ ⇒ "
         f"{frac('δ<i>x</i><sub>A</sub>', 'δ<i>x</i><sub>D</sub>')} = 3")),
    Q("Pour extraire le bouchon de 30 mm, de quelle longueur l'opérateur doit-il déplacer la poignée ?", H_NUM,
      num(90, "mm"), "90 mm", eq("course de la poignée = 3 × 30 = 90 mm")),
    Q("Calcule le travail fourni par l'opérateur sur cette course.", H_NUM, num(F4 * 0.09, "J"),
      f"<i>W</i> = {fr(F4 * 0.09, 1)} J", eq(f"<i>W</i> = <i>F</i> × 0,09 = 120 × 0,09 = {fr(F4 * 0.09, 1)} J")),
    Q("Applique le principe du travail virtuel : calcule l'effort <i>T</i> exercé par le bouchon.", H_NUM,
      num(3 * F4, "N"), f"<i>T</i> = 3·<i>F</i> = {fr(3 * F4, 0)} N",
      "<p>Pour tout déplacement virtuel compatible avec les liaisons, la somme des travaux des efforts extérieurs est "
      "nulle ; le collier, fixe, ne travaille pas :</p>" +
      eq("<i>F</i>·δ<i>x</i><sub>A</sub> − <i>T</i>·δ<i>x</i><sub>D</sub> = 0 ⇒ "
         f"<i>T</i> = <i>F</i> × {frac('δ<i>x</i><sub>A</sub>', 'δ<i>x</i><sub>D</sub>')} = 120 × 3 = {fr(3 * F4, 0)} N") +
      "<p>On retrouve <i>T</i> = 3·<i>F</i> : le pantographe multiplie l'effort par trois, au prix d'une course trois "
      "fois plus longue à la poignée.</p>"),
])]


# ============================================================ définitions des activités (accueil et configuration)
# image de chaque activité (accueil et page de l'activité) : la figure du manuel, src/images/carte-*.jpg
# (outils/extraire_figures.py, puis outils/preparer_images.py) ; texte alternatif et légende
IMAGES_ACT = {
    "1.1": ("Camion de 14 000 kg roulant à 108 km/h", "Énergie cinétique d'un camion (figure du cours)."),
    "1.2": ("Palan levant puis descendant une charge : poids et vitesse du centre de gravité",
            "Puissance développée par le poids d'une charge (figure du cours)."),
    "1.3": ("Cabine d'ascenseur entre ses glissières ; escalier roulant incliné à 30°",
            "Les deux systèmes : la cabine d'ascenseur et l'escalier roulant."),
    "1.4": ("Skieurs en vol au-dessus du tremplin", "Les skieurs que tire le remonte-pente (figure du cours)."),
    "1.5": ("Wagonnet guidé sur un rail incliné à 70°, vitesse 0,3 m/s, poids 300 daN", "Wagonnet de levage."),
    "2.1": ("Tire-bouchon à pantographe posé sur la bouteille, effort F sur la poignée", "Tire-bouchon."),
    "2.2": ("Wagonnet de 300 kg arrivant à 2 m/s sur un amortisseur à ressort, rail incliné de 10°",
            "Amortisseur de fin de course."),
    "2.3": ("Amortisseur à ressort en bout de rail, course de 100 mm", "L'amortisseur à ressort."),
    "2.4": ("Automobile descendant une pente à 90 km/h, distance d'arrêt x", "Freinage dans une pente."),
    "2.5": ("Vérin de levage suspendu, charge de 3 000 daN descendant à 0,3 m/s", "Vérin de levage."),
    "2.6": ("Vérin relié en B à un balancier articulé en A, poids de 5 000 daN", "Levage de balancier."),
    "2.7": ("Frein à sabot : levier articulé en A, sabot appuyé sur le tambour, effort F", "Frein à sabot."),
    "2.8": ("Frein à disque industriel : deux garnitures serrent le tambour de part et d'autre",
            "Freinage par deux garnitures symétriques (figure du cours)."),
    "2.9": ("Roue dentée A entraînée par un couple, engrenant avec la roue B", "Roues dentées."),
}


def act(key, prefix, n, title, parts, consignes, mots, sub):
    alt, legende = IMAGES_ACT[n]
    return {"key": key, "prefix": prefix, "tag": "Activité " + n, "level": "Niveau " + n[0], "title": title,
            "parts": parts, "docs": ["DT1"], "consignes": consignes, "image": "carte-" + n.replace(".", "-"),
            "valt": alt, "legende": legende, "mots": mots, "sub": sub}


ACTIVITES = [
    act("qcm-travail-energie", "a", "1.1", "QCM : travail et énergie cinétique", A1, CONSIGNES_QCM,
        ["Couple", "Translation", "Rotation"],
        "Trois questions à propositions : travail d'un couple, énergie cinétique en translation et en rotation."),
    act("qcm-puissance", "b", "1.2", "QCM : puissance d'une force, d'un couple", A2, CONSIGNES_QCM,
        ["Produit scalaire", "Force", "Couple"],
        "Deux questions à propositions : puissance d'une force (produit scalaire) et puissance d'un couple."),
    act("ascenseur-escalier", "c", "1.3", "Ascenseur et escalier roulant", A3, CONSIGNES_CALCUL,
        ["Travail", "Puissance", "Rendement"],
        "Deux levages de personnes : travail et puissance d'une cabine d'ascenseur, rendement d'un escalier roulant."),
    act("remonte-pente-bateau", "d", "1.4", "Remonte-pente et bateau", A4, CONSIGNES_CALCUL,
        ["Puissance moyenne", "Rendement", "Résistance"],
        "Puissance moyenne et rendement : le moteur d'un remonte-pente, la résistance à l'avancement d'un bateau."),
    act("skip-chargement", "e", "1.5", "Skip de chargement", SKIP, CONSIGNES_CALCUL,
        ["Dénivellation", "Puissance du poids", "Rendement"],
        "Un wagonnet levé le long d'un rail incliné : énergie de levage, puissance du poids et puissance du moteur."),
    act("tire-bouchon", "f", "2.1", "Tire-bouchon", TIREBOUCHON, CONSIGNES_CALCUL,
        ["Travail virtuel", "Pantographe", "Rapport des efforts"],
        "Un pantographe de barres articulées : déplacements virtuels, puis principe du travail virtuel, T = 3·F."),
    act("amortisseur", "g", "2.2", "Amortisseur de fin de course", A5, CONSIGNES_CALCUL,
        ["Énergie cinétique", "Ressort", "Théorème"],
        "Un wagonnet freiné par un ressort : théorème de l'énergie cinétique, raideur et effort en fin de course."),
    act("wagon-pente", "h", "2.3", "Wagon sur une pente de 2 %", A6, CONSIGNES_CALCUL,
        ["Conservation", "Ressort", "Course"],
        "Conservation de l'énergie : la vitesse au contact de l'amortisseur, puis la course de compression du ressort."),
    act("freinage-pente", "i", "2.4", "Freinage dans une pente", A7, CONSIGNES_CALCUL,
        ["Distance d'arrêt", "Pente", "Énergie dissipée"],
        "Une automobile freine en descente : distance d'arrêt et énergie dissipée par le freinage."),
    act("verin-levage", "j", "2.5", "Vérin de levage", A8, CONSIGNES_CALCUL,
        ["Décélération", "Effort", "Pression"],
        "Arrêt d'une charge en fin de course : effort de décélération et pression maximale dans le vérin."),
    act("balancier", "k", "2.6", "Levage de balancier", BALANCIER, CONSIGNES_CALCUL,
        ["Rotation", "Huygens", "Pression"],
        "Un balancier manœuvré par un vérin : vitesses et effort de retenue, puis amortissement en fin de course."),
    act("frein-sabot", "l", "2.7", "Frein à sabot", A9, CONSIGNES_CALCUL,
        ["Moment d'inertie", "Couple de freinage", "Levier"],
        "Arrêter un tambour en 50 tours : couple de freinage, effort presseur et effort sur le levier."),
    act("frein-deux-sabots", "m", "2.8", "Frein à deux sabots", A10, CONSIGNES_CALCUL,
        ["Deux sabots", "Effort", "Puissance de freinage"],
        "Le même tambour, freiné par deux sabots depuis 400 tr/min : efforts sur les leviers et puissance de freinage."),
    act("roues-dentees", "n", "2.9", "Roues dentées", ROUES, CONSIGNES_CALCUL,
        ["Roulement", "Moment d'inertie", "Mise en vitesse"],
        "Deux roues dentées mises en vitesse : théorème de l'énergie cinétique, nombre de tours et effort entre les dentures."),
]
