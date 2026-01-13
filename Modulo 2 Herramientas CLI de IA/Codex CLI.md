# Codex CLI (OpenAI)

## Información

| | |
|---|---|
| **Duración** | 20 minutos |
| **Nivel** | Principiante |
| **Requisitos** | Node.js 18+, cuenta OpenAI o ChatGPT Plus |
| **Costo** | Gratis con ChatGPT Plus, o pago por uso con API |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Instalar y configurar Codex CLI
- [ ] Autenticarte con ChatGPT Plus o API key
- [ ] Entender los tres modos de aprobación
- [ ] Usar el comando `codex review` para code reviews
- [ ] Ejecutar tareas en la nube con Cloud Tasks

---

## ¿Por Qué Codex CLI?

| Ventaja | Descripción |
|---------|-------------|
| **Integración ChatGPT** | Si ya pagas ChatGPT Plus, sin costo adicional |
| **Cloud Tasks** | Puede ejecutar tareas en paralelo en la nube |
| **Code Review integrado** | Comando específico para revisiones |

---

## 1. Instalación

```bash
# Via npm
npm install -g @openai/codex

# Verificar
codex --version
```

### Alternativas

```bash
# Via Homebrew (macOS)
brew install --cask codex

# Via yarn
yarn global add @openai/codex
```

### ⚠️ Error Común: Conflicto con Homebrew

Si tienes Homebrew instalado, puede haber conflicto con el nombre `codex`:

```bash
# Si hay conflicto, desinstalar primero
brew uninstall codex  # Si existe otro package

# Luego instalar la versión correcta
npm install -g @openai/codex
```

---

## 2. Autenticación

### Opción 1: Con cuenta ChatGPT

```bash
codex
# Seleccionar "Sign in with ChatGPT"
# Autoriza en el navegador
```

### Opción 2: API Key

```bash
export OPENAI_API_KEY="sk-..."
```

### 📍 Checkpoint 1

Antes de continuar, verifica:
- [ ] `codex --version` muestra la versión correcta
- [ ] Puedes autenticarte con ChatGPT o API key

---

## 3. Modos de Aprobación

```bash
# Solo sugerencias (no ejecuta nada)
codex --approval-mode suggest

# Auto-edita archivos, confirma comandos
codex --approval-mode auto-edit

# Todo automático (¡cuidado!)
codex --approval-mode full-auto
```

### Diagrama de modos

```
┌─────────────────────────────────────────────────────────────┐
│  MODOS DE APROBACIÓN                                         │
│                                                              │
│  Seguro ◄─────────────────────────────────────────► Rápido  │
│                                                              │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────────┐ │
│  │ suggest  │     │auto-edit │     │     full-auto        │ │
│  │          │     │          │     │                      │ │
│  │Solo      │     │Edita     │     │ Todo automático      │ │
│  │sugiere   │     │archivos  │     │ sin confirmación     │ │
│  └──────────┘     └──────────┘     └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

> 💡 **Recomendación**: Empieza con `suggest` para aprender. Pasa a `auto-edit` cuando entiendas el flujo. Usa `full-auto` solo en entornos de prueba aislados.

### ⚠️ Advertencia: Modo full-auto

**Nunca** uses `--approval-mode full-auto` en:
- Repositorios con código de producción
- Proyectos con acceso a bases de datos reales
- Sistemas donde un error puede ser costoso

---

## 4. Comandos Básicos

### Sesión interactiva

```bash
codex

# Dentro de la sesión:
> Explain this codebase to me
> Fix the failing tests
> Add input validation to the form
```

### Prompt directo

```bash
# Ejecutar prompt
codex "Explain this codebase to me"

# Resumir sesión anterior
codex resume

# Ejecutar script automatizado
codex exec "Run tests and fix failures"
```

---

## 5. Feature Única: Code Review

Codex tiene un comando dedicado para revisiones de código:

```bash
# Review de cambios actuales (staged + unstaged)
codex review

# Review de commit específico
codex review HEAD~3

# Review de los últimos N commits
codex review HEAD~5..HEAD

# Review de PR de GitHub
codex review --pr 123
```

### Ejemplo de output

```
## Code Review Summary

### Security Issues (1)
- **src/api/users.ts:45** - SQL injection vulnerability
  Severity: CRITICAL
  Suggestion: Use parameterized queries

### Performance (2)
- **src/services/data.ts:78** - N+1 query detected
- **src/utils/cache.ts:23** - Cache not invalidated

### Code Quality (3)
- **src/models/user.ts:12** - Unused import
- ...
```

---

## 6. Feature Única: Cloud Tasks

Ejecuta tareas en paralelo en la nube de OpenAI:

```bash
# Ejecutar tests en la nube (paralelo)
codex cloud "Run full test suite" --background

# Ver tareas activas
codex cloud list

# Ver resultado de tarea
codex cloud result <task-id>

# Cancelar tarea
codex cloud cancel <task-id>
```

### Casos de uso

- **Tests extensos**: Ejecutar toda la suite mientras sigues trabajando
- **Análisis grandes**: Revisar todo el codebase en background
- **Migraciones**: Ejecutar scripts de migración monitoreados

---

## 7. Configuración

### Archivo config.toml

```toml
# ~/.codex/config.toml

[model]
default = "gpt-4o"

[features]
web_search_request = true

[sandbox_workspace_write]
network_access = true

[mcp]
servers = ["github", "linear"]
```

---

## 8. Cuándo Elegir Codex

| Escenario | ¿Codex? | Por qué |
|-----------|---------|---------|
| Ya pagas ChatGPT Plus | ✅ Sí | Sin costo adicional |
| Necesitas code review | ✅ Sí | Comando dedicado |
| Tareas paralelas | ✅ Sí | Cloud tasks |
| Razonamiento complejo | ❌ No | Claude superior |
| Contexto masivo | ❌ No | Gemini tiene 1M |

---

## 📍 Checkpoint Final

Verifica que puedes:
- [ ] Ejecutar `codex --version`
- [ ] Autenticarte con ChatGPT o API key
- [ ] Ejecutar `codex review` en un proyecto con cambios Git
- [ ] Entender los tres modos de aprobación
- [ ] Saber cuándo elegir Codex sobre otras CLIs

---

## Resumen

| Aspecto | Codex CLI |
|---------|-----------|
| **Mejor para** | Usuarios de ChatGPT Plus, code reviews, tareas paralelas |
| **Feature única** | `codex review` y Cloud Tasks |
| **Costo** | Gratis con ChatGPT Plus |
| **Limitación** | Razonamiento menos profundo que Claude |

---

## Recursos

- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [OpenAI Platform](https://platform.openai.com/)
- [ChatGPT Plus](https://chat.openai.com/) (para suscripción)
