// NYC School Zones · download the PSAL's campus lists: the schools whose students play on one shared set of teams
//
// The PSAL's school data only loads in a browser, so this runs in yours:
//   1. Open https://www.psal.org/profiles/profile.aspx and wait for the school list to load.
//   2. Open the browser console (Chrome/Edge: Cmd+Option+J or Ctrl+Shift+J; Firefox: Cmd+Option+K or Ctrl+Shift+K;
//      Safari: turn on Develop menu in Settings > Advanced, then Cmd+Option+C).
//   3. Paste this whole file and press Enter. It asks the PSAL, one school at a time, for each school's campus list
//      (the "Campus Schools List" button on a school's profile), so it takes a few minutes.
//   4. It saves psal_campuses.json to your Downloads folder.
//   5. Then: python3 scripts/fetch_data.py psal ~/Downloads/psal_campuses.json
(async () => {
  const API = "/SportDisplay.svc";
  const get = (url) => fetch(API + url, { headers: { Accept: "application/json" } }).then((r) => {
    if (!r.ok) throw new Error(r.status + " " + url);
    return r.json();
  });
  const schools = (await get("/vw_Schools?$orderby=newname asc")).d;
  console.log(`${schools.length} PSAL schools`);
  // most shared programs are named "… Campus" (John Jay Campus), but not all (East Harlem Pride), so it asks about
  // every school and keeps the ones with a list; fetch_data.py psal merges the same list found under several names.
  // A profile asks for a 5-character id.
  console.log("asking each school for its campus list…");
  const out = [];
  let i = 0;
  for (const c of schools) {
    if (++i % 50 === 0) console.log(`${i} of ${schools.length}…`);
    const id = String(c.cschool).trim().padStart(5, "0");
    try {
      const members = (await get(`/GetSchoolByCampus?schoolID ='${id}'`)).d || [];
      if (members.length) out.push({ psal: id, name: c.newname, schools: members });
    } catch (e) {
      console.warn(c.newname, e.message);
      out.push({ psal: id, name: c.newname, error: e.message });
    }
    await new Promise((r) => setTimeout(r, 200)); // gently
  }
  console.log(`${out.filter((c) => c.schools).length} schools with a campus list`);
  const blob = new Blob([JSON.stringify({ source: "PSAL campus school lists (psal.org GetSchoolByCampus)",
    fetched: new Date().toISOString().slice(0, 10), campuses: out })], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "psal_campuses.json";
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log("Done. Next: python3 scripts/fetch_data.py psal ~/Downloads/psal_campuses.json");
})();
