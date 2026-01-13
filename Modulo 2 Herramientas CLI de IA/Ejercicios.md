# Ejercicios: Módulo 2 - Herramientas CLI de IA

## Información

| | |
|---|---|
| **Dificultad progresiva** | Básico → Intermedio → Avanzado |
| **Tiempo total estimado** | 3-4 horas |
| **Requisitos** | Al menos una CLI instalada (Claude Code, Gemini, OpenCode) |

---

## Ejercicio 1: Instalación y primera ejecución

**Nivel**: Básico
**Tiempo**: 20 minutos

### Objetivo
Instalar y verificar el funcionamiento de una CLI de IA.

### Instrucciones

1. Elige una CLI: Claude Code, Gemini CLI u OpenCode
2. Instálala siguiendo la documentación
3. Verifica la instalación
4. Ejecuta tu primer prompt

### Pasos

```bash
# Opción 1: Claude Code
npm install -g @anthropic-ai/claude-code
claude --version
claude "Hola, ¿qué puedes hacer?"

# Opción 2: Gemini CLI
npm install -g @google/gemini-cli
gemini --version
gemini "Hola, ¿qué puedes hacer?"

# Opción 3: OpenCode
npm install -g opencode-ai
opencode --version
```

### Criterios de éxito
- [ ] La CLI se instala sin errores
- [ ] Puedes ejecutar `--version`
- [ ] Recibes respuesta a tu primer prompt

---

## Ejercicio 2: Análisis de proyecto

**Nivel**: Básico
**Tiempo**: 25 minutos

### Objetivo
Usar la CLI para analizar la estructura de un proyecto existente.

### Instrucciones

1. Clona un proyecto de ejemplo o usa uno propio
2. Navega al directorio del proyecto
3. Pide a la CLI que analice la estructura
4. Pide explicación de archivos específicos

### Comandos sugeridos

```bash
# Clonar proyecto de ejemplo
git clone https://github.com/expressjs/express.git
cd express

# Iniciar CLI
claude  # o gemini / opencode

# Prompts a probar:
> ¿Cuál es la estructura de este proyecto?
> Explica qué hace el archivo lib/router/index.js
> ¿Qué patrones de diseño usa este proyecto?
> Lista las dependencias principales y para qué sirven
```

### Preguntas a responder
1. ¿Cuántos archivos analizó la CLI?
2. ¿Identificó correctamente el tipo de proyecto?
3. ¿Las explicaciones fueron precisas?

### Criterios de éxito
- [ ] La CLI navega el proyecto correctamente
- [ ] Entiendes mejor la estructura después del análisis
- [ ] La CLI puede explicar archivos específicos

---

## Ejercicio 3: Crear archivo CLAUDE.md

**Nivel**: Básico
**Tiempo**: 30 minutos

### Objetivo
Crear un archivo de contexto que mejore las respuestas de la CLI.

### Instrucciones

1. Crea un proyecto de ejemplo o usa TaskFlow
2. Crea el archivo CLAUDE.md en la raíz
3. Incluye información relevante
4. Verifica que la CLI lo usa

### Plantilla de CLAUDE.md

```markdown
# Proyecto: [Nombre]

## Descripción
[Descripción breve del proyecto]

## Stack Tecnológico
- **Backend**: [tecnologías]
- **Frontend**: [tecnologías]
- **Base de datos**: [tecnologías]

## Estructura del Proyecto
[Árbol de directorios principal]

## Comandos Principales
- `npm run dev` - [descripción]
- `npm test` - [descripción]
- `npm run build` - [descripción]

## Convenciones de Código
- [Convención 1]
- [Convención 2]

## Reglas Específicas
- [Regla 1]
- [Regla 2]
```

### Test

```bash
claude
> ¿Qué stack usa este proyecto?
# Debería usar la información de CLAUDE.md

> ¿Cómo ejecuto los tests?
# Debería responder con el comando de CLAUDE.md
```

### Criterios de éxito
- [ ] CLAUDE.md creado con información útil
- [ ] La CLI usa la información del archivo
- [ ] Las respuestas son más precisas

---

## Ejercicio 4: Comandos personalizados

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Crear comandos reutilizables para tareas comunes.

### Instrucciones

1. Crea la carpeta `.claude/commands/`
2. Crea al menos 2 comandos personalizados
3. Prueba los comandos

### Comando 1: Review de seguridad

```markdown
# .claude/commands/security.md

# Análisis de Seguridad

Analiza el código buscando vulnerabilidades de seguridad:

## Checklist
- [ ] Inyección SQL
- [ ] XSS (Cross-Site Scripting)
- [ ] Secrets hardcodeados
- [ ] Dependencias vulnerables
- [ ] Autenticación débil

## Para cada problema encontrado:
1. Archivo y línea
2. Tipo de vulnerabilidad
3. Severidad (CRÍTICA/ALTA/MEDIA/BAJA)
4. Código sugerido para corregir
```

### Comando 2: Generar tests

```markdown
# .claude/commands/tests.md

# Generar Tests

Genera tests unitarios para el archivo o función especificada: $ARGUMENTS

## Requisitos
- Usar el framework de testing del proyecto
- Cubrir casos principales y edge cases
- Incluir tests de error
- Seguir el patrón AAA (Arrange, Act, Assert)

## Estructura esperada
1. Describe el qué se está testeando
2. Tests para happy path
3. Tests para errores
4. Tests para edge cases
```

### Uso

```bash
claude
> /project:security
> /project:tests src/auth/login.ts
```

### Criterios de éxito
- [ ] Los comandos se ejecutan correctamente
- [ ] Generan output útil y estructurado
- [ ] Son reutilizables

---

## Ejercicio 5: Refactoring asistido

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Usar la CLI para refactorizar código de forma segura.

### Instrucciones

1. Identifica código que necesite refactoring
2. Pide a la CLI que lo analice
3. Aplica las sugerencias paso a paso
4. Verifica que todo sigue funcionando

### Código de ejemplo para refactorizar

```javascript
// archivo: legacy_code.js
function procesar(d) {
    var r = [];
    for (var i = 0; i < d.length; i++) {
        if (d[i].active == true) {
            if (d[i].age > 18) {
                if (d[i].country == 'ES') {
                    r.push({
                        n: d[i].firstName + ' ' + d[i].lastName,
                        e: d[i].email,
                        a: d[i].age
                    });
                }
            }
        }
    }
    return r;
}
```

### Prompts sugeridos

```bash
claude
> Analiza este código y sugiere mejoras de legibilidad
> Refactoriza usando ES6+ (arrow functions, destructuring, etc)
> Añade validación de inputs
> Genera la documentación JSDoc
```

### Criterios de éxito
- [ ] El código refactorizado es más legible
- [ ] Mantiene la misma funcionalidad
- [ ] Sigue las mejores prácticas modernas

---

## Ejercicio 6: Debugging con CLI

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Usar la CLI para encontrar y corregir bugs.

### Instrucciones

1. Usa el código con bugs proporcionado
2. Pide a la CLI que identifique los problemas
3. Corrige los bugs siguiendo las sugerencias
4. Verifica la corrección

### Código con bugs

```python
# buggy_code.py
def calcular_descuento(precio, porcentaje):
    """Calcula el precio con descuento."""
    descuento = precio * porcentaje  # Bug: debería ser / 100
    return precio - descuento

def buscar_usuario(usuarios, id):
    """Busca un usuario por ID."""
    for usuario in usuarios:
        if usuario.id == id:  # Bug: 'id' es keyword reservada
            return usuarios  # Bug: debería retornar 'usuario'
    return None

def procesar_datos(datos):
    """Procesa una lista de datos."""
    resultados = []
    for i in range(len(datos)):
        if datos[i] > 0:
            resultados.append(datos[i] * 2)
        # Bug: no maneja el else, algunos datos se pierden
    return resultados

class Contador:
    count = 0  # Bug: debería ser self.count en __init__

    def incrementar(self):
        count += 1  # Bug: debería ser self.count
        return count
```

### Prompts sugeridos

```bash
claude
> Analiza buggy_code.py y encuentra todos los bugs
> Explica cada bug y cómo corregirlo
> Genera la versión corregida del código
```

### Criterios de éxito
- [ ] La CLI identifica todos los bugs
- [ ] Las explicaciones son correctas
- [ ] El código corregido funciona

---

## Ejercicio 7: Generar código nuevo

**Nivel**: Intermedio
**Tiempo**: 45 minutos

### Objetivo
Usar la CLI para generar código completo siguiendo especificaciones.

### Instrucciones

1. Describe una funcionalidad a implementar
2. Pide a la CLI que genere el código
3. Revisa y ajusta según necesidades
4. Pide tests para el código generado

### Especificación de ejemplo

```markdown
## Funcionalidad: API de Tareas

Crear un endpoint REST para gestión de tareas:

### Endpoints
- GET /tasks - Lista todas las tareas (con paginación)
- POST /tasks - Crea una tarea
- GET /tasks/:id - Obtiene una tarea
- PUT /tasks/:id - Actualiza una tarea
- DELETE /tasks/:id - Elimina una tarea

### Modelo de Tarea
- id: UUID
- title: string (requerido, max 200 chars)
- description: string (opcional)
- status: enum (pending, in_progress, completed)
- priority: enum (low, medium, high)
- createdAt: timestamp
- updatedAt: timestamp

### Requisitos
- Express.js
- TypeScript
- Validación de inputs
- Manejo de errores
```

### Prompts sugeridos

```bash
claude
> Implementa esta API de tareas siguiendo la especificación
> Usa Express con TypeScript
> Incluye validación y manejo de errores
> Genera también los tests
```

### Criterios de éxito
- [ ] Código generado compila sin errores
- [ ] Implementa todos los endpoints
- [ ] Incluye validación y errores

---

## Ejercicio 8: Comparativa de CLIs

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Comparar el rendimiento y calidad de diferentes CLIs.

### Instrucciones

1. Instala al menos 2 CLIs diferentes
2. Ejecuta las mismas tareas en cada una
3. Documenta las diferencias
4. Elige tu favorita para cada caso de uso

### Tareas a comparar

```bash
# Tarea 1: Análisis de código
"Analiza este archivo y sugiere mejoras de rendimiento"

# Tarea 2: Generación de código
"Crea una función que valide emails con regex"

# Tarea 3: Debugging
"Encuentra el bug en este código: [código con bug]"

# Tarea 4: Explicación
"Explica qué hace este algoritmo paso a paso"
```

### Tabla de comparación

| Aspecto | Claude Code | Gemini CLI | OpenCode |
|---------|-------------|------------|----------|
| Velocidad de respuesta | | | |
| Calidad del código | | | |
| Precisión del análisis | | | |
| Manejo de contexto | | | |
| Facilidad de uso | | | |

### Criterios de éxito
- [ ] Pruebas realizadas en al menos 2 CLIs
- [ ] Tabla de comparación completada
- [ ] Conclusiones documentadas

---

## Ejercicio 9: Automatización de tareas

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Crear scripts que automatizan flujos de trabajo con la CLI.

### Instrucciones

1. Identifica una tarea repetitiva
2. Crea un script que la automatice
3. Integra con Git hooks o CI/CD

### Script de ejemplo: Pre-commit review

```bash
#!/bin/bash
# pre-commit-review.sh

# Obtener archivos modificados
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|py)$')

if [ -z "$FILES" ]; then
    echo "No hay archivos para revisar"
    exit 0
fi

echo "Revisando archivos modificados..."

for FILE in $FILES; do
    echo "Analizando: $FILE"

    # Usar Claude CLI en modo no interactivo
    REVIEW=$(claude -p "Revisa este código y reporta problemas críticos. Solo responde si hay problemas. Sé breve." < "$FILE")

    if [ -n "$REVIEW" ]; then
        echo "⚠️ Problemas encontrados en $FILE:"
        echo "$REVIEW"
        echo ""
    fi
done

echo "✅ Revisión completada"
```

### Instalación como hook

```bash
# Copiar a .git/hooks/pre-commit
cp pre-commit-review.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Criterios de éxito
- [ ] El script funciona correctamente
- [ ] Se integra con el flujo de trabajo
- [ ] Ahorra tiempo en tareas repetitivas

---

## Ejercicio 10: Proyecto integrador - Asistente de desarrollo

**Nivel**: Avanzado
**Tiempo**: 60 minutos

### Objetivo
Crear un flujo de trabajo completo asistido por CLI.

### Escenario

Vas a implementar una nueva feature usando la CLI como asistente:

1. **Análisis**: Entender el código existente
2. **Planificación**: Diseñar la solución
3. **Implementación**: Escribir el código
4. **Testing**: Generar y ejecutar tests
5. **Documentación**: Documentar los cambios
6. **Review**: Revisar antes de commit

### Feature a implementar

```markdown
## Feature: Sistema de notificaciones

Añadir notificaciones push a TaskFlow:
- Notificar cuando una tarea está próxima a vencer
- Notificar cuando alguien te asigna una tarea
- Permitir configurar preferencias de notificación
```

### Flujo de trabajo

```bash
# 1. Análisis
claude
> Analiza el proyecto y dime dónde debería implementar las notificaciones
> ¿Qué componentes existentes puedo reutilizar?

# 2. Planificación
> Diseña la arquitectura para el sistema de notificaciones
> ¿Qué archivos necesito crear/modificar?

# 3. Implementación
> Implementa el servicio de notificaciones
> Crea el endpoint para configurar preferencias

# 4. Testing
> Genera tests para el servicio de notificaciones
> ¿Hay edge cases que debería cubrir?

# 5. Documentación
> Genera documentación para la nueva feature
> Actualiza el README con las instrucciones

# 6. Review
> Revisa todos los cambios antes del commit
> ¿Hay algo que mejorar?
```

### Criterios de éxito
- [ ] Feature implementada completamente
- [ ] Tests generados y pasando
- [ ] Documentación actualizada
- [ ] Código revisado y listo para commit

---

## Recursos adicionales

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [OpenCode Documentation](https://opencode.ai/docs)
