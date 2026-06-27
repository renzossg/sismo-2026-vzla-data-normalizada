# -*- coding: utf-8 -*-
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT,"data","processed","sismo2026_final_dataset.json"),encoding="utf-8"))

html = """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sismo 2026 VZLA — Explorador de datos</title>
<style>
:root{--bg:#0f1420;--card:#171e2e;--mut:#8a97ad;--bd:#26314a;--tx:#e8edf6;--ac:#4f9cff}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--tx)}
.wrap{max-width:1200px;margin:0 auto;padding:20px}
h1{font-size:20px;margin:0 0 4px}.sub{color:var(--mut);font-size:13px;margin-bottom:16px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.stat{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;min-width:90px}
.stat b{font-size:22px;display:block}.stat span{color:var(--mut);font-size:12px}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
select,input{background:var(--card);color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:9px 11px;font-size:13px}
input[type=text]{flex:1;min-width:220px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--bd);vertical-align:top}
th{position:sticky;top:0;background:#1c2438;cursor:pointer;user-select:none;white-space:nowrap}
tr:hover td{background:#1b2233}
.tablewrap{max-height:62vh;overflow:auto;border:1px solid var(--bd);border-radius:10px}
.pill{font-size:11px;padding:2px 8px;border-radius:20px;white-space:nowrap}
.alta{background:#15391f;color:#7ee2a0}.media{background:#3a3413;color:#e8d27a}.baja{background:#3a1d13;color:#f0a98c}
.dead{color:#ff8585;font-weight:600}
.muted{color:var(--mut)}
a{color:var(--ac)}
.count{color:var(--mut);font-size:13px;margin:10px 2px}
</style></head><body><div class="wrap">
<h1>Sismo 2026 VZLA — Explorador de datos normalizados</h1>
<div class="sub">__N__ personas únicas · 10 centros · fuente: carpeta Drive "SISMO 2026 VZLA". Datos sensibles — uso restringido.</div>
<div class="stats" id="stats"></div>
<div class="controls">
 <select id="hosp"></select>
 <select id="conf"><option value="">Confianza: todas</option><option>alta</option><option>media</option><option>baja</option></select>
 <select id="tipo"><option value="">Tipo: todos</option><option value="paciente">paciente</option><option value="personal_contingencia">personal_contingencia</option></select>
 <select id="dead"><option value="">Todos</option><option value="si">Solo fallecidos</option></select>
 <input type="text" id="q" placeholder="Buscar nombre o cédula…">
</div>
<div class="count" id="count"></div>
<div class="tablewrap"><table><thead><tr>
<th data-k="nombre_completo">Nombre</th><th data-k="cedula">Cédula</th><th data-k="edad">Edad</th>
<th data-k="hospital">Centro</th><th data-k="procedencia">Procedencia</th><th data-k="diagnostico">Diagnóstico/Obs.</th>
<th data-k="confianza">Conf.</th><th data-k="n_fuentes">Fuentes</th></tr></thead>
<tbody id="tb"></tbody></table></div>
</div>
<script>
const DATA = __DATA__;
const $=s=>document.querySelector(s);
let sortK="hospital", sortDir=1;
const hosps=[...new Set(DATA.map(d=>d.hospital))].sort();
$("#hosp").innerHTML='<option value="">Centro: todos</option>'+hosps.map(h=>`<option>${h}</option>`).join("");
function stats(rows){
 const dead=rows.filter(r=>r.fallecido).length, ci=rows.filter(r=>r.cedula).length;
 $("#stats").innerHTML=[["Personas",rows.length],["Con cédula",ci],["Sin cédula",rows.length-ci],["Fallecidos",dead]]
  .map(s=>`<div class="stat"><b>${s[1]}</b><span>${s[0]}</span></div>`).join("");
}
function render(){
 const h=$("#hosp").value,c=$("#conf").value,t=$("#tipo").value,d=$("#dead").value,q=$("#q").value.toLowerCase().trim();
 let rows=DATA.filter(r=>(!h||r.hospital===h)&&(!c||r.confianza===c)&&(!t||r.tipo_lista===t)&&(!d||r.fallecido)
   &&(!q||(r.nombre_completo||"").toLowerCase().includes(q)||(r.cedula||"").includes(q)));
 rows.sort((a,b)=>{let x=(a[sortK]??""),y=(b[sortK]??"");if(sortK==="edad"||sortK==="n_fuentes"){x=+x||0;y=+y||0}
   return (x>y?1:x<y?-1:0)*sortDir});
 stats(rows);
 $("#count").textContent=rows.length+" registros mostrados";
 $("#tb").innerHTML=rows.map(r=>`<tr>
  <td>${r.fallecido?'<span class="dead">†</span> ':''}${r.nombre_completo||'<span class=muted>—</span>'}</td>
  <td>${r.cedula||'<span class=muted>—</span>'}</td><td>${r.edad||''}</td>
  <td>${r.hospital||''}</td><td>${r.procedencia||''}</td>
  <td>${(r.diagnostico||r.parentesco_observacion||'')}</td>
  <td><span class="pill ${r.confianza}">${r.confianza}</span></td>
  <td>${r.n_fuentes>1?('<b>'+r.n_fuentes+'</b>'):r.n_fuentes}</td></tr>`).join("");
}
document.querySelectorAll("th").forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(k===sortK)sortDir*=-1;else{sortK=k;sortDir=1}render()});
["#hosp","#conf","#tipo","#dead"].forEach(s=>$(s).onchange=render);$("#q").oninput=render;
render();
</script></body></html>"""
html = html.replace("__N__", str(len(data))).replace("__DATA__", json.dumps(data, ensure_ascii=False))
open(os.path.join(ROOT,"explorador.html"),"w",encoding="utf-8").write(html)
print("explorador.html generado:", len(data), "registros")
