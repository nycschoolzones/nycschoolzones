// NYC School Zones · download the PSAL's school data: each school's teams, and its campus list (the schools whose
// students play on one shared set of teams)
//
// The PSAL's school data only loads in a browser, so this runs in yours:
//   1. Open https://www.psal.org/profiles/profile.aspx and wait for the school list to load.
//   2. Open the browser console (Chrome/Edge: Cmd+Option+J or Ctrl+Shift+J; Firefox: Cmd+Option+K or Ctrl+Shift+K;
//      Safari: turn on Develop menu in Settings > Advanced, then Cmd+Option+C).
//   3. Paste this whole file and press Enter. For every PSAL school it asks for what its profile page shows: the
//      school's details, its teams in the two latest seasons, and its campus list (the "Campus Schools List" button).
//      It logs progress and takes about five minutes.
//   4. It saves psal_campuses.json to your Downloads folder.
//   5. Then: python3 scripts/fetch_data.py psal ~/Downloads/psal_campuses.json
//
// Left out: coaches, phone numbers and email addresses.
(async () => {
  const API = "/SportDisplay.svc";
  const get = (url) => fetch(API + url, { headers: { Accept: "application/json" } }).then((r) => {
    if (!r.ok) throw new Error(r.status + " " + url);
    return r.json();
  }).then((j) => j.d || []);
  const PRIVATE = /mail|phone|fax|coach|contact|ext$|expr4|expr9|^__/i;  // Expr4, Expr9: head and assistant coaches
  const keep = (row) => Object.fromEntries(Object.entries(row || {}).filter(([k]) => !PRIVATE.test(k)));
  const q = (s) => encodeURIComponent(s);

  const schools = await get("/vw_Schools?$orderby=newname asc");
  console.log(`${schools.length} PSAL schools`);
  const campuses = [], out = [];
  let done = 0;
  async function one(s) {
    const id = String(s.cschool).trim().padStart(5, "0");
    const rec = { psal: id, name: s.newname, row: keep(s) };
    try {
      rec.profile = (await get(`/GetSchoolProfile?schid='${id}'`)).map(keep)[0] || null;
      const seasons = [...new Set((await get(`/vw_School_Profile?$filter=${q(`cschool eq'${id}'`)}&$select=season&$orderby=season desc`))
        .map((x) => x.season))].slice(0, 2);
      rec.teams = [];
      for (const season of seasons) {
        const rows = await get(`/vw_School_Profile?$filter=${q(`cschool eq'${id}' and (season eq '${season}')`)}&$orderby=Expr8 asc`);
        rec.teams.push(...rows.map((t) => ({ season: t.season, csport: t.csport, team: t.Expr8, status: t.status,
          wins: t.nwins, losses: t.nloses })));
      }
      const members = await get(`/GetSchoolByCampus?schoolID ='${id}'`);
      if (members.length) campuses.push({ psal: id, name: s.newname, schools: members.map(keep) });
    } catch (e) {
      console.warn(s.newname, e.message);
      rec.error = e.message;
      campuses.push({ psal: id, name: s.newname, error: e.message });
    }
    out.push(rec);
    if (++done % 50 === 0) console.log(`${done} of ${schools.length}…`);
  }
  for (let i = 0; i < schools.length; i += 4) { // four schools at a time, gently
    await Promise.all(schools.slice(i, i + 4).map(one));
    await new Promise((r) => setTimeout(r, 200));
  }
  console.log(`${out.filter((r) => r.teams && r.teams.length).length} schools with teams, ` +
    `${campuses.filter((c) => c.schools).length} with a campus list, ${out.filter((r) => r.error).length} errors`);
  const blob = new Blob([JSON.stringify({ source: "PSAL school profiles and campus lists (psal.org)",
    fetched: new Date().toISOString().slice(0, 10), campuses, schools: out })], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "psal_campuses.json";
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log("Done. Next: python3 scripts/fetch_data.py psal ~/Downloads/psal_campuses.json");
})();
