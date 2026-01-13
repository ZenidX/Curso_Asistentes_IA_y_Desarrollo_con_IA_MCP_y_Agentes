# Módulo 2: Herramientas CLI de IA para Coding

## Información del Módulo

| | |
|---|---|
| **Duración estimada** | 3-4 horas |
| **Nivel** | Principiante-Intermedio |
| **Prerrequisitos** | Módulo 1 completado, terminal básica |

---

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. ✅ Instalar y configurar Claude Code, Gemini CLI y Codex CLI
2. ✅ Ejecutar comandos básicos e interactuar con tu codebase via CLI
3. ✅ Crear archivos de contexto (CLAUDE.md, GEMINI.md) para personalizar el comportamiento
4. ✅ Elegir la herramienta adecuada según el caso de uso
5. ✅ Crear comandos personalizados para automatizar tareas repetitivas

---

## El Proyecto del Curso: TaskFlow

A lo largo de los módulos 2-6, construiremos **TaskFlow**, una aplicación de gestión de tareas. En este módulo, usaremos las CLIs de IA para:

- Analizar un proyecto existente
- Generar código nuevo
- Refactorizar código
- Ejecutar y debuggear tests

```
TaskFlow/
├── src/
│   ├── models/       # Modelos de datos
│   ├── services/     # Lógica de negocio
│   └── api/          # Endpoints REST
├── tests/
└── package.json
```

---

## 1. Introducción: ¿Por Qué CLIs de IA?

**⏱️ Tiempo estimado: 15 minutos**

### El Problema

Imagina este escenario cotidiano:

1. Estás programando en VS Code
2. Tienes una duda → abres ChatGPT en el navegador
3. Copias código de tu editor al chat
4. Copias la respuesta de vuelta
5. Repites 20 veces al día

**Tiempo perdido en cambios de contexto: ~1-2 horas/día**

### La Solución

Las CLIs de IA viven en tu terminal. No necesitas cambiar de contexto porque:

```
┌─────────────────────────────────────────────────────────────┐
│  Tu Terminal                                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ $ claude "Explica qué hace src/services/auth.ts"        ││
│  │                                                          ││
│  │ El archivo implementa la autenticación JWT...           ││
│  │ [Lee el archivo automáticamente, sin que copies nada]   ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Comparativa: Chat Web vs CLI

| Aspecto | Chat Web | CLI de IA |
|---------|----------|-----------|
| Acceso a archivos | Manual (copiar/pegar) | Automático |
| Ejecutar comandos | No puede | Sí |
| Contexto del proyecto | Limitado | Completo |
| Flujo de trabajo | Interrumpido | Integrado |
| Automatización | Imposible | Total |

### 💡 Concepto Clave

> **Agente de Coding**: Un LLM que no solo responde preguntas, sino que puede **leer archivos**, **escribir código**, **ejecutar comandos** y **verificar resultados**. Es como tener un programador junior en tu terminal que nunca se cansa.

---

## 2. Claude Code (Anthropic)

**⏱️ Tiempo estimado: 45 minutos**

### ¿Por Qué Claude Code?

Claude Code es la CLI oficial de Anthropic. Sus fortalezas:

- **Mejor razonamiento**: Claude destaca en entender código complejo
- **Más seguro**: Pide confirmación antes de acciones destructivas
- **MCP nativo**: Integración profunda con Model Context Protocol

### 2.1 Instalación

#### Windows (PowerShell como Administrador)

```powershell
# Opción 1: Instalador oficial
irm https://claude.ai/install.ps1 | iex

# Opción 2: Via npm (requiere Node.js)
npm install -g @anthropic-ai/claude-code
```

#### macOS / Linux

```bash
# Instalador oficial
curl -fsSL https://claude.ai/install.sh | bash

# Via npm
npm install -g @anthropic-ai/claude-code
```

#### Verificar instalación

```bash
claude --version
# Debería mostrar: claude-code v1.x.x
```

### ⚠️ Error Común: "claude no reconocido"

**Síntoma**: `'claude' is not recognized as an internal or external command`

**Causa**: La ruta no está en el PATH del sistema.

**Solución**:
```bash
# Ver dónde se instaló
npm list -g @anthropic-ai/claude-code

# Añadir al PATH (ejemplo Windows)
# Panel de Control → Sistema → Variables de entorno → Path → Añadir ruta
```

### 2.2 Primera Ejecución y Autenticación

```bash
# Iniciar Claude Code
claude

# Te pedirá autenticarte:
# 1. Abre el enlace en tu navegador
# 2. Inicia sesión con tu cuenta de Anthropic
# 3. Autoriza el acceso
```

**Alternativa: API Key manual**

```bash
# En tu .bashrc, .zshrc o variables de entorno Windows
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"
```

### 📍 Checkpoint 1

Antes de continuar, verifica que puedes:
- [ ] Ejecutar `claude --version` sin errores
- [ ] Iniciar `claude` y ver el prompt interactivo
- [ ] Autenticarte correctamente

---

### 2.3 Modos de Operación

Claude Code tiene tres niveles de autonomía:

```
┌─────────────────────────────────────────────────────────────┐
│  NIVEL DE AUTONOMÍA                                          │
│                                                              │
│  Seguro ◄─────────────────────────────────────────► Rápido  │
│                                                              │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────────┐ │
│  │  Normal  │     │Auto-edit │     │ YOLO (Peligroso!)    │ │
│  │          │     │          │     │                      │ │
│  │ Confirma │     │ Edita    │     │ Hace todo sin        │ │
│  │ todo     │     │ archivos │     │ preguntar            │ │
│  │          │     │ auto     │     │                      │ │
│  └──────────┘     └──────────┘     └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Modo Normal (Recomendado para aprender)

```bash
claude
# Pide confirmación para cada acción
```

#### Modo Auto-Accept

```bash
claude --auto-accept
# Acepta ediciones de archivos automáticamente
# PERO sigue pidiendo confirmación para comandos shell
```

#### Modo YOLO (¡Cuidado!)

```bash
claude --dangerously-skip-permissions
# Ejecuta TODO sin confirmación
# Solo para scripts automatizados en entornos controlados
```

### ⚠️ Error Común: Ejecutar YOLO en producción

**Nunca** uses `--dangerously-skip-permissions` con acceso a:
- Repositorios con código de producción
- Bases de datos reales
- Sistemas de archivos críticos

Un simple "borra los archivos temporales" podría interpretarse mal.

---

### 2.4 Comandos Esenciales

#### Prompt Interactivo

```bash
# Iniciar sesión interactiva
claude

# Ya dentro de la sesión, simplemente escribe:
> Explica la estructura de este proyecto
> ¿Qué hace la función authenticateUser?
> Añade validación de email al formulario de registro
```

#### Prompt Directo (One-shot)

```bash
# Ejecutar un prompt y salir
claude "Resume los cambios del último commit"

# Con archivo de entrada (útil para logs)
cat error.log | claude -p "Explica este error y sugiere solución"
```

#### Comandos Slash

Dentro de la sesión interactiva:

| Comando | Qué hace | Cuándo usarlo |
|---------|----------|---------------|
| `/help` | Muestra todos los comandos | Cuando no recuerdes algo |
| `/model` | Cambia el modelo | Si necesitas más potencia (Opus) o velocidad (Haiku) |
| `/clear` | Limpia el contexto | Cuando cambies de tarea |
| `/cost` | Muestra el costo acumulado | Para controlar gastos |
| `/compact` | Comprime el contexto | Cuando la conversación es muy larga |
| `/mcp` | Lista servidores MCP | Para verificar integraciones |

### 🎯 Práctica Guiada 1: Analizar un Proyecto

Vamos a practicar con un proyecto real. Si no tienes uno a mano:

```bash
# Clonar proyecto de ejemplo
git clone https://github.com/expressjs/express.git
cd express

# Iniciar Claude Code
claude

# Prueba estos prompts:
> ¿Cuál es la estructura de este proyecto?
> ¿Qué patrones de diseño usa?
> Explica cómo funciona el middleware
```

**Observa cómo Claude**:
1. Lee automáticamente los archivos relevantes
2. Navega la estructura del proyecto
3. Conecta conceptos entre archivos

---

### 2.5 El Archivo CLAUDE.md: Tu Contexto Personalizado

**¿Por qué es importante?**

Sin contexto, Claude tiene que "adivinar" cómo es tu proyecto cada vez. Con `CLAUDE.md`, le das información permanente.

#### Dónde crearlo

```
tu-proyecto/
├── CLAUDE.md          ← Aquí (raíz del proyecto)
├── src/
├── tests/
└── package.json
```

#### Estructura Recomendada

```markdown
# Proyecto: TaskFlow

## Descripción
Aplicación de gestión de tareas con API REST y frontend React.

## Stack Tecnológico
- **Backend**: Node.js 20, Express 4.x, TypeScript 5.x
- **Base de datos**: PostgreSQL 15 + Prisma ORM
- **Frontend**: React 18, TailwindCSS
- **Testing**: Jest + React Testing Library

## Estructura del Proyecto
src/
├── api/          # Controladores Express
├── services/     # Lógica de negocio
├── models/       # Modelos Prisma
├── middleware/   # Auth, validación, etc.
└── utils/        # Helpers compartidos

## Convenciones de Código
- **Nombrado**: camelCase para variables, PascalCase para clases/componentes
- **Commits**: Conventional Commits (feat:, fix:, docs:, etc.)
- **Branches**: feature/*, bugfix/*, hotfix/*

## Comandos Principales
- `npm run dev` - Servidor de desarrollo
- `npm test` - Ejecutar tests
- `npm run lint` - Verificar estilo
- `npm run build` - Build de producción

## Reglas Específicas
- Siempre usar TypeScript strict mode
- Todos los endpoints deben tener tests
- No usar `any` - buscar tipos correctos
- Preferir composición sobre herencia

## Contexto de Negocio
- Los usuarios pueden tener máximo 100 tareas activas
- Las tareas archivadas se eliminan después de 30 días
- El API tiene rate limiting de 100 req/min por usuario
```

### 💡 Tip: Evoluciona tu CLAUDE.md

Cada vez que expliques algo a Claude que debería "recordar", añádelo al CLAUDE.md:

```bash
# Durante una sesión
> Las tareas usan soft-delete, nunca DELETE real

# Después, añade a CLAUDE.md:
## Notas Importantes
- Usamos soft-delete: campo `deleted_at` en lugar de DELETE
```

---

### 2.6 Comandos Personalizados

Puedes crear "recetas" reutilizables en `.claude/commands/`.

#### Ejemplo: Comando de Code Review

```markdown
# .claude/commands/review.md

# Code Review Exhaustivo

Realiza un code review del código actual con este checklist:

## 1. Seguridad (CRÍTICO)
- [ ] ¿Hay inyección SQL posible?
- [ ] ¿Se validan todos los inputs del usuario?
- [ ] ¿Los secretos están en variables de entorno?
- [ ] ¿Se sanitiza output para prevenir XSS?

## 2. Performance
- [ ] ¿Hay consultas N+1?
- [ ] ¿Se usa paginación para listas grandes?
- [ ] ¿Hay operaciones bloqueantes en async?

## 3. Calidad
- [ ] ¿Hay código duplicado?
- [ ] ¿Los nombres son descriptivos?
- [ ] ¿Las funciones tienen una sola responsabilidad?

## 4. Testing
- [ ] ¿Hay tests para los casos principales?
- [ ] ¿Se testean los edge cases?

## Formato de Salida
Para cada problema:
- **Archivo:línea**: descripción
- **Severidad**: CRÍTICO | ALTO | MEDIO | BAJO
- **Sugerencia**: cómo arreglarlo
```

**Uso**:
```bash
claude
> /project:review
```

#### Ejemplo: Comando de Nuevo Endpoint

```markdown
# .claude/commands/new-endpoint.md

# Crear Nuevo Endpoint REST

Crea un nuevo endpoint siguiendo nuestras convenciones:

## Parámetros necesarios
- **Recurso**: $ARGUMENTS (ej: "users", "tasks")

## Archivos a crear
1. `src/api/{recurso}.controller.ts` - Controlador
2. `src/services/{recurso}.service.ts` - Servicio
3. `tests/{recurso}.test.ts` - Tests

## Plantilla de Controlador
- Usar decoradores de validación
- Manejar errores con try/catch
- Documentar con JSDoc

## Plantilla de Test
- Mínimo 5 tests: CRUD + error case
- Usar factories para datos de prueba

Genera el código siguiendo estas pautas.
```

**Uso**:
```bash
claude
> /project:new-endpoint tasks
```

---

### 📍 Checkpoint 2

Antes de pasar a Gemini CLI, verifica:
- [ ] Puedes crear y editar un archivo CLAUDE.md
- [ ] Entiendes los tres modos de operación
- [ ] Has probado al menos 3 comandos slash
- [ ] Puedes crear un comando personalizado básico

---

## 3. Gemini CLI (Google)

**⏱️ Tiempo estimado: 30 minutos**

### ¿Por Qué Gemini CLI?

- **Gratis**: Tier gratuito muy generoso (1000 requests/día)
- **Contexto masivo**: 1 millón de tokens (vs 200K de Claude)
- **Open Source**: Código completamente abierto

### 3.1 Instalación

```bash
# Via npm
npm install -g @google/gemini-cli

# Verificar
gemini --version
```

### 3.2 Límites del Tier Gratuito

| Recurso | Límite |
|---------|--------|
| Requests por minuto | 60 |
| Requests por día | 1,000 |
| Tokens de contexto | 1,000,000 |
| Modelo | Gemini 2.5 Pro |

**Cálculo práctico**: 1000 req/día ÷ 8 horas = **125 prompts/hora**. Más que suficiente para desarrollo normal.

### 3.3 Comandos Básicos

```bash
# Sesión interactiva
gemini

# Prompt directo
gemini "Analiza este proyecto"

# Con formato de salida
gemini -p "Lista las dependencias" --output-format json
```

### 3.4 Cuándo Elegir Gemini sobre Claude

| Escenario | Mejor opción | Por qué |
|-----------|--------------|---------|
| Proyecto con muchos archivos | Gemini | Contexto de 1M tokens |
| Análisis de monorepos | Gemini | Puede "ver" más código |
| Presupuesto limitado | Gemini | Tier gratuito |
| Razonamiento complejo | Claude | Mejor en lógica |
| Código crítico/seguro | Claude | Más conservador |

### 🎯 Práctica Guiada 2: Comparar CLIs

Ejecuta el mismo prompt en ambas CLIs y compara:

```bash
# En un proyecto mediano
cd tu-proyecto

# Con Claude
claude "Identifica los 3 mayores problemas de arquitectura"

# Con Gemini
gemini "Identifica los 3 mayores problemas de arquitectura"
```

**Observa**:
- ¿Cuál da respuestas más detalladas?
- ¿Cuál es más rápido?
- ¿Las recomendaciones son similares?

---

## 4. Codex CLI (OpenAI)

**⏱️ Tiempo estimado: 20 minutos**

### ¿Por Qué Codex CLI?

- **Integración ChatGPT**: Si ya pagas ChatGPT Plus, sin costo adicional
- **Cloud Tasks**: Puede ejecutar tareas en paralelo en la nube
- **Code Review integrado**: Comando específico para revisiones

### 4.1 Instalación

```bash
npm install -g @openai/codex
codex --version
```

### 4.2 Autenticación

```bash
codex
# Seleccionar "Sign in with ChatGPT"
# O usar API key:
export OPENAI_API_KEY="sk-..."
```

### 4.3 Modos de Aprobación

```bash
# Solo sugerencias (no ejecuta nada)
codex --approval-mode suggest

# Auto-edita archivos, confirma comandos
codex --approval-mode auto-edit

# Todo automático
codex --approval-mode full-auto
```

### 4.4 Feature Única: Code Review

```bash
# Review de cambios actuales
codex review

# Review de commit específico
codex review HEAD~3

# Review de PR de GitHub
codex review --pr 123
```

### 4.5 Feature Única: Cloud Tasks

```bash
# Ejecutar tests en la nube (paralelo)
codex cloud "Run full test suite" --background

# Ver tareas activas
codex cloud list

# Ver resultado
codex cloud result <task-id>
```

---

## 5. Comparativa Final: ¿Cuál Elegir?

**⏱️ Tiempo estimado: 10 minutos**

### Tabla de Decisión

| Si necesitas... | Usa | Razón |
|-----------------|-----|-------|
| Mejor razonamiento | Claude Code | Superior en lógica compleja |
| Máximo contexto | Gemini CLI | 1M tokens |
| Costo $0 | Gemini CLI | Tier gratuito generoso |
| Integración ChatGPT | Codex CLI | Mismo ecosistema |
| Tareas paralelas | Codex CLI | Cloud tasks |
| MCP avanzado | Claude Code | Mejor soporte |

### Recomendación del Curso

Para seguir este curso, recomendamos **Claude Code** porque:
1. Los módulos 4-5 usan MCP extensivamente
2. El razonamiento superior ayuda en arquitectura (módulo 6)
3. Es la herramienta principal del instructor

Pero **cualquiera funciona** para los ejercicios básicos.

---

## 6. Ejercicios Prácticos

### Ejercicio 1: Setup Completo (30 min)
**Nivel: Básico**

1. Instala Claude Code (o Gemini CLI)
2. Clona el proyecto de ejemplo: `git clone https://github.com/your/taskflow-starter`
3. Crea un archivo CLAUDE.md con la información del proyecto
4. Ejecuta: `claude "Explica este codebase"`
5. Verifica que entiende la estructura

**Criterio de éxito**: Claude describe correctamente las carpetas y tecnologías.

### Ejercicio 2: Refactoring Asistido (45 min)
**Nivel: Intermedio**

1. Identifica un archivo con código duplicado
2. Pide a Claude que lo detecte: `"Encuentra código duplicado en src/"`
3. Pide la refactorización: `"Refactoriza para eliminar la duplicación"`
4. Revisa los cambios antes de aceptar
5. Ejecuta tests para verificar

**Criterio de éxito**: Los tests siguen pasando después del refactor.

### Ejercicio 3: Comando Personalizado (30 min)
**Nivel: Intermedio**

Crea un comando `/project:security-check` que:
1. Busque secrets hardcodeados
2. Verifique dependencias con vulnerabilidades
3. Revise configuración de CORS
4. Genere un informe en formato markdown

**Criterio de éxito**: El comando genera un informe útil.

### Ejercicio 4: Comparativa de CLIs (20 min)
**Nivel: Básico**

1. Instala Gemini CLI además de Claude Code
2. Ejecuta el mismo prompt en ambas:
   ```
   "Analiza src/services/ y sugiere mejoras de performance"
   ```
3. Documenta las diferencias en:
   - Tiempo de respuesta
   - Profundidad del análisis
   - Sugerencias concretas

**Criterio de éxito**: Tienes una opinión informada sobre cuál prefieres.

---

## 7. Troubleshooting

### Problemas Comunes

#### "Rate limit exceeded"

**Causa**: Demasiados requests en poco tiempo.

**Solución**:
```bash
# Esperar unos minutos, o
# Usar modo más eficiente (menos requests):
claude --model haiku  # Más rápido, menos límites
```

#### "Context length exceeded"

**Causa**: El proyecto es muy grande para el contexto.

**Solución**:
```bash
# Usar /compact
claude
> /compact

# O usar Gemini para proyectos grandes
gemini "Analiza el proyecto"  # 1M tokens de contexto
```

#### "Command not found" después de instalar

**Solución**:
```bash
# Verificar instalación global
npm list -g

# Reinstalar
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code

# Reiniciar terminal
```

---

## Resumen del Módulo

### Lo que aprendiste

1. **Por qué CLIs > Chat web**: Integración, contexto, automatización
2. **Claude Code**: Instalación, modos, CLAUDE.md, comandos
3. **Gemini CLI**: Tier gratuito, contexto masivo
4. **Codex CLI**: Cloud tasks, code review integrado
5. **Cuándo usar cada una**: Tabla de decisión

### Preparación para el Módulo 3

En el próximo módulo aprenderás:
- Cómo funcionan las ventanas de contexto internamente
- Model Context Protocol (MCP) en profundidad
- Subagentes y sistemas multi-agente
- Hooks para automatización

**Tarea previa**: Ten Claude Code instalado y funcionando. Lo usaremos intensivamente.

---

## Recursos Adicionales

- [Documentación oficial Claude Code](https://docs.anthropic.com/claude-code)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [Comparativa actualizada de CLIs](https://github.com/anthropics/claude-code/wiki/CLI-Comparison)
