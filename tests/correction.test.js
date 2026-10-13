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
const { REP, PLANCHES } = require("./reponses.js");

const score = (g, ans) => { const r = G.grade(ans, g); return r.invalid ? "invalid" : r.score; };
const toutes = Object.entries(EXOS).flatMap(([k, e]) => Object.entries(e.qcfg).map(([id, c]) => ({ act: k, id, ...c })));
const fr = (x) => String(+x.toPrecision(5)).replace(".", ",");

test("configuration : 14 activités, 10 analytiques (A1 à A10) et 4 graphiques (G1 à G4)", () => {
  const titres = Object.values(EXOS).map((e) => e.title);
  assert.equal(titres.length, 14);
  for (const e of Object.values(EXOS)) {
    assert.ok(e.parts.length >= 1 && e.parts.length <= 2, e.title + " : une partie par exercice, deux au plus");
    assert.equal(e.minutes, e.parts.reduce((s, p) => s + p.minutes, 0));
    for (const p of e.parts) assert.equal(p.points, Object.values(e.qcfg).filter((c) => c.part === p.num).length);
  }
  assert.equal(toutes.length, 100);  // 84 cases saisies ou cochées, 16 relevées sur les planches
});

test("chaque case a sa réponse de référence (ou sa construction), qui obtient le point", () => {
  const surPlanche = new Set(Object.values(PLANCHES).map((p) => p.q));
  for (const c of toutes) {
    const grp = c.id.replace(/_\d+$/, "");
    if (surPlanche.has(grp)) continue;  // cases relevées sur une planche : testées plus bas et dans le navigateur
    assert.ok(REP[c.id] !== undefined, "pas de référence pour " + c.id);
    assert.equal(score(c.grader, REP[c.id]), 1, `${c.act} ${c.label} : « ${REP[c.id]} »`);
  }
});

test("valeurs numériques : hors tolérance refusées, unité manquante ou fausse à moitié, multiples acceptés", () => {
  let n = 0;
  for (const c of toutes.filter((x) => x.grader.type === "num" && REP[x.id] !== undefined)) {
    const g = c.grader, v = g.value;
    if (v !== 0) assert.equal(score(g, fr(v * 1.08) + (g.unit ? " " + g.unit.label : "")), 0, c.label + " : +8 % accepté");
    if (g.unit) {
      assert.equal(score(g, fr(v)), 0.5, c.label + " : sans unité");
      assert.equal(score(g, fr(v) + " furlong"), 0.5, c.label + " : unité fausse");
      for (const vr of g.variants || []) if (vr.unit) assert.equal(score(g, fr(vr.value) + " " + vr.unit.label), 1, c.label + " en " + vr.unit.label);
    }
    n++;
  }
  assert.ok(n >= 75, "cases numériques testées : " + n);
  // quelques saisies d'élève typiques
  const q = (act, id) => EXOS[act].qcfg[id].grader;
  assert.equal(score(q("ascenseur-escalier", "c1_3"), "10486 W"), 1);
  assert.equal(score(q("ascenseur-escalier", "c1_3"), "10,5 kW"), 1);
  assert.equal(score(q("ascenseur-escalier", "c2_3"), "81,8 %"), 1);
  assert.equal(score(q("ascenseur-escalier", "c2_3"), "0,82"), 1);
  assert.equal(score(q("frein-sabot", "i1_8"), "F = 443 N"), 1);
  assert.equal(score(q("frein-sabot", "i1_5"), "111,7 N.m"), 1);
  assert.equal(score(q("frein-sabot", "i1_1"), "160 kg.m^2"), 1);
  assert.equal(score(q("verin-levage", "h1_6"), "23,5 MPa"), 1);
  assert.equal(score(q("verin-levage", "h1_6"), "235 bars"), 1);
  assert.equal(score(q("wagon-pente", "f1_2"), "2,8 m.s-1"), 1);
  assert.equal(score(q("wagon-pente", "f1_4"), "0,0153 m"), 1);
  assert.equal(score(q("wagon-pente", "f1_4"), "0,178 m"), 0, "réponse du manuel, incompatible avec K = 10 000 kN/m");
  assert.equal(score(q("amortisseur", "e1_3"), "651,1 J"), 0, "le travail du ressort est résistant : signe exigé");
  assert.equal(score(q("roues-dentees", "l2_4"), "16,3 tours"), 1);
  assert.equal(score(q("tire-bouchon", "n2_2"), "360 N"), 1);
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

test("planches : la valeur attendue de chaque relevé est juste, une construction fausse ne l'est pas", () => {
  for (const [pid, pl] of Object.entries(PLANCHES)) {
    const cases = toutes.filter((c) => c.id.startsWith(pl.q + "_"));
    assert.ok(cases.length >= 1, pid);
    for (const c of cases) {
      const g = c.grader;
      assert.equal(score(g, String(g.value)), 1, c.label);
      const tol = Math.max(g.absTol || 0, (g.relTol || 0) * Math.abs(g.value));
      assert.equal(score(g, String(g.value + 1.5 * tol + 0.01)), 0, c.label + " : hors tolérance");
    }
  }
  // le tire-bouchon : la poignée va trois fois plus vite que la vis
  const tb = EXOS["tire-bouchon"].qcfg;
  assert.equal(tb.n1_1_6.grader.value, 45);
  assert.equal(tb.n2_1.grader.value, 3);
});

test("valeurs du manuel retrouvées quand l'énoncé est cohérent", () => {
  const v = (act, id) => EXOS[act].qcfg[id].grader.value;
  const proche = (a, b, rel) => assert.ok(Math.abs(a - b) <= rel * Math.abs(b), a + " ≠ " + b);
  proche(v("ascenseur-escalier", "c1_3"), 10.48, 0.002);   // 10,48 kW
  proche(v("ascenseur-escalier", "c1_5"), 218.46, 0.001);  // 218,46 kJ
  proche(v("remonte-pente-bateau", "d2_4"), 210, 0.005);   // 210 kN
  proche(v("wagon-pente", "f1_2"), 2.8, 0.005);            // 2,8 m/s
  proche(v("freinage-pente", "g1_4"), 205, 0.002);         // 205 m
  proche(v("freinage-pente", "g1_5"), 512.6, 0.001);       // 512,6 kJ
  proche(v("verin-levage", "h1_3"), 6880, 0.001);          // 6 880 N
  proche(v("verin-levage", "h1_6"), 235, 0.002);           // 235 bars
  proche(v("frein-sabot", "i1_8"), 443, 0.001);            // 443 N
  proche(v("roues-dentees", "l2_4"), 16.3, 0.002);         // 16,3 tours
  proche(v("roues-dentees", "l2_5"), 50, 0.001);           // 50 N
  proche(v("skip-chargement", "k2_1"), 42.3, 0.001);       // 42,3 kJ
  proche(v("skip-chargement", "k2_3"), 1.2, 0.01);         // 1,2 kW
});
