# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo does

Normalizes dispersed hospital patient data (PDFs, photos, spreadsheets) from the Google Drive folder "SISMO 2026 VZLA" into a single deduplicated dataset. No external dependencies — pure Python 3 stdlib only.

## Commands

```bash
# Full pipeline: raw sources -> completo + final datasets + reporte_final.txt
python3 scripts/build_dataset.py

# Drive inventory -> manifiesto_archivos.csv / .json
python3 scripts/make_manifest.py
```

All output goes to `data/processed/`. Scripts use `__file__`-relative paths so they work from any directory.

El explorador web `index.html` carga el JSON por fetch y funciona directo en GitHub Pages — no requiere script de generación.

## Data pipeline architecture

```
data/raw/          (pipe-delimited text files, # comment lines)
  master_registry.txt         N|HOSPITAL|NOMBRE|EDAD
  huc_report.txt              N|NOMBRE|EDAD|CEDULA|PROCEDENCIA|ESTADO|DIAGNOSTICO
  sheet1.md                   ### TABLA N sections, then pipe rows
  carlos_arvelo_personal.txt  N|NOMBRE|EDAD|SEXO|CI|PARENTESCO|PROCEDENCIA
  catia_fotos.txt             NOMBRE|EDAD|CI|DIRECCION|AREA
  elavila_fotos.txt           N|NOMBRES|APELLIDOS|EDAD|CI|DIAGNOSTICO
  ciudadcaribia_fotos.txt     APELLIDOS|NOMBRES|EDAD|CI|PROCEDENCIA|ESTADO
        |
        v  build_dataset.py (one parser block per source)
        |
data/processed/
  sismo2026_completo.*         all rows undeduped (741 records)
  sismo2026_final_dataset.*    deduplicated (655 persons)  ← primary output
  reporte_final.txt            summary counts and cross-source matches

index.html        explorador web (carga el JSON por fetch, funciona en GitHub Pages)
```

**Deduplication logic** in `build_dataset.py`:
1. Group by `cedula` (digits only, stripped by `norm_ci()`).
2. Records without `cedula`: group by `(normalized_nombre_completo, hospital)`.
3. `merge()` picks the highest-confidence record as base and fills empty fields from lower-confidence ones. Confidence tiers: `alta` (digitized sheets) > `media` (PDF/institutional reports) > `baja` (OCR of photos).

**Adding a new source**: add a `data/raw/<source>.txt` in pipe-delimited format with `#` header comments, then add a parser block in `build_dataset.py` using `add(**fields)` — the `add()` function fills defaults for any missing fields.

## Dataset schema

`id, tipo_lista, hospital, apellidos, nombres, nombre_completo, edad, cedula, cedula_raw, sexo, procedencia, diagnostico, parentesco_observacion, fecha_reporte, hora_reporte, fallecido, confianza, n_fuentes, fuentes, fuente_links`

- `cedula`: digits only (for DB matching). `cedula_raw`: original as it appears in the source.
- `tipo_lista`: `paciente` or `personal_contingencia` (Carlos Arvelo family/staff list).
- `n_fuentes / fuentes / fuente_links`: cross-source traceability.

## Known data quality issues

- **José Gregorio Hernández**: some persons split into 2 rows with different last names but same cédula (transcription artefact from the original sheet).
- **Hospital Vargas**: `fecha_reporte` appears auto-filled sequentially (25-06, 26-06…) and is likely not real.
- **El Ávila / Ciudad Caribia** (`confianza=baja`): OCR from photos — verify cédulas/names against source images before trusting.
- Cédulas with 8+ digits in HUC data are likely OCR errors from the original report.
- **Not included**: "Sobrevivientes Campo de Golf" (19 handwritten photo lists); raw OCR is in `data/processed/fuentes_imagenes_ocr_crudo.md` for manual review.
