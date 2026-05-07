---
title: Sentiment Analysis Service
sdk: docker
app_port: 8000
pinned: false
short_description: API de análisis de sentimiento en español (RoBERTuito)
models:
  - pysentimiento/robertuito-sentiment-analysis
---

# Servicio de Análisis de Sentimiento

Servicio que analiza si un texto es positivo, negativo o neutral. Se usa para el Diario Emocional.

## ¿Qué hace?

Cuando le envías un texto como "Hoy me siento muy feliz", te responde:
- Es positivo/negativo/neutral
- Qué tan seguro está (confianza)
- Puntajes de cada sentimiento

## Instalación (Windows)

1. **Abrir terminal en la carpeta del proyecto:**
```bash
cd D:/Projects/Personal/sentiment-analysis-service
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
```

3. **Activar el entorno:**
```bash
source venv/Scripts/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

5. **Copiar archivo de configuración:**
```bash
cp .env.example .env
```

## Ejecutar

```bash
python app/main.py
```

El servicio se inicia en: http://localhost:8000

La primera vez descargará el modelo (puede tardar unos minutos).

## Probar que funciona

Abre en tu navegador: http://localhost:8000/docs

Ahí puedes probar el endpoint `/analyze` directamente.

O usa este comando:
```bash
curl -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d "{\"text\": \"Me siento muy feliz hoy\"}"
```

## Respuesta ejemplo

```json
{
  "sentimiento_general": "positivo",
  "score_positivo": 0.92,
  "score_negativo": 0.05,
  "score_neutral": 0.03,
  "confianza": 0.92,
  "modelo_usado": "pysentimiento/robertuito-sentiment-analysis"
}
```

## Conectar con tu backend Express

```typescript
const response = await axios.post("http://localhost:8000/analyze", {
  text: textoDelDiario,
  diario_id: idDelDiario
});

const analisis = response.data;
// Guarda 'analisis' en tu base de datos
```

## Archivos importantes

- `app/main.py` - Aplicación principal
- `app/analyzer.py` - Lógica del análisis de sentimiento
- `app/models.py` - Estructura de los datos
- `app/config.py` - Configuración
- `requirements.txt` - Librerías necesarias
- `.env` - Configuración (puerto, etc)

## Notas

- Es 100% gratuito
- Funciona en Windows sin problemas
- Usa CPU (no necesitas GPU)
- El modelo es especializado en español
- Ver `TODO.md` para funcionalidades futuras
