# Documentación técnica

## Archivos principales
- `index.html` - explorador estático para web/GitHub Pages; carga el dataset final por `fetch`.
- `data/processed/sismo2026_final_dataset.json` / `.csv` - dataset final deduplicado.
- `data/processed/sismo2026_completo.json` / `.csv` - todas las filas sin deduplicar.
- `data/processed/reporte_final.txt` - conteos, cruces y resumen final.
- `data/processed/manifiesto_archivos.csv` / `.json` - inventario del Drive.
- `data/processed/fuentes_imagenes_ocr_crudo.md` - OCR crudo para revisión manual.

## Esquema del dataset final
`id, tipo_lista, hospital, apellidos, nombres, nombre_completo, edad, cedula, cedula_raw, sexo, procedencia, diagnostico, parentesco_observacion, fecha_reporte, hora_reporte, fallecido, confianza, n_fuentes, fuentes, fuente_links`

- `cedula`: solo dígitos para matching.
- `cedula_raw`: valor original tal como aparece en la fuente.
- `n_fuentes / fuentes / fuente_links`: trazabilidad y cruce entre fuentes.
- `confianza`: `alta` (hojas digitalizadas), `media` (PDF/reporte institucional), `baja` (OCR de fotos).
- `tipo_lista`: `paciente` o `personal_contingencia`.

## Resultado actual
- `741` apariciones crudas -> `655` personas únicas.
- `52` personas aparecen en más de una fuente.
- `305` con cédula.
- `350` sin cédula.
- `4` fallecidos.

## Fuentes integradas
- Registro Maestro (PDF) -> Cruz Roja, Periférico de Catia, Domingo Luciani, Pérez Carreño.
- Reporte HUC (PDF) -> Hospital Universitario de Caracas.
- Hojas digitalizadas (Sheets) -> Carlos Arvelo, Vargas, José Gregorio Hernández.
- PDF de personal de contingencia -> Carlos Arvelo.
- Fotos legibles / OCR -> Catia, Clínica El Ávila, Ciudad Caribia.

## Estructura del repositorio
```text
sismo-2026-vzla-data-normalizada/
├── index.html
├── README.md
├── docs/
│   └── readme.md
├── scripts/
│   ├── build_dataset.py
│   └── make_manifest.py
└── data/
    ├── raw/
    └── processed/
```

## Cómo regenerar los resultados
```bash
python3 scripts/build_dataset.py
python3 scripts/make_manifest.py
```

Todos los resultados se escriben en `data/processed/`.

## Explorador web
- `index.html` carga `data/processed/sismo2026_final_dataset.json` con `fetch`.
- En GitHub Pages funciona directamente al servirse por HTTP desde el mismo origen.
- En local, hay que servir el repo por HTTP. Ejemplo:

```bash
python3 -m http.server
```

Luego abre `http://localhost:8000/`.

## Notas de calidad
- José Gregorio Hernández: hay filas con apellidos distintos y misma cédula.
- Hospital Vargas: la fecha del reporte parece autollenada secuencialmente y podría no ser real.
- El Ávila y Ciudad Caribia (`confianza=baja`): provienen de OCR; conviene verificar contra la imagen original.
- Cédulas atípicas en HUC pueden venir de errores de OCR.

## No incluido
- Sobrevivientes Campo de Golf (Playa Los Cocos): requiere transcripción humana.
- Fotos manuscritas adicionales o consolidados redundantes ya cubiertos por otras fuentes.
