# Módulo 3: Fundamentos de Software de IA para Desarrollo

## Índice
1. [Ventanas de Contexto](#1-ventanas-de-contexto)
2. [Model Context Protocol (MCP)](#2-model-context-protocol-mcp)
3. [Subagentes y Multi-Agent Systems](#3-subagentes-y-multi-agent-systems)
4. [Hooks y Automatización](#4-hooks-y-automatización)
5. [Configuración Avanzada](#5-configuración-avanzada)
6. [Ejercicios Prácticos](#6-ejercicios-prácticos)

---

## 1. Ventanas de Contexto

### ¿Qué es la Ventana de Contexto?

La ventana de contexto es la cantidad máxima de texto (medida en tokens) que un modelo puede procesar en una sola interacción. Incluye tanto el input (tu prompt + historial) como el output (respuesta del modelo).

```
┌─────────────────────────────────────────────────────────┐
│                  VENTANA DE CONTEXTO                     │
│  ┌──────────────────┐  ┌───────────────────────────────┐│
│  │  INPUT TOKENS    │  │       OUTPUT TOKENS           ││
│  │  - System prompt │  │       (Respuesta)             ││
│  │  - Historial     │  │                               ││
│  │  - Tu mensaje    │  │                               ││
│  └──────────────────┘  └───────────────────────────────┘│
│         ◄─────────── Total: max_context_tokens ────────►│
└─────────────────────────────────────────────────────────┘
```

### Tamaños por Modelo (2025)

| Modelo | Ventana de Contexto | Equivalente Aproximado |
|--------|---------------------|------------------------|
| Gemini 3 | 1,000,000 tokens | ~750,000 palabras |
| Claude 4.5 | 200,000 tokens | ~150,000 palabras |
| GPT-5.2 | 128,000 tokens | ~96,000 palabras |
| DeepSeek-V3 | 128,000 tokens | ~96,000 palabras |

**Referencia**: 100K tokens ≈ 75,000 palabras ≈ 300 páginas

### ¿Por qué importa la Ventana de Contexto?

1. **Proyectos grandes**: Más contexto = más archivos que puede "ver" simultáneamente
2. **Conversaciones largas**: Sin truncar historial
3. **Documentos completos**: Análisis de libros, codebases enteros
4. **Menos fragmentación**: Menos necesidad de dividir tareas

### Gestión Eficiente del Contexto

#### Estrategia 1: Compresión de Contexto

```python
def compress_context(messages: list, max_tokens: int = 50000) -> list:
    """
    Estrategia: Mantener mensajes recientes completos,
    resumir los antiguos.
    """
    recent = messages[-10:]  # Últimos 10 mensajes completos
    old = messages[:-10]

    if old:
        summary = llm.summarize(old)
        return [
            {"role": "system", "content": f"Resumen de conversación previa: {summary}"}
        ] + recent

    return recent
```

#### Estrategia 2: Context Pruning

```python
def prune_context(messages: list, relevance_threshold: float = 0.5) -> list:
    """
    Elimina mensajes menos relevantes para la tarea actual.
    """
    # Calcular relevancia de cada mensaje respecto a la tarea
    scored_messages = [
        (msg, calculate_relevance(msg, current_task))
        for msg in messages
    ]

    # Mantener solo mensajes relevantes
    return [msg for msg, score in scored_messages if score >= relevance_threshold]
```

#### Estrategia 3: Sliding Window

```python
def sliding_window(messages: list, window_size: int = 20) -> list:
    """
    Mantiene solo los últimos N mensajes.
    Simple pero efectivo para conversaciones largas.
    """
    if len(messages) > window_size:
        # Guardar system prompt + últimos mensajes
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-window_size:]
        return system + recent
    return messages
```

### Context Compaction en Herramientas CLI

**Codex CLI** implementa "compaction" automático:
```
Sesión larga → Detecta límite cercano → Resume contexto → Continúa con contexto fresco
```

**Claude Code** ofrece el comando `/compact`:
```bash
# Compactar manualmente cuando el contexto es muy largo
/compact
```

---

## 2. Model Context Protocol (MCP)

### ¿Qué es MCP?

MCP (Model Context Protocol) es un **protocolo abierto** que permite la integración estandarizada entre aplicaciones LLM y fuentes de datos/herramientas externas.

Piensa en MCP como un "USB para LLMs": una interfaz estándar que permite conectar cualquier herramienta a cualquier modelo.

### Arquitectura MCP

```
┌───────────────────────────────────────────────────────────────┐
│                        CLIENTE MCP                             │
│  (Claude Desktop, Claude Code, Gemini CLI, tu aplicación)     │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           │ JSON-RPC sobre stdio/HTTP
                           │
┌──────────────────────────▼────────────────────────────────────┐
│                      SERVIDOR MCP                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Resources  │  │    Tools    │  │   Prompts   │            │
│  │  (lectura)  │  │ (ejecución) │  │ (plantillas)│            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
└─────────┼────────────────┼────────────────┼───────────────────┘
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Database │    │   API    │    │   File   │
    │          │    │ Externa  │    │  System  │
    └──────────┘    └──────────┘    └──────────┘
```

### Componentes MCP

#### 1. Resources (Recursos)
Datos de **solo lectura** que el LLM puede consultar.

```json
{
  "uri": "file:///proyecto/README.md",
  "name": "README del proyecto",
  "mimeType": "text/markdown"
}
```

Ejemplos:
- Contenido de archivos
- Resultados de consultas SQL
- Documentación de APIs
- Configuración del sistema

#### 2. Tools (Herramientas)
Funciones **ejecutables** que el LLM puede invocar.

```json
{
  "name": "crear_issue",
  "description": "Crea un issue en GitHub",
  "inputSchema": {
    "type": "object",
    "properties": {
      "titulo": {"type": "string"},
      "descripcion": {"type": "string"},
      "etiquetas": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["titulo"]
  }
}
```

Ejemplos:
- Ejecutar comandos shell
- Llamar a APIs externas
- Escribir archivos
- Enviar notificaciones

#### 3. Prompts (Plantillas)
Templates reutilizables para tareas comunes.

```json
{
  "name": "code-review",
  "description": "Realiza code review de un archivo",
  "arguments": [
    {"name": "file", "description": "Ruta del archivo a revisar"}
  ]
}
```

### Transportes Soportados

| Transporte | Uso | Ejemplo |
|------------|-----|---------|
| **stdio** | Servidores locales | Procesos en tu máquina |
| **HTTP/SSE** | Servidores remotos | APIs en la nube |
| **Streamable HTTP** | Nuevo estándar | Bidireccional eficiente |

### Configuración Básica de MCP

#### Para Claude Code / Claude Desktop

```json
// ~/.claude/settings.json o claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db"
      }
    }
  }
}
```

#### Para Servidores Remotos (HTTP)

```json
{
  "mcpServers": {
    "aws-knowledge": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http"
    },
    "cloudflare-workers": {
      "command": "npx",
      "args": ["mcp-remote", "https://workers.mcp.cloudflare.com/mcp"]
    }
  }
}
```

### Flujo de Comunicación MCP

```
1. Usuario: "Crea un issue en GitHub sobre el bug de login"

2. Cliente MCP (Claude Code):
   - Identifica que necesita la herramienta "crear_issue"
   - Prepara los parámetros: {titulo: "Bug de login", descripcion: "..."}

3. Servidor MCP (GitHub):
   - Recibe la solicitud JSON-RPC
   - Ejecuta: gh issue create --title "Bug de login" --body "..."
   - Devuelve: {success: true, issue_number: 123, url: "..."}

4. Cliente MCP:
   - Recibe respuesta
   - LLM genera: "He creado el issue #123. Puedes verlo en: ..."
```

---

## 3. Subagentes y Multi-Agent Systems

### Concepto

Los **subagentes** permiten delegar tareas especializadas a agentes secundarios mientras el agente principal coordina el trabajo.

```
┌────────────────────────────────────────────────────────────┐
│                  AGENTE PRINCIPAL                           │
│                  (Orquestador)                              │
└──────────────────────┬─────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Subagente   │ │  Subagente   │ │  Subagente   │
│  Frontend    │ │  Backend     │ │  Testing     │
│  (React)     │ │  (Node.js)   │ │  (Jest)      │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Casos de Uso

1. **Desarrollo paralelo**: Frontend y backend simultáneo
2. **Testing mientras coding**: Tests se escriben junto al código
3. **Documentación continua**: Docs se actualizan automáticamente
4. **Code review cruzado**: Un subagente revisa lo que otro escribió

### Ejemplo en Claude Code

```bash
# El agente principal coordina:
claude "Implementa una feature de autenticación con:
- Backend API (JWT tokens)
- Frontend (React form)
- Tests (unitarios + integración)
- Documentación

Trabaja en paralelo donde sea posible."
```

Claude Code puede internamente:
1. Spawnar un subagente para el backend
2. Spawnar otro para el frontend (en paralelo)
3. Coordinar cuando ambos terminan para integrar
4. Ejecutar tests al final

### Patrón de Implementación

```python
class MainAgent:
    def __init__(self):
        self.subagents = {
            "frontend": FrontendAgent(),
            "backend": BackendAgent(),
            "testing": TestAgent(),
            "docs": DocsAgent()
        }

    def execute_task(self, task: str):
        # 1. Analizar y descomponer tarea
        subtasks = self.decompose(task)

        # 2. Identificar dependencias
        dependency_graph = self.build_dependencies(subtasks)

        # 3. Ejecutar en paralelo donde sea posible
        results = []
        for level in dependency_graph.levels():
            level_results = asyncio.gather(*[
                self.subagents[subtask.type].execute(subtask)
                for subtask in level
            ])
            results.extend(level_results)

        # 4. Integrar resultados
        return self.integrate(results)

    def decompose(self, task: str) -> list:
        """Divide la tarea en subtareas especializadas."""
        return self.llm.analyze(f"Divide esta tarea: {task}")
```

### Comunicación entre Agentes

```python
class AgentMessage:
    sender: str
    recipient: str
    message_type: str  # "request", "response", "notification"
    content: dict
    metadata: dict

class AgentBus:
    """Bus de comunicación entre agentes."""

    async def send(self, message: AgentMessage):
        recipient = self.agents[message.recipient]
        await recipient.receive(message)

    async def broadcast(self, message: AgentMessage):
        for agent in self.agents.values():
            if agent.name != message.sender:
                await agent.receive(message)
```

---

## 4. Hooks y Automatización

### ¿Qué son los Hooks?

Los hooks permiten ejecutar acciones automáticas en puntos específicos del workflow del agente.

### Hooks en Claude Code

```json
// .claude/hooks.json
{
  "hooks": {
    "pre-edit": {
      "command": "npm run format",
      "description": "Formatear código antes de editar"
    },
    "post-edit": {
      "command": "npm run lint --fix",
      "description": "Lint después de cada edición"
    },
    "pre-command": {
      "command": "echo 'Ejecutando: $COMMAND'",
      "description": "Log de comandos"
    },
    "post-command": {
      "command": "./scripts/check-result.sh",
      "description": "Verificar resultado de comando"
    },
    "pre-commit": {
      "command": "npm test && npm run lint",
      "description": "Tests y lint antes de commit"
    },
    "on-error": {
      "command": "./scripts/notify-error.sh",
      "description": "Notificar errores"
    }
  }
}
```

### Tipos de Hooks Disponibles

| Hook | Cuándo se ejecuta |
|------|-------------------|
| `pre-edit` | Antes de modificar un archivo |
| `post-edit` | Después de modificar un archivo |
| `pre-command` | Antes de ejecutar un comando shell |
| `post-command` | Después de ejecutar un comando shell |
| `pre-commit` | Antes de hacer git commit |
| `post-commit` | Después de hacer git commit |
| `on-error` | Cuando ocurre un error |
| `on-start` | Al iniciar sesión |
| `on-end` | Al terminar sesión |

### Comandos Personalizados

Crea comandos reutilizables en `.claude/commands/`:

#### Ejemplo: Comando de Deploy

```markdown
# .claude/commands/deploy.md

# Deploy a Producción

Sigue estos pasos para hacer deploy:

## Pre-requisitos
- [ ] Todos los tests pasan
- [ ] El código está formateado
- [ ] No hay warnings de lint

## Pasos
1. Ejecutar suite de tests completa: `npm run test:all`
2. Build de producción: `npm run build`
3. Deploy a staging: `./scripts/deploy-staging.sh`
4. Ejecutar smoke tests: `npm run test:smoke -- --env=staging`
5. Si todo OK, deploy a producción: `./scripts/deploy-prod.sh`
6. Verificar health checks: `curl https://api.example.com/health`
7. Notificar en Slack: `./scripts/notify-deploy.sh`

## Rollback
Si algo falla: `./scripts/rollback.sh`

Confirma cada paso antes de continuar.
```

**Uso**: `/project:deploy`

#### Ejemplo: Comando de Code Review

```markdown
# .claude/commands/review.md

# Code Review Completo

Realiza un code review exhaustivo del código actual.

## Checklist
1. **Seguridad**
   - Buscar inyecciones SQL/XSS
   - Verificar validación de inputs
   - Revisar manejo de secretos

2. **Performance**
   - Identificar N+1 queries
   - Buscar operaciones bloqueantes
   - Verificar uso de caché

3. **Calidad**
   - Código duplicado
   - Funciones muy largas
   - Nombres poco descriptivos

4. **Tests**
   - Cobertura suficiente
   - Tests de edge cases
   - Tests de integración

## Formato de Salida
Para cada problema encontrado:
- Archivo y línea
- Severidad (CRÍTICO/ALTO/MEDIO/BAJO)
- Descripción
- Sugerencia de fix
```

**Uso**: `/project:review`

### Scripts de Automatización

#### Script de Setup de Proyecto

```bash
#!/bin/bash
# .claude/scripts/setup-project.sh

echo "🚀 Configurando proyecto para desarrollo con IA..."

# Crear estructura de carpetas
mkdir -p .claude/commands
mkdir -p .claude/scripts

# Crear CLAUDE.md si no existe
if [ ! -f CLAUDE.md ]; then
    cat > CLAUDE.md << 'EOF'
# Contexto del Proyecto

## Stack
- TODO: Definir tecnologías

## Convenciones
- TODO: Definir convenciones

## Comandos
- `npm run dev` - Desarrollo
- `npm test` - Tests
EOF
    echo "✅ CLAUDE.md creado"
fi

# Verificar dependencias
command -v node >/dev/null 2>&1 || echo "⚠️  Node.js no instalado"
command -v git >/dev/null 2>&1 || echo "⚠️  Git no instalado"

echo "✅ Setup completado"
```

---

## 5. Configuración Avanzada

### Variables de Entorno

```bash
# Claude Code
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export CLAUDE_MODEL="claude-sonnet-4-5-20250929"
export CLAUDE_MAX_TOKENS=4096

# Gemini CLI
export GOOGLE_API_KEY="AIza..."
export GEMINI_MODEL="gemini-3-pro"

# Codex CLI
export OPENAI_API_KEY="sk-..."
export CODEX_MODEL="gpt-5.2-codex"

# MCP común
export MCP_LOG_LEVEL="debug"  # Para debugging
```

### Archivo de Configuración Global

```json
// ~/.claude/settings.json
{
  "model": "claude-sonnet-4-5-20250929",
  "maxTokens": 4096,
  "temperature": 0.7,

  "permissions": {
    "allowFileWrite": true,
    "allowShellCommands": true,
    "allowNetworkAccess": true,
    "requireConfirmation": true,
    "dangerousCommands": ["rm -rf", "sudo", "chmod 777"]
  },

  "mcpServers": {
    // Servidores MCP configurados globalmente
  },

  "memory": {
    "enabled": true,
    "path": "~/.claude/memory",
    "maxSize": "100MB"
  },

  "ui": {
    "theme": "dark",
    "showTokenCount": true,
    "showCost": true,
    "compactMode": false
  },

  "hooks": {
    "enabled": true,
    "timeout": 30000
  }
}
```

### Configuración por Proyecto

```json
// proyecto/.claude/config.json
{
  "extends": "~/.claude/settings.json",

  "model": "claude-opus-4-5-20251101",  // Override para este proyecto

  "context": {
    "include": ["src/**", "tests/**", "docs/**"],
    "exclude": ["node_modules/**", "dist/**", "*.log"]
  },

  "mcpServers": {
    "proyecto-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"  // De .env
      }
    }
  }
}
```

### Perfiles de Configuración

```json
// ~/.claude/profiles/frontend.json
{
  "name": "Frontend Development",
  "model": "claude-sonnet-4-5-20250929",
  "context": {
    "focus": ["*.tsx", "*.ts", "*.css", "*.scss"],
    "exclude": ["*.test.*"]
  },
  "systemPrompt": "Eres un experto en React, TypeScript y CSS moderno."
}

// ~/.claude/profiles/backend.json
{
  "name": "Backend Development",
  "model": "claude-opus-4-5-20251101",
  "context": {
    "focus": ["*.py", "*.sql", "*.yaml"],
    "exclude": ["*.pyc", "__pycache__"]
  },
  "systemPrompt": "Eres un experto en Python, FastAPI y PostgreSQL."
}
```

**Uso**: `claude --profile frontend`

---

## 6. Ejercicios Prácticos

### Ejercicio 1: Gestión de Contexto

Experimenta con diferentes tamaños de contexto:

```bash
# Cargar un archivo grande
claude "Lee package.json y todos los archivos en src/ y explica la arquitectura"

# Ver uso de contexto
/tokens

# Compactar si es necesario
/compact
```

### Ejercicio 2: Configurar MCP

1. Configura el MCP de filesystem
2. Usa el MCP de Git
3. Verifica con `/mcp`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

### Ejercicio 3: Crear Hooks

1. Crea un hook pre-commit que ejecute tests
2. Crea un hook post-edit que formatee código
3. Prueba que funcionen

### Ejercicio 4: Comandos Personalizados

1. Crea un comando `/project:setup` que configure el proyecto
2. Crea un comando `/project:status` que muestre estado del proyecto
3. Prueba ambos comandos

### Ejercicio 5: Multi-Agente Manual

Simula un sistema multi-agente:

```bash
# Terminal 1 - Agente Backend
claude "Eres el agente de Backend. Implementa una API REST de usuarios."

# Terminal 2 - Agente Frontend
claude "Eres el agente de Frontend. Implementa un formulario de registro."

# Terminal 3 - Coordinador
claude "Revisa el trabajo de los otros agentes e intégralos."
```

---

## Recursos Adicionales

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Building MCP Servers](https://modelcontextprotocol.io/docs/building)

---

## Próximo Módulo

En el **Módulo 4: MCPs Oficiales del Mercado** aprenderás:
- MCPs de referencia de Anthropic
- AWS MCP Servers
- Cloudflare MCP Servers
- Firebase, GitHub, bases de datos y más
