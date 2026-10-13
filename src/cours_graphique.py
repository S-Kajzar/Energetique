# -*- coding: utf-8 -*-
"""Cours 2 — Énergétique : résolution graphique (?ex=cours-graphique).

La partie « résolution graphique » du chapitre : le cours fourni pose les outils (travail d'une force variable comme
aire sous une courbe, figure du ressort ; produit scalaire, travail et puissance par projection ; vitesses d'un
solide en rotation et en mouvement plan, disque qui roule sans glisser) ; ce cours les rassemble en méthodes de
construction, ajoute les méthodes de cinématique graphique dont ont besoin les activités (répartition linéaire,
équiprojectivité, centre instantané de rotation) et le principe des puissances virtuelles, puis présente l'atelier de
construction des activités G1 à G4, avec une planche libre (sans note) pour s'exercer."""
import math

import construction as cg
from commun import eq, frac, vec, fr


def formule(main, units=""):
    return (f'<div class="formule"><span class="f-main">{main}</span>' +
            (f'<span class="f-units">{units}</span>' if units else "") + "</div>")


def demo(titre, ident, controles, svg, sorties, note="", vb="0 0 480 270"):
    ctr = "".join(
        (f'<label>{lab} <output id="{ident}-{k}-o"></output><input type="range" id="{ident}-{k}" min="{a}" max="{b}" '
         f'step="{s}" value="{v}"></label>') if a is not None else
        f'<label class="chk"><input type="checkbox" id="{ident}-{k}"{" checked" if v else ""}> {lab}</label>'
        for k, lab, a, b, s, v in controles)
    out = "".join(f'<div><span>{lab}</span><b id="{ident}-x{k}">–</b></div>' for k, lab in sorties)
    return (f'<div class="simu" id="{ident}"><h3>{titre}</h3><div class="simu-grid">{ctr}</div>'
            f'<svg class="simu-svg fs" viewBox="{vb}" role="img" aria-label="{titre}">{svg}</svg>'
            f'<div class="simu-out">{out}</div>' + (f'<p class="small">{note}</p>' if note else "") + "</div>")


# ============================================================ planche libre : bielle-manivelle
def planche_libre():
    O = (40.0, 110.0)
    r, Lb, a = 30.0, 100.0, math.radians(35)
    A = (O[0] + r * math.cos(a), O[1] - r * math.sin(a))
    B = (A[0] + math.sqrt(Lb ** 2 - (O[1] - A[1]) ** 2), O[1])
    M = cg.mul(cg.add(A, B), 0.5)
    vA = cg.mul((-math.sin(a), -math.cos(a)), 30)
    tA = cg.add(A, vA)
    I = cg.inter(O, cg.sub(A, O), B, (0, 1))
    w = 30 / cg.dist(I, A)

    def v(P):  # rotation autour de I, même sens que A
        d = cg.sub(P, I)
        s = 1 if (vA[0] * -d[1] + vA[1] * d[0]) * 0 + (cg.sub(A, I)[0] * vA[1] - cg.sub(A, I)[1] * vA[0]) > 0 else -1
        return cg.mul(cg.unit(cg.perp(d)), w * cg.norme(d) * s)
    vB = v(B)
    vM = v(M)
    fond = (cg.ligne((O[0] - 20, O[1]), (215, O[1]), "axe") + cg.cercle(O, r, "fin") + cg.pivot_fixe(O) +
            cg.poly([(B[0] - 12, O[1] - 8), (B[0] + 12, O[1] - 8), (B[0] + 12, O[1] + 8), (B[0] - 12, O[1] + 8)], "mb", True) +
            cg.ligne(O, A, "m") + cg.ligne(A, B, "m") + cg.articulation(A) + cg.articulation(B) +
            cg.point(O, "O", (-4, -3)) + cg.point(A, "A", (-1, 6)) + cg.point(B, "B", (2, -10)) + cg.point(M, "M", (1, 6)) +
            cg.fleche(A, tA) + cg.nom_vecteur((tA[0] - 2, tA[1] - 3), "V", "A", ancre="end") +
            cg.texte((60, 132), "manivelle OA, bielle AB, piston B guidé sur l'axe", "tc", "start"))
    corr = (cg.ligne(O, cg.add(O, cg.mul(cg.sub(I, O), 1.08)), "axe") + cg.ligne((B[0], 6), (B[0], 130), "axe") +
            cg.point(I, "I", (2, -2)) + cg.fleche(B, cg.add(B, vB)) +
            cg.nom_vecteur((B[0] + vB[0] / 2, B[1] + 8), "V", "B") + cg.ligne(I, M, "fin") + cg.fleche(M, cg.add(M, vM)) +
            cg.nom_vecteur((M[0] + vM[0] - 2, M[1] + vM[1] - 3), "V", "M", ancre="end"))
    cfg = cg.planche("libre", 220, 140, fond, points={"O": O, "A": A, "B": B, "M": M},
                     lignes=[{"a": O, "b": A, "nom": "OA"}, {"a": A, "b": B, "nom": "AB"},
                             {"a": (O[0] - 20, O[1]), "b": (215, O[1]), "inf": True, "nom": "axe"}],
                     vecteurs=[{"a": A, "b": tA, "nom": "VA"}], cercles=[{"c": O, "r": r}],
                     echelles={"L": (2, "mm", 0), "V": (0.05, "m/s", 2)}, corr=corr, libre=True,
                     aria="Bielle-manivelle : manivelle OA, bielle AB, piston B ; vitesse de A donnée",
                     legende="Planche libre : rien n'est noté. « Afficher la correction » superpose la construction attendue.")
    return cfg, cg.norme(vB) * 0.05, cg.norme(vM) * 0.05


PL_LIBRE, VB_LIBRE, VM_LIBRE = planche_libre()

QUIZ = [
    ("Sur une planche, l'échelle des vitesses est 1 mm ↔ 0,02 m/s. Un vecteur vitesse de 45 mm représente :",
     ["0,9 m/s", "2,25 m/s", "0,45 m/s"], 0, "45 × 0,02 = 0,9 m/s."),
    ("Le travail d'une force variable F(x) entre x₁ et x₂ se lit graphiquement comme :",
     ["la pente de la courbe", "l'aire sous la courbe entre x₁ et x₂", "la valeur de F en x₂"], 1,
     "W = ∫ F·dx : c'est l'aire comprise entre la courbe et l'axe des x."),
    ("Pour obtenir la puissance d'une force graphiquement, on projette :",
     ["la vitesse sur la direction de la force", "la force sur l'horizontale", "le point d'application sur le sol"], 0,
     "P = F × (projection de V sur la direction de F), ou V × (projection de F sur V)."),
    ("Dans un solide en rotation autour d'un axe fixe O, les extrémités des vitesses des points d'un même rayon sont :",
     ["sur un cercle de centre O", "alignées avec O", "toutes à la même distance"], 1,
     "V = ω·OM : la norme est proportionnelle à la distance à O (triangle des vitesses)."),
    ("L'équiprojectivité affirme que, pour deux points A et B d'un même solide :",
     ["V<sub>A</sub> = V<sub>B</sub>", "les projections de V<sub>A</sub> et V<sub>B</sub> sur (AB) sont égales",
      "V<sub>A</sub> et V<sub>B</sub> sont perpendiculaires"], 1, "Le solide est indéformable : la distance AB ne varie pas."),
    ("Le CIR d'un solide se trouve :", ["au centre de gravité", "à l'intersection des perpendiculaires aux vitesses",
                                        "toujours sur le bâti"], 1,
     "Chaque vitesse est perpendiculaire au rayon qui la relie au CIR."),
    ("Une roue roule sans glisser sur le sol. Son CIR est :", ["son centre", "le point de contact avec le sol",
                                                               "le point le plus haut"], 1,
     "Le point de contact a une vitesse nulle à cet instant : le point haut va deux fois plus vite que le centre."),
    ("Puissances virtuelles : le point d'entrée d'un levier va 3 fois plus vite que le point de sortie. L'effort de sortie est :",
     ["3 fois plus grand", "3 fois plus petit", "égal"], 0, "F<sub>e</sub>·V<sub>e</sub> = F<sub>s</sub>·V<sub>s</sub>."),
]


def render(A):
    s = A.course_head(
        "Cours 2", "Niveau 2", "Énergétique : résolution graphique",
        "Résoudre un problème d'énergétique en construisant à l'échelle : lire un travail comme une aire, une puissance "
        "par projection, construire les vitesses d'un mécanisme (répartition linéaire, équiprojectivité, centre "
        "instantané de rotation), puis conclure par le bilan des puissances. Avec l'atelier de construction des activités.")
    s += '<div class="cours">'
    s += ('<div class="remarque"><p>Le cours 1 calcule. Celui-ci <b>construit</b> : quand un mécanisme a une géométrie '
          "compliquée, les vitesses de ses points (et donc les puissances, les travaux) se trouvent plus vite et plus "
          "sûrement par une construction à l'échelle que par le calcul. La précision est celle du tracé, quelques "
          "pour cent : largement suffisante pour choisir un moteur ou dimensionner un vérin.</p></div>")
    s += A.course_nav([("cg-echelles", "Échelles"), ("cg-aire", "Travail et aire"), ("cg-proj", "Projection"),
                       ("cg-rotation", "Rotation"), ("cg-equi", "Équiprojectivité"), ("cg-cir", "CIR"),
                       ("cg-virtuel", "Puissances virtuelles"), ("atelier", "L'atelier"), ("cg-quiz", "Quiz")])

    b = ("<p>Une construction graphique représente chaque grandeur par une longueur. Il faut donc une échelle par "
         "nature de grandeur, choisie pour que la figure tienne sur la feuille et reste précise :</p>"
         "<ul><li><b>échelle des longueurs</b> : le mécanisme est dessiné à l'échelle (1 mm du dessin ↔ 0,1 m, par "
         "exemple) ;</li><li><b>échelle des vitesses</b> : 1 mm ↔ 0,005 m/s, par exemple ; un vecteur de 60 mm "
         "représente alors 0,3 m/s ;</li><li><b>échelle des efforts</b> : 1 mm ↔ 50 N, par exemple.</li></ul>"
         "<p>Bonnes pratiques : choisir des échelles simples (1, 2, 5 × 10<sup>n</sup>) ; donner aux vecteurs connus "
         "une longueur de 3 à 8 cm ; construire au crayon fin ; nommer chaque point construit ; lire le résultat en "
         "mesurant puis en convertissant. Dans l'atelier, chaque planche annonce ses échelles et l'outil Mesurer fait la "
         "conversion.</p>" +
         formule("valeur = longueur mesurée × échelle", "exemple : 56,4 mm × 0,005 m/s par mm = 0,282 m/s"))
    s += A.course_section(1, "cg-echelles", "Échelles et précision", b)

    svg_aire = ('<g id="cg-ai-grille"></g><path id="cg-ai-zone" fill="rgba(31,95,168,.25)" stroke="none"/>'
                '<line class="m" x1="60" y1="230" x2="450" y2="230"/><line class="m" x1="60" y1="230" x2="60" y2="20"/>'
                '<path class="m" id="cg-ai-droite"/><text x="440" y="250" class="tn">f</text>'
                '<text x="40" y="30" class="tn">F</text><text x="70" y="40" class="tc" id="cg-ai-leg"></text>')
    b = ("<p>Le cours 1 a établi le travail d'une force variable : <i>W</i><sub>1/2</sub> = ∫ <i>F</i>·cos θ·d<i>s</i>. "
         "Graphiquement, c'est l'<b>aire</b> comprise entre la courbe de l'effort utile et l'axe des déplacements. Pour "
         "un ressort, la charge croît linéairement avec la flèche (<i>F</i> = <i>k</i>·<i>f</i>) : l'aire entre "
         "<i>f</i><sub>1</sub> et <i>f</i><sub>2</sub> est un trapèze.</p>" +
         formule(f"<i>W</i><sub>1/2</sub> = aire du trapèze = {frac('<i>F</i><sub>1</sub> + <i>F</i><sub>2</sub>', '2')}·(<i>f</i><sub>2</sub> − <i>f</i><sub>1</sub>) = "
                 f"{frac('<i>k</i>', '2')}·(<i>f</i><sub>2</sub>² − <i>f</i><sub>1</sub>²)") +
         demo("Le travail d'un ressort, une aire", "cg-ai",
              [("k", "Raideur k (N/mm)", 2, 20, 1, 10), ("f1", "Flèche initiale f₁ (mm)", 0, 40, 1, 10),
               ("f2", "Flèche finale f₂ (mm)", 0, 40, 1, 30)], svg_aire,
              [("f", "Efforts F₁ et F₂"), ("w", "Aire = travail"), ("c", "Carreaux comptés")],
              "Un carreau du quadrillage vaut 5 mm × 50 N = 0,25 J : compter les carreaux donne l'ordre de grandeur, la "
              "formule du trapèze la valeur exacte. La même méthode vaut pour une courbe quelconque (découper l'aire en "
              "bandes)."))
    s += A.course_section(2, "cg-aire", "Le travail, une aire sous la courbe", b)

    svg_proj = ('<line class="fin" x1="20" y1="180" x2="460" y2="180"/><circle class="art" cx="140" cy="180" r="5"/>'
                '<path class="vb" id="cg-pj-v"/><path class="vr" id="cg-pj-vf"/><path class="pointille" id="cg-pj-p"/>'
                '<path id="cg-pj-c" stroke="#1B7A43" stroke-width="7" stroke-opacity=".55" fill="none"/>'
                '<text class="tn tb" x="330" y="172">V</text><text class="tn tr" id="cg-pj-fl">F</text>'
                '<text class="tn" x="124" y="204">A</text>')
    b = ("<p>Travail (<i>W</i> = " + vec("F") + "·" + vec("AB") + ") et puissance (<i>P</i> = " + vec("F") + "·" +
         vec("V") + ") sont des <b>produits scalaires</b>. Graphiquement, un produit scalaire est le produit de la norme "
         "d'un vecteur par la <b>projection orthogonale</b> de l'autre sur sa direction :</p>" +
         formule(f"{vec('F')}·{vec('V')} = <i>F</i>·<i>V</i>·cos θ = <i>V</i> × (projection de {vec('F')} sur {vec('V')}) "
                 f"= <i>F</i> × (projection de {vec('V')} sur {vec('F')})") +
         "<p>La projection se construit avec une perpendiculaire (outil Projeté de l'atelier). Le signe se lit sur le "
         "dessin : projection dans le sens du mouvement, puissance motrice ; en sens contraire, résistante.</p>" +
         demo("Puissance d'une force par projection", "cg-pj",
              [("t", "Angle θ entre F et V (°)", 0, 180, 5, 50), ("f", "Effort F (N)", 50, 300, 10, 200)], svg_proj,
              [("pr", "Projection de F sur V"), ("p", "Puissance (V = 2 m/s)"), ("s", "Nature")]) +
         '<div class="exemple"><h3>Le travail du poids ne dépend que de la dénivellation</h3>'
         "<p>Le poids est vertical : seule la projection verticale du déplacement compte. Quelle que soit la trajectoire "
         "(rampe courbe, rail incliné, escalier), <i>W</i> = ± <i>P</i>·<i>h</i>. De même, la puissance du poids est "
         "<i>P</i> × (composante verticale de la vitesse). Activité G1 : le skip de chargement.</p></div>")
    s += A.course_section(3, "cg-proj", "Le produit scalaire par projection", b)

    svg_rot = ('<circle class="mf" cx="150" cy="140" r="110"/><circle class="art" cx="150" cy="140" r="5"/>'
               '<text class="tn" x="132" y="134">O</text><line class="fin" x1="150" y1="140" x2="290" y2="140"/>'
               '<path class="pointille" id="cg-rot-arc"/><line class="axe" id="cg-rot-tri"/>'
               '<line class="fin" id="cg-rot-om"/><path class="vb" id="cg-rot-va"/><path class="vr" id="cg-rot-vm2"/>'
               '<path class="vr" id="cg-rot-vm"/><circle class="art" id="cg-rot-m" r="4"/><circle class="art" cx="250" cy="140" r="4"/>'
               '<text class="tn" x="244" y="160">A</text><text class="tn" id="cg-rot-ml">M</text>'
               '<text class="tn tb" x="256" y="70">V<tspan class="ind" dy="3">A</tspan></text>'
               '<text class="tc" x="300" y="40">droite O → extrémité de V</text><text class="tc" x="300" y="56">(triangle des vitesses)</text>')
    b = ("<p>Pour un solide en rotation autour d'un axe fixe O, chaque point M a une vitesse <b>perpendiculaire</b> au "
         "rayon OM et de norme <b>proportionnelle</b> à OM : <i>V</i><sub>M</sub> = ω·OM. Les extrémités des vitesses "
         "des points d'un même rayon sont donc alignées avec O : c'est la <b>répartition linéaire</b> des vitesses, ou "
         "<b>triangle des vitesses</b>.</p>"
         "<p><b>Construction</b> (une vitesse " + vec("V") + "<sub>A</sub> connue, M quelconque) :</p><ol>"
         "<li>ramener M sur le rayon OA : cercle de centre O passant par M (Compas) ; il coupe OA en M′ ;</li>"
         "<li>tracer la droite qui joint O à l'extrémité de " + vec("V") + "<sub>A</sub> ;</li>"
         "<li>en M′, la perpendiculaire à OA coupe cette droite : la longueur obtenue est <i>V</i><sub>M</sub> ;</li>"
         "<li>reporter cette longueur en M, perpendiculairement à OM, dans le sens de rotation (Report).</li></ol>" +
         demo("Triangle des vitesses d'un solide en rotation", "cg-rot",
              [("w", "Vitesse de A, V<sub>A</sub> (m/s)", 0.5, 2, 0.1, 1.2), ("r", "Distance OM (mm)", 20, 110, 5, 70),
               ("a", "Position angulaire de M (°)", 0, 340, 10, 120)], svg_rot,
              [("vm", "Vitesse de M"), ("om", "OM / OA"), ("w2", "ω")],
              "Rayon OA = 100 mm (dessin à l'échelle 1:1 ici). Toutes les vitesses tournent avec le solide, mais leur "
              "rapport ne dépend que des distances à O."))
    s += A.course_section(4, "cg-rotation", "Vitesses d'un solide en rotation : répartition linéaire", b)

    svg_bm = ('<line class="axe" x1="20" y1="180" x2="470" y2="180"/><circle class="fin" cx="110" cy="180" r="60"/>'
              '<rect class="mb" id="cg-bm-pis" width="56" height="34" rx="3"/><line class="m" id="cg-bm-oa"/>'
              '<line class="m" id="cg-bm-ab"/><circle class="art" cx="110" cy="180" r="5"/>'
              '<circle class="art" id="cg-bm-a" r="5"/><circle class="art" id="cg-bm-b" r="5"/>'
              '<g id="cg-bm-eq"><path class="pointille" id="cg-bm-p1"/><path class="pointille" id="cg-bm-p2"/>'
              '<path id="cg-bm-pa" stroke="#1B7A43" stroke-width="7" stroke-opacity=".55" fill="none"/>'
              '<path id="cg-bm-pb" stroke="#1B7A43" stroke-width="7" stroke-opacity=".55" fill="none"/></g>'
              '<g id="cg-bm-ci"><line class="axe" id="cg-bm-i1"/><line class="axe" id="cg-bm-i2"/>'
              '<circle class="art" id="cg-bm-i" r="4"/><text class="tn tr" id="cg-bm-il">I</text></g>'
              '<path class="vb" id="cg-bm-va"/><path class="vr" id="cg-bm-vb"/>'
              '<text class="tn" x="92" y="204">O</text><text class="tn" id="cg-bm-al">A</text><text class="tn" id="cg-bm-bl">B</text>')
    b = ("<p>Le solide est indéformable : la distance entre deux de ses points A et B ne change pas. Leurs vitesses ont "
         "donc la <b>même projection</b> sur la droite (AB).</p>" +
         formule(f"{vec('V')}<sub>A</sub>·{vec('AB')} = {vec('V')}<sub>B</sub>·{vec('AB')}") +
         "<p><b>Construction</b> (" + vec("V") + "<sub>A</sub> connue, direction de " + vec("V") + "<sub>B</sub> connue) :</p><ol>"
         "<li>projeter l'extrémité de " + vec("V") + "<sub>A</sub> sur (AB) (Projeté) ;</li>"
         "<li>reporter cette projection à partir de B, sur (AB), dans le même sens (Report) ;</li>"
         "<li>tracer la perpendiculaire à (AB) en ce point : elle coupe la direction de " + vec("V") + "<sub>B</sub> à "
         "l'extrémité de " + vec("V") + "<sub>B</sub>.</li></ol>"
         "<p>Exemple : la bielle-manivelle. A tourne autour de O (vitesse perpendiculaire à OA) ; le piston B est guidé "
         "sur l'axe (vitesse horizontale). L'équiprojectivité le long de la bielle AB donne la vitesse du piston.</p>" +
         demo("Bielle-manivelle : équiprojectivité et CIR", "cg-bm",
              [("t", "Angle de la manivelle (°)", 10, 170, 5, 50), ("e", "Montrer les projections (équiprojectivité)", None, None, None, True),
               ("c", "Montrer le CIR de la bielle", None, None, None, False)], svg_bm,
              [("va", "V<sub>A</sub> (manivelle)"), ("vb", "V<sub>B</sub> (piston)"), ("r", "Rapport V<sub>B</sub>/V<sub>A</sub>")],
              "Manivelle OA = 60 mm à 1 500 tr/min ; bielle AB = 200 mm. Le rapport des vitesses change avec la position : "
              "c'est lui qui fixe, par les puissances, le rapport des efforts."))
    s += A.course_section(5, "cg-equi", "Équiprojectivité", b)

    svg_disc = ('<line class="m" x1="20" y1="220" x2="460" y2="220"/><circle class="mb" cx="220" cy="140" r="80"/>'
                '<circle class="art" cx="220" cy="140" r="5"/><circle class="art" cx="220" cy="220" r="4"/>'
                '<text class="tn" x="206" y="134">G</text><text class="tn tr" x="226" y="240">I</text>'
                '<line class="fin" id="cg-disc-im"/><path class="vr" id="cg-disc-vm"/><path class="vb" id="cg-disc-vg"/>'
                '<circle class="art" id="cg-disc-m" r="4"/><text class="tn" id="cg-disc-ml">M</text>')
    b = ("<p>À chaque instant, un solide en mouvement plan tourne autour d'un point, son <b>centre instantané de "
         "rotation</b> (CIR) I : la vitesse de chaque point M est perpendiculaire à IM et proportionnelle à IM "
         "(<i>V</i><sub>M</sub> = ω·IM), comme pour une rotation autour d'un axe fixe.</p>"
         "<p><b>Construction</b> : le CIR est à l'intersection des perpendiculaires aux directions de deux vitesses. "
         "Pour la bielle (démonstration ci-dessus) : la perpendiculaire à " + vec("V") + "<sub>A</sub> en A est la droite "
         "(OA) ; la perpendiculaire à " + vec("V") + "<sub>B</sub> en B est la verticale de B. Les normes se transportent "
         "ensuite par le triangle des vitesses autour de I.</p>"
         "<p><b>Roulement sans glissement</b> : le point de contact avec le sol a une vitesse nulle, c'est le CIR. Le "
         "centre G va à ω·<i>R</i>, le point haut à 2·ω·<i>R</i> (cours 1, disque roulant). Deux roues dentées qui "
         "engrènent ont la même vitesse au point de contact de leurs cercles primitifs (activité G2).</p>" +
         demo("Disque roulant : le CIR au contact", "cg-disc", [("a", "Position du point M sur le disque (°)", 0, 350, 10, 60),
                                                                ("r", "Distance GM (% du rayon)", 0, 100, 5, 100)],
              svg_disc, [("im", "IM / R"), ("vm", "V<sub>M</sub> / V<sub>G</sub>"), ("d", "Direction")],
              "Pour tous les points, la vitesse est perpendiculaire au segment qui les relie au point de contact I."))
    s += A.course_section(6, "cg-cir", "Centre instantané de rotation", b)

    b = ("<p>Pour un mécanisme en équilibre (ou en mouvement uniforme, énergie cinétique constante) dont les liaisons "
         "sont parfaites (sans frottement), la somme des puissances des efforts extérieurs est nulle pour tout "
         "mouvement possible, réel ou imaginé (virtuel) : c'est le <b>principe des puissances virtuelles</b>, forme "
         "« en vitesse » du principe du travail virtuel.</p>" +
         formule("Σ <i>P</i>(efforts extérieurs) = 0 ⇒ <i>F</i><sub>e</sub>·<i>V</i><sub>e</sub> = <i>F</i><sub>s</sub>·<i>V</i><sub>s</sub>",
                 "avec des vitesses projetées sur les directions des efforts") +
         "<p>Le rapport des efforts est l'inverse du rapport des vitesses. Il suffit donc d'imaginer un petit mouvement "
         "du mécanisme, d'en construire les vitesses (à n'importe quelle échelle : seul leur rapport compte), et de "
         "conclure. Les efforts intérieurs et les actions des liaisons parfaites ne travaillent pas : ils "
         "n'apparaissent pas dans le bilan, et c'est tout l'intérêt de la méthode.</p>"
         '<div class="exemple"><h3>Exemples des activités</h3><ul>'
         "<li><b>Balancier</b> (G3) : la tige en B retient le poids en G ; <i>V</i><sub>G</sub> = 2·<i>V</i><sub>B</sub>, "
         "donc <i>F</i><sub>B</sub> = 2·<i>P</i>.</li>"
         "<li><b>Tire-bouchon</b> (G4) : la poignée va 3 fois plus vite que la vis ; l'effort sur le bouchon vaut 3 fois "
         "l'effort de l'opérateur.</li></ul></div>" +
         '<div class="simu" id="cg-lev"><h3>Levier : rapport des vitesses, rapport des efforts</h3><div class="simu-grid">'
         '<label>Bras d\'entrée a (mm) <output id="cg-lev-a-o"></output><input type="range" id="cg-lev-a" min="100" max="800" step="50" value="600"></label>'
         '<label>Bras de sortie b (mm) <output id="cg-lev-b-o"></output><input type="range" id="cg-lev-b" min="50" max="600" step="50" value="200"></label>'
         '<label>Effort d\'entrée F<sub>e</sub> (N) <output id="cg-lev-f-o"></output><input type="range" id="cg-lev-f" min="10" max="500" step="10" value="100"></label></div>'
         '<div class="simu-out"><div><span>Rapport V<sub>e</sub> / V<sub>s</sub></span><b id="cg-lev-r">–</b></div>'
         '<div><span>Effort de sortie F<sub>s</sub></span><b id="cg-lev-fs">–</b></div><div><span>Bilan des puissances</span>'
         '<b id="cg-lev-p">–</b></div></div><p class="small">Levier pivotant en O : V = ω·distance à O (répartition linéaire). '
         "Pour 1 rad/s, la puissance d'entrée égale la puissance de sortie.</p></div>")
    s += A.course_section(7, "cg-virtuel", "Le principe des puissances virtuelles", b)

    b = ("<p>Les activités de résolution graphique (G1 à G4) se font sur des <b>planches</b> à l'échelle : le mécanisme "
         "est dessiné, ses points sont nommés, les vecteurs connus sont tracés. Les outils de la barre construisent "
         "comme à la règle, à l'équerre et au compas :</p><ul>"
         "<li><b>Point</b>, <b>Segment</b>, <b>Droite</b> (par deux points), <b>Vecteur</b> (origine, puis extrémité : sa "
         "valeur s'affiche à l'échelle des vitesses) ;</li>"
         "<li><b>Compas</b> (centre, puis un point du cercle) et <b>Report</b> (une longueur, puis le centre où la "
         "reporter) ;</li>"
         "<li><b>Perpendiculaire</b> et <b>Parallèle</b> (la ligne de référence, puis le point de passage), "
         "<b>Projeté</b> (le point, puis la ligne) ;</li>"
         "<li><b>Mesurer</b> (longueur convertie avec toutes les échelles) et <b>Nommer</b> (un point placé : I1, H…).</li></ul>"
         "<p><b>Aimantation</b> : un clic près d'un point, d'une extrémité, d'une intersection ou d'une ligne s'y "
         "accroche (repère jaune) ; les constructions sont donc exactes. <b>Annuler</b>, <b>Rétablir</b>, <b>Gomme</b>, "
         "zoom et plein écran complètent la barre ; Échap abandonne un tracé commencé.</p>"
         "<p>Dans une activité, la planche relève ce qui est noté (la norme et la direction des vecteurs tracés depuis "
         "les points demandés, la position des points nommés) ; la question se valide comme les autres, puis la "
         "correction se superpose en rouge.</p>"
         '<h3>Planche libre : bielle-manivelle</h3><p>Rien n\'est noté ici. La vitesse de A est donnée.</p><ol>'
         "<li>Construis la vitesse du piston B par équiprojectivité le long de la bielle AB.</li>"
         "<li>Construis le CIR I de la bielle (perpendiculaires aux vitesses de A et de B) et nomme-le.</li>"
         "<li>Construis la vitesse du milieu M de la bielle (perpendiculaire à IM, triangle des vitesses).</li></ol>" +
         cg.rendu(PL_LIBRE, (), "planche libre") +
         f'<p class="small">Résultats attendus : <i>V</i><sub>B</sub> ≈ {fr(VB_LIBRE, 2)} m/s, <i>V</i><sub>M</sub> ≈ '
         f'{fr(VM_LIBRE, 2)} m/s (vitesse de A : 1,5 m/s).</p>')
    s += A.course_section(8, "atelier", "L'atelier de construction", b)
    s += A.quiz_section(9, "cg-quiz", QUIZ, "cgq")
    s += ('<div class="cours-foot"><a class="btn" href="?ex=cours-analytique">Cours 1 : approche analytique</a>'
          '<a class="btn" href="?ex=skip-chargement">Activité G1</a><a class="btn" href="?ex=formulaire-energetique">Formulaire</a>'
          '<a class="btn ghost" href="?">Retour à l\'accueil</a></div></div>')
    return s


JS = r"""
  function initCoursGraphique(root) {
    function $(i) { return document.getElementById(i); }
    function val(i) { return parseFloat($(i).value); }
    function set(i, at) { var e = $(i); for (var k in at) e.setAttribute(k, at[k]); }
    // ---------- aire sous la droite du ressort : 1 mm de flèche = 9 px ; 1 N = 0,2 px (F max 800 N)
    (function () {
      var g = $("cg-ai-grille");
      for (var i = 0; i <= 40; i += 5) svgEl("line", { x1: 60 + i * 9, y1: 230, x2: 60 + i * 9, y2: 70, "class": "fin", opacity: ".35" }, g);
      for (var j = 0; j <= 800; j += 50) svgEl("line", { x1: 60, y1: 230 - j * 0.2, x2: 420, y2: 230 - j * 0.2, "class": "fin", opacity: ".35" }, g);
    })();
    lier(root, "#cg-ai input", function () {
      var k = val("cg-ai-k"), f1 = val("cg-ai-f1"), f2 = val("cg-ai-f2"), a = Math.min(f1, f2), b = Math.max(f1, f2);
      function X(f) { return 60 + f * 9; } function Y(F) { return 230 - Math.min(F, 800) * 0.2; }
      $("cg-ai-k-o").textContent = k + " N/mm"; $("cg-ai-f1-o").textContent = f1 + " mm"; $("cg-ai-f2-o").textContent = f2 + " mm";
      set("cg-ai-droite", { d: "M60 230L" + X(40) + " " + Y(40 * k) });
      set("cg-ai-zone", { d: "M" + X(a) + " 230L" + X(a) + " " + Y(k * a) + "L" + X(b) + " " + Y(k * b) + "L" + X(b) + " 230Z" });
      var W = k / 2 * (b * b - a * a) / 1000;  // N/mm × mm² = N·mm → J
      $("cg-ai-xf").textContent = fr(k * f1, 0) + " N → " + fr(k * f2, 0) + " N";
      $("cg-ai-xw").textContent = (f2 >= f1 ? "" : "−") + fr(W, 2) + " J";
      $("cg-ai-xc").textContent = fr(W / 0.25, 1) + " carreaux";
      $("cg-ai-leg").textContent = f2 >= f1 ? "compression : travail reçu par le ressort" : "détente : travail rendu par le ressort";
    });
    // ---------- projection
    lier(root, "#cg-pj input", function () {
      var t = val("cg-pj-t") * Math.PI / 180, F = val("cg-pj-f"), ax = 140, ay = 180, k = 0.6;
      var fx = ax + F * k * Math.cos(t), fy = ay - F * k * Math.sin(t), pr = F * Math.cos(t);
      $("cg-pj-t-o").textContent = val("cg-pj-t") + "°"; $("cg-pj-f-o").textContent = F + " N";
      set("cg-pj-v", { d: flecheD(ax, ay, 320, ay, 12) }); set("cg-pj-vf", { d: flecheD(ax, ay, fx, fy, 12) });
      set("cg-pj-p", { d: "M" + fx + " " + fy + "L" + fx + " " + ay });
      set("cg-pj-c", { d: "M" + ax + " " + (ay + 7) + "L" + fx + " " + (ay + 7) });
      set("cg-pj-fl", { x: fx + 6, y: fy - 4 });
      $("cg-pj-xpr").textContent = fr(pr, 0) + " N"; $("cg-pj-xp").textContent = fr(pr * 2, 0) + " W";
      $("cg-pj-xs").textContent = pr > 0.5 ? "motrice" : (pr < -0.5 ? "résistante" : "nulle");
    });
    // ---------- triangle des vitesses (rotation autour de O ; OA = 100 px, 1 m/s ↔ 60 px)
    lier(root, "#cg-rot input", function () {
      var VA = val("cg-rot-w"), r = val("cg-rot-r"), a = val("cg-rot-a") * Math.PI / 180, O = [150, 140], la = VA * 60, lm = la * r / 100;
      $("cg-rot-w-o").textContent = fr(VA, 1) + " m/s"; $("cg-rot-r-o").textContent = r + " mm"; $("cg-rot-a-o").textContent = val("cg-rot-a") + "°";
      var M = [O[0] + r * Math.cos(a), O[1] - r * Math.sin(a)], Mp = [O[0] + r, O[1]], u = [-Math.sin(a), -Math.cos(a)];
      set("cg-rot-va", { d: flecheD(250, 140, 250, 140 - la, 11) });
      set("cg-rot-tri", { x1: O[0], y1: O[1], x2: O[0] + 125, y2: O[1] - 1.25 * la });
      set("cg-rot-vm2", { d: lm > 1 ? flecheD(Mp[0], Mp[1], Mp[0], Mp[1] - lm, 9) : "" });
      set("cg-rot-arc", { d: "M" + Mp[0] + " " + Mp[1] + "A" + r + " " + r + " 0 " + (a > Math.PI ? 1 : 0) + " 0 " + M[0] + " " + M[1] });
      set("cg-rot-om", { x1: O[0], y1: O[1], x2: M[0], y2: M[1] });
      set("cg-rot-vm", { d: lm > 1 ? flecheD(M[0], M[1], M[0] + u[0] * lm, M[1] + u[1] * lm, 11) : "" });
      set("cg-rot-m", { cx: M[0], cy: M[1] }); set("cg-rot-ml", { x: M[0] + 8, y: M[1] + 16 });
      $("cg-rot-xvm").textContent = fr(VA * r / 100, 2) + " m/s"; $("cg-rot-xom").textContent = fr(r / 100, 2);
      $("cg-rot-xw2").textContent = fr(VA / 0.1, 1) + " rad/s";
    });
    // ---------- bielle-manivelle : OA = 60 px (60 mm), AB = 200 px ; 1 m/s ↔ 4 px
    lier(root, "#cg-bm input", function () {
      var t = val("cg-bm-t") * Math.PI / 180, O = [110, 180], R = 60, L = 200, kv = 4;
      var A = [O[0] + R * Math.cos(t), O[1] - R * Math.sin(t)], B = [A[0] + Math.sqrt(L * L - Math.pow(O[1] - A[1], 2)), O[1]];
      var VA = 1500 * Math.PI / 30 * 0.06, va = [-Math.sin(t) * VA * kv, -Math.cos(t) * VA * kv];
      var u = [(B[0] - A[0]) / L, (B[1] - A[1]) / L], p = va[0] * u[0] + va[1] * u[1], vb = p / u[0];
      $("cg-bm-t-o").textContent = val("cg-bm-t") + "°";
      set("cg-bm-oa", { x1: O[0], y1: O[1], x2: A[0], y2: A[1] }); set("cg-bm-ab", { x1: A[0], y1: A[1], x2: B[0], y2: B[1] });
      set("cg-bm-a", { cx: A[0], cy: A[1] }); set("cg-bm-b", { cx: B[0], cy: B[1] }); set("cg-bm-pis", { x: B[0] - 28, y: O[1] - 17 });
      set("cg-bm-al", { x: A[0] - 20, y: A[1] - 6 }); set("cg-bm-bl", { x: B[0] + 6, y: B[1] + 30 });
      set("cg-bm-va", { d: flecheD(A[0], A[1], A[0] + va[0], A[1] + va[1], 11) });
      set("cg-bm-vb", { d: Math.abs(vb) > 1 ? flecheD(B[0], B[1], B[0] + vb, B[1], 11) : "" });
      var pa = [A[0] + u[0] * p, A[1] + u[1] * p], pb = [B[0] + u[0] * p, B[1] + u[1] * p];
      set("cg-bm-p1", { d: "M" + (A[0] + va[0]) + " " + (A[1] + va[1]) + "L" + pa[0] + " " + pa[1] });
      set("cg-bm-p2", { d: "M" + (B[0] + vb) + " " + B[1] + "L" + pb[0] + " " + pb[1] });
      set("cg-bm-pa", { d: "M" + A[0] + " " + A[1] + "L" + pa[0] + " " + pa[1] }); set("cg-bm-pb", { d: "M" + B[0] + " " + B[1] + "L" + pb[0] + " " + pb[1] });
      $("cg-bm-eq").style.display = $("cg-bm-e").checked ? "" : "none";
      // CIR de la bielle : intersection de (OA) et de la verticale de B
      var I = Math.abs(Math.cos(t)) > 0.05 ? [B[0], O[1] - (B[0] - O[0]) * Math.tan(t)] : null;
      $("cg-bm-ci").style.display = $("cg-bm-c").checked && I && I[1] > -400 && I[1] < 700 ? "" : "none";
      if (I) {
        set("cg-bm-i1", { x1: O[0], y1: O[1], x2: I[0], y2: I[1] }); set("cg-bm-i2", { x1: B[0], y1: O[1], x2: I[0], y2: I[1] });
        set("cg-bm-i", { cx: I[0], cy: I[1] }); set("cg-bm-il", { x: I[0] + 8, y: I[1] + 4 });
      }
      $("cg-bm-xva").textContent = fr(VA, 2) + " m/s"; $("cg-bm-xvb").textContent = fr(Math.abs(vb) / kv, 2) + " m/s";
      $("cg-bm-xr").textContent = fr(Math.abs(vb) / kv / VA, 2);
    });
    // ---------- disque roulant : CIR au point de contact I
    lier(root, "#cg-disc input", function () {
      var a = val("cg-disc-a") * Math.PI / 180, r = val("cg-disc-r") / 100 * 80, G = [220, 140], I = [220, 220], k = 1.1;
      var M = [G[0] + r * Math.cos(a), G[1] - r * Math.sin(a)], d = [M[0] - I[0], M[1] - I[1]], L = Math.sqrt(d[0] * d[0] + d[1] * d[1]);
      $("cg-disc-a-o").textContent = val("cg-disc-a") + "°"; $("cg-disc-r-o").textContent = val("cg-disc-r") + " %";
      set("cg-disc-im", { x1: I[0], y1: I[1], x2: M[0], y2: M[1] });
      set("cg-disc-vm", { d: L > 1 ? flecheD(M[0], M[1], M[0] - d[1] * k, M[1] + d[0] * k, 10) : "" });
      set("cg-disc-vg", { d: flecheD(G[0], G[1], G[0] + 80 * k, G[1], 10) });
      set("cg-disc-m", { cx: M[0], cy: M[1] }); set("cg-disc-ml", { x: M[0] + 6, y: M[1] - 6 });
      $("cg-disc-xim").textContent = fr(L / 80, 2); $("cg-disc-xvm").textContent = fr(L / 80, 2);
      $("cg-disc-xd").textContent = "perpendiculaire à IM";
    });
    lier(root, "#cg-lev input", function () {
      var a = val("cg-lev-a"), b = val("cg-lev-b"), F = val("cg-lev-f");
      $("cg-lev-a-o").textContent = a + " mm"; $("cg-lev-b-o").textContent = b + " mm"; $("cg-lev-f-o").textContent = F + " N";
      $("cg-lev-r").textContent = fr(a / b, 2); $("cg-lev-fs").textContent = fr(F * a / b, 0) + " N";
      $("cg-lev-p").textContent = fr(F * a / 1000, 1) + " W = " + fr(F * a / b * b / 1000, 1) + " W";
    });
    initQuiz(root.querySelector("#cg-quiz"));
  }
"""

CSS = """
/* ---------- cours 2 ---------- */
.simu-grid label.chk{flex-direction:row; align-items:center; gap:8px; font-weight:600}
"""
