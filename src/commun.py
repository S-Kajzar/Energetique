# -*- coding: utf-8 -*-
"""Outils partagés par le générateur, les cours et les activités : écriture des nombres et des calculs, correcteurs
numériques du moteur Grading (valeur, tolérance, unité et ses multiples), blocs de contenu des parties."""
import base64
import html
import math
import pathlib
import struct

IMAGES = pathlib.Path(__file__).resolve().parent / "images"
G = 9.81  # accélération de la pesanteur retenue dans tout le site (m/s²), comme dans le cours


# ============================================================ écriture
def esc(s):
    return html.escape(str(s), quote=True)


def fr(x, d=1):
    """Nombre à la française : espace fine insécable entre les milliers, virgule décimale."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def sig(x, n=3):
    """Nombre arrondi à n chiffres significatifs, écrit à la française (sans zéros inutiles après la virgule)."""
    if x == 0:
        return "0"
    d = max(0, n - 1 - int(math.floor(math.log10(abs(x)))))
    return fr(round(x, d), d)


def frac(a, b):
    return f'<span class="frac"><span>{a}</span><span>{b}</span></span>'


def eq(*lignes):
    """Lignes de calcul : une par paragraphe .eq (défilement horizontal si besoin)."""
    return "".join(f'<p class="eq">{l}</p>' for l in lignes)


def vec(lettre, indice=""):
    """Vecteur : lettre surmontée d'une flèche, indice éventuel."""
    sub = f"<sub>{indice}</sub>" if indice else ""
    return f'<span class="vec">{lettre}</span>{sub}'


def svg_uri(svg):
    """Dessin SVG autonome intégré en data URI (vignettes de l'accueil)."""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


def jpg(name):
    """Image JPEG de src/images intégrée en data URI ; dimensions lues dans le segment SOF."""
    data = (IMAGES / f"{name}.jpg").read_bytes()
    i = 2
    while i < len(data):
        marker, size = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return "data:image/jpeg;base64," + base64.b64encode(data).decode(), w, h
        i += 2 + size
    raise ValueError(f"{name}.jpg : dimensions introuvables")


def donnees(*items, titre="Données"):
    return (f'<div class="data"><p class="data-title">{titre}</p><ul>' +
            "".join(f"<li>{i}</li>" for i in items) + "</ul></div>")


# ============================================================ unités et correcteurs numériques
# Formes acceptées après normalisation par le moteur (normUnit) : minuscules, sans accents, séparateurs « . · * »
# remplacés par des espaces puis morceaux recollés (« N·m » → « nm », « m.s-1 » → « ms-1 »).
UNITES = {
    "J": ["j", "joule", "joules"],
    "kJ": ["kj", "kilojoule", "kilojoules"],
    "W": ["w", "watt", "watts"],
    "kW": ["kw", "kilowatt", "kilowatts"],
    "N": ["n", "newton", "newtons"],
    "kN": ["kn", "kilonewton", "kilonewtons"],
    "N·m": ["nm", "mn", "newtonmetre", "newtonmetres", "newtonsmetre", "newtonsmetres"],
    "m/s": ["m/s", "ms-1", "metre/s", "metres/s", "metre/seconde", "metres/seconde"],
    "mm/s": ["mm/s", "mms-1", "millimetre/s", "millimetres/s"],
    "rad/s": ["rad/s", "rads-1", "radian/s", "radians/s", "radian/seconde", "radians/seconde"],
    "tr/min": ["tr/min", "trmin-1", "tour/min", "tours/min", "tpm"],
    "kg·m²": ["kgm2", "m2kg"],
    "kg": ["kg", "kilogramme", "kilogrammes", "kilo", "kilos"],
    "m": ["m", "metre", "metres"],
    "mm": ["mm", "millimetre", "millimetres"],
    "mm²": ["mm2", "millimetrecarre", "millimetrescarres"],
    "N/m": ["n/m", "nm-1", "newton/m", "newtons/m"],
    "kN/m": ["kn/m", "knm-1", "kilonewton/m", "kilonewtons/m"],
    "bar": ["bar", "bars"],
    "MPa": ["mpa", "megapascal", "megapascals"],
    "Pa": ["pa", "pascal", "pascals"],
    "N/mm²": ["n/mm2", "nmm-2"],
    "s": ["s", "seconde", "secondes", "sec"],
    "rad": ["rad", "radian", "radians"],
    "tours": ["tours", "tour", "tr"],
    "°": ["°", "degre", "degres", "deg"],
}
# multiples acceptés en variante : la même grandeur écrite dans une autre unité (valeur convertie)
MULTIPLES = {
    "J": {"kJ": 1e-3}, "kJ": {"J": 1e3},
    "W": {"kW": 1e-3}, "kW": {"W": 1e3},
    "N": {"kN": 1e-3}, "kN": {"N": 1e3},
    "m": {"mm": 1e3}, "mm": {"m": 1e-3},
    "m/s": {"mm/s": 1e3}, "mm/s": {"m/s": 1e-3},
    "N/m": {"kN/m": 1e-3}, "kN/m": {"N/m": 1e3},
    "bar": {"MPa": 0.1, "N/mm²": 0.1, "Pa": 1e5},
    "MPa": {"bar": 10, "N/mm²": 1, "Pa": 1e6},
}


def unite(u):
    return {"label": u, "accept": UNITES[u]}


def num(v, u=None, rel=0.02, abs_=None, alt=()):
    """Correcteur numérique du moteur Grading : valeur v à rel près (2 % par défaut, pour g = 9,81 ou 10 et les
    arrondis intermédiaires), unité u et ses multiples. alt : autres valeurs justes (sans unité imposée)."""
    g = {"type": "num", "value": v}
    if abs_ is not None:
        g["absTol"] = abs_
    else:
        g["relTol"] = rel
    if u:
        g["unit"] = unite(u)
    variants = []
    for u2, k in (MULTIPLES.get(u, {}) if u else {}).items():
        variants.append({"value": v * k, "relTol": rel, "unit": unite(u2)} if abs_ is None else
                        {"value": v * k, "absTol": abs_ * k, "unit": unite(u2)})
    for a in alt:
        variants.append({"value": a, "relTol": rel} if abs_ is None else {"value": a, "absTol": abs_})
    if variants:
        g["variants"] = variants
    return g


# ============================================================ blocs de contenu d'une partie
def HTML(raw):
    return {"kind": "html", "html": raw}


def Q(stem, hint, grader, expected, why):
    """Question à une case (saisie libre) : un point, l'unité en vaut la moitié."""
    return {"kind": "q", "stem": stem, "hint": hint, "grader": grader, "expected": expected, "why": why}


def QCM(stem, opts, bonnes, why, img=""):
    """Question à propositions : opts = [texte…] repérées a, b, c… ; bonnes = « a » ou « bc » (plusieurs)."""
    keys = "abcdefgh"[:len(opts)]
    bonnes = "".join(sorted(bonnes))
    multi = len(bonnes) > 1
    # la case masquée reçoit les repères choisis, triés (« b,c ») ; le moteur les compare d'un bloc (« bc »)
    grader = {"type": "code", "equals": [bonnes]}
    attendu = " ; ".join(f"{k}) {o}" for k, o in zip(keys, opts) if k in bonnes)
    return {"kind": "grp", "qcm": True, "stem": stem, "multi": multi, "img": img, "why": why,
            "hint": "Une ou plusieurs réponses justes : sélectionne toutes celles qui conviennent.",
            "opts": list(zip(keys, opts)), "fields": [("Réponse", grader, attendu)]}


def QBAR(docs, ans="ci-dessous"):
    return {"kind": "qbar", "docs": list(docs), "ans": ans}
