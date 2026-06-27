# -*- coding: utf-8 -*-
import re, json, csv, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "processed")
os.makedirs(OUT, exist_ok=True)

LINKS = {
    "master_pdf": "https://drive.google.com/file/d/10tLqzNMBs_gl-VMiK7KaQTDbqvpSoutI/view",
    "sheet1": "https://docs.google.com/spreadsheets/d/1wzpm_7pd0fC4hFou5FzppMNeZkd6J6NvrPqy-PWNvRY",
    "arvelo_personal_pdf": "https://drive.google.com/file/d/13U9VcEa6iNnRkLANEA_Gk9mdpVcZ0WqR/view",
    "huc_pdf": "https://drive.google.com/file/d/1mA7z1Mtyb2VzvKlE2H9PBS6v8tEpdPJb/view",
    "catia_folder": "https://drive.google.com/drive/folders/10gm4GStjkb6hCgr5yMdvh77H36hA7M-w",
    "elavila_folder": "https://drive.google.com/drive/folders/1DvHmDkLOeK6NG-WlC0bphKmhDr52MY_S",
    "caribia_folder": "https://drive.google.com/drive/folders/13JEMBh0VJVUxndt-wj_bujNqd_i9rin0",
}

records = []
def norm_ci(raw):
    if not raw: return ""
    if not re.search(r"\d", raw): return ""
    return re.sub(r"\D","", raw)
def clean(s): return (s or "").strip()

def add(**k):
    base = dict(tipo_lista="", hospital="", apellidos="", nombres="", nombre_completo="",
               edad="", cedula="", cedula_raw="", sexo="", procedencia="",
               parentesco_observacion="", diagnostico="", fecha_reporte="", hora_reporte="",
               fallecido=False, confianza="", fuente_archivo="", fuente_link="", fuente_tipo="")
    base.update(k)
    if not base["nombre_completo"]:
        base["nombre_completo"] = (clean(base["apellidos"])+" "+clean(base["nombres"])).strip()
    base["nombre_completo"] = re.sub(r"\s+"," ",base["nombre_completo"]).strip()
    records.append(base)

# 1) MASTER REGISTRY (omitimos Universitario: lo reemplaza el Reporte HUC, más completo)
with open(os.path.join(RAW,"master_registry.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=line.split("|")
        if len(p)<4: continue
        n,hosp,name,edad=p[0],p[1],p[2],p[3]
        if "Universitario" in hosp: continue
        add(tipo_lista="paciente",hospital=clean(hosp),nombre_completo=clean(name),edad=clean(edad),
            confianza="media",fuente_archivo="1_5040023583598840087 (2).pdf (Registro Maestro)",
            fuente_link=LINKS["master_pdf"],fuente_tipo="PDF consolidado")

# 2) SHEET 1 (Arvelo / Vargas / JGH)
section=None
with open(os.path.join(RAW,"sheet1.md"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if line.startswith("### TABLA 1"): section="arvelo"; continue
        if line.startswith("### TABLA 2"): section="vargas"; continue
        if line.startswith("### TABLA 3"): section="jgh"; continue
        if not line.strip() or "|" not in line: continue
        p=[x.strip() for x in line.split("|")]
        if section=="arvelo":
            ap,no,ed,ci=(p+["","","",""])[:4]
            add(tipo_lista="paciente",hospital="Hospital Militar Dr. Carlos Arvelo",
                apellidos=ap,nombres=no,edad=ed,cedula=norm_ci(ci),cedula_raw=ci,confianza="alta",
                fuente_archivo="Lista digitalizada de pacientes (Sheet)",fuente_link=LINKS["sheet1"],fuente_tipo="Google Sheet")
        elif section=="vargas":
            nom,ci,ed,_,fe,ho=(p+["","","","","",""])[:6]
            add(tipo_lista="paciente",hospital="Hospital Vargas de Caracas",
                nombre_completo=nom,edad=ed,cedula=norm_ci(ci),cedula_raw=ci,fecha_reporte=fe,hora_reporte=ho,
                confianza="alta",fuente_archivo="Lista digitalizada de pacientes (Sheet)",fuente_link=LINKS["sheet1"],fuente_tipo="Google Sheet")
        elif section=="jgh":
            ap,no,ed,ci,proc,_,fe=(p+["","","","","","",""])[:7]
            add(tipo_lista="paciente",hospital="Hospital José Gregorio Hernández",
                apellidos=ap,nombres=no,edad=ed,cedula=norm_ci(ci),cedula_raw=ci,procedencia=proc,fecha_reporte=fe,
                confianza="alta",fuente_archivo="Lista digitalizada de pacientes (Sheet)",fuente_link=LINKS["sheet1"],fuente_tipo="Google Sheet")

# 3) CARLOS ARVELO personal contingencia
with open(os.path.join(RAW,"carlos_arvelo_personal.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split("|")]; p=(p+[""]*7)[:7]
        _,nombre,edad,sexo,ci,par,proc=p
        fall="fallecid" in (par+proc+nombre).lower()
        add(tipo_lista="personal_contingencia",hospital="Hospital Militar Dr. Carlos Arvelo",
            nombre_completo=nombre,edad=edad,sexo=sexo,cedula=norm_ci(ci),cedula_raw=ci,
            parentesco_observacion=par,procedencia=proc,fallecido=fall,confianza="media",
            fuente_archivo="lista_personal_contingencia.pdf",fuente_link=LINKS["arvelo_personal_pdf"],fuente_tipo="PDF (OCR)")

# 4) HUC report (Universitario, con cédula)
with open(os.path.join(RAW,"huc_report.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split("|")]; p=(p+[""]*7)[:7]
        _,nombre,edad,ci,proc,estado,diag=p
        fall = "FALLEC" in estado.upper()
        add(tipo_lista="paciente",hospital="Hospital Universitario de Caracas",
            nombre_completo=nombre,edad=edad,cedula=norm_ci(ci),cedula_raw=ci,procedencia=proc,
            diagnostico=diag,parentesco_observacion=estado,fallecido=fall,confianza="media",
            fuente_archivo="Reporte HUC 24-06-26.pdf",fuente_link=LINKS["huc_pdf"],fuente_tipo="PDF institucional")

# 5) CATIA fotos (legibles, con cédula)
with open(os.path.join(RAW,"catia_fotos.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split("|")]; p=(p+[""]*5)[:5]
        nombre,edad,ci,direc,area=p
        add(tipo_lista="paciente",hospital="Periférico de Catia",
            nombre_completo=nombre,edad=edad,cedula=norm_ci(ci),cedula_raw=ci,procedencia=direc,
            parentesco_observacion=area,confianza="media",
            fuente_archivo="Fotos Hospital de Catia",fuente_link=LINKS["catia_folder"],fuente_tipo="Imagen (OCR legible)")

# 6) EL AVILA fotos (confianza baja)
with open(os.path.join(RAW,"elavila_fotos.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split("|")]; p=(p+[""]*6)[:6]
        _,no,ap,ed,ci,diag=p
        add(tipo_lista="paciente",hospital="Clínica El Ávila",
            apellidos=ap,nombres=no,edad=ed,cedula=norm_ci(ci),cedula_raw=ci,diagnostico=diag,
            confianza="baja",fuente_archivo="Fotos Clínica El Ávila",fuente_link=LINKS["elavila_folder"],fuente_tipo="Imagen (OCR baja)")

# 7) CIUDAD CARIBIA fotos (confianza baja)
with open(os.path.join(RAW,"ciudadcaribia_fotos.txt"),encoding="utf-8") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split("|")]; p=(p+[""]*6)[:6]
        ap,no,ed,ci,proc,estado=p
        add(tipo_lista="paciente",hospital="Hospital Ciudad Caribia",
            apellidos=ap,nombres=no,edad=ed,cedula=norm_ci(ci),cedula_raw=ci,procedencia=proc,
            parentesco_observacion=estado,confianza="baja",
            fuente_archivo="Fotos Hospital Ciudad Caribia",fuente_link=LINKS["caribia_folder"],fuente_tipo="Imagen (OCR baja)")

for i,r in enumerate(records,1): r["id"]=i

# ---------- DATASET COMPLETO (sin deduplicar) ----------
cols=["id","tipo_lista","hospital","apellidos","nombres","nombre_completo","edad","cedula","cedula_raw",
      "sexo","procedencia","diagnostico","parentesco_observacion","fecha_reporte","hora_reporte",
      "fallecido","confianza","fuente_archivo","fuente_link","fuente_tipo"]
def write_csv(path,rows,columns):
    with open(path,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns); w.writeheader()
        for r in rows: w.writerow({c:r.get(c,"") for c in columns})
json.dump(records,open(os.path.join(OUT,"sismo2026_completo.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
write_csv(os.path.join(OUT,"sismo2026_completo.csv"),records,cols)

# ---------- DEDUPLICACIÓN -> DATASET FINAL ----------
CONF={"alta":3,"media":2,"baja":1,"":0}
def merge(group):
    g=sorted(group,key=lambda r:CONF[r["confianza"]],reverse=True)
    out=dict(g[0])
    for r in g[1:]:
        for fld in ["edad","sexo","procedencia","diagnostico","parentesco_observacion","apellidos","nombres","fecha_reporte","hora_reporte"]:
            if not out.get(fld) and r.get(fld): out[fld]=r[fld]
        if r["fallecido"]: out["fallecido"]=True
    fuentes=sorted({r["fuente_archivo"] for r in group})
    out["fuentes"]="; ".join(fuentes)
    out["fuente_links"]=" ; ".join(sorted({r["fuente_link"] for r in group}))
    out["n_fuentes"]=len(fuentes)
    out["confianza"]=max(group,key=lambda r:CONF[r["confianza"]])["confianza"]
    return out

final=[]
by_ci=defaultdict(list); no_ci=[]
for r in records:
    (by_ci[r["cedula"]] if r["cedula"] else no_ci).append(r) if r["cedula"] else no_ci.append(r)
# fix: clean grouping
by_ci=defaultdict(list); no_ci=[]
for r in records:
    if r["cedula"]: by_ci[r["cedula"]].append(r)
    else: no_ci.append(r)
for ci,grp in by_ci.items():
    final.append(merge(grp))
# sin cédula: deduplicar por nombre_completo normalizado + hospital
seen={}
for r in no_ci:
    key=(re.sub(r"[^a-z0-9 ]","",r["nombre_completo"].lower()).strip(), r["hospital"])
    if key[0]=="":
        m=merge([r]); final.append(m); continue
    if key in seen: seen[key].append(r)
    else: seen[key]=[r]
for key,grp in seen.items():
    final.append(merge(grp))

for i,r in enumerate(sorted(final,key=lambda x:(x["hospital"],x["nombre_completo"])),1): r["id"]=i
final=sorted(final,key=lambda x:(x["hospital"],x["nombre_completo"]))

fcols=["id","tipo_lista","hospital","apellidos","nombres","nombre_completo","edad","cedula","cedula_raw",
       "sexo","procedencia","diagnostico","parentesco_observacion","fecha_reporte","hora_reporte",
       "fallecido","confianza","n_fuentes","fuentes","fuente_links"]
json.dump(final,open(os.path.join(OUT,"sismo2026_final_dataset.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
write_csv(os.path.join(OUT,"sismo2026_final_dataset.csv"),final,fcols)

# ---------- REPORTE ----------
rep=[]
rep.append("REPORTE FINAL - SISMO 2026 VZLA"); rep.append("="*55)
rep.append(f"Registros crudos (todas las fuentes): {len(records)}")
rep.append(f"Registros finales (deduplicados):     {len(final)}")
rep.append(f"  - colapsados por cédula/nombre:      {len(records)-len(final)}")
rep.append("")
rep.append("FINAL por hospital/centro:")
for k,v in Counter(r["hospital"] for r in final).most_common(): rep.append(f"  {v:>4}  {k}")
rep.append("")
rep.append("FINAL por tipo de lista:")
for k,v in Counter(r["tipo_lista"] for r in final).most_common(): rep.append(f"  {v:>4}  {k}")
rep.append("")
rep.append("FINAL por confianza:")
for k,v in Counter(r["confianza"] for r in final).most_common(): rep.append(f"  {v:>4}  {k}")
con_ci=sum(1 for r in final if r["cedula"])
rep.append("")
rep.append(f"Con cédula: {con_ci}   Sin cédula: {len(final)-con_ci}")
rep.append(f"Fallecidos: {sum(1 for r in final if r['fallecido'])}")
multi=[r for r in final if r["n_fuentes"]>1]
rep.append(f"Personas presentes en >1 fuente (cruce confirmado): {len(multi)}")
rep.append("")
rep.append("Ejemplos de cruce multi-fuente:")
for r in multi[:15]:
    rep.append(f"  [{r['cedula'] or 's/c'}] {r['nombre_completo']} ({r['hospital']}) <- {r['fuentes']}")
txt="\n".join(rep)
open(os.path.join(OUT,"reporte_final.txt"),"w",encoding="utf-8").write(txt)
print(txt)
