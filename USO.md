# 📖 Guía de Uso - Sistema de Análisis de Sentimientos

## 👤 Para Usuarios (Pacientes)

### Escribir una entrada en el Diario Emocional

1. **Inicia sesión** con tu cuenta de paciente
2. Ve a **"Mis Tareas"**
3. Haz clic en el botón **"Diario Emocional"**
4. Selecciona **cómo te sientes** (emoticon)
5. Escribe tus **pensamientos y sentimientos** del día
6. Haz clic en **"Guardar Entrada"**

**¿Qué pasa después de guardar?**
- Tu entrada se guarda inmediatamente
- Si tienes internet, se analiza automáticamente (toma 2-5 segundos)
- Si NO tienes internet, se marca como "pendiente de análisis"
- Cuando recuperes internet, se analizará automáticamente

### Ver entradas anteriores

Puedes agregar más texto a tu entrada del día:

1. Abre el **Diario Emocional**
2. Si ya escribiste hoy, verás tu entrada anterior
3. Escribe más en el campo **"Agregar más pensamientos"**
4. Haz clic en **"Agregar a mi entrada"**

El sistema re-analizará tu entrada con el nuevo texto.

---

## 👨‍⚕️ Para Psicólogos

### Ver el análisis de sentimientos de un paciente

1. Ve a **"Pacientes"**
2. Selecciona un paciente
3. Haz clic en el tab **"Análisis de Sentimientos"**

### Qué información verás:

#### 1. **Alertas Detectadas** (arriba, si las hay)
- **⚠️ Alerta Crítica**: Indica palabras de alto riesgo (requiere atención inmediata)
- **⚠️ Advertencia**: Patrones negativos recurrentes
- **ℹ️ Info**: Observaciones generales

**Ejemplo:**
```
⚠️ Alta frecuencia de ansiedad detectada (45% de las entradas)
```

#### 2. **Métricas Clave**

**Total de Entradas:**
- Número de entradas del diario en el período seleccionado

**Sentimiento Promedio:**
- **Esperanzador** 🟢: Sentimiento general positivo
- **Desafiante** 🔴: Sentimiento general negativo
- **Equilibrado** 🟡: Sentimiento neutro

**Emoción Predominante:**
- La emoción más frecuente detectada en los textos
- Ejemplos: Ansioso, Feliz, Tranquilo, Estresado

**Tendencia:**
- 📈 **Mejorando**: Sentimiento ha mejorado últimamente
- 📉 **Empeorando**: Sentimiento ha empeorado
- → **Estable**: Sin cambios significativos

#### 3. **Distribución de Emociones**

Gráfico de barras mostrando:
- Cuántas veces aparece cada emoción
- Porcentaje del total

**Ejemplo:**
- Ansioso: 12 veces (35%)
- Tranquilo: 8 veces (24%)
- Feliz: 6 veces (18%)

#### 4. **Evolución Temporal**

Timeline visual de cómo ha cambiado el sentimiento día a día.

**Cómo leerlo:**
- **Barras hacia arriba** = Sentimiento positivo
- **Barras hacia abajo** = Sentimiento negativo
- **Altura** = Intensidad del sentimiento
- **Color** = Verde (positivo), Rojo (negativo), Naranja (neutral)

#### 5. **Palabras Clave**

Las palabras más mencionadas en las entradas.

**Colores:**
- 🟢 Verde: Palabras con contexto positivo
- 🔴 Rojo: Palabras con contexto negativo
- 🟠 Naranja: Palabras neutras

**Ejemplo:**
- trabajo (18 veces) - Rojo
- familia (15 veces) - Verde
- preocupación (12 veces) - Rojo

**Cómo interpretarlo:**
Si "trabajo" aparece mucho en rojo, significa que el paciente asocia el trabajo con sentimientos negativos.

#### 6. **Insights Clave**

Observaciones automáticas del sistema:

**Ejemplo:**
- ⚠️ "Alta frecuencia de entradas con ansiedad (35% de las entradas)"
- ✅ "Tendencia al alza en los últimos 3 días (+0.45 puntos)"
- ℹ️ "Patrón identificado: ansiedad relacionada con temas laborales"

### Cambiar el período de análisis

En la parte superior derecha:
- **Últimos 7 días** - Vista semanal (predeterminado)
- **Últimos 14 días** - Vista quincenal
- **Últimos 30 días** - Vista mensual

---

## 🔧 Para Desarrolladores

### Flujo de procesamiento

```
1. Paciente guarda entrada
   ↓
2. Backend guarda en DB (estado: "pendiente")
   ↓
3. Backend llama async a microservicio Python
   ↓
4. Python analiza texto y retorna resultados
   ↓
5. Backend guarda análisis en tabla analisis_sentimiento
   ↓
6. Backend marca entrada como "analizado"
```

### Si está offline:

```
1. Paciente guarda entrada
   ↓
2. Backend guarda en DB (estado: "pendiente")
   ↓
3. Llamada a microservicio falla (sin internet)
   ↓
4. Backend registra el error pero NO falla la operación
   ↓
5. Entrada queda marcada como "pendiente"

Cuando vuelve online:
6. Backend.processPendingAnalysis() procesa todas las pendientes
```

### Endpoints disponibles

#### Backend Node.js

**Obtener análisis agregado:**
```http
GET /api/analisis/:pacienteId?periodo=30
```

**Respuesta:**
```json
{
  "total_entradas": 15,
  "sentimiento_promedio": 0.23,
  "distribucion_emociones": {
    "Ansioso": 5,
    "Feliz": 4,
    "Tranquilo": 6
  },
  "palabras_clave": [
    {"word": "trabajo", "frequency": 18},
    {"word": "familia", "frequency": 15}
  ],
  "alertas": [
    {
      "type": "warning",
      "text": "Alta frecuencia de ansiedad detectada"
    }
  ],
  "evolucion_temporal": [
    {
      "fecha": "2026-01-25",
      "sentimiento": "esperanzador",
      "score": 0.75,
      "emocion": "Feliz",
      "confianza": 0.85
    }
  ]
}
```

**Procesar entradas pendientes:**
```http
POST /api/analisis/:pacienteId/procesar-pendientes
```

**Respuesta:**
```json
{
  "success": true,
  "message": "5 entradas procesadas exitosamente",
  "processed": 5
}
```

**Analizar entrada específica:**
```http
POST /api/analisis/entrada/:diarioId/analizar
```

#### Microservicio Python

**Análisis básico:**
```http
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "text": "Hoy me siento muy feliz"
}
```

**Análisis completo (con emociones, keywords, alertas):**
```http
POST http://localhost:8000/analyze/enhanced
Content-Type: application/json

{
  "text": "Hoy me siento muy feliz",
  "diario_id": "uuid-opcional"
}
```

### Consultas SQL útiles

**Ver entradas pendientes de análisis:**
```sql
SELECT id, fecha_entrada, estado_analisis
FROM diario_emocional
WHERE estado_analisis = 'pendiente'
ORDER BY fecha_entrada DESC;
```

**Ver análisis de un paciente:**
```sql
SELECT
  a.fecha_analisis,
  a.sentimiento_general,
  a.emocion_predominante,
  a.confianza
FROM analisis_sentimiento a
WHERE a.paciente_id = 'uuid-del-paciente'
ORDER BY a.fecha_analisis DESC;
```

**Distribución de emociones:**
```sql
SELECT
  emocion_predominante,
  COUNT(*) as total
FROM analisis_sentimiento
WHERE paciente_id = 'uuid-del-paciente'
GROUP BY emocion_predominante
ORDER BY total DESC;
```

**Ver alertas críticas:**
```sql
SELECT
  d.fecha_entrada,
  d.texto_entrada,
  a.alertas
FROM analisis_sentimiento a
JOIN diario_emocional d ON d.id = a.diario_emocional_id
WHERE a.alertas::text LIKE '%critical%'
ORDER BY d.fecha_entrada DESC;
```

### Configurar reintento automático

Si quieres que el sistema reintente analizar entradas con error:

```typescript
// En backend: services/diarioEmocional.service.ts

// Agregar método:
static async retryFailedAnalysis() {
  const failedEntries = await this.repo.find({
    where: { estado_analisis: "error" }
  });

  for (const entry of failedEntries) {
    await AnalisisSentimientoService.analizarEntrada(entry.id);
  }
}
```

### Logs del sistema

**Microservicio Python:**
```
INFO:     Analysis complete - Sentiment: positivo (confidence: 0.85)
```

**Backend Node.js:**
```
Analizando entrada abc-123...
✅ Análisis completado para entrada abc-123
```

**Ver errores:**
```
Error analizando entrada abc-123: Connection refused
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Paciente escribe diario todos los días

✅ **Automático**: Cada entrada se analiza al guardar
✅ **Sin acción adicional**: El psicólogo ve el análisis actualizado

### Caso 2: Paciente escribe offline y luego vuelve online

1. Paciente escribe 3 entradas sin internet (quedan pendientes)
2. Paciente recupera conexión
3. Al escribir la 4ta entrada (con internet):
   - Se analizan las 3 pendientes anteriores
   - Se analiza la 4ta actual
   - Total: 4 análisis procesados

### Caso 3: Psicólogo quiere ver evolución de un mes

1. Psicólogo abre tab "Análisis de Sentimientos"
2. Selecciona "Últimos 30 días" en el dropdown
3. Ve todas las métricas agregadas del mes

### Caso 4: Sistema detecta alerta crítica

1. Paciente escribe entrada con palabras de alto riesgo
2. Sistema genera alerta automáticamente
3. Psicólogo ve la alerta destacada en el tab
4. Psicólogo puede revisar la entrada original para contexto

---

## 🐛 Troubleshooting

### El análisis no se está procesando

**Verificar:**
1. ¿Microservicio Python está corriendo? → `http://localhost:8000/health`
2. ¿Backend tiene la URL correcta? → Verificar `.env`
3. ¿Hay entradas pendientes? → Verificar en base de datos

**Solución manual:**
```http
POST /api/analisis/:pacienteId/procesar-pendientes
```

### El tab muestra "No hay datos"

**Posibles causas:**
1. No hay entradas del diario para ese paciente
2. Las entradas aún están pendientes de análisis
3. El período seleccionado no tiene datos

**Solución:**
- Cambiar el período (7 días → 30 días)
- Procesar entradas pendientes manualmente

### Las alertas no aparecen

**Verificar:**
- El texto tiene que tener palabras clave específicas
- El sentimiento debe ser negativo con alta confianza
- Ver los logs del microservicio Python

---

## 📊 Métricas de Performance

**Tiempo de análisis:**
- 1 entrada: ~2-5 segundos
- 10 entradas pendientes: ~20-50 segundos
- Depende de: longitud del texto, carga del servidor

**Uso de memoria:**
- Microservicio Python: ~1-2 GB (modelo cargado en RAM)
- Backend Node.js: ~100-200 MB
- Base de datos: ~1 KB por análisis

---

## 🔐 Consideraciones de Seguridad

1. **Solo el psicólogo asignado** puede ver el análisis del paciente
2. **El paciente NO ve** su propio análisis (solo escribe)
3. **Las alertas críticas** se registran pero NO se muestran al paciente
4. **Los textos originales** NO se envían al psicólogo, solo el análisis

---

## 📚 Recursos Adicionales

- **INSTALACION.md** - Cómo instalar todo
- **API.md** - Documentación completa de la API
- **ARQUITECTURA_ANALISIS.md** - Diagrama y arquitectura técnica
