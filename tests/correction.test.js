// Tests unitaires du moteur de correction appliqué aux cases des activités.
//   node --test tests/correction.test.js
// Le moteur (Grading) et la configuration (__EXOS__) sont lus dans la page générée :
// on teste exactement ce que l'élève utilisera.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const PAGE = path.join(__dirname, "..", "index.html");
const html = fs.readFileSync(PAGE, "utf8");
const code = html.slice(html.indexOf("/*GRADING-START*/"), html.indexOf("/*GRADING-END*/"));
const mod = { exports: {} };
new Function("module", code + "\nmodule.exports = Grading;")(mod);
const G = mod.exports;
const EXOS = JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1]);
const { REP } = require("./reponses.js");

const score = (g, ans) => { const r = G.grade(ans, g); return r.invalid ? "invalid" : r.score; };
const toutes = Object.entries(EXOS).flatMap(([k, e]) => Object.entries(e.qcfg).map(([id, c]) => ({ act: k, id, ...c })));
const fr = (x) => String(+x.toPrecision(5)).replace(".", ",");
const q = (act, id) => EXOS[act].qcfg[id].grader;

test("configuration : 14 activités d'une ou deux parties, 84 cases", () => {
  assert.equal(Object.keys(EXOS).length, 14);
  for (const e of Object.values(EXOS)) {
    assert.ok(e.parts.length >= 1 && e.parts.length <= 2, e.title + " : une partie par exercice, deux au plus");
    assert.equal(e.minutes, e.parts.reduce((s, p) => s + p.minutes, 0));
    for (const p of e.parts) assert.equal(p.points, Object.values(e.qcfg).filter((c) => c.part === p.num).length);
  }
  assert.equal(toutes.length, 84);
});

test("chaque case a sa réponse de référence, qui obtient le point", () => {
  for (const c of toutes) {
    assert.ok(REP[c.id] !== undefined, "pas de référence pour " + c.id);
    assert.equal(score(c.grader, REP[c.id]), 1, `${c.act} ${c.label} : « ${REP[c.id]} »`);
  }
});

test("valeurs numériques : hors tolérance refusées, unité manquante ou fausse à moitié, multiples acceptés", () => {
  let n = 0;
  for (const c of toutes.filter((x) => x.grader.type === "num")) {
    const g = c.grader, v = g.value;
    if (v !== 0) assert.equal(score(g, fr(v * 1.08) + (g.unit ? " " + g.unit.label : "")), 0, c.label + " : +8 % accepté");
    if (g.unit) {
      assert.equal(score(g, fr(v)), 0.5, c.label + " : sans unité");
      assert.equal(score(g, fr(v) + " furlong"), 0.5, c.label + " : unité fausse");
      for (const vr of g.variants || []) if (vr.unit) assert.equal(score(g, fr(vr.value) + " " + vr.unit.label), 1, c.label + " en " + vr.unit.label);
    }
    n++;
  }
  assert.equal(n, 79);
  // quelques saisies d'élève typiques
  assert.equal(score(q("ascenseur-escalier", "c1_3"), "10486 W"), 1);
  assert.equal(score(q("ascenseur-escalier", "c1_3"), "10,5 kW"), 1);
  assert.equal(score(q("ascenseur-escalier", "c2_3"), "81,8 %"), 1);
  assert.equal(score(q("ascenseur-escalier", "c2_3"), "0,82"), 1);
  assert.equal(score(q("frein-sabot", "l1_8"), "F = 443 N"), 1);
  assert.equal(score(q("frein-sabot", "l1_5"), "111,7 N.m"), 1);
  assert.equal(score(q("frein-sabot", "l1_1"), "160 kg.m^2"), 1);
  assert.equal(score(q("verin-levage", "j1_6"), "23,5 MPa"), 1);
  assert.equal(score(q("verin-levage", "j1_6"), "235 bars"), 1);
  assert.equal(score(q("wagon-pente", "h1_2"), "2,8 m.s-1"), 1);
  assert.equal(score(q("wagon-pente", "h1_4"), "0,0153 m"), 1);
  assert.equal(score(q("wagon-pente", "h1_4"), "0,178 m"), 0, "réponse du manuel, incompatible avec K = 10 000 kN/m");
  assert.equal(score(q("amortisseur", "g1_3"), "651,1 J"), 0, "le travail du ressort est résistant : signe exigé");
  assert.equal(score(q("roues-dentees", "n1_6"), "16,3 tours"), 1);
  assert.equal(score(q("tire-bouchon", "f1_1"), "3"), 1);
  assert.equal(score(q("tire-bouchon", "f1_4"), "360 N"), 1);
  assert.equal(score(q("skip-chargement", "e1_4"), "846 W"), 0, "la puissance du poids est négative");
});

test("QCM : seules les bonnes propositions, toutes, obtiennent le point", () => {
  const qcm = toutes.filter((c) => c.act.startsWith("qcm-"));
  assert.equal(qcm.length, 5);
  for (const c of qcm) {
    const bonne = REP[c.id];
    for (let m = 1; m < 8; m++) {
      const choix = ["a", "b", "c"].filter((_, i) => m & (1 << i)).join(",");
      assert.equal(score(c.grader, choix), choix === bonne ? 1 : 0, `${c.act} ${c.label} : ${choix}`);
    }
  }
  assert.deepEqual(qcm.map((c) => REP[c.id]), ["a", "b,c", "c", "b,c", "a,b,c"]);
});

test("valeurs du manuel retrouvées quand l'énoncé est cohérent", () => {
  const v = (act, id) => q(act, id).value;
  const proche = (a, b, rel) => assert.ok(Math.abs(a - b) <= rel * Math.abs(b), a + " ≠ " + b);
  proche(v("ascenseur-escalier", "c1_3"), 10.48, 0.002);   // 10,48 kW
  proche(v("ascenseur-escalier", "c1_5"), 218.46, 0.001);  // 218,46 kJ
  proche(v("remonte-pente-bateau", "d2_4"), 210, 0.005);   // 210 kN
  proche(v("skip-chargement", "e1_2"), 42.3, 0.001);       // 42,3 kJ
  proche(v("skip-chargement", "e1_5"), 1.2, 0.01);         // 1,2 kW
  proche(v("tire-bouchon", "f1_4"), 3 * 120, 1e-9);        // T = 3·F
  proche(v("wagon-pente", "h1_2"), 2.8, 0.005);            // 2,8 m/s
  proche(v("freinage-pente", "i1_4"), 205, 0.002);         // 205 m
  proche(v("freinage-pente", "i1_5"), 512.6, 0.001);       // 512,6 kJ
  proche(v("verin-levage", "j1_3"), 6880, 0.001);          // 6 880 N
  proche(v("verin-levage", "j1_6"), 235, 0.002);           // 235 bars
  proche(v("frein-sabot", "l1_8"), 443, 0.001);            // 443 N
  proche(v("roues-dentees", "n1_6"), 16.3, 0.002);         // 16,3 tours
  proche(v("roues-dentees", "n1_7"), 50, 0.001);           // 50 N
});
