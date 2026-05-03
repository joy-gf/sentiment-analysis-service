# 📦 Guía de Instalación - Microservicio de Análisis de Sentimientos

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.9 o superior** ([Descargar aquí](https://www.python.org/downloads/))
- **pip** (gestor de paquetes de Python, viene con Python)
- **PostgreSQL** (ya instalado para tu backend)
- **Node.js y npm** (ya instalado para tu backend)

### Verificar instalaciones

```bash
# Verificar Python
python --version
# O en algunos sistemas:
python3 --version

# Verificar pip
pip --version
# O:
pip3 --version
```

---

## 🐍 Instalación del Microservicio Python

### Paso 1: Navegar al directorio

```bash
cd D:\Projects\Personal\sentiment-analysis-service
```

### Paso 2: Crear entorno virtual (RECOMENDADO)

Un entorno virtual aísla las dependencias del proyecto del sistema.

**En Windows (Git Bash o CMD):**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Git Bash:
source venv/Scripts/activate
# En CMD:
venv\Scripts\activate
```

**En Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\Activate.ps1
```

**En Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

Cuando el entorno esté activado, verás `(venv)` al inicio de tu línea de comando.

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Si requirements.txt no existe o falta algo, instalar manualmente:**

```bash
# Dependencias principales
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install transformers==4.35.2
pip install torch==2.1.0
pip install python-dotenv==1.0.0

# Nota: torch puede tardar varios minutos en descargar (es un paquete grande)
```

### Paso 4: Verificar instalación

```bash
# Ver paquetes instalados
pip list

# Deberías ver: fastapi, uvicorn, transformers, torch, python-dotenv
```

### Paso 5: Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# En la carpeta sentiment-analysis-service, crear .env
touch .env
```

**Contenido del archivo `.env`:**

```env
# Modelo de análisis de sentimientos
MODEL_NAME=pysentimiento/robertuito-sentiment-analysis

# Dispositivo (cpu o cuda para GPU)
DEVICE=cpu

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# CORS - orígenes permitidos (tu frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174
```

### Paso 6: Primera ejecución (descarga del modelo)

La primera vez que ejecutes el servicio, descargará el modelo de ML (~500MB).

```bash
# Iniciar el servicio
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**
```
INFO:     Will watch for changes in these directories: ['D:\\Projects\\Personal\\sentiment-analysis-service']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Loading model: pysentimiento/robertuito-sentiment-analysis
Downloading model... (esto puede tardar varios minutos)
INFO:     Model loaded successfully on device: cpu
INFO:     Service ready!
INFO:     Application startup complete.
```

### Paso 7: Verificar que funciona

Abre tu navegador en: **http://localhost:8000**

Deberías ver:
```json
{
  "service": "Sentiment Analysis API",
  "version": "0.1.0",
  "status": "running"
}
```

**Probar endpoint de salud:**
http://localhost:8000/health

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "pysentimiento/robertuito-sentiment-analysis"
}
```

---

## 🔧 Instalación del Backend (Node.js)

### Paso 1: Navegar al backend

```bash
cd D:\Projects\Personal\mdg-backend
```

### Paso 2: Instalar dependencia de axios

```bash
npm install axios
```

### Paso 3: Ejecutar migraciones

```bash
npm run migration:run
```

**Salida esperada:**
```
📝 Creando tabla analisis_sentimiento...
✅ Tabla analisis_sentimiento creada exitosamente
📝 Agregando campo estado_analisis a diario_emocional...
✅ Campo agregado exitosamente
```

### Paso 4: Configurar variables de entorno

Editar archivo `.env` del backend, agregar:

```env
# URL del microservicio de análisis
SENTIMENT_SERVICE_URL=http://localhost:8000
```

### Paso 5: Reiniciar el backend

```bash
npm run dev
```

---

## 🚀 Iniciar todo el sistema

### Orden recomendado:

1. **Base de datos (PostgreSQL)** - Debe estar corriendo
2. **Microservicio Python** - Terminal 1
3. **Backend Node.js** - Terminal 2
4. **Frontend React** - Terminal 3

### Terminal 1: Microservicio Python

```bash
cd D:\Projects\Personal\sentiment-analysis-service
source venv/Scripts/activate  # Activar entorno virtual
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Backend Node.js

```bash
cd D:\Projects\Personal\mdg-backend
npm run dev
```

### Terminal 3: Frontend React

```bash
cd D:\Projects\Personal\proyecto-de-grado
npm run dev
```

---

## 🧪 Probar el sistema

### 1. Probar microservicio directamente

**Usando curl:**
```bash
curl -X POST "http://localhost:8000/analyze/enhanced" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hoy me siento muy feliz porque logré terminar mi proyecto"}'
```

**Usando Postman o similar:**
- URL: `POST http://localhost:8000/analyze/enhanced`
- Body (JSON):
```json
{
  "text": "Hoy me siento muy feliz porque logré terminar mi proyecto"
}
```

**Respuesta esperada:**
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
    {"word": "proyecto", "frequency": 1},
    {"word": "logré", "frequency": 1},
    {"word": "terminar", "frequency": 1}
  ],
  "alertas": []
}
```

### 2. Probar desde el frontend

1. Inicia sesión como paciente
2. Ve a "Mis Tareas" → "Diario Emocional"
3. Escribe una entrada
4. Haz clic en "Guardar Entrada"
5. Espera unos segundos
6. Ve al tab de "Análisis de Sentimientos" (como psicólogo viendo al paciente)

---

## ❌ Problemas Comunes

### Error: "python no reconocido"

**Solución:**
- Instala Python desde python.org
- Asegúrate de marcar "Add Python to PATH" durante la instalación
- Reinicia tu terminal

### Error: "pip no reconocido"

**Solución:**
```bash
python -m pip --version
# Usar: python -m pip install -r requirements.txt
```

### Error: "Cannot find module transformers"

**Solución:**
```bash
# Asegúrate de tener el entorno virtual activado
source venv/Scripts/activate
pip install transformers torch
```

### Error: "Address already in use" (puerto 8000 ocupado)

**Solución:**
```bash
# Cambiar puerto en el comando
python -m uvicorn app.main:app --reload --port 8001

# Y actualizar en backend .env:
SENTIMENT_SERVICE_URL=http://localhost:8001
```

### Error: "Connection refused" desde backend

**Solución:**
- Verifica que el microservicio Python esté corriendo
- Verifica que el puerto sea correcto (8000)
- Verifica la variable SENTIMENT_SERVICE_URL en backend

### Modelo tarda mucho en descargar

**Solución:**
- Es normal, el modelo pesa ~500MB
- Se descarga solo la primera vez
- Ten paciencia, puede tardar 5-15 minutos dependiendo de tu conexión

### Error: "torch not found" o problemas con torch

**Solución (Windows):**
```bash
# Instalar versión específica de torch
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

---

## 🔄 Actualizar el sistema

### Si haces cambios en el código Python:

El servidor se reinicia automáticamente (modo `--reload`)

### Si haces cambios en el backend Node.js:

El servidor se reinicia automáticamente (modo `dev`)

### Si cambias las migraciones:

```bash
cd D:\Projects\Personal\mdg-backend
npm run migration:run
```

---

## 🛑 Detener los servicios

Para detener cualquier servicio, presiona:
```
Ctrl + C
```

Para desactivar el entorno virtual de Python:
```bash
deactivate
```

---

## 📚 Próximos pasos

Una vez instalado todo, consulta:
- `USO.md` - Guía de uso del sistema
- `API.md` - Documentación de la API
- `ARQUITECTURA_ANALISIS.md` - Arquitectura técnica
