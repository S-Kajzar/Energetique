#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Images des cartes de l'accueil et des pages d'activité, tirées des figures du manuel (src/images/originaux,
découpées par outils/extraire_figures.py) :
  - src/images/carte-*.jpg : une image par carte, 480 × 270, la figure entière centrée sur fond blanc ;
    deux figures côte à côte pour une activité qui réunit deux exercices (1.3) ;
  - src/images/accueil.jpg : montage d'illustration de l'accueil (quatre systèmes des activités).

    python3 outils/preparer_images.py"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORIG = ROOT / "src" / "images" / "originaux"
OUT = ROOT / "src" / "images"

# carte → figure(s) du manuel
CARTES = {
    "carte-cours": ["fig-tremplin"],
    "carte-1-1": ["fig-camion"],
    "carte-1-2": ["fig-palan-puissance"],
    "carte-1-3": ["fig-ascenseur", "fig-escalier"],
    "carte-1-4": ["fig-skieur"],
    "carte-1-5": ["fig-wagonnet-levage"],
    "carte-2-1": ["fig-tire-bouchon"],
    "carte-2-2": ["fig-amortisseur"],
    "carte-2-3": ["fig-amortisseur-ressort"],
    "carte-2-4": ["fig-freinage-pente"],
    "carte-2-5": ["fig-verin"],
    "carte-2-6": ["fig-balancier"],
    "carte-2-7": ["fig-frein-sabot"],
    "carte-2-8": ["fig-frein-disque"],
    "carte-2-9": ["fig-roues"],
}
MONTAGE = ["fig-ascenseur", "fig-roues", "fig-frein-sabot", "fig-freinage-pente"]


def dans(fig, w, h, marge=8):
    """La figure entière, réduite pour tenir dans w × h (marge comprise), centrée sur fond blanc."""
    im = Image.open(ORIG / f"{fig}.jpg").convert("RGB")
    k = min((w - 2 * marge) / im.width, (h - 2 * marge) / im.height)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    fond = Image.new("RGB", (w, h), "white")
    fond.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return fond


def carte(figs, w=480, h=270):
    if len(figs) == 1:
        return dans(figs[0], w, h)
    fond = Image.new("RGB", (w, h), "white")
    for i, f in enumerate(figs):
        fond.paste(dans(f, w // len(figs), h, 6), (i * w // len(figs), 0))
    return fond


def main():
    for nom, figs in CARTES.items():
        carte(figs).save(OUT / f"{nom}.jpg", quality=82, optimize=True)
    W, H = 720, 405
    m = Image.new("RGB", (W, H), "white")
    for i, f in enumerate(MONTAGE):
        m.paste(dans(f, W // 2, H // 2, 6), ((i % 2) * W // 2, (i // 2) * H // 2))
    m.save(OUT / "accueil.jpg", quality=82, optimize=True)
    poids = sum((OUT / f"{n}.jpg").stat().st_size for n in list(CARTES) + ["accueil"])
    print(f"{len(CARTES)} cartes et le montage d'accueil : {poids / 1024:.0f} Kio")


if __name__ == "__main__":
    main()
