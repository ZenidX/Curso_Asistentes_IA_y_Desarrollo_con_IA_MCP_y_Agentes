# OpenCode

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Principiante |
| **Requisitos** | Terminal moderna, API key de cualquier proveedor |
| **Costo** | Open source (pagas solo por los LLMs que uses) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Instalar OpenCode en tu sistema operativo
- [ ] Configurar múltiples proveedores de IA
- [ ] Usar los modos Plan y Build efectivamente
- [ ] Crear un archivo AGENTS.md para tu proyecto
- [ ] Usar modelos locales con Ollama

---

## ¿Por Qué OpenCode?

OpenCode es una alternativa **100% open source** a Claude Code que destaca por:

| Ventaja | Descripción |
|---------|-------------|
| **Multi-proveedor** | Soporta OpenAI, Anthropic, Google, Groq, Ollama y más |
| **TUI avanzada** | Interfaz de terminal moderna con Bubble Tea |
| **Sin vendor lock-in** | Usa cualquier modelo, incluso locales |
| **Privacidad** | No almacena tu código en servidores externos |

---

## 1. Instalación

### Script de instalación (Recomendado)

```bash
curl -fsSL https://opencode.ai/install | bash
```

### Via npm

```bash
npm install -g opencode-ai
```

### Windows

```powershell
# Scoop
scoop bucket add extras
scoop install extras/opencode

# Chocolatey
choco install opencode
```

### macOS (Homebrew)

```bash
brew install anomalyco/tap/opencode
```

### Verificar instalación

```bash
opencode --version
```

### ⚠️ Error Común: Permisos en Windows

**Síntoma**: Error de permisos al instalar con script curl

**Solución**:
```powershell
# Usar PowerShell como Administrador
# O instalar via Scoop/Chocolatey (no requiere admin)
scoop install extras/opencode
```

### 📍 Checkpoint 1

Antes de continuar, verifica:
- [ ] `opencode --version` funciona correctamente
- [ ] Tienes al menos una API key de cualquier proveedor

---

## 2. Configuración Inicial

### Conectar con OpenCode Zen (más fácil)

```bash
opencode
# Ejecuta /connect
# Autentícate en opencode.ai/auth
# Configura billing (hay tier gratuito)
```

### Usar tu propia API key

```bash
# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# Google
export GOOGLE_API_KEY="AIza..."

# Múltiples a la vez - OpenCode detecta automáticamente
```

---

## 3. Proveedores Soportados

| Proveedor | Modelos | Configuración |
|-----------|---------|---------------|
| **OpenAI** | GPT-4o, GPT-4, GPT-3.5 | `OPENAI_API_KEY` |
| **Anthropic** | Claude 3.5, Claude 3 | `ANTHROPIC_API_KEY` |
| **Google** | Gemini Pro, Flash | `GOOGLE_API_KEY` |
| **Groq** | Llama, Mixtral | `GROQ_API_KEY` |
| **AWS Bedrock** | Claude, Titan | AWS credentials |
| **Azure OpenAI** | GPT-4, GPT-3.5 | Azure credentials |
| **Ollama** | Cualquier modelo local | `OLLAMA_HOST` |
| **OpenRouter** | 100+ modelos | `OPENROUTER_API_KEY` |

> 💡 **Concepto clave**: OpenCode detecta automáticamente las API keys configuradas. Puedes tener múltiples proveedores y cambiar entre ellos con `/model` sin reconfigurar nada.

---

## 4. Interfaz TUI

OpenCode tiene una interfaz de terminal avanzada:

```
┌─────────────────────────────────────────────────────────────┐
│  OpenCode                                      Claude 3.5   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  > Analiza este proyecto y sugiere mejoras                  │
│                                                             │
│  Analizando estructura del proyecto...                      │
│  ├── src/                                                   │
│  ├── tests/                                                 │
│  └── package.json                                           │
│                                                             │
│  ## Sugerencias de mejora:                                  │
│  1. Añadir TypeScript para type safety                      │
│  2. Configurar ESLint + Prettier                            │
│  3. ...                                                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [Tab] Plan/Build  [@] Files  [/] Commands  [?] Help        │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Comandos Principales

### Comandos Slash

| Comando | Función |
|---------|---------|
| `/init` | Analiza el proyecto y genera `AGENTS.md` |
| `/undo` | Revierte cambios (repetible) |
| `/redo` | Restaura cambios deshechos |
| `/share` | Crea enlace compartible de la conversación |
| `/connect` | Conecta con OpenCode Zen |
| `/model` | Cambia el modelo activo |

### Atajos de teclado

| Tecla | Función |
|-------|---------|
| `Tab` | Alterna entre modo Plan y Build |
| `@` | Búsqueda fuzzy de archivos |
| `/` | Abre menú de comandos |
| `Ctrl+C` | Cancela operación actual |
| `Ctrl+Z` | Undo rápido |

---

## 6. Modos de Operación

### Modo Plan (Pensar)

```bash
# Activa con Tab o automáticamente al planificar
> Diseña la arquitectura para un sistema de notificaciones

# OpenCode:
# - Analiza el codebase
# - Propone arquitectura
# - NO hace cambios aún
```

### Modo Build (Ejecutar)

```bash
# Activa con Tab después de planificar
> Implementa el plan

# OpenCode:
# - Crea archivos
# - Modifica código
# - Ejecuta comandos
```

> 💡 **Tip**: El flujo recomendado es: Plan primero (para que la IA piense), luego Build (para ejecutar). Esto reduce errores porque la IA planifica antes de actuar.

---

## 7. Archivo AGENTS.md

OpenCode usa `AGENTS.md` como archivo de contexto (similar a CLAUDE.md):

```markdown
# AGENTS.md

## Proyecto
Aplicación de e-commerce con Next.js

## Stack
- Next.js 14 (App Router)
- Prisma + PostgreSQL
- TailwindCSS
- Stripe para pagos

## Convenciones
- Componentes en PascalCase
- Hooks personalizados con prefijo `use`
- Server Actions para mutaciones

## Comandos
- `npm run dev` - Desarrollo
- `npm run test` - Tests
- `npm run db:push` - Sync schema
```

### Generar automáticamente

```bash
opencode
> /init
# Analiza el proyecto y genera AGENTS.md
```

---

## 8. Uso No Interactivo

Para scripts y automatización:

```bash
# Prompt directo
opencode "Explica este proyecto" --non-interactive

# Desde stdin
cat error.log | opencode "Analiza este error" --non-interactive

# Con modelo específico
opencode "Genera tests" --model claude-3-5-sonnet --non-interactive
```

---

## 9. Modelos Locales con Ollama

OpenCode funciona completamente offline con Ollama:

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Descargar modelo
ollama pull llama3.2
ollama pull codellama

# 3. Usar en OpenCode
export OLLAMA_HOST="http://localhost:11434"
opencode
> /model ollama/llama3.2
```

### Ventajas de modelos locales

- **Privacidad total**: Tu código nunca sale de tu máquina
- **Sin costos**: Gratis después de descargar
- **Sin límites**: Sin rate limiting
- **Offline**: Funciona sin internet

---

## 10. Cuándo Elegir OpenCode

| Escenario | ¿OpenCode? | Por qué |
|-----------|------------|---------|
| Quieres probar múltiples LLMs | ✅ Sí | Multi-proveedor |
| Privacidad es crítica | ✅ Sí | Modelos locales |
| Prefieres open source | ✅ Sí | 100% abierto |
| Necesitas TUI avanzada | ✅ Sí | Bubble Tea |
| Quieres MCP avanzado | ❌ No | Claude Code mejor |
| Usas solo Claude | ❌ No | Claude Code nativo |

---

## 📍 Checkpoint Final

Verifica que puedes:
- [ ] Ejecutar `opencode --version`
- [ ] Configurar al menos un proveedor de IA
- [ ] Usar los modos Plan y Build con Tab
- [ ] Generar un archivo AGENTS.md con `/init`
- [ ] Cambiar entre modelos con `/model`
- [ ] Entender cuándo elegir OpenCode sobre otras CLIs

---

## Resumen

| Aspecto | OpenCode |
|---------|----------|
| **Mejor para** | Flexibilidad, privacidad, multi-proveedor |
| **Feature única** | TUI moderna, soporte Ollama nativo |
| **Costo** | Open source (pagas por los LLMs) |
| **Limitación** | MCP menos maduro que Claude Code |

---

## Recursos

- [OpenCode Website](https://opencode.ai/)
- [OpenCode Docs](https://opencode.ai/docs/)
- [OpenCode GitHub](https://github.com/opencode-ai/opencode)
- [OpenCode Download](https://opencode.ai/download)
