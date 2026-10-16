// Tests navigateur (Playwright + Chromium) : accueil, cours, formulaire, activités en entraînement et en examen, QCM.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { chromium } = require("playwright");
const { REP } = require("./reponses.js");

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

test("accueil : le cours, le formulaire, les activités, les études de cas ; cartes illustrées à mots-clés", async () => {
  const { context, page, errors } = await open("");
  assert.ok(await page.locator("body.hub").count());
  assert.ok(!(await page.isVisible("main.page")));
  assert.match(await text(page, "#home h1"), /Énergétique/);
  assert.deepEqual(await page.locator("#home h2").allInnerTexts(), ["Le cours", "Le formulaire", "Les activités", "Études de cas"]);
  const card = (sel) => page.locator(sel).evaluateAll((cs) => cs.map((c) => [
    c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent,
    c.querySelector("a") ? c.querySelector("a").getAttribute("href") : null]));
  assert.deepEqual(await card(".cours-grid .mode-card"), [["Cours", "Énergétique : travail, énergies, puissance", "?ex=cours-energetique"]]);
  assert.deepEqual(await card(".form-grid .mode-card"), [["Formulaire", "Formulaire d'énergétique", "?ex=formulaire-energetique"]]);
  const act = await card(".exo-grid .mode-card");
  assert.deepEqual(act.map((c) => c[0]), ["1.1", "1.2", "1.3", "1.4", "1.5"].map((n) => "Activité " + n + " Niveau 1")
    .concat(["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"].map((n) => "Activité " + n + " Niveau 2")));
  assert.equal(act[5][2], "?ex=tire-bouchon");
  assert.equal(await page.locator("#home").getByText(/graphique|atelier/i).count(), 0, "plus de résolution graphique");
  assert.deepEqual(await card(".etude-grid .mode-card"), [["Étude 1", "Étude de cas", null]]);
  // chaque carte : une vignette, 3 à 5 mots-clés, pas de paragraphe ; toutes de la même taille
  const cartes = await page.locator("#home .carte-v").evaluateAll((cs) => cs.map((c) => ({
    img: c.querySelector("img.cv-img") ? c.querySelector("img.cv-img").naturalWidth : -1,
    mots: c.querySelectorAll(".cv-mots li").length, p: c.querySelectorAll("p:not(.etat)").length,
    w: Math.round(c.offsetWidth), h: c.offsetHeight })));
  assert.equal(cartes.length, 1 + 1 + 14 + 1);
  // le cours et les activités : les figures du manuel (JPEG) ; formulaire et étude à venir : un dessin (SVG)
  const types = await page.locator("#home .carte-v img.cv-img").evaluateAll((is) => is.map((i) => i.src.slice(5, 15)));
  assert.equal(types.filter((t) => t === "image/jpeg").length, 15);
  assert.equal(types.filter((t) => t === "image/svg+").length, 2);
  assert.ok(await page.locator(".home-hero img").evaluate((i) => i.src.startsWith("data:image/jpeg") && i.naturalWidth > 0));
  // icône de l'onglet : l'engrenage, en SVG intégré
  assert.match(await page.locator('head link[rel="icon"]').getAttribute("href"), /^data:image\/svg\+xml;base64,/);
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

test("cours : dix sections, simulateurs, signe du travail, aire du ressort, travail virtuel, tremplin, jeu, quiz", async () => {
  const { context, page, errors } = await open("?ex=cours-energetique");
  assert.match(await text(page, "#home .home-head"), /Cours[\s\S]*Énergétique : travail, énergies, puissance/);
  assert.equal(await page.locator(".cours-sec").count(), 10);
  assert.equal(await page.locator(".cours-sec .part-body > p").first().evaluate((e) => getComputedStyle(e).maxWidth), "none");
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
  // travail du ressort : l'aire du trapèze, de 10 à 30 mm sous 10 N/mm
  assert.equal(await text(page, "#ca-aire-xw"), "4,00 J");
  assert.equal(await text(page, "#ca-aire-xc"), "16,0 carreaux");
  // travail virtuel : bras de 600 et 200 mm, effort triplé
  assert.equal(await text(page, "#ca-lev-fs"), "300 N");
  assert.match(await text(page, "#ca-lev-w"), /^0,60 J = 0,60 J$/);
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

test("formulaire : formules et unités, en pleine page", async () => {
  const { context, page, errors } = await open("?ex=formulaire-energetique");
  assert.equal(await page.locator(".cours-sec").count(), 1);
  assert.match(await text(page, "#f-formules"), /Théorème de Huygens/);
  assert.match(await text(page, "#f-formules"), /Travail virtuel/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité 1.3 en entraînement : réponses justes, 20/20 ; unité manquante, demi-point", async () => {
  const { context, page, errors } = await open("?ex=ascenseur-escalier");
  await page.click("[data-mode=training]");
  assert.equal(await page.locator(".part").count(), 2);
  // le texte occupe toute la largeur blanche de la section
  for (const sel of [".q-stem", ".q-hint", ".data", ".consignes p"])
    assert.equal(await page.locator(sel).first().evaluate((e) => getComputedStyle(e).maxWidth), "none", sel);
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

test("activité 2.7 en examen : rien avant la remise, remise en deux temps, note", async () => {
  const { context, page, errors } = await open("?ex=frein-sabot");
  await page.click("[data-mode=exam]");
  const ids = casesSaisies("l");
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

test("QCM (activités 1.1 et 1.2) : propositions à cocher, correction marquée, 20/20", async () => {
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

test("activités 1.5 et 2.1 en entraînement (skip, tire-bouchon) : réponses justes, 20/20", async () => {
  for (const [act, pre, n] of [["skip-chargement", "e", 5], ["tire-bouchon", "f", 4]]) {
    const { context, page, errors } = await open("?ex=" + act);
    await page.click("[data-mode=training]");
    const ids = casesSaisies(pre);
    assert.equal(ids.length, n);
    for (const id of ids) await repondre(page, id, REP[id]);
    assert.equal(await page.locator(".q.is-ok").count(), n);
    assert.equal(await note(page), "20,0/20");
    assert.deepEqual(errors, []);
    await context.close();
  }
});

test("activités 2.6 et 2.9 en examen (balancier, roues dentées) : rien avant la remise, puis 20/20", async () => {
  for (const [act, pre] of [["balancier", "k"], ["roues-dentees", "n"]]) {
    const { context, page, errors } = await open("?ex=" + act);
    await page.click("[data-mode=exam]");
    for (const id of casesSaisies(pre)) await page.fill(`#in-${id}`, REP[id]);
    assert.equal(await page.locator(".q.is-ok").count(), 0);
    assert.equal(await page.locator(".q-expl:not([hidden])").count(), 0);
    await page.click("#exam-submit"); await page.click("#exam-submit");
    assert.equal(await page.locator(".q.is-ok").count(), casesSaisies(pre).length);
    assert.equal(await text(page, ".final-note"), "20,0/20");
    assert.deepEqual(errors, []);
    await context.close();
  }
});

test("téléphone : la page d'une activité ne déborde pas", async () => {
  const { context, page, errors } = await open("?ex=balancier", { width: 390, height: 844 });
  await page.click("[data-mode=training]");
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  assert.deepEqual(errors, []);
  await context.close();
});
