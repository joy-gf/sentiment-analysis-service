# ✅ Integración Frontend Completada - Análisis de Sentimientos

## 📝 Resumen

La integración del sistema de análisis de sentimientos con el frontend ha sido completada. El tab de "Análisis de Sentimientos" ahora obtiene datos reales del backend en lugar de usar datos simulados.

## 🔧 Cambios Realizados

### 1. **Hook personalizado para análisis de sentimientos**

**Archivo creado:** `D:\Projects\Personal\proyecto-de-grado\src\features\patients\hooks\useAnalisisSentimiento.ts`

**Funcionalidad:**
- Obtiene análisis agregado del backend mediante `/api/analisis/:pacienteId?periodo=X`
- Maneja estados de carga y error
- Permite cambiar el período de análisis (7, 14, 30 días)
- Proporciona función `refresh()` para recargar datos

**Ejemplo de uso:**
```typescript
const { analisis, loading, error, refresh } = useAnalisisSentimiento(pacienteId, 7);
```

### 2. **Actualización del AnalisisSentimientoTab**

**Archivo modificado:** `D:\Projects\Personal\proyecto-de-grado\src\features\patients\components\tabs\AnalisisSentimientoTab.tsx`

**Cambios implementados:**
- ✅ Reemplazado todos los datos mock con datos reales del backend
- ✅ Agregado manejo de estados de carga (CircularProgress)
- ✅ Agregado manejo de errores (Alert)
- ✅ Agregado manejo de datos vacíos
- ✅ Implementado mapeo de emociones a emojis (EMOTION_EMOJI_MAP)
- ✅ Implementado detección de sentimiento para palabras clave
- ✅ Cambiado selector de período de string a número (7, 30, 90 días)
- ✅ Integrado alertas e insights desde el backend
- ✅ Integrado distribución de emociones desde el backend
- ✅ Integrado evolución temporal desde el backend
- ✅ Integrado palabras clave desde el backend

## 🎨 Características Implementadas

### Estados de UI

1. **Loading State**
   ```
   Muestra CircularProgress mientras carga datos del backend
   ```

2. **Error State**
   ```
   Muestra Alert con mensaje de error si falla la petición
   ```

3. **Empty State**
   ```
   Muestra mensaje cuando no hay entradas del diario para analizar
   ```

4. **Data State**
   ```
   Muestra todos los componentes visuales con datos reales
   ```

### Mapeo de Datos

**Sentimientos (backend → frontend):**
- `esperanzador` → Color verde (#4CAF50) → "Esperanzador"
- `desafiante` → Color rojo (#F44336) → "Desafiante"
- `equilibrado` → Color naranja (#FF9800) → "Equilibrado"

**Emociones → Emojis:**
```typescript
Ansioso → 😰
Tranquilo → 😌
Feliz → 😊
Estresado → 😫
Motivado → 🤩
Triste → 😢
Enojado → 😠
Frustrado → 😤
Esperanzado → 🙏
Cansado → 😴
Neutral → 😐
```

**Palabras Clave - Detección de Sentimiento:**
- Palabras positivas: familia, alegría, esperanza, gratitud, feliz, amor, logro → Color verde
- Palabras negativas: trabajo, preocupación, estrés, ansiedad, miedo, tristeza → Color rojo
- Palabras neutrales: todo lo demás → Color naranja

## 🧪 Próximos Pasos para Testing

### Paso 1: Iniciar Microservicio Python

```bash
cd D:\Projects\Personal\sentiment-analysis-service
source venv/Scripts/activate  # Git Bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verificar que funciona:**
- Abrir: http://localhost:8000
- Debería mostrar: `{"service": "Sentiment Analysis API", "version": "0.1.0", "status": "running"}`

### Paso 2: Verificar Backend tiene Variable de Entorno

**Archivo:** `D:\Projects\Personal\mdg-backend\.env`

```env
SENTIMENT_SERVICE_URL=http://localhost:8000
```

### Paso 3: Ejecutar Migraciones (si no se hizo antes)

```bash
cd D:\Projects\Personal\mdg-backend
npm run migration:run
```

**Debería crear:**
- Tabla `analisis_sentimiento`
- Campo `estado_analisis` en tabla `diario_emocional`

### Paso 4: Iniciar Backend

```bash
cd D:\Projects\Personal\mdg-backend
npm run dev
```

### Paso 5: Iniciar Frontend

```bash
cd D:\Projects\Personal\proyecto-de-grado
npm run dev
```

## 🎯 Flujo de Testing Completo

### 1. Como Paciente - Escribir Entrada de Diario

1. Iniciar sesión como paciente
2. Ir a **"Mis Tareas"** → **"Diario Emocional"**
3. Seleccionar emoji
4. Escribir texto (ejemplo: "Hoy me siento muy ansioso por el trabajo. Tengo miedo de no cumplir con los plazos.")
5. Hacer clic en **"Guardar Entrada"**
6. **Esperar 2-5 segundos** (análisis en background)

**Qué sucede:**
- Backend guarda entrada con `estado_analisis = "pendiente"`
- Backend llama async a microservicio Python
- Python analiza texto y devuelve: sentimiento, emoción, keywords, alertas
- Backend guarda análisis en tabla `analisis_sentimiento`
- Backend marca entrada como `estado_analisis = "analizado"`

### 2. Como Psicólogo - Ver Análisis

1. Iniciar sesión como psicólogo/administrador
2. Ir a **"Pacientes"**
3. Seleccionar el paciente que escribió la entrada
4. Hacer clic en tab **"Análisis de Sentimientos"**

**Qué deberías ver:**
- ✅ **Alertas Detectadas**: Si hay palabras de alto riesgo
- ✅ **Total de Entradas**: Número de entradas analizadas
- ✅ **Sentimiento General**: Esperanzador/Desafiante/Equilibrado con score
- ✅ **Emoción Predominante**: Con emoji (ej: Ansioso 😰)
- ✅ **Tendencia**: Mejorando/Empeorando/Estable
- ✅ **Distribución de Emociones**: Gráfico de barras
- ✅ **Evolución Temporal**: Timeline con barras positivas/negativas
- ✅ **Palabras Clave**: Nube de palabras con colores según sentimiento
- ✅ **Insights Clave**: Observaciones automáticas

### 3. Cambiar Período de Análisis

1. En el tab de Análisis de Sentimientos
2. Cambiar el dropdown de "Últimos 7 días" (predeterminado) a "Últimos 14 días" o "Últimos 30 días"
3. Los datos se recargan automáticamente

## 🔍 Verificación de Datos en Base de Datos

### Ver entradas del diario:

```sql
SELECT
  id,
  fecha_entrada,
  emocion_seleccionada,
  estado_analisis
FROM diario_emocional
WHERE paciente_id = 'uuid-del-paciente'
ORDER BY fecha_entrada DESC;
```

### Ver análisis guardados:

```sql
SELECT
  fecha_analisis,
  sentimiento_general,
  emocion_predominante,
  confianza,
  palabras_clave,
  alertas
FROM analisis_sentimiento
WHERE paciente_id = 'uuid-del-paciente'
ORDER BY fecha_analisis DESC;
```

### Ver entradas pendientes de análisis:

```sql
SELECT
  id,
  fecha_entrada,
  estado_analisis
FROM diario_emocional
WHERE estado_analisis = 'pendiente'
ORDER BY fecha_entrada DESC;
```

## 🐛 Troubleshooting

### El tab muestra "No hay entradas del diario emocional para analizar"

**Causas posibles:**
1. El paciente no ha escrito ninguna entrada
2. Las entradas están pendientes de análisis
3. El período seleccionado no tiene datos

**Solución:**
- Verificar que el paciente tenga entradas en la base de datos
- Forzar análisis de pendientes: `POST /api/analisis/:pacienteId/procesar-pendientes`

### El tab muestra error de conexión

**Causas posibles:**
1. El microservicio Python no está corriendo
2. El backend no tiene la variable SENTIMENT_SERVICE_URL correcta
3. El backend no está corriendo

**Solución:**
1. Verificar que http://localhost:8000/health responda
2. Verificar .env del backend
3. Reiniciar backend

### Los datos no se actualizan al cambiar el período

**Solución:**
- Hacer refresh de la página
- Verificar la consola del navegador por errores

### Las palabras clave no tienen el color correcto

**Nota:** El sistema usa heurísticas simples para asignar colores. Palabras ambiguas pueden aparecer como neutrales (naranja). Esto es normal y se puede mejorar con un modelo más avanzado en el futuro.

## 📊 Ejemplo de Respuesta del Backend

```json
{
  "total_entradas": 5,
  "sentimiento_promedio": -0.35,
  "distribucion_emociones": {
    "Ansioso": 3,
    "Tranquilo": 1,
    "Feliz": 1
  },
  "palabras_clave": [
    {"word": "trabajo", "frequency": 8},
    {"word": "miedo", "frequency": 5},
    {"word": "familia", "frequency": 3}
  ],
  "alertas": [
    {
      "type": "warning",
      "text": "Se detecta alta frecuencia de entradas con ansiedad (60% de las entradas)"
    }
  ],
  "evolucion_temporal": [
    {
      "fecha": "2026-01-25",
      "sentimiento": "desafiante",
      "score": -0.65,
      "emocion": "Ansioso",
      "confianza": 0.85
    },
    {
      "fecha": "2026-01-24",
      "sentimiento": "equilibrado",
      "score": 0.15,
      "emocion": "Tranquilo",
      "confianza": 0.72
    }
  ]
}
```

## ✨ Mejoras Futuras Posibles

1. **Exportar análisis como PDF** para compartir con el paciente
2. **Comparación entre períodos** (ej: comparar últimos 30 días vs 30 días anteriores)
3. **Alertas en tiempo real** cuando se detecte riesgo crítico
4. **Gráficos más avanzados** con bibliotecas como Chart.js o Recharts
5. **Análisis de temas** mediante topic modeling
6. **Detección de patrones temporales** (ej: ansiedad los lunes)
7. **Recomendaciones automáticas** basadas en el análisis

## 📚 Documentación Relacionada

- `INSTALACION.md` - Guía de instalación paso a paso
- `USO.md` - Guía de uso para usuarios, psicólogos y desarrolladores
- `ARQUITECTURA_ANALISIS.md` - Arquitectura técnica del sistema

---

## ✅ Checklist de Integración

- [x] Hook useAnalisisSentimiento creado
- [x] AnalisisSentimientoTab actualizado con datos reales
- [x] Estados de loading, error y vacío implementados
- [x] Mapeo de sentimientos implementado
- [x] Mapeo de emociones a emojis implementado
- [x] Detección de sentimiento para palabras clave implementada
- [x] Selector de período funcional
- [x] Integración con backend endpoints completada
- [ ] Testing end-to-end realizado
- [ ] Validación con datos reales de pacientes
- [ ] Documentación de usuario actualizada

**Estado:** ✅ **INTEGRACIÓN FRONTEND COMPLETA**

**Próximo paso:** Iniciar servicios y realizar testing end-to-end
