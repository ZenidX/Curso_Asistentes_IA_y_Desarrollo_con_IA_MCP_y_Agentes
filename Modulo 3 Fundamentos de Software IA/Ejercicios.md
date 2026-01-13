# Ejercicios: Módulo 3 - Fundamentos de Software IA

## Información

| | |
|---|---|
| **Dificultad progresiva** | Básico → Intermedio → Avanzado |
| **Tiempo total estimado** | 3-4 horas |
| **Requisitos** | Claude Code funcionando, proyecto de ejemplo |

---

## Ejercicio 1: Calcular tokens

**Nivel**: Básico
**Tiempo**: 20 minutos

### Objetivo
Entender cómo se calculan los tokens y su impacto en el contexto.

### Instrucciones

1. Usa una herramienta de conteo de tokens
2. Analiza diferentes tipos de contenido
3. Estima el uso de contexto de un proyecto

### Práctica

```python
# Usar tiktoken (OpenAI) o similar
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

textos = [
    "Hola mundo",
    "def calculate_average(numbers): return sum(numbers) / len(numbers)",
    "La inteligencia artificial (IA) es un campo de la informática...",
    # Añade más ejemplos
]

for texto in textos:
    tokens = enc.encode(texto)
    print(f"Texto: {texto[:50]}...")
    print(f"Tokens: {len(tokens)}")
    print(f"Ratio chars/token: {len(texto)/len(tokens):.2f}")
    print()
```

### Preguntas a responder

1. ¿Cuántos tokens tiene un archivo de 100 líneas de código?
2. ¿Cuál es el ratio promedio caracteres/token en español?
3. ¿Cabe tu proyecto completo en el contexto de Claude (200K tokens)?

### Criterios de éxito
- [ ] Puedes estimar tokens de cualquier texto
- [ ] Entiendes la relación tokens/palabras
- [ ] Sabes calcular si un proyecto cabe en contexto

---

## Ejercicio 2: Gestión de contexto

**Nivel**: Básico
**Tiempo**: 25 minutos

### Objetivo
Practicar técnicas para optimizar el uso del contexto.

### Instrucciones

1. Carga un proyecto mediano en Claude
2. Observa el uso de contexto con `/cost`
3. Aplica técnicas de optimización
4. Compara antes y después

### Técnicas a probar

```bash
claude

# 1. Ver uso actual
> /cost

# 2. Compactar contexto
> /compact

# 3. Limpiar y empezar nuevo tema
> /clear

# 4. Ser específico en lo que necesitas
> Analiza SOLO el archivo src/auth/login.ts
# vs
> Analiza todo el proyecto
```

### Tabla de comparación

| Técnica | Tokens antes | Tokens después | Reducción |
|---------|--------------|----------------|-----------|
| Compact | | | |
| Scope específico | | | |
| Clear + nuevo | | | |

### Criterios de éxito
- [ ] Conoces los comandos de gestión de contexto
- [ ] Puedes reducir el uso cuando es necesario
- [ ] Entiendes cuándo aplicar cada técnica

---

## Ejercicio 3: Configurar un MCP básico

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Configurar tu primer servidor MCP y verificar su funcionamiento.

### Instrucciones

1. Configura el MCP de Filesystem
2. Verifica que funciona
3. Prueba operaciones básicas

### Configuración

```json
// claude_desktop_config.json o settings.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/ruta/a/tu/proyecto"
      ]
    }
  }
}
```

### Verificación

```bash
claude

# Verificar que el MCP está activo
> /mcp

# Probar operaciones
> Lista los archivos en el directorio raíz
> Lee el contenido de README.md
> Crea un archivo test.txt con el contenido "Hola MCP"
> Elimina el archivo test.txt
```

### Criterios de éxito
- [ ] El MCP aparece en `/mcp`
- [ ] Puedes listar archivos
- [ ] Puedes leer y escribir archivos

---

## Ejercicio 4: MCP con múltiples servidores

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Configurar y usar múltiples MCPs simultáneamente.

### Instrucciones

1. Configura Filesystem + Git MCPs
2. Usa ambos en una sesión
3. Crea un workflow que use los dos

### Configuración

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/mi/proyecto"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/mi/proyecto"]
    }
  }
}
```

### Workflow de ejemplo

```bash
claude

# 1. Verificar estado
> Muestra el estado de Git

# 2. Crear un archivo
> Crea un archivo CHANGELOG.md con los últimos cambios

# 3. Añadir a Git
> Añade CHANGELOG.md al staging

# 4. Crear commit
> Crea un commit con el mensaje "docs: añadir changelog"
```

### Criterios de éxito
- [ ] Ambos MCPs funcionan
- [ ] Puedes usar herramientas de ambos
- [ ] El workflow completo funciona

---

## Ejercicio 5: Memory MCP

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Usar el MCP de memoria para persistir conocimiento entre sesiones.

### Instrucciones

1. Configura Memory MCP
2. Guarda información del proyecto
3. Recupera la información en una nueva sesión

### Configuración

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### Práctica

```bash
# Sesión 1: Guardar información
claude
> Recuerda que el proyecto TaskFlow usa PostgreSQL como base de datos
> Recuerda que el usuario principal se llama "admin@taskflow.com"
> Recuerda que el servidor está en el puerto 3000

# Cerrar y abrir nueva sesión

# Sesión 2: Recuperar
claude
> ¿Qué base de datos usa TaskFlow?
> ¿Cuál es el usuario principal?
> ¿En qué puerto corre el servidor?
```

### Criterios de éxito
- [ ] Memory MCP configurado
- [ ] La información persiste entre sesiones
- [ ] Puedes consultar el conocimiento guardado

---

## Ejercicio 6: Entender subagentes

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Comprender cuándo y cómo se usan los subagentes.

### Instrucciones

1. Identifica tareas que benefician de subagentes
2. Observa cómo Claude divide el trabajo
3. Compara ejecución con y sin subagentes

### Tareas para probar

```bash
claude

# Tarea simple (no necesita subagente)
> ¿Qué hora es?

# Tarea que puede usar subagente
> Analiza todos los archivos .ts del proyecto y genera un informe de calidad

# Tarea compleja (probablemente usa subagentes)
> Encuentra todos los TODOs en el código, crea issues en GitHub para cada uno,
> y genera un resumen en TODOS.md
```

### Observaciones a documentar

1. ¿Cuándo decidió usar subagentes?
2. ¿Cómo dividió el trabajo?
3. ¿Fue más eficiente?

### Criterios de éxito
- [ ] Entiendes cuándo se usan subagentes
- [ ] Puedes identificar tareas candidatas
- [ ] Comprendes los beneficios y limitaciones

---

## Ejercicio 7: Crear un hook básico

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Crear hooks para automatizar acciones en Claude Code.

### Instrucciones

1. Crea el archivo de configuración de hooks
2. Implementa un hook pre-commit
3. Implementa un hook post-respuesta
4. Prueba los hooks

### Configuración de hooks

```json
// .claude/hooks.json
{
  "hooks": {
    "pre-tool-call": {
      "bash": {
        "command": "echo 'Ejecutando comando bash...' >> /tmp/claude_log.txt"
      }
    },
    "post-response": {
      "match": ".*\\b(TODO|FIXME|HACK)\\b.*",
      "command": "echo 'Se detectó marcador de código' >> /tmp/claude_alerts.txt"
    }
  }
}
```

### Verificación

```bash
# Probar el hook
claude
> Ejecuta 'ls -la'
# Debería registrar en /tmp/claude_log.txt

# Verificar log
cat /tmp/claude_log.txt
```

### Criterios de éxito
- [ ] Hooks configurados correctamente
- [ ] Se ejecutan en los momentos correctos
- [ ] Puedes usar hooks para automatización

---

## Ejercicio 8: Optimizar prompts para CLIs

**Nivel**: Avanzado
**Tiempo**: 40 minutos

### Objetivo
Aprender a escribir prompts efectivos para CLIs de IA.

### Instrucciones

1. Compara prompts vagos vs específicos
2. Mide la calidad de las respuestas
3. Desarrolla un "template" de prompts efectivos

### Comparativas

```bash
# Prompt vago
> Mejora este código

# Prompt específico
> Refactoriza la función calculateTotal en src/utils/math.ts para:
> 1. Usar reduce en lugar de for loop
> 2. Añadir manejo de arrays vacíos
> 3. Añadir tipos TypeScript
> 4. Mantener compatibilidad hacia atrás
```

### Template de prompt efectivo

```markdown
## Tarea: [Acción específica]

### Contexto
- Archivo(s): [lista de archivos]
- Tecnología: [stack]
- Restricciones: [limitaciones]

### Requisitos
1. [Requisito específico 1]
2. [Requisito específico 2]
3. [Requisito específico 3]

### Formato de salida
- [Cómo quieres la respuesta]

### Ejemplos (si aplica)
- Input: X → Output: Y
```

### Criterios de éxito
- [ ] Notas diferencia entre prompts vagos y específicos
- [ ] Tienes un template reutilizable
- [ ] Las respuestas son más precisas

---

## Ejercicio 9: Debugging de MCPs

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Aprender a diagnosticar y resolver problemas con MCPs.

### Instrucciones

1. Introduce un error intencional en la config
2. Diagnostica el problema
3. Corrígelo

### Errores comunes a practicar

```json
// Error 1: Path incorrecto
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta/que/no/existe"]
    }
  }
}

// Error 2: Package incorrecto
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git-typo"]
    }
  }
}

// Error 3: JSON malformado
{
  "mcpServers": {
    "filesystem": {
      "command": "npx"
      "args": ["-y", "@modelcontextprotocol/server-filesystem"]  // falta coma
    }
  }
}
```

### Comandos de diagnóstico

```bash
# Verificar sintaxis JSON
cat config.json | python -m json.tool

# Probar package manualmente
npx -y @modelcontextprotocol/server-filesystem --help

# Ver logs de Claude
# macOS: ~/Library/Logs/Claude/
# Windows: %APPDATA%\Claude\logs\
# Linux: ~/.config/Claude/logs/
```

### Criterios de éxito
- [ ] Puedes identificar errores comunes
- [ ] Conoces las herramientas de diagnóstico
- [ ] Puedes resolver problemas de configuración

---

## Ejercicio 10: Proyecto integrador - Sistema completo con MCPs

**Nivel**: Avanzado
**Tiempo**: 60 minutos

### Objetivo
Configurar un entorno de desarrollo completo con múltiples MCPs.

### Escenario

Configura TaskFlow con:
- Filesystem MCP para archivos
- Git MCP para versionado
- Memory MCP para contexto persistente
- Fetch MCP para obtener recursos web

### Configuración completa

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/taskflow"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/taskflow"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

### Workflow de prueba

```bash
claude

# 1. Verificar todos los MCPs
> /mcp

# 2. Guardar contexto del proyecto
> Recuerda que TaskFlow es un gestor de tareas con Express y PostgreSQL

# 3. Obtener información de una librería
> Obtén la documentación de Prisma ORM de su sitio web

# 4. Crear un archivo con la información
> Crea un archivo docs/prisma-notes.md con un resumen

# 5. Commitear los cambios
> Añade y commitea el nuevo archivo
```

### Criterios de éxito
- [ ] Todos los MCPs funcionan
- [ ] Puedes crear workflows que usen múltiples MCPs
- [ ] El entorno está listo para desarrollo

---

## Recursos adicionales

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Code Hooks](https://docs.anthropic.com/claude-code/hooks)
