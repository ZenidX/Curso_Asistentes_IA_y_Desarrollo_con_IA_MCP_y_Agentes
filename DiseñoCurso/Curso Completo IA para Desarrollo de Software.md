# Curso Completo: IA para Desarrollo de Software

## Índice General

1. [Módulo 1: APIs de IA - Fundamentos y Comparativa](#módulo-1)
2. [Módulo 2: Herramientas CLI de IA para Coding](#módulo-2)
3. [Módulo 3: Fundamentos de Software de IA para Desarrollo](#módulo-3)
4. [Módulo 4: MCPs Oficiales del Mercado](#módulo-4)
5. [Módulo 5: Desarrollo de MCPs Propios](#módulo-5)
6. [Módulo 6: Arquitectura de Desarrollo Asistido por IA](#módulo-6)

---

# Módulo 1: APIs de IA - Fundamentos y Comparativa {#módulo-1}

## 1.1 Introducción a las APIs de IA Generativa

Las APIs de IA permiten integrar capacidades de modelos de lenguaje en aplicaciones de software. Cada proveedor ofrece diferentes modelos optimizados para distintos casos de uso.

## 1.2 Claude API (Anthropic)

### Modelos Disponibles (2025)
| Modelo | Identificador | Características |
|--------|---------------|-----------------|
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | Más avanzado e inteligente |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | Balance rendimiento/costo |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Rápido y económico |

### Endpoint Principal
```bash
POST https://api.anthropic.com/v1/messages
```

### Ejemplo de Llamada
```python
import anthropic

client = anthropic.Anthropic(api_key="tu-api-key")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explica qué es una API REST"}
    ]
)
print(message.content[0].text)
```

### Características Únicas
- **Ventana de contexto**: Hasta 200K tokens
- **Visión**: Análisis de imágenes y documentos PDF
- **Tool Use**: Llamada a funciones estructurada
- **Extended Thinking**: Razonamiento paso a paso

---

## 1.3 OpenAI API (ChatGPT/GPT)

### Modelos Disponibles (2025)
| Modelo | Uso Recomendado |
|--------|-----------------|
| GPT-5.2 | Propósito general, multimodal |
| GPT-5.2 Pro | Razonamiento profundo |
| GPT-5.2-Codex | Coding y software engineering |
| o3, o4-mini | Modelos de razonamiento |

### Endpoint Principal
```bash
POST https://api.openai.com/v1/chat/completions
# Nuevo: POST https://api.openai.com/v1/responses (Agent-native)
```

### Ejemplo de Llamada
```python
from openai import OpenAI

client = OpenAI(api_key="tu-api-key")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Eres un asistente de programación."},
        {"role": "user", "content": "Escribe una función que ordene una lista"}
    ]
)
print(response.choices[0].message.content)
```

### Características Únicas
- **Responses API**: Diseñada para agentes
- **Function Calling**: Integración con herramientas
- **Vision**: Análisis de imágenes
- **Realtime API**: Voz en tiempo real

---

## 1.4 Google Gemini API

### Modelos Disponibles (2025)
| Modelo | Características |
|--------|-----------------|
| Gemini 3 Pro | Más inteligente, razonamiento avanzado |
| Gemini 3 Flash | Velocidad optimizada, bajo costo |
| Gemini 3 Deep Think | Razonamiento profundo extendido |

### Endpoint Principal
```bash
POST https://generativelanguage.googleapis.com/v1/models/{model}:generateContent
```

### Ejemplo de Llamada
```python
import google.generativeai as genai

genai.configure(api_key="tu-api-key")
model = genai.GenerativeModel('gemini-3-pro')

response = model.generate_content("¿Qué es machine learning?")
print(response.text)
```

### Características Únicas
- **Ventana de contexto**: 1M tokens (la más grande)
- **Multimodal nativo**: Texto, imagen, audio, video
- **Google Search Grounding**: Búsqueda integrada
- **Code Execution**: Ejecución de código en sandbox

---

## 1.5 DeepSeek API

### Modelos Principales
| Modelo | Especialización |
|--------|-----------------|
| DeepSeek-V3 | Propósito general |
| DeepSeek-Coder | Optimizado para código |
| DeepSeek-R1 | Razonamiento (open-source) |

### Ejemplo de Llamada
```python
from openai import OpenAI  # Compatible con formato OpenAI

client = OpenAI(
    api_key="tu-deepseek-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[{"role": "user", "content": "Optimiza este código SQL"}]
)
```

### Ventajas
- Precios muy competitivos
- Excelente rendimiento en código
- Modelos open-source disponibles

---

## 1.6 xAI Grok API

### Modelos Disponibles
| Modelo | Características |
|--------|-----------------|
| Grok-2 | Modelo principal |
| Grok-2 Vision | Con capacidades de visión |

### Ejemplo de Llamada
```python
from openai import OpenAI

client = OpenAI(
    api_key="tu-xai-key",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-2-latest",
    messages=[{"role": "user", "content": "Analiza esta tendencia de mercado"}]
)
```

---

## 1.7 Tabla Comparativa de APIs

| Característica | Claude | OpenAI | Gemini | DeepSeek | Grok |
|----------------|--------|--------|--------|----------|------|
| Contexto máx. | 200K | 128K | 1M | 128K | 128K |
| Visión | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tool Use | ✅ | ✅ | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ | ✅ |
| Batch API | ✅ | ✅ | ✅ | ❌ | ❌ |
| Web Search | ✅ | ✅ | ✅ | ❌ | ✅ |

---

# Módulo 2: Herramientas CLI de IA para Coding {#módulo-2}

## 2.1 Claude Code (Anthropic)

### Descripción
Claude Code es una herramienta agéntica de programación que vive en tu terminal, entiende tu codebase y te ayuda a programar más rápido mediante comandos en lenguaje natural.

### Instalación
```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Alternativa via npm
npm install -g @anthropic-ai/claude-code
```

### Comandos Básicos
```bash
# Iniciar sesión interactiva
claude

# Ejecutar prompt directo
claude "Explica este codebase"

# Modo no interactivo (pipeable)
claude -p "Analiza app.log y encuentra errores"

# Con archivo de entrada
cat error.log | claude -p "¿Qué causó este error?"
```

### Comandos Slash Importantes
| Comando | Función |
|---------|---------|
| `/help` | Mostrar ayuda |
| `/model` | Cambiar modelo (Sonnet, Opus, Haiku) |
| `/bug` | Reportar un bug |
| `/clear` | Limpiar contexto |
| `/config` | Ver/editar configuración |
| `/mcp` | Gestionar servidores MCP |

### Modos de Operación
```bash
# Modo normal (pide confirmación)
claude

# Modo auto-accept (acepta ediciones automáticamente)
claude --auto-accept

# Modo YOLO (ejecuta todo sin confirmación) ⚠️
claude --dangerously-skip-permissions
```

### Configuración CLAUDE.md
Crea un archivo `CLAUDE.md` en la raíz del proyecto:
```markdown
# Contexto del Proyecto

## Stack Tecnológico
- Backend: Node.js + Express
- Frontend: React + TypeScript
- Base de datos: PostgreSQL

## Convenciones
- Usar camelCase para variables
- Tests con Jest
- Commits en formato Conventional Commits

## Comandos útiles
- `npm run dev` - Iniciar desarrollo
- `npm test` - Ejecutar tests
```

---

## 2.2 Gemini CLI (Google)

### Descripción
Gemini CLI es un agente de IA open-source que trae el poder de Gemini directamente a tu terminal, con acceso gratuito generoso para usuarios con cuenta de Google.

### Instalación
```bash
# Via npm (recomendado)
npm install -g @anthropic-ai/gemini-cli

# Verificar instalación
gemini --version
```

### Límites Gratuitos
- 60 requests/minuto
- 1,000 requests/día
- Acceso a Gemini 2.5/3 Pro
- Ventana de contexto de 1M tokens

### Comandos Básicos
```bash
# Iniciar sesión interactiva
gemini

# Prompt directo
gemini "Resume los cambios de ayer en git"

# Modo no interactivo
gemini -p "Explica la arquitectura" --output-format json
```

### Comandos Slash
| Comando | Función |
|---------|---------|
| `/help` | Ayuda |
| `/chat` | Nueva conversación |
| `/settings` | Configuración |
| `/model` | Seleccionar modelo |
| `/memory list` | Ver archivos de memoria |
| `/extensions` | Gestionar extensiones |

### Configuración en settings.json
```json
// ~/.gemini/settings.json
{
  "theme": "dark",
  "model": "gemini-3-flash",
  "previewFeatures": true,
  "showStatusInTitle": true
}
```

### Archivo GEMINI.md
Similar a CLAUDE.md, proporciona contexto persistente:
```markdown
# Proyecto: E-commerce API

## Tecnologías
- Python 3.11 + FastAPI
- MongoDB
- Docker + Kubernetes

## Reglas de código
- Type hints obligatorios
- Docstrings en Google style
```

---

## 2.3 OpenAI Codex CLI

### Descripción
Codex CLI es un agente de coding de OpenAI que corre localmente y se conecta con el ecosistema Codex cloud para tareas paralelas.

### Instalación
```bash
# Via npm
npm install -g @openai/codex

# Via Homebrew (macOS)
brew install --cask codex
```

### Autenticación
```bash
# Iniciar y autenticar con ChatGPT
codex
# Seleccionar "Sign in with ChatGPT"
```

### Comandos Básicos
```bash
# Sesión interactiva
codex

# Prompt inicial
codex "Explain this codebase to me"

# Resumir sesión anterior
codex resume

# Ejecutar script automatizado
codex exec "Run tests and fix failures"
```

### Modos de Aprobación
```bash
# Suggest (solo sugiere, no ejecuta)
codex --approval-mode suggest

# Auto-edit (edita archivos, pide confirmación para comandos)
codex --approval-mode auto-edit

# Full-auto (todo automático) ⚠️
codex --approval-mode full-auto
```

### Configuración config.toml
```toml
# ~/.codex/config.toml
[model]
default = "gpt-5.2-codex"

[features]
web_search_request = true

[sandbox_workspace_write]
network_access = true

[mcp]
servers = ["github", "linear"]
```

### Code Review Integrado
```bash
# Revisión de código antes de commit
codex review

# Revisión de commit específico
codex review HEAD~1
```

---

## 2.4 Comparativa de CLIs

| Característica | Claude Code | Gemini CLI | Codex CLI |
|----------------|-------------|------------|-----------|
| **Precio** | API pay-as-you-go | Gratis (límites) | Suscripción ChatGPT |
| **Open Source** | Parcial | ✅ Completo | Parcial |
| **MCP Support** | ✅ Cliente y servidor | ✅ Cliente | ✅ Cliente |
| **IDE Integration** | VS Code, JetBrains | VS Code | VS Code, Cursor |
| **Cloud Tasks** | ❌ | ❌ | ✅ Paralelas |
| **Modelo por defecto** | Claude Sonnet 4.5 | Gemini 3 Flash | GPT-5.2-Codex |

---

# Módulo 3: Fundamentos de Software de IA para Desarrollo {#módulo-3}

## 3.1 Ventanas de Contexto

### ¿Qué es la Ventana de Contexto?
La ventana de contexto es la cantidad máxima de texto (medida en tokens) que un modelo puede procesar en una sola interacción.

### Tamaños por Modelo (2025)
| Modelo | Ventana de Contexto |
|--------|---------------------|
| Gemini 3 | 1,000,000 tokens |
| Claude 4.5 | 200,000 tokens |
| GPT-5.2 | 128,000 tokens |

### Gestión Eficiente del Contexto

```python
# Ejemplo: Compresión de contexto
def compress_context(messages, max_tokens=50000):
    """
    Estrategia: Mantener mensajes recientes completos,
    resumir los antiguos
    """
    recent = messages[-10:]  # Últimos 10 mensajes completos
    old = messages[:-10]
    
    if old:
        summary = llm.summarize(old)
        return [{"role": "system", "content": f"Resumen previo: {summary}"}] + recent
    return recent
```

### Context Compaction (Codex)
GPT-5.2-Codex implementa "compaction" automático:
```
Sesión larga → Detecta límite → Resume contexto → Continúa con contexto fresco
```

---

## 3.2 Model Context Protocol (MCP)

### ¿Qué es MCP?
MCP es un protocolo abierto que permite la integración estandarizada entre aplicaciones LLM y fuentes de datos/herramientas externas.

### Arquitectura MCP
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Cliente   │────▶│   Servidor  │────▶│   Recurso   │
│   (Claude)  │◀────│    MCP      │◀────│  (GitHub)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Componentes MCP
1. **Resources**: Datos de solo lectura (archivos, APIs)
2. **Tools**: Funciones ejecutables por el LLM
3. **Prompts**: Plantillas reutilizables

### Transportes Soportados
| Transporte | Uso |
|------------|-----|
| **stdio** | Servidores locales |
| **HTTP/SSE** | Servidores remotos |
| **Streamable HTTP** | Nuevo estándar |

### Configuración Básica
```json
// ~/.claude/settings.json o claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxx"
      }
    }
  }
}
```

---

## 3.3 Subagentes y Multi-Agent Systems

### Concepto
Los subagentes permiten delegar tareas especializadas mientras el agente principal coordina el trabajo.

### Ejemplo en Claude Code
```bash
# El agente principal puede spawnar subagentes para:
# - Backend API mientras frontend se desarrolla en paralelo
# - Tests mientras se implementa la feature
# - Documentación mientras se refactoriza
```

### Patrón de Implementación
```python
# Pseudo-código de orquestación de subagentes
class MainAgent:
    def execute_task(self, task):
        # Analizar y dividir tarea
        subtasks = self.decompose(task)
        
        # Asignar a subagentes especializados
        results = []
        for subtask in subtasks:
            if subtask.type == "frontend":
                result = FrontendAgent().execute(subtask)
            elif subtask.type == "backend":
                result = BackendAgent().execute(subtask)
            elif subtask.type == "testing":
                result = TestAgent().execute(subtask)
            results.append(result)
        
        # Integrar resultados
        return self.integrate(results)
```

---

## 3.4 Hooks y Automatización

### Hooks en Claude Code
Los hooks permiten ejecutar acciones automáticas en puntos específicos:

```json
// .claude/hooks.json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint && npm test"
    },
    "post-edit": {
      "command": "prettier --write"
    },
    "on-error": {
      "command": "notify-slack.sh"
    }
  }
}
```

### Comandos Personalizados
Crear `.claude/commands/deploy.md`:
```markdown
# Deploy Command

Ejecuta el siguiente flujo de deployment:

1. Ejecutar tests: `npm test`
2. Build de producción: `npm run build`
3. Deploy a staging: `./scripts/deploy-staging.sh`
4. Verificar health check
5. Si ok, deploy a producción: `./scripts/deploy-prod.sh`

Confirma cada paso antes de continuar.
```

Uso: `/project:deploy`

---

## 3.5 Configuración Avanzada

### Variables de Entorno Importantes

```bash
# Claude Code
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_MODEL="claude-sonnet-4-5-20250929"

# Gemini CLI
export GOOGLE_API_KEY="AIza..."
export GOOGLE_GENAI_USE_VERTEXAI=true  # Para Vertex AI

# Codex CLI
export OPENAI_API_KEY="sk-..."
```

### Archivo de Configuración Global

```json
// Ejemplo: ~/.claude/settings.json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow_file_write": true,
    "allow_shell_commands": true,
    "require_confirmation": true
  },
  "mcpServers": {
    // Servidores MCP configurados
  },
  "memory": {
    "enabled": true,
    "path": "~/.claude/memory"
  }
}
```

---

# Módulo 4: MCPs Oficiales del Mercado {#módulo-4}

## 4.1 MCPs de Referencia (Anthropic)

Servidores MCP oficiales que demuestran las capacidades del protocolo:

| MCP Server | Función |
|------------|---------|
| **Everything** | Servidor de referencia con prompts, resources y tools |
| **Filesystem** | Operaciones de archivos con control de acceso |
| **Git** | Leer, buscar y manipular repositorios Git |
| **Memory** | Sistema de memoria persistente basado en knowledge graph |
| **Fetch** | Obtener contenido web para LLMs |
| **Sequential Thinking** | Resolución de problemas paso a paso |

### Instalación de MCPs de Referencia
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    }
  }
}
```

---

## 4.2 AWS MCP Servers

AWS proporciona una suite completa de servidores MCP:

### Servidores Principales

| Servidor | Función |
|----------|---------|
| **AWS API** | Ejecutar comandos AWS CLI |
| **AWS Knowledge** | Documentación y best practices |
| **AWS CDK** | Guía de CDK y CloudFormation |
| **AWS Cost Analysis** | Análisis de costos |
| **AWS Nova Canvas** | Generación de imágenes |

### Configuración AWS API MCP
```json
{
  "mcpServers": {
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil",
        "AWS_REGION": "eu-west-1",
        "READ_OPERATIONS_ONLY": "true"
      }
    }
  }
}
```

### AWS Knowledge MCP (Remoto)
```json
{
  "mcpServers": {
    "aws-knowledge": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http"
    }
  }
}
```

### Tools Disponibles (AWS API)
- `execute_aws_command`: Ejecutar comandos AWS CLI
- `get_execution_plan`: Planes paso a paso para tareas AWS

---

## 4.3 Cloudflare MCP Servers

Cloudflare ofrece MCPs remotos para su plataforma de desarrollo:

### Servidores Disponibles

| Servidor | URL | Función |
|----------|-----|---------|
| **Workers** | `workers.mcp.cloudflare.com` | Gestión de Workers |
| **KV** | `kv.mcp.cloudflare.com` | Key-Value storage |
| **R2** | `r2.mcp.cloudflare.com` | Object storage |
| **D1** | `d1.mcp.cloudflare.com` | SQL database |
| **Observability** | `observability.mcp.cloudflare.com` | Analytics y logs |
| **Bindings** | `bindings.mcp.cloudflare.com` | Gestión de bindings |

### Configuración
```json
{
  "mcpServers": {
    "cloudflare-workers": {
      "command": "npx",
      "args": ["mcp-remote", "https://workers.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-r2": {
      "command": "npx",
      "args": ["mcp-remote", "https://r2.mcp.cloudflare.com/mcp"]
    }
  }
}
```

---

## 4.4 Firebase MCP

### Instalación
```json
{
  "mcpServers": {
    "firebase": {
      "command": "npx",
      "args": ["-y", "@gannonh/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "/path/to/serviceAccountKey.json",
        "FIREBASE_STORAGE_BUCKET": "proyecto.firebasestorage.app"
      }
    }
  }
}
```

### Capacidades
- **Authentication**: Gestión de usuarios
- **Firestore**: Operaciones CRUD en documentos
- **Storage**: Subida y gestión de archivos

### Tools Disponibles
| Tool | Función |
|------|---------|
| `firestore_add_document` | Crear documento |
| `firestore_get_document` | Obtener documento |
| `firestore_query` | Consultar colección |
| `firestore_list_collections` | Listar colecciones |
| `storage_upload` | Subir archivo |
| `auth_get_user` | Obtener usuario |

---

## 4.5 GitHub MCP

### Configuración
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

### Capacidades
- Listar y buscar repositorios
- Crear y gestionar issues
- Crear y revisar pull requests
- Gestionar branches
- Leer contenido de archivos

---

## 4.6 Bases de Datos

### PostgreSQL MCP
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

### MySQL MCP
```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@benborber/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "mydb"
      }
    }
  }
}
```

### MongoDB MCP
```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mcp-mongo-server"],
      "env": {
        "MONGODB_URI": "mongodb://localhost:27017/mydb"
      }
    }
  }
}
```

---

## 4.7 Otros MCPs Populares

| MCP | Función |
|-----|---------|
| **Slack** | Enviar mensajes, buscar en canales |
| **Linear** | Gestión de issues y proyectos |
| **Notion** | Lectura/escritura de páginas |
| **Jira** | Gestión de tickets |
| **Sentry** | Análisis de errores |
| **Puppeteer** | Automatización de browser |
| **Docker** | Gestión de contenedores |
| **Kubernetes** | Operaciones de cluster |

---

# Módulo 5: Desarrollo de MCPs Propios {#módulo-5}

## 5.1 Arquitectura de un MCP Server

### Componentes Principales
```
MCP Server
├── Transport Layer (stdio / HTTP)
├── Protocol Handler (JSON-RPC)
├── Resources (datos de solo lectura)
├── Tools (funciones ejecutables)
└── Prompts (plantillas)
```

### Flujo de Comunicación
```
Cliente MCP ──JSON-RPC──▶ Servidor MCP ──▶ Recurso Externo
     ◀──────Response──────     ◀────Data────
```

---

## 5.2 Crear un MCP Server en Python

### Paso 1: Configurar el Proyecto
```bash
# Crear directorio
mkdir mi-mcp-server && cd mi-mcp-server

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install mcp fastmcp
```

### Paso 2: Implementar el Servidor
```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

# Crear instancia del servidor
server = Server("mi-servidor-mcp")

# Definir un Tool
@server.tool()
async def buscar_productos(query: str, categoria: str = None) -> str:
    """
    Busca productos en el catálogo.
    
    Args:
        query: Término de búsqueda
        categoria: Categoría opcional para filtrar
    """
    # Simular búsqueda en base de datos
    productos = [
        {"id": 1, "nombre": "Laptop Pro", "precio": 1299},
        {"id": 2, "nombre": "Mouse Wireless", "precio": 49},
    ]
    
    # Filtrar por query
    resultados = [p for p in productos if query.lower() in p["nombre"].lower()]
    
    return json.dumps(resultados, indent=2)

# Definir un Resource
@server.resource("inventario://productos")
async def get_inventario() -> str:
    """Devuelve el inventario completo de productos."""
    inventario = {
        "total_productos": 150,
        "categorias": ["electrónica", "hogar", "deportes"],
        "ultima_actualizacion": "2025-01-08"
    }
    return json.dumps(inventario)

# Definir un Prompt
@server.prompt("analizar-ventas")
async def prompt_analizar_ventas(periodo: str = "mensual") -> str:
    """Prompt para analizar ventas."""
    return f"""Analiza las ventas del periodo {periodo}.
    
    Incluye:
    1. Productos más vendidos
    2. Tendencias de crecimiento
    3. Recomendaciones de stock
    
    Usa los datos del inventario y las búsquedas disponibles."""

# Ejecutar servidor
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Paso 3: Configurar en Claude/Gemini
```json
{
  "mcpServers": {
    "mi-servidor": {
      "command": "python",
      "args": ["/path/to/mi-mcp-server/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/mi-mcp-server"
      }
    }
  }
}
```

---

## 5.3 Crear un MCP Server en TypeScript

### Paso 1: Inicializar Proyecto
```bash
mkdir mcp-typescript && cd mcp-typescript
npm init -y
npm install @modelcontextprotocol/sdk
npm install -D typescript @types/node
```

### Paso 2: Configurar TypeScript
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./build",
    "strict": true
  },
  "include": ["src/**/*"]
}
```

### Paso 3: Implementar el Servidor
```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Crear servidor
const server = new Server(
  { name: "mi-servidor-ts", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

// Registrar herramientas disponibles
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "calcular_precio",
      description: "Calcula el precio con descuento",
      inputSchema: {
        type: "object",
        properties: {
          precio_base: { type: "number", description: "Precio original" },
          descuento: { type: "number", description: "Porcentaje de descuento" },
        },
        required: ["precio_base", "descuento"],
      },
    },
    {
      name: "obtener_clima",
      description: "Obtiene el clima de una ciudad",
      inputSchema: {
        type: "object",
        properties: {
          ciudad: { type: "string", description: "Nombre de la ciudad" },
        },
        required: ["ciudad"],
      },
    },
  ],
}));

// Manejar llamadas a herramientas
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "calcular_precio": {
      const { precio_base, descuento } = args as { precio_base: number; descuento: number };
      const precio_final = precio_base * (1 - descuento / 100);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              precio_original: precio_base,
              descuento: `${descuento}%`,
              precio_final: precio_final.toFixed(2),
            }),
          },
        ],
      };
    }
    
    case "obtener_clima": {
      const { ciudad } = args as { ciudad: string };
      // Simular API de clima
      const clima = {
        ciudad,
        temperatura: Math.floor(Math.random() * 30) + 5,
        condicion: ["soleado", "nublado", "lluvioso"][Math.floor(Math.random() * 3)],
      };
      return {
        content: [{ type: "text", text: JSON.stringify(clima) }],
      };
    }
    
    default:
      throw new Error(`Tool desconocido: ${name}`);
  }
});

// Listar recursos
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "config://app",
      name: "Configuración de la App",
      mimeType: "application/json",
    },
  ],
}));

// Leer recursos
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "config://app") {
    return {
      contents: [
        {
          uri: "config://app",
          mimeType: "application/json",
          text: JSON.stringify({ version: "1.0", env: "production" }),
        },
      ],
    };
  }
  throw new Error("Recurso no encontrado");
});

// Iniciar servidor
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Servidor MCP iniciado");
}

main().catch(console.error);
```

### Paso 4: Compilar y Ejecutar
```bash
# Compilar
npm run build  # o: npx tsc

# Probar con MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js
```

---

## 5.4 Servidor MCP con HTTP Transport

```typescript
// src/http-server.ts
import express from "express";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const app = express();
const server = new Server(
  { name: "http-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Configurar tools... (igual que antes)

// Endpoint SSE
app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});

// Endpoint para mensajes
app.post("/messages", express.json(), async (req, res) => {
  // Manejar mensajes entrantes
});

app.listen(3000, () => {
  console.log("MCP HTTP Server en puerto 3000");
});
```

---

## 5.5 Usando FastMCP (Python Simplificado)

```python
# fast_server.py
from fastmcp import FastMCP

mcp = FastMCP("Mi Servidor Rápido")

@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b

@mcp.tool()
def buscar_usuario(email: str) -> dict:
    """Busca un usuario por email."""
    # Simular base de datos
    return {
        "email": email,
        "nombre": "Usuario Demo",
        "activo": True
    }

@mcp.resource("stats://daily")
def estadisticas_diarias() -> str:
    """Estadísticas del día."""
    import json
    return json.dumps({
        "visitas": 1500,
        "conversiones": 45,
        "ingresos": 2340.50
    })

if __name__ == "__main__":
    mcp.run()
```

---

## 5.6 Testing de MCP Servers

### Usando MCP Inspector
```bash
# Instalar inspector
npm install -g @modelcontextprotocol/inspector

# Ejecutar con tu servidor
npx @modelcontextprotocol/inspector python server.py
npx @modelcontextprotocol/inspector node build/index.js
```

### Tests Unitarios (Python)
```python
# test_server.py
import pytest
import asyncio
from server import buscar_productos

@pytest.mark.asyncio
async def test_buscar_productos():
    resultado = await buscar_productos("Laptop")
    assert "Laptop Pro" in resultado

@pytest.mark.asyncio
async def test_buscar_sin_resultados():
    resultado = await buscar_productos("xyz123")
    assert resultado == "[]"
```

---

# Módulo 6: Arquitectura de Desarrollo Asistido por IA {#módulo-6}

## 6.1 Patrones de Arquitectura

### Patrón 1: Agente Único con MCPs
```
┌─────────────────────────────────────────────────┐
│                 Claude Code                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ GitHub  │ │ Firebase│ │  AWS    │  ... MCPs │
│  │   MCP   │ │   MCP   │ │  MCP    │           │
│  └────┬────┘ └────┬────┘ └────┬────┘           │
└───────┼──────────┼──────────┼──────────────────┘
        │          │          │
        ▼          ▼          ▼
    [GitHub]   [Firebase]   [AWS]
```

### Patrón 2: Multi-Agente Orquestado
```
┌──────────────────────────────────────────────────────┐
│                  Agente Orquestador                   │
│                   (Claude Code)                       │
└──────────────────────┬───────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Subagente  │ │   Subagente  │ │   Subagente  │
│   Frontend   │ │   Backend    │ │   Testing    │
│  (React/Vue) │ │  (API/DB)    │ │  (Jest/Py)   │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Patrón 3: Pipeline CI/CD Asistido
```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Code   │───▶│  Test   │───▶│ Review  │───▶│ Deploy  │
│  Agent  │    │  Agent  │    │  Agent  │    │  Agent  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
  [Codex]       [Codex]       [Claude]       [Claude]
 Generate      Run Tests     Code Review    Deploy Script
```

---

## 6.2 Caso Práctico: Desarrollo de Feature Completa

### Objetivo
Implementar una nueva feature de "Sistema de Notificaciones" usando desarrollo asistido por IA.

### Paso 1: Planificación con Claude
```bash
claude "Necesito implementar un sistema de notificaciones push para 
nuestra app. Analiza el codebase actual y propón una arquitectura 
que incluya: backend (Node.js), base de datos (PostgreSQL), 
y servicio de push (Firebase). Genera un plan detallado."
```

### Paso 2: Configurar MCPs Necesarios
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "..." }
    },
    "postgres": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "..." }
    },
    "firebase": {
      "command": "npx",
      "args": ["-y", "@gannonh/firebase-mcp"],
      "env": { "SERVICE_ACCOUNT_KEY_PATH": "..." }
    }
  }
}
```

### Paso 3: Desarrollo Iterativo

```bash
# 1. Crear estructura de base de datos
claude "Usando el MCP de PostgreSQL, crea las tablas necesarias 
para el sistema de notificaciones: usuarios, dispositivos, 
notificaciones, preferencias."

# 2. Implementar backend
claude "Implementa los endpoints REST para:
- POST /api/notifications (crear notificación)
- GET /api/notifications/:userId (listar notificaciones)
- PUT /api/notifications/:id/read (marcar como leída)
- POST /api/devices/register (registrar dispositivo)"

# 3. Integrar Firebase
claude "Configura Firebase Cloud Messaging para enviar 
notificaciones push. Usa el MCP de Firebase para verificar 
la configuración."

# 4. Tests
claude "Escribe tests unitarios y de integración para el 
sistema de notificaciones. Ejecuta los tests y corrige 
cualquier fallo."

# 5. Code Review
claude "Revisa todo el código generado. Verifica:
- Manejo de errores
- Validación de inputs
- Seguridad (inyección SQL, autenticación)
- Performance"

# 6. Documentación
claude "Genera documentación API en formato OpenAPI/Swagger 
y actualiza el README con instrucciones de uso."

# 7. Pull Request
claude "Crea un pull request en GitHub con todos los cambios.
Incluye descripción detallada y tests coverage."
```

---

## 6.3 Workflow Completo con Múltiples Herramientas

### Escenario: Bug Fix Urgente

```bash
# 1. Identificar el bug (Sentry MCP)
claude "@sentry Muéstrame los errores críticos de las últimas 24 horas"

# 2. Analizar código relacionado
claude "Analiza el stack trace del error AUTH_FAILED y encuentra 
la causa raíz en el código"

# 3. Crear branch y fix
claude "Crea una branch 'fix/auth-issue-1234', implementa el fix 
y verifica que los tests pasen"

# 4. Code Review automático
codex review  # Usando Codex para revisión independiente

# 5. Crear PR
claude "@github Crea un PR desde fix/auth-issue-1234 a main 
con el template de hotfix"

# 6. Notificar al equipo
claude "@slack Envía un mensaje a #engineering: 
'Hotfix AUTH_FAILED en revisión, PR #xxx'"
```

---

## 6.4 Automatización de Workflows

### GitHub Actions con Claude
```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Claude Code
        run: |
          curl -fsSL https://claude.ai/install.sh | bash
          
      - name: Run AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review the changes in this PR. 
          Focus on security, performance, and best practices. 
          Output as GitHub comment format."
          
      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            // Publicar el review como comentario en el PR
```

### Script de Traducción Automática
```bash
#!/bin/bash
# translate-strings.sh

claude -p "Find all new text strings in src/ that need 
translation. Translate them to Spanish and French. 
Create a PR for the language team to review."
```

---

## 6.5 Mejores Prácticas

### 1. Proporciona Contexto Rico
```markdown
# CLAUDE.md / GEMINI.md

## Proyecto: E-commerce Platform

### Arquitectura
- Monorepo con pnpm workspaces
- Frontend: Next.js 14 + TypeScript
- Backend: Node.js + Fastify
- DB: PostgreSQL + Prisma ORM
- Cache: Redis
- Queue: BullMQ

### Convenciones
- Código en inglés, comentarios en español
- Tests: mínimo 80% coverage
- Commits: Conventional Commits
- PRs: requieren 2 approvals

### Variables de entorno
Ver .env.example para referencia

### Comandos frecuentes
- `pnpm dev` - Desarrollo local
- `pnpm test` - Tests
- `pnpm db:migrate` - Migraciones
```

### 2. Usa TDD con IA
```bash
# Primero los tests
claude "Escribe tests para un servicio de carrito de compras 
que debe: agregar items, remover items, calcular totales, 
aplicar descuentos"

# Luego la implementación
claude "Implementa el CartService para que pasen todos los tests"

# Verificar
claude "Ejecuta los tests y muestra el coverage"
```

### 3. Divide Tareas Complejas
```bash
# En lugar de:
claude "Construye un sistema de autenticación completo"

# Mejor:
claude "Paso 1: Diseña el schema de DB para usuarios y sesiones"
claude "Paso 2: Implementa el endpoint de registro"
claude "Paso 3: Implementa el endpoint de login con JWT"
claude "Paso 4: Implementa middleware de autenticación"
claude "Paso 5: Añade refresh tokens"
claude "Paso 6: Tests de integración"
```

### 4. Verificación Cruzada
```bash
# Usa diferentes herramientas para verificar
claude "Implementa la función de validación"
codex "Review this implementation for edge cases"
gemini "Check for security vulnerabilities"
```

---

## 6.6 Métricas y Monitoreo

### Dashboard de Productividad
```python
# metrics.py - Ejemplo de tracking
import json
from datetime import datetime

def log_ai_interaction(tool: str, task_type: str, duration: float, success: bool):
    """Registra interacciones con herramientas de IA."""
    metric = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool,  # claude, codex, gemini
        "task_type": task_type,  # code_gen, review, debug, docs
        "duration_seconds": duration,
        "success": success
    }
    
    with open("ai_metrics.jsonl", "a") as f:
        f.write(json.dumps(metric) + "\n")

# Análisis
def analyze_productivity():
    """Analiza métricas de productividad."""
    # Tiempo promedio por tipo de tarea
    # Tasa de éxito por herramienta
    # Comparativa pre/post IA
    pass
```

---

## 6.7 Checklist de Implementación

### Para Nuevos Proyectos
- [ ] Crear archivo CLAUDE.md/GEMINI.md con contexto del proyecto
- [ ] Configurar MCPs necesarios (GitHub, DB, servicios cloud)
- [ ] Establecer convenciones de código en el contexto
- [ ] Configurar comandos personalizados en `.claude/commands/`
- [ ] Integrar en CI/CD para code review automático

### Para Proyectos Existentes
- [ ] Documentar arquitectura actual para contexto de IA
- [ ] Identificar tareas repetitivas para automatizar
- [ ] Configurar MCPs para servicios existentes
- [ ] Crear comandos para workflows comunes
- [ ] Establecer métricas de productividad

### Seguridad
- [ ] No incluir secrets en archivos de contexto
- [ ] Configurar permisos apropiados en MCPs
- [ ] Revisar código generado antes de deploy
- [ ] Usar modo de confirmación en producción
- [ ] Auditar accesos a MCPs regularmente

---

## Recursos Adicionales

### Documentación Oficial
- [Claude Code Docs](https://code.claude.com/docs)
- [Gemini CLI Docs](https://geminicli.com/docs)
- [Codex CLI Docs](https://developers.openai.com/codex/cli)
- [MCP Specification](https://modelcontextprotocol.io)

### Repositorios
- [MCP Servers (Oficial)](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)

### Comunidades
- [Claude Developers Discord](https://discord.gg/anthropic)
- [Gemini CLI GitHub Discussions](https://github.com/google-gemini/gemini-cli/discussions)

---

*Curso actualizado: Enero 2026*
*Versión: 1.0*