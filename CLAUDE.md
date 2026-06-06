# CLAUDE.md — Proyecto Par Biomagnético

## Descripción del Proyecto

Guía de referencia web de página única (SPA) para **Pares Biomagnéticos (PBs)**, basada en los trabajos del Dr. Isaac Goiz Durán y David Goiz Martínez (BRI 2017). La aplicación es bilingüe español/ruso con un botón de toggle ES/RU en el header.

**Contenido:**
- 210 Pares Biomagnéticos Nivel 1 (PBs 1–210)
- 115 Pares Nivel 2 / Bioenergética (PBs 211–325)
- 28 Pares Emocionales
- Protocolo de Rastreo Completo
- Índice de enfermedades con protocolos Top 10/5
- Búsqueda global

## Archivos del Proyecto

```
biomagnetismo/
├── index.html              # Aplicación completa (~2115 líneas, todo en un archivo)
├── disease_data.js         # Datos generados: const TOP10 y const DISEASE_DATA
├── build_disease_data.py   # Script que genera disease_data.js (editar aquí los protocolos)
├── netlify.toml            # Config de deploy: publish=".", redirect /* → /index.html
├── start.bat               # Servidor local: python -m http.server 8080
├── KB_PROJECT_PLAN.md      # Plan de base de conocimientos personal (proyecto separado)
├── tools/
│   ├── extract_pdfs.py     # Extrae texto de PDFs fuente → pdf_texts/
│   ├── fill_pbs.py         # Rellena datos de PBs desde pdf_texts/
│   ├── find_missing_pbs.py # Detecta PBs sin datos
│   └── list_empty_pbs.py   # Lista PBs con campos vacíos
├── pdf_texts/              # Textos extraídos de los PDFs fuente (13 archivos .txt)
├── img/
│   ├── pbs/                # Imágenes de posicionamiento: pb_001.jpg … pb_NNN.jpg
│   ├── preview/            # Miniaturas pg25_img0.jpeg … (páginas 25–32)
│   └── preview_full/       # Páginas completas pg25_full.png … pg25_3x.png
└── screenshots/            # Capturas de pantalla de desarrollo
```

## PDFs Fuente

Los PDFs originales están en:
```
C:\Users\usuario\Downloads\3_Биомагнетизм_BQ\Маркеры_негатива\libros biomag\
```

PDFs extraídos a `pdf_texts/` (13 archivos):
- `LINDE29-Bio-Magne-Tismo-Kronos (1).pdf.txt` — Guía principal Nivel 1
- `LINDE 3-Guia-Pares-Biomagnetico-2do-nivel (1).pdf.txt` — Guía Nivel 2
- `Guia de rastreo segundo nivel.pdf.txt` — Protocolo de rastreo
- `Pares por enfermedad.pdf.pdf.txt` — Enfermedades y protocolos
- `Diccionario Bio-Emocional 2016.pdf.txt` — Pares emocionales
- `55822230-rastreo-biomagnetismo-completo-con-imagenes-1.pdf.txt`
- `Correos electrónicos 😍Atlas David Goiz.pdf.txt`
- Y otros 6 PDFs de referencia

## Estado Actual

- **Nivel 1:** datos completos (210 PBs), imágenes en `img/pbs/pb_NNN.jpg`
- **Nivel 2:** datos completos (115 PBs), PBs 211–325
- **Enfermedades:** ~60 enfermedades con protocolos en `build_disease_data.py` → `disease_data.js`
- **Traducción ES→RU:** implementada con dual-label en tablas (nombre en español + traducción rusa debajo)
- **Deploy:** configurado para Netlify (rama main)

## Pipeline de Datos

```
PDFs fuente (Downloads/)
    ↓ tools/extract_pdfs.py
pdf_texts/*.txt
    ↓ tools/fill_pbs.py (asistencia para poblar datos)
build_disease_data.py (edición manual de TOP10 y DISEASES)
    ↓ python build_disease_data.py
disease_data.js  ← cargado por index.html vía <script src="disease_data.js">
```

Para regenerar `disease_data.js`:
```
python build_disease_data.py
```

## Arquitectura de index.html

Todo el código está en un único archivo `index.html`:
1. **CSS inline** en `<style>` (líneas ~8–160)
2. **HTML estático** con `data-i18n="clave"` en cada texto traducible
3. **JavaScript** al final del `<body>` con:
   - Arrays `N1_PBS[]` y `N2_PBS[]` con todos los pares
   - Objeto `TRANSLATIONS` con todas las traducciones ES→RU
   - Funciones: `showTab()`, `toggleLanguage()`, `applyLang()`, `openModal()`, `searchAll()`
   - Los datos de enfermedades vienen de `disease_data.js` (cargado antes)

## Sistema de Traducción ES/RU

### Mecanismo

- Cada elemento HTML tiene `data-i18n="clave"` o `data-i18n-html="true"`
- `applyLang(lang)` recorre el DOM y reemplaza textos según el idioma activo
- El idioma se guarda en `localStorage` como `'lang'`
- El botón toggle alterna entre `'es'` y `'ru'`

### Dual-label en tablas

En modo ruso, los nombres de PBs y patologías se muestran con **doble etiqueta**:
```html
<span class="dual-label">
  Nombre en español
  <span class="trans">Перевод на русский</span>
</span>
```
Clase `.dual-label-sm` para texto más pequeño (dentro de modal).

### Estructura del objeto TRANSLATIONS

```javascript
const TRANSLATIONS = {
  es: { /* todas las claves en español */ },
  ru: {
    // UI strings
    "title": "Биомагнетический пар — Справочник",
    // Nombres de PBs (puntos anatómicos)
    pbNames: { "Timo – Recto": "Тимус – Прямая кишка", ... },
    // Patologías
    pathologies: { "VIH": "ВИЧ", ... },
    // Enfermedades (índice)
    diseases: { "Diabetes Mellitus": "Сахарный диабет", ... },
    // Síntomas
    symptoms: { "Cefalea, mareo": "Головная боль, головокружение", ... },
    // Emociones
    emotions: { "Miedo": "Страх", ... },
    // Top 10 nombres de categorías
    tops: { "Top 10 Cardiológico": "Топ 10 Кардиологический", ... }
  }
}
```

## Reglas de Traducción Español → Ruso

### Nombres anatómicos (puntos de PBs)

- El formato es siempre `"Punto Rastreo – Punto Impacto"` (guión largo `–`)
- Traducir ambos puntos por separado cuando sea posible
- **Correcciones conocidas y ya aplicadas:**
  - `Tima` → `Timo` (Timos en ruso: Тимус) — error tipográfico en PDFs originales
  - `Tiraacusares` → `Tráquea` — error OCR en PDFs originales
- Nombres de órganos estándar: usar terminología médica rusa establecida
- Lateralidad: `Derecho/Izquierdo` → `Правый/Левый` (o sin artículo si no aplica)

### Patologías y microorganismos

- Nombres científicos de microorganismos (Candida albicans, etc.) NO se traducen
- Nombres de enfermedades: usar nombre médico ruso establecido
- VIH/SIDA → ВИЧ/СПИД

### Interfaz UI

- Mantener consistencia: "Nivel 1" → "Уровень 1", "Par Biomagnético" → "Биомагнетический пар"
- "Polo negativo (rastreo)" → "Отрицательный полюс (зондирование)"
- "Polo positivo (impacto)" → "Положительный полюс (воздействие)"

### Tipos de PBs

- VIRUS → ВИРУС
- BACTERIAS → БАКТЕРИИ
- HONGOS → ГРИБКИ
- PARÁSITOS → ПАРАЗИТЫ
- ESPECIALES → ОСОБЫЕ (o СПЕЦИАЛЬНЫЕ)

## Cómo Ejecutar Localmente

```bat
start.bat
```
Abre el navegador en `http://localhost:8080` usando `python -m http.server 8080`.

O directamente:
```
python -m http.server 8080
```

## Deploy

- **Plataforma:** Netlify
- **Rama:** main
- **Configuración:** `netlify.toml` (publish=`.`, redirect `/*` → `/index.html`)
- No hay build step — se sirven los archivos estáticos directamente

## Imágenes de PBs

Cada Par Biomagnético puede tener imagen de posicionamiento en `img/pbs/pb_NNN.jpg` (con cero-padding a 3 dígitos). Si el archivo no existe, el modal no muestra imagen. El thumbnail aparece en la tabla y el modal muestra la imagen a tamaño completo.

## Notas Importantes

- `build_disease_data.py` es la fuente de verdad para los protocolos de enfermedades — editarlo directamente para añadir/corregir enfermedades, luego regenerar `disease_data.js`
- Los datos de los PBs (N1_PBS y N2_PBS) están hardcodeados en `index.html` — no se generan con script
- `KB_PROJECT_PLAN.md` es un plan para una base de conocimiento personal separada (no relacionada con la guía biomagnética)
- El proyecto NO usa frameworks ni dependencias externas — HTML/CSS/JS puro
