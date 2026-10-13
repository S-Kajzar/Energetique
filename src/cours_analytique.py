# -*- coding: utf-8 -*-
"""Cours 1 — Énergétique : approche analytique (?ex=cours-analytique).

Source : le chapitre « Énergétique » fourni (pages photographiées du manuel). Tout son texte est repris, section par
section : notions d'énergie et de puissance, travail d'une force et d'un couple, énergies potentielle et cinétique,
puissance, rendement, théorèmes. Les figures sont redessinées en SVG ; plusieurs deviennent interactives (énergie et
puissance du palan, signe du travail, tremplin) et les exemples chiffrés deviennent des calculateurs. Les méthodes
graphiques (aire sous une courbe, projection, vitesses construites) font l'objet du cours 2."""
import math

from commun import eq, fr, frac, vec
from figures import C, F, L, PL, R, T, V, personnage, sol, tremplin


def formule(main, units=""):
    return (f'<div class="formule"><span class="f-main">{main}</span>' +
            (f'<span class="f-units">{units}</span>' if units else "") + "</div>")


def svgfig(inner, caption, alt, vb="0 0 480 270", maxw=520, ident=""):
    i = f' id="{ident}"' if ident else ""
    return (f'<figure class="fig fig-svg" style="max-width:{maxw}px"><svg class="fs"{i} viewBox="{vb}" role="img" '
            f'aria-label="{alt}">{inner}</svg><figcaption>{caption}</figcaption></figure>')


def sim(titre, ident, controles, sorties, extra=""):
    ctr = "".join(f'<label>{lab} <output id="{ident}-{k}-o"></output><input type="range" id="{ident}-{k}" '
                  f'min="{a}" max="{b}" step="{s}" value="{v}"></label>' for k, lab, a, b, s, v in controles)
    out = "".join(f'<div><span>{lab}</span><b id="{ident}-{k}">–</b></div>' for k, lab in sorties)
    cls = "simu-out simu-out4" if len(sorties) == 4 else "simu-out"
    return (f'<div class="simu" id="{ident}"><h3>{titre}</h3><div class="simu-grid">{ctr}</div>'
            f'<div class="{cls}">{out}</div>{extra}</div>')


# ============================================================ figures
def fig_palan_reservoir():
    s = ""
    for x0, lab in ((10, "état initial"), (250, "état final")):
        s += R(x0 + 10, 18, 120, 10, "mf") + C((x0 + 70, 38), 10, "mb") + T((x0 + 2, 60), lab, "tc tr")
        yc = 200 if x0 == 10 else 120
        s += L((x0 + 70, 48), (x0 + 70, yc - 22)) + PL([(x0 + 50, yc - 4), (x0 + 70, yc - 22), (x0 + 90, yc - 4)])
        s += R(x0 + 46, yc - 4, 48, 32, "mo") + sol((x0 + 10, 240), (x0 + 130, 240))
        s += R(x0 + 160, 150, 60, 86, "fin") + L((x0 + 150, 120), (x0 + 172, 120)) + L((x0 + 172, 120), (x0 + 172, 132))
        if x0 == 250:
            s += R(x0 + 161, 158, 58, 77, "mb")
            s += L((x0 + 34, 228), (x0 + 34, 148), "fin") + F((x0 + 34, 190), (x0 + 34, 150), "cote", 7)
            s += F((x0 + 34, 190), (x0 + 34, 226), "cote", 7) + T((x0 + 14, 194), "h", "tn")
    s += T((60, 262), "palan : charge de masse m", "tc") + T((300, 262), "réservoir : volume V d'eau", "tc")
    return s


def fig_travail_theta():
    """Travail élémentaire : la force tourne autour de A (curseur θ)."""
    return ('<line class="fin" x1="40" y1="200" x2="440" y2="200"/>'
            '<path class="vb" d="" id="ca-dl"/><path class="vr" d="" id="ca-f"/>'
            '<path class="pointille" d="" id="ca-proj"/><path class="vv" d="" id="ca-fc" style="stroke-width:5;opacity:.6"/>'
            '<path class="fin" d="" id="ca-arc"/><text class="tn" id="ca-th" x="0" y="0">θ</text>'
            '<circle class="art" cx="120" cy="200" r="4"/><text class="tn" x="104" y="222">A</text>'
            '<text class="tn" x="388" y="222">A′</text><text class="tn tb" x="300" y="190">Δl</text>'
            '<text class="tn tr" id="ca-fl" x="0" y="0">F</text>')


def fig_rampe():
    s = sol((20, 240), (460, 240)) + '<path class="mo" d="M40 70 C150 70 200 110 260 150 S380 200 440 205 L440 240 L40 240 Z"/>'
    s += R(70, 44, 30, 26, "mf") + T((60, 40), "G₁", "tn") + R(400, 179, 30, 26, "mf") + T((432, 176), "G₂", "tn")
    s += '<path class="pointille" d="M85 57 C170 60 220 100 270 135 S380 180 415 192"/>'
    s += F((300, 150), (300, 200), "vr", 9) + V((306, 196), "P", "", "tr")
    s += L((85, 57), (470, 57), "pointille") + L((415, 192), (470, 192), "pointille")
    s += F((462, 120), (462, 59), "cote", 7) + F((462, 130), (462, 190), "cote", 7) + T((448, 130), "h", "tn")
    s += T((180, 98), "trajectoire de G", "tc")
    return s


def fig_couple():
    s = C((240, 140), 70, "mb") + C((240, 140), 10, "art") + L((240, 140), (330, 90), "fin") + L((240, 140), (330, 160), "fin")
    s += '<path class="vrl" d="M172 120 A72 72 0 0 1 270 74"/>' + F((262, 70), (274, 76), "vr", 10)
    s += T((210, 66), "C", "tn tr") + '<path class="fin" d="M290 112 A56 56 0 0 1 295 152"/>' + T((300, 138), "θ", "tn")
    s += T((336, 92), "position 2", "tc") + T((336, 166), "position 1", "tc")
    return s


def fig_ressort_torsion():
    s = ""
    for i in range(9):
        s += f'<ellipse class="m" cx="{200 + i * 12}" cy="130" rx="7" ry="34"/>'
    s += L((194, 100), (130, 40)) + L((302, 100), (360, 40)) + T((150, 230), "C = k·α : le couple croît avec l'angle", "tc")
    s += '<path class="vrl" d="M120 70 A90 90 0 0 1 170 26"/>' + F((164, 24), (174, 28), "vr", 9) + T((112, 40), "α", "tn")
    return s


def fig_ep():
    s = L((60, 30), (60, 240), "fin") + F((60, 240), (60, 22), "vk", 8) + T((66, 30), "z (altitude)", "tc")
    s += L((50, 240), (460, 240), "fin") + C((170, 80), 18, "mb") + T((196, 74), "G₁ : Ep₁ = m·g·z₁", "tn")
    s += F((170, 98), (170, 140), "vr", 9) + T((178, 128), "m·g", "tc tr") + C((170, 200), 18, "pointille")
    s += T((196, 204), "G₂ : Ep₂ = m·g·z₂", "tn") + L((54, 80), (150, 80), "pointille") + L((54, 200), (150, 200), "pointille")
    s += T((36, 84), "z₁", "tn") + T((36, 204), "z₂", "tn") + F((110, 140), (110, 82), "cote", 7) + F((110, 140), (110, 198), "cote", 7)
    s += T((116, 144), "h", "tn")
    return s


def fig_volant():
    s = '<ellipse class="mb" cx="200" cy="140" rx="40" ry="100"/>' + R(200, 40, 70, 200, "mb")
    s += '<ellipse class="mf" cx="270" cy="140" rx="40" ry="100"/>' + C((270, 140), 6, "art")
    s += L((150, 140), (360, 140), "axe") + T((300, 34), "Ø 2 000", "tc") + T((210, 262), "h = 500", "tc")
    s += '<path class="vbl" d="M330 70 A60 90 0 0 1 340 200"/>' + F((340, 190), (338, 204), "vb", 9) + T((346, 140), "ω", "tn tb")
    return s


def fig_disque():
    s = sol((20, 220), (460, 220)) + C((200, 160), 60, "mb") + C((200, 160), 5, "art") + T((206, 152), "G", "tn")
    s += T((194, 240), "I", "tn") + C((200, 220), 3, "art")
    s += F((200, 160), (270, 160), "vr", 9) + V((252, 152), "V", "G", "tr")
    s += F((200, 100), (340, 100), "vr", 9) + V((330, 92), "V", "", "tr") + T((344, 104), "= 2·VG", "tc")
    s += L((200, 220), (340, 100), "pointille") + '<path class="pointille" d="M60 220 C 90 120, 160 100, 200 100"/>'
    s += T((40, 120), "cycloïde (trajectoire d'un point du bord)", "tc")
    return s


def fig_puissance_force():
    s = '<path class="fin" d="M40 230 Q200 100 440 150"/>' + C((200, 162), 4, "art") + T((186, 182), "A", "tn")
    s += F((200, 162), (320, 140), "vb", 10) + V((322, 136), "V", "", "tb") + F((200, 162), (250, 50), "vr", 10)
    s += V((256, 52), "F", "", "tr") + T((236, 126), "θ", "tn") + T((330, 120), "tangente en A", "tc")
    return s


def fig_palan_montee():
    s = R(40, 20, 400, 14, "mf") + C((160, 50), 12, "mb") + L((160, 62), (160, 120)) + R(120, 120, 80, 50, "mo")
    s += F((150, 170), (150, 240), "vr", 9) + V((132, 232), "P", "", "tr") + F((175, 110), (175, 70), "vb", 9)
    s += V((182, 84), "V", "G", "tb") + T((140, 260), "montée : P = −P·V", "tc")
    s += C((330, 50), 12, "mb") + L((330, 62), (330, 120)) + R(290, 120, 80, 50, "mo")
    s += F((320, 170), (320, 240), "vr", 9) + V((302, 232), "P", "", "tr") + F((350, 172), (350, 212), "vb", 9)
    s += V((356, 206), "V", "G", "tb") + T((300, 260), "descente : P = +P·V", "tc")
    return s


def fig_rendement():
    s = sol((40, 230), (440, 230)) + R(170, 120, 140, 100, "mb", 6) + T((240, 176), "machine", "tc", "middle")
    s += F((60, 170), (166, 170), "vb", 14) + T((60, 158), "W fournie", "tb")
    s += F((314, 170), (420, 170), "vv", 14) + T((340, 158), "W restituée", "tn")
    for x in (200, 240, 280):
        s += f'<path class="vrl" d="M{x} 116 q-8 -12 0 -24 t0 -24 t0 -24"/>'
    s += T((210, 34), "W perdue (chaleur, frottements)", "tr")
    return s


def fig_frein_disque():
    s = C((200, 140), 100, "mb") + C((200, 140), 30, "mf") + C((200, 140), 5, "art") + T((206, 132), "O", "tn")
    s += R(120, 52, 48, 64, "mo") + R(232, 52, 48, 64, "mo") + T((112, 44), "plaquettes", "tc")
    s += L((200, 140), (200, 84), "fin") + T((206, 110), "r = 150 mm", "tc")
    s += '<path class="vbl" d="M300 110 A104 104 0 0 1 296 182"/>' + F((298, 174), (295, 186), "vb", 9)
    s += T((306, 150), "ω", "tn tb") + R(360, 40, 16, 200, "mb") + F((330, 90), (358, 90), "vr", 9) + F((410, 90), (378, 90), "vr", 9)
    s += T((322, 80), "N", "tn tr") + T((402, 80), "−N", "tn tr") + T((384, 236), "tambour seul", "tc")
    return s


# ============================================================ contenu
ESSENTIEL = [
    ("Travail", "Énergie échangée par une force qui se déplace : <i>W</i> = <i>F</i>·<i>AB</i>·cos θ, en joules. "
                "Moteur si &gt; 0, résistant si &lt; 0.", "Le poids : <i>W</i> = ± <i>m</i>·<i>g</i>·<i>h</i>, quel que soit le chemin."),
    ("Couple", "Travail d'un couple constant : <i>W</i> = <i>C</i>·θ (θ en radians).", "Ressort de torsion : <i>W</i> = ½·<i>k</i>·α²."),
    ("Énergie potentielle", "Stockée par la position (pesanteur : <i>m</i>·<i>g</i>·<i>z</i>) ou la déformation "
                            "(ressort : ½·<i>k</i>·<i>f</i>²).", "Elle ne dépend que des positions initiale et finale."),
    ("Énergie cinétique", "Liée à la vitesse : ½·<i>m</i>·<i>V</i>² en translation, ½·<i>J</i>·ω² en rotation.",
     "Vitesse doublée : énergie quadruplée."),
    ("Puissance", "Débit d'énergie : <i>P</i> = d<i>W</i>/d<i>t</i>, en watts. <i>P</i> = <i>F</i>·<i>V</i>·cos θ ; "
                  "<i>P</i> = <i>C</i>·ω.", "1 cv = 736 W."),
    ("Rendement", "η = <i>W</i> restituée / <i>W</i> fournie ≤ 1.", "L'énergie perdue part en chaleur, en frottements…"),
    ("Théorème de l'énergie cinétique", "Δ<i>E</i><sub>c</sub> = somme des travaux des actions extérieures.",
     "Une seule équation, sans calculer d'accélération."),
    ("Conservation de l'énergie", "Système isolé, sans frottement : <i>E</i><sub>c</sub> + <i>E</i><sub>p</sub> = constante.",
     "Le skieur : <i>m</i>·<i>g</i>·<i>h</i> = ½·<i>m</i>·<i>v</i>²."),
]

JEU_ENERGIES = [("Un ressort de suspension comprimé", "el"), ("Une voiture lancée à 90 km/h", "ci"),
                ("L'eau d'un barrage, retenue en altitude", "pe"), ("Un volant de presse qui tourne", "ci"),
                ("La barre de torsion d'un véhicule, vrillée", "el"), ("Une charge levée par un palan, immobile en haut", "pe"),
                ("Un skieur en haut du tremplin, à l'arrêt", "pe"), ("Le même skieur à l'envol", "ci")]
CHOIX_ENERGIES = [("pe", "Potentielle de pesanteur"), ("el", "Potentielle élastique"), ("ci", "Cinétique")]

QUIZ = [
    ("Une charge de 1 000 daN est levée de 2 m. Le travail fourni vaut :", ["2 000 J", "20 000 J", "200 J"], 1,
     "<i>W</i> = <i>P</i>·<i>h</i> = 10 000 N × 2 m = 20 000 J."),
    ("Le palan déplace horizontalement la même charge, sans la lever. Le travail du poids vaut :",
     ["0 J", "20 000 J", "−20 000 J"], 0, "La force (verticale) est perpendiculaire au déplacement : cos 90° = 0."),
    ("Un moteur fournit un couple de 20 N·m à 1 500 tr/min. Sa puissance est d'environ :", ["30 kW", "3,1 kW", "314 W"], 1,
     "<i>P</i> = <i>C</i>·ω = 20 × 1 500·π/30 ≈ 3 142 W."),
    ("La vitesse d'un véhicule est divisée par deux. Son énergie cinétique est :", ["divisée par 2", "divisée par 4",
                                                                                   "inchangée"], 1,
     "<i>E</i><sub>c</sub> est proportionnelle au carré de la vitesse."),
    ("Dans <i>E</i><sub>c</sub> = ½·<i>J</i>·ω², ω s'exprime en :", ["tr/min", "rad/s", "m/s"], 1,
     "ω en rad/s : convertir les tr/min par ω = π·<i>N</i>/30."),
    ("Un disque roule sans glisser. Son énergie cinétique vaut :", ["½·m·V<sub>G</sub>²", "¾·m·V<sub>G</sub>²",
                                                                    "½·J<sub>G</sub>·ω²"], 1,
     "½·<i>m</i>·<i>V</i><sub>G</sub>² + ½·(<i>m</i>·<i>R</i>²/2)·(<i>V</i><sub>G</sub>/<i>R</i>)² = ¾·<i>m</i>·<i>V</i><sub>G</sub>²."),
    ("Une force est perpendiculaire à la vitesse de son point d'application. Sa puissance est :", ["maximale", "nulle",
                                                                                                  "négative"], 1,
     "<i>P</i> = <i>F</i>·<i>V</i>·cos 90° = 0 : elle ne travaille pas."),
    ("Un moteur absorbe 2 kW et fournit 1,6 kW. Son rendement vaut :", ["0,8", "1,25", "0,4"], 0,
     "η = 1,6 / 2 = 0,8 ; 0,4 kW sont perdus."),
    ("Le théorème de l'énergie cinétique conduit, pour un solide :", ["à trois équations", "à une seule équation",
                                                                     "à aucune équation"], 1,
     "Une équation scalaire, contre trois équations de projection (dans le plan) pour le principe fondamental."),
    ("La conservation de l'énergie mécanique s'applique :", ["toujours", "s'il n'y a pas de frottement (système isolé)",
                                                            "seulement en rotation"], 1,
     "Avec des frottements, une partie de l'énergie est perdue en chaleur."),
]


def render(A):
    s = A.course_head(
        "Cours 1", "Niveau 1", "Énergétique : approche analytique",
        "Définir l'énergie et la puissance ; calculer le travail d'une force et d'un couple ; énergies potentielle et "
        "cinétique (translation, rotation, mouvement plan) ; rendement ; théorème de l'énergie cinétique et loi de "
        "conservation de l'énergie.")
    s += '<div class="cours">'
    s += ('<div class="remarque"><p>Les problèmes liés à l\'énergie sont d\'une grande importance : l\'énergie est à '
          "l'origine de tous les mouvements du monde de la technologie. Elle existe sous plusieurs formes : mécanique, "
          "électrique, chaleur… Une bonne connaissance des phénomènes énergétiques permet de construire des machines "
          "moins gourmandes en énergie. Les théorèmes sur l'énergie permettent, dans certains cas, de déterminer les "
          "efforts sans avoir à calculer les accélérations, comme l'exige le principe fondamental de la dynamique.</p>"
          "<p>La loi de conservation de l'énergie relie l'énergie potentielle (la hauteur <i>h</i> de départ d'un "
          "skieur sur un tremplin) et l'énergie cinétique (sa vitesse <i>v</i> avant le saut).</p></div>")
    s += svgfig(tremplin(), "Figure 1 — Du haut du tremplin à l'envol : l'énergie potentielle devient cinétique.",
                "Skieur sur un tremplin : hauteur h, vitesse v à l'envol", maxw=560)
    s += A.course_nav([("ca-notions", "Énergie et puissance"), ("ca-travail", "Travail d'une force"),
                       ("ca-couple", "Travail d'un couple"), ("ca-ep", "Énergie potentielle"),
                       ("ca-ec", "Énergie cinétique"), ("ca-puissance", "Puissance"), ("ca-rendement", "Rendement"),
                       ("ca-theoremes", "Théorèmes"), ("ca-essentiel", "L'essentiel"), ("ca-quiz", "Quiz")])

    # ---------- I. notions
    b = ("<p>L'énergie et la puissance sont deux notions qui, bien que liées, sont différentes. Mettons ces différences "
         "en évidence à partir des deux dispositifs de la figure 2.</p>" +
         svgfig(fig_palan_reservoir(), "Figure 2 — Notion de puissance et d'énergie (ou travail).",
                "Palan levant une charge de la hauteur h ; réservoir rempli par un robinet") +
         "<p>Pour remplir le réservoir, il faut fournir un certain volume <i>V</i> d'eau. De la même manière, pour lever "
         "la charge de masse <i>m</i> sur la hauteur <i>h</i>, il faut fournir une certaine quantité d'énergie <i>W</i>.</p>"
         "<p>Quelle que soit l'ouverture du robinet, c'est-à-dire quel que soit le débit d'eau, la quantité d'eau "
         "nécessaire au remplissage est toujours la même, <i>V</i>. De la même façon, si l'on ne tient pas compte du "
         "rendement (des pertes ou des fuites d'énergie), la quantité d'énergie à fournir pour lever la charge est la "
         "même quelle que soit la vitesse de levage.</p>"
         "<p>Plus le débit d'eau délivré par le robinet est élevé, plus vite le réservoir sera rempli. De même, plus la "
         "vitesse de levée de la charge est grande, plus la puissance fournie instantanément est grande et plus vite la "
         "charge sera levée.</p>"
         '<div class="remarque"><p><b>Le travail ou l\'énergie</b> représente ce qu\'il faut fournir globalement à un '
         "système pour l'amener d'un état initial à un état final. La manière dont le chemin est parcouru entre ces deux "
         "états n'a pas d'importance.</p><p><b>La puissance</b> caractérise le débit d'énergie fourni à chaque instant. "
         "Elle ne dépend ni de l'état initial ni de l'état final du système, mais permet de décrire les flots d'énergie "
         "entre ces deux états.</p></div>" +
         sim("Lever la même charge plus ou moins vite", "ca-palan",
             [("v", "Vitesse de levage (m/s)", 0.05, 0.5, 0.05, 0.1), ("h", "Hauteur de levage (m)", 1, 6, 0.5, 2)],
             [("w", "Énergie à fournir"), ("t", "Durée du levage"), ("p", "Puissance fournie")],
             '<p class="small">Charge de 1 000 daN (10 000 N). Change la vitesse : l\'énergie ne bouge pas, la durée et la '
             "puissance si.</p>"))
    s += A.course_section(1, "ca-notions", "Notions d'énergie et de puissance", b)

    # ---------- II. travail d'une force
    b = ("<h3>Travail élémentaire Δ<i>W</i> d'une force " + vec("F") + "</h3>"
         "<p>Le travail élémentaire Δ<i>W</i> de la force " + vec("F") + " dont le point d'application A se déplace de " +
         vec("Δl") + " entre A et A′ (" + vec("Δl") + " = " + vec("AA′") + ") est égal au produit scalaire de " + vec("F") +
         " par " + vec("Δl") + ".</p>" +
         formule(f"Δ<i>W</i> = {vec('F')}·{vec('Δl')} = <i>F</i>·Δ<i>l</i>·cos θ", "<i>W</i> en J (joules) ; <i>F</i> en N ; Δ<i>l</i> en m") +
         '<div class="cours-split"><div><p><b>Remarque :</b></p><ul>'
         "<li>si 0 ≤ θ &lt; 90° : cos θ &gt; 0, Δ<i>W</i> &gt; 0 : le travail de " + vec("F") + " est <b>moteur</b> ;</li>"
         "<li>si θ = 90° : cos θ = 0, Δ<i>W</i> = 0 : le travail de " + vec("F") + " est <b>nul</b> ;</li>"
         "<li>si 90° &lt; θ ≤ 180° : cos θ &lt; 0, Δ<i>W</i> &lt; 0 : le travail de " + vec("F") + " est <b>résistant</b>.</li></ul>"
         '<div class="simu" id="ca-theta"><h3>Fais tourner la force</h3><div class="simu-grid">'
         '<label>Angle θ entre ' + vec("F") + ' et ' + vec("Δl") + ' <output id="ca-theta-o"></output>'
         '<input type="range" id="ca-theta-r" min="0" max="180" step="5" value="40"></label></div>'
         '<p class="simu-verdict" id="ca-theta-v"></p></div></div>' +
         svgfig(fig_travail_theta(), "Figure 3 — Travail élémentaire : la projection de " + vec("F") + " sur le déplacement.",
                "Force F appliquée en A, déplacement de A à A′, angle θ", "0 0 480 270", 460) + "</div>"
         "<h3>Travail d'une force constante</h3>"
         "<p>La force " + vec("F") + " se déplace de A<sub>1</sub> à A<sub>2</sub> en conservant la même direction et "
         "la même intensité. La trajectoire A<sub>1</sub>A<sub>2</sub> peut être divisée en une infinité de petits "
         "déplacements élémentaires A<sub>1</sub>N<sub>1</sub>, N<sub>1</sub>N<sub>2</sub>, …, N<sub>n</sub>A<sub>2</sub>, "
         "dont la somme vaut " + vec("A₁A₂") + ". Le travail entre A<sub>1</sub> et A<sub>2</sub> s'écrit :</p>" +
         eq(f"<i>W</i><sub>1/2</sub> = {vec('F')}·{vec('A₁N₁')} + {vec('F')}·{vec('N₁N₂')} + … + {vec('F')}·{vec('NₙA₂')} = "
            f"{vec('F')}·({vec('A₁N₁')} + … + {vec('NₙA₂')}) = {vec('F')}·{vec('A₁A₂')}") +
         "<p>Le travail de " + vec("F") + " de A<sub>1</sub> à A<sub>2</sub> se ramène au produit scalaire de " + vec("F") +
         " par le déplacement " + vec("A₁A₂") + " :</p>" + formule(f"<i>W</i> = {vec('F')}·{vec('A₁A₂')}") +
         '<div class="exemple"><h3>Exemple : travail du poids ' + vec("P") + "</h3>"
         "<p>Un objet descend une rampe de forme quelconque de G<sub>1</sub> à G<sub>2</sub>.</p>" +
         svgfig(fig_rampe(), "Figure 4 — Travail des forces de pesanteur.", "Objet descendant une rampe courbe de G1 à "
                "G2, dénivellation h", maxw=440) +
         formule(f"<i>W</i><sub>1/2</sub> = {vec('P')}·{vec('G₁G₂')} = <i>P</i>·<i>h</i>") +
         "<p>Quelle que soit la trajectoire de G, le travail de " + vec("P") + " est égal au produit de <i>P</i> par la "
         "dénivellation <i>h</i>. Supposons que l'objet soit un skieur de 80 kg descendant une pente dont la différence "
         "de niveau est de 300 m entre le haut et le bas :</p>" +
         eq("<i>W</i> = 80 × 9,81 × 300 = 235 440 J = 235,4 kJ") +
         "<p><b>Remarque :</b> dans le cas de la figure 2, le travail de levage de la charge (1 000 daN) sur la hauteur "
         "<i>h</i> = 2 m est <i>W</i> = 10 000 × 2 = 20 000 J. Si le palan se déplace horizontalement sans lever la "
         "charge, le travail fourni est nul.</p></div>"
         "<h3>Travail d'une force dans le cas général</h3>"
         "<p><i>s</i>, abscisse curviligne, mesure le déplacement du point d'application A de la force " + vec("F") +
         " sur sa trajectoire : <i>s</i> = <i>s</i><sub>1</sub> en A<sub>1</sub>, <i>s</i> = <i>s</i><sub>2</sub> en "
         "A<sub>2</sub> ; AA′ = d<i>s</i> est le déplacement élémentaire de A. Entre A et A′ : d<i>W</i> = " + vec("F") +
         "·" + vec("ds") + " = <i>F</i>·d<i>s</i>·cos θ. Entre A<sub>1</sub> et A<sub>2</sub> :</p>" +
         formule(f"<i>W</i><sub>1/2</sub> = ∫<sub><i>s</i>₁</sub><sup><i>s</i>₂</sup> <i>F</i>·cos θ·d<i>s</i>",
                 "somme des travaux élémentaires ; graphiquement : l'aire sous la courbe <i>F</i>·cos θ en fonction de "
                 "<i>s</i> (cours 2)"))
    s += A.course_section(2, "ca-travail", "Travail d'une force", b)

    # ---------- II.4–5 couple et ressorts de torsion
    b = ('<div class="cours-split"><div><p>Le travail d\'un couple constant <i>C</i> se déplaçant de l\'angle θ est '
         "égal au produit de <i>C</i> par θ.</p>" +
         formule("<i>W</i> = <i>C</i>·θ", "<i>W</i> en J ; θ en rad ; <i>C</i> en N·m") + "</div>" +
         svgfig(fig_couple(), "Figure 5 — Travail d'un couple constant.", "Couple C faisant tourner un solide de la "
                "position 1 à la position 2, d'un angle θ", maxw=360) + "</div>"
         '<div class="exemple"><h3>Exemple</h3><p>Un moteur électrique tournant à 1 500 tr/min exerce un couple constant '
         "de 20 N·m sur un récepteur. Déterminons le travail réalisé par minute et par seconde.</p>" +
         eq("par minute : Δθ = 1 500 × 2π ≈ 9 425 rad ; Δ<i>W</i> = 20 × 9 425 ≈ 188,5 kJ",
            "par seconde : Δ<i>W</i>′ = Δ<i>W</i> / 60 ≈ 3 142 J") +
         "<p><b>Remarque :</b> dans la mesure où le couple est constant, Δ<i>W</i>′ est aussi égal à la puissance "
         "instantanée du moteur (3 142 W), en notant que 1 W = 1 J·s<sup>−1</sup>.</p></div>" +
         sim("Travail et puissance d'un moteur", "ca-mot",
             [("c", "Couple C (N·m)", 1, 100, 1, 20), ("n", "Vitesse N (tr/min)", 100, 3000, 100, 1500),
              ("d", "Durée (s)", 1, 120, 1, 60)],
             [("th", "Angle balayé"), ("w", "Travail"), ("p", "Puissance")]) +
         "<h3>Cas des ressorts de torsion</h3>"
         '<div class="cours-split"><div><p>Pour les ressorts de torsion (barre de torsion, cylindriques à spires et à '
         "spirale), le couple <i>C</i> supporté est fonction de l'angle d'enroulement α.</p>" +
         formule(f"<i>C</i> = <i>k</i>·α ; <i>W</i> = {frac('1', '2')}·<i>C</i>·α = {frac('1', '2')}·<i>k</i>·α²",
                 "<i>C</i> en N·m ; <i>k</i> en N·m·rad<sup>−1</sup> ; α en rad ; <i>W</i> en J") +
         "<p><b>Remarque :</b> <i>k</i> est la raideur du ressort ; <i>W</i>, le travail réalisé, est aussi l'énergie "
         "potentielle stockée ou restituée par le ressort.</p></div>" +
         svgfig(fig_ressort_torsion(), "Figure 6 — Exemple de ressort de torsion.", "Ressort de torsion à spires, "
                "branches écartées d'un angle α", maxw=340) + "</div>")
    s += A.course_section(3, "ca-couple", "Travail d'un couple constant ; ressorts de torsion", b)

    # ---------- III. énergie potentielle
    b = ("<p>Dans le cas d'un travail effectué par les forces de pesanteur ou par des forces engendrées par des "
         "ressorts, on parle d'énergie potentielle. Cette notion simplifie l'analyse des problèmes : le travail réalisé "
         "est indépendant des trajectoires et dépend uniquement des positions initiale et finale (forces dites "
         "<b>conservatives</b>).</p>"
         "<h3>Énergie potentielle de pesanteur</h3>"
         '<div class="cours-split"><div><p>L\'énergie potentielle dépend de l\'altitude <i>z</i> de l\'objet : plus '
         "l'objet est haut, plus il a d'énergie potentielle.</p>" +
         formule("<i>E</i><sub>p</sub> = <i>m</i>·<i>g</i>·<i>z</i>",
                 "<i>E</i><sub>p1</sub> − <i>E</i><sub>p2</sub> = <i>m</i>·<i>g</i>·(<i>z</i><sub>1</sub> − <i>z</i><sub>2</sub>) = <i>m</i>·<i>g</i>·<i>h</i>") +
         "</div>" + svgfig(fig_ep(), "Figure 7 — Énergie potentielle de pesanteur.", "Objet à l'altitude z1 puis z2, "
                           "dénivellation h", maxw=380) + "</div>"
         "<h3>Énergie potentielle élastique (ressort)</h3>"
         "<p>Charge sur le ressort : <i>F</i> = <i>k</i>·<i>f</i> = <i>k</i>·(<i>l</i><sub>0</sub> − <i>x</i>), avec "
         "<i>l</i><sub>0</sub> longueur libre (au repos), <i>x</i> longueur du ressort sous charge, <i>f</i> déformation "
         "(flèche) du ressort, <i>k</i> raideur du ressort.</p>"
         "<p>Travail élémentaire développé par une charge <i>F</i> comprimant le ressort : si <i>x</i><sub>1</sub> − "
         "<i>x</i><sub>2</sub> = d<i>x</i> est très petit, <i>F</i> varie très peu et Δ<i>W</i> = <i>F</i>·d<i>x</i>. "
         "Le travail total, entre les flèches <i>f</i><sub>1</sub> et <i>f</i><sub>2</sub>, est :</p>" +
         eq(f"<i>W</i><sub>1/2</sub> = ∫ <i>k</i>·<i>f</i>·d<i>f</i> = {frac('<i>k</i>', '2')}·(<i>f</i><sub>2</sub>² − <i>f</i><sub>1</sub>²)") +
         formule(f"<i>E</i><sub>p</sub> = {frac('<i>k</i>·<i>f</i>²', '2')} ; <i>E</i><sub>p2</sub> − <i>E</i><sub>p1</sub> = "
                 f"{frac('<i>k</i>', '2')}·(<i>f</i><sub>2</sub>² − <i>f</i><sub>1</sub>²)",
                 "<i>E</i><sub>p</sub> en J ; <i>k</i> en N·m<sup>−1</sup> ; <i>f</i> en m") +
         "<p>La compression du ressort permet d'accumuler de l'énergie potentielle. Pour les ressorts de torsion : "
         "<i>E</i><sub>p</sub> = ½·<i>k</i>·α² (α en rad, <i>k</i> en N·m·rad<sup>−1</sup>). Le travail du ressort est "
         "aussi l'aire sous la droite <i>F</i> = <i>k</i>·<i>f</i> : le cours 2 la fait varier à la souris.</p>")
    s += A.course_section(4, "ca-ep", "Énergie potentielle", b)

    # ---------- IV. énergie cinétique
    b = ("<p>On peut considérer l'énergie cinétique comme une sorte d'énergie potentielle liée à la vitesse de "
         "déplacement : plus un solide se déplace rapidement, plus il accumule d'énergie cinétique.</p>"
         "<h3>Solide en translation rectiligne</h3>"
         "<p>Tous les points du solide se déplacent à la même vitesse : " + vec("V") + " = " + vec("V") + "<sub>G</sub> = " +
         vec("V") + "<sub>M</sub> = … L'énergie cinétique d'un solide en translation rectiligne est égale à la moitié du "
         "produit de sa masse <i>m</i> par le carré de sa vitesse <i>V</i>.</p>" +
         formule(f"<i>E</i><sub>c</sub> = <i>T</i> = {frac('1', '2')}·<i>m</i>·<i>V</i>²", "<i>E</i><sub>c</sub> en J ; <i>m</i> en kg ; <i>V</i> en m·s<sup>−1</sup>") +
         '<div class="exemple"><h3>Exemple : énergie cinétique d\'un camion de 14 000 kg roulant à 108 km/h</h3>' +
         eq(f"<i>V</i> = {frac('108', '3,6')} = 30 m/s ; <i>E</i><sub>c</sub> = ½ × 14 000 × 30² = 6 300 000 J = 6 300 kJ") +
         "<p><b>Remarque :</b> si la vitesse du véhicule est divisée par deux (54 km/h), l'énergie cinétique est divisée "
         "par 4 (6 300 / 4 = 1 575 kJ), et inversement. Le travail des freins consiste à absorber de l'énergie "
         "cinétique pour ralentir le véhicule. En cas de choc, l'énergie cinétique accumulée est brutalement convertie "
         "en déformations (carrosserie…).</p></div>" +
         sim("Énergie cinétique d'un véhicule", "ca-ecv",
             [("m", "Masse (kg)", 500, 40000, 500, 14000), ("v", "Vitesse (km/h)", 10, 130, 2, 108)],
             [("vs", "Vitesse en m/s"), ("ec", "Énergie cinétique"), ("h", "Hauteur de chute équivalente")],
             '<p class="small">Hauteur de chute équivalente : celle d\'où il faudrait tomber pour atteindre la même '
             "vitesse (<i>m</i>·<i>g</i>·<i>h</i> = ½·<i>m</i>·<i>V</i>²).</p>") +
         "<h3>Solide en rotation par rapport à un axe fixe</h3>"
         "<p>Pour l'élément M de masse d<i>m</i> dont la vitesse est <i>V</i><sub>M</sub> = ω·<i>r</i>, l'énergie "
         "cinétique est ½·(ω·<i>r</i>)²·d<i>m</i>. Pour l'ensemble du solide : <i>E</i><sub>c</sub> = ½·ω²·Σ <i>r</i>²·d<i>m</i>. "
         "Le terme <i>J</i> = Σ <i>r</i>²·d<i>m</i> est le moment d'inertie par rapport à l'axe de rotation. L'énergie "
         "cinétique d'un solide en rotation est égale à la moitié du produit du moment d'inertie <i>J</i> (par rapport à "
         "son axe de rotation) par le carré de sa vitesse angulaire ω.</p>" +
         formule(f"<i>E</i><sub>c</sub> = <i>T</i> = {frac('1', '2')}·<i>J</i>·ω²", "<i>E</i><sub>c</sub> en J ; <i>J</i> en kg·m² ; ω en rad·s<sup>−1</sup>") +
         '<div class="exemple"><h3>Exemple : volant de presse</h3><div class="cours-split"><div>'
         "<p>Volant cylindrique (Ø 2 m, <i>h</i> = 0,5 m) tournant à 1 000 tr/min autour de son axe de révolution ; "
         "masse volumique de l'acier ρ = 7 800 kg·m<sup>−3</sup>.</p>" +
         eq("<i>m</i> = ρ·π·<i>R</i>²·<i>h</i> = 7 800 × π × 1² × 0,5 ≈ 12 252 kg",
            f"<i>J</i> = {frac('<i>m</i>·<i>R</i>²', '2')} = {frac('12 252 × 1²', '2')} = 6 126 kg·m²",
            f"<i>E</i><sub>c</sub> = ½·<i>J</i>·ω² = {frac('6 126', '2')} × ({frac('1 000·π', '30')})² ≈ 33 590 kJ") +
         "</div>" + svgfig(fig_volant(), "Figure 8 — Volant.", "Volant cylindrique de diamètre 2 000 mm et "
                           "d'épaisseur 500 mm, tournant à la vitesse ω", maxw=320) + "</div></div>" +
         sim("Énergie d'un volant d'inertie", "ca-vol",
             [("d", "Diamètre (m)", 0.2, 3, 0.1, 2), ("h", "Épaisseur (m)", 0.1, 1, 0.05, 0.5),
              ("n", "Vitesse (tr/min)", 100, 3000, 50, 1000)],
             [("m", "Masse"), ("j", "Moment d'inertie"), ("ec", "Énergie cinétique")],
             '<p class="small">Acier : ρ = 7 800 kg/m³. Doubler la vitesse quadruple l\'énergie ; doubler le diamètre la '
             "multiplie par 16 (masse × 4, rayon² × 4).</p>") +
         "<h3>Solide en mouvement plan</h3>"
         "<p><b>Définition 1</b></p>" +
         formule(f"<i>E</i><sub>c</sub> = <i>T</i> = {frac('1', '2')}·<i>m</i>·<i>V</i><sub>G</sub>² + {frac('1', '2')}·<i>J</i><sub>G</sub>·ω²",
                 "<i>V</i><sub>G</sub> : vitesse (absolue) du centre de gravité G (m/s) ; ω : vitesse angulaire du solide "
                 "(rad/s) ; <i>m</i> : masse (kg) ; <i>J</i><sub>G</sub> : moment d'inertie par rapport à un axe "
                 "perpendiculaire au plan du mouvement passant par G (kg·m²)") +
         "<p><b>Définition 2</b></p>" +
         formule(f"<i>E</i><sub>c</sub> = {frac('1', '2')}·<i>J</i><sub>I</sub>·ω² avec <i>J</i><sub>I</sub> = <i>J</i><sub>G</sub> + <i>m</i>·IG²",
                 "I : centre instantané de rotation ; <i>J</i><sub>I</sub> : moment d'inertie par rapport à l'axe "
                 "instantané de rotation (passant par I, perpendiculaire au plan du mouvement)") +
         '<div class="exemple"><h3>Exemple : disque plein roulant sans glisser</h3><div class="cours-split"><div>'
         "<p>Un disque plein, de masse <i>m</i> et de rayon <i>R</i>, roule sans glisser sur un plan horizontal à la "
         "vitesse angulaire ω. Le mouvement est un mouvement plan de centre instantané de rotation I (point de contact).</p>" +
         eq(f"<i>V</i><sub>G</sub> = ω·<i>R</i> ; <i>J</i><sub>G</sub> = {frac('<i>m</i>·<i>R</i>²', '2')}",
            f"<i>E</i><sub>c</sub> = ½·<i>m</i>·ω²·<i>R</i>² + ½·{frac('<i>m</i>·<i>R</i>²', '2')}·ω² = {frac('3·<i>m</i>·ω²·<i>R</i>²', '4')}") +
         "<p><b>Remarque :</b> par la définition 2, <i>E</i><sub>c</sub> = ½·(<i>J</i><sub>G</sub> + <i>m</i>·IG²)·ω² = "
         "½·(<i>m</i>·<i>R</i>²/2 + <i>m</i>·<i>R</i>²)·ω² = 3·<i>m</i>·ω²·<i>R</i>²/4 : le même résultat.</p></div>" +
         svgfig(fig_disque(), "Figure 9 — Disque plein roulant sans glisser sur un plan horizontal.",
                "Disque roulant : centre G, point de contact I, vitesse de G et du point haut", maxw=380) + "</div></div>")
    s += A.course_section(5, "ca-ec", "Énergie cinétique", b)

    # ---------- V. puissance
    b = ("<p>La puissance définit la quantité de travail effectué par unité de temps (par seconde), autrement dit le "
         "débit d'énergie.</p><h3>Puissance moyenne</h3>" +
         formule(f"<i>P</i><sub>m</sub> = {frac('Δ<i>W</i>', 'Δ<i>t</i>')}", "<i>P</i><sub>m</sub> en W (watts) ; "
                 "Δ<i>W</i> : travail réalisé pendant Δ<i>t</i> (J) ; Δ<i>t</i> en s") +
         "<h3>Puissance instantanée</h3>" +
         formule(f"<i>P</i> = lim<sub>Δ<i>t</i>→0</sub> {frac('Δ<i>W</i>', 'Δ<i>t</i>')} = {frac('d<i>W</i>', 'd<i>t</i>')}",
                 "1 watt = 1 joule / 1 seconde = 1 J·s<sup>−1</sup> ; autre unité usuelle : le cheval, 1 cv = 736 W") +
         "<p>Lorsque l'intervalle de temps Δ<i>t</i> devient très petit, la puissance moyenne tend vers la puissance "
         "instantanée.</p><h3>Puissance développée par une force " + vec("F") + "</h3>"
         '<div class="cours-split"><div><p>La puissance instantanée <i>P</i> développée par une force ' + vec("F") +
         " dont le point d'application A se déplace à la vitesse " + vec("V") + " sur sa trajectoire est égale au "
         "produit scalaire de " + vec("F") + " par " + vec("V") + ".</p>" +
         formule(f"<i>P</i> = {vec('F')}·{vec('V')} = <i>F</i>·<i>V</i>·cos θ", "<i>P</i> en W ; <i>F</i> en N ; <i>V</i> en m·s<sup>−1</sup>") +
         "<p><b>Remarques :</b> si <i>P</i> &gt; 0, la puissance est motrice (force motrice) ; si <i>P</i> &lt; 0, elle "
         "est résistante ou réceptive (force résistante). La vitesse " + vec("V") + " doit être une vitesse absolue "
         "(repère de référence lié à la Terre).</p></div>" +
         svgfig(fig_puissance_force(), "Figure 10 — Puissance d'une force.", "Force F et vitesse V du point A, tangente "
                "à la trajectoire, angle θ", maxw=360) + "</div>"
         '<div class="exemple"><h3>Exemple : le palan de la figure 2</h3><div class="cours-split"><div>'
         "<p>Le poids " + vec("P") + " de la charge est de 1 000 daN ; la vitesse de translation, en montée comme en "
         "descente, est de 0,1 m/s.</p>" +
         eq("Montée : <i>P</i> = " + vec("P") + "·" + vec("V") + " = <i>P</i>·<i>V</i>·cos 180° = 10 000 × 0,1 × (−1) = −1 000 W",
            "Descente : <i>P</i> = " + vec("P") + "·" + vec("V") + " = <i>P</i>·<i>V</i>·cos 0° = +1 000 W") +
         "<p>En montée, le poids est résistant : le palan doit fournir 1 000 W. En descente, il est moteur : le palan "
         "doit freiner la charge.</p></div>" +
         svgfig(fig_palan_montee(), "Figure 11 — Puissance développée par le poids, en montée et en descente.",
                "Charge levée puis descendue à vitesse constante, poids P et vitesse V", maxw=360) + "</div></div>"
         "<h3>Puissance développée par un couple <i>C</i></h3>"
         "<p>La puissance développée par un couple <i>C</i> se déplaçant à la vitesse angulaire ω est égale au produit "
         "de <i>C</i> par ω.</p>" +
         formule("<i>P</i> = <i>C</i>·ω", "<i>P</i> en W ; <i>C</i> en N·m ; ω en rad·s<sup>−1</sup>") +
         '<div class="exemple"><h3>Exemple</h3><p>Le moteur de la section 3 : couple constant de 20 N·m à 1 500 tr/min.</p>' +
         eq(f"<i>P</i> = <i>C</i>·ω = 20 × {frac('1 500 × π', '30')} ≈ 3 142 W") + "</div>"
         "<h3>Puissance d'un torseur d'action</h3>"
         "<p>Soit un torseur d'action {𝒯} dont le déplacement est défini par le torseur cinématique {𝒱}. La puissance "
         "développée est égale au produit (ou comoment) des deux torseurs :</p>" +
         formule(f"<i>P</i> = {{𝒯}}·{{𝒱}} = {vec('R')}·{vec('V')}<sub>A</sub> + {vec('M')}<sub>A</sub>·{vec('ω')}",
                 f"{{𝒯}} = ({vec('R')}, {vec('M')}<sub>A</sub>) ; {{𝒱}} = ({vec('ω')}, {vec('V')}<sub>A</sub>) ; le résultat "
                 "est indépendant du point A choisi pour écrire les torseurs"))
    s += A.course_section(6, "ca-puissance", "Puissance", b)

    # ---------- VI. rendement
    b = ('<div class="cours-split"><div><p>Le rendement η (êta) d\'une machine est égal au rapport de l\'énergie '
         "restituée sur l'énergie fournie (ou reçue).</p>" +
         formule(f"η = {frac('<i>W</i> restituée', '<i>W</i> fournie')} ≤ 1") +
         formule(f"η = {frac('<i>W</i> restituée − <i>W</i> perdue', '<i>W</i> fournie')} = 1 − {frac('<i>W</i> perdue', '<i>W</i> fournie')}") +
         "<p><b>Remarque :</b> l'énergie perdue peut l'être sous forme de chaleur, de frottements… Le rendement s'écrit "
         "aussi avec les puissances : η = <i>P</i><sub>utile</sub> / <i>P</i><sub>absorbée</sub>.</p></div>" +
         svgfig(fig_rendement(), "Figure 12 — Énergies fournie, restituée et perdue.", "Machine recevant W fournie, "
                "restituant W restituée et perdant de la chaleur", maxw=400) + "</div>" +
         sim("Rendement d'une machine", "ca-eta",
             [("f", "Puissance fournie (W)", 100, 5000, 100, 2000), ("u", "Puissance restituée (% de la fournie)", 10, 100, 1, 80)],
             [("r", "Puissance restituée"), ("p", "Puissance perdue"), ("e", "Rendement η")]))
    s += A.course_section(7, "ca-rendement", "Notion de rendement", b)

    # ---------- VII. théorèmes
    b = ("<h3>Théorème de l'énergie cinétique (ou de l'énergie-puissance)</h3>"
         "<p>Le théorème traduit sous forme énergétique les équations du principe fondamental de la dynamique. Il permet "
         "de déterminer des efforts dynamiques sans avoir à calculer les accélérations mises en jeu.</p>"
         '<div class="remarque"><p>En pratique, l\'application du théorème aboutit à une seule équation, alors que le '
         "principe fondamental conduit à trois équations de projection (dans le plan).</p></div>"
         "<p><b>Énoncé 1</b> : pour un solide isolé, le travail des forces extérieures pendant un intervalle de temps "
         "est égal à la variation de l'énergie cinétique du solide.</p>" +
         formule("<i>T</i><sub>2</sub> − <i>T</i><sub>1</sub> = [Δ<i>T</i>]<sub>1</sub><sup>2</sup> = [<i>W</i>(Σ<i>F</i><sub>ext</sub>)]<sub>1</sub><sup>2</sup>") +
         "<ul><li>Translation rectiligne : " + frac("<i>m</i>", "2") + "·(<i>V</i><sub>2</sub>² − <i>V</i><sub>1</sub>²) = [<i>W</i>(<i>F</i><sub>ext</sub>)]<sub>1</sub><sup>2</sup></li>"
         "<li>Rotation d'axe fixe : " + frac("<i>J</i>", "2") + "·(ω<sub>2</sub>² − ω<sub>1</sub>²) = [<i>W</i>(<i>F</i><sub>ext</sub>)]<sub>1</sub><sup>2</sup></li>"
         "<li>Mouvement plan : " + frac("<i>m</i>", "2") + "·(<i>V</i><sub>G2</sub>² − <i>V</i><sub>G1</sub>²) + " +
         frac("<i>J</i><sub>G</sub>", "2") + "·(ω<sub>2</sub>² − ω<sub>1</sub>²) = [<i>W</i>(<i>F</i><sub>ext</sub>)]<sub>1</sub><sup>2</sup></li></ul>"
         "<p><b>Énoncé 2</b> : pour un solide isolé, la dérivée de l'énergie cinétique est égale à la puissance "
         "développée par les forces extérieures.</p>" + formule(f"{frac('d<i>T</i>', 'd<i>t</i>')} = <i>P</i>(Σ<i>F</i><sub>ext</sub>)") +
         "<p><b>Remarque :</b> pour un ensemble de solides, au travail des forces extérieures à l'ensemble, il faut "
         "ajouter le travail des actions mutuelles exercées entre chacun des solides de l'ensemble.</p>"
         '<div class="exemple"><h3>Exemple : freinage d\'un tambour de frein à disque</h3><div class="cours-split"><div>'
         "<p>Un tambour (<i>J</i> = 100 kg·m² par rapport à son axe de rotation) tourne à la vitesse de 20 rad/s "
         "(≈ 190 tr/min). Le freinage est réalisé en 3 tours. Déterminons le couple de freinage <i>C</i>, supposé "
         "constant.</p><p><b>Résolution :</b> la variation d'énergie cinétique du tambour en rotation est :</p>" +
         eq(f"<i>T</i><sub>2</sub> − <i>T</i><sub>1</sub> = {frac('<i>J</i>', '2')}·(ω<sub>2</sub>² − ω<sub>1</sub>²) = {frac('100', '2')} × (0 − 20²) = −20 kJ") +
         "<p>La seule action extérieure fournissant un travail (résistant) au tambour isolé est le couple de freinage "
         "<i>C</i>. Toutes les autres actions (poids, actions des paliers) passent par l'axe de rotation et, de ce fait, "
         "ne produisent aucun travail.</p>" +
         eq("[<i>W</i>(<i>F</i><sub>ext</sub>)]<sub>1</sub><sup>2</sup> = −<i>C</i>·θ = −<i>C</i> × 2π × 3 (travail résistant)",
            "Théorème : −20 000 J = −6π·<i>C</i>, d'où <i>C</i> ≈ 1 061 N·m") +
         "<p><b>Remarque :</b> on a deux jeux de plaquettes de frein, au rayon de freinage <i>r</i> = 150 mm ; il en "
         f"résulte <i>F</i> = <i>C</i> / (2·<i>r</i>) = 1 061 / (2 × 0,15) ≈ 3 537 N et <i>N</i> = <i>F</i> / μ "
         "(μ coefficient de frottement).</p></div>" +
         svgfig(fig_frein_disque(), "Figure 13 — Exemple : frein à disque industriel.", "Tambour serré par deux "
                "plaquettes au rayon de 150 mm, efforts presseurs N et −N", maxw=380) + "</div></div>"
         "<h3>Loi de conservation de l'énergie</h3>"
         "<p><b>Loi</b> : pour un solide ou un système énergétiquement isolé, et dont les forces dépendent d'une énergie "
         "potentielle (forces de pesanteur, actions exercées par des ressorts), l'énergie mécanique totale mise en jeu "
         "reste constante entre deux instants successifs.</p>" +
         formule("<i>T</i><sub>2</sub> + <i>E</i><sub>p2</sub> = <i>T</i><sub>1</sub> + <i>E</i><sub>p1</sub> = constante",
                 "énergie mécanique totale : [Δ<i>T</i>]<sub>1</sub><sup>2</sup> + [Δ<i>E</i><sub>p</sub>]<sub>1</sub><sup>2</sup> = 0") +
         "<p>La loi de conservation de l'énergie est un cas particulier (intégrale première) du théorème précédent, "
         "obéissant à un certain nombre de conditions.</p><p><b>Remarque :</b> un système est énergétiquement isolé "
         "s'il n'échange aucune énergie avec son milieu extérieur : pas de pertes par frottement, etc.</p>"
         '<div class="simu" id="ca-tremplin"><h3>Le tremplin : l\'énergie se conserve</h3><div class="simu-grid">'
         '<label>Hauteur de départ <i>h</i> (m) <output id="ca-tremplin-h-o"></output><input type="range" id="ca-tremplin-h" min="10" max="90" step="5" value="40"></label>'
         '<label>Position du skieur sur la piste <output id="ca-tremplin-s-o"></output><input type="range" id="ca-tremplin-s" min="0" max="100" step="1" value="0"></label></div>'
         '<svg class="simu-svg fs" viewBox="0 0 480 220" id="ca-tremplin-svg" role="img" aria-label="Piste du tremplin, skieur et '
         'barres d\'énergie"><path class="mo" d="M440 30 L300 150 Q270 176 230 180 L120 180 L120 196 L440 196 Z"/>'
         '<circle id="ca-sk" r="9" class="mb" cx="440" cy="30"/><rect id="ca-bep" class="mb" x="30" width="26"/>'
         '<rect id="ca-bec" class="mo" x="64" width="26"/><line class="m" x1="24" y1="190" x2="96" y2="190"/>'
         '<text x="30" y="208" class="tb">Ep</text><text x="64" y="208" class="tr">Ec</text></svg>'
         '<div class="simu-out"><div><span>Énergie potentielle (skieur de 80 kg)</span><b id="ca-tremplin-ep">–</b></div>'
         '<div><span>Énergie cinétique</span><b id="ca-tremplin-ec">–</b></div><div><span>Vitesse</span><b id="ca-tremplin-v">–</b></div></div>'
         '<p class="small">Sans frottement, la somme Ep + Ec reste constante : au bas de la piste, ½·<i>m</i>·<i>v</i>² = '
         "<i>m</i>·<i>g</i>·<i>h</i>, soit <i>v</i> = √(2·<i>g</i>·<i>h</i>), indépendante de la masse.</p></div>")
    s += A.course_section(8, "ca-theoremes", "Théorèmes sur l'énergie", b)

    # ---------- l'essentiel, jeu, quiz
    cartes = "".join(f'<button type="button" class="carte" aria-expanded="false"><b>{t}</b><span class="dos">{d}<i>{x}</i></span></button>'
                     for t, d, x in ESSENTIEL)
    b = (f'<p>Retourne chaque carte pour revoir l\'essentiel.</p><div class="cartes">{cartes}</div>'
         "<h3>Jeu : quelle forme d'énergie ?</h3><p>Pour chaque situation, choisis la forme d'énergie stockée.</p>" +
         A.jeu_html(JEU_ENERGIES, CHOIX_ENERGIES, "ca-jeu"))
    s += A.course_section(9, "ca-essentiel", "L'essentiel à retenir", b)
    s += A.quiz_section(10, "ca-quiz", QUIZ, "caq")
    s += ('<div class="cours-foot"><a class="btn" href="?ex=cours-graphique">Cours 2 : résolution graphique</a>'
          '<a class="btn" href="?ex=formulaire-energetique">Formulaire</a>'
          '<a class="btn ghost" href="?">Retour à l\'accueil</a></div></div>')
    return s


JS = r"""
  function initCoursAnalytique(root) {
    function $(i) { return document.getElementById(i); }
    function val(i) { return parseFloat($(i).value); }
    function energie(w) { return Math.abs(w) >= 1e6 ? frs(w / 1e6, 3) + " MJ" : Math.abs(w) >= 1e3 ? frs(w / 1e3, 3) + " kJ" : frs(w, 3) + " J"; }
    function puiss(p) { return Math.abs(p) >= 1e3 ? frs(p / 1e3, 3) + " kW" : frs(p, 3) + " W"; }
    // palan : même énergie, durée et puissance selon la vitesse
    lier(root, "#ca-palan input", function () {
      var v = val("ca-palan-v"), h = val("ca-palan-h"), w = 10000 * h, t = h / v;
      $("ca-palan-v-o").textContent = fr(v, 2) + " m/s"; $("ca-palan-h-o").textContent = fr(h, 1) + " m";
      $("ca-palan-w").textContent = energie(w); $("ca-palan-t").textContent = fr(t, 1) + " s"; $("ca-palan-p").textContent = puiss(w / t);
    });
    // travail élémentaire : signe selon θ
    lier(root, "#ca-theta input", function () {
      var th = val("ca-theta-r"), a = th * Math.PI / 180, ax = 120, ay = 200, Lf = 130;
      var fx = ax + Lf * Math.cos(a), fy = ay - Lf * Math.sin(a), px = ax + Lf * Math.cos(a);
      $("ca-theta-o").textContent = th + "°";
      $("ca-f").setAttribute("d", flecheD(ax, ay, fx, fy, 12));
      $("ca-dl").setAttribute("d", flecheD(ax, ay, 380, ay, 12));
      $("ca-proj").setAttribute("d", "M" + fx + " " + fy + "L" + px + " " + ay);
      $("ca-fc").setAttribute("d", Math.abs(px - ax) > 1 ? "M" + ax + " " + (ay + 8) + "L" + px + " " + (ay + 8) : "");
      $("ca-fl").setAttribute("x", fx + 6); $("ca-fl").setAttribute("y", fy - 4);
      var r = 34, ex = ax + r * Math.cos(a), ey = ay - r * Math.sin(a);
      $("ca-arc").setAttribute("d", "M" + (ax + r) + " " + ay + "A" + r + " " + r + " 0 0 0 " + ex + " " + ey);
      $("ca-th").setAttribute("x", ax + 44 * Math.cos(a / 2) - 3); $("ca-th").setAttribute("y", ay - 44 * Math.sin(a / 2) + 4);
      var c = Math.cos(a), v = $("ca-theta-v");
      v.className = "simu-verdict " + (c > 1e-9 ? "ok" : (c < -1e-9 ? "ko" : ""));
      v.textContent = "cos θ = " + fr(c, 2) + " : " + (c > 1e-9 ? "ΔW > 0, travail moteur (la projection, en vert, va dans le sens du déplacement)."
        : (c < -1e-9 ? "ΔW < 0, travail résistant (la projection va contre le déplacement)." : "ΔW = 0, travail nul (force perpendiculaire au déplacement)."));
    });
    lier(root, "#ca-mot input", function () {
      var C = val("ca-mot-c"), N = val("ca-mot-n"), d = val("ca-mot-d"), w = N * Math.PI / 30, th = w * d;
      $("ca-mot-c-o").textContent = C + " N·m"; $("ca-mot-n-o").textContent = N + " tr/min"; $("ca-mot-d-o").textContent = d + " s";
      $("ca-mot-th").textContent = frs(th, 4) + " rad"; $("ca-mot-w").textContent = energie(C * th); $("ca-mot-p").textContent = puiss(C * w);
    });
    lier(root, "#ca-ecv input", function () {
      var m = val("ca-ecv-m"), v = val("ca-ecv-v") / 3.6, ec = 0.5 * m * v * v;
      $("ca-ecv-m-o").textContent = fr(m, 0) + " kg"; $("ca-ecv-v-o").textContent = val("ca-ecv-v") + " km/h";
      $("ca-ecv-vs").textContent = fr(v, 1) + " m/s"; $("ca-ecv-ec").textContent = energie(ec); $("ca-ecv-h").textContent = fr(v * v / 19.62, 1) + " m";
    });
    lier(root, "#ca-vol input", function () {
      var d = val("ca-vol-d"), h = val("ca-vol-h"), n = val("ca-vol-n"), r = d / 2, m = 7800 * Math.PI * r * r * h, J = m * r * r / 2, w = n * Math.PI / 30;
      $("ca-vol-d-o").textContent = fr(d, 1) + " m"; $("ca-vol-h-o").textContent = fr(h, 2) + " m"; $("ca-vol-n-o").textContent = n + " tr/min";
      $("ca-vol-m").textContent = fr(m, 0) + " kg"; $("ca-vol-j").textContent = frs(J, 4) + " kg·m²"; $("ca-vol-ec").textContent = energie(0.5 * J * w * w);
    });
    lier(root, "#ca-eta input", function () {
      var f = val("ca-eta-f"), u = val("ca-eta-u") / 100;
      $("ca-eta-f-o").textContent = f + " W"; $("ca-eta-u-o").textContent = Math.round(u * 100) + " %";
      $("ca-eta-r").textContent = puiss(f * u); $("ca-eta-p").textContent = puiss(f * (1 - u)); $("ca-eta-e").textContent = fr(u, 2);
    });
    // tremplin : position le long de la piste, conservation Ep + Ec
    lier(root, "#ca-tremplin input", function () {
      var h = val("ca-tremplin-h"), s = val("ca-tremplin-s") / 100, m = 80, g = 9.81;
      var x, y;  // piste : droite de (440, 30) à (300, 150), puis courbe jusqu'à (230, 180)
      if (s < 0.75) { var k = s / 0.75; x = 440 - 140 * k; y = 30 + 120 * k; }
      else { var q = (s - 0.75) / 0.25; x = (1 - q) * (1 - q) * 300 + 2 * q * (1 - q) * 270 + q * q * 230; y = (1 - q) * (1 - q) * 150 + 2 * q * (1 - q) * 176 + q * q * 180; }
      var z = h * (180 - y) / 150, ep = m * g * z, ec = m * g * (h - z), v = Math.sqrt(2 * g * (h - z));
      $("ca-sk").setAttribute("cx", x); $("ca-sk").setAttribute("cy", y - 10);
      var H = 150, e = m * g * h;
      $("ca-bep").setAttribute("y", 190 - H * ep / e); $("ca-bep").setAttribute("height", H * ep / e);
      $("ca-bec").setAttribute("y", 190 - H * ec / e); $("ca-bec").setAttribute("height", H * ec / e);
      $("ca-tremplin-h-o").textContent = h + " m"; $("ca-tremplin-s-o").textContent = Math.round(s * 100) + " %";
      $("ca-tremplin-ep").textContent = energie(ep); $("ca-tremplin-ec").textContent = energie(ec);
      $("ca-tremplin-v").textContent = fr(v, 1) + " m/s (" + fr(v * 3.6, 0) + " km/h)";
    });
    initCartes(root); initJeu(root.querySelector("#ca-jeu")); initQuiz(root.querySelector("#ca-quiz"));
  }
"""

CSS = """
/* ---------- cours 1 ---------- */
#ca-theta{flex:1 1 300px}
"""
