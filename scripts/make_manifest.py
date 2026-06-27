# -*- coding: utf-8 -*-
import json, csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "processed")
os.makedirs(OUT, exist_ok=True)

def L(id, kind):
    if kind=="folder": return f"https://drive.google.com/drive/folders/{id}"
    if kind=="sheet":  return f"https://docs.google.com/spreadsheets/d/{id}"
    if kind=="doc":    return f"https://docs.google.com/document/d/{id}"
    return f"https://drive.google.com/file/d/{id}/view"

# (carpeta, nombre, id, kind, estado)
INV = [
("(raíz)","SISMO 2026 VZLA","1o36ifaRz45kAs5rKzci49aD0mP5JB_YI","folder","carpeta raíz"),
# --- archivos sueltos en raíz ---
("(raíz)","1_5040023583598840087 (2).pdf  [Registro Maestro 337]","10tLqzNMBs_gl-VMiK7KaQTDbqvpSoutI","file","EXTRAÍDO"),
("(raíz)","Ingresos por sismo en Hospitales consolidado - Consolidado.pdf","1Ez1nYX0kIbPqGPInDIeWw_qP4bqqI66-","file","PENDIENTE (PDF grande)"),
("(raíz)","Listado 2 (Google Doc)","125LObYNRazMhUuxeF8FFthiA5YJaGFyApKiUHyO4olo","doc","PENDIENTE"),
("(raíz)","LISTAS DE PERSONAS EN MULTIPLES HOSPITALES (Google Doc)","1SHnWBNnzxsJ30Yr1bY8cF3SP2By7mX2jtquHiyKLesU","doc","PENDIENTE"),
# --- subcarpetas ---
("(raíz)","CLINICAS EL AVILA","1DvHmDkLOeK6NG-WlC0bphKmhDr52MY_S","folder","solo imágenes (4) - OCR crudo"),
("(raíz)","HOSPITAL CARLOS ARVELEDO","1Yku1lGK5RVSgAS56UhbRHDhtYgraJZqj","folder","doc->drive externo"),
("(raíz)","HOSPITAL CIUDAD CARIBIA","13JEMBh0VJVUxndt-wj_bujNqd_i9rin0","folder","solo imágenes (2) - OCR crudo"),
("(raíz)","HOSPITAL DE CATIA","10gm4GStjkb6hCgr5yMdvh77H36hA7M-w","folder","solo imágenes (6) - PENDIENTE"),
("(raíz)","HOSPITAL LUCIANI CARACAS","1womt9b3TSngAE31YoYSWowYY930rZPkZ","folder","imágenes (19); datos en Registro Maestro"),
("(raíz)","HOSPITAL PEREZ CARREÑO","1GfyUgXJncw1qNKI1qjiceo_hv87IG0Q6","folder","imágenes (31); datos en Registro Maestro"),
("(raíz)","HOSPITAL UNIVERSITARIO CARACAS","1A1JTzkBhBU2xT4WdUSHSD8EusPos13IJ","folder","1 PDF; datos en Registro Maestro"),
("(raíz)","HOSPITAL VARGAS DE CARACAS","15s28bbAxuluxJbe-zb9KNJ_-ywn90qWT","folder","imágenes (5); datos en Sheet digitalizada"),
("(raíz)","LINK DE BUSQUEDA DE PERSONAS","16U7z2m_yvoHfHUEikpjXAJ1_K5yEOr9g","folder","doc utilitario (no pacientes)"),
("(raíz)","LISTA DIGITALIZADA DIFERENTES ESTADOS","1sUF0SzGBPru03loWh6BLIKC4m-UIE87R","folder","2 Sheets digitalizadas"),
("(raíz)","Sobrevivientes en campo de golf Playa Los cocos","1EByuS5LU7mb8rIKShoOUp0jJzNyHFszT","folder","solo imágenes (19)+doc - PENDIENTE"),
# --- Carlos Arvelo: doc + drive externo ---
("HOSPITAL CARLOS ARVELEDO","HOSPITAL MILITAR DR CARLOS ARVELEDO (doc->link)","1TZ6BVF9PT2KEXCbnfCcPKEDmquQsqHAGTABY3BCc858","doc","EXTRAÍDO (apunta a drive externo)"),
("Listado Dr Carlos Arveledo 25/06 (externo roossinai09)","lista_personal_contingencia.pdf [151]","13U9VcEa6iNnRkLANEA_Gk9mdpVcZ0WqR","file","EXTRAÍDO"),
("Listado Dr Carlos Arveledo 25/06 (externo)","IMG_6109.PNG","1yDDVGGQAM4nuU2UoycIzqz-EB1Cfls1U","file","fuente imagen del PDF"),
("Listado Dr Carlos Arveledo 25/06 (externo)","IMG_6110.PNG","1ZicUPJIrcFhIaY8dq0zlq_hSYj_IWqVK","file","fuente imagen del PDF"),
("Listado Dr Carlos Arveledo 25/06 (externo)","IMG_6111.PNG","14YP-w3UxAMJ_nCxmj5wRZx4KfKmU16DX","file","fuente imagen del PDF"),
("Listado Dr Carlos Arveledo 25/06 (externo)","IMG_6112.PNG","1c4GkqcoeHZ_ebQV0QfE1AYkuc9JHJ_f2","file","fuente imagen del PDF"),
# --- LISTA DIGITALIZADA DIFERENTES ESTADOS ---
("LISTA DIGITALIZADA DIFERENTES ESTADOS","Lista digitalizada de pacientes en hospitales (Sheet)","1wzpm_7pd0fC4hFou5FzppMNeZkd6J6NvrPqy-PWNvRY","sheet","EXTRAÍDO (Arvelo+Vargas+JGH)"),
("LISTA DIGITALIZADA DIFERENTES ESTADOS","Pacientes en hospitales 2 (Sheet)","1EQ-_ENQUhtLaTdZtyhLZuSJZ7WG4RUuyc7ipGc7emhM","sheet","EXTRAÍDO (Vargas, borrador)"),
("LISTA DIGITALIZADA DIFERENTES ESTADOS","Imagen de enlace.png","1NxRqLMtXrYEm3TQILN-ItE7bJ5K_0Uno","file","imagen"),
# --- HOSPITAL UNIVERSITARIO CARACAS ---
("HOSPITAL UNIVERSITARIO CARACAS","Reporte HUC 24-06-26 (1).pdf","1mA7z1Mtyb2VzvKlE2H9PBS6v8tEpdPJb","file","PENDIENTE"),
# --- LINK DE BUSQUEDA ---
("LINK DE BUSQUEDA DE PERSONAS","LINK BUSCA Y REGISTRA PERSONAS (doc)","15AENoLpeRKZN-Bmcb6eNhMCGZofnc5vDR45s4m8AGb4","doc","utilitario"),
# --- Sobrevivientes: doc ---
("Sobrevivientes en campo de golf","DIRECCION (doc)","175B0H2x0Kad6e08cwr4eRvUzu8wZHYeBD1FvkKS68kI","doc","PENDIENTE"),
]

# imágenes por carpeta (id, nombre)
IMG = {
"CLINICAS EL AVILA": [
 ("1aB-1pMesako_0rugAKZ1NE-H9Sdb59tH","WhatsApp Image ... (1).jpeg"),
 ("16VkYy9pnogKsbOjkP4t8nOQe-XPVbUCZ","WhatsApp Image ... (2).jpeg"),
 ("1ZRC1zj9rqedSNWoYhFmFRfwdxAqygelF","WhatsApp Image ... (3).jpeg"),
 ("1ade_iyLlp8cUchIa4Vtni_e1OeUlBXI6","WhatsApp Image ... .jpeg"),
],
"HOSPITAL CIUDAD CARIBIA": [
 ("1p7jgqsgcX51LxlP0WtCJbmIoDyFM5jbL","WhatsApp Image 4.34.19 PM.jpeg"),
 ("1f36IPOcITMnYe1tAMIcjuMVNZSf-iBfg","WhatsApp Image 4.34.20 PM.jpeg"),
],
"HOSPITAL DE CATIA": [
 ("1sk217wPfDVR82nAPKvtTKWTGRwrM3cvI","WA 10.16.43 AM (1).jpeg"),
 ("1r-jnigTq1__XTBWjH1MfyMe0epG_Ndva","WA 10.16.43 AM.jpeg"),
 ("1PYZHee2NvOZuY3Jop55o2oQcX6HodTbz","WA 11.16.11 AM (1).jpeg"),
 ("1E_Q28pOXou8j1HdjcjGRd9DF55juyR3c","WA 11.16.11 AM (2).jpeg"),
 ("1FXG1YQMpOigPH_tUfiVRS2xLZEMYdJWE","WA 11.16.11 AM (3).jpeg"),
 ("1HWVdVmTc8PKqlCIg1l3hyuTwSN6PjJee","WA 11.16.11 AM.jpeg"),
],
"HOSPITAL VARGAS DE CARACAS": [
 ("19nrLxkN53199ENbklMVLzcmQZXchD-Mz","IMG-20260625-WA0732.jpg"),
 ("1RHxG49VYKkjzBCofFp1DIo_am2N2KwgK","IMG-20260625-WA0763.jpg"),
 ("1F_AW9srOkj5VX7Bhntuh1oimvpruKqXx","IMG-20260625-WA0764.jpg"),
 ("1iPVOvTERVN_XB-5T1JqR84mKpq3Bw0Un","WA 7.45.54 PM (1).jpeg"),
 ("1sPN9GvBW43SqY6X0G2GlnLg9kO0sNZ3G","WA 7.45.54 PM.jpeg"),
],
}

rows=[]
for carpeta,nombre,id_,kind,estado in INV:
    rows.append(dict(carpeta=carpeta,nombre=nombre,tipo=kind,estado=estado,link=L(id_,kind),id=id_))
for carpeta,items in IMG.items():
    for id_,nombre in items:
        rows.append(dict(carpeta=carpeta,nombre=nombre,tipo="imagen",estado="imagen (OCR pendiente/crudo)",link=L(id_,"file"),id=id_))

# Luciani(19), Perez(31), Sobrevivientes(19) imágenes: registradas a nivel carpeta (datos ya en fuentes estructuradas o pendientes)
extra_counts = {"HOSPITAL LUCIANI CARACAS":19,"HOSPITAL PEREZ CARREÑO":31,"Sobrevivientes en campo de golf":19}
for c,n in extra_counts.items():
    rows.append(dict(carpeta=c,nombre=f"[{n} imágenes — ver carpeta]",tipo="imagen(grupo)",estado="OCR pendiente",link="(ver carpeta)",id=""))

with open(os.path.join(OUT,"manifiesto_archivos.json"),"w",encoding="utf-8") as f:
    json.dump(rows,f,ensure_ascii=False,indent=2)
with open(os.path.join(OUT,"manifiesto_archivos.csv"),"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["carpeta","nombre","tipo","estado","link","id"]); w.writeheader()
    for r in rows: w.writerow(r)

print(f"Manifiesto: {len(rows)} entradas")
from collections import Counter
for k,v in Counter(r["estado"] for r in rows).most_common(): print(f"  {v:>3}  {k}")
