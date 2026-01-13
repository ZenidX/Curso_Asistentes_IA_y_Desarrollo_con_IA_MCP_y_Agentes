# Módulo 2: Herramientas CLI de IA para Coding

## Información del Módulo

| | |
|---|---|
| **Duración estimada** | 3-4 horas |
| **Nivel** | Principiante-Intermedio |
| **Prerrequisitos** | Módulo 1 completado, terminal básica |

---

## Contenido del Módulo

| Archivo | Herramienta | Descripción |
|---------|-------------|-------------|
| [Claude Code.md](Claude%20Code.md) | Claude Code | CLI oficial de Anthropic |
| [Gemini CLI.md](Gemini%20CLI.md) | Gemini CLI | CLI open source de Google |
| [Codex CLI.md](Codex%20CLI.md) | Codex CLI | CLI de OpenAI con cloud tasks |
| [OpenCode.md](OpenCode.md) | OpenCode | CLI open source multi-proveedor |

---

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. ✅ Instalar y configurar Claude Code, Gemini CLI, Codex CLI y OpenCode
2. ✅ Ejecutar comandos básicos e interactuar con tu codebase via CLI
3. ✅ Crear archivos de contexto (CLAUDE.md, AGENTS.md) para personalizar el comportamiento
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

## 2. Comparativa de CLIs

### Tabla de Decisión Rápida

| Si necesitas... | Usa | Razón |
|-----------------|-----|-------|
| Mejor razonamiento | Claude Code | Superior en lógica compleja |
| Máximo contexto | Gemini CLI | 1M tokens |
| Costo $0 | Gemini CLI / OpenCode | Tier gratuito generoso |
| Multi-proveedor | OpenCode | Soporta todos los LLMs |
| Open Source completo | OpenCode | 100% código abierto |
| Integración ChatGPT | Codex CLI | Mismo ecosistema |
| Tareas paralelas cloud | Codex CLI | Cloud tasks |
| MCP avanzado | Claude Code | Mejor soporte |

### Tabla Comparativa Detallada

| Característica | Claude Code | Gemini CLI | Codex CLI | OpenCode |
|----------------|-------------|------------|-----------|----------|
| **Empresa** | Anthropic | Google | OpenAI | Open Source |
| **Precio** | API pay-as-you-go | Gratis (límites) | Suscripción ChatGPT | Gratis + API keys |
| **Open Source** | Parcial | ✅ Completo | Parcial | ✅ Completo |
| **Contexto máx** | 200K tokens | 1M tokens | 128K tokens | Depende del modelo |
| **MCP Support** | ✅ Cliente y servidor | ✅ Cliente | ✅ Cliente | ✅ Cliente |
| **Multi-modelo** | Solo Claude | Solo Gemini | Solo GPT | ✅ Todos |
| **TUI** | Básica | Básica | Básica | ✅ Avanzada |
| **Archivo contexto** | CLAUDE.md | GEMINI.md | .codex/ | AGENTS.md |

### Recomendación del Curso

Para seguir este curso, recomendamos **Claude Code** porque:
1. Los módulos 4-5 usan MCP extensivamente
2. El razonamiento superior ayuda en arquitectura (módulo 6)
3. Es la herramienta principal del instructor

**OpenCode** es excelente alternativa si:
- Quieres usar múltiples proveedores
- Prefieres soluciones 100% open source
- Necesitas trabajar offline con modelos locales

---

## 3. Ejercicios Prácticos

### Ejercicio 1: Setup Completo (30 min)
**Nivel: Básico**

1. Instala al menos dos CLIs de tu elección
2. Clona un proyecto de ejemplo
3. Crea el archivo de contexto correspondiente
4. Ejecuta un análisis del proyecto en ambas
5. Compara las respuestas

### Ejercicio 2: Comparativa de CLIs (20 min)
**Nivel: Básico**

1. Ejecuta el mismo prompt en las CLIs instaladas:
   ```
   "Analiza src/ y sugiere mejoras de performance"
   ```
2. Documenta las diferencias en:
   - Tiempo de respuesta
   - Profundidad del análisis
   - Sugerencias concretas

### Ejercicio 3: Refactoring Asistido (45 min)
**Nivel: Intermedio**

1. Identifica un archivo con código duplicado
2. Pide a la CLI que lo detecte
3. Solicita la refactorización
4. Revisa los cambios antes de aceptar
5. Ejecuta tests para verificar

---

## 4. Troubleshooting Común

### "Rate limit exceeded"

**Causa**: Demasiados requests en poco tiempo.

**Solución**:
- Esperar unos minutos
- Usar modelo más económico
- Considerar OpenCode con modelos locales

### "Context length exceeded"

**Causa**: El proyecto es muy grande para el contexto.

**Solución**:
- Usar comando de compactación (`/compact`)
- Usar Gemini CLI (1M tokens)
- Limitar el scope del análisis

### "Command not found"

**Solución**:
```bash
# Verificar instalación
npm list -g

# Reinstalar
npm uninstall -g <paquete>
npm install -g <paquete>

# Reiniciar terminal
```

---

## Resumen del Módulo

### Lo que aprendiste

1. **Por qué CLIs > Chat web**: Integración, contexto, automatización
2. **Claude Code**: Mejor razonamiento, MCP nativo
3. **Gemini CLI**: Tier gratuito, contexto masivo
4. **Codex CLI**: Cloud tasks, code review integrado
5. **OpenCode**: Multi-proveedor, 100% open source
6. **Cuándo usar cada una**: Tabla de decisión

### Preparación para el Módulo 3

En el próximo módulo aprenderás:
- Cómo funcionan las ventanas de contexto internamente
- Model Context Protocol (MCP) en profundidad
- Subagentes y sistemas multi-agente
- Hooks para automatización

**Tarea previa**: Ten al menos una CLI instalada y funcionando.

---

## Recursos Adicionales

- [Documentación Claude Code](https://docs.anthropic.com/claude-code)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [OpenCode Docs](https://opencode.ai/docs/)
- [OpenCode GitHub](https://github.com/opencode-ai/opencode)
