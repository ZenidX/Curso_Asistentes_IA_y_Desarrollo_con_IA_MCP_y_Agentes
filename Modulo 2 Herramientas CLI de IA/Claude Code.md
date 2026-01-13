# Claude Code (Anthropic)

## Información

| | |
|---|---|
| **Duración** | 45 minutos |
| **Nivel** | Principiante |
| **Requisitos** | Node.js 18+, cuenta Anthropic |
| **Costo** | Pago por uso (API) o incluido en suscripción |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Instalar y autenticar Claude Code
- [ ] Usar los tres modos de operación (Normal, Auto-accept, YOLO)
- [ ] Dominar los comandos slash esenciales
- [ ] Crear un archivo CLAUDE.md para tu proyecto
- [ ] Crear comandos personalizados reutilizables

---

## ¿Por Qué Claude Code?

Claude Code es la CLI oficial de Anthropic. Sus fortalezas:

| Ventaja | Descripción |
|---------|-------------|
| **Mejor razonamiento** | Claude destaca en entender código complejo |
| **Más seguro** | Pide confirmación antes de acciones destructivas |
| **MCP nativo** | Integración profunda con Model Context Protocol |

---

## 1. Instalación

### Windows (PowerShell como Administrador)

```powershell
# Opción 1: Instalador oficial
irm https://claude.ai/install.ps1 | iex

# Opción 2: Via npm (requiere Node.js)
npm install -g @anthropic-ai/claude-code
```

### macOS / Linux

```bash
# Instalador oficial
curl -fsSL https://claude.ai/install.sh | bash

# Via npm
npm install -g @anthropic-ai/claude-code
```

### Verificar instalación

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

---

## 2. Primera Ejecución y Autenticación

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

## 3. Modos de Operación

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

### Modo Normal (Recomendado para aprender)

```bash
claude
# Pide confirmación para cada acción
```

### Modo Auto-Accept

```bash
claude --auto-accept
# Acepta ediciones de archivos automáticamente
# PERO sigue pidiendo confirmación para comandos shell
```

### Modo YOLO (¡Cuidado!)

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

## 4. Comandos Esenciales

### Prompt Interactivo

```bash
# Iniciar sesión interactiva
claude

# Ya dentro de la sesión, simplemente escribe:
> Explica la estructura de este proyecto
> ¿Qué hace la función authenticateUser?
> Añade validación de email al formulario de registro
```

### Prompt Directo (One-shot)

```bash
# Ejecutar un prompt y salir
claude "Resume los cambios del último commit"

# Con archivo de entrada (útil para logs)
cat error.log | claude -p "Explica este error y sugiere solución"
```

### Comandos Slash

Dentro de la sesión interactiva:

| Comando | Qué hace | Cuándo usarlo |
|---------|----------|---------------|
| `/help` | Muestra todos los comandos | Cuando no recuerdes algo |
| `/model` | Cambia el modelo | Si necesitas más potencia (Opus) o velocidad (Haiku) |
| `/clear` | Limpia el contexto | Cuando cambies de tarea |
| `/cost` | Muestra el costo acumulado | Para controlar gastos |
| `/compact` | Comprime el contexto | Cuando la conversación es muy larga |
| `/mcp` | Lista servidores MCP | Para verificar integraciones |

---

## 5. El Archivo CLAUDE.md: Tu Contexto Personalizado

### ¿Por qué es importante?

Sin contexto, Claude tiene que "adivinar" cómo es tu proyecto cada vez. Con `CLAUDE.md`, le das información permanente.

### Dónde crearlo

```
tu-proyecto/
├── CLAUDE.md          ← Aquí (raíz del proyecto)
├── src/
├── tests/
└── package.json
```

### Estructura Recomendada

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

## 6. Comandos Personalizados

Puedes crear "recetas" reutilizables en `.claude/commands/`.

### Ejemplo: Comando de Code Review

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

### Ejemplo: Comando de Nuevo Endpoint

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

## 7. Práctica Guiada

### Analizar un Proyecto

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

## 📍 Checkpoint Final

Antes de continuar, verifica:
- [ ] Puedes crear y editar un archivo CLAUDE.md
- [ ] Entiendes los tres modos de operación
- [ ] Has probado al menos 3 comandos slash
- [ ] Puedes crear un comando personalizado básico
- [ ] Sabes cuándo elegir Claude Code sobre otras CLIs

---

## Resumen

| Aspecto | Claude Code |
|---------|-------------|
| **Mejor para** | Razonamiento complejo, código crítico, MCP |
| **Feature única** | Mejor análisis de código, MCP nativo |
| **Costo** | Pago por uso o suscripción |
| **Limitación** | Contexto menor (200K vs 1M de Gemini) |

---

## Recursos

- [Documentación oficial](https://docs.anthropic.com/claude-code)
- [Claude Code en GitHub](https://github.com/anthropics/claude-code)
