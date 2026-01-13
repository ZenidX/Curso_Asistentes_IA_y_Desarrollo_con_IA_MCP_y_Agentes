# Módulo 3: Fundamentos de Software de IA para Desarrollo

## Información del Módulo

| | |
|---|---|
| **Duración estimada** | 4-5 horas |
| **Nivel** | Intermedio |
| **Prerrequisitos** | Módulo 2 completado, Claude Code funcionando |

---

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. ✅ Entender qué son las ventanas de contexto y gestionar proyectos grandes
2. ✅ Explicar la arquitectura de Model Context Protocol (MCP)
3. ✅ Configurar servidores MCP básicos en Claude Code
4. ✅ Comprender cuándo y cómo usar subagentes
5. ✅ Crear hooks para automatizar tareas repetitivas

---

## Continuación del Proyecto: TaskFlow

En este módulo, expandiremos TaskFlow con capacidades de IA:

```
TaskFlow/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
├── .claude/
│   ├── commands/       ← Comandos personalizados (Módulo 2)
│   └── hooks.json      ← NUEVO: Automatización
├── mcp-config.json     ← NUEVO: Configuración MCP
└── CLAUDE.md
```

**Objetivo del módulo**: Configurar MCPs para que Claude pueda acceder a nuestra base de datos y ejecutar comandos de forma segura.

---

## 1. Ventanas de Contexto

**⏱️ Tiempo estimado: 45 minutos**

### 1.1 ¿Qué es la Ventana de Contexto?

Imagina que estás hablando con alguien que tiene memoria limitada. Solo puede "recordar" las últimas N palabras de la conversación. Eso es esencialmente una ventana de contexto.

```
┌─────────────────────────────────────────────────────────────┐
│                  VENTANA DE CONTEXTO                         │
│                                                              │
│  ┌────────────────────┐   ┌────────────────────────────────┐│
│  │    TU INPUT        │ + │      RESPUESTA DEL LLM        ││
│  │  - System prompt   │   │                                ││
│  │  - Historial       │   │                                ││
│  │  - Tu mensaje      │   │                                ││
│  │  - Archivos leídos │   │                                ││
│  └────────────────────┘   └────────────────────────────────┘│
│                                                              │
│  ◄───────────── Máximo: X tokens ─────────────────────────► │
└─────────────────────────────────────────────────────────────┘
```

### 💡 Concepto Clave: Tokens

> Un **token** no es una palabra. Es un fragmento de texto que el modelo procesa. En español, una palabra típica = 1.5-2 tokens. La palabra "autenticación" = 3 tokens.

**Regla práctica**: 100 tokens ≈ 75 palabras ≈ 1/4 de página A4

### 1.2 Tamaños por Modelo (2025)

| Modelo | Ventana | Equivalente | Ejemplo de Uso |
|--------|---------|-------------|----------------|
| **Gemini 3** | 1M tokens | ~3,000 páginas | Analizar monorepos completos |
| **Claude 4.5** | 200K tokens | ~600 páginas | Proyectos medianos completos |
| **GPT-5.2** | 128K tokens | ~400 páginas | Proyectos pequeños/medianos |

### 1.3 ¿Por Qué Importa Esto?

**Escenario real**: Tu proyecto TaskFlow tiene:
- 50 archivos TypeScript
- 10,000 líneas de código
- Documentación en 5 archivos markdown

**Pregunta**: ¿Puede Claude "ver" todo esto a la vez?

```
Cálculo aproximado:
- 10,000 líneas × 10 tokens/línea = 100,000 tokens
- Documentación: ~5,000 tokens
- System prompt + CLAUDE.md: ~2,000 tokens
- Tu mensaje: ~500 tokens
─────────────────────────────────────────────────
Total: ~107,500 tokens

Claude 4.5 (200K): ✅ Cabe completo
GPT-5.2 (128K): ⚠️ Justo, sin margen
```

### 📍 Checkpoint 1

Antes de continuar, responde:
- [ ] ¿Cuántos tokens tiene aproximadamente tu proyecto actual?
- [ ] ¿Qué modelo necesitarías para analizarlo completo?

---

### 1.4 El Problema: Contexto Lleno

Cuando el contexto se llena, el modelo "olvida" información antigua. Esto causa:

1. **Pérdida de instrucciones**: Olvida reglas del CLAUDE.md
2. **Código inconsistente**: Olvida decisiones anteriores
3. **Errores de referencia**: "¿Qué archivo era ese?"

### ⚠️ Señales de Alerta

```
Síntoma: Claude empieza a "olvidar" lo que le dijiste hace 5 mensajes
Síntoma: Sugiere código que contradice decisiones anteriores
Síntoma: Pregunta cosas que ya habías aclarado
```

### 1.5 Estrategias de Gestión

#### Estrategia 1: Compactación Manual

Cuando la conversación es muy larga:

```bash
claude
> /compact
# Claude resume la conversación y libera espacio
```

**Cuándo usar**: Cada 30-50 intercambios o cuando notes "olvidos".

#### Estrategia 2: Sesiones Enfocadas

En lugar de una sesión larga para todo:

```bash
# Sesión 1: Backend
claude "Implementa el endpoint de autenticación"
# Terminar y cerrar

# Sesión 2: Frontend
claude "Implementa el formulario de login"
# Nueva sesión, contexto fresco
```

**Por qué funciona**: Cada sesión tiene contexto completo para su tarea.

#### Estrategia 3: Documentar Decisiones

Mantén un archivo de decisiones que Claude siempre lee:

```markdown
# decisions.md (incluir en CLAUDE.md)

## Decisiones Arquitectónicas

### 2025-01-05: Autenticación
- Elegimos JWT sobre sessions
- Refresh tokens con rotación
- Tokens expiran en 15 minutos

### 2025-01-06: Base de Datos
- Soft-delete para todos los modelos
- Campo `deleted_at` nullable
- Índice parcial para queries de no-eliminados
```

**Por qué funciona**: El contexto "recuerda" decisiones sin que las repitas.

---

### 🎯 Práctica Guiada 1: Medir tu Contexto

1. Abre Claude Code en tu proyecto
2. Ejecuta varios prompts de análisis
3. Usa `/cost` para ver tokens consumidos
4. Cuando llegues a ~50% del contexto, usa `/compact`
5. Observa cómo continúa la conversación

```bash
claude
> Analiza la estructura del proyecto
> Explica el flujo de autenticación
> ¿Qué mejoras de performance sugieres?
> /cost  # Ver tokens usados
> /compact  # Si es necesario
```

---

## 2. Model Context Protocol (MCP)

**⏱️ Tiempo estimado: 90 minutos**

### 2.1 El Problema que Resuelve MCP

Sin MCP, la integración de LLMs con herramientas externas era un desastre:

```
┌─────────────────────────────────────────────────────────────┐
│  ANTES DE MCP: Cada integración es custom                    │
│                                                              │
│  Claude ──custom code──► GitHub                              │
│  Claude ──custom code──► Slack                               │
│  Claude ──custom code──► PostgreSQL                          │
│  Claude ──custom code──► Tu API                              │
│                                                              │
│  Problema: N integraciones × M LLMs = N×M implementaciones   │
└─────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│  CON MCP: Protocolo estándar                                 │
│                                                              │
│  Claude  ─┐                   ┌─► GitHub MCP                 │
│  GPT     ─┼──► MCP Protocol ──┼─► Slack MCP                  │
│  Gemini  ─┘                   ├─► PostgreSQL MCP             │
│                               └─► Tu API MCP                 │
│                                                              │
│  Ventaja: M LLMs + N herramientas = M + N implementaciones   │
└─────────────────────────────────────────────────────────────┘
```

### 💡 Concepto Clave: MCP es como USB para LLMs

> Antes de USB, cada dispositivo tenía su conector propietario. USB estandarizó la conexión. **MCP hace lo mismo para LLMs**: cualquier herramienta MCP funciona con cualquier cliente MCP.

### 2.2 Arquitectura MCP

```
┌───────────────────────────────────────────────────────────────┐
│                     TU COMPUTADORA                             │
│                                                                │
│  ┌─────────────────┐         ┌─────────────────────────────┐  │
│  │  Claude Code    │         │     Servidor MCP            │  │
│  │  (Cliente MCP)  │◄──────►│     (proceso separado)      │  │
│  │                 │ JSON-   │  ┌─────┐ ┌─────┐ ┌───────┐  │  │
│  │                 │  RPC    │  │Tools│ │Rsrc │ │Prompts│  │  │
│  └─────────────────┘         │  └──┬──┘ └──┬──┘ └───┬───┘  │  │
│                              │     │       │       │       │  │
│                              └─────┼───────┼───────┼───────┘  │
│                                    │       │       │          │
│                                    ▼       ▼       ▼          │
│                              ┌─────────────────────────────┐  │
│                              │    Sistemas Externos        │  │
│                              │  (DB, APIs, Filesystem)     │  │
│                              └─────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### 2.3 Los Tres Componentes de MCP

#### 1. Resources (Recursos) - Solo Lectura

Los recursos son **datos que el LLM puede consultar** pero no modificar.

```json
{
  "uri": "db://tasks/pending",
  "name": "Tareas pendientes",
  "mimeType": "application/json"
}
```

**Ejemplos de Resources**:
- Contenido de un archivo
- Resultado de una query SQL (SELECT)
- Estado actual de la aplicación
- Configuración del sistema

**Analogía**: Como un informe que puedes leer pero no editar.

#### 2. Tools (Herramientas) - Ejecución

Las herramientas son **funciones que el LLM puede invocar**.

```json
{
  "name": "crear_tarea",
  "description": "Crea una nueva tarea en el sistema",
  "inputSchema": {
    "type": "object",
    "properties": {
      "titulo": {"type": "string"},
      "prioridad": {"type": "string", "enum": ["alta", "media", "baja"]}
    },
    "required": ["titulo"]
  }
}
```

**Ejemplos de Tools**:
- Crear/actualizar/eliminar registros
- Enviar emails o notificaciones
- Ejecutar comandos del sistema
- Llamar a APIs externas

**Analogía**: Como botones de acción en una interfaz.

#### 3. Prompts (Plantillas) - Reutilización

Los prompts son **templates predefinidos** para tareas comunes.

```json
{
  "name": "code-review",
  "description": "Revisa código siguiendo nuestras guías",
  "arguments": [
    {"name": "archivo", "description": "Ruta al archivo a revisar"}
  ]
}
```

**Ejemplos de Prompts**:
- Template de code review
- Formato de commit message
- Estructura de documentación

**Analogía**: Como plantillas de documentos que rellenas.

### 📍 Checkpoint 2

Clasifica estos elementos en Resource, Tool, o Prompt:
- [ ] Leer la lista de usuarios de la base de datos → _______
- [ ] Enviar un mensaje a Slack → _______
- [ ] Template para escribir tests → _______
- [ ] Crear un nuevo issue en GitHub → _______

<details>
<summary>Ver respuestas</summary>

- Leer usuarios → **Resource** (solo lectura)
- Enviar a Slack → **Tool** (acción)
- Template de tests → **Prompt** (plantilla)
- Crear issue → **Tool** (acción)

</details>

---

### 2.4 Configurar tu Primer MCP

Vamos a configurar el MCP de filesystem para que Claude pueda acceder a archivos de forma segura.

#### Paso 1: Localizar la configuración

```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Linux
~/.config/claude/claude_desktop_config.json

# O para Claude Code
~/.claude/settings.json
```

#### Paso 2: Añadir el servidor

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/TuUsuario/Proyectos/TaskFlow"
      ]
    }
  }
}
```

#### Paso 3: Verificar

```bash
claude
> /mcp
# Debería mostrar: filesystem (connected)

> Lee el archivo src/services/auth.ts usando el MCP de filesystem
```

### ⚠️ Error Común: "MCP server not found"

**Causa**: npx no puede encontrar el paquete.

**Solución**:
```bash
# Instalar globalmente primero
npm install -g @modelcontextprotocol/server-filesystem

# Luego en la config, usar la ruta completa:
{
  "command": "node",
  "args": [
    "C:/Users/TuUsuario/AppData/Roaming/npm/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
    "C:/Users/TuUsuario/Proyectos/TaskFlow"
  ]
}
```

---

### 2.5 Flujo de Comunicación MCP

Entender este flujo te ayudará a debuggear problemas:

```
Usuario: "Crea una tarea llamada 'Revisar PR #42'"

1. Claude analiza el mensaje
2. Claude identifica que necesita la tool "crear_tarea"
3. Claude envía al servidor MCP:
   {
     "method": "tools/call",
     "params": {
       "name": "crear_tarea",
       "arguments": {"titulo": "Revisar PR #42"}
     }
   }

4. El servidor ejecuta la función
5. El servidor responde:
   {
     "result": {
       "content": [{"type": "text", "text": "Tarea #123 creada"}]
     }
   }

6. Claude incorpora el resultado en su respuesta:
   "He creado la tarea #123 'Revisar PR #42'"
```

### 🎯 Práctica Guiada 2: Configurar MCP de Git

1. Añade el MCP de Git a tu configuración:

```json
{
  "mcpServers": {
    "filesystem": { /* ... */ },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    }
  }
}
```

2. Reinicia Claude Code

3. Prueba estos comandos:
```bash
claude
> /mcp  # Verificar que git está conectado
> ¿Cuáles son los últimos 5 commits de este repo?
> ¿Hay cambios sin commitear?
> Muestra el diff del último commit
```

---

## 3. Subagentes y Sistemas Multi-Agente

**⏱️ Tiempo estimado: 45 minutos**

### 3.1 ¿Qué es un Subagente?

Un subagente es un **agente secundario** que el agente principal puede "spawner" para tareas específicas.

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE PRINCIPAL                          │
│                    (Claude Code)                             │
│                                                              │
│  "Implementa autenticación completa con frontend y tests"   │
│                           │                                  │
│           ┌───────────────┼───────────────┐                  │
│           ▼               ▼               ▼                  │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│    │Subagente │    │Subagente │    │Subagente │             │
│    │ Backend  │    │ Frontend │    │  Tests   │             │
│    │          │    │          │    │          │             │
│    │• JWT     │    │• Login   │    │• Unit    │             │
│    │• Refresh │    │• Logout  │    │• E2E     │             │
│    │• Middleware│  │• Token   │    │• Mocks   │             │
│    └──────────┘    └──────────┘    └──────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 ¿Por Qué Usar Subagentes?

| Sin Subagentes | Con Subagentes |
|----------------|----------------|
| Un solo "hilo" de trabajo | Trabajo paralelo |
| Contexto compartido (se llena rápido) | Cada subagente tiene su contexto |
| Si falla una parte, todo se afecta | Fallos aislados |
| Difícil de coordinar tareas grandes | Divide y vencerás |

### 3.3 Cuándo Claude Usa Subagentes

Claude Code automáticamente puede usar subagentes cuando:

1. **Tareas paralelas**: "Implementa backend y frontend simultáneamente"
2. **Búsquedas amplias**: "Encuentra todos los usos de esta función en el proyecto"
3. **Análisis complejos**: "Revisa todo el código buscando vulnerabilidades"

### 💡 Concepto Clave: El "Task Tool"

> En Claude Code, cuando ves que se lanza un "Task", es un subagente. El agente principal coordina y el Task ejecuta trabajo específico.

### 3.4 Patrón Manual: Multi-Terminal

Puedes simular subagentes manualmente:

```bash
# Terminal 1 - Agente Backend
claude "Eres el desarrollador backend. Implementa el endpoint
        POST /api/auth/login con JWT. Avísame cuando termines."

# Terminal 2 - Agente Frontend
claude "Eres el desarrollador frontend. Implementa el componente
        LoginForm que llame a POST /api/auth/login. Avísame cuando
        termines."

# Terminal 3 - Coordinador
claude "Revisa el trabajo en src/api/auth.ts y src/components/LoginForm.tsx.
        Verifica que sean compatibles y que funcionen juntos."
```

### 📍 Checkpoint 3

Responde:
- [ ] ¿Cuándo usarías subagentes?
- [ ] ¿Cuál es la ventaja principal de dividir el trabajo?

---

## 4. Hooks y Automatización

**⏱️ Tiempo estimado: 45 minutos**

### 4.1 ¿Qué son los Hooks?

Los hooks son **scripts que se ejecutan automáticamente** en puntos específicos del workflow de Claude.

```
Usuario: "Edita auth.ts para añadir validación"
                    │
                    ▼
            ┌──────────────┐
            │  pre-edit    │ ◄── Hook: npm run format
            │   HOOK       │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  Claude      │
            │  edita       │
            │  archivo     │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  post-edit   │ ◄── Hook: npm run lint
            │   HOOK       │
            └──────────────┘
                    │
                    ▼
            Archivo editado y validado
```

### 4.2 Tipos de Hooks Disponibles

| Hook | Cuándo se ejecuta | Uso típico |
|------|-------------------|------------|
| `pre-edit` | Antes de editar archivo | Formatear, crear backup |
| `post-edit` | Después de editar | Lint, type-check |
| `pre-command` | Antes de ejecutar comando | Logging, validación |
| `post-command` | Después de comando | Verificar resultado |
| `pre-commit` | Antes de git commit | Tests, lint |
| `on-error` | Cuando algo falla | Notificaciones |

### 4.3 Configurar Hooks

Crea `.claude/hooks.json` en tu proyecto:

```json
{
  "hooks": {
    "post-edit": {
      "command": "npm run lint:fix",
      "description": "Auto-fix linting después de edición",
      "timeout": 30000
    },
    "pre-commit": {
      "command": "npm test && npm run lint",
      "description": "Tests y lint antes de commit",
      "timeout": 120000
    },
    "on-error": {
      "command": "echo 'Error en Claude Code' >> ~/.claude/errors.log",
      "description": "Loggear errores"
    }
  }
}
```

### 4.4 Hooks Prácticos para TaskFlow

#### Hook: Formatear antes de editar

```json
{
  "pre-edit": {
    "command": "npx prettier --write",
    "args": ["$FILE"],
    "description": "Formatear archivo antes de editar"
  }
}
```

**$FILE** se reemplaza con la ruta del archivo que Claude va a editar.

#### Hook: Verificar tipos después de editar

```json
{
  "post-edit": {
    "command": "npx tsc --noEmit",
    "description": "Verificar tipos TypeScript",
    "continueOnError": true
  }
}
```

**continueOnError**: No bloquea si hay errores de tipos (solo avisa).

#### Hook: Tests antes de commit

```json
{
  "pre-commit": {
    "command": "npm test -- --coverage --watchAll=false",
    "description": "Ejecutar tests con coverage",
    "timeout": 180000
  }
}
```

### ⚠️ Error Común: Hook que bloquea todo

**Problema**: Un hook lento o que falla bloquea el workflow.

**Solución**:
```json
{
  "post-edit": {
    "command": "npm run lint",
    "timeout": 10000,
    "continueOnError": true,
    "async": true
  }
}
```

- **timeout**: Máximo tiempo de ejecución
- **continueOnError**: No bloquear si falla
- **async**: Ejecutar en background

---

### 🎯 Práctica Guiada 3: Crear Sistema de Hooks

1. Crea la estructura de hooks:

```bash
mkdir -p .claude
touch .claude/hooks.json
```

2. Añade configuración:

```json
{
  "hooks": {
    "post-edit": {
      "command": "npx prettier --write $FILE && npx eslint --fix $FILE",
      "description": "Format y lint automático",
      "timeout": 15000,
      "continueOnError": true
    },
    "pre-commit": {
      "command": "npm test -- --watchAll=false",
      "description": "Tests antes de commit",
      "timeout": 120000
    }
  }
}
```

3. Prueba el sistema:

```bash
claude
> Añade un comentario al inicio de src/index.ts
# Observa cómo se ejecuta prettier y eslint automáticamente
```

---

## 5. Configuración Avanzada

**⏱️ Tiempo estimado: 30 minutos**

### 5.1 Estructura Completa de Configuración

```
~/.claude/                    # Configuración global
├── settings.json             # Settings globales
├── memory/                   # Memoria persistente
└── profiles/                 # Perfiles de trabajo
    ├── frontend.json
    └── backend.json

tu-proyecto/
├── .claude/                  # Configuración del proyecto
│   ├── config.json           # Override de settings
│   ├── hooks.json            # Hooks del proyecto
│   └── commands/             # Comandos personalizados
│       ├── deploy.md
│       └── review.md
├── CLAUDE.md                 # Contexto del proyecto
└── mcp-config.json           # Servidores MCP
```

### 5.2 Perfiles de Trabajo

Crea perfiles para diferentes contextos:

```json
// ~/.claude/profiles/frontend.json
{
  "name": "Frontend Developer",
  "model": "claude-sonnet-4-5",
  "systemPrompt": "Eres experto en React 18, TypeScript y TailwindCSS.
                   Siempre usas hooks modernos y evitas class components.",
  "context": {
    "include": ["src/components/**", "src/hooks/**", "src/styles/**"],
    "exclude": ["src/api/**", "src/services/**"]
  }
}
```

```json
// ~/.claude/profiles/backend.json
{
  "name": "Backend Developer",
  "model": "claude-opus-4-5",
  "systemPrompt": "Eres experto en Node.js, Express y PostgreSQL.
                   Priorizas seguridad y performance.",
  "context": {
    "include": ["src/api/**", "src/services/**", "src/models/**"],
    "exclude": ["src/components/**"]
  }
}
```

**Uso**:
```bash
claude --profile frontend
claude --profile backend
```

### 5.3 Variables de Entorno Importantes

```bash
# API Keys
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."
export DATABASE_URL="postgresql://..."

# Configuración de Claude Code
export CLAUDE_MODEL="claude-sonnet-4-5-20250929"
export CLAUDE_MAX_TOKENS=4096

# Debug
export MCP_LOG_LEVEL="debug"  # Para ver comunicación MCP
```

---

## 6. Ejercicios Prácticos

### Ejercicio 1: Análisis de Contexto (20 min)
**Nivel: Básico**

1. Abre un proyecto mediano (10+ archivos)
2. Inicia Claude Code y pide análisis general
3. Después de 20 prompts, usa `/cost`
4. Practica `/compact` y observa la diferencia

**Criterio de éxito**: Entiendes cuánto contexto consume tu proyecto.

### Ejercicio 2: Configurar MCP Básico (30 min)
**Nivel: Intermedio**

1. Configura el MCP de filesystem para tu proyecto
2. Configura el MCP de git
3. Verifica con `/mcp`
4. Ejecuta: "Muestra los archivos modificados en el último commit"

**Criterio de éxito**: Ambos MCPs responden correctamente.

### Ejercicio 3: Sistema de Hooks (30 min)
**Nivel: Intermedio**

1. Crea `.claude/hooks.json`
2. Añade hook `post-edit` que ejecute prettier
3. Añade hook `pre-commit` que ejecute tests
4. Prueba editando un archivo y haciendo commit

**Criterio de éxito**: Los hooks se ejecutan automáticamente.

### Ejercicio 4: Multi-Agente Manual (45 min)
**Nivel: Avanzado**

1. Abre 3 terminales
2. En cada una, inicia Claude con un rol diferente:
   - Terminal 1: "Eres el arquitecto. Diseña el sistema"
   - Terminal 2: "Eres el implementador. Escribe el código"
   - Terminal 3: "Eres el tester. Escribe tests y verifica"
3. Coordina el trabajo manualmente entre las 3

**Criterio de éxito**: Produces código funcional con tests usando coordinación manual.

---

## 7. Troubleshooting

### "Context window full"

**Solución rápida**:
```bash
claude
> /compact
```

**Solución permanente**: Divide el trabajo en sesiones más pequeñas.

### "MCP server disconnected"

**Diagnóstico**:
```bash
# Ver logs del servidor MCP
export MCP_LOG_LEVEL=debug
claude
> /mcp
```

**Solución común**: Reiniciar el servidor MCP (salir y entrar de Claude).

### "Hook timeout exceeded"

**Solución**:
```json
{
  "pre-commit": {
    "command": "npm test",
    "timeout": 300000,
    "async": true
  }
}
```

---

## Resumen del Módulo

### Lo que aprendiste

1. **Ventanas de contexto**: Qué son, tamaños, estrategias de gestión
2. **MCP**: Arquitectura, componentes (Resources, Tools, Prompts)
3. **Configuración MCP**: Filesystem, Git, verificación
4. **Subagentes**: Cuándo y cómo dividir trabajo
5. **Hooks**: Automatización de tareas repetitivas

### Preparación para el Módulo 4

En el próximo módulo veremos **MCPs oficiales del mercado**:
- AWS MCP Servers
- Cloudflare MCP
- Firebase, GitHub, bases de datos
- Cómo elegir y combinar MCPs

**Tarea previa**: Ten al menos 2 MCPs configurados y funcionando.

---

## Recursos Adicionales

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Code Docs - MCP](https://docs.anthropic.com/claude-code/mcp)
- [Awesome MCP](https://github.com/punkpeye/awesome-mcp-servers)
