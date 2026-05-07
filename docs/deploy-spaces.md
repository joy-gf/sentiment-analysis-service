# Despliegue en HuggingFace Spaces (Demo / MVP)

Despliegue gratuito para la demo del proyecto de grado, ejecutando el modelo
`pysentimiento/robertuito-sentiment-analysis` directamente en el contenedor.

## Requisitos previos

- Cuenta en [huggingface.co](https://huggingface.co)
- Git instalado localmente
- Repo `sentiment-analysis-service` en local

## Por qué Spaces y no Render

| Recurso | Render free | HF Spaces free |
|---|---|---|
| RAM | 512 MB | **16 GB** |
| Disco | ~512 MB | 50 GB (no persistente) |
| Sleep | 15 min sin tráfico | 48 h sin tráfico |
| Modelo local con `transformers` | No entra (OOM) | Entra cómodo |

El modelo RoBERTuito ocupa ~440 MB en disco y ~1.5–2 GB de RAM una vez cargado.
En Render free no entra; en Spaces free sobra.

---

## Paso 1 — Crear el Space

1. Entrar a [huggingface.co/new-space](https://huggingface.co/new-space)
2. Configurar:
   - **Space name**: `sentiment-analysis-service` (o el que prefieras)
   - **License**: la que aplique (MIT recomendado para proyectos de grado)
   - **Select the Space SDK**: **Docker** → **Blank**
   - **Space hardware**: **CPU basic — Free**
   - **Visibility**: **Public**
3. Clic en **Create Space**

Esto crea un repo git en `https://huggingface.co/spaces/<tu-usuario>/sentiment-analysis-service`.

---

## Paso 2 — Obtener token de write para empujar al Space

1. En HuggingFace: **Settings → Access Tokens → New token**
2. Nombre: `spaces-deploy`, Role: **Write**
3. Copiar el token (empieza con `hf_...`)

---

## Paso 3 — Empujar el código al Space

Desde la raíz del proyecto (`sentiment-analysis-service`):

```bash
# 1. Agregar el remoto del Space
git remote add space https://<tu-usuario>:<hf_token>@huggingface.co/spaces/<tu-usuario>/sentiment-analysis-service

# 2. Empujar la rama main
git push space main
```

> Si tu rama local se llama distinto, ajusta: `git push space tu-rama:main`.

> Alternativa sin meter el token en la URL: clonar el repo del Space en otra carpeta,
> copiar los archivos y hacer commit+push usando las credenciales de git.

---

## Paso 4 — Esperar el build

1. Abrir `https://huggingface.co/spaces/<tu-usuario>/sentiment-analysis-service`
2. Pestaña **Logs → Build**: ver el `pip install` (5–10 min la primera vez por torch)
3. Pestaña **Logs → Container**: cuando aparezca `Uvicorn running on http://0.0.0.0:8000` está listo
4. La primera petición descarga el modelo del Hub (~30 s adicionales)

---

## Paso 5 — Probar

URL pública: `https://<tu-usuario>-sentiment-analysis-service.hf.space`

```bash
# Health check
curl https://<tu-usuario>-sentiment-analysis-service.hf.space/health

# Análisis básico
curl -X POST https://<tu-usuario>-sentiment-analysis-service.hf.space/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Me siento muy bien hoy"}'

# Análisis enriquecido
curl -X POST https://<tu-usuario>-sentiment-analysis-service.hf.space/analyze/enhanced \
  -H "Content-Type: application/json" \
  -d '{"text": "Me siento muy bien hoy"}'
```

Respuesta esperada del `/health`:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "pysentimiento/robertuito-sentiment-analysis"
}
```

---

## Paso 6 — Conectar con el backend

En las variables de entorno del backend:

```
SENTIMENT_SERVICE_URL=https://<tu-usuario>-sentiment-analysis-service.hf.space
```

Si el frontend hace llamadas directas, agregar la URL del frontend a `CORS_ORIGINS`
en los **Settings → Variables and secrets** del Space.

---

## Variables de entorno opcionales en el Space

Configurar en **Settings → Variables and secrets**:

| Key | Valor sugerido | Notas |
|---|---|---|
| `MODEL_NAME` | `pysentimiento/robertuito-sentiment-analysis` | Default en `config.py` |
| `CORS_ORIGINS` | `https://tu-frontend.com` | Coma-separado si hay varios |
| `HF_API_TOKEN` | _no setear_ | Si se setea, intenta usar el router de HF; el modelo de la tesis no está soportado, así que **dejar vacío** |

---

## Notas sobre el free tier

- **Sleep**: 48 h sin tráfico → próxima petición tarda ~30–60 s en despertar (rebuild + carga de modelo).
- **Para la defensa de tesis**: hacer un curl al `/health` 1–2 minutos antes de la demo para tener el Space "warm".
- **Mantenerlo activo entre clases/iteraciones**: configurar [cron-job.org](https://cron-job.org) (gratis) con un GET a `/health` cada 6 h.
- **Disco no persistente**: si el contenedor se reinicia, vuelve a descargar el modelo del Hub (rápido, mismo datacenter).

---

## Tabla de funcionamiento por entorno

| Entorno | Modo | Cómo |
|---|---|---|
| Local (desarrollo) | Modelo local con `transformers` | `pip install -r requirements-local.txt` |
| Spaces (demo / MVP) | Modelo local dentro del contenedor | Push a Space; sin `HF_API_TOKEN` |
| Producción (AWS) | Modelo local dentro del servidor | Imagen Docker en ECS/EKS |

El `analyzer.py` selecciona el modo automáticamente:
- Sin `HF_API_TOKEN` → carga local con `transformers` (camino usado en Spaces).
- Con `HF_API_TOKEN` → usa el router `router.huggingface.co/hf-inference` (requiere modelo soportado).
