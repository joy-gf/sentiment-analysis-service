# 🧠 Arquitectura de Análisis de Sentimientos

## 📋 Resumen

Sistema de análisis de sentimientos para diarios emocionales con procesamiento automático, detección offline/online y almacenamiento de resultados.

## 🏗️ Arquitectura General

```
┌─────────────────┐
│   Frontend      │
│  (React + MUI)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐         ┌──────────────────┐
│  Backend API    │────────▶│  Microservicio   │
│  (Node.js +     │◀────────│  Análisis ML     │
│   TypeORM)      │         │  (Python/FastAPI)│
└────────┬────────┘         └──────────────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   - diario_emocional
│   - analisis_sentimiento
└─────────────────┘
```

## 🔄 Flujo de Análisis

### 1. **Paciente guarda entrada de diario**

```
Usuario escribe → Guarda entrada → Backend crea registro
                                   estado_analisis = "pendiente"
```

### 2. **Análisis automático**

```
Backend.create() → triggerAnalysis() [async]
                   ├─ Llama a MS Python (/analyze/enhanced)
                   ├─ MS retorna: sentimiento, emoción, keywords, alertas
                   ├─ Backend guarda en tabla analisis_sentimiento
                   └─ Marca diario como estado_analisis = "analizado"
```

### 3. **Si está offline**

```
Diario se guarda → estado_analisis = "pendiente"

Cuando vuelve online:
  → Backend.processPendingAnalysis(pacienteId)
  → Procesa todas las entradas pendientes en lote
  → Actualiza estados a "analizado"
```

## 📊 Modelos de Datos

### DiarioEmocional (Actualizado)
```sql
- id: UUID
- paciente_id: UUID
- fecha_entrada: DATE
- emocion_seleccionada: VARCHAR(50)  -- Emoji que seleccionó
- texto_entrada: TEXT
- estado_analisis: VARCHAR(20)       -- ✨ NUEVO
  └─ valores: "pendiente", "analizado", "error"
```

### AnalisisSentimiento (Nueva tabla)
```sql
- id: UUID
- diario_emocional_id: UUID
- paciente_id: UUID
- fecha_analisis: DATE
- sentimiento_general: VARCHAR(20)   -- esperanzador, desafiante, equilibrado
- confianza: DECIMAL(5,4)
- score_positivo: DECIMAL(5,4)
- score_negativo: DECIMAL(5,4)
- score_neutral: DECIMAL(5,4)
- emocion_predominante: VARCHAR(50)  -- Ansioso, Feliz, etc.
- palabras_clave: JSONB              -- [{"word": "...", "frequency": N}]
- alertas: JSONB                     -- [{"type": "...", "text": "..."}]
- modelo_usado: VARCHAR(255)
```

## 🎯 Endpoints Backend

### Diario Emocional
- `POST /api/diario-emocional` - Crear entrada (dispara análisis automático)
- `PUT /api/diario-emocional/:id` - Actualizar (re-analiza si cambió texto)
- `GET /api/diario-emocional/:pacienteId` - Obtener entradas

### Análisis
- `GET /api/analisis/:pacienteId` - Análisis agregado (para el tab)
- `GET /api/analisis/:pacienteId/entradas` - Análisis individuales
- `POST /api/analisis/:pacienteId/procesar-pendientes` - Forzar análisis
- `POST /api/analisis/entrada/:diarioId/analizar` - Analizar entrada específica

## 🤖 Microservicio Python

### Endpoint Principal
**POST /analyze/enhanced**

**Request:**
```json
{
  "text": "Hoy me siento muy bien...",
  "diario_id": "uuid-123"
}
```

**Response:**
```json
{
  "sentimiento_general": "positivo",
  "score_positivo": 0.85,
  "score_negativo": 0.10,
  "score_neutral": 0.05,
  "confianza": 0.85,
  "modelo_usado": "pysentimiento/robertuito-sentiment-analysis",
  "emocion_predominante": "Feliz",
  "palabras_clave": [
    {"word": "proyecto", "frequency": 3},
    {"word": "logré", "frequency": 2}
  ],
  "alertas": [
    {
      "type": "info",
      "text": "Sentimiento positivo detectado"
    }
  ]
}
```

### Componentes del MS

1. **SentimentAnalyzer** - Análisis base con transformers
2. **EmotionDetector** - Detecta emoción específica (Ansioso, Feliz, etc.)
3. **KeywordExtractor** - Extrae palabras clave frecuentes
4. **AlertGenerator** - Genera alertas basadas en contenido

## 📈 Tab de Análisis (Frontend)

### Datos que muestra:
1. **Alertas detectadas** - Del campo `alertas` JSONB
2. **Total de entradas** - COUNT de análisis
3. **Sentimiento general** - Promedio de scores
4. **Emoción predominante** - Más frecuente en el período
5. **Distribución de emociones** - Gráfico de barras
6. **Evolución temporal** - Timeline de sentimientos por fecha
7. **Palabras clave** - Agregado de todas las entradas

### Llamada al cargar el tab:
```typescript
const response = await api.get(`/analisis/${pacienteId}?periodo=30`);

// Retorna:
{
  total_entradas: 15,
  sentimiento_promedio: 0.23,
  distribucion_emociones: {
    "Ansioso": 5,
    "Feliz": 4,
    "Tranquilo": 6
  },
  palabras_clave: [
    {"word": "trabajo", "frequency": 18},
    {"word": "familia", "frequency": 15}
  ],
  alertas: [...],
  evolucion_temporal: [
    {
      fecha: "2026-01-25",
      sentimiento: "esperanzador",
      score: 0.75,
      emocion: "Feliz",
      confianza: 0.85
    },
    ...
  ]
}
```

## 🔧 Variables de Entorno

### Backend (.env)
```bash
SENTIMENT_SERVICE_URL=http://localhost:8000
```

### Microservicio Python (.env)
```bash
MODEL_NAME=pysentimiento/robertuito-sentiment-analysis
DEVICE=cpu
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🚀 Ventajas de esta arquitectura

1. ✅ **No bloquea al usuario** - Análisis asíncrono
2. ✅ **Funciona offline** - Marca como pendiente
3. ✅ **Procesa lotes** - Eficiente al volver online
4. ✅ **Datos históricos** - Almacena análisis por fecha
5. ✅ **Escalable** - MS Python puede escalar independientemente
6. ✅ **Amigable** - Términos comprensibles (esperanzador vs positivo)
7. ✅ **Alertas automáticas** - Detecta patrones de riesgo
8. ✅ **Sin duplicados** - Un análisis por entrada de diario

## 📝 Próximos pasos para integrar

1. ✅ Ejecutar migraciones en backend
2. ✅ Instalar dependencias del MS Python
3. ✅ Iniciar MS Python: `cd sentiment-analysis-service && python -m uvicorn app.main:app --reload`
4. ✅ Iniciar backend Node.js
5. ✅ Probar crear entrada de diario
6. ✅ Ver análisis en el tab de "Análisis de Sentimientos"
