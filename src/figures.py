# -*- coding: utf-8 -*-
"""Figures redessinées en SVG (les pages fournies sont des photographies du manuel, peu lisibles) : figures des
énoncés, et vignettes des deux cartes de l'accueil qui n'ont pas de figure d'origine (formulaire, étude à venir). Toutes sur un canevas de 480 × 270 (format des cartes) ;
la même figure sert de vignette (SVG autonome, style intégré) et de figure d'énoncé (SVG dans la page)."""
import math

from commun import esc

W, H = 480, 270
STYLE = """<style>
.m{fill:none;stroke:#1C2530;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.mf{fill:#E9ECE8;stroke:#1C2530;stroke-width:1.4;stroke-linejoin:round}
.mb{fill:#D9DFE6;stroke:#1C2530;stroke-width:1.4;stroke-linejoin:round}
.mo{fill:#F6E2C2;stroke:#1C2530;stroke-width:1.4;stroke-linejoin:round}
.fin{fill:none;stroke:#5A6670;stroke-width:1}
.axe{fill:none;stroke:#5A6670;stroke-width:.8;stroke-dasharray:14 3 2 3}
.h{stroke:#1C2530;stroke-width:1}
.art{fill:#fff;stroke:#1C2530;stroke-width:1.4}
text{font-family:system-ui,'Segoe UI',Roboto,Arial,sans-serif;font-size:13px;fill:#1C2530}
.tn{font-weight:700;font-style:italic}
.tc{font-size:11.5px;fill:#46525C}
.tr{fill:#B42318;font-weight:700}
.tb{fill:#1F5FA8;font-weight:700}
.ind{font-size:.72em;font-style:normal}
.vr{stroke:#B42318;fill:#B42318}.vb{stroke:#1F5FA8;fill:#1F5FA8}.vk{stroke:#1C2530;fill:#1C2530}.vv{stroke:#1B7A43;fill:#1B7A43}
.vr,.vb,.vk,.vv{stroke-width:2.2;stroke-linecap:round}
.vrl{stroke:#B42318;fill:none;stroke-width:2.2}.vbl{stroke:#1F5FA8;fill:none;stroke-width:2.2}
.cote{stroke:#5A6670;stroke-width:.9;fill:#5A6670}
.pointille{fill:none;stroke:#5A6670;stroke-width:1;stroke-dasharray:4 3}
</style>"""


def n(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def autonome(inner, fond="#FFFFFF"):
    """SVG autonome (vignettes et illustration de l'accueil, intégrées en data URI)."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{STYLE}'
            f'<rect width="{W}" height="{H}" fill="{fond}"/>{inner}</svg>')


def figure(inner, caption, alt, maxw=560):
    """Figure d'énoncé : le même dessin, dans la page (style de la page)."""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="fig fig-svg" style="max-width:{maxw}px"><svg class="fs" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{esc(alt)}">{inner}</svg>{cap}</figure>')


# ============================================================ primitives (pixels)
def L(a, b, cls="m"):
    return f'<line class="{cls}" x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}"/>'


def PL(pts, cls="m", ferme=False):
    tag = "polygon" if ferme else "polyline"
    return f'<{tag} class="{cls}" points="{" ".join(n(x) + "," + n(y) for x, y in pts)}"/>'


def C(c, r, cls="m"):
    return f'<circle class="{cls}" cx="{n(c[0])}" cy="{n(c[1])}" r="{n(r)}"/>'


def R(x, y, w, h, cls="mf", rx=0):
    return f'<rect class="{cls}" x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{rx}"/>'


def T(p, s, cls="", ancre="start", taille=None):
    st = f' style="font-size:{taille}px"' if taille else ""
    c = f' class="{cls}"' if cls else ""
    return f'<text{c} x="{n(p[0])}" y="{n(p[1])}" text-anchor="{ancre}"{st}>{s}</text>'


def F(a, b, cls="vr", h=10):
    """Flèche (vecteur) de a vers b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dy)
    h = min(h, Ln * 0.45)
    ux, uy = dx / Ln, dy / Ln
    bx, by = b[0] - ux * h, b[1] - uy * h
    return (f'<path class="{cls}" d="M{n(a[0])} {n(a[1])}L{n(b[0] - ux * h * 0.7)} {n(b[1] - uy * h * 0.7)}'
            f'M{n(b[0])} {n(b[1])}L{n(bx - uy * h * 0.38)} {n(by + ux * h * 0.38)}'
            f'L{n(bx + uy * h * 0.38)} {n(by - ux * h * 0.38)}Z"/>')


def V(p, lettre, ind="", cls="tr", ancre="start"):
    """Nom d'un vecteur : lettre surmontée d'une flèche, indice éventuel."""
    w = 8.5 * len(lettre)
    x0 = p[0] - (w / 2 if ancre == "middle" else (w if ancre == "end" else 0))
    col = {"tr": "#B42318", "tb": "#1F5FA8", "": "#1C2530", "tv": "#1B7A43"}.get(cls, "#1C2530")
    sub = f'<tspan class="ind" dy="3">{ind}</tspan>' if ind else ""
    return (T(p, f"{lettre}{sub}", f"tn {cls}".strip(), ancre) +
            f'<path d="M{n(x0)} {n(p[1] - 12)}h{n(w)}m-3 -2.4l3 2.4l-3 2.4" fill="none" stroke="{col}" stroke-width="1.2"/>')


def sol(a, b, cote=1):
    """Bâti : trait et hachures (cote = 1 : sous le trait, -1 : au-dessus)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dy)
    ux, uy = dx / Ln, dy / Ln
    nx, ny = -uy * cote, ux * cote
    hs = []
    s = 4
    while s < Ln:
        x, y = a[0] + ux * s, a[1] + uy * s
        hs.append(L((x, y), (x - ux * 6 + nx * 7, y - uy * 6 + ny * 7), "h"))
        s += 8
    return L(a, b) + "".join(hs)


def cote(a, b, s, decal=14, cls="tc"):
    """Cote entre a et b, décalée de decal vers la gauche du sens a → b, texte au milieu."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dy)
    ux, uy = dx / Ln, dy / Ln
    wx, wy = uy * decal, -ux * decal
    a2, b2 = (a[0] + wx, a[1] + wy), (b[0] + wx, b[1] + wy)
    m = ((a2[0] + b2[0]) / 2 + uy * 9, (a2[1] + b2[1]) / 2 - ux * 9 + 4)
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90 or ang < -90:
        ang += 180
    return (L(a, (a2[0] + uy * 4, a2[1] - ux * 4), "fin") + L(b, (b2[0] + uy * 4, b2[1] - ux * 4), "fin") +
            F(((a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2), a2, "cote", 7) +
            F(((a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2), b2, "cote", 7) +
            f'<text class="{cls}" x="{n(m[0])}" y="{n(m[1])}" text-anchor="middle" '
            f'transform="rotate({n(ang)} {n(m[0])} {n(m[1])})">{s}</text>')


def roue(c, r):
    return C(c, r, "mb") + C(c, r * 0.35, "art")


def pivot(p, r=5):
    x, y = p
    return (PL([(x, y), (x - 10, y + 16), (x + 10, y + 16)], "mf", True) + sol((x - 15, y + 16), (x + 15, y + 16)) +
            C(p, r, "art"))


def personnage(x, y, s=1.0, cls="m"):
    """Silhouette debout, pieds en (x, y)."""
    return (C((x, y - 52 * s), 6 * s, "mf") + L((x, y - 45 * s), (x, y - 20 * s), cls) +
            L((x, y - 20 * s), (x - 7 * s, y), cls) + L((x, y - 20 * s), (x + 7 * s, y), cls) +
            L((x, y - 40 * s), (x - 9 * s, y - 27 * s), cls) + L((x, y - 40 * s), (x + 9 * s, y - 27 * s), cls))


def skieur(x, y, ang=0, s=1.0):
    """Skieur accroupi, skis inclinés de ang degrés (sens trigonométrique), pieds en (x, y)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), -math.sin(a)
    sk = L((x - ux * 22 * s, y - uy * 22 * s), (x + ux * 26 * s, y + uy * 26 * s), "m")
    return (sk + L((x, y), (x - 4 * s, y - 14 * s)) + L((x - 4 * s, y - 14 * s), (x + 4 * s, y - 26 * s)) +
            L((x + 4 * s, y - 26 * s), (x - 2 * s, y - 38 * s), "m") + C((x, y - 44 * s), 5.5 * s, "mo") +
            L((x - 1 * s, y - 34 * s), (x + 12 * s, y - 28 * s)))


# ============================================================ accueil et cartes
def tremplin(lab=True):
    s = sol((60, 240), (470, 240))
    s += PL([(462, 68), (448, 76), (300, 190), (250, 222), (150, 222), (150, 232), (252, 232), (305, 198), (462, 82)],
            "mo", True)
    for x in (200, 300, 380, 440):
        y0 = 232 if x < 252 else (198 - (x - 305) * 0.74 if x > 305 else 215)
        s += L((x, y0), (x, 240), "m")
    s += skieur(438, 80, -38, 0.85) + skieur(205, 220, 0, 0.9)
    s += F((180, 196), (110, 196), "vr", 11) + V((112, 186), "v", "", "tr")
    s += PL([(70, 150), (100, 178), (150, 196)], "pointille")
    if lab:
        s += L((448, 76), (478, 76), "pointille") + L((470, 222), (478, 222), "pointille") + L((250, 222), (470, 222), "pointille")
        s += F((472, 140), (472, 78), "cote", 8) + F((472, 160), (472, 220), "cote", 8) + T((458, 154), "h", "tn")
        s += T((300, 100), "Énergie potentielle", "tb", "end") + T((300, 116), "m·g·h", "tc", "end")
        s += F((310, 120), (250, 168), "vb", 10) + T((40, 125), "Énergie cinétique", "tr") + T((40, 143), "½·m·v²", "tc")
    return s


def carte_formulaire():
    s = R(110, 20, 260, 234, "mf", 4) + R(110, 20, 260, 34, "mb", 4)
    s += T((240, 43), "Formulaire d'énergétique", "tn", "middle")
    lignes = ["W = F · AB · cos θ", "W = C · θ", "Ep = m · g · z", "Ec = ½ · m · V²", "Ec = ½ · J · ω²",
              "P = F · V · cos θ = C · ω", "η = W restituée / W fournie"]
    for i, t in enumerate(lignes):
        s += T((130, 78 + i * 25), t, "", "start", 14)
    return autonome(s)


def treuil(gris=False):
    s = sol((40, 230), (440, 230)) + R(60, 150, 90, 70, "mb", 6) + T((105, 192), "M", "tn", "middle")
    s += R(150, 172, 60, 26, "mf") + R(210, 160, 70, 50, "mf", 4) + T((245, 190), "réd.", "tc", "middle")
    s += L((280, 185), (330, 185)) + C((360, 185), 32, "mb") + C((360, 185), 6, "art")
    s += L((392, 185), (392, 70)) + R(370, 70, 44, 40, "mo", 2) + F((392, 112), (392, 160), "vr", 10)
    s += T((420, 150), "P", "tn tr")
    return s


def carte_etude():
    return autonome(treuil())


# ============================================================ figures des activités
def fig_qcm1():
    s = C((130, 140), 60, "mb") + C((130, 140), 8, "art") + L((130, 140), (190, 140), "fin")
    s += '<path class="vrl" d="M80 95 A68 68 0 0 1 182 100"/>' + F((176, 92), (184, 102), "vr", 10)
    s += T((125, 60), "C", "tn tr") + T((198, 150), "θ", "tn")
    s += sol((260, 210), (460, 210)) + R(300, 160, 90, 50, "mo", 3) + F((345, 140), (440, 140), "vb", 11)
    s += V((400, 128), "V", "", "tb") + T((320, 192), "m", "tn")
    s += T((130, 240), "travail d'un couple", "tc", "middle") + T((360, 240), "énergie cinétique", "tc", "middle")
    return s


def fig_qcm2():
    s = '<path class="fin" d="M30 220 Q140 120 240 150"/>' + C((140, 156), 5, "art")
    s += F((140, 156), (232, 128), "vb", 11) + F((140, 156), (190, 60), "vr", 11)
    s += V((236, 126), "V", "", "tb") + V((194, 60), "F", "", "tr") + T((166, 128), "θ", "tn")
    s += C((360, 140), 50, "mb") + C((360, 140), 7, "art")
    s += '<path class="vrl" d="M318 104 A58 58 0 0 1 404 106"/>' + F((398, 98), (406, 108), "vr", 10)
    s += T((356, 70), "C", "tn tr") + T((420, 150), "ω", "tn")
    s += T((140, 250), "puissance d'une force", "tc", "middle") + T((360, 250), "puissance d'un couple", "tc", "middle")
    return s


def fig_ascenseur():
    s = R(130, 20, 14, 236, "mf") + R(336, 20, 14, 236, "mf") + sol((120, 256), (360, 256))
    s += T((116, 150), "glissière fixe", "tc", "end")
    s += R(150, 90, 180, 150, "mb", 2) + L((240, 20), (240, 90), "m") + T((246, 50), "câble", "tc")
    s += personnage(285, 232) + T((168, 228), "cabine", "tc")
    s += F((200, 200), (200, 120), "vr", 11) + V((208, 132), "V", "", "tr") + T((208, 150), "1,2 m/s", "tc")
    s += T((360, 120), "m = 850 kg", "tn") + T((360, 140), "frottements", "tc") + T((360, 156), "40 daN", "tc")
    s += cote((462, 246), (462, 30), "25 m", 0)
    return s


def fig_escalier():
    s = sol((30, 230), (450, 230))
    a = math.radians(30)
    x0, y0, Ln = 90, 220, 300
    x1, y1 = x0 + Ln * math.cos(a), y0 - Ln * math.sin(a)
    s += PL([(x0 - 30, y0 + 6), (x1 + 30, y1 + 6), (x1 + 30, y1 + 24), (x0 - 30, y0 + 24)], "mb", True)
    pts = [(x0 - 30, y0)]
    k = 12
    for i in range(k + 1):
        x = x0 + Ln * math.cos(a) * i / k
        y = y0 - Ln * math.sin(a) * i / k
        pts += [(x, pts[-1][1]), (x, y)]
    pts.append((x1 + 30, y1))
    s += PL(pts, "m") + personnage(x0 + 110 * math.cos(a), y0 - 110 * math.sin(a) - 4)
    s += F((x0 + 30, y0 + 40), (x0 + 120, y0 - 12), "vr", 10) + V((x0 + 70, y0 + 30), "V", "", "tr")
    s += L((x1, y1), (x1 + 50, y1), "pointille") + cote((x1 + 40, y0), (x1 + 40, y1), "h = 5 m", 0)
    s += '<path class="fin" d="M150 220 A60 60 0 0 0 142 190"/>' + T((156, 212), "30°", "tc")
    s += T((300, 60), "36 personnes par minute", "tc") + T((300, 76), "60 daN par personne", "tc")
    return s


def fig_remonte():
    s = sol((20, 240), (460, 240)) + PL([(40, 240), (440, 60), (470, 60)], "mo")
    s += L((40, 228), (440, 50), "fin")
    for i in range(1, 6):
        x = 40 + 400 * i / 6
        y = 240 - 180 * i / 6
        s += L((x, y - 12 + 0), (x, y - 50), "m") if i in (2, 4) else ""
        s += skieur(x, y - 3, 24, 0.6)
    s += F((150, 205), (230, 169), "vr", 10) + V((176, 214), "V", "", "tr") + T((196, 214), "= 120 m/min", "tc")
    s += cote((40, 240), (440, 60), "L = 1 800 m", 26)
    s += L((440, 60), (440, 240), "pointille") + cote((455, 240), (455, 60), "600 m", 0)
    s += T((60, 60), "1 200 skieurs par heure", "tc") + T((60, 76), "70 kg par skieur", "tc")
    return s


def fig_bateau():
    s = '<path class="mb" d="M60 140 L400 140 L370 200 L100 200 Z"/>' + R(170, 100, 120, 40, "mf", 3)
    s += '<path class="fin" d="M20 170 q20 -8 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0"/>'
    s += C((80, 210), 12, "mo") + L((80, 210), (110, 196))
    s += F((260, 70), (380, 70), "vb", 11) + V((300, 60), "V", "", "tb") + T((330, 60), "= 15 nœuds", "tc")
    s += F((440, 175), (405, 175), "vr", 10) + V((424, 166), "R", "", "tr")
    s += T((200, 124), "turbine", "tc") + T((40, 245), "hélice", "tc")
    return s


def wagonnet(x, y, ang, s=1.0, txt="m = 300 kg"):
    """Wagonnet posé sur un rail incliné de ang degrés (descendant vers la droite), roues en (x, y)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = uy, -ux

    def p(u, v):
        return (x + ux * u * s + nx * v * s, y + uy * u * s + ny * v * s)
    caisse = PL([p(-55, 14), p(55, 14), p(62, 60), p(-62, 60)], "mb", True)
    return caisse + roue(p(-30, 10), 10 * s) + roue(p(30, 10), 10 * s) + T(p(-30, 36), txt, "tc")


def fig_amortisseur(pente="10°", ang=10, texte_v="V = 2 m/s", course="c = 100 mm"):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    x0, y0 = 30, 120
    pt = lambda d: (x0 + ux * d, y0 + uy * d)
    s = L(pt(0), pt(420), "m") + L((x0, y0), (x0 + 120, y0), "pointille") + T((x0 + 50, y0 + 18 + 0), pente, "tc")
    s += wagonnet(*pt(170), ang)
    s += F(pt(120)[:1] + (pt(120)[1] - 90,), (pt(200)[0], pt(200)[1] - 90), "vr", 10)
    s += T((pt(150)[0], pt(150)[1] - 100), texte_v, "tr")
    b0, b1 = pt(330), pt(410)
    s += PL([(b0[0], b0[1] - 18), (b1[0], b1[1] - 18), (b1[0], b1[1] - 46), (b0[0], b0[1] - 46)], "mf", True)
    zz = [(b0[0] + (b1[0] - b0[0]) * i / 10, b0[1] - 32 + (b1[1] - b0[1]) * i / 10 + (8 if i % 2 else -8)) for i in range(11)]
    s += PL(zz, "m") + L((b0[0] - 30, b0[1] - 32), (b0[0], b0[1] - 32)) + R(b0[0] - 34, b0[1] - 44, 6, 24, "art")
    s += T((b0[0] + 10, b0[1] - 56), "amortisseur à ressort", "tc")
    s += cote((b0[0] - 34, b0[1] + 6), (b0[0], b0[1] + 6), course, -16)
    return s


def fig_wagon_pente():
    return fig_amortisseur("2 %", 6, "départ arrêté, 20 m avant le contact", "course x")


def fig_auto():
    a = math.radians(14)
    ux, uy = math.cos(a), math.sin(a)
    x0, y0 = 20, 90
    pt = lambda d: (x0 + ux * d, y0 + uy * d)
    s = L(pt(0), pt(470)) + L(pt(0), (x0 + 200, y0), "pointille")
    s += T((x0 + 70, y0 + 6 + 14), "pente 10 %", "tc")
    c = pt(130)
    nx, ny = uy, -ux

    def q(u, v):
        return (c[0] + ux * u + nx * v, c[1] + uy * u + ny * v)
    s += PL([q(-70, 12), q(70, 12), q(72, 30), q(30, 34), q(10, 52), q(-40, 52), q(-62, 34), q(-74, 30)], "mo", True)
    s += roue(q(-45, 10), 12) + roue(q(45, 10), 12)
    s += F(q(-20, 80), q(60, 80), "vr", 10) + T(q(-10, 92), "90 km/h", "tr")
    s += cote(pt(170), pt(420), "distance d'arrêt x", 16)
    s += T((300, 60), "m = 1 000 kg", "tc") + T((300, 76), "freinage : 2 500 N", "tc")
    return s


def fig_verin(balancier=False):
    s = sol((150, 20), (330, 20), -1) + C((240, 34), 9, "art")
    s += R(222, 42, 36, 96, "mb", 2) + R(226, 104, 28, 8, "mf") + L((240, 112), (240, 180))
    s += L((222, 64), (205, 64)) + T((200, 68), "air", "tc", "end") + L((258, 124), (276, 124)) + T((280, 128), "huile", "tc")
    if not balancier:
        s += C((240, 186), 6, "art") + R(205, 192, 70, 44, "mf", 2)
        s += F((300, 140), (300, 200), "vr", 10) + V((306, 172), "V", "", "tr") + T((306, 188), "0,3 m/s", "tc")
        s += F((250, 214), (250, 262), "vk", 9) + V((258, 252), "P", "", "") + T((270, 252), "3 000 daN", "tc")
    return s


def fig_frein_sabot(deux=False):
    s = C((250, 170), 70, "mb") + C((250, 170), 28, "mf") + pivot((250, 170), 6)
    s += '<path class="vbl" d="M170 150 A82 82 0 0 1 200 100"/>' + F((196, 106), (202, 98), "vb", 9)
    s += T((168, 120), "ω", "tn tb")
    if not deux:
        s += pivot((60, 84), 6) + PL([(60, 84), (110, 74), (430, 74)], "m")
        s += R(212, 74, 76, 22, "mo") + F((430, 30), (430, 72), "vr", 10) + V((438, 44), "F", "", "tr")
        s += cote((60, 74), (250, 74), "600", 26) + cote((250, 74), (430, 74), "800", 26)
        s += T((70, 120), "A", "tn") + T((296, 92), "sabot", "tc")
    else:
        for sgn in (1, -1):
            x = 250 + sgn * 92
            s += R(x - 11 - (sgn - 1) * 0, 136, 22, 68, "mo") if True else ""
            s += L((x, 236), (x, 40)) + pivot((x, 236), 5) + F((x + sgn * 34, 50), (x + sgn * 2, 50), "vr", 9)
        s += T((380, 46), "F", "tn tr") + T((106, 46), "F", "tn tr")
    s += L((250, 170), (300, 120), "fin") + T((290, 140), "r = 360", "tc")
    return s


def fig_skip():
    s = sol((30, 250), (460, 250))
    a = math.radians(70)
    x0, y0 = 150, 250
    top = (x0 + 220 * math.cos(a), y0 - 220 * math.sin(a))
    s += L((x0, y0), top, "m") + L((x0 + 12, y0), (top[0] + 12, top[1]), "m")
    s += '<path class="fin" d="M182 250 A32 32 0 0 0 163 220"/>' + T((186, 236), "70°", "tc")
    g = (x0 + 110 * math.cos(a) + 30, y0 - 110 * math.sin(a))
    s += PL([(g[0] - 20, g[1] - 26), (g[0] + 26, g[1] - 26), (g[0] + 18, g[1] + 14), (g[0] - 14, g[1] + 14)], "mo", True)
    s += F(g, (g[0] + 40 * math.cos(a), g[1] - 40 * math.sin(a)), "vb", 10) + V((g[0] + 20, g[1] - 44), "V", "", "tb")
    s += F((g[0] + 4, g[1]), (g[0] + 4, g[1] + 60), "vr", 10) + V((g[0] + 12, g[1] + 56), "P", "", "tr")
    s += cote((x0, y0), top, "15 m", -30) + T((300, 80), "vidage", "tc") + T((300, 110), "P = 300 daN", "tc")
    s += T((300, 126), "V = 0,3 m/s", "tc")
    return s


def engrenage(c, r, z, cls="mb"):
    pts = []
    for i in range(z * 2):
        a = math.pi * i / z
        rr = r + (5 if i % 2 == 0 else -5)
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    return PL(pts, cls, True) + C(c, 6, "art")


def fig_roues():
    s = engrenage((150, 140), 50, 12, "mf") + engrenage((280, 140), 125 * 0.66, 30, "mo")
    s += T((140, 70), "roue A", "tc") + T((300, 40), "roue B", "tc")
    s += '<path class="vrl" d="M110 92 A62 62 0 0 1 170 78"/>' + F((164, 76), (174, 80), "vr", 9)
    s += V((104, 84), "C", "A", "tr") + L((150, 140), (150, 190), "fin") + T((156, 172), "rA", "tc")
    s += L((280, 140), (360, 140), "fin") + T((320, 132), "rB", "tc")
    return s


def fig_balancier():
    s = fig_verin(True)
    s += L((240, 180), (240, 200)) + C((240, 204), 5, "art")
    s += R(162, 196, 296, 18, "mf") + pivot((170, 214), 5) + T((156, 210), "A", "tn", "end")
    s += T((246, 232), "B", "tn") + F((310, 214), (310, 262), "vk", 9) + V((318, 254), "P", "", "")
    s += T((330, 254), "5 000 daN en G", "tc") + F((290, 150), (290, 190), "vr", 9) + T((296, 168), "0,3 m/s", "tc")
    s += cote((170, 196), (240, 196), "1 m", 12) + cote((240, 196), (310, 196), "1 m", 12)
    return s


def tire_bouchon_geom(x0=150, y0=135, u=34, yv=54, c=18):
    """Pantographe du tire-bouchon (pixels) : collier en x0, axe en y0 ; demi-pas u, demi-hauteur yv."""
    x1 = u * (yv - c) / yv
    P = {"C1": (x0, y0 - c), "C2": (x0, y0 + c)}
    xs = [x0 + x1 + k * u for k in range(6)]
    P["P1"], P["Q1"] = (xs[0], y0 - yv), (xs[0], y0 + yv)
    P["D"] = (xs[1], y0)
    P["P2"], P["Q2"] = (xs[2], y0 - yv), (xs[2], y0 + yv)
    P["E"] = (xs[3], y0)
    P["P3"], P["Q3"] = (xs[4], y0 - yv), (xs[4], y0 + yv)
    P["H"] = (xs[5], y0)
    return P


def fig_tirebouchon():
    P = tire_bouchon_geom()
    s = R(126, 108, 22, 54, "mf", 3) + T((96, 104), "bouteille", "tc")
    s += PL([(40, 130), (148, 128), (P["D"][0], 132), (P["D"][0], 138), (148, 142), (40, 140)], "mb", True)
    for x in range(48, 140, 12):
        s += L((x, 124), (x + 6, 146), "fin")
    bars = [("C1", "P1"), ("C2", "Q1"), ("P1", "Q2"), ("Q1", "P2"), ("P2", "Q3"), ("Q2", "P3"), ("P3", "H"), ("Q3", "H")]
    for a, b in bars:
        s += L(P[a], P[b], "m")
    for k in ("C1", "C2", "P1", "Q1", "D", "P2", "Q2", "E", "P3", "Q3", "H"):
        s += C(P[k], 3.5, "art")
    s += L(P["H"], (P["H"][0] + 60, P["H"][1])) + L((P["H"][0] + 60, 95), (P["H"][0] + 60, 175))
    s += F((P["H"][0] + 64, 135), (P["H"][0] + 110, 135), "vr", 10) + V((P["H"][0] + 92, 126), "F", "", "tr")
    s += T((P["H"][0] + 52, 152), "A", "tn") + T((P["D"][0] + 4, 126), "D", "tn")
    s += F((40, 135), (8, 135), "vr", 10) + V((14, 126), "T", "", "tr")
    return s
