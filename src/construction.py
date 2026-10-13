# -*- coding: utf-8 -*-
"""Atelier de construction graphique : planches à l'échelle pour la cinématique et l'énergétique graphiques.

Une planche est un dessin SVG coté en millimètres (le mécanisme, ses points nommés, les vecteurs donnés) sur lequel
l'élève construit avec des outils de géométrie : point, segment, droite, vecteur, cercle (compas), perpendiculaire,
parallèle, projeté orthogonal, mesure à l'échelle, nom d'un point. Les tracés s'aimantent aux points, aux
extrémités, aux intersections et aux lignes. Rien n'est tracé à main levée : une construction juste donne un
résultat exact, à la précision du clic près.

Lien avec le gabarit (même principe que les étiquettes du dépôt « Chaîne fonctionnelle ») : une question de
construction est une question à plusieurs cases du gabarit (mécanisme « fast-q ») dont les champs sont masqués ;
la planche y écrit ce qu'elle relève sur le tracé (norme et direction d'un vecteur à l'échelle, écart d'un point
nommé à sa position attendue) et le moteur Grading les corrige comme toute autre case : modes entraînement et
examen, note pondérée, récapitulatif et impression sont ceux du gabarit. Une fois la question corrigée, la planche
se verrouille et la correction (tracée en rouge) se superpose au tracé de l'élève.
"""
import html
import json
import math

from commun import fr, sig

CORR = "#C62828"  # couleur des corrections, celle des tracés du gabarit


# ============================================================ géométrie (calcul des corrections)
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def norme(a):
    return math.hypot(a[0], a[1])


def unit(a):
    n = norme(a)
    return (a[0] / n, a[1] / n)


def perp(a):
    return (-a[1], a[0])


def dist(a, b):
    return norme(sub(a, b))


def inter(p1, d1, p2, d2):
    """Intersection des droites (p1, d1) et (p2, d2)."""
    den = d1[0] * d2[1] - d1[1] * d2[0]
    w = sub(p2, p1)
    t = (w[0] * d2[1] - w[1] * d2[0]) / den
    return add(p1, mul(d1, t))


def projete(p, a, d):
    t = ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / (d[0] ** 2 + d[1] ** 2)
    return add(a, mul(d, t))


def angle(v):
    """Direction d'un vecteur de la planche en degrés, sens trigonométrique (l'axe y du dessin est vers le bas)."""
    return math.degrees(math.atan2(-v[1], v[0]))


# ============================================================ dessin en millimètres (fond et correction)
def n(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def ligne(a, b, cls="m"):
    return f'<line class="{cls}" x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}"/>'


def poly(pts, cls="m", ferme=False):
    tag = "polygon" if ferme else "polyline"
    return f'<{tag} class="{cls}" points="{" ".join(n(x) + "," + n(y) for x, y in pts)}"/>'


def cercle(c, r, cls="m"):
    return f'<circle class="{cls}" cx="{n(c[0])}" cy="{n(c[1])}" r="{n(r)}"/>'


def texte(p, s, cls="t", ancre="middle", taille=None):
    st = f' style="font-size:{n(taille)}px"' if taille else ""
    return f'<text class="{cls}" x="{n(p[0])}" y="{n(p[1])}" text-anchor="{ancre}"{st}>{s}</text>'


def nom_svg(s):
    """Nom d'un point ou d'un vecteur : lettre(s) puis indice (« I1 » → I₁ ; « VD » → V⃗ indice D)."""
    base, ind = s, ""
    while base and base[-1].isdigit():
        base, ind = base[:-1], base[-1] + ind
    return html.escape(base) + (f'<tspan class="ind" dy="1.2">{ind}</tspan>' if ind else "")


def fleche(a, b, cls="v", h=2.6):
    """Vecteur de a vers b, pointe pleine de longueur h (mm)."""
    u = unit(sub(b, a))
    L = dist(a, b)
    h = min(h, L * 0.45)
    base = sub(b, mul(u, h))
    w = perp(u)
    p1, p2 = add(base, mul(w, h * 0.36)), sub(base, mul(w, h * 0.36))
    return (f'<g class="{cls}">{ligne(a, sub(b, mul(u, h * 0.7)), "vt")}'
            f'{poly([b, p1, p2], "vp", True)}</g>')


def nom_vecteur(p, lettre, indice="", cls="nv", ancre="middle"):
    """Libellé d'un vecteur : lettre surmontée d'une flèche, indice éventuel."""
    ind = f'<tspan class="ind" dy="1.2">{html.escape(indice)}</tspan>' if indice else ""
    w = 2.6 * len(lettre)
    x0 = p[0] - (w / 2 if ancre == "middle" else (w if ancre == "end" else 0))
    return (f'<g class="{cls}">{texte(p, html.escape(lettre) + ind, "tv", ancre)}'
            f'<path class="fv" d="M{n(x0)} {n(p[1] - 4.1)}h{n(w)}m-1 -0.8l1 0.8l-1 0.8"/></g>')


def point(p, nom="", pos=(2, -2), cls="pt"):
    """Point repéré : croix et nom décalé de pos (mm)."""
    x, y = p
    c = (f'<g class="{cls}"><path d="M{n(x - 1.4)} {n(y - 1.4)}L{n(x + 1.4)} {n(y + 1.4)}M{n(x - 1.4)} {n(y + 1.4)}'
         f'L{n(x + 1.4)} {n(y - 1.4)}"/>')
    if nom:
        ancre = "start" if pos[0] > 0.5 else ("end" if pos[0] < -0.5 else "middle")
        c += texte((x + pos[0], y + pos[1]), nom_svg(nom), "tn", ancre)
    return c + "</g>"


def articulation(p, r=1.6, cls="art"):
    return cercle(p, r, cls)


def sol(a, b, cote=1, cls="sol"):
    """Bâti : trait épais et hachures (cote = 1 : hachures sous le trait)."""
    d = unit(sub(b, a))
    nrm = mul(perp(d), -cote)
    L = dist(a, b)
    hs = "".join(ligne(add(a, mul(d, s)), add(add(a, mul(d, s - 2.2)), mul(nrm, -2.6)), "h")
                 for s in [i * 3 + 2.2 for i in range(int((L - 2.2) // 3) + 1)])
    return f'<g class="{cls}">{ligne(a, b, "m")}{hs}</g>'


def pivot_fixe(p, cls="pf"):
    """Liaison pivot avec le bâti : cercle et petit triangle hachuré."""
    x, y = p
    tri = poly([(x, y), (x - 3.2, y + 5), (x + 3.2, y + 5)], "m", True)
    return f'<g class="{cls}">{tri}{sol((x - 4.6, y + 5), (x + 4.6, y + 5))}{cercle(p, 1.8, "art")}</g>'


def cote(a, b, s, decal=6, cls="cote"):
    """Cote entre a et b, ligne de cote décalée de decal (mm) vers la gauche du sens a → b."""
    d = unit(sub(b, a))
    w = mul(perp(d), -decal)
    a2, b2 = add(a, w), add(b, w)
    mid = mul(add(a2, b2), 0.5)
    ang = math.degrees(math.atan2(d[1], d[0]))
    if ang > 90 or ang < -90:
        ang += 180
    off = mul(unit(w), 2.2)
    t = add(mid, off)
    return (f'<g class="{cls}">{ligne(a, add(a2, mul(unit(w), 1.2)), "cl")}{ligne(b, add(b2, mul(unit(w), 1.2)), "cl")}'
            f'{fleche(mid, a2, "cf", 1.8)}{fleche(mid, b2, "cf", 1.8)}'
            f'<text class="tc" x="{n(t[0])}" y="{n(t[1])}" text-anchor="middle" dominant-baseline="middle" '
            f'transform="rotate({n(ang)} {n(t[0])} {n(t[1])})">{s}</text></g>')


def arc_angle(c, r, a1, a2, s="", cls="ang"):
    """Arc d'angle de centre c, de a1 à a2 (degrés, sens trigonométrique), libellé s."""
    p1 = (c[0] + r * math.cos(math.radians(a1)), c[1] - r * math.sin(math.radians(a1)))
    p2 = (c[0] + r * math.cos(math.radians(a2)), c[1] - r * math.sin(math.radians(a2)))
    grand = 1 if (a2 - a1) % 360 > 180 else 0
    m = math.radians((a1 + a2) / 2)
    t = (c[0] + (r + 3.2) * math.cos(m), c[1] - (r + 3.2) * math.sin(m) + 1.3)
    return (f'<g class="{cls}"><path d="M{n(p1[0])} {n(p1[1])}A{n(r)} {n(r)} 0 {grand} 0 {n(p2[0])} {n(p2[1])}"/>'
            + (texte(t, s, "ta") if s else "") + "</g>")


# ============================================================ planche
def planche(ident, w, h, fond, *, points=None, lignes=(), vecteurs=(), cercles=(), echelles=None, attendus=(),
            corr="", aria="", legende="", vech="V", libre=False, consigne=""):
    """Description d'une planche. Les éléments donnés (points nommés, lignes, vecteurs, cercles) sont dessinés dans
    le fond et repris dans la configuration pour l'aimantation et le choix d'une ligne de référence.
      echelles : {"L": (k, unité, déc.), "V": (k, unité, déc.)…} : 1 mm de la planche représente k unités
      attendus : relevés notés, dans l'ordre des cases de la question
        {"type": "vnorme", "en": "D"}           norme du dernier vecteur tracé depuis le point D (échelle vech)
        {"type": "vangle", "en": "D", "ref": a} direction de ce vecteur, en degrés, ramenée vers a
        {"type": "point", "nom": "I1", "x":…, "y":…}  écart (mm) entre le point nommé I1 et sa position attendue
      vech : échelle des vecteurs tracés par l'élève (« V » : vitesses)."""
    return {"id": ident, "w": w, "h": h, "fond": fond, "corr": corr, "aria": aria, "legende": legende,
            "points": points or {}, "lignes": list(lignes), "vecteurs": list(vecteurs), "cercles": list(cercles),
            "echelles": {k: {"k": v[0], "u": v[1], "d": v[2]} for k, v in (echelles or {}).items()},
            "attendus": list(attendus), "vech": vech, "libre": libre, "consigne": consigne}


def texte_echelles(ech):
    noms = {"L": "longueurs", "V": "vitesses", "F": "efforts"}
    return " · ".join(f"{noms.get(k, k)} : 1 mm ↔ {fr(e['k'], e['d'])} {e['u']}" for k, e in ech.items())


OUTILS = [
    ("Tracer", [("point", "Point", "Placer un point (il s'aimante aux points et aux intersections)"),
                ("segment", "Segment", "Tracer un segment entre deux points"),
                ("droite", "Droite", "Tracer la droite qui passe par deux points"),
                ("vecteur", "Vecteur", "Tracer un vecteur : son origine, puis son extrémité"),
                ("cercle", "Compas", "Tracer un cercle : son centre, puis un point du cercle"),
                ("report", "Report", "Reporter une longueur au compas : ses deux extrémités, puis le centre du cercle")]),
    ("Construire", [("perpendiculaire", "Perpendiculaire", "Perpendiculaire à une ligne, passant par un point"),
                    ("parallele", "Parallèle", "Parallèle à une ligne, passant par un point"),
                    ("projete", "Projeté", "Projeté orthogonal d'un point sur une ligne")]),
    ("Lire", [("mesurer", "Mesurer", "Mesurer une longueur, convertie avec les échelles"),
              ("nommer", "Nommer", "Donner un nom à un point que tu as placé (I1, J…)")]),
]


def rendu(cfg, fids=(), titre=""):
    """HTML de la planche ; fids : identifiants des cases (masquées) que remplissent les relevés notés."""
    data = {k: cfg[k] for k in ("w", "h", "points", "lignes", "vecteurs", "cercles", "echelles", "vech", "libre")}
    data["attendus"] = [dict(a, fid=f) for a, f in zip(cfg["attendus"], fids)]
    outils = '<span class="sep"></span>'.join(
        f'<span class="tb-group"><span class="tb-lab">{g}</span>' + "".join(
            f'<button type="button" data-outil="{k}" aria-pressed="{"true" if k == "point" else "false"}" '
            f'title="{html.escape(t)}">{lab}</button>' for k, lab, t in btns) + "</span>"
        for g, btns in OUTILS)
    barre = (f'<div class="sk-toolbar cg-toolbar" role="toolbar" aria-label="Outils de construction {html.escape(titre)}">'
             f'{outils}<span class="sep"></span>'
             '<button type="button" data-outil="gomme" aria-pressed="false" title="Effacer un de tes tracés">Gomme</button>'
             '<button type="button" data-act="annuler" title="Annuler le dernier tracé (Ctrl+Z)">Annuler</button>'
             '<button type="button" data-act="retablir" title="Rétablir (Ctrl+Y)">Rétablir</button>'
             '<button type="button" data-act="effacer">Tout effacer</button><span class="sep"></span>'
             '<span class="tb-group"><span class="tb-lab">Vue</span>'
             '<button type="button" data-zoom="out" aria-label="Réduire le zoom">−</button><span class="zoom-val">100 %</span>'
             '<button type="button" data-zoom="in" aria-label="Agrandir le zoom">+</button>'
             '<button type="button" data-zoom="reset">Ajuster</button>'
             '<button type="button" data-outil="vue" aria-pressed="false" title="Faire glisser la planche agrandie">Déplacer</button></span>'
             '<button type="button" data-act="aimant" aria-pressed="true" title="Aimantation aux points, intersections et lignes">Aimantation</button>'
             '<span class="spacer"></span><button type="button" data-act="plein" aria-pressed="false">Plein écran</button></div>')
    corr_ui = ('<button type="button" class="btn ghost cg-voir" aria-pressed="false">Afficher la correction</button>'
               if cfg["libre"] else
               '<label class="cg-corr-toggle"><input type="checkbox"> Superposer la correction</label>')
    leg = f'<p class="cg-leg">{cfg["legende"]}</p>' if cfg["legende"] else ""
    ech = f'<p class="cg-ech"><b>Échelles</b> — {texte_echelles(cfg["echelles"])}</p>' if cfg["echelles"] else ""
    return (f'<div class="cg{" cg-libre" if cfg["libre"] else ""}" id="cg-{cfg["id"]}" data-cg="{cfg["id"]}" '
            f'data-cfg="{html.escape(json.dumps(data, ensure_ascii=False, separators=(",", ":")))}">{barre}'
            f'<div class="cg-stage"><svg class="cg-svg" viewBox="0 0 {n(cfg["w"])} {n(cfg["h"])}" role="img" '
            f'aria-label="{html.escape(cfg["aria"])}"><rect class="cg-papier" width="{n(cfg["w"])}" height="{n(cfg["h"])}"/>'
            f'<g class="cg-fond">{cfg["fond"]}</g><g class="cg-corr">{cfg["corr"]}</g><g class="cg-eleve"></g>'
            f'<g class="cg-aide"></g></svg></div>'
            f'<div class="cg-foot"><p class="cg-info" aria-live="polite">Outil Point : touche la planche pour placer '
            f'un point.</p>{corr_ui}</div>{ech}{leg}</div>')


# ============================================================ style
CG_CSS = """
/* ---------- atelier de construction graphique (planches à l'échelle) ---------- */
.cg{margin:10px 0 8px; max-width:1040px}
.cg-toolbar{position:sticky; top:0; z-index:4}
.cg-toolbar button[data-outil="gomme"][aria-pressed="true"]{background:var(--rouge); border-color:var(--rouge)}
.cg-toolbar button[data-act="aimant"][aria-pressed="true"]{background:var(--vert-pale); color:var(--vert); border-color:var(--vert)}
.cg-stage{position:relative; border:1px solid var(--trait); background:#fff; line-height:0; overflow:hidden}
.cg-stage.zoomed{overflow:auto; max-height:min(76vh,720px)}
.cg-svg{display:block; width:100%; height:auto; touch-action:none; cursor:crosshair; user-select:none; -webkit-user-select:none;
  font-family:var(--f-texte)}
.cg.outil-vue .cg-svg{cursor:grab} .cg.outil-gomme .cg-svg{cursor:cell}
.cg.locked .cg-svg{cursor:default}
.cg-papier{fill:#fff}
.cg-svg .m{fill:none; stroke:#1C2530; stroke-width:.55; stroke-linecap:round; stroke-linejoin:round}
.cg-svg .mf{fill:#E9ECE8; stroke:#1C2530; stroke-width:.45; stroke-linejoin:round}
.cg-svg .mb{fill:#D9DFE6; stroke:#1C2530; stroke-width:.45; stroke-linejoin:round}
.cg-svg .fin{fill:none; stroke:#5A6670; stroke-width:.3}
.cg-svg .axe{fill:none; stroke:#5A6670; stroke-width:.25; stroke-dasharray:6 1.2 1 1.2}
.cg-svg .h{stroke:#1C2530; stroke-width:.3}
.cg-svg .art{fill:#fff; stroke:#1C2530; stroke-width:.45}
.cg-svg .pt path{fill:none; stroke:#1C2530; stroke-width:.4}
.cg-svg .t,.cg-svg .tn,.cg-svg .tv,.cg-svg .tc,.cg-svg .ta{font-size:4.2px; fill:#1C2530; paint-order:stroke; stroke:#fff; stroke-width:.9px; stroke-linejoin:round}
.cg-svg .tn{font-weight:700; font-style:italic}
.cg-svg .tv{font-weight:700; font-style:italic}
.cg-svg .tc,.cg-svg .ta{font-size:3.4px; fill:#46525C}
.cg-svg .ind{font-size:.72em; font-style:normal}
.cg-svg .v .vt{stroke:#1C2530; stroke-width:.75; fill:none} .cg-svg .v .vp{fill:#1C2530; stroke:none}
.cg-svg .fv{fill:none; stroke:#1C2530; stroke-width:.3}
.cg-svg .cote .cl{stroke:#5A6670; stroke-width:.2} .cg-svg .cf .vt{stroke:#5A6670; stroke-width:.2} .cg-svg .cf .vp{fill:#5A6670}
.cg-svg .ang path{fill:none; stroke:#5A6670; stroke-width:.25}
.cg-svg .rail{fill:none; stroke:#1C2530; stroke-width:1.2}
/* correction : rouge, au-dessus du fond, sous le tracé de l'élève ; masquée tant qu'elle n'est pas dévoilée */
.cg-corr{display:none} .cg-corr.on{display:inline}
.cg-corr .m,.cg-corr .fin{stroke:#C62828} .cg-corr .axe{stroke:#C62828; stroke-width:.3}
.cg-corr .v .vt{stroke:#C62828; stroke-width:.8} .cg-corr .v .vp{fill:#C62828}
.cg-corr .pt path{stroke:#C62828} .cg-corr .t,.cg-corr .tn,.cg-corr .tv,.cg-corr .ta{fill:#C62828} .cg-corr .fv{stroke:#C62828}
.cg-corr .ang path{stroke:#C62828}
/* tracés de l'élève : épaisseurs indépendantes du zoom */
.cg-eleve *{vector-effect:non-scaling-stroke}
.cg-eleve .e-dr{stroke:#6B7A88; stroke-width:1.1; stroke-dasharray:7 4; fill:none}
.cg-eleve .e-seg{stroke:#2E3B47; stroke-width:1.4; fill:none}
.cg-eleve .e-seg.pointille{stroke:#6B7A88; stroke-dasharray:3 3}
.cg-eleve .e-cer{stroke:#6B7A88; stroke-width:1.1; stroke-dasharray:7 4; fill:none}
.cg-eleve .e-vec line{stroke:#1F5FA8; stroke-width:2.6} .cg-eleve .e-vec path{fill:#1F5FA8; stroke:none}
.cg-eleve .e-pt path{stroke:#1F5FA8; stroke-width:1.6; fill:none}
.cg-eleve text{font-size:4px; font-weight:700; font-style:italic; fill:#1F5FA8; paint-order:stroke; stroke:#fff; stroke-width:3px; stroke-linejoin:round; vector-effect:none}
.cg-eleve text.e-val{font-style:normal; font-weight:600; font-size:3.3px}
.cg-eleve .e-mes{stroke:#B26A00; stroke-width:1.4; stroke-dasharray:2 3; fill:none}
.cg-aide *{vector-effect:non-scaling-stroke; pointer-events:none}
.cg-aide .a-snap{fill:rgba(242,183,5,.35); stroke:#B26A00; stroke-width:1.5}
.cg-aide .a-prev{stroke:#B26A00; stroke-width:1.3; stroke-dasharray:5 4; fill:none}
.cg-aide .a-sel{stroke:#F2B705; stroke-width:6; stroke-opacity:.55; fill:none; stroke-linecap:round}
.cg-foot{display:flex; flex-wrap:wrap; gap:6px 14px; align-items:center; margin-top:6px}
.cg-info{flex:1 1 320px; margin:0; font-size:.88rem; color:var(--encre); background:var(--jaune-pale); border-left:4px solid var(--jaune); padding:4px 10px; min-height:1.9em}
.cg-corr-toggle{display:none; align-items:center; gap:6px; font-size:.92rem; cursor:pointer}
.cg.revealed .cg-corr-toggle{display:inline-flex}
.cg-ech,.cg-leg{margin:4px 0 0; font-size:.85rem; color:var(--encre-2)}
.cg.locked .cg-toolbar button:disabled{opacity:.4}
.cg-nom{position:absolute; z-index:3; width:5.5em; font:700 15px var(--f-texte); border:2px solid var(--bleu); padding:1px 4px; line-height:1.2}
.cg.is-full{position:fixed; inset:0; z-index:60; background:var(--beton); margin:0; padding:10px; max-width:none; overflow:auto; display:flex; flex-direction:column}
.cg.is-full .cg-stage{flex:1 1 auto; overflow:auto; max-height:none}
.cg.is-full .cg-svg{max-height:calc(100vh - 150px); width:auto; max-width:100%; margin:0 auto}
.cg.is-full .cg-stage.zoomed .cg-svg{max-height:none; max-width:none}
body.cg-full-open{overflow:hidden}
body.cg-full-open .banner,body.cg-full-open .rail{display:none}
/* relevé de la construction dans la question */
.cg-q .grp-fields{max-width:760px}
.cg-val{font:600 .92rem var(--f-titre); color:var(--bleu)}
.cg-q .sol{min-height:1.9em}
@media print{
  .cg-toolbar,.cg-foot,.cg-voir{display:none!important}
  .cg-stage{overflow:visible!important; max-height:none!important; border:1px solid #999}
  .cg-svg{width:100%!important; max-height:150mm}
  .cg{break-inside:avoid}
  body:not(.corrections-open) .cg-corr{display:none!important}
}
"""


# ============================================================ moteur
CG_JS = r"""<script>/* Atelier de construction graphique : outils de géométrie sur des planches à l'échelle.
   Chaque planche relève sur le tracé ce que notent ses cases (masquées) et les remplit ; le moteur du gabarit les
   corrige. Un champ verrouillé par le moteur verrouille la planche ; la correction affichée dévoile le tracé corrigé. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg", ZOOMS = [1, 1.5, 2, 3, 4];
  var registre = window.__CG__ = {};
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function mk(tag, at, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) if (at[k] !== null && at[k] !== undefined) e.setAttribute(k, at[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function fr(x, d) { return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/^-/, "−"); }
  function chiffres(x, nb) {
    if (!isFinite(x) || Math.abs(x) < 1e-12) return "0";
    var d = Math.max(0, nb - 1 - Math.floor(Math.log10(Math.abs(x))));
    return fr(x, Math.min(d, 6));
  }
  // ---------- géométrie plane (millimètres de la planche, axe y vers le bas) ----------
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
  function add(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function mul(a, k) { return [a[0] * k, a[1] * k]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1]; }
  function crs(a, b) { return a[0] * b[1] - a[1] * b[0]; }
  function len(a) { return Math.sqrt(a[0] * a[0] + a[1] * a[1]); }
  function dist(a, b) { return len(sub(a, b)); }
  function unit(a) { var l = len(a) || 1; return [a[0] / l, a[1] / l]; }
  function perp(a) { return [-a[1], a[0]]; }
  // ligne support : p + t·d, t entre t0 et t1 (droite : bornes infinies)
  function lin(o) {
    if (o.t === "dr") return { p: o.a, d: sub(o.b, o.a), t0: -Infinity, t1: Infinity };
    if (o.t === "seg" || o.t === "vec") return { p: o.a, d: sub(o.b, o.a), t0: 0, t1: 1 };
    return null;
  }
  function interLL(A, B) {
    var den = crs(A.d, B.d);
    if (Math.abs(den) < 1e-9 * len(A.d) * len(B.d)) return [];
    var w = sub(B.p, A.p), t = crs(w, B.d) / den, u = crs(w, A.d) / den, e = 1e-6;
    if (t < A.t0 - e || t > A.t1 + e || u < B.t0 - e || u > B.t1 + e) return [];
    return [add(A.p, mul(A.d, t))];
  }
  function interLC(A, c) {
    var d = A.d, f = sub(A.p, c.c), a = dot(d, d), b = 2 * dot(f, d), q = dot(f, f) - c.r * c.r, D = b * b - 4 * a * q, out = [];
    if (D < 0) return out;
    var s = Math.sqrt(D);
    [(-b - s) / (2 * a), (-b + s) / (2 * a)].forEach(function (t) { if (t >= A.t0 - 1e-6 && t <= A.t1 + 1e-6) out.push(add(A.p, mul(d, t))); });
    return out;
  }
  function interCC(a, b) {
    var d = dist(a.c, b.c);
    if (d < 1e-9 || d > a.r + b.r + 1e-9 || d < Math.abs(a.r - b.r) - 1e-9) return [];
    var x = (d * d + a.r * a.r - b.r * b.r) / (2 * d), h = Math.sqrt(Math.max(0, a.r * a.r - x * x));
    var u = unit(sub(b.c, a.c)), m = add(a.c, mul(u, x)), v = perp(u);
    return h < 1e-9 ? [m] : [add(m, mul(v, h)), sub(m, mul(v, h))];
  }
  function inter(o1, o2) {
    var l1 = lin(o1), l2 = lin(o2);
    if (l1 && l2) return interLL(l1, l2);
    if (l1 && o2.t === "cer") return interLC(l1, o2);
    if (l2 && o1.t === "cer") return interLC(l2, o1);
    if (o1.t === "cer" && o2.t === "cer") return interCC(o1, o2);
    return [];
  }
  function surObjet(o, p) {
    var l = lin(o);
    if (l) {
      var t = dot(sub(p, l.p), l.d) / dot(l.d, l.d);
      t = Math.max(l.t0, Math.min(l.t1, t));
      return add(l.p, mul(l.d, t));
    }
    if (o.t === "cer") { var v = sub(p, o.c); return len(v) < 1e-9 ? [o.c[0] + o.r, o.c[1]] : add(o.c, mul(unit(v), o.r)); }
    return null;
  }
  function projete(p, o) { var l = lin(o), t = dot(sub(p, l.p), l.d) / dot(l.d, l.d); return add(l.p, mul(l.d, t)); }
  // droite (ou demi-droite) coupée aux bords de la planche
  function clip(p, d, W, H) {
    var t0 = -Infinity, t1 = Infinity;
    [[d[0], p[0], 0, W], [d[1], p[1], 0, H]].forEach(function (c) {
      if (Math.abs(c[0]) < 1e-12) { if (c[1] < c[2] || c[1] > c[3]) { t0 = 1; t1 = 0; } return; }
      var a = (c[2] - c[1]) / c[0], b = (c[3] - c[1]) / c[0];
      t0 = Math.max(t0, Math.min(a, b)); t1 = Math.min(t1, Math.max(a, b));
    });
    return t0 > t1 ? null : [add(p, mul(d, t0)), add(p, mul(d, t1))];
  }
  // noms : « I₁ », « i1 », « I 1 » désignent le même point
  function nomNorm(s) {
    return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 0x2080); })
      .replace(/[^A-Za-z0-9']/g, "").toUpperCase();
  }
  function ecrireNom(t, nom) {  // lettres, puis chiffres en indice
    var m = /^(.*?)(\d*)$/.exec(nom);
    t.textContent = m[1];
    if (m[2]) { var s = mk("tspan", { dy: "1.1", "font-size": "0.72em", "font-style": "normal" }, t); s.textContent = m[2]; }
  }

  function Planche(root) {
    var self = this, c;
    this.root = root; this.id = root.getAttribute("data-cg");
    this.cfg = c = JSON.parse(root.getAttribute("data-cfg"));
    this.svg = $("svg.cg-svg", root); this.stage = $(".cg-stage", root);
    this.gE = $(".cg-eleve", root); this.gA = $(".cg-aide", root); this.gC = $(".cg-corr", root);
    this.info = $(".cg-info", root);
    this.objs = []; this.hist = []; this.futur = [];
    this.outil = "point"; this.pend = null; this.zoom = 1; this.aimant = true; this.locked = false;
    this.mesure = null; this.survol = null; this.inters = [];
    this.donnes = [];
    Object.keys(c.points).forEach(function (k) { self.donnes.push({ t: "pt", p: c.points[k], nom: k, donne: true }); });
    c.lignes.forEach(function (l) { self.donnes.push({ t: l.inf ? "dr" : "seg", a: l.a, b: l.b, nom: l.nom, donne: true }); });
    c.vecteurs.forEach(function (v) { self.donnes.push({ t: "vec", a: v.a, b: v.b, nom: v.nom, donne: true }); });
    c.cercles.forEach(function (k) { self.donnes.push({ t: "cer", c: k.c, r: k.r, donne: true }); });
    this.q = root.closest(".fast-q");

    $$("[data-outil]", root).forEach(function (b) { b.addEventListener("click", function () { self.choisir(b.getAttribute("data-outil")); }); });
    $$("[data-zoom]", root).forEach(function (b) { b.addEventListener("click", function () { self.setZoom(b.getAttribute("data-zoom")); }); });
    $("[data-act=annuler]", root).addEventListener("click", function () { self.annuler(); });
    $("[data-act=retablir]", root).addEventListener("click", function () { self.retablir(); });
    var eff = $("[data-act=effacer]", root), effT;
    eff.addEventListener("click", function () {
      if (self.locked) return;
      if (eff.dataset.armed) { clearTimeout(effT); delete eff.dataset.armed; eff.textContent = "Tout effacer"; self.memo(); self.objs = []; self.mesure = null; self.change(); return; }
      eff.dataset.armed = "1"; eff.textContent = "Confirmer l'effacement";
      effT = setTimeout(function () { delete eff.dataset.armed; eff.textContent = "Tout effacer"; }, 3000);
    });
    var aim = $("[data-act=aimant]", root);
    aim.addEventListener("click", function () { self.aimant = !self.aimant; aim.setAttribute("aria-pressed", self.aimant ? "true" : "false"); });
    $("[data-act=plein]", root).addEventListener("click", function () { self.plein(); });
    var tg = $(".cg-corr-toggle input", root);
    if (tg) tg.addEventListener("change", function () { self.gC.classList.toggle("on", tg.checked); });
    var voir = $(".cg-voir", root);
    if (voir) voir.addEventListener("click", function () {
      var on = voir.getAttribute("aria-pressed") !== "true";
      voir.setAttribute("aria-pressed", on ? "true" : "false"); voir.textContent = on ? "Masquer la correction" : "Afficher la correction";
      self.gC.classList.toggle("on", on);
    });

    var sv = this.svg, down = null;
    sv.addEventListener("pointerdown", function (e) {
      if (e.button > 0) return;
      down = { x: e.clientX, y: e.clientY, sl: self.stage.scrollLeft, st: self.stage.scrollTop, id: e.pointerId, touch: e.pointerType !== "mouse" };
      if (self.outil === "vue") { sv.setPointerCapture(e.pointerId); e.preventDefault(); }
    });
    sv.addEventListener("pointermove", function (e) {
      if (down && self.outil === "vue") {
        self.stage.scrollLeft = down.sl - (e.clientX - down.x); self.stage.scrollTop = down.st - (e.clientY - down.y); return;
      }
      if (self.locked) return;
      self.survol = self.capter(e, e.pointerType !== "mouse");
      self.aide();
    });
    sv.addEventListener("pointerleave", function () { self.survol = null; self.aide(); });
    sv.addEventListener("pointerup", function (e) {
      var d = down; down = null;
      if (!d || self.outil === "vue" || self.locked) return;
      if (Math.hypot(e.clientX - d.x, e.clientY - d.y) > (d.touch ? 14 : 7)) return;
      var s = self.capter(e, d.touch);
      self.survol = s;
      self.clic(s);
    });
    root.addEventListener("keydown", function (e) {
      if (e.target.tagName === "INPUT") return;
      if (e.key === "Escape" && self.pend) { self.pend = null; self.aide(); self.consigne(); }
      else if ((e.ctrlKey || e.metaKey) && (e.key === "z" || e.key === "Z")) { e.preventDefault(); self.annuler(); }
      else if ((e.ctrlKey || e.metaKey) && (e.key === "y" || e.key === "Y")) { e.preventDefault(); self.retablir(); }
    });
    // la question corrigée par le moteur (case verrouillée, correction affichée) verrouille la planche
    if (this.q) {
      new MutationObserver(function () {
        var inp = $(".sol input", self.q);
        if (inp && inp.disabled && !self.locked) self.verrouiller();
        var ex = $(".q-expl", self.q);
        if (ex && !ex.hidden && !self.revealed) self.reveler();
      }).observe(this.q, { subtree: true, attributes: true, attributeFilter: ["disabled", "hidden"] });
    }
    this.change(true);
    this.consigne();
    registre[this.id] = this;
  }
  var P = Planche.prototype;

  P.tous = function () { return this.donnes.concat(this.objs); };
  P.pxmm = function () { var m = this.svg.getScreenCTM(); return m ? m.a : 3; };
  P.pos = function (e) {
    var m = this.svg.getScreenCTM(), pt = this.svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    var q = pt.matrixTransform(m.inverse());
    return [q.x, q.y];
  };
  // ---------- aimantation : points (et extrémités), intersections, puis lignes ----------
  P.cibles = function () {
    var out = [];
    this.tous().forEach(function (o) {
      if (o.t === "pt") out.push({ p: o.p, k: "point", nom: o.nom });
      else if (o.t === "seg" || o.t === "vec") { out.push({ p: o.a, k: "point" }); out.push({ p: o.b, k: "point" }); }
      else if (o.t === "cer") out.push({ p: o.c, k: "point" });
    });
    return out;
  };
  P.majInters = function () {
    var L = this.tous().filter(function (o) { return o.t !== "pt"; }), out = [];
    for (var i = 0; i < L.length; i++)
      for (var j = i + 1; j < L.length; j++)
        inter(L[i], L[j]).forEach(function (p) { out.push({ p: p, k: "inter" }); });
    this.inters = out;
  };
  P.capter = function (e, touch) {
    var raw = this.pos(e), R = (touch ? 22 : 12) / this.pxmm();
    var res = { p: raw, raw: raw, k: "libre" };
    if (!this.aimant) return res;
    var best = null, bd = R;
    this.cibles().concat(this.inters).forEach(function (c) {
      var d = dist(c.p, raw) - (c.k === "point" ? 0.15 * R : 0);  // un point existant l'emporte sur une intersection voisine
      if (d < bd) { bd = d; best = c; }
    });
    if (best) return { p: best.p.slice(), raw: raw, k: best.k, nom: best.nom };
    var sur = null, sd = R * 0.7;
    this.tous().forEach(function (o) {
      if (o.t === "pt") return;
      var q = surObjet(o, raw);
      if (q && dist(q, raw) < sd) { sd = dist(q, raw); sur = q; }
    });
    return sur ? { p: sur, raw: raw, k: "sur" } : res;
  };
  P.linProche = function (raw) {
    var R = 12 / this.pxmm(), best = null, bd = R;
    this.tous().forEach(function (o) {
      if (!lin(o)) return;
      var d = dist(surObjet(o, raw), raw);
      if (d < bd) { bd = d; best = o; }
    });
    return best;
  };
  P.objProche = function (raw) {  // seuls les tracés de l'élève s'effacent ; les points d'abord
    var R = 12 / this.pxmm(), best = null, bd = R;
    this.objs.forEach(function (o) {
      var d = o.t === "pt" ? dist(o.p, raw) - 0.3 * R : dist(surObjet(o, raw), raw);
      if (d < bd) { bd = d; best = o; }
    });
    return best;
  };
  P.ptNomme = function (nom) {
    var k = nomNorm(nom), r = null;
    this.tous().forEach(function (o) { if (o.t === "pt" && o.nom && nomNorm(o.nom) === k) r = o; });
    return r;
  };
  P.nomEn = function (p) {
    var r = "";
    this.tous().forEach(function (o) { if (o.t === "pt" && o.nom && dist(o.p, p) < 0.3) r = o.nom; });
    return r;
  };
  P.vecteurEn = function (nom) {
    var pt = this.ptNomme(nom), r = null;
    if (!pt) return null;
    this.objs.forEach(function (o) { if (o.t === "vec" && dist(o.a, pt.p) < 0.5) r = o; });
    return r;
  };
  // ---------- outils ----------
  var CONSIGNES = {
    point: "Outil Point : touche la planche pour placer un point (il s'aimante aux points et aux intersections).",
    segment: "Outil Segment : touche le premier point, puis le second.",
    droite: "Outil Droite : touche deux points de la droite.",
    vecteur: "Outil Vecteur : touche l'origine (le point où s'applique le vecteur), puis l'extrémité.",
    cercle: "Outil Compas : touche le centre, puis un point du cercle.",
    report: "Outil Report : touche les deux extrémités de la longueur à reporter, puis le centre du cercle de ce rayon.",
    perpendiculaire: "Outil Perpendiculaire : touche la ligne de référence (droite, segment ou vecteur), puis le point de passage.",
    parallele: "Outil Parallèle : touche la ligne de référence (droite, segment ou vecteur), puis le point de passage.",
    projete: "Outil Projeté : touche le point à projeter, puis la ligne sur laquelle le projeter.",
    mesurer: "Outil Mesurer : touche les deux extrémités de la longueur à mesurer.",
    nommer: "Outil Nommer : touche un point que tu as placé, puis écris son nom (par exemple I1).",
    gomme: "Gomme : touche un de tes tracés pour l'effacer (le dessin donné ne s'efface pas).",
    vue: "Déplacer : fais glisser la planche agrandie."
  };
  P.consigne = function () { this.dire(CONSIGNES[this.outil]); };
  P.dire = function (s) { this.info.textContent = s; };
  P.choisir = function (o) {
    if (this.locked && o !== "vue") return;
    this.outil = o; this.pend = null;
    var r = this.root;
    $$("[data-outil]", r).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-outil") === o ? "true" : "false"); });
    r.classList.toggle("outil-vue", o === "vue"); r.classList.toggle("outil-gomme", o === "gomme");
    this.consigne(); this.aide();
  };
  P.ech = function (k) { return this.cfg.echelles[k]; };
  P.texteLongueur = function (L) {
    var self = this, parts = [fr(L, 1) + " mm sur la planche"];
    Object.keys(this.cfg.echelles).forEach(function (k) {
      var e = self.ech(k), nm = { L: "longueurs", V: "vitesses", F: "efforts" }[k] || k;
      parts.push(chiffres(L * e.k, 3) + " " + e.u + " (" + nm + ")");
    });
    return parts.join(" · ");
  };
  P.clic = function (s) {
    var o = this.outil, p = s.p, self = this;
    if (o === "point") {
      if (s.k === "point") { this.dire("Il y a déjà un point ici" + (s.nom ? " : " + s.nom : "") + "."); return; }
      this.ajouter([{ t: "pt", p: p }]); this.dire("Point placé" + (s.k === "inter" ? " à l'intersection." : ".") + " Outil Nommer pour lui donner un nom."); return;
    }
    if (o === "nommer") {
      var R = 12 / this.pxmm(), cand = null, bd = R;
      this.objs.forEach(function (x) { if (x.t === "pt" && dist(x.p, s.raw) < bd) { bd = dist(x.p, s.raw); cand = x; } });
      if (!cand) { this.dire("Touche un point que tu as placé (outil Point) pour le nommer."); return; }
      this.saisirNom(cand); return;
    }
    if (o === "gomme") {
      var x = this.objProche(s.raw);
      if (!x) { this.dire("Rien à effacer ici : seuls tes tracés s'effacent."); return; }
      this.memo(); this.objs.splice(this.objs.indexOf(x), 1); this.change(); this.dire("Tracé effacé (Annuler pour le rétablir)."); return;
    }
    if (o === "report") {
      if (!this.pend) { this.pend = { p: p }; this.aide(); this.dire("Touche maintenant l'autre extrémité de la longueur à reporter."); return; }
      if (!this.pend.q) {
        if (dist(this.pend.p, p) < 0.2) { this.dire("Les deux points sont confondus : touche l'autre extrémité."); return; }
        this.pend.q = p; this.aide(); this.dire("Longueur prise (" + this.texteLongueur(dist(this.pend.p, p)) + "). Touche le centre du cercle."); return;
      }
      var rr = dist(this.pend.p, this.pend.q); this.pend = null;
      this.ajouter([{ t: "cer", c: p, r: rr }]); this.consigne(); return;
    }
    if (["segment", "droite", "vecteur", "cercle", "mesurer"].indexOf(o) >= 0) {
      if (!this.pend) {
        this.pend = { p: p };
        this.dire({ segment: "Touche maintenant l'autre extrémité du segment.", droite: "Touche un second point de la droite.",
          vecteur: "Touche maintenant l'extrémité du vecteur : sa longueur, lue à l'échelle, s'affiche en direct.",
          cercle: "Touche maintenant un point du cercle : le rayon est la distance au centre.",
          mesurer: "Touche maintenant l'autre extrémité." }[o]);
        this.aide(); return;
      }
      var a = this.pend.p; this.pend = null;
      if (dist(a, p) < 0.2) { this.dire("Les deux points sont confondus : recommence."); this.aide(); return; }
      if (o === "segment") this.ajouter([{ t: "seg", a: a, b: p }]);
      else if (o === "droite") this.ajouter([{ t: "dr", a: a, b: p }]);
      else if (o === "vecteur") { this.ajouter([{ t: "vec", a: a, b: p }]); this.dire("Vecteur tracé : " + this.texteVecteur({ a: a, b: p }) + "."); return; }
      else if (o === "cercle") this.ajouter([{ t: "cer", c: a, r: dist(a, p) }]);
      else { this.mesure = [a, p]; this.dessiner(); this.dire("Longueur : " + this.texteLongueur(dist(a, p)) + "."); return; }
      this.consigne(); return;
    }
    if (o === "perpendiculaire" || o === "parallele") {
      if (!this.pend) {
        var l = this.linProche(s.raw);
        if (!l) { this.dire("Touche d'abord une ligne de référence : une droite, un segment ou un vecteur."); return; }
        this.pend = { obj: l }; this.aide();
        this.dire("Touche maintenant le point par lequel passe la " + (o === "parallele" ? "parallèle." : "perpendiculaire.")); return;
      }
      var L = lin(this.pend.obj), d = unit(o === "parallele" ? L.d : perp(L.d)); this.pend = null;
      this.ajouter([{ t: "dr", a: p, b: add(p, mul(d, 10)) }]); this.consigne(); return;
    }
    if (o === "projete") {
      if (!this.pend) { this.pend = { p: p }; this.aide(); this.dire("Touche maintenant la ligne sur laquelle projeter ce point."); return; }
      var l2 = this.linProche(s.raw);
      if (!l2) { this.dire("Touche une droite, un segment ou un vecteur."); return; }
      var a2 = this.pend.p, q = projete(a2, l2); this.pend = null;
      var add2 = [{ t: "pt", p: q }];
      if (dist(a2, q) > 0.2) add2.unshift({ t: "seg", a: a2, b: q, pointille: true });
      this.ajouter(add2); this.dire("Projeté placé : il s'aimante comme tout point."); return;
    }
  };
  P.saisirNom = function (pt) {
    var self = this, r = this.stage.getBoundingClientRect(), m = this.svg.getScreenCTM();
    var inp = document.createElement("input");
    inp.className = "cg-nom"; inp.type = "text"; inp.maxLength = 6; inp.value = pt.nom || "";
    inp.setAttribute("aria-label", "Nom du point");
    inp.style.left = (pt.p[0] * m.a + m.e - r.left + this.stage.scrollLeft + 8) + "px";
    inp.style.top = (pt.p[1] * m.d + m.f - r.top + this.stage.scrollTop - 30) + "px";
    this.stage.appendChild(inp); setTimeout(function () { inp.focus(); inp.select(); }, 0);
    var fini = false;
    function valider(ok) {
      if (fini) return; fini = true;
      var v = inp.value.trim().replace(/\s+/g, "");
      inp.remove();
      if (!ok) return;
      if (v && self.tous().some(function (o) { return o !== pt && o.t === "pt" && o.nom && nomNorm(o.nom) === nomNorm(v); })) {
        self.dire("Le nom " + v + " est déjà pris."); return;
      }
      self.memo(); pt.nom = v || undefined; self.change(); self.dire(v ? "Point nommé " + v + "." : "Nom retiré.");
    }
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); valider(true); } if (e.key === "Escape") valider(false); });
    inp.addEventListener("blur", function () { valider(true); });
  };
  // ---------- historique ----------
  P.memo = function () { this.hist.push(JSON.stringify(this.objs)); this.futur = []; if (this.hist.length > 200) this.hist.shift(); };
  P.ajouter = function (list) { this.memo(); this.objs = this.objs.concat(list); this.change(); };
  P.annuler = function () {
    if (this.locked || !this.hist.length) return;
    this.futur.push(JSON.stringify(this.objs)); this.objs = JSON.parse(this.hist.pop()); this.pend = null; this.change(); this.dire("Dernière action annulée.");
  };
  P.retablir = function () {
    if (this.locked || !this.futur.length) return;
    this.hist.push(JSON.stringify(this.objs)); this.objs = JSON.parse(this.futur.pop()); this.change(); this.dire("Action rétablie.");
  };
  P.change = function (init) { this.majInters(); this.dessiner(); this.releve(init); };
  // ---------- dessin ----------
  P.texteVecteur = function (v) {
    var e = this.ech(this.cfg.vech), L = dist(v.a, v.b), nom = this.nomEn(v.a);
    var t = (nom ? "V" + nom + " : " : "") + fr(L, 1) + " mm";
    return e ? t + " soit " + chiffres(L * e.k, 3) + " " + e.u : t;
  };
  P.trace = function (o, g) {
    var W = this.cfg.w, H = this.cfg.h;
    if (o.t === "pt") {
      var x = o.p[0], y = o.p[1], k = 1.3;
      var gp = mk("g", { "class": "e-pt" }, g);
      mk("path", { d: "M" + (x - k) + " " + (y - k) + "L" + (x + k) + " " + (y + k) + "M" + (x - k) + " " + (y + k) + "L" + (x + k) + " " + (y - k) }, gp);
      if (o.nom) ecrireNom(mk("text", { x: x + 1.8, y: y - 1.8 }, gp), o.nom);
    } else if (o.t === "seg") mk("line", { "class": "e-seg" + (o.pointille ? " pointille" : ""), x1: o.a[0], y1: o.a[1], x2: o.b[0], y2: o.b[1] }, g);
    else if (o.t === "dr") {
      var c = clip(o.a, sub(o.b, o.a), W, H);
      if (c) mk("line", { "class": "e-dr", x1: c[0][0], y1: c[0][1], x2: c[1][0], y2: c[1][1] }, g);
    } else if (o.t === "cer") mk("circle", { "class": "e-cer", cx: o.c[0], cy: o.c[1], r: o.r }, g);
    else if (o.t === "vec") {
      var u = unit(sub(o.b, o.a)), L = dist(o.a, o.b), h = Math.min(2.8, L * 0.45), w = perp(u);
      var base = sub(o.b, mul(u, h)), gv = mk("g", { "class": "e-vec" }, g);
      var e2 = sub(o.b, mul(u, h * 0.7));
      mk("line", { x1: o.a[0], y1: o.a[1], x2: e2[0], y2: e2[1] }, gv);
      var p1 = add(base, mul(w, h * 0.36)), p2 = sub(base, mul(w, h * 0.36));
      mk("path", { d: "M" + o.b[0] + " " + o.b[1] + "L" + p1[0] + " " + p1[1] + "L" + p2[0] + " " + p2[1] + "Z" }, gv);
      var nom = this.nomEn(o.a), e = this.ech(this.cfg.vech), side = w[1] > 0 ? mul(w, -1) : w;  // libellé du côté haut
      var m = add(mul(add(o.a, o.b), 0.5), mul(side, 3.2));
      if (nom) {
        var t = mk("text", { x: m[0], y: m[1], "text-anchor": "middle" }, gv);
        t.textContent = "V"; var s = mk("tspan", { dy: "1.1", "font-size": "0.72em", "font-style": "normal" }, t); s.textContent = nom;
      }
      if (e) {
        var t2 = mk("text", { "class": "e-val", x: m[0], y: m[1] + (nom ? 4.2 : 0), "text-anchor": "middle" }, gv);
        t2.textContent = chiffres(L * e.k, 3) + " " + e.u;
      }
    }
  };
  P.dessiner = function () {
    var g = this.gE, self = this;
    while (g.firstChild) g.removeChild(g.firstChild);
    // constructions d'abord, puis segments, vecteurs et points par-dessus
    var ordre = { dr: 0, cer: 0, seg: 1, vec: 2, pt: 3 };
    this.objs.slice().sort(function (a, b) { return ordre[a.t] - ordre[b.t]; }).forEach(function (o) { self.trace(o, g); });
    if (this.mesure) mk("line", { "class": "e-mes", x1: this.mesure[0][0], y1: this.mesure[0][1], x2: this.mesure[1][0], y2: this.mesure[1][1] }, g);
    this.aide();
  };
  P.aide = function () {
    var g = this.gA, s = this.survol, o = this.outil, k = 1 / this.pxmm();
    while (g.firstChild) g.removeChild(g.firstChild);
    if (this.locked) return;
    if (this.pend && this.pend.obj) {
      var l = this.pend.obj, L = lin(l), c = l.t === "dr" ? clip(L.p, L.d, this.cfg.w, this.cfg.h) : [l.a, l.b];
      if (c) mk("line", { "class": "a-sel", x1: c[0][0], y1: c[0][1], x2: c[1][0], y2: c[1][1] }, g);
    }
    if (!s) return;
    var p = s.p;
    if (o === "report" && this.pend && this.pend.q) {
      mk("line", { "class": "a-sel", x1: this.pend.p[0], y1: this.pend.p[1], x2: this.pend.q[0], y2: this.pend.q[1] }, g);
      mk("circle", { "class": "a-prev", cx: p[0], cy: p[1], r: dist(this.pend.p, this.pend.q) }, g);
    } else if (this.pend && this.pend.p) {
      var a = this.pend.p;
      if (o === "cercle") mk("circle", { "class": "a-prev", cx: a[0], cy: a[1], r: dist(a, p) }, g);
      else if (o === "droite") { var c2 = clip(a, sub(p, a), this.cfg.w, this.cfg.h); if (c2 && dist(a, p) > 0.1) mk("line", { "class": "a-prev", x1: c2[0][0], y1: c2[0][1], x2: c2[1][0], y2: c2[1][1] }, g); }
      else if (o === "projete") { var l3 = this.linProche(s.raw); if (l3) { var q = projete(a, l3); mk("line", { "class": "a-prev", x1: a[0], y1: a[1], x2: q[0], y2: q[1] }, g); } }
      else mk("line", { "class": "a-prev", x1: a[0], y1: a[1], x2: p[0], y2: p[1] }, g);
      if (o === "vecteur" && dist(a, p) > 0.2) this.dire("Vecteur en cours : " + this.texteVecteur({ a: a, b: p }) + ".");
      if ((o === "mesurer" || o === "segment") && dist(a, p) > 0.2) this.dire("Longueur : " + this.texteLongueur(dist(a, p)) + ".");
      if (o === "cercle" && dist(a, p) > 0.2) this.dire("Rayon : " + this.texteLongueur(dist(a, p)) + ".");
    }
    if (o === "perpendiculaire" || o === "parallele") {
      if (!this.pend) { var l4 = this.linProche(s.raw); if (l4) { var c4 = l4.t === "dr" ? clip(lin(l4).p, lin(l4).d, this.cfg.w, this.cfg.h) : [l4.a, l4.b]; if (c4) mk("line", { "class": "a-sel", x1: c4[0][0], y1: c4[0][1], x2: c4[1][0], y2: c4[1][1] }, g); } return; }
      var L2 = lin(this.pend.obj), d = unit(o === "parallele" ? L2.d : perp(L2.d)), c5 = clip(p, d, this.cfg.w, this.cfg.h);
      if (c5) mk("line", { "class": "a-prev", x1: c5[0][0], y1: c5[0][1], x2: c5[1][0], y2: c5[1][1] }, g);
    }
    if (o === "projete" && this.pend) return;
    if (o === "gomme" || o === "nommer" || o === "vue") return;
    if (s.k === "point") mk("circle", { "class": "a-snap", cx: p[0], cy: p[1], r: 7 * k }, g);
    else if (s.k === "inter") mk("rect", { "class": "a-snap", x: p[0] - 6 * k, y: p[1] - 6 * k, width: 12 * k, height: 12 * k, transform: "rotate(45 " + p[0] + " " + p[1] + ")" }, g);
    else if (s.k === "sur") mk("circle", { "class": "a-snap", cx: p[0], cy: p[1], r: 4 * k }, g);
  };
  // ---------- relevé : ce que notent les cases de la question ----------
  P.releve = function () {
    var self = this;
    (this.cfg.attendus || []).forEach(function (a) {
      var v = "", txt = "";
      if (a.type === "vnorme" || a.type === "vangle") {
        var V = self.vecteurEn(a.en);
        if (V) {
          var d = sub(V.b, V.a);
          if (a.type === "vnorme") {
            var e = self.ech(a.ech || self.cfg.vech), val = len(d) * e.k;
            v = String(+val.toPrecision(5)); txt = chiffres(val, 3) + " " + e.u;
          } else {
            var ang = Math.atan2(-d[1], d[0]) * 180 / Math.PI, ref = a.ref || 0;
            while (ang > ref + 180) ang -= 360;
            while (ang <= ref - 180) ang += 360;
            v = String(Math.round(ang * 10) / 10); txt = fr(ang, 0) + "° (sens trigonométrique, depuis l'horizontale vers la droite)";
          }
        } else txt = "vecteur à tracer depuis le point " + a.en;
      } else if (a.type === "point") {
        var pt = self.ptNomme(a.nom);
        if (pt && !pt.donne) { v = String(Math.round(dist(pt.p, [a.x, a.y]) * 100) / 100); txt = "point " + a.nom + " placé"; }
        else txt = "point à placer, puis à nommer " + a.nom;
      }
      var inp = document.getElementById("in-" + a.fid), sp = self.q && $('.cg-val[data-fid="' + a.fid + '"]', self.q);
      if (inp && inp.disabled) return;
      if (sp) sp.textContent = txt;
      if (inp && inp.value !== v) { inp.value = v; inp.dispatchEvent(new Event("input", { bubbles: true })); }
    });
  };
  P.verrouiller = function () {
    this.locked = true; this.pend = null; this.root.classList.add("locked");
    $$(".cg-toolbar button", this.root).forEach(function (b) {
      var keep = b.hasAttribute("data-zoom") || b.getAttribute("data-outil") === "vue" || b.getAttribute("data-act") === "plein";
      if (!keep) b.disabled = true;
    });
    this.aide();
    this.dire("Construction verrouillée : elle a été corrigée.");
  };
  P.reveler = function () {
    this.revealed = true; this.root.classList.add("revealed");
    var tg = $(".cg-corr-toggle input", this.root);
    if (tg) { tg.checked = true; this.gC.classList.add("on"); }
    this.dire("Correction superposée en rouge : compare-la à ta construction (la case à cocher la masque).");
  };
  // ---------- vue ----------
  P.setZoom = function (what) {
    var i = ZOOMS.indexOf(this.zoom), st = this.stage;
    if (i < 0) i = 0;
    if (what === "in") i = Math.min(ZOOMS.length - 1, i + 1); else if (what === "out") i = Math.max(0, i - 1); else i = 0;
    var cx = (st.scrollLeft + st.clientWidth / 2) / Math.max(1, st.scrollWidth), cy = (st.scrollTop + st.clientHeight / 2) / Math.max(1, st.scrollHeight);
    this.zoom = ZOOMS[i];
    st.classList.toggle("zoomed", this.zoom > 1);
    this.svg.style.width = this.zoom > 1 ? this.zoom * 100 + "%" : "";
    this.svg.style.maxWidth = this.zoom > 1 ? "none" : "";
    $(".zoom-val", this.root).textContent = Math.round(this.zoom * 100) + " %";
    $("[data-zoom=out]", this.root).disabled = this.zoom === ZOOMS[0];
    $("[data-zoom=in]", this.root).disabled = this.zoom === ZOOMS[ZOOMS.length - 1];
    requestAnimationFrame(function () { st.scrollLeft = cx * st.scrollWidth - st.clientWidth / 2; st.scrollTop = cy * st.scrollHeight - st.clientHeight / 2; });
    this.aide();
  };
  P.plein = function () {
    var on = !this.root.classList.contains("is-full"), b = $("[data-act=plein]", this.root);
    this.root.classList.toggle("is-full", on); document.body.classList.toggle("cg-full-open", on);
    b.textContent = on ? "Quitter le plein écran" : "Plein écran"; b.setAttribute("aria-pressed", on ? "true" : "false");
    if (!on) this.root.scrollIntoView({ block: "start" });
  };
  // ---------- outils de test ----------
  P.charger = function (list) { this.memo(); this.objs = JSON.parse(JSON.stringify(list)); this.change(); };
  P.etat = function () { return JSON.parse(JSON.stringify(this.objs)); };

  function init(scope) { $$(".cg[data-cg]", scope).forEach(function (r) { if (!registre[r.getAttribute("data-cg")]) new Planche(r); }); }
  init(document);
  window.__initCG__ = init;
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var f = $(".cg.is-full"); if (f && registre[f.getAttribute("data-cg")] && !registre[f.getAttribute("data-cg")].pend) registre[f.getAttribute("data-cg")].plein();
  });
})();
</script>"""
