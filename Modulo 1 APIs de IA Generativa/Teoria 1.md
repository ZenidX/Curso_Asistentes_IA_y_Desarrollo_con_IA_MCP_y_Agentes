# Módulo 1: APIs de IA Generativa

## Información del Módulo

| Campo | Detalle |
|-------|---------|
| **Duración estimada** | 3-4 horas |
| **Nivel** | Principiante |
| **Prerrequisitos** | Conocimientos básicos de programación, Python instalado |
| **Herramientas necesarias** | Python 3.8+, pip, editor de código |

---

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Entender qué son las APIs de IA Generativa y para qué sirven
- [ ] Obtener API Keys gratuitas de los principales proveedores
- [ ] Comprender los conceptos de tokens, prompts y parámetros
- [ ] Realizar llamadas básicas a las APIs de OpenAI, Anthropic, Google y Ollama
- [ ] Elegir el proveedor adecuado según el caso de uso
- [ ] Implementar streaming y manejo de errores

---

## Continuación del Proyecto: TaskFlow

A lo largo de los módulos, construiremos **TaskFlow**, una aplicación de gestión de tareas. En este módulo, sentaremos las bases:

```
TaskFlow/
├── config/
│   └── config.yaml       ← Configuración de APIs
├── scripts/
│   ├── 01_basico/        ← Primeros pasos con cada API
│   ├── 02_intermedio/    ← Streaming y comparativas
│   └── 03_avanzado/      ← Function calling, embeddings
└── requirements.txt
```

**Objetivo del módulo**: Conectar TaskFlow con múltiples proveedores de IA para generar descripciones de tareas, sugerir prioridades y responder consultas.

---

## 1. Introducción a las APIs de IA Generativa

**Tiempo estimado: 20 minutos**

### 1.1 ¿Qué son las APIs de IA Generativa?

Las APIs de IA Generativa son interfaces que permiten a los desarrolladores integrar modelos de lenguaje avanzados (LLMs) en sus aplicaciones. Estos modelos pueden:

- **Generar texto**: Responder preguntas, escribir artículos, código, emails
- **Analizar contenido**: Resumir documentos, extraer información, clasificar texto
- **Transformar datos**: Traducir idiomas, reformatear información, convertir formatos
- **Razonar**: Resolver problemas lógicos, matemáticos, de programación

### 💡 Concepto Clave

> **API (Application Programming Interface)**: Es un "contrato" entre tu código y un servicio externo. Envías datos en un formato específico, y recibes una respuesta estructurada. No necesitas saber cómo funciona el modelo internamente, solo cómo comunicarte con él.

### 1.2 Principales Proveedores

| Proveedor | Modelos Principales | Ventajas | Ideal para |
|-----------|---------------------|----------|------------|
| **OpenAI** | GPT-4o, GPT-4o-mini | Ecosistema maduro, documentación extensa | Producción, aplicaciones comerciales |
| **Anthropic** | Claude 3.5, Claude 3 Opus/Sonnet/Haiku | Contexto largo (200K), seguridad | Análisis de documentos largos |
| **Google** | Gemini 1.5 Pro/Flash | Tier gratuito generoso, multimodal | Aprendizaje, prototipos |
| **Ollama** | Llama 3.2, Mistral, CodeLlama | 100% local, privacidad, sin costes | Desarrollo offline, datos sensibles |

### 📍 Checkpoint 1

Antes de continuar, responde:
- [ ] ¿Qué proveedor usarías para analizar un libro de 500 páginas?
- [ ] ¿Cuál es mejor para desarrollo sin conexión a internet?

<details>
<summary>Ver respuestas</summary>

- Libro de 500 páginas → **Anthropic Claude** (200K tokens) o **Google Gemini** (1M tokens)
- Desarrollo offline → **Ollama** (modelos locales)

</details>

---

## 2. Cómo obtener API Keys (GRATIS)

**Tiempo estimado: 30 minutos**

### 2.1 OpenAI

**Créditos gratuitos**: $5 para nuevos usuarios

**Pasos**:
1. Regístrate en [platform.openai.com](https://platform.openai.com/)
2. Ve a **API Keys** en el menú lateral
3. Haz clic en **"Create new secret key"**
4. Copia la key (solo se muestra una vez)

```
Formato: sk-proj-xxxxxxxxxxxxxxxxxxxx
```

**Precios aproximados** (después del crédito gratuito):
| Modelo | Input | Output |
|--------|-------|--------|
| GPT-4o-mini | $0.15 / 1M tokens | $0.60 / 1M tokens |
| GPT-4o | $2.50 / 1M tokens | $10 / 1M tokens |

### ⚠️ Error Común

> **No guardar la key**: OpenAI solo muestra la API key una vez. Si la pierdes, tendrás que generar una nueva. Guárdala inmediatamente en un lugar seguro.

---

### 2.2 Anthropic (Claude)

**Créditos gratuitos**: Disponibles al registrarse

**Pasos**:
1. Regístrate en [console.anthropic.com](https://console.anthropic.com/)
2. Ve a **Settings → API Keys**
3. Haz clic en **"Create Key"**
4. Copia la key

```
Formato: sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
```

**Precios aproximados**:
| Modelo | Input | Output |
|--------|-------|--------|
| Claude 3 Haiku | $0.25 / 1M tokens | $1.25 / 1M tokens |
| Claude 3.5 Sonnet | $3 / 1M tokens | $15 / 1M tokens |

---

### 2.3 Google AI Studio (Gemini)

**Tier gratuito**: MUY GENEROSO - 60 requests/minuto sin coste

**Pasos**:
1. Ve a [aistudio.google.com](https://aistudio.google.com/)
2. Haz clic en **"Get API Key"**
3. Selecciona o crea un proyecto de Google Cloud
4. Copia la key generada

```
Formato: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Límites gratuitos**:
- 60 requests por minuto
- 1 millón de tokens por minuto
- Sin límite diario

### 💡 Concepto Clave

> **Por qué Gemini es ideal para aprender**: Su tier gratuito es el más generoso del mercado. Puedes hacer miles de llamadas al día sin coste, perfecto para experimentar y aprender.

---

### 2.4 Ollama (100% GRATIS)

Ollama permite ejecutar LLMs localmente, sin necesidad de API key ni conexión a internet.

**Instalación**:

```bash
# Windows (PowerShell como administrador)
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

**Descargar un modelo**:

```bash
# Modelo ligero (3B parámetros, ~2GB)
ollama pull llama3.2

# Modelo para código
ollama pull codellama

# Ver modelos disponibles
ollama list
```

**Verificar instalación**:

```bash
ollama run llama3.2 "Hola, ¿cómo estás?"
```

### 🎯 Práctica Guiada 1: Configurar tu Entorno

1. Elige al menos 2 proveedores
2. Obtén las API keys siguiendo los pasos anteriores
3. Crea el archivo de configuración:

```bash
cd TaskFlow
cp config/config.example.yaml config/config.yaml
```

4. Añade tus keys al archivo `config/config.yaml`
5. Verifica que no esté en git: `cat .gitignore | grep config.yaml`

**Criterios de éxito**:
- [ ] Tienes al menos 2 API keys
- [ ] El archivo config.yaml tiene tus keys
- [ ] El archivo NO está en control de versiones

---

## 3. Conceptos Fundamentales

**Tiempo estimado: 45 minutos**

### 3.1 Tokens

Los tokens son las unidades básicas que procesan los LLMs. No son exactamente palabras ni caracteres.

**Regla aproximada**:
- Inglés: 1 token ≈ 4 caracteres ≈ 0.75 palabras
- Español: 1 token ≈ 3-4 caracteres (varía más por acentos)

**Ejemplos de tokenización**:

```
"Hola mundo"              → ["Hola", " mundo"]           → 2 tokens
"Inteligencia artificial" → ["Int", "elig", "encia", " artificial"] → 4 tokens
"12345"                   → ["123", "45"]                → 2 tokens
```

### 💡 Concepto Clave

> **¿Por qué importan los tokens?**
> 1. **Coste**: Se paga por token procesado
> 2. **Límites**: Los modelos tienen contexto máximo en tokens
> 3. **Velocidad**: Más tokens = respuesta más lenta

**Regla práctica**: 100 tokens ≈ 75 palabras ≈ 1/4 de página A4

---

### 3.2 Prompts y Completions

```
┌─────────────────────────────────────────┐
│  PROMPT (Input)                         │
│  "Explica qué es Python en 2 frases"    │
├─────────────────────────────────────────┤
│            ↓ Modelo LLM ↓               │
├─────────────────────────────────────────┤
│  COMPLETION (Output)                    │
│  "Python es un lenguaje de programación │
│   interpretado y de alto nivel..."      │
└─────────────────────────────────────────┘
```

**Tipos de prompts**:

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **System** | Define el comportamiento del modelo | "Eres un asistente experto en Python" |
| **User** | El mensaje del usuario | "¿Cómo ordeno una lista?" |
| **Assistant** | Respuestas previas (para contexto) | "Puedes usar sort() o sorted()..." |

---

### 3.3 Parámetros Principales

#### Temperature (0.0 - 2.0)

Controla la aleatoriedad/creatividad de las respuestas.

| Valor | Comportamiento | Uso recomendado |
|-------|----------------|-----------------|
| 0.0 | Determinista, siempre igual | Código, datos estructurados |
| 0.3-0.5 | Consistente con ligera variación | Resúmenes, traducciones |
| 0.7 | Equilibrado (default) | Conversación general |
| 1.0-1.5 | Creativo | Escritura creativa, brainstorming |
| 2.0 | Muy aleatorio | Experimentación |

```python
# Ejemplo: Mismo prompt, diferente temperature
prompt = "Escribe un título para un artículo sobre IA"

# temperature=0: "Inteligencia Artificial: Una Guía Completa"
# temperature=0.7: "El Futuro es Ahora: Cómo la IA Está Cambiando Todo"
# temperature=1.5: "¡Robots Pensantes! La Revolución Silenciosa"
```

#### Max Tokens

Límite máximo de tokens en la respuesta.

```python
max_tokens=50   # Respuestas cortas (1-2 oraciones)
max_tokens=500  # Respuestas medianas (1-2 párrafos)
max_tokens=4096 # Respuestas largas (artículos)
```

### ⚠️ Error Común

> **Respuesta cortada abruptamente**: Si el modelo alcanza `max_tokens`, la respuesta se corta sin aviso. Aumenta el límite si ves respuestas incompletas.

#### Top P (Nucleus Sampling)

Alternativa a temperature. Selecciona tokens cuya probabilidad acumulada suma P.

```python
top_p=0.1  # Solo considera el 10% más probable → Muy conservador
top_p=0.9  # Considera el 90% más probable → Más variado
top_p=1.0  # Considera todos los tokens (default)
```

**Recomendación**: Usa `temperature` O `top_p`, no ambos a la vez.

---

### 3.4 Ventana de Contexto

Cada modelo tiene un límite de tokens totales (input + output).

| Modelo | Contexto Máximo | Equivalente |
|--------|-----------------|-------------|
| GPT-4o | 128K tokens | ~400 páginas |
| GPT-4o-mini | 128K tokens | ~400 páginas |
| Claude 3.5 Sonnet | 200K tokens | ~600 páginas |
| Gemini 1.5 Pro | 1M tokens | ~3,000 páginas |
| Llama 3.2 (Ollama) | 128K tokens | ~400 páginas |

### 📍 Checkpoint 2

Responde:
- [ ] ¿Qué temperature usarías para generar código?
- [ ] Si una respuesta se corta a la mitad, ¿qué parámetro debes ajustar?
- [ ] ¿Cuántas páginas aproximadamente caben en 100K tokens?

<details>
<summary>Ver respuestas</summary>

- Código → **temperature=0** (determinista, consistente)
- Respuesta cortada → Aumentar **max_tokens**
- 100K tokens → Aproximadamente **300 páginas**

</details>

---

## 4. Estructura de las APIs

**Tiempo estimado: 40 minutos**

### 4.1 Autenticación

Todas las APIs (excepto Ollama) requieren autenticación via HTTP headers.

```python
# OpenAI
headers = {"Authorization": "Bearer sk-..."}

# Anthropic
headers = {"x-api-key": "sk-ant-...", "anthropic-version": "2023-06-01"}

# Google
# Se pasa como parámetro: ?key=AIza...
```

---

### 4.2 Endpoint Principal: Chat Completions

#### OpenAI

`POST https://api.openai.com/v1/chat/completions`

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "¿Qué es Python?"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

#### Anthropic

`POST https://api.anthropic.com/v1/messages`

```json
{
  "model": "claude-3-haiku-20240307",
  "max_tokens": 500,
  "system": "Eres un asistente útil.",
  "messages": [
    {"role": "user", "content": "¿Qué es Python?"}
  ]
}
```

#### Google

`POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

```json
{
  "contents": [
    {"role": "user", "parts": [{"text": "¿Qué es Python?"}]}
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 500
  }
}
```

#### Ollama

`POST http://localhost:11434/api/chat`

```json
{
  "model": "llama3.2",
  "messages": [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "¿Qué es Python?"}
  ],
  "stream": false
}
```

---

### 4.3 Formato de Respuesta

**Estructura común** (simplificada):

```json
{
  "id": "chatcmpl-xxx",
  "model": "gpt-4o-mini",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Python es un lenguaje de programación..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  }
}
```

**Campos importantes**:

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `content` | La respuesta generada | Mostrar al usuario |
| `finish_reason` | Por qué terminó | `stop` (normal), `length` (cortado), `content_filter` (bloqueado) |
| `usage` | Tokens consumidos | Calcular costes, monitorear uso |

---

### 🎯 Práctica Guiada 2: Tu Primera Llamada a la API

```python
# scripts/01_basico/primera_llamada.py
import os
from openai import OpenAI

# Cargar API key desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Hacer la llamada
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente experto en Python."},
        {"role": "user", "content": "¿Cómo ordeno una lista en Python?"}
    ],
    temperature=0.7,
    max_tokens=500
)

# Extraer y mostrar la respuesta
print(response.choices[0].message.content)
print(f"\nTokens usados: {response.usage.total_tokens}")
```

**Pasos**:
1. Crea el archivo `scripts/01_basico/primera_llamada.py`
2. Configura la variable de entorno: `export OPENAI_API_KEY="tu-key"`
3. Ejecuta: `python scripts/01_basico/primera_llamada.py`

**Criterios de éxito**:
- [ ] El script se ejecuta sin errores
- [ ] Recibes una respuesta del modelo
- [ ] Puedes ver los tokens consumidos

---

## 5. Comparativa de Proveedores

**Tiempo estimado: 20 minutos**

### 5.1 Cuándo usar cada uno

| Necesidad | Recomendación | Razón |
|-----------|---------------|-------|
| Aprender/Experimentar gratis | **Google Gemini** | Tier gratuito más generoso |
| Privacidad total / Offline | **Ollama** | 100% local |
| Máxima calidad | **Claude 3.5 Sonnet** o **GPT-4o** | Mejores resultados |
| Coste mínimo + buena calidad | **GPT-4o-mini** o **Claude 3 Haiku** | Balance precio/rendimiento |
| Contexto muy largo | **Gemini 1.5 Pro** | 1M tokens |
| Generación de código | **GPT-4o** o **Claude 3.5 Sonnet** | Optimizados para código |

### 5.2 Límites de Rate

| Proveedor | Tier Gratuito | Requests/minuto |
|-----------|---------------|-----------------|
| OpenAI | Limitado tras $5 | 3-500 (según tier) |
| Anthropic | Créditos iniciales | 5-50 (según tier) |
| Google | Muy generoso | 60 |
| Ollama | Ilimitado | Solo limitado por hardware |

---

### 📍 Checkpoint 3

Responde:
- [ ] ¿Qué proveedor elegirías para un proyecto sin presupuesto?
- [ ] ¿Cuál usarías para procesar documentos confidenciales de una empresa?
- [ ] ¿Qué modelo tiene el contexto más grande?

<details>
<summary>Ver respuestas</summary>

- Sin presupuesto → **Google Gemini** (tier gratuito generoso) u **Ollama** (gratis)
- Documentos confidenciales → **Ollama** (datos nunca salen de tu máquina)
- Mayor contexto → **Gemini 1.5 Pro** (1M tokens)

</details>

---

## 6. Ejercicios Prácticos

**Tiempo estimado: 60 minutos**

### Estructura de los Scripts

```
scripts/
├── 01_basico/           # Primeros pasos
│   ├── openai_basico.py
│   ├── anthropic_basico.py
│   ├── google_basico.py
│   └── ollama_basico.py
├── 02_intermedio/       # Técnicas intermedias
│   ├── comparar_modelos.py
│   ├── parametros_avanzados.py
│   └── streaming.py
└── 03_avanzado/         # Funcionalidades avanzadas
    ├── function_calling.py
    └── embeddings.py
```

### Configuración Inicial

```bash
# 1. Copia el archivo de configuración
cp config/config.example.yaml config/config.yaml

# 2. Añade tus API keys en config/config.yaml

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta tu primer script
python scripts/01_basico/openai_basico.py
```

### Progresión Recomendada

| Nivel | Script | Qué aprenderás |
|-------|--------|----------------|
| **Básico** | `openai_basico.py` | Llamada simple, extraer respuesta |
| **Básico** | `anthropic_basico.py` | Diferencias con OpenAI |
| **Básico** | `google_basico.py` | Estructura de Gemini |
| **Básico** | `ollama_basico.py` | Modelos locales |
| **Intermedio** | `comparar_modelos.py` | Mismo prompt, diferentes modelos |
| **Intermedio** | `streaming.py` | Respuestas en tiempo real |
| **Avanzado** | `function_calling.py` | LLMs que usan herramientas |
| **Avanzado** | `embeddings.py` | Búsqueda semántica |

---

### 🎯 Práctica Guiada 3: Comparar Modelos

Crea un script que envíe el mismo prompt a diferentes proveedores y compare:

```python
# scripts/02_intermedio/comparar_modelos.py
import time
from openai import OpenAI
from anthropic import Anthropic

prompt = "Explica qué es recursión en programación en 3 oraciones."

# OpenAI
start = time.time()
openai_response = # ... tu código
openai_time = time.time() - start

# Anthropic
start = time.time()
anthropic_response = # ... tu código
anthropic_time = time.time() - start

# Comparar
print("=== OpenAI ===")
print(f"Tiempo: {openai_time:.2f}s")
print(f"Respuesta: {openai_response}")

print("\n=== Anthropic ===")
print(f"Tiempo: {anthropic_time:.2f}s")
print(f"Respuesta: {anthropic_response}")
```

**Criterios de éxito**:
- [ ] El script llama a ambos proveedores
- [ ] Mide el tiempo de cada uno
- [ ] Muestra ambas respuestas para comparar

---

## 7. Troubleshooting

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `401 Unauthorized` | API key inválida o expirada | Regenerar la key |
| `429 Rate Limit` | Demasiadas peticiones | Esperar o usar otro tier |
| `400 Bad Request` | Formato incorrecto | Revisar estructura del JSON |
| `context_length_exceeded` | Prompt muy largo | Reducir tokens de entrada |

### Comandos de Diagnóstico

```bash
# Verificar que Ollama está corriendo
curl http://localhost:11434/api/version

# Probar conexión a OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Ver modelos disponibles en Ollama
ollama list
```

---

## Resumen del Módulo

### Lo que aprendiste

1. **APIs de IA Generativa**: Qué son y para qué sirven
2. **API Keys**: Cómo obtenerlas gratis de cada proveedor
3. **Tokens**: Unidades de procesamiento, cálculo de costes
4. **Parámetros**: temperature, max_tokens, top_p
5. **Estructura de APIs**: Requests y responses de cada proveedor
6. **Comparativa**: Cuándo usar cada proveedor

### Preparación para el Módulo 2

En el próximo módulo aprenderás a usar **CLIs de IA** (Claude Code, Gemini CLI, OpenCode) que te permiten:
- Interactuar con IA desde tu terminal
- Analizar y modificar código automáticamente
- Ejecutar comandos basados en lenguaje natural

**Tarea previa**: Ten al menos una API key funcionando y haber ejecutado un script básico.

---

## Recursos Adicionales

- [Documentación OpenAI](https://platform.openai.com/docs)
- [Documentación Anthropic](https://docs.anthropic.com/)
- [Documentación Google AI](https://ai.google.dev/docs)
- [Documentación Ollama](https://github.com/ollama/ollama)
- [Tokenizer Online](https://platform.openai.com/tokenizer) - Visualiza tokenización
