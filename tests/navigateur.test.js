// Tests navigateur (Playwright + Chromium) : accueil, cours, formulaire, activités en entraînement et en examen,
// QCM, atelier de construction (tracés au clic, verrouillage, correction superposée).
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { chromium } = require("playwright");
const { REP, PLANCHES } = require("./reponses.js");

const FILE = path.join(__dirname, "..", "index.html");
const URL = "file://" + FILE;
let browser;

test.before(async () => { browser = await chromium.launch(); });
test.after(async () => { await browser.close(); });

async function open(q, viewport) {
  const context = await browser.newContext({ viewport: viewport || { width: 1366, height: 900 } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("dialog", (d) => d.accept());
  await page.goto(URL + q);
  return { context, page, errors };
}
const text = (page, sel) => page.locator(sel).first().innerText();
const note = async (page) => (await text(page, "#score-val")).replace(/\s/g, "");
// question à une case : saisir puis valider, comme l'élève
async function repondre(page, id, v) {
  await page.fill(`#in-${id}`, v);
  await page.click(`#${id} .btn-validate`);
}
async function cocher(page, gid, lettres) {
  for (const k of lettres.split(",")) await page.click(`#${gid} .qcm-o[data-k="${k}"]`);
}
const casesSaisies = (prefix) => Object.keys(REP).filter((id) => id.startsWith(prefix) && /^[a-z]\d+_\d+$/.test(id));
// planche : coordonnées en mm → pixels de l'écran
async function clic(page, pid, mm) {
  const [x, y] = await page.evaluate(([id, p]) => {
    const s = document.querySelector(`#cg-${id} svg`), m = s.getScreenCTM();
    return [m.a * p[0] + m.e, m.d * p[1] + m.f];
  }, [pid, mm]);
  await page.mouse.click(x, y);
}
const outil = (page, pid, o) => page.click(`#cg-${pid} [data-outil=${o}]`);
const objets = (page, pid) => page.evaluate((id) => window.__CG__[id].etat(), pid);

test("accueil : cours, formulaire, deux rubriques d'activités, études de cas ; cartes illustrées à mots-clés", async () => {
  const { context, page, errors } = await open("");
  assert.ok(await page.locator("body.hub").count());
  assert.ok(!(await page.isVisible("main.page")));
  assert.match(await text(page, "#home h1"), /Énergétique/);
  assert.deepEqual(await page.locator("#home h2").allInnerTexts(),
    ["Les cours", "Le formulaire", "Activités : approche analytique", "Activités : résolution graphique", "Études de cas"]);
  const card = (sel) => page.locator(sel).evaluateAll((cs) => cs.map((c) => [
    c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent,
    c.querySelector("a") ? c.querySelector("a").getAttribute("href") : null]));
  assert.deepEqual(await card(".cours-grid .mode-card"), [
    ["Cours 1 Niveau 1", "Énergétique : approche analytique", "?ex=cours-analytique"],
    ["Cours 2 Niveau 2", "Énergétique : résolution graphique", "?ex=cours-graphique"]]);
  assert.deepEqual(await card(".form-grid .mode-card"), [["Formulaire", "Formulaire d'énergétique", "?ex=formulaire-energetique"]]);
  const ana = await card(".rub-analytique .mode-card");
  assert.deepEqual(ana.map((c) => c[0].split(" Niveau")[0]), ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"].map((n) => "Activité " + n));
  const gra = await card(".rub-graphique .mode-card");
  assert.deepEqual(gra.map((c) => c[2]), ["?ex=skip-chargement", "?ex=roues-dentees", "?ex=balancier", "?ex=tire-bouchon",
    "?ex=cours-graphique#atelier"]);
  assert.deepEqual(await card(".etude-grid .mode-card"), [["Étude 1", "Étude de cas", null]]);
  // chaque carte : une vignette dessinée, 3 à 5 mots-clés, pas de paragraphe ; toutes de la même taille
  const cartes = await page.locator("#home .carte-v").evaluateAll((cs) => cs.map((c) => ({
    img: c.querySelector("img.cv-img") ? c.querySelector("img.cv-img").naturalWidth : -1,
    mots: c.querySelectorAll(".cv-mots li").length, p: c.querySelectorAll("p:not(.etat)").length,
    w: Math.round(c.offsetWidth), h: c.offsetHeight })));
  assert.equal(cartes.length, 2 + 1 + 10 + 5 + 1);
  for (const c of cartes) {
    assert.ok(c.img > 0, "vignette chargée");
    assert.ok(c.mots >= 3 && c.mots <= 5, JSON.stringify(c));
    assert.equal(c.p, 0);
    assert.equal(c.w, cartes[0].w);
    assert.ok(Math.abs(c.h - cartes[0].h) <= 1, "même hauteur");
  }
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const src = fs.readFileSync(FILE, "utf8").replace(/data:[^"]+/g, "");
  assert.doesNotMatch(src, /\b(BTS|STI2D|bac(calaur[ée]at)?|session \d|[ée]preuve|acad[ée]mie|sujet z[ée]ro|brevet)\b/i);
  assert.deepEqual(errors, []);
  await context.close();
});

test("adresse inconnue : retour à l'accueil", async () => {
  const { context, page, errors } = await open("?ex=inconnu");
  assert.ok(await page.locator(".cours-grid").count());
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1 : dix sections, simulateurs, signe du travail, tremplin, cartes, jeu et quiz", async () => {
  const { context, page, errors } = await open("?ex=cours-analytique");
  assert.match(await text(page, "#home .home-head"), /Cours 1[\s\S]*Niveau 1[\s\S]*approche analytique/);
  assert.equal(await page.locator(".cours-sec").count(), 10);
  const range = (sel, v) => page.locator(sel).evaluate((e, x) => { e.value = x; e.dispatchEvent(new Event("input")); }, v);
  // même énergie, plus vite : plus de puissance
  assert.equal(await text(page, "#ca-palan-w"), "20,0 kJ");
  assert.equal(await text(page, "#ca-palan-p"), "1,00 kW");
  await range("#ca-palan-v", "0.5");
  assert.equal(await text(page, "#ca-palan-w"), "20,0 kJ");
  assert.equal(await text(page, "#ca-palan-p"), "5,00 kW");
  // signe du travail selon l'angle
  await range("#ca-theta-r", "90");
  assert.match(await text(page, "#ca-theta-v"), /travail nul/);
  await range("#ca-theta-r", "150");
  assert.match(await text(page, "#ca-theta-v"), /résistant/);
  // exemples du cours : moteur, camion, volant
  assert.equal(await text(page, "#ca-mot-p"), "3,14 kW");
  assert.equal(await text(page, "#ca-ecv-ec"), "6,30 MJ");
  assert.equal(await text(page, "#ca-vol-ec"), "33,6 MJ");
  // tremplin : en bas de la piste, toute l'énergie est cinétique
  await range("#ca-tremplin-s", "100");
  assert.match(await text(page, "#ca-tremplin-v"), /^28,0 m\/s/);
  await page.click(".carte >> nth=0");
  assert.equal(await page.locator(".carte >> nth=0").getAttribute("aria-expanded"), "true");
  await page.click("#ca-jeu .jeu-l >> nth=0 >> button[data-v=el]");
  assert.equal(await text(page, "#ca-jeu .jeu-s"), "1 / 8");
  const fs_ = page.locator("#ca-quiz .quiz-q");
  for (let i = 0; i < await fs_.count(); i++) {
    const ok = await fs_.nth(i).getAttribute("data-ok");
    await fs_.nth(i).locator(`input[value="${ok}"]`).check();
  }
  assert.equal(await text(page, "#ca-quiz #qz-score"), "10 / 10");
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 2 : démonstrations (aire, projection, rotation, bielle-manivelle, CIR, levier) et planche libre", async () => {
  const { context, page, errors } = await open("?ex=cours-graphique");
  assert.equal(await page.locator(".cours-sec").count(), 9);
  const range = (sel, v) => page.locator(sel).evaluate((e, x) => { e.value = x; e.dispatchEvent(new Event("input")); }, v);
  assert.equal(await text(page, "#cg-ai-xw"), "4,00 J");       // 10 N/mm, de 10 à 30 mm
  await range("#cg-pj-t", "90");
  assert.equal(await text(page, "#cg-pj-xs"), "nulle");
  assert.equal(await text(page, "#cg-rot-xvm"), "0,84 m/s");    // 1,2 m/s × 70/100
  assert.equal(await page.locator("#cg-bm-ci").evaluate((e) => e.style.display), "none");
  await page.check("#cg-bm-c");
  assert.equal(await page.locator("#cg-bm-ci").evaluate((e) => e.style.display), "");
  await range("#cg-disc-a", "90");
  assert.equal(await text(page, "#cg-disc-xvm"), "2,00");      // point haut : deux fois la vitesse du centre
  assert.equal(await text(page, "#cg-lev-fs"), "300 N");
  // planche libre : on trace, on efface, on montre la correction ; rien n'est noté
  await page.locator("#cg-libre").scrollIntoViewIfNeeded();
  await outil(page, "libre", "point");
  await clic(page, "libre", [120, 40]);
  assert.equal((await objets(page, "libre")).length, 1);
  await page.click("#cg-libre [data-act=annuler]");
  assert.equal((await objets(page, "libre")).length, 0);
  await page.click("#cg-libre [data-act=retablir]");
  assert.equal((await objets(page, "libre")).length, 1);
  assert.equal(await page.locator("#cg-libre .cg-corr.on").count(), 0);
  await page.click("#cg-libre .cg-voir");
  assert.equal(await page.locator("#cg-libre .cg-corr.on").count(), 1);
  assert.equal(await page.locator("#cg-libre .cg-corr").evaluate((g) => getComputedStyle(g).display), "inline");
  assert.deepEqual(errors, []);
  await context.close();
});

test("formulaire : formules et méthodes graphiques, en pleine page", async () => {
  const { context, page, errors } = await open("?ex=formulaire-energetique");
  assert.equal(await page.locator(".cours-sec").count(), 2);
  assert.match(await text(page, "#f-formules"), /Ec = ½·m·V²|½·<i>m<\/i>|E\s*c/);
  assert.match(await text(page, "#f-methodes"), /Équiprojectivité/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité A3 en entraînement : réponses justes, 20/20 ; unité manquante, demi-point", async () => {
  const { context, page, errors } = await open("?ex=ascenseur-escalier");
  await page.click("[data-mode=training]");
  assert.equal(await page.locator(".part").count(), 2);
  const ids = casesSaisies("c");
  assert.equal(ids.length, 8);
  for (const id of ids) await repondre(page, id, REP[id]);
  assert.equal(await page.locator(".q.is-ok").count(), 8);
  assert.equal(await note(page), "20,0/20");
  await context.close();
  // une unité oubliée ne rapporte que la moitié du point
  const o = await open("?ex=ascenseur-escalier");
  await o.page.click("[data-mode=training]");
  await repondre(o.page, "c1_1", "8338,5");
  assert.match(await text(o.page, "#c1_1 .q-status"), /unité manquante/);
  assert.equal(await o.page.locator("#c1_1.is-half").count(), 1);
  assert.deepEqual(errors.concat(o.errors), []);
  await o.context.close();
});

test("activité A9 en examen : rien avant la remise, remise en deux temps, note", async () => {
  const { context, page, errors } = await open("?ex=frein-sabot");
  await page.click("[data-mode=exam]");
  const ids = casesSaisies("i");
  for (const id of ids.slice(0, 6)) await page.fill(`#in-${id}`, REP[id]);
  await page.fill(`#in-${ids[6]}`, "1 N");
  assert.equal(await page.locator(".q-expl:not([hidden])").count(), 0);
  await page.click("#exam-submit");
  assert.match(await text(page, "#exam-warn"), /1 réponse\(s\) encore vide/);
  await page.click("#exam-submit");
  assert.equal(await page.locator(".q.is-ok").count(), 6);
  assert.equal(await page.locator(".q-expl:not([hidden])").count(), 8);
  assert.equal(await text(page, ".final-note"), "15,0/20");
  assert.deepEqual(errors, []);
  await context.close();
});

test("QCM (A1 et A2) : propositions à cocher, correction marquée, 20/20", async () => {
  for (const [act, pre] of [["qcm-travail-energie", "a"], ["qcm-puissance", "b"]]) {
    const { context, page, errors } = await open("?ex=" + act);
    await page.click("[data-mode=training]");
    for (const id of Object.keys(REP).filter((k) => k.startsWith(pre))) {
      const gid = id.replace(/_1$/, "");
      await cocher(page, gid, REP[id]);
      await page.click(`#${gid} .btn-fast`);
      assert.equal(await page.locator(`#${gid} .qcm-o.ok`).count(), REP[id].split(",").length);
      assert.equal(await page.locator(`#${gid} .qcm-o.ko`).count(), 0);
    }
    assert.equal(await note(page), "20,0/20");
    assert.deepEqual(errors, []);
    await context.close();
  }
  // une réponse incomplète est fausse : la proposition oubliée est montrée
  const { context, page } = await open("?ex=qcm-puissance");
  await page.click("[data-mode=training]");
  await cocher(page, "b1_1", "b");
  await page.click("#b1_1 .btn-fast");
  assert.match(await text(page, "#b1_1 .q-status"), /fausse ou incomplète/);
  assert.match(await text(page, '#b1_1 .qcm-o[data-k="c"]'), /à cocher/);
  await context.close();
});

test("activité G1 : construction au clic (perpendiculaire, projeté, vecteur, nom), relevé, 20/20", async () => {
  const { context, page, errors } = await open("?ex=skip-chargement");
  await page.click("[data-mode=training]");
  const cfg = await page.evaluate(() => JSON.parse(document.querySelector("#cg-skip").getAttribute("data-cfg")));
  const P = cfg.points, V = cfg.vecteurs[0].b, pid = "skip";
  await page.locator("#cg-skip .cg-stage").scrollIntoViewIfNeeded();
  // relevé vide au départ : les cases masquées sont vides
  assert.deepEqual(await page.locator("#k1_1 .sol input").evaluateAll((is) => is.map((i) => i.value)), ["", "", ""]);
  await outil(page, pid, "perpendiculaire"); await clic(page, pid, [150, 165]); await clic(page, pid, P.G);
  await outil(page, pid, "projete"); await clic(page, pid, V); await clic(page, pid, [P.G[0], 60]);
  const proj = (await objets(page, pid)).filter((o) => o.t === "pt")[0].p;
  await outil(page, pid, "vecteur"); await clic(page, pid, P.G); await clic(page, pid, proj);
  await outil(page, pid, "perpendiculaire"); await clic(page, pid, [150, 165]); await clic(page, pid, P.O);
  await outil(page, pid, "projete"); await clic(page, pid, P.T); await clic(page, pid, [P.O[0], 80]);
  const h = (await objets(page, pid)).filter((o) => o.t === "pt").pop().p;
  await outil(page, pid, "nommer"); await clic(page, pid, h);
  await page.locator("#cg-skip .cg-nom").fill("H"); await page.keyboard.press("Enter");
  assert.deepEqual(await page.locator("#k1_1 .cg-val").allInnerTexts(),
    ["0,282 m/s", "90° (sens trigonométrique, depuis l'horizontale vers la droite)", "point H placé"]);
  // l'outil Mesurer lit la dénivellation OH à l'échelle des longueurs
  await outil(page, pid, "mesurer"); await clic(page, pid, P.O); await clic(page, pid, h);
  assert.match(await text(page, "#cg-skip .cg-info"), /14,1 m \(longueurs\)/);
  await page.click("#k1_1 .btn-fast");
  assert.equal(await page.locator("#k1_1 .sol.is-ok").count(), 3);
  assert.equal(await page.locator("#cg-skip.locked").count(), 1);
  assert.equal(await page.locator("#cg-skip .cg-corr.on").count(), 1);
  // planche verrouillée : un clic ne trace plus rien
  const n = (await objets(page, pid)).length;
  await clic(page, pid, [100, 100]);
  assert.equal((await objets(page, pid)).length, n);
  for (const id of casesSaisies("k")) await repondre(page, id, REP[id]);
  assert.equal(await note(page), "20,0/20");
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité G4 : CIR et vitesses du pantographe, T = 3·F, 20/20", async () => {
  const { context, page, errors } = await open("?ex=tire-bouchon");
  await page.click("[data-mode=training]");
  const pl = PLANCHES.tirebouchon;
  await page.evaluate((o) => window.__CG__.tirebouchon.charger(o), pl.objets);
  assert.deepEqual(await page.locator(`#${pl.q} .sol input`).evaluateAll((is) => is.map((i) => +(+i.value).toFixed(1))),
    [0, 23.7, 0, 38.2, 0, 45, 0]);
  await page.click(`#${pl.q} .btn-fast`);
  assert.equal(await page.locator(`#${pl.q} .sol.is-ok`).count(), 7);
  for (const id of casesSaisies("n")) await repondre(page, id, REP[id]);
  assert.equal(await note(page), "20,0/20");
  assert.deepEqual(errors, []);
  await context.close();
});

test("atelier : report de longueur, gomme, noms uniques, CIR mal placé refusé", async () => {
  const { context, page, errors } = await open("?ex=tire-bouchon");
  await page.click("[data-mode=training]");
  const pid = "tirebouchon", cfg = await page.evaluate(() => JSON.parse(document.querySelector("#cg-tirebouchon").getAttribute("data-cfg")));
  const P = cfg.points;
  await page.locator("#cg-tirebouchon .cg-stage").scrollIntoViewIfNeeded();
  // report : la longueur DE, reportée en H
  await outil(page, pid, "report"); await clic(page, pid, P.D); await clic(page, pid, P.E); await clic(page, pid, P.H);
  const cer = (await objets(page, pid))[0];
  assert.equal(cer.t, "cer");
  assert.ok(Math.abs(cer.r - (P.E[0] - P.D[0])) < 1e-6 && cer.c[0] === P.H[0]);
  await outil(page, pid, "gomme"); await clic(page, pid, [P.H[0], P.H[1] - cer.r]);
  assert.equal((await objets(page, pid)).length, 0);
  // un point nommé I1 loin de sa place : relevé fait, mais faux
  await outil(page, pid, "point"); await clic(page, pid, [60, 30]);
  await outil(page, pid, "nommer"); await clic(page, pid, [60, 30]);
  await page.locator("#cg-tirebouchon .cg-nom").fill("I1"); await page.keyboard.press("Enter");
  await outil(page, pid, "point"); await clic(page, pid, [150, 30]);
  await outil(page, pid, "nommer"); await clic(page, pid, [150, 30]);
  await page.locator("#cg-tirebouchon .cg-nom").fill("i₁"); await page.keyboard.press("Enter");
  assert.match(await text(page, "#cg-tirebouchon .cg-info"), /déjà pris/);
  await page.click("#n1_1 .btn-fast");          // cases vides : confirmation demandée
  await page.click("#n1_1 .btn-fast");
  assert.equal(await page.locator("#n1_1 .sol.is-ok").count(), 0);
  // zoom et plein écran (Échap en sort)
  await page.click("#cg-tirebouchon [data-zoom=in]");
  assert.equal(await text(page, "#cg-tirebouchon .zoom-val"), "150 %");
  await page.click("#cg-tirebouchon [data-act=plein]");
  assert.equal(await page.locator("#cg-tirebouchon.is-full").count(), 1);
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("#cg-tirebouchon.is-full").count(), 0);
  assert.deepEqual(errors, []);
  await context.close();
});

test("activités G2 et G3 en examen : constructions et calculs, rien avant la remise, puis 20/20", async () => {
  for (const [act, pid, pre] of [["roues-dentees", "roues", "l"], ["balancier", "balancier", "m"]]) {
    const { context, page, errors } = await open("?ex=" + act);
    await page.click("[data-mode=exam]");
    const pl = PLANCHES[pid];
    await page.evaluate(([id, o]) => window.__CG__[id].charger(o), [pid, pl.objets]);
    for (const id of casesSaisies(pre)) await page.fill(`#in-${id}`, REP[id]);
    assert.equal(await page.locator(`#cg-${pid} .cg-corr.on`).count(), 0);
    assert.equal(await page.locator(".sol.is-ok, .q.is-ok").count(), 0);
    await page.click("#exam-submit"); await page.click("#exam-submit");
    assert.equal(await page.locator(`#cg-${pid}.locked`).count(), 1);
    assert.equal(await page.locator(`#cg-${pid} .cg-corr.on`).count(), 1);
    assert.equal(await text(page, ".final-note"), "20,0/20");
    assert.deepEqual(errors, []);
    await context.close();
  }
});

test("téléphone : la page d'une activité graphique ne déborde pas, la planche reste utilisable", async () => {
  const { context, page, errors } = await open("?ex=balancier", { width: 390, height: 844 });
  await page.click("[data-mode=training]");
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  const box = await page.locator("#cg-balancier svg").boundingBox();
  assert.ok(box.width > 260 && box.width <= 390, JSON.stringify(box));  // entre le rail des documents et la marge ; le zoom agrandit
  assert.deepEqual(errors, []);
  await context.close();
});
