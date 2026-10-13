#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère la page « Énergétique » (index.html) : un accueil sur le modèle des dépôts « Résistance des matériaux » et
« Chaîne fonctionnelle », deux cours interactifs (approche analytique, résolution graphique), le formulaire,
les activités tirées des exercices du cours (une activité par exercice, les plus courts réunis par deux) et la
rubrique « Études de cas », chacun ouvert par ?ex=…

    python3 src/generer.py

Le bloc <style> du gabarit, le moteur de correction (Grading) et le moteur applicatif sont recopiés tels quels ;
seules les entrées propres au sujet du moteur applicatif sont remplacées, chaque remplacement étant vérifié :
DECOR, DR_NAMES, le texte de la fenêtre « Imprimer les DR », le libellé « Diagramme validé » des questions à
plusieurs cases et CONSEIL_MIN, lu dans window.__CONSEIL_MIN__ puisque la durée conseillée dépend de l'activité
ouverte. Un petit script d'aiguillage, exécuté avant les moteurs, installe le contenu demandé par l'adresse.

Les activités de résolution graphique utilisent l'atelier de construction (src/construction.py) : ses planches
remplissent les cases masquées de leurs questions, que le moteur du gabarit corrige comme les autres.
"""
import copy
import json
import pathlib
import re

import activites
import construction
import cours_analytique
import cours_graphique
import figures
from commun import esc, fr, svg_uri

ROOT = pathlib.Path(__file__).resolve().parent.parent
GABARIT = ROOT / "src" / "gabarit-exercice-interactif.html"
SORTIE = ROOT / "index.html"
TITRE = "Énergétique"


def sub_once(text, pattern, repl, flags=0):
    """Remplacement vérifié : le motif doit apparaître exactement une fois."""
    new, n = re.subn(pattern, lambda m: repl, text, flags=flags)
    assert n == 1, f"motif introuvable ou multiple : {pattern!r} ({n})"
    return new


# ============================================================ rendu HTML des questions
def render_q(q, part):
    """Question à une case (saisie libre, valeur et unité)."""
    qid, label = q["id"], q["label"]
    return f"""
        <div class="q" id="{qid}" data-q="{qid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{q['stem']}</strong></p>
          <p class="q-hint" id="h-{qid}">{q['hint']}</p>
          <div class="q-row">
            <input type="text" class="q-input" id="in-{qid}" aria-label="Réponse {label}" aria-describedby="h-{qid}" autocomplete="off" autocapitalize="off" spellcheck="false">
            <button type="button" class="btn btn-validate">Valider</button>
            <span class="q-status" aria-live="polite"></span>
            <span class="print-only pstat">Non validée : comptée fausse</span>
          </div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="q-unit-msg" hidden></p>
            <p class="q-expected"><span>Réponse attendue :</span> {q['expected']}</p>
            <div class="q-why">{q['why']}</div>
          </div>
        </div>"""


def render_qcm(b):
    """Question à propositions : un clic coche une proposition ; la case du gabarit, masquée, reçoit les repères."""
    gid, label, fid = b["id"], b["label"], b["fids"][0]
    opts = "".join(f'<button type="button" class="qcm-o" data-k="{k}" role="checkbox" aria-checked="false">'
                   f'<span class="qcm-k">{k}</span><span class="qcm-t">{t}</span></button>' for k, t in b["opts"])
    return f"""
        <div class="fast-q grp qcm" id="{gid}" data-multi="1">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{b['stem']}</strong></p>
          <p class="q-hint">{b['hint']}</p>{b.get('img', '')}
          <div class="qcm-opts" role="group" aria-label="Propositions de la question {label}">{opts}</div>
          <div class="sol qcm-sol"><input type="hidden" id="in-{fid}" data-q="{fid}"><span class="mark" aria-live="polite"></span></div>
          <div class="fast-foot"><button type="button" class="btn btn-fast" disabled>Valider</button>
            <span class="q-status" aria-live="polite"></span></div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="qcm-rep"><b>Réponse attendue :</b> {b['fields'][0][2]}</p>
            <div class="q-why"><p class="why-t">Explication</p>{b['why']}</div>
          </div>
        </div>"""


def render_cg(b):
    """Construction graphique : la planche, puis le relevé de la construction (une ligne par case notée, son
    champ masqué que remplit la planche), le bouton « Valider » et la correction commune."""
    gid, label = b["id"], b["label"]
    rows = "".join(
        f'<div class="grp-l"><span class="grp-lab" id="lb-{fid}">{fl}</span><div class="sol">'
        f'<input type="hidden" id="in-{fid}" data-q="{fid}"><span class="cg-val" data-fid="{fid}">—</span>'
        f'<span class="mark" aria-live="polite"></span></div></div>'
        for fid, (fl, _g, _e) in zip(b["fids"], b["fields"]))
    sol = "".join(f"<tr><td>{fl}</td><td>{e}</td></tr>" for fl, _g, e in b["fields"])
    n = len(b["fields"])
    return f"""
        <div class="fast-q grp cg-q" id="{gid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{b['stem']}</strong></p>
          <p class="q-hint">{b['hint']}</p>
          {construction.rendu(b['cg'], b['fids'], label)}
          <p class="cg-releve-t">Relevé de ta construction (mis à jour à chaque tracé)</p>
          <div class="grp-fields" role="group" aria-label="Relevé de la construction {label}">{rows}</div>
          <div class="fast-foot"><button type="button" class="btn btn-fast">Valider la construction ({n} point{'s' if n > 1 else ''})</button>
            <span class="q-status" aria-live="polite"></span></div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <table class="t grp-sol"><thead><tr><th>Relevé</th><th>Attendu</th></tr></thead><tbody>{sol}</tbody></table>
            <div class="q-why"><p class="why-t">Construction attendue</p>{b['why']}</div>
          </div>
        </div>"""


def render_qbar(b):
    chips = " ".join(f'<button type="button" class="doc-chip" data-doc="{d}" aria-pressed="false">{d}</button>'
                     for d in b["docs"])
    return (f'\n      <div class="qbar" role="group" aria-label="{b["label"]}"><div class="qb-num">{b["label"]}</div>'
            f'<div class="qb-docs">Documents à consulter : {chips}</div><div class="qb-ans">Répondre : {b["ans"]}</div></div>')


def item_points(b):
    return {"q": 1, "grp": len(b.get("fields", ()))}.get(b["kind"], 0)


def part_points(p):
    return sum(item_points(b) for b in p["blocks"])


def hm(minutes):
    h, m = divmod(minutes, 60)
    return f"{h} h {m:02d}" if h else f"{m} min"


HOUSE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.3" '
         'stroke-linejoin="round" stroke-linecap="round"><path d="M3 11.5 12 4l9 7.5"/>'
         '<path d="M5.5 9.8V20h4.5v-5.5h4V20h4.5V9.8"/></svg>')

CUR = {"total": 1}


def pct(minutes):
    return fr(minutes / CUR["total"] * 100, 1)


def render_part(p):
    pts = part_points(p)
    body = "\n      ".join(p["intro"])
    blocks = []
    for b in p["blocks"]:
        if b["kind"] == "q":
            blocks.append(render_q(b, p))
        elif b["kind"] == "grp" and b.get("qcm"):
            blocks.append(render_qcm(b))
        elif b["kind"] == "grp" and b.get("cg"):
            blocks.append(render_cg(b))
        elif b["kind"] == "qbar":
            blocks.append(render_qbar(b))
        else:
            blocks.append(b["html"])
    n = p["num"]
    return f"""
  <section class="part" id="partie-{n}" aria-labelledby="t-partie-{n}">
    <header class="part-head"><div class="part-num" aria-hidden="true">{n}</div>
      <div><h2 id="t-partie-{n}"><span class="sr-only">Partie {n} : </span>{p['title']}</h2>
        <div class="duree">Durée conseillée : {hm(p['minutes'])} · Barème : {pts} point{'s' if pts > 1 else ''}, soit {pct(p['minutes'])} % de la note</div></div></header>
    <div class="part-body">
      {body}{''.join(blocks)}
    </div>
  </section>"""


def prepare_exo(e):
    """Copie et numérote les parties d'une activité (Q1.1, Q1.2…) ; calcule sa configuration pour les moteurs."""
    parts = copy.deepcopy(e["parts"])
    for i, p in enumerate(parts):
        p["num"] = str(i + 1)
        k = 0
        for b in p["blocks"]:
            if b["kind"] in ("q", "grp"):
                k += 1
                b["id"] = f"{e['prefix']}{p['num']}_{k}"
                b["label"] = f"Q{p['num']}.{k}"
                if b["kind"] == "grp":
                    b["fids"] = [f"{b['id']}_{j + 1}" for j in range(len(b["fields"]))]
                    if b.get("cg"):
                        assert len(b["cg"]["attendus"]) == len(b["fields"]), b["cg"]["id"]
        for j, b in enumerate(p["blocks"]):  # la barre de documents prend le numéro de la question qui la suit
            if b["kind"] == "qbar":
                nxt = next((x for x in p["blocks"][j + 1:] if x["kind"] in ("q", "grp")), None)
                b["label"] = nxt["label"] if nxt else f"Partie {p['num']}"
    e["P"] = parts
    e["minutes"] = sum(p["minutes"] for p in parts)
    e["n_q"] = sum(1 for p in parts for b in p["blocks"] if b["kind"] in ("q", "grp"))
    e["points"] = sum(part_points(p) for p in parts)
    e["n_cg"] = sum(1 for p in parts for b in p["blocks"] if b.get("cg"))
    qcfg, parts_cfg = {}, []
    for p in parts:
        parts_cfg.append({"num": p["num"], "title": p["title"], "minutes": p["minutes"],
                          "duration": hm(p["minutes"]), "points": part_points(p)})
        for b in p["blocks"]:
            if b["kind"] == "q":
                qcfg[b["id"]] = {"label": b["label"], "part": p["num"], "pts": 1, "grader": b["grader"]}
            elif b["kind"] == "grp":
                for fid, (fl, g, _x) in zip(b["fids"], b["fields"]):
                    lab = b["label"] if len(b["fields"]) == 1 else f"{b['label']} — {re.sub(r'<[^>]+>', '', fl)}"
                    qcfg[fid] = {"label": lab, "part": p["num"], "pts": 1, "grader": g}
    np_ = len(parts)
    cg = f", dont {e['n_cg']} construction{'s' if e['n_cg'] > 1 else ''} graphique{'s' if e['n_cg'] > 1 else ''}" if e["n_cg"] else ""
    e["cfg"] = {"title": e["title"], "minutes": e["minutes"], "duree": hm(e["minutes"]),
                "cartouche": f"{e['n_q']} questions{cg}, {e['points']} points, en {np_} partie"
                             f"{'s' if np_ > 1 else ''}" + (" pondérées par leur durée." if np_ > 1 else "."),
                "parts": parts_cfg, "qcfg": qcfg, "skcfg": {}}


def render_docs(e):
    rail, tabs, secs = [], [], []
    first_dt = True
    for key, title, kind, is_dt, content in sorted((d for d in activites.DOCS if d[0] in e["docs"]),
                                                   key=lambda d: (d[3], d[0])):
        if is_dt and first_dt:
            if rail:  # séparation entre dossiers de présentation et dossiers techniques
                rail.append('<div class="grp" aria-hidden="true"></div>')
            first_dt = False
        cls = "tab dt" if is_dt else "tab"
        rail.append(f'<button type="button" class="{cls}" data-doc="{key}" aria-selected="false" title="{esc(title)}">{key}</button>')
        tabs.append(f'<button type="button" data-doc="{key}" aria-selected="false">{key}</button>')
        secs.append(f'<section class="doc" id="doc-{key}" data-title="{key} : {esc(title)}" data-kind="{kind}">{content}\n</section>')
    return "".join(rail), "".join(tabs), "\n".join(secs)


def pastille(level):
    if not level:
        return ""
    return f' <span class="pastille n{level.split()[-1]}">{level}</span>'


def render_exo_home(e):
    docs = sorted(e["docs"])
    docs_txt = (", ".join(docs[:-1]) + " et " + docs[-1]) if len(docs) > 1 else (docs[0] if docs else "")
    np_ = len(e["P"])
    facts = ('<div class="home-facts">'
             f'<div><b>{np_} partie{"s" if np_ > 1 else ""}</b><span>{e["n_q"]} questions</span></div>'
             f'<div><b>{hm(e["minutes"])}</b><span>durée conseillée</span></div>' +
             (f'<div><b>{len(docs)} document{"s" if len(docs) > 1 else ""}</b><span>{docs_txt}</span></div>' if docs else
              '<div><b>Une réponse</b><span>ou plusieurs, à cocher</span></div>') +
             f'<div><b>{e["points"]} points</b><span>{"constructions comprises" if e["n_cg"] else "un par réponse"}</span></div></div>')
    return (f'<div class="home-top"><div class="home-top-l"><header class="home-head"><span class="mc-tag">{e["tag"]}</span>{pastille(e.get("level"))}'
            f'<h1 id="home-title">{e["title"]}</h1><p class="home-sub">{e["sub"]}</p></header>{facts}</div>'
            f'<figure class="home-hero"><img src="{svg_uri(e["hero"][0])}" alt="{esc(e["hero"][1])}" width="480" height="270">'
            f'<figcaption class="small">{e["hero"][2]}</figcaption></figure></div>')


MODES_HTML = """<h2 class="home-choose">Choisis ton mode de travail</h2>
<div class="modes">
  <article class="mode-card">
    <div class="mc-head"><span class="mc-tag">Mode 1</span><h3>Mode entraînement</h3></div>
    <p class="mc-lead">Pour apprendre en avançant, question par question.</p>
    <ul><li>Chaque question se valide isolément ; la démarche corrigée s'affiche aussitôt.</li>
      <li>La note pondérée s'actualise en continu dans le bandeau.</li>
      <li>Les documents et le chronomètre restent disponibles, sans contrainte de temps.</li></ul>
    <button type="button" class="btn btn-mode" data-mode="training">Commencer l'entraînement</button>
  </article>
  <article class="mode-card exam">
    <div class="mc-head"><span class="mc-tag">Mode 2</span><h3>Mode examen</h3></div>
    <p class="mc-lead">Pour se placer dans les conditions d'une évaluation.</p>
    <ul><li>Aucune correction et aucune note pendant la composition ; les réponses restent modifiables.</li>
      <li>Le chronomètre tourne, à comparer à la durée conseillée.</li>
      <li>En fin de sujet, le bouton « J'ai fini, je fais corriger ma copie » dévoile d'un coup les corrections, les notes par partie et la note globale.</li></ul>
    <button type="button" class="btn btn-mode" data-mode="exam">Composer en mode examen</button>
  </article>
</div>
<p class="home-note small">Le mode se choisit une seule fois : pour en changer, reviens à l'accueil (onglet maison) et rouvre l'activité. Rien n'est enregistré sur l'ordinateur.</p>
<p class="home-back"><a class="btn ghost" href="?">""" + HOUSE + """ Retour à l'accueil</a></p>"""


# ============================================================ ACCUEIL
COURS = [
    {"key": "cours-analytique", "tag": "Cours 1", "level": "Niveau 1", "title": "Énergétique : approche analytique",
     "mots": ["Travail", "Énergies", "Puissance", "Rendement", "Théorèmes"], "vign": figures.carte_cours_1,
     "alt": "Skieur sur un tremplin : l'énergie potentielle devient énergie cinétique"},
    {"key": "cours-graphique", "tag": "Cours 2", "level": "Niveau 2", "title": "Énergétique : résolution graphique",
     "mots": ["Échelles", "Projection", "Équiprojectivité", "CIR", "Puissances virtuelles"], "vign": figures.carte_cours_2,
     "alt": "Bielle et manivelle : vitesses construites par équiprojectivité"},
]
FORMULAIRE = {"key": "formulaire-energetique", "tag": "Formulaire", "title": "Formulaire d'énergétique",
              "mots": ["Formules", "Unités", "Méthodes graphiques"], "vign": figures.carte_formulaire,
              "alt": "Fiche de formules : travail, énergies, puissance, rendement"}
ATELIER = {"tag": "Atelier", "title": "Atelier de construction libre", "href": "?ex=cours-graphique#atelier",
           "mots": ["Outils de tracé", "Aimantation", "Échelles", "Sans note"], "vign": figures.carte_atelier,
           "alt": "Planche de construction : droites, perpendiculaires et vecteurs"}
# Rubrique « Études de cas » : tant qu'aucune étude n'est décrite, une carte l'annonce.
ETUDE_A_VENIR = ("Étude de cas", ["Système réel", "Bilan énergétique", "Choix d'un moteur"], figures.carte_etude,
                 "Treuil de levage : moteur, réducteur, tambour")
OUVRIR = ("Ouvrir l'activité", "Ouvrir l'étude")
RUBRIQUES = [("analytique", "Activités : approche analytique"), ("graphique", "Activités : résolution graphique")]


def carte(tag, title, mots, href, bouton, vign=None, alt="", cls=""):
    """Carte de l'accueil : vignette (dessin SVG), étiquette, titre, mots-clés, bouton."""
    img = '<div class="cv-img cv-vide" aria-hidden="true"></div>'
    if vign:
        img = f'<img class="cv-img" src="{svg_uri(vign())}" alt="{esc(alt)}" width="480" height="270">'
    mots_html = '<ul class="cv-mots">' + "".join(f"<li>{m}</li>" for m in mots) + "</ul>"
    btn = f'<a class="btn" href="{href}">{bouton}</a>' if href else '<p class="small ex-meta etat">En cours d\'édition</p>'
    return (f'<article class="mode-card carte-v {cls}">{img}<div class="mc-head"><span class="mc-tag">{tag}</span>'
            f"<h3>{title}</h3></div>{mots_html}{btn}</article>")


def _exo_card(e):
    return carte(e["tag"] + pastille(e.get("level")), e["title"], e["mots"], f'?ex={e["key"]}',
                 OUVRIR[bool(e.get("etude"))], e["vign"], e["valt"])


def render_hub():
    cours = "".join(carte(c["tag"] + pastille(c.get("level")), c["title"], c["mots"], f'?ex={c["key"]}', "Lire le cours",
                          c["vign"], c["alt"], "cours-card") for c in COURS)
    form = carte(FORMULAIRE["tag"], FORMULAIRE["title"], FORMULAIRE["mots"], f'?ex={FORMULAIRE["key"]}',
                 "Ouvrir le formulaire", FORMULAIRE["vign"], FORMULAIRE["alt"])
    rubs = ""
    for k, titre in RUBRIQUES:
        cards = "".join(_exo_card(e) for e in EXO_DEFS if e["rubrique"] == k and not e.get("etude"))
        if k == "graphique":
            cards += carte(ATELIER["tag"], ATELIER["title"], ATELIER["mots"], ATELIER["href"], "Ouvrir l'atelier",
                           ATELIER["vign"], ATELIER["alt"])
        rubs += f'<h2 class="home-choose">{titre}</h2><div class="ex-grid exo-grid rub-{k}">{cards}</div>'
    etudes = "".join(_exo_card(e) for e in EXO_DEFS if e.get("etude")) or carte(
        "Étude 1", ETUDE_A_VENIR[0], ETUDE_A_VENIR[1], None, None, ETUDE_A_VENIR[2], ETUDE_A_VENIR[3], "en-edition")
    return (f'<div class="home-top"><div class="home-top-l"><header class="home-head"><h1 id="home-title">{TITRE}</h1>'
            "<p class=\"home-sub\">Travail, énergies potentielle et cinétique, puissance, rendement : faire le bilan "
            "énergétique d'un mécanisme, puis en tirer un effort, une vitesse ou une puissance. Deux approches : le "
            "calcul (approche analytique) et la construction à l'échelle (résolution graphique, avec un atelier de "
            "tracé). Des cours, un formulaire et des activités de deux niveaux, à faire en mode entraînement ou en mode "
            "examen.</p></header></div>"
            f'<figure class="home-hero"><img src="{svg_uri(figures.hero_accueil())}" alt="Un skieur s\'élance d\'un '
            f'tremplin : à la hauteur h de départ correspond la vitesse v au bas de la piste" width="480" height="270">'
            '<figcaption class="small">La loi de conservation de l\'énergie relie la hauteur de départ et la vitesse '
            "d'envol.</figcaption></figure></div>"
            f'<h2 class="home-choose">Les cours</h2><div class="ex-grid cours-grid">{cours}</div>'
            f'<h2 class="home-choose">Le formulaire</h2><div class="ex-grid form-grid">{form}</div>'
            f'{rubs}'
            f'<h2 class="home-choose">Études de cas</h2><div class="ex-grid etude-grid">{etudes}</div>'
            f'<p class="home-note small">Pastilles : {pastille("Niveau 1").strip()} premier niveau, '
            f'{pastille("Niveau 2").strip()} niveau approfondi. Chaque activité propose le mode entraînement '
            "(correction question par question) ou le mode examen (correction à la remise de la copie). Les activités "
            "de résolution graphique se font sur des planches à l'échelle, avec les outils de l'atelier de "
            "construction. Rien n'est enregistré sur l'ordinateur.</p>")


# ============================================================ COURS — éléments communs (repris du dépôt « Chaîne fonctionnelle »)
def course_head(tag, level, title, sub):
    return (f'<div class="home-top home-top-single"><div class="home-top-l"><header class="home-head">'
            f'<span class="mc-tag">{tag}</span>{pastille(level)}<h1 id="home-title">{title}</h1>'
            f'<p class="home-sub">{sub}</p></header></div></div>')


def course_section(n, ident, titre, body):
    return (f'<section class="part cours-sec" id="{ident}" aria-labelledby="{ident}-t"><header class="part-head">'
            f'<div class="part-num" aria-hidden="true">{n}</div><div><h2 id="{ident}-t" style="padding:14px 16px">{titre}'
            f'</h2></div></header><div class="part-body">{body}</div></section>')


def course_nav(items):
    return ('<nav class="cours-nav no-print" aria-label="Étapes du cours">' +
            "".join(f'<a href="#{a}">{n}. {t}</a>' for n, (a, t) in enumerate(items, 1)) + "</nav>")


def quiz_html(questions, name):
    """Quiz noté (moteur initQuiz) : questions = [(énoncé, [choix], indice juste, explication)]."""
    return "".join(
        f'<fieldset class="quiz-q" data-ok="{ok}"><legend><span class="q-num">{i + 1}</span> {q}</legend>' +
        "".join(f'<label><input type="radio" name="{name}{i}" value="{j}"> {o}</label>' for j, o in enumerate(opts)) +
        f'<p class="quiz-fb" aria-live="polite"></p><p class="quiz-why" hidden>{why}</p></fieldset>'
        for i, (q, opts, ok, why) in enumerate(questions))


def quiz_section(n, ident, questions, name):
    return course_section(n, ident, "Quiz : vérifie tes connaissances",
                          f'<p>Choisis une réponse : la correction s\'affiche aussitôt.</p><div class="quiz">'
                          f'{quiz_html(questions, name)}</div><div class="quiz-score" aria-live="polite">'
                          f'<span id="qz-score">0 / {len(questions)}</span><span id="qz-stars" aria-hidden="true"></span>'
                          '<button type="button" class="btn ghost" id="qz-reset">Recommencer</button></div>')


def jeu_html(lignes, choix, ident):
    """Jeu de classement : chaque ligne (libellé, clé juste) propose les mêmes boutons (clé, texte)."""
    rows = "".join(
        f'<div class="jeu-l" data-ok="{ok}"><span>{t}</span>' +
        "".join(f'<button type="button" class="btn ghost" data-v="{k}">{nm}</button>' for k, nm in choix) +
        '<b class="jeu-fb" aria-live="polite"></b></div>' for t, ok in lignes)
    return (f'<div class="jeu" id="{ident}">{rows}<p class="jeu-score" aria-live="polite">Score : '
            f'<span class="jeu-s">0 / {len(lignes)}</span> <button type="button" class="btn ghost jeu-reset">'
            'Recommencer</button></p></div>')


AIDES = type("Aides", (), {})()
for _f in (course_head, course_section, course_nav, quiz_html, quiz_section, jeu_html, pastille):
    setattr(AIDES, _f.__name__, _f)

COURS_COMMUN_JS = r"""
  function initQuiz(root) {
    function q(s) { return root.querySelector(s); }
    function qa(s) { return Array.prototype.slice.call(root.querySelectorAll(s)); }
    var qs = qa(".quiz-q");
    function score() {
      var n = qs.filter(function (f) { return f.classList.contains("is-ok"); }).length;
      var done = qs.filter(function (f) { return f.classList.contains("done"); }).length;
      var st = n === qs.length ? 3 : n >= qs.length - 2 ? 2 : n >= 2 ? 1 : 0;
      q("#qz-score").textContent = n + " / " + qs.length;
      q("#qz-stars").textContent = done === qs.length ? "★★★".slice(0, st) + "☆☆☆".slice(0, 3 - st) : "";
    }
    qs.forEach(function (fs) {
      fs.addEventListener("change", function (e) {
        if (fs.classList.contains("done")) return;
        var ok = e.target.value === fs.getAttribute("data-ok");
        fs.classList.add("done", ok ? "is-ok" : "is-ko");
        fs.querySelector(".quiz-fb").textContent = ok ? "✔ Bonne réponse !" : "✘ Pas tout à fait.";
        fs.querySelector(".quiz-why").hidden = false;
        Array.prototype.forEach.call(fs.querySelectorAll("input"), function (i) {
          i.disabled = true;
          if (i.value === fs.getAttribute("data-ok")) i.parentNode.classList.add("good");
        });
        score();
      });
    });
    q("#qz-reset").addEventListener("click", function () {
      qs.forEach(function (fs) {
        fs.classList.remove("done", "is-ok", "is-ko");
        fs.querySelector(".quiz-fb").textContent = "";
        fs.querySelector(".quiz-why").hidden = true;
        Array.prototype.forEach.call(fs.querySelectorAll("input"), function (i) { i.disabled = false; i.checked = false; i.parentNode.classList.remove("good"); });
      });
      score();
    });
    score();
  }
  // jeu de classement : un clic par ligne, le bon bouton est montré en cas d'erreur
  function initJeu(box) {
    var lignes = Array.prototype.slice.call(box.querySelectorAll(".jeu-l"));
    function score() {
      box.querySelector(".jeu-s").textContent = lignes.filter(function (l) { return l.classList.contains("is-ok"); }).length + " / " + lignes.length;
    }
    lignes.forEach(function (l) {
      Array.prototype.forEach.call(l.querySelectorAll("button"), function (b) {
        b.addEventListener("click", function () {
          if (l.classList.contains("is-ok") || l.classList.contains("is-ko")) return;
          var good = l.getAttribute("data-ok"), ok = b.getAttribute("data-v") === good;
          l.classList.add(ok ? "is-ok" : "is-ko");
          b.classList.add(ok ? "pick-ok" : "pick-ko");
          if (!ok) l.querySelector('button[data-v="' + good + '"]').classList.add("pick-good");
          l.querySelector(".jeu-fb").textContent = ok ? "✔" : "✘";
          score();
        });
      });
    });
    box.querySelector(".jeu-reset").addEventListener("click", function () {
      lignes.forEach(function (l) {
        l.classList.remove("is-ok", "is-ko");
        l.querySelector(".jeu-fb").textContent = "";
        Array.prototype.forEach.call(l.querySelectorAll("button"), function (b) { b.classList.remove("pick-ok", "pick-ko", "pick-good"); });
      });
      score();
    });
    score();
  }
  // cartes à retourner
  function initCartes(root) {
    Array.prototype.forEach.call(root.querySelectorAll(".carte"), function (b) {
      b.addEventListener("click", function () { b.setAttribute("aria-expanded", b.getAttribute("aria-expanded") === "true" ? "false" : "true"); });
    });
  }
  function fr(x, d) { return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/^-/, "−"); }
  function frs(x, n) {  // n chiffres significatifs
    if (!isFinite(x) || x === 0) return "0";
    var d = Math.max(0, (n || 3) - 1 - Math.floor(Math.log10(Math.abs(x))));
    return fr(x, Math.min(d, 6));
  }
  var SVGNS = "http://www.w3.org/2000/svg";
  function svgEl(tag, at, parent) {
    var e = document.createElementNS(SVGNS, tag);
    for (var k in at) e.setAttribute(k, at[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  // flèche (vecteur) de (x1, y1) à (x2, y2) : chemin de la tige et de la pointe
  function flecheD(x1, y1, x2, y2, h) {
    var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy);
    if (L < 0.5) return "";
    h = Math.min(h || 9, L * 0.45);
    var ux = dx / L, uy = dy / L, bx = x2 - ux * h, by = y2 - uy * h;
    return "M" + x1 + " " + y1 + "L" + (x2 - ux * h * 0.7) + " " + (y2 - uy * h * 0.7) +
      "M" + x2 + " " + y2 + "L" + (bx - uy * h * 0.38) + " " + (by + ux * h * 0.38) + "L" + (bx + uy * h * 0.38) + " " + (by - ux * h * 0.38) + "Z";
  }
  function lier(root, sel, fn) {  // curseurs et cases : recalcul à chaque changement
    Array.prototype.forEach.call(root.querySelectorAll(sel), function (i) { i.addEventListener("input", fn); i.addEventListener("change", fn); });
    fn();
  }
"""

COURS_COMMUN_CSS = """
/* ---------- cours interactifs (repris des dépôts RDM et « Chaîne fonctionnelle ») ---------- */
.cours .part{margin-bottom:22px}
.cours-nav{display:flex; flex-wrap:wrap; gap:6px; margin:0 0 16px}
.cours-nav a{font:600 .92rem var(--f-titre); color:var(--encre); background:var(--papier); border:1.5px solid var(--encre); padding:5px 12px; text-decoration:none}
.cours-nav a:hover{background:var(--jaune-pale)}
.cours .part-body h3{font:700 1.12rem var(--f-titre); margin:18px 0 6px}
.formule{display:flex; flex-wrap:wrap; gap:14px 28px; align-items:center; border:2px solid var(--rouge); background:#fff; padding:10px 18px; margin:12px 0; max-width:720px}
.formule .f-main{font:700 1.35rem var(--f-titre); line-height:2}
.formule .f-units{font-size:.9rem; color:var(--encre-2)}
.simu{border:2px solid var(--bleu); background:var(--bleu-pale); padding:12px 16px; margin:14px 0}
.simu h3{margin:0 0 8px!important; font:700 1.15rem var(--f-titre); color:var(--bleu)}
.simu-grid{display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px 18px}
@media (max-width:640px){ .simu-grid{grid-template-columns:1fr} }
.simu-grid label{display:block; font-weight:600; font-size:.92rem}
.simu-grid label input[type=range],.simu-grid label select{display:block; margin-top:4px}
.simu-grid output{margin-left:4px}
.simu-grid output{font:700 1rem var(--f-titre); color:var(--bleu)}
.simu-grid input[type=range]{width:100%; accent-color:var(--bleu)}
.simu-grid select{padding:5px; border:1.5px solid var(--encre-2); background:#fff; font:inherit}
.simu-out{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin:12px 0 8px}
.simu-out div{background:var(--encre); color:#fff; padding:6px 10px}
.simu-out span{display:block; font-size:.78rem; color:#D7DDE2}
.simu-out b{font:700 1.1rem var(--f-titre); color:var(--jaune)}
.simu-out4{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:760px){ .simu-out,.simu-out4{grid-template-columns:repeat(2,minmax(0,1fr))} }
.simu-verdict{font-weight:700; margin:8px 0 4px}
.simu-verdict.ok{color:var(--vert)} .simu-verdict.ko{color:var(--rouge)}
.simu-defi{margin-top:8px; background:#fff; border:1px dashed var(--bleu); padding:6px 10px}
.simu-defi summary{cursor:pointer; font-weight:600}
.simu-svg{display:block; width:100%; height:auto; max-width:760px; background:#fff; border:1px solid var(--trait-fin); margin:8px 0; font-family:var(--f-texte)}
.exemple{background:#F6F7F4; border:1px solid var(--trait-fin); padding:6px 16px; margin-top:12px}
.exemple h3{font:700 1.05rem var(--f-titre); margin:10px 0 4px}
.remarque{border-left:6px solid var(--jaune); background:var(--jaune-pale); padding:8px 14px; margin:12px 0; max-width:80ch}
.remarque p{margin:.2rem 0}
.quiz{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px}
.quiz-q{border:1.5px solid var(--encre); background:#fff; padding:8px 14px 10px; margin:0}
.quiz-q legend{font-weight:700; padding:0 4px}
.quiz-q label{display:block; padding:3px 0; cursor:pointer}
.quiz-q.is-ok{border-color:var(--vert); background:var(--vert-pale)}
.quiz-q.is-ko{border-color:var(--rouge); background:var(--rouge-pale)}
.quiz-q label.good{font-weight:700; color:var(--vert)}
.quiz-fb{margin:4px 0 0; font-weight:700}
.quiz-q.is-ok .quiz-fb{color:var(--vert)} .quiz-q.is-ko .quiz-fb{color:var(--rouge)}
.quiz-why{margin:2px 0 0; font-size:.9rem}
.quiz-score{display:flex; align-items:center; gap:14px; margin:14px 0 0; font:700 1.3rem var(--f-titre)}
#qz-stars{color:var(--jaune); font-size:1.6rem; letter-spacing:2px}
.jeu{border:2px solid var(--encre); background:#fff; padding:10px 14px; margin:12px 0 0}
.jeu-l{display:flex; flex-wrap:wrap; gap:6px 8px; align-items:center; padding:6px 0; border-top:1px solid var(--trait-fin)}
.jeu-l>span{flex:1 1 240px; font-weight:600}
.jeu-l .btn{padding:4px 9px; font-size:.88rem}
.jeu-l .btn.pick-ok{background:var(--vert); border-color:var(--vert); color:#fff}
.jeu-l .btn.pick-ko{background:var(--rouge); border-color:var(--rouge); color:#fff}
.jeu-l .btn.pick-good{outline:3px solid var(--vert); outline-offset:1px}
.jeu-l.is-ok{background:var(--vert-pale)} .jeu-l.is-ko{background:var(--rouge-pale)}
.jeu-fb{min-width:1.5em; font-size:1.1rem} .jeu-l.is-ok .jeu-fb{color:var(--vert)} .jeu-l.is-ko .jeu-fb{color:var(--rouge)}
.jeu-score{display:flex; align-items:center; gap:12px; font:700 1.2rem var(--f-titre); margin:8px 0 0}
.jeu-score .btn{font-size:.9rem; padding:5px 12px}
.cartes{display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:12px; margin:8px 0 14px}
.carte{display:flex; flex-direction:column; gap:6px; align-items:flex-start; text-align:left; min-height:96px; padding:12px 14px; border:2px solid var(--encre); border-left-width:8px; border-left-color:var(--bleu); background:var(--jaune-pale); font:inherit; cursor:pointer}
.carte b{font:700 1.15rem var(--f-titre); letter-spacing:.03em; color:var(--bleu)}
.carte .dos{display:none; font-size:.93rem}
.carte .dos i{display:block; margin-top:4px; font-style:normal; color:var(--encre-2)}
.carte[aria-expanded="true"]{background:#fff}
.carte[aria-expanded="true"] .dos{display:block}
.carte[aria-expanded="false"]::after{content:"Clique pour retourner"; font-size:.8rem; color:var(--encre-2)}
.cours-foot{display:flex; flex-wrap:wrap; gap:10px; margin:6px 0 0}
.cours-foot .small{align-self:center}
@media print{
  body.cours-page #home{display:block!important; padding:0}
  .no-print,.cours-nav,.cours-foot{display:none!important}
  .quiz-why[hidden]{display:block!important}
  .carte .dos{display:block!important}
  .carte::after{display:none!important}
}
"""

COURS_RENDER = {"cours-analytique": lambda: cours_analytique.render(AIDES),
                "cours-graphique": lambda: cours_graphique.render(AIDES),
                "formulaire-energetique": lambda: activites.page_formulaire(AIDES)}
COURS_JS = (COURS_COMMUN_JS + cours_analytique.JS + cours_graphique.JS +
            '\n  var INIT = { "cours-analytique": initCoursAnalytique, "cours-graphique": initCoursGraphique, '
            '"formulaire-energetique": function () {} };\n')
COURS_CSS = COURS_COMMUN_CSS + cours_analytique.CSS + cours_graphique.CSS


# ============================================================ AIGUILLAGE
ROUTER_JS = r"""<script>/* Aiguillage : accueil, cours ou activité selon ?ex=… — s'exécute avant les moteurs du gabarit */
(function () {
  "use strict";
  var EXOS = window.__EXOS__, ex = new URLSearchParams(location.search).get("ex") || "";
  function $(s) { return document.querySelector(s); }
  function tpl(id) { return document.getElementById(id).innerHTML; }__COURS_JS__
  var home = $("#home .home-inner");
  window.__PARTS__ = []; window.__QCFG__ = {}; window.__SKCFG__ = {}; window.__CONSEIL_MIN__ = 0;
  if (Object.prototype.hasOwnProperty.call(EXOS, ex)) {
    var E = EXOS[ex];
    window.__PARTS__ = E.parts; window.__QCFG__ = E.qcfg; window.__SKCFG__ = E.skcfg;
    window.__CONSEIL_MIN__ = E.minutes;
    document.title = E.title + " — __TITRE__ — activité interactive";
    document.body.classList.add("exo-" + ex);
    $(".rail").innerHTML = tpl("tpl-rail-" + ex) + '<div class="grp" aria-hidden="true"></div>' +
      '<a class="tab tab-home" href="?" title="Retour à l\'accueil" aria-label="Retour à l\'accueil">__HOUSE__</a>';
    $(".dp-tabs").innerHTML = tpl("tpl-tabs-" + ex);
    $(".dp-body").innerHTML = tpl("tpl-docs-" + ex);
    $("#parts").innerHTML = tpl("tpl-parts-" + ex);
    $(".consignes").innerHTML = tpl("tpl-consignes-" + ex);
    home.innerHTML = tpl("tpl-home-" + ex) + tpl("tpl-modes");
    $(".cartouche h1").textContent = E.title;
    $(".cartouche .title p").textContent = E.cartouche;
    Array.prototype.forEach.call(document.querySelectorAll(".print-conseil"), function (el) { el.textContent = E.duree; });
  } else {
    document.body.classList.add("hub");
    var page = document.getElementById("tpl-" + ex) && /^(cours-|formulaire-)/.test(ex) ? "tpl-" + ex : "tpl-hub";
    home.innerHTML = tpl(page);
    if (page !== "tpl-hub") {
      document.body.classList.add("cours-page", "page-" + ex);
      if (typeof INIT[ex] === "function") INIT[ex](home);
      document.title = home.querySelector("h1").textContent + " — __TITRE__";
    } else document.title = "__TITRE__ — cours et activités interactives";
  }
})();
</script>"""


CONTENT_CSS = """<style>
/* ---------- compléments de contenu (hors gabarit) : écriture des calculs, documents ---------- */
.eq{margin:.35rem 0 .55rem; overflow-x:auto; line-height:2.1}
.frac{display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; margin:0 .12em; line-height:1.25}
.frac>span{padding:0 .25em; white-space:nowrap}
.frac>span:first-child{border-bottom:1px solid currentColor}
.vec{position:relative; display:inline-block; font-style:italic; padding-top:.32em; line-height:1}
.vec::before{content:""; position:absolute; left:.04em; right:-.08em; top:.08em; border-top:1.2px solid currentColor}
.vec::after{content:""; position:absolute; right:-.14em; top:-.12em; border:solid currentColor; border-width:1.2px 1.2px 0 0; width:.24em; height:.24em; transform:rotate(45deg)}
.doc-text ol,.doc-text ul{padding-left:1.2rem}
.doc-text li{margin:.2rem 0}
.doc-text h3{font:700 1.08rem var(--f-titre); margin:14px 0 6px}
.calc{display:inline-block; font:600 .9rem ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; background:#fff; border:1px solid var(--trait); padding:2px 8px; margin:2px 0}
.cours-split{display:flex; gap:18px; align-items:flex-start; flex-wrap:wrap}
.cours-split>div{flex:1 1 300px}
.cours-split>.fig{flex:0 1 auto; margin:0 auto}
.part-body .fig{margin:14px auto}
.fig svg{display:block; width:100%; height:auto; font-family:var(--f-texte)}
.fig-svg{background:#fff; border:1px solid var(--trait-fin); padding:6px}
.fig figcaption{font-size:.86rem; color:var(--encre-2); margin-top:4px}
/* figures redessinées (SVG) : traits, cotes, vecteurs */
.fs .m{fill:none; stroke:#1C2530; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round}
.fs .mf{fill:#E9ECE8; stroke:#1C2530; stroke-width:1.4; stroke-linejoin:round}
.fs .mb{fill:#D9DFE6; stroke:#1C2530; stroke-width:1.4; stroke-linejoin:round}
.fs .mo{fill:#F6E2C2; stroke:#1C2530; stroke-width:1.4; stroke-linejoin:round}
.fs .fin{fill:none; stroke:#5A6670; stroke-width:1}
.fs .axe{fill:none; stroke:#5A6670; stroke-width:.8; stroke-dasharray:14 3 2 3}
.fs .h{stroke:#1C2530; stroke-width:1}
.fs .art{fill:#fff; stroke:#1C2530; stroke-width:1.4}
.fs text{font-size:13px; fill:#1C2530}
.fs .tn{font-weight:700; font-style:italic}
.fs .tc{font-size:11.5px; fill:#46525C}
.fs .tr{fill:#B42318; font-weight:700}
.fs .tb{fill:#1F5FA8; font-weight:700}
.fs .ind{font-size:.72em; font-style:normal}
.fs .vr{stroke:#B42318; fill:#B42318} .fs .vb{stroke:#1F5FA8; fill:#1F5FA8} .fs .vk{stroke:#1C2530; fill:#1C2530} .fs .vv{stroke:#1B7A43; fill:#1B7A43}
.fs .vr,.fs .vb,.fs .vk,.fs .vv{stroke-width:2.2; stroke-linecap:round}
.fs .vrl{stroke:#B42318; fill:none; stroke-width:2.2} .fs .vbl{stroke:#1F5FA8; fill:none; stroke-width:2.2}
.fs .cote{stroke:#5A6670; stroke-width:.9; fill:#5A6670}
.fs .pointille{fill:none; stroke:#5A6670; stroke-width:1; stroke-dasharray:4 3}

/* ---------- questions à plusieurs cases (mécanisme « fast-q » du gabarit) ---------- */
.grp{margin:14px 0 6px; padding:10px 0 12px 14px; border-left:3px solid var(--trait-fin)}
.grp-fields{display:flex; flex-direction:column; gap:6px; margin:8px 0 4px; max-width:820px}
.grp-l{display:grid; grid-template-columns:minmax(150px,.9fr) minmax(0,1.3fr); gap:4px 14px; align-items:center; padding:2px 0; border-bottom:1px dashed var(--trait-fin)}
.grp-lab{font-size:.95rem}
.grp .sol{display:flex; align-items:center; gap:8px}
.grp .sol .mark{flex:0 0 4.6em; font-size:.82rem; font-weight:700}
.grp .sol.is-ok .mark{color:var(--vert)} .grp .sol.is-ko .mark{color:var(--rouge)}
.grp .sol.is-ok .cg-val{color:var(--vert)} .grp .sol.is-ko .cg-val{color:var(--rouge)}
.grp .fast-foot .q-status{font-weight:700}
.grp-sol{max-width:780px; margin:4px 0 8px}
.grp-sol td:last-child{font-weight:600}
.q-why .why-t{font:700 .95rem var(--f-titre); margin:.6rem 0 .2rem}
.cg-releve-t{margin:10px 0 0; font:700 .85rem var(--f-titre); text-transform:uppercase; letter-spacing:.04em; color:var(--encre-2)}
@media (max-width:620px){ .grp-l{grid-template-columns:minmax(0,1fr)} }
/* ---------- QCM (questions à propositions) ---------- */
.qcm-opts{display:flex; flex-direction:column; gap:6px; margin:8px 0 4px; max-width:820px}
.qcm-o{display:flex; align-items:center; gap:10px; width:100%; text-align:left; background:#fff; border:1.5px solid var(--trait); border-radius:3px; padding:8px 12px; font:inherit; font-size:.97rem; color:var(--encre); cursor:pointer}
.qcm-o:hover:not(:disabled){border-color:var(--encre); background:var(--jaune-pale)}
.qcm-o:focus-visible{outline:3px solid var(--jaune); outline-offset:1px}
.qcm-k{flex:0 0 auto; min-width:1.9em; height:1.9em; display:inline-flex; align-items:center; justify-content:center; border:1.5px solid var(--bleu); color:var(--bleu); font:700 .85rem var(--f-titre); border-radius:3px}
.qcm-o[aria-checked="true"]{border-color:var(--bleu); background:var(--bleu-pale); box-shadow:inset 0 0 0 1px var(--bleu)}
.qcm-o[aria-checked="true"] .qcm-k{background:var(--bleu); color:#fff}
.qcm-o:disabled{cursor:default}
.qcm-o.ok{border-color:var(--vert); background:var(--vert-pale)} .qcm-o.ok .qcm-k{border-color:var(--vert); background:var(--vert); color:#fff}
.qcm-o.ko{border-color:var(--rouge); background:var(--rouge-pale)} .qcm-o.ko .qcm-k{border-color:var(--rouge); background:var(--rouge); color:#fff}
.qcm-o .qcm-tag{margin-left:auto; flex:0 0 auto; font:700 .75rem var(--f-titre); padding:1px 7px; color:#fff}
.qcm-o.ok .qcm-tag{background:var(--vert)} .qcm-o.ko .qcm-tag{background:var(--rouge)}
.qcm-sol{min-height:0}
.qcm-rep{margin:0 0 6px}
@media print{ .qcm-o{padding:2px 8px; font-size:9pt; break-inside:avoid} .qcm{break-inside:avoid} }

/* ---------- accueil, cours et retour (d'après les dépôts RDM et « Chaîne fonctionnelle ») ---------- */
a.btn{display:inline-flex; align-items:center; gap:8px; text-decoration:none}
a.btn svg,.c-top svg{width:18px; height:18px; flex:0 0 auto}
.tab-home{display:flex; align-items:center; justify-content:center; padding:8px 0 8px 4px; background:var(--encre); color:var(--jaune); text-decoration:none}
.tab-home svg{width:22px; height:22px; display:block}
.tab-home:hover{background:#2E3B47}
.c-top{margin:0 0 12px}
.c-top a{display:inline-flex; align-items:center; gap:6px; font:600 .95rem var(--f-titre); color:var(--encre); text-decoration:none; border:1.5px solid var(--encre); background:var(--papier); padding:5px 12px 5px 10px}
.c-top a:hover{background:var(--jaune-pale)}
#home{padding:20px 20px 32px}
.home-top{display:grid; grid-template-columns:minmax(0,1.6fr) minmax(0,1fr); gap:14px; align-items:stretch; margin:0 0 14px}
.home-top-single{grid-template-columns:1fr}
.home-top-l{display:flex; flex-direction:column; gap:10px; min-width:0}
.home-top .home-head{padding:14px 20px; flex:1}
.home-top .home-head h1{margin:6px 0 6px; font-size:clamp(1.4rem,2.4vw,1.85rem)}
.home-top .home-sub{font-size:.95rem}
.home-top .home-hero{margin:0; padding:8px; display:flex; flex-direction:column; justify-content:center; min-width:0}
.home-top .home-hero img{width:auto!important; max-width:100%; max-height:170px; margin:0 auto}
body.hub .home-top .home-hero img{max-height:210px}
.home-top .home-hero figcaption{font-size:.78rem; line-height:1.3; margin-top:4px}
.home-top .home-facts{grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin:0}
.home-top .home-facts div{padding:6px 10px}
.home-top .home-facts b{font-size:1.02rem}
.home-top .home-facts span{font-size:.76rem; line-height:1.3; display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
@media (max-width:980px){ .home-top .home-facts{grid-template-columns:repeat(2,minmax(0,1fr))} }
@media (max-width:820px){ .home-top{grid-template-columns:1fr} }
#home .home-choose{margin:18px 0 8px; font-size:1.25rem}
#home .mode-card{padding:12px 18px 14px}
#home .mode-card .mc-lead{margin:2px 0 4px; font-size:.92rem}
#home .mode-card ul{margin:0 0 10px; font-size:.9rem; line-height:1.45}
#home .mode-card li{margin:.15rem 0}
#home .mode-card .btn{padding:9px 16px}
#home .home-note{margin:10px 0 0}
.home-back{margin:12px 0 0}
.ex-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:16px}
.ex-grid .mode-card p{margin:4px 0 8px; font-size:.95rem}
.ex-grid .mode-card .ex-meta{margin:0 0 12px; font-size:.85rem}
.ex-grid .mode-card h3{font-size:1.2rem}
.ex-grid .mc-head{flex-direction:column; align-items:flex-start; gap:6px}
.ex-grid .mode-card .btn{margin-top:auto; align-self:flex-start}
.ex-grid .en-edition{border-style:dashed; border-color:var(--trait)}
.ex-grid .en-edition h3,.ex-grid .en-edition p{color:var(--encre-2)}
.ex-grid .etat{font-weight:700; color:var(--orange)}
/* cartes de l'accueil : image, titre, mots-clés ; toutes de la même taille, dans toutes les rubriques */
body.hub .ex-grid{grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); grid-auto-rows:1fr}
.carte-v{display:grid; grid-template-rows:auto auto 62px 46px; gap:8px; padding:0 0 16px!important; overflow:hidden; height:100%}
body.hub .carte-v>*:not(.cv-img){margin-left:18px; margin-right:18px}
.carte-v .cv-img{display:block; width:100%; height:auto; aspect-ratio:16/9; object-fit:cover; background:#fff; border-bottom:2px solid var(--encre); margin:0}
.carte-v .cv-vide{background:repeating-linear-gradient(135deg,#F4F5F2 0 12px,#ECEEEA 12px 24px)}
.carte-v .mc-head{margin:6px 18px 0}
.carte-v h3{margin:0; min-height:2.4em; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; line-height:1.2}
#home .carte-v .cv-mots{display:flex; flex-wrap:wrap; align-content:flex-start; gap:5px; list-style:none; margin:0 18px; padding:0}
#home .carte-v .cv-mots li{margin:0}
body.hub .carte-v .btn,body.hub .carte-v .etat{align-self:end; justify-self:start; margin-top:0; margin-bottom:0}
.cv-mots li{font:600 .8rem var(--f-titre); background:var(--bleu-pale); color:var(--encre); border:1px solid #C9D8EC; padding:2px 8px; border-radius:12px; white-space:nowrap}
.en-edition .cv-img{filter:grayscale(1) opacity(.55)}
.en-edition .cv-mots li{background:#F4F5F2; border-color:var(--trait-fin); color:var(--encre-2)}
.pastille{display:inline-block; font:700 .72rem var(--f-titre); letter-spacing:.03em; background:var(--vert); color:#fff; padding:2px 8px; margin-left:6px; vertical-align:middle}
.pastille.n2{background:var(--bleu)}
.mc-tag .pastille{margin-left:8px; font-size:.68rem; padding:1px 6px}

__COURS_CSS__
@media print{
  .c-top,.home-back{display:none!important}
  /* correctif repris du dépôt RDM : dans le gabarit, « .sketch .q-expl[hidden] » l'emporte sur
     « body:not(.corrections-open) .q-expl » et imprimerait la correction des tracés avant la remise de la copie */
  body:not(.corrections-open) .sketch .q-expl[hidden]{display:none!important}
  .eq{overflow:visible; line-height:1.7}
  .grp-l{break-inside:avoid}
}
</style>"""


QCM_JS = r"""<script>/* QCM : un clic coche ou décoche une proposition ; les repères cochés, triés, vont dans la case masquée du gabarit */
(function () {
  "use strict";
  var parts = document.getElementById("parts");
  if (!parts || !parts.querySelector(".qcm")) return;
  function inp(q) { return q.querySelector(".sol input"); }
  function maj(q) {
    var i = inp(q), v = Array.prototype.filter.call(q.querySelectorAll(".qcm-o"), function (o) { return o.getAttribute("aria-checked") === "true"; })
      .map(function (o) { return o.getAttribute("data-k"); }).sort().join(",");
    i.value = v;
    var b = q.querySelector(".btn-fast");
    if (!i.disabled) b.disabled = !v;
    i.dispatchEvent(new Event("input", { bubbles: true }));
  }
  parts.addEventListener("click", function (e) {
    var o = e.target.closest(".qcm-o");
    if (!o || o.disabled) return;
    var q = o.closest(".qcm");
    if (inp(q).disabled) return;
    o.setAttribute("aria-checked", o.getAttribute("aria-checked") === "true" ? "false" : "true");
    maj(q);
  });
  parts.addEventListener("keydown", function (e) {
    var o = e.target.closest && e.target.closest(".qcm-o");
    if (!o || (e.key !== "ArrowDown" && e.key !== "ArrowUp")) return;
    var all = Array.prototype.slice.call(o.parentNode.querySelectorAll(".qcm-o")), k = all.indexOf(o) + (e.key === "ArrowDown" ? 1 : -1);
    if (all[k]) { e.preventDefault(); all[k].focus(); }
  });
  // une fois la question corrigée par le moteur (champ verrouillé) : propositions justes et fausses marquées
  function corriger(q) {
    var id = inp(q).getAttribute("data-q"), g = (window.__QCFG__[id] || {}).grader || {}, bons = {};
    String((g.equals || [""])[0]).split("").forEach(function (k) { bons[k] = 1; });
    Array.prototype.forEach.call(q.querySelectorAll(".qcm-o"), function (o) {
      var k = o.getAttribute("data-k"), sel = o.getAttribute("aria-checked") === "true", tag;
      o.disabled = true;
      if (bons[k] || sel) {
        o.classList.add(bons[k] ? "ok" : "ko");
        tag = document.createElement("span"); tag.className = "qcm-tag";
        tag.textContent = bons[k] ? (sel ? "✔ cochée, juste" : "✔ à cocher") : "✘ cochée, fausse";
        o.appendChild(tag);
      }
    });
    var juste = q.querySelector(".sol").classList.contains("is-ok");
    q.querySelector(".q-status").textContent = juste ? "Réponse juste" : (inp(q).value ? "Réponse fausse ou incomplète" : "Pas de réponse");
  }
  new MutationObserver(function (ms) {
    ms.forEach(function (m) {
      var i = m.target;
      if (i.tagName !== "INPUT" || !i.disabled) return;
      var q = i.closest(".qcm");
      if (q && !q.classList.contains("corrigee")) { q.classList.add("corrigee"); corriger(q); }
    });
  }).observe(parts, { subtree: true, attributes: true, attributeFilter: ["disabled"] });
})();
</script>"""


# ============================================================ ASSEMBLAGE
DECOR_JS = """  var DECOR = {
    // aucun tracé à main levée : les constructions se font dans l'atelier (src/construction.py)
  };
"""
DR_NAMES_JS = """  var DR_NAMES = {
    // aucun document réponse à imprimer
  };
"""
EXO_DEFS = activites.ACTIVITES


def build():
    g = GABARIT.read_text(encoding="utf-8")

    # le commentaire d'en-tête du gabarit cite « <style> » : on part de la vraie balise
    s0 = g.index("<style>:root{")
    style = g[s0:g.index("</style>", s0) + len("</style>")]
    grading = re.search(r"<script>/\*GRADING-START\*/.*?</script>", g, re.S).group(0)
    app_start = g.index("<script>(function () {")
    app = g[app_start:g.rindex("</script>") + len("</script>")]

    # entrées du moteur réservées au sujet ; la durée conseillée dépend de l'activité ouverte
    app = sub_once(app, r"var CONSEIL_MIN = \d+;", "var CONSEIL_MIN = window.__CONSEIL_MIN__ || 0;")
    app = sub_once(app, r"  var DECOR = \{\n.*?\n  \};\n", DECOR_JS, re.S)
    app = sub_once(app, r"  var DR_NAMES = \{\n.*?\n  \};\n", DR_NAMES_JS, re.S)
    app = sub_once(app, r"Quatre pages, une par document", "Une page par document réponse")
    app = sub_once(app, r'btn\.textContent = "Diagramme validé";', 'btn.textContent = "Réponses validées";')

    templates, exos_cfg = [], {}
    for e in EXO_DEFS:
        prepare_exo(e)
    for e in EXO_DEFS:
        CUR["total"] = e["minutes"]
        parts_html = "".join(render_part(p) for p in e["P"])
        rail, tabs, secs = render_docs(e)
        k = e["key"]
        templates += [f'<template id="tpl-rail-{k}">{rail}</template>',
                      f'<template id="tpl-tabs-{k}">{tabs}</template>',
                      f'<template id="tpl-docs-{k}">{secs}</template>',
                      f'<template id="tpl-home-{k}">{render_exo_home(e)}</template>',
                      f'<template id="tpl-consignes-{k}">{e["consignes"]}</template>',
                      f'<template id="tpl-parts-{k}">{parts_html}\n</template>']
        exos_cfg[k] = e["cfg"]
    templates.append(f'<template id="tpl-modes">{MODES_HTML}</template>')
    templates.append(f'<template id="tpl-hub">{render_hub()}</template>')
    for key, fn in COURS_RENDER.items():
        templates.append(f'<template id="tpl-{key}">{fn()}</template>')

    config = f"<script>window.__EXOS__ = {json.dumps(exos_cfg, ensure_ascii=False)};</script>"
    router = (ROUTER_JS.replace("__COURS_JS__", COURS_JS).replace("__TITRE__", TITRE)
              .replace("__HOUSE__", HOUSE.replace("'", "\\'")))

    page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITRE} — cours et activités interactives</title>
<meta name="description" content="Énergétique, cours et activités interactives de deux niveaux : travail d'une force et d'un couple, énergies potentielle et cinétique, puissance, rendement, théorème de l'énergie cinétique, conservation de l'énergie ; résolution graphique avec un atelier de construction.">
{style}
{CONTENT_CSS.replace("__COURS_CSS__", COURS_CSS + construction.CG_CSS)}
</head>
<body class="no-mode">

<nav class="rail" aria-label="Documents de l'activité"></nav>

<aside id="docpanel" aria-label="Documents de l'activité" aria-hidden="true">
  <div class="dp-head">
    <h3 id="dp-title">Documents</h3>
    <button type="button" id="dp-out" aria-label="Réduire">−</button><span id="dp-zoom" class="small">100 %</span>
    <button type="button" id="dp-in" aria-label="Agrandir">+</button>
    <button type="button" id="dp-fit">Ajuster</button>
    <button type="button" id="dp-close">Fermer</button>
  </div>
  <div class="dp-tabs" role="tablist" aria-label="Choisir un document"></div>
  <div class="dp-body"></div>
</aside>

<section id="home" aria-labelledby="home-title"><div class="home-inner"></div></section>

<main class="page">
  <section class="print-only print-summary">
    <p>Élève : <span class="print-nom"></span> | Copie imprimée le <span class="print-date"></span></p>
    <p>Mode : <span class="print-mode"></span> | Temps de rédaction : <strong class="print-time"></strong> (durée conseillée : <span class="print-conseil"></span>)</p>
    <p class="print-note-line">Note finale pondérée : <strong class="final-note"></strong></p>
    <p class="print-nograde">Copie non corrigée : les corrections et la note n'apparaissent qu'après la remise de la copie en mode examen.</p>
  </section>

  <nav class="c-top" aria-label="Navigation"><a href="?">{HOUSE} Accueil</a></nav>

  <header class="cartouche">
    <div class="title">
      <h1>{TITRE}</h1>
      <p></p></div>
    <div class="nom"><label for="nom-eleve">Nom et prénom</label><input id="nom-eleve" type="text" autocomplete="name"></div>
  </header>

  <div class="consignes"></div>

  <div id="parts"></div>

  <section class="recap" id="recap" aria-labelledby="t-recap">
    <header class="recap-head"><h2 id="t-recap">Récapitulatif et note finale</h2>
      <p class="small">Les questions non validées comptent comme fausses. Chaque partie est ramenée sur 20, puis pondérée par sa durée conseillée.</p></header>
    <div id="exam-submit-wrap">
      <p class="es-lead">Ta copie n'est pas encore corrigée : aucune réponse n'est verrouillée, tu peux encore revenir sur les questions et les constructions.</p>
      <button type="button" class="btn btn-exam" id="exam-submit">J'ai fini, je fais corriger ma copie</button>
      <p class="es-warn" id="exam-warn" role="alert"></p>
    </div>
    <div id="recap-graded">
      <div class="recap-wrap">
        <table class="t recap-table">
          <thead><tr><th>Partie</th><th>Durée</th><th>Poids</th><th>Points</th><th>Note /20</th><th>Contribution</th></tr></thead>
          <tbody id="recap-body"></tbody>
          <tfoot><tr><th colspan="4">Note globale pondérée</th><th class="final-note"></th><th></th></tr></tfoot>
        </table>
      </div>
      <p class="final-detail small"></p>
    </div>
    <div class="recap-foot" id="recap-foot"><button type="button" class="btn btn-print">Imprimer ma copie</button>
      <span class="small no-print">L'impression reprend tes réponses, tes constructions, les corrections et ce récapitulatif.</span>
      <a class="btn ghost no-print" href="?">{HOUSE} Retour à l'accueil</a></div>
  </section>
</main>

<footer class="banner" aria-label="Suivi de la composition">
  <div class="score-block"><div class="lab">Note provisoire</div><div class="score" id="score-val">–<small>/20</small></div></div>
  <div class="exam-block"><div class="lab">Mode examen</div><div class="exam-state">Note masquée</div></div>
  <div class="timer-block"><div class="lab">Temps</div><div class="timer" id="timer-val">0:00:00</div></div>
  <div class="count" id="score-count" aria-live="polite"></div>
  <div class="spacer"></div>
  <button type="button" class="btn-docs" id="btn-docs">Documents</button>
</footer>

{chr(10).join(templates)}

{config}
{router}
{grading}
{app}
{QCM_JS}
{construction.CG_JS}
</body>
</html>
"""
    SORTIE.write_text(page, encoding="utf-8")
    print(f"{SORTIE.name} : {len(page.encode('utf-8')) / 1024:.0f} Kio")
    for e in EXO_DEFS:
        print(f"  ?ex={e['key']} : {e['tag']} — {len(e['P'])} partie(s), {e['n_q']} questions, {e['points']} points, "
              f"{hm(e['minutes'])}")
    for key in COURS_RENDER:
        print(f"  ?ex={key}")


if __name__ == "__main__":
    build()
