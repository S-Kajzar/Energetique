#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Découpe les figures du manuel dans les pages photographiées fournies (PDF) et les nettoie : correction de
l'éclairage (division par le fond flou : ombres et dégradés de la photo disparaissent), niveaux, légère saturation.
Écrit src/images/originaux/fig-*.jpg, que reprend outils/preparer_images.py.

    python3 outils/extraire_figures.py cours.pdf exercices.pdf exo2.pdf

Les PDF ne sont pas versionnés (photographies d'un manuel) : seules les figures découpées le sont.
Cadres : fractions de la page (x0, y0, x1, y1), relevées sur les pages fournies."""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SORTIE = ROOT / "src" / "images" / "originaux"

# figure : (document, page (0 = première), cadre, légende du manuel)
FIGURES = {
    "fig-palan-reservoir": ("cours", 1, (0.105, 0.135, 0.975, 0.296), "Fig. 1 — Notion de puissance et d'énergie"),
    "fig-tremplin": ("cours", 0, (0.085, 0.705, 0.890, 0.940), "Le skieur sur le tremplin (ouverture du chapitre)"),
    "fig-skieur": ("cours", 0, (0.090, 0.705, 0.420, 0.935), "Le skieur en vol (ouverture du chapitre)"),
    "fig-camion": ("cours", 5, (0.525, 0.024, 0.985, 0.172), "Fig. 11 — Exemple : camion"),
    "fig-disque": ("cours", 6, (0.362, 0.345, 0.880, 0.487), "Fig. 14 — Disque plein roulant sans glisser"),
    "fig-palan-puissance": ("cours", 7, (0.660, 0.360, 0.972, 0.500), "Fig. 16 — Puissance développée par le palan"),
    "fig-frein-disque": ("cours", 9, (0.075, 0.060, 0.985, 0.300), "Fig. 18 — Frein à disque industriel"),
    "fig-ascenseur": ("exercices", 0, (0.560, 0.415, 0.915, 0.548), "Fig. 22 — Cabine d'ascenseur"),
    "fig-escalier": ("exercices", 0, (0.560, 0.565, 0.915, 0.684), "Fig. 23 — Escalier roulant"),
    "fig-tire-bouchon": ("exercices", 0, (0.098, 0.802, 0.915, 0.932), "Fig. 24 — Tire-bouchon"),
    "fig-wagonnet-levage": ("exercices", 1, (0.535, 0.290, 0.962, 0.490), "Fig. 25 — Wagonnet de levage"),
    "fig-amortisseur": ("exercices", 1, (0.540, 0.526, 0.956, 0.655), "Fig. 26 — Amortisseur de fin de course"),
    "fig-amortisseur-ressort": ("exercices", 1, (0.745, 0.540, 0.956, 0.655), "Fig. 26 — l'amortisseur à ressort"),
    "fig-freinage-pente": ("exercices", 1, (0.550, 0.792, 0.998, 0.938), "Fig. 27 — Freinage dans une pente"),
    "fig-verin": ("exo2", 0, (0.566, 0.026, 0.921, 0.259), "Fig. 31 — Vérin de levage"),
    "fig-balancier": ("exo2", 0, (0.567, 0.298, 0.921, 0.513), "Fig. 32 — Levage de balancier"),
    "fig-frein-sabot": ("exo2", 0, (0.570, 0.527, 0.921, 0.683), "Fig. 33 — Frein à sabot"),
    "fig-roues": ("exo2", 0, (0.579, 0.760, 0.921, 0.920), "Fig. 34 — Roues"),
}
# niveaux propres à une figure (noir, blanc) : la page du palan, mal éclairée, est plus pâle
NIVEAUX = {"fig-palan-puissance": (95, 238)}


def nettoyer(im, noir=40, blanc=232):
    """Photo d'une page → figure sur fond blanc : on divise par l'éclairage (le fond flou), puis on étale les niveaux."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    fond = np.asarray(im.convert("RGB").filter(ImageFilter.GaussianBlur(radius=max(im.size) / 18))).astype(np.float32)
    # le fond est estimé sur la luminance pour garder les couleurs des figures
    lum = fond.mean(axis=2, keepdims=True)
    a = np.clip(a / np.maximum(lum, 1) * 255 * 0.98, 0, 255)
    a = np.clip((a - noir) / (blanc - noir), 0, 1) ** 0.9 * 255
    out = Image.fromarray(a.astype(np.uint8))
    return ImageEnhance.Color(out).enhance(1.25)


def main(pdfs):
    noms = {"cours": None, "exercices": None, "exo2": None}
    for p in pdfs:
        n = pathlib.Path(p).name.lower()
        cle = "exo2" if "exo_2" in n or "exo2" in n else ("exercices" if "exercice" in n else "cours")
        noms[cle] = p
    assert all(noms.values()), f"trois PDF attendus (cours, exercices, exo 2) : {noms}"
    SORTIE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        pages = {}
        for cle, pdf in noms.items():
            subprocess.run(["pdfimages", "-j", pdf, f"{tmp}/{cle}"], check=True)
            pages[cle] = sorted(pathlib.Path(tmp).glob(f"{cle}-*.jpg"))
        for nom, (doc, page, (x0, y0, x1, y1), _leg) in FIGURES.items():
            im = Image.open(pages[doc][page])
            w, h = im.size
            fig = nettoyer(im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h))), *NIVEAUX.get(nom, (40, 232)))
            if fig.width > 1200:
                fig = fig.resize((1200, round(fig.height * 1200 / fig.width)), Image.LANCZOS)
            fig.save(SORTIE / f"{nom}.jpg", quality=86, optimize=True)
            print(f"{nom}.jpg : {fig.width} × {fig.height}")


if __name__ == "__main__":
    main(sys.argv[1:])
