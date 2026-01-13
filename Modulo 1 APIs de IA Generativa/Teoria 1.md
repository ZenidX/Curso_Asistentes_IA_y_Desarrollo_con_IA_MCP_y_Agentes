# Módulo 1: APIs de IA Generativa

## Índice
1. [Introducción](#1-introducción)
2. [Cómo obtener API Keys (GRATIS)](#2-cómo-obtener-api-keys-gratis)
3. [Conceptos Fundamentales](#3-conceptos-fundamentales)
4. [Estructura de las APIs](#4-estructura-de-las-apis)
5. [Comparativa de Proveedores](#5-comparativa-de-proveedores)
6. [Ejercicios Prácticos](#6-ejercicios-prácticos)

---

## 1. Introducción

### ¿Qué son las APIs de IA Generativa?

Las APIs de IA Generativa son interfaces que permiten a los desarrolladores integrar modelos de lenguaje avanzados (LLMs) en sus aplicaciones. Estos modelos pueden:

- **Generar texto**: Responder preguntas, escribir artículos, código, emails
- **Analizar contenido**: Resumir documentos, extraer información, clasificar texto
- **Transformar datos**: Traducir idiomas, reformatear información, convertir formatos
- **Razonar**: Resolver problemas lógicos, matemáticos, de programación

### Principales Proveedores

| Proveedor | Modelos Principales | Ventajas |
|-----------|---------------------|----------|
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-3.5 | Ecosistema maduro, documentación extensa |
| **Anthropic** | Claude 3.5, Claude 3 (Opus, Sonnet, Haiku) | Contexto largo (200K tokens), seguridad |
| **Google** | Gemini 1.5 Pro, Gemini 1.5 Flash | Tier gratuito generoso, multimodal |
| **Ollama** | Llama 3.2, Mistral, CodeLlama | 100% local, privacidad, sin costes |

---

## 2. Cómo obtener API Keys (GRATIS)

### OpenAI

**Créditos gratuitos**: $5 para nuevos usuarios

1. Regístrate en [platform.openai.com](https://platform.openai.com/)
2. Ve a **API Keys** en el menú lateral
3. Haz clic en **"Create new secret key"**
4. Copia la key (solo se muestra una vez)

```
Formato: sk-proj-xxxxxxxxxxxxxxxxxxxx
```

**Precios aproximados** (después del crédito gratuito):
- GPT-4o-mini: $0.15 / 1M tokens input, $0.60 / 1M tokens output
- GPT-4o: $2.50 / 1M tokens input, $10 / 1M tokens output

### Anthropic (Claude)

**Créditos gratuitos**: Disponibles al registrarse

1. Regístrate en [console.anthropic.com](https://console.anthropic.com/)
2. Ve a **Settings → API Keys**
3. Haz clic en **"Create Key"**
4. Copia la key

```
Formato: sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
```

**Precios aproximados**:
- Claude 3 Haiku: $0.25 / 1M tokens input, $1.25 / 1M tokens output
- Claude 3.5 Sonnet: $3 / 1M tokens input, $15 / 1M tokens output

### Google AI Studio (Gemini)

**Tier gratuito**: MUY GENEROSO - 60 requests/minuto sin coste

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

### Ollama (100% GRATIS)

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

# Modelo más potente (requiere más RAM)
ollama pull llama3.2:70b

# Modelo para código
ollama pull codellama
```

**Verificar instalación**:

```bash
ollama list  # Ver modelos instalados
ollama run llama3.2 "Hola, ¿cómo estás?"  # Probar
```

---

## 3. Conceptos Fundamentales

### 3.1 Tokens

Los tokens son las unidades básicas que procesan los LLMs. No son exactamente palabras ni caracteres.

**Regla aproximada**:
- Inglés: 1 token ≈ 4 caracteres ≈ 0.75 palabras
- Español: 1 token ≈ 3-4 caracteres (varía más por acentos)

**Ejemplos de tokenización**:

```
"Hola mundo" → ["Hola", " mundo"] → 2 tokens
"Inteligencia artificial" → ["Int", "elig", "encia", " artificial"] → 4 tokens
"12345" → ["123", "45"] → 2 tokens
```

**¿Por qué importan los tokens?**
- El coste se calcula por tokens
- Los modelos tienen límites de contexto en tokens
- Afectan la velocidad de respuesta

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

- **System prompt**: Define el comportamiento del modelo
- **User prompt**: El mensaje del usuario
- **Assistant prompt**: Respuestas previas del modelo (para contexto)

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
# temperature=1.5: "¡Robots Pensantes! La Revolución Silenciosa que no Viste Venir"
```

#### Max Tokens

Límite máximo de tokens en la respuesta.

```python
max_tokens=50   # Respuestas cortas
max_tokens=500  # Respuestas medianas
max_tokens=4096 # Respuestas largas
```

**Importante**: Si el modelo alcanza el límite, la respuesta se corta abruptamente.

#### Top P (Nucleus Sampling)

Alternativa a temperature. Selecciona tokens cuya probabilidad acumulada suma P.

```python
top_p=0.1  # Solo considera el 10% más probable → Muy conservador
top_p=0.9  # Considera el 90% más probable → Más variado
top_p=1.0  # Considera todos los tokens (default)
```

**Recomendación**: Usa `temperature` O `top_p`, no ambos a la vez.

#### Frequency Penalty (-2.0 a 2.0)

Penaliza tokens según cuántas veces ya aparecieron.

```python
frequency_penalty=0.0  # Sin penalización (default)
frequency_penalty=0.5  # Reduce repeticiones
frequency_penalty=1.0  # Evita repeticiones fuertemente
```

#### Presence Penalty (-2.0 a 2.0)

Penaliza tokens que ya aparecieron (sin importar frecuencia).

```python
presence_penalty=0.0  # Sin penalización (default)
presence_penalty=0.6  # Favorece temas nuevos
```

### 3.4 Ventana de Contexto

Cada modelo tiene un límite de tokens totales (input + output).

| Modelo | Contexto Máximo |
|--------|-----------------|
| GPT-4o | 128K tokens |
| GPT-4o-mini | 128K tokens |
| Claude 3.5 Sonnet | 200K tokens |
| Claude 3 Opus | 200K tokens |
| Gemini 1.5 Pro | 1M tokens |
| Gemini 1.5 Flash | 1M tokens |
| Llama 3.2 (Ollama) | 128K tokens |

**Cálculo aproximado**: 100K tokens ≈ 75,000 palabras ≈ 300 páginas

---

## 4. Estructura de las APIs

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

### 4.2 Endpoint Principal: Chat Completions

**OpenAI** - `POST https://api.openai.com/v1/chat/completions`

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

**Anthropic** - `POST https://api.anthropic.com/v1/messages`

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

**Google** - `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

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

**Ollama** - `POST http://localhost:11434/api/chat`

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

### 4.3 Formato de Respuesta

**OpenAI/Anthropic** (simplificado):

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
- `content`: La respuesta generada
- `finish_reason`: Por qué terminó (`stop`, `length`, `content_filter`)
- `usage`: Tokens consumidos (para calcular costes)

---

## 5. Comparativa de Proveedores

### Cuándo usar cada uno

| Necesidad | Recomendación |
|-----------|---------------|
| Aprender/Experimentar gratis | Google Gemini (tier gratuito generoso) |
| Privacidad total / Offline | Ollama (local) |
| Máxima calidad | Claude 3.5 Sonnet o GPT-4o |
| Coste mínimo con buena calidad | GPT-4o-mini o Claude 3 Haiku |
| Contexto muy largo (libros enteros) | Gemini 1.5 Pro (1M tokens) |
| Generación de código | GPT-4o, Claude 3.5 Sonnet, o CodeLlama |

### Límites de Rate

| Proveedor | Tier Gratuito | Requests/minuto |
|-----------|---------------|-----------------|
| OpenAI | Limitado tras $5 | 3-500 (según tier) |
| Anthropic | Créditos iniciales | 5-50 (según tier) |
| Google | Muy generoso | 60 |
| Ollama | Ilimitado | Solo limitado por hardware |

---

## 6. Ejercicios Prácticos

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

1. **Copia el archivo de configuración**:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```

2. **Añade tus API keys** en `config/config.yaml`

3. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta tu primer script**:
   ```bash
   python scripts/01_basico/openai_basico.py
   ```

### Progresión Recomendada

1. **Nivel Básico**: Ejecuta cada script de `01_basico/` para familiarizarte con cada API
2. **Nivel Intermedio**: Experimenta con `comparar_modelos.py` para ver diferencias entre proveedores
3. **Nivel Avanzado**: Explora `function_calling.py` para ver cómo los modelos pueden usar herramientas

### Webapp Interactiva

Para una experiencia visual, ejecuta la aplicación web:

```bash
cd webapp
uvicorn app:app --reload
```

Abre [http://localhost:8000](http://localhost:8000) en tu navegador.

---

## Recursos Adicionales

- [Documentación OpenAI](https://platform.openai.com/docs)
- [Documentación Anthropic](https://docs.anthropic.com/)
- [Documentación Google AI](https://ai.google.dev/docs)
- [Documentación Ollama](https://github.com/ollama/ollama)
