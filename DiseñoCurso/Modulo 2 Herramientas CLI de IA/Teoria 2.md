# Módulo 2: Herramientas CLI de IA para Coding

## Índice
1. [Introducción](#1-introducción)
2. [Claude Code (Anthropic)](#2-claude-code-anthropic)
3. [Gemini CLI (Google)](#3-gemini-cli-google)
4. [Codex CLI (OpenAI)](#4-codex-cli-openai)
5. [Comparativa de CLIs](#5-comparativa-de-clis)
6. [Ejercicios Prácticos](#6-ejercicios-prácticos)

---

## 1. Introducción

Las herramientas CLI de IA para coding son agentes que viven en tu terminal y te ayudan a programar más rápido mediante comandos en lenguaje natural. Entienden tu codebase, ejecutan tareas rutinarias y manejan workflows completos.

### ¿Por qué usar CLIs de IA?

| Ventaja | Descripción |
|---------|-------------|
| **Velocidad** | No necesitas cambiar de contexto entre IDE y chat |
| **Integración** | Acceso directo al sistema de archivos y terminal |
| **Automatización** | Pueden ejecutar comandos, tests y builds |
| **Contexto** | Entienden todo tu proyecto, no solo archivos aislados |

---

## 2. Claude Code (Anthropic)

### Descripción
Claude Code es una herramienta agéntica de programación que vive en tu terminal, entiende tu codebase y te ayuda a programar más rápido mediante comandos en lenguaje natural.

### Instalación

```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell como administrador)
irm https://claude.ai/install.ps1 | iex

# Alternativa via npm
npm install -g @anthropic-ai/claude-code

# Verificar instalación
claude --version
```

### Autenticación

```bash
# Primera ejecución - te pedirá login
claude

# O configurar API key manualmente
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"
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

# Resumir conversación anterior
claude --resume

# Continuar desde la última sesión
claude --continue
```

### Comandos Slash Importantes

| Comando | Función |
|---------|---------|
| `/help` | Mostrar ayuda completa |
| `/model` | Cambiar modelo (Sonnet, Opus, Haiku) |
| `/clear` | Limpiar contexto de conversación |
| `/config` | Ver/editar configuración |
| `/mcp` | Gestionar servidores MCP |
| `/bug` | Reportar un bug |
| `/cost` | Ver costo de la sesión actual |
| `/compact` | Compactar el contexto largo |

### Modos de Operación

```bash
# Modo normal (pide confirmación para cada acción)
claude

# Modo auto-accept (acepta ediciones de archivos automáticamente)
claude --auto-accept

# Modo YOLO - ejecuta todo sin confirmación (PELIGROSO)
claude --dangerously-skip-permissions
```

### Configuración CLAUDE.md

Crea un archivo `CLAUDE.md` en la raíz del proyecto para dar contexto persistente:

```markdown
# Contexto del Proyecto

## Stack Tecnológico
- Backend: Node.js + Express
- Frontend: React + TypeScript
- Base de datos: PostgreSQL
- ORM: Prisma

## Convenciones de Código
- Usar camelCase para variables y funciones
- PascalCase para componentes y clases
- Tests con Jest y React Testing Library
- Commits en formato Conventional Commits

## Estructura del Proyecto
- /src/api - Endpoints REST
- /src/components - Componentes React
- /src/services - Lógica de negocio
- /src/utils - Utilidades compartidas

## Comandos Útiles
- `npm run dev` - Iniciar desarrollo
- `npm test` - Ejecutar tests
- `npm run lint` - Verificar linting
- `npm run build` - Build de producción

## Notas Importantes
- La base de datos requiere Docker: `docker-compose up -d`
- Variables de entorno en .env.local (no commitear)
```

### Comandos Personalizados

Crea comandos en `.claude/commands/`:

```markdown
# .claude/commands/deploy.md

# Comando de Deploy

Ejecuta el siguiente flujo de deployment:

1. Ejecutar tests: `npm test`
2. Verificar linting: `npm run lint`
3. Build de producción: `npm run build`
4. Deploy a staging: `./scripts/deploy-staging.sh`
5. Verificar health check: `curl https://staging.example.com/health`
6. Si todo ok, deploy a producción: `./scripts/deploy-prod.sh`

Confirma cada paso antes de continuar.
```

Uso: `/project:deploy`

### Configuración Avanzada

```json
// ~/.claude/settings.json
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

## 3. Gemini CLI (Google)

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

| Característica | Límite |
|----------------|--------|
| Requests/minuto | 60 |
| Requests/día | 1,000 |
| Modelo disponible | Gemini 2.5/3 Pro |
| Ventana de contexto | 1,000,000 tokens |

### Comandos Básicos

```bash
# Iniciar sesión interactiva
gemini

# Prompt directo
gemini "Resume los cambios de ayer en git"

# Modo no interactivo con formato de salida
gemini -p "Explica la arquitectura" --output-format json

# Con modelo específico
gemini -m gemini-3-pro "Analiza este código"
```

### Comandos Slash

| Comando | Función |
|---------|---------|
| `/help` | Mostrar ayuda |
| `/chat` | Nueva conversación |
| `/settings` | Configuración |
| `/model` | Seleccionar modelo |
| `/memory list` | Ver archivos de memoria |
| `/extensions` | Gestionar extensiones |
| `/stats` | Estadísticas de uso |

### Configuración

```json
// ~/.gemini/settings.json
{
  "theme": "dark",
  "model": "gemini-3-flash",
  "previewFeatures": true,
  "showStatusInTitle": true,
  "defaultOutputFormat": "markdown",
  "extensions": {
    "github": true,
    "filesystem": true
  }
}
```

### Archivo GEMINI.md

Similar a CLAUDE.md, proporciona contexto persistente:

```markdown
# Proyecto: E-commerce API

## Tecnologías
- Python 3.11 + FastAPI
- MongoDB con Motor (async)
- Docker + Kubernetes
- Redis para caché

## Reglas de Código
- Type hints obligatorios en todas las funciones
- Docstrings en Google style
- Tests con pytest (mínimo 80% coverage)
- Formateo con Black + isort

## Arquitectura
- /app/routers - Endpoints FastAPI
- /app/models - Modelos Pydantic
- /app/services - Lógica de negocio
- /app/repositories - Acceso a datos
```

### Extensiones (MCP)

Gemini CLI soporta extensiones que son equivalentes a MCPs:

```bash
# Listar extensiones disponibles
gemini extensions list

# Instalar extensión
gemini extensions install github

# Usar extensión en prompt
gemini "@github lista los PRs abiertos"
```

---

## 4. Codex CLI (OpenAI)

### Descripción
Codex CLI es un agente de coding de OpenAI que corre localmente y se conecta con el ecosistema Codex cloud para tareas paralelas.

### Instalación

```bash
# Via npm
npm install -g @openai/codex

# Via Homebrew (macOS)
brew install --cask codex

# Verificar
codex --version
```

### Autenticación

```bash
# Iniciar y autenticar con ChatGPT
codex
# Seleccionar "Sign in with ChatGPT"

# O usar API key
export OPENAI_API_KEY="sk-..."
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

# Con modelo específico
codex --model gpt-5.2-codex "Optimiza este código"
```

### Modos de Aprobación

```bash
# Suggest - solo sugiere, no ejecuta nada
codex --approval-mode suggest

# Auto-edit - edita archivos automáticamente, pide confirmación para comandos
codex --approval-mode auto-edit

# Full-auto - todo automático (PELIGROSO)
codex --approval-mode full-auto
```

### Code Review Integrado

```bash
# Revisión de código antes de commit
codex review

# Revisión de commit específico
codex review HEAD~1

# Revisión de PR
codex review --pr 123
```

### Configuración

```toml
# ~/.codex/config.toml
[model]
default = "gpt-5.2-codex"

[features]
web_search_request = true
code_execution = true

[sandbox_workspace_write]
network_access = true

[mcp]
servers = ["github", "linear"]
```

### Tareas en la Nube

Codex permite ejecutar tareas en paralelo en la nube:

```bash
# Iniciar tarea en background
codex cloud "Run full test suite" --background

# Ver tareas activas
codex cloud list

# Ver resultado de tarea
codex cloud result <task-id>
```

---

## 5. Comparativa de CLIs

### Tabla Comparativa General

| Característica | Claude Code | Gemini CLI | Codex CLI |
|----------------|-------------|------------|-----------|
| **Precio** | API pay-as-you-go | Gratis (con límites) | Suscripción ChatGPT |
| **Open Source** | Parcial | Completo | Parcial |
| **MCP Support** | Cliente y servidor | Cliente | Cliente |
| **IDE Integration** | VS Code, JetBrains | VS Code | VS Code, Cursor |
| **Cloud Tasks** | No | No | Sí (paralelas) |
| **Modelo por defecto** | Claude Sonnet 4.5 | Gemini 3 Flash | GPT-5.2-Codex |
| **Contexto máximo** | 200K tokens | 1M tokens | 128K tokens |

### Cuándo Usar Cada Uno

| Escenario | Mejor Opción | Razón |
|-----------|--------------|-------|
| Proyectos grandes (muchos archivos) | Gemini CLI | Ventana de 1M tokens |
| Coding asistido detallado | Claude Code | Mejor razonamiento |
| Integración con OpenAI ecosystem | Codex CLI | Nativo con ChatGPT |
| Presupuesto limitado | Gemini CLI | Tier gratuito generoso |
| Tareas paralelas/background | Codex CLI | Cloud tasks |
| Mejor code review | Claude Code | Análisis profundo |

### Comandos Equivalentes

| Acción | Claude Code | Gemini CLI | Codex CLI |
|--------|-------------|------------|-----------|
| Iniciar | `claude` | `gemini` | `codex` |
| Prompt directo | `claude "..."` | `gemini "..."` | `codex "..."` |
| Cambiar modelo | `/model` | `/model` | `--model` |
| Limpiar contexto | `/clear` | `/chat` | `/clear` |
| Ver ayuda | `/help` | `/help` | `--help` |
| Configuración | `/config` | `/settings` | `config.toml` |

---

## 6. Ejercicios Prácticos

### Ejercicio 1: Configuración Inicial

1. Instala Claude Code o Gemini CLI
2. Crea un proyecto de ejemplo
3. Configura el archivo CLAUDE.md/GEMINI.md
4. Ejecuta comandos básicos

### Ejercicio 2: Análisis de Codebase

```bash
# Con Claude Code
claude "Analiza este proyecto y dame:
1. Estructura de directorios explicada
2. Tecnologías detectadas
3. Patrones de arquitectura usados
4. Posibles mejoras"
```

### Ejercicio 3: Refactoring Asistido

```bash
# Identificar código duplicado
claude "Encuentra código duplicado en src/ y sugiere abstracciones"

# Aplicar refactoring
claude "Aplica el refactoring sugerido, asegurándote de mantener los tests pasando"
```

### Ejercicio 4: Generación de Tests

```bash
# Generar tests para un módulo
claude "Genera tests unitarios para src/services/auth.ts
con cobertura mínima del 80%"

# Verificar tests
claude "Ejecuta los tests y corrige cualquier fallo"
```

### Ejercicio 5: Debugging

```bash
# Analizar un error
cat logs/error.log | claude -p "Analiza este error y sugiere soluciones"

# Fix automático
claude "Aplica el fix para el error anterior y verifica que funcione"
```

### Ejercicio 6: Documentación

```bash
# Generar README
claude "Genera un README.md completo para este proyecto incluyendo:
- Descripción
- Requisitos
- Instalación
- Uso
- API Reference
- Contributing"
```

---

## Recursos Adicionales

- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [Awesome AI CLI Tools](https://github.com/awesome-ai/cli-tools)

---

## Próximo Módulo

En el **Módulo 3: Fundamentos de Software de IA** aprenderás:
- Ventanas de contexto y su gestión
- Model Context Protocol (MCP) en profundidad
- Subagentes y sistemas multi-agente
- Hooks y automatización
