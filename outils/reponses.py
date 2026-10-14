#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit tests/reponses.js : la réponse de référence de chaque case des activités, telle qu'un élève la saisirait
(nombre écrit à la française, avec son unité).
À relancer si les activités changent :  python3 outils/reponses.py"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import activites  # noqa: E402
import generer  # noqa: E402


def ecrit(v):
    """Quatre chiffres significatifs, virgule décimale, espace des milliers (comme une copie d'élève)."""
    if v == 0:
        return "0"
    d = max(0, 3 - int(math.floor(math.log10(abs(v)))))
    s = f"{v:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


rep = {}
for e in activites.ACTIVITES:
    generer.prepare_exo(e)
    for p in e["P"]:
        for b in p["blocks"]:
            if b["kind"] == "q":
                g = b["grader"]
                rep[b["id"]] = ecrit(g["value"]) + (" " + g["unit"]["label"] if "unit" in g else "")
            elif b["kind"] == "grp" and b.get("qcm"):
                rep[b["fids"][0]] = ",".join(b["fields"][0][1]["equals"][0])
txt = ("// Réponses de référence (écrites par outils/reponses.py) : une saisie juste pour chaque case des activités.\n"
       f"module.exports = {{\n  REP: {json.dumps(rep, ensure_ascii=False, indent=2)}\n}};\n")
(ROOT / "tests" / "reponses.js").write_text(txt, encoding="utf-8")
print(f"tests/reponses.js : {len(rep)} cases")
