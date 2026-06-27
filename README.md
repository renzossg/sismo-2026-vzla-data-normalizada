# SISMO 2026 VZLA — Dataset normalizado FINAL

Normalización de la carpeta de Drive **SISMO 2026 VZLA** (ingresos hospitalarios tras el sismo)
a un formato único, deduplicado, para contrastar contra una base de datos.

> ## ℹ️ Sobre este repositorio
>
> Este repositorio **no es la fuente original** de los datos: es únicamente la **normalización
> y estructuración** de una base de datos que ya se encuentra **pública** en Google Drive,
> compartida abiertamente como parte de la respuesta a la emergencia del sismo.
>
> **Fuente original (Google Drive, pública):**
> https://drive.google.com/drive/folders/1o36ifaRz45kAs5rKzci49aD0mP5JB_YI
>
> El **único objetivo** de este trabajo es **ordenar y unificar** esa información dispersa
> (PDFs, imágenes, hojas de cálculo de distintos hospitales) en un formato consistente y
> consultable, para facilitar la coordinación y la ubicación de personas afectadas.
> No se recolectaron datos nuevos ni se añadió información que no estuviera ya en la fuente.
>
> Los datos pertenecen a sus titulares y a las instituciones que los generaron. Se pide a quien
> los utilice hacerlo **con responsabilidad y con el único fin de ayudar** a las personas
> afectadas por la emergencia.

## Archivos principales
- **`sismo2026_final_dataset.json` / `.csv`** — ⭐ dataset FINAL deduplicado (una fila por persona).
- `sismo2026_completo.json` / `.csv` — todas las filas SIN deduplicar (cada fila = una aparición en una fuente).
- `reporte_final.txt` — conteos finales, cruces multi-fuente, fallecidos.
- `manifiesto_archivos.csv` / `.json` — inventario de TODO el Drive con links y estado.
- `fuentes_imagenes_ocr_crudo.md` — OCR crudo de listas manuscritas (El Ávila, Ciudad Caribia, Sobrevivientes) para verificación manual.

## Esquema del dataset final
`id, tipo_lista, hospital, apellidos, nombres, nombre_completo, edad, cedula, cedula_raw,
sexo, procedencia, diagnostico, parentesco_observacion, fecha_reporte, hora_reporte,
fallecido, confianza, n_fuentes, fuentes, fuente_links`

- **cedula**: solo dígitos (para hacer match con la BD). **cedula_raw**: como aparece en la fuente.
- **n_fuentes / fuentes / fuente_links**: en cuántas y cuáles fuentes aparece la persona (trazabilidad y cruce).
- **confianza**: `alta` (hojas digitalizadas) · `media` (PDF/reporte impreso) · `baja` (foto manuscrita).
- **tipo_lista**: `paciente` o `personal_contingencia` (familiares/personal — Carlos Arvelo).

## Resultado
- **741 apariciones crudas → 655 personas únicas** tras deduplicar por cédula (y por nombre+hospital cuando no hay cédula).
- **52 personas** aparecen en más de una fuente (cruce confirmado).
- **305** con cédula · **350** sin cédula · **4** fallecidos.

| Centro | Personas |
|---|---|
| Hospital Militar Dr. Carlos Arvelo | 132 |
| Hospital Pérez Carreño | 104 |
| Hospital Domingo Luciani | 89 |
| Periférico de Catia | 74 |
| Hospital Universitario de Caracas | 69 |
| Hospital Vargas de Caracas | 58 |
| Hospital José Gregorio Hernández | 53 |
| Clínica El Ávila | 33 |
| Cruz Roja | 27 |
| Hospital Ciudad Caribia | 16 |

## Fuentes integradas
- Registro Maestro (PDF) → Cruz Roja, Periférico Catia, Domingo Luciani, Pérez Carreño.
- Reporte HUC (PDF, con cédula/procedencia/diagnóstico) → Hospital Universitario (reemplaza al Maestro por ser más completo; incluye 3 fallecidos).
- Hojas digitalizadas (Sheets) → Carlos Arvelo, Vargas, José Gregorio Hernández.
- PDF personal de contingencia → Carlos Arvelo (familiares/personal).
- Fotos legibles → Periférico de Catia (con cédula), Clínica El Ávila, Hospital Ciudad Caribia.

## Notas de calidad (revisar antes de cargar a la BD)
- **José Gregorio Hernández**: hay personas en 2 filas con apellidos distintos y misma cédula (artefacto de transcripción de la hoja original).
- **Hospital Vargas**: la columna "Fecha del reporte" de la hoja parece autollenada secuencialmente (25-06, 26-06…) y probablemente NO es real.
- **El Ávila / Ciudad Caribia (confianza baja)**: provienen de OCR de fotos; verificar cédulas/nombres contra la imagen.
- Cédulas con largo atípico (p. ej. 8+ dígitos en HUC) pueden ser errores de OCR del reporte original.

## NO incluido (requiere transcripción humana)
- **Sobrevivientes Campo de Golf (Playa Los Cocos)**: 19 fotos de listas manuscritas de SOLO nombres
  (refugio, no pacientes), muy ruidosas y solapadas. Por seguridad (es una lista para ubicar personas)
  no se transcribieron automáticamente. Quedan en `fuentes_imagenes_ocr_crudo.md`.
- Fotos manuscritas adicionales de Catia (pizarras) y PDFs/Docs consolidados redundantes
  (`Consolidado.pdf`, `Listado 2`, `LISTAS DE PERSONAS…`) — ya cubiertos por las fuentes integradas.

## Estructura del repositorio
```
sismo-2026-vzla-data-normalizada/
├── README.md
├── scripts/
│   ├── build_dataset.py     # parsea data/raw -> dataset final + completo + reporte
│   └── make_manifest.py     # genera el manifiesto de archivos del Drive
└── data/
    ├── raw/                 # textos fuente extraídos del Drive (insumos)
    └── processed/           # RESULTADOS (datasets finales, manifiesto, reportes)
```

## Cómo regenerar los resultados
```bash
python3 scripts/build_dataset.py
python3 scripts/make_manifest.py
```
Los archivos se escriben en `data/processed/`.
