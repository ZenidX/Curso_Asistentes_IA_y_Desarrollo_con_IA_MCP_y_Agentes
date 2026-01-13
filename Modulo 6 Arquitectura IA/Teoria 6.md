# Modulo 6: Arquitectura de Desarrollo Asistido por IA

---

## Informacion del Modulo

| Aspecto | Detalle |
|---------|---------|
| **Duracion Total** | 6-8 horas |
| **Nivel** | Avanzado |
| **Prerrequisitos** | Modulos 1-5 completados, experiencia con Git y CI/CD |
| **Herramientas Necesarias** | Claude Code, GitHub CLI, acceso a cloud (AWS/GCP/Azure) |
| **Proyecto Final** | TaskFlow - Aplicacion de gestion de tareas con arquitectura IA completa |

---

## Objetivos de Aprendizaje

Al finalizar este modulo, seras capaz de:

- [ ] Disenar arquitecturas de desarrollo asistido por IA usando patrones apropiados
- [ ] Implementar sistemas multi-agente para proyectos complejos
- [ ] Configurar pipelines CI/CD con integracion de IA
- [ ] Crear workflows automatizados con multiples MCPs
- [ ] Establecer metricas y monitoreo para medir productividad
- [ ] Aplicar mejores practicas de seguridad en desarrollo con IA
- [ ] Completar el proyecto TaskFlow integrando todos los conceptos del curso

---

## Indice

1. [Patrones de Arquitectura](#1-patrones-de-arquitectura) - 90 min
2. [Caso de Estudio: TaskFlow](#2-caso-de-estudio-taskflow) - 120 min
3. [Workflow Completo con MCPs](#3-workflow-completo-con-mcps) - 60 min
4. [Automatizacion de Workflows](#4-automatizacion-de-workflows) - 60 min
5. [Mejores Practicas](#5-mejores-practicas) - 45 min
6. [Checklists de Implementacion](#6-checklists-de-implementacion) - 30 min
7. [Metricas y Monitoreo](#7-metricas-y-monitoreo) - 45 min
8. [Ejercicios Finales](#8-ejercicios-finales) - Variable
9. [Troubleshooting](#9-troubleshooting) - Referencia
10. [Conclusion del Curso](#10-conclusion-del-curso)

---

## 1. Patrones de Arquitectura

**Tiempo estimado: 90 minutos**

### Introduccion

Los patrones de arquitectura definen como estructurar la interaccion entre agentes de IA y tu flujo de desarrollo. Elegir el patron correcto es crucial para maximizar la productividad sin sacrificar control.

---

### Patron 1: Agente Unico con MCPs

**Tiempo estimado: 20 minutos**

El patron mas simple y recomendado para comenzar: un agente de IA conectado a multiples MCPs.

```
+-------------------------------------------------------------+
|                      Claude Code                             |
|  +----------+ +----------+ +----------+ +----------+        |
|  |  GitHub  | | Firebase | |   AWS    | | Postgres |  MCPs  |
|  |   MCP    | |   MCP    | |   MCP    | |   MCP    |        |
|  +----+-----+ +----+-----+ +----+-----+ +----+-----+        |
+-------+------------+------------+------------+--------------+
        |            |            |            |
        v            v            v            v
    [GitHub]    [Firebase]     [AWS]     [PostgreSQL]
```

**Cuando usar**:
- Proyectos pequenos/medianos
- Un solo desarrollador
- Tareas lineales y secuenciales
- Primeras implementaciones de IA en equipos

**Ejemplo de uso**:
```bash
claude "Crea un endpoint de usuarios:
1. Usa PostgreSQL MCP para crear la tabla
2. Implementa el codigo en src/api/users.ts
3. Crea un PR en GitHub
4. Despliega a AWS Lambda"
```

> **Checkpoint 1**: Antes de continuar, asegurate de entender que un agente unico puede orquestar multiples servicios a traves de MCPs.

---

### Patron 2: Multi-Agente Orquestado

**Tiempo estimado: 25 minutos**

Multiples agentes especializados coordinados por un orquestador central.

```
+----------------------------------------------------------------+
|                    AGENTE ORQUESTADOR                           |
|                    (Claude Code Principal)                      |
+-----------------------------+----------------------------------+
                              |
         +--------------------+--------------------+
         v                    v                    v
+-----------------+ +-----------------+ +-----------------+
|   Subagente     | |   Subagente     | |   Subagente     |
|   Frontend      | |   Backend       | |   Testing       |
|   (React/Vue)   | |   (API/DB)      | |   (Jest/Pytest) |
|   + GitHub MCP  | |   + DB MCPs     | |   + CI/CD MCP   |
+-----------------+ +-----------------+ +-----------------+
```

**Cuando usar**:
- Proyectos grandes con multiples componentes
- Equipos de mas de 3 desarrolladores
- Necesidad de desarrollo paralelo
- Features que involucran frontend + backend + infraestructura

**Implementacion practica**:
```bash
# Terminal 1: Agente Frontend
claude --profile frontend "Implementa el formulario de registro"

# Terminal 2: Agente Backend
claude --profile backend "Implementa la API de registro"

# Terminal 3: Agente Testing
claude --profile testing "Monitorea cambios y genera tests"

# Terminal 4: Orquestador
claude "Coordina la implementacion de la feature de registro:
- Frontend esta trabajando en el formulario
- Backend esta trabajando en la API
- Testing generara tests cuando ambos terminen
Integra cuando todo este listo."
```

> **Error Comun**: Iniciar multiples agentes sin definir claramente las responsabilidades de cada uno. Esto causa conflictos en archivos y duplicacion de trabajo.

---

### Patron 3: Pipeline CI/CD Asistido

**Tiempo estimado: 25 minutos**

Agentes especializados en cada fase del pipeline de desarrollo.

```
+-------------+    +-------------+    +-------------+    +-------------+
|    Code     +--->+    Test     +--->+   Review    +--->+   Deploy    |
|   Agent     |    |   Agent     |    |   Agent     |    |   Agent     |
+------+------+    +------+------+    +------+------+    +------+------+
       |                  |                  |                  |
       v                  v                  v                  v
   [Claude]           [Claude]          [Claude]           [Claude]
   Genera             Ejecuta           Revisa             Despliega
   codigo             tests             codigo             cambios
```

**Cuando usar**:
- CI/CD automatizado existente
- Necesidad de quality gates estrictos
- Deployment frecuente (varias veces al dia)
- Equipos que practican DevOps

**Ejemplo de configuracion**:
```yaml
# Cada agente tiene un rol especifico en el pipeline
stages:
  - code_generation  # Claude genera codigo
  - automated_tests  # Claude ejecuta y valida tests
  - ai_review       # Claude revisa cambios
  - deployment      # Claude asiste en deploy
```

---

### Patron 4: Especializacion por Dominio

**Tiempo estimado: 20 minutos**

Agentes expertos en areas especificas del desarrollo.

```
+---------------------------------------------------------------------+
|                         ROUTER                                       |
|              (Analiza la tarea y la asigna al experto)              |
+-----------------------------+---------------------------------------+
                              |
    +------------+------------+------------+------------+
    v            v            v            v            v
+--------+  +--------+  +--------+  +--------+  +--------+
|Security|  |Database|  |  API   |  |  UI    |  | DevOps |
| Expert |  | Expert |  | Expert |  | Expert |  | Expert |
+--------+  +--------+  +--------+  +--------+  +--------+
```

**Implementacion con profiles**:
```json
// ~/.claude/profiles/security-expert.json
{
  "name": "Security Expert",
  "systemPrompt": "Eres un experto en seguridad con 15 anos de experiencia.
Tu enfoque principal es identificar vulnerabilidades OWASP Top 10,
revisar autenticacion/autorizacion, y asegurar datos sensibles.",
  "model": "claude-opus-4-5-20251101"
}
```

```json
// ~/.claude/profiles/database-expert.json
{
  "name": "Database Expert",
  "systemPrompt": "Eres un DBA senior especializado en PostgreSQL y Redis.
Tu enfoque es optimizacion de queries, modelado de datos,
indices y rendimiento de base de datos.",
  "model": "claude-opus-4-5-20251101"
}
```

> **Checkpoint 2**: Eres capaz de identificar que patron usarias para: a) Un proyecto personal, b) Una startup con 10 desarrolladores, c) Una empresa con CI/CD maduro?

---

### Practica Guiada 1: Seleccion de Patron

**Objetivo**: Elegir el patron correcto para diferentes escenarios.

**Ejercicio**: Para cada escenario, indica que patron usarias y por que:

| Escenario | Patron Recomendado | Justificacion |
|-----------|-------------------|---------------|
| App movil con 1 dev | | |
| Plataforma e-commerce, equipo de 15 | | |
| Microservicios con deploy continuo | | |
| Refactoring de sistema legacy | | |

**Criterios de exito**:
- Identificas correctamente al menos 3 de 4 escenarios
- Tu justificacion menciona las caracteristicas clave del patron

<details>
<summary>Ver solucion</summary>

| Escenario | Patron Recomendado | Justificacion |
|-----------|-------------------|---------------|
| App movil con 1 dev | Agente Unico | Proyecto pequeno, un desarrollador, tareas lineales |
| Plataforma e-commerce, equipo de 15 | Multi-Agente Orquestado | Proyecto grande, equipos multiples, desarrollo paralelo |
| Microservicios con deploy continuo | Pipeline CI/CD Asistido | CI/CD automatizado, quality gates, deployment frecuente |
| Refactoring de sistema legacy | Especializacion por Dominio | Necesita expertos en diferentes areas (DB, seguridad, API) |

</details>

---

## 2. Caso de Estudio: TaskFlow

**Tiempo estimado: 120 minutos**

### Descripcion del Proyecto

**TaskFlow** es una aplicacion de gestion de tareas que desarrollaremos como proyecto integrador del curso. Implementaremos un **Sistema de Notificaciones Push** usando desarrollo asistido por IA.

### Arquitectura Final de TaskFlow

```
+------------------+     +------------------+     +------------------+
|   React Native   |     |   Node.js API    |     |   PostgreSQL     |
|   Mobile App     +---->+   + Express      +---->+   + Redis Cache  |
+--------+---------+     +--------+---------+     +------------------+
         |                        |
         |                        |
         v                        v
+------------------+     +------------------+
| Firebase Cloud   |     |   AWS Lambda     |
|   Messaging      |     |   (Workers)      |
+------------------+     +------------------+
```

### Stack Tecnologico

| Componente | Tecnologia | MCP Asociado |
|------------|------------|--------------|
| Backend | Node.js + Express | - |
| Base de datos | PostgreSQL | @modelcontextprotocol/server-postgres |
| Mobile | React Native | - |
| Push Notifications | Firebase Cloud Messaging | @anthropic-ai/firebase-mcp |
| Cloud | AWS | awslabs.aws-api-mcp-server |
| Control de versiones | GitHub | @modelcontextprotocol/server-github |

---

### Paso 1: Planificacion con IA

**Tiempo estimado: 15 minutos**

```bash
claude "Necesito implementar un sistema de notificaciones push para
nuestra app movil TaskFlow.

Stack actual:
- Backend: Node.js + Express
- Base de datos: PostgreSQL
- Mobile: React Native
- Cloud: AWS

Analiza el codebase actual y propon una arquitectura que incluya:
1. Esquema de base de datos
2. Endpoints de API necesarios
3. Integracion con Firebase Cloud Messaging
4. Componentes mobile

Genera un plan detallado antes de implementar."
```

**Resultado esperado**: Un plan estructurado con estimaciones de tiempo y dependencias claras.

> **Error Comun**: Pedir al agente que "implemente todo" sin dar contexto del stack existente. Siempre proporciona informacion sobre tu proyecto actual.

---

### Paso 2: Configurar MCPs Necesarios

**Tiempo estimado: 20 minutos**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_..." }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "postgresql://..." }
    },
    "firebase": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "/path/to/key.json",
        "FIREBASE_STORAGE_BUCKET": "proyecto.appspot.com"
      }
    },
    "aws": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": { "AWS_PROFILE": "mi-perfil" }
    }
  }
}
```

> **Error Comun**: Commitear credenciales en el archivo de configuracion. Usa variables de entorno o un archivo `.env` que este en `.gitignore`.

**Verificacion de MCPs**:
```bash
# Verificar que cada MCP este funcionando
claude "@postgres SELECT 1"  # Debe responder con exito
claude "@github whoami"      # Debe mostrar tu usuario
claude "@firebase list-projects"  # Debe listar proyectos
```

> **Checkpoint 3**: Todos tus MCPs responden correctamente? Si alguno falla, revisa la seccion de Troubleshooting.

---

### Paso 3: Desarrollo Iterativo

#### 3.1 Crear estructura de base de datos

**Tiempo estimado: 15 minutos**

```bash
claude "Usando PostgreSQL MCP, crea las tablas necesarias:

1. notification_preferences
   - user_id (FK a users)
   - push_enabled (boolean)
   - email_enabled (boolean)
   - categories (jsonb) - que tipos de notificaciones recibir

2. devices
   - id
   - user_id (FK)
   - device_token (string, unique)
   - platform (ios/android)
   - last_active (timestamp)

3. notifications
   - id
   - user_id (FK)
   - title
   - body
   - data (jsonb)
   - sent_at
   - read_at
   - delivery_status

Incluye indices apropiados para las consultas frecuentes."
```

**SQL generado esperado**:
```sql
-- Tabla de preferencias
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    push_enabled BOOLEAN DEFAULT true,
    email_enabled BOOLEAN DEFAULT false,
    categories JSONB DEFAULT '{"marketing": true, "updates": true, "alerts": true}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Tabla de dispositivos
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    device_token VARCHAR(255) UNIQUE NOT NULL,
    platform VARCHAR(20) CHECK (platform IN ('ios', 'android')),
    last_active TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de notificaciones
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    body TEXT,
    data JSONB,
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    delivery_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indices
CREATE INDEX idx_devices_user_id ON devices(user_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_sent_at ON notifications(sent_at DESC);
CREATE INDEX idx_notifications_unread ON notifications(user_id) WHERE read_at IS NULL;
```

---

#### 3.2 Implementar endpoints API

**Tiempo estimado: 25 minutos**

```bash
claude "Implementa los endpoints REST en src/api/notifications/:

POST /api/notifications
- Crear y enviar notificacion a usuario(s)
- Usar Firebase Cloud Messaging para push
- Guardar en base de datos

GET /api/notifications/:userId
- Listar notificaciones del usuario
- Paginacion con limit y offset
- Filtros: read/unread, por fecha

PUT /api/notifications/:id/read
- Marcar como leida

POST /api/devices/register
- Registrar dispositivo para push
- Actualizar token si ya existe

DELETE /api/devices/:deviceId
- Eliminar dispositivo (logout)

Incluye:
- Validacion con Joi/Zod
- Manejo de errores consistente
- Logging estructurado
- Tests unitarios para cada endpoint"
```

> **Error Comun**: No especificar el manejo de errores. Sin instrucciones claras, el agente puede generar codigo sin try/catch adecuados.

---

#### 3.3 Integrar Firebase Cloud Messaging

**Tiempo estimado: 20 minutos**

```bash
claude "Configura Firebase Cloud Messaging:

1. Usa el Firebase MCP para verificar la configuracion
2. Crea src/services/pushService.ts con:
   - sendToDevice(token, payload)
   - sendToMultiple(tokens[], payload)
   - sendToTopic(topic, payload)
3. Implementa retry con exponential backoff
4. Maneja tokens invalidos (eliminar de DB)
5. Incluye metricas de envio"
```

**Codigo esperado (estructura)**:
```typescript
// src/services/pushService.ts
import * as admin from 'firebase-admin';

interface PushPayload {
  title: string;
  body: string;
  data?: Record<string, string>;
}

export class PushService {
  private maxRetries = 3;

  async sendToDevice(token: string, payload: PushPayload): Promise<boolean> {
    // Implementacion con retry
  }

  async sendToMultiple(tokens: string[], payload: PushPayload): Promise<void> {
    // Batch sending con manejo de tokens invalidos
  }

  async sendToTopic(topic: string, payload: PushPayload): Promise<void> {
    // Envio a topico
  }

  private async handleInvalidToken(token: string): Promise<void> {
    // Eliminar token de la base de datos
  }
}
```

---

#### 3.4 Ejecutar tests

**Tiempo estimado: 15 minutos**

```bash
claude "Ejecuta toda la suite de tests:
1. Tests unitarios de los nuevos endpoints
2. Tests de integracion con la base de datos
3. Tests de integracion con Firebase (mock)

Muestra el coverage y corrige cualquier fallo.
El coverage minimo debe ser 80%."
```

**Salida esperada**:
```
PASS  tests/api/notifications.test.ts
  POST /api/notifications
    ✓ crea y envia notificacion exitosamente (45ms)
    ✓ falla con payload invalido (12ms)
    ✓ falla con usuario inexistente (8ms)
  GET /api/notifications/:userId
    ✓ retorna lista paginada (23ms)
    ✓ filtra por estado read/unread (18ms)
  ...

Coverage: 87.3%
Statements: 156/179
Branches: 34/42
Functions: 28/31
Lines: 148/169
```

> **Checkpoint 4**: Tus tests pasan con al menos 80% de coverage? Si no, pide al agente que genere tests adicionales para los casos faltantes.

---

#### 3.5 Code Review con IA

**Tiempo estimado: 15 minutos**

```bash
claude "Revisa todo el codigo generado para notificaciones.

Verifica:
1. Seguridad
   - Hay inyeccion SQL?
   - Los endpoints estan autenticados?
   - Se validan los permisos?

2. Performance
   - Queries eficientes?
   - Hay N+1 queries?
   - Se usa cache donde corresponde?

3. Mantenibilidad
   - Codigo limpio y legible?
   - Buena separacion de responsabilidades?
   - Documentacion adecuada?

4. Edge cases
   - Que pasa si Firebase falla?
   - Que pasa con tokens expirados?
   - Limites de rate?"
```

---

#### 3.6 Documentacion

**Tiempo estimado: 10 minutos**

```bash
claude "Genera documentacion:

1. Actualiza README.md con la nueva feature
2. Genera docs/api/notifications.md con:
   - Descripcion de endpoints
   - Ejemplos de requests/responses
   - Codigos de error
3. Anade comentarios JSDoc a funciones publicas
4. Crea guia de configuracion de Firebase"
```

---

#### 3.7 Pull Request

**Tiempo estimado: 5 minutos**

```bash
claude "Crea un Pull Request en GitHub:

1. Branch: feature/notifications-system
2. Titulo descriptivo
3. Descripcion con:
   - Resumen de cambios
   - Screenshots si aplica
   - Testing realizado
   - Checklist de review
4. Asigna reviewers apropiados
5. Anade labels relevantes"
```

---

### Practica Guiada 2: Implementar una Feature Adicional

**Objetivo**: Aplicar el flujo completo de desarrollo para agregar programacion de notificaciones.

**Requisitos**:
1. Los usuarios pueden programar notificaciones para una fecha/hora futura
2. Un worker procesa las notificaciones programadas
3. Se pueden cancelar notificaciones programadas

**Pasos**:
1. Modifica el schema de la tabla `notifications` para incluir `scheduled_at`
2. Crea endpoint `POST /api/notifications/schedule`
3. Implementa el worker que procesa notificaciones programadas
4. Anade tests

**Nivel de dificultad**: Intermedio

**Criterios de exito**:
- [ ] La notificacion se crea con estado "scheduled"
- [ ] El worker detecta y envia notificaciones cuando llega su hora
- [ ] Se puede cancelar una notificacion programada
- [ ] Tests cubren los casos principales

---

## 3. Workflow Completo con MCPs

**Tiempo estimado: 60 minutos**

### Escenario Real: Bug Fix Urgente en Produccion

Este workflow demuestra como usar multiples MCPs para resolver un bug critico de manera eficiente.

```bash
# 1. Identificar el bug (Sentry MCP)
claude "@sentry Muestrame los errores criticos de las ultimas 24 horas
en el servicio de pagos"

# Respuesta esperada:
# Error AUTH_TOKEN_INVALID en checkout.js:234
# Ocurrencias: 1,247
# Usuarios afectados: 892
# Stack trace: ...

# 2. Analizar codigo relacionado
claude "Analiza el stack trace del error AUTH_TOKEN_INVALID.
Lee el codigo en checkout.js y encuentra la causa raiz.
Revisa tambien los cambios recientes en Git que puedan estar relacionados."

# 3. Verificar en base de datos
claude "@postgres Revisa la tabla auth_tokens para ver si hay
tokens expirados o invalidos que coincidan con el timeframe del error"

# 4. Crear branch y fix
claude "Crea una branch 'hotfix/auth-token-validation'.
Implementa el fix basado en tu analisis.
Asegurate de:
- Anadir validacion de expiracion
- Manejar el caso de token invalido gracefully
- Loggear el error correctamente"

# 5. Tests
claude "Escribe tests para cubrir el bug:
- Test cuando token esta expirado
- Test cuando token es invalido
- Test cuando token es valido
Ejecuta los tests y verifica que pasen."

# 6. Code Review automatico
claude "Revisa el fix implementado.
Hay efectos secundarios?
El fix es completo o solo parcial?"

# 7. Crear PR
claude "@github Crea un PR desde hotfix/auth-token-validation a main.
Usa el template de hotfix.
Marca como urgente."

# 8. Notificar al equipo
claude "@slack Envia un mensaje a #engineering:
'Hotfix para AUTH_TOKEN_INVALID en review.
PR #xxx - necesita review urgente.
Error afectaba checkout de pagos.'"

# 9. Deploy (despues de approval)
claude "@aws Despliega el hotfix a produccion usando CodeDeploy.
Monitorea los logs por 15 minutos despues del deploy."
```

> **Error Comun**: Hacer deploy sin verificar que el PR fue aprobado. Siempre espera el approval antes de desplegar a produccion.

> **Checkpoint 5**: Puedes identificar los 5 MCPs diferentes usados en este workflow?

<details>
<summary>Ver respuesta</summary>

1. **Sentry MCP**: Para identificar el error
2. **PostgreSQL MCP**: Para verificar datos en la base
3. **GitHub MCP**: Para crear branch y PR
4. **Slack MCP**: Para notificar al equipo
5. **AWS MCP**: Para desplegar el fix

</details>

---

## 4. Automatizacion de Workflows

**Tiempo estimado: 60 minutos**

### GitHub Actions con Claude

**Tiempo estimado: 25 minutos**

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Claude Code
        run: |
          curl -fsSL https://claude.ai/install.sh | bash

      - name: Get Changed Files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Run AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Revisa estos archivos cambiados: ${{ steps.changed.outputs.files }}

          Enfocate en:
          1. Bugs potenciales
          2. Vulnerabilidades de seguridad
          3. Problemas de performance
          4. Mejores practicas de codigo

          Genera el review en formato JSON con estructura:
          {
            'issues': [
              {'file': '...', 'line': N, 'severity': '...', 'message': '...', 'suggestion': '...'}
            ],
            'summary': '...',
            'approve': true/false
          }" > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));

            let body = '## AI Code Review\n\n';
            body += `### Summary\n${review.summary}\n\n`;

            if (review.issues.length > 0) {
              body += '### Issues Found\n';
              for (const issue of review.issues) {
                body += `- **${issue.severity}** in \`${issue.file}:${issue.line}\`: ${issue.message}\n`;
                body += `  - Suggestion: ${issue.suggestion}\n`;
              }
            } else {
              body += 'No issues found!\n';
            }

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });
```

> **Error Comun**: No almacenar `ANTHROPIC_API_KEY` como secret de GitHub. Nunca pongas API keys directamente en el workflow.

---

### Script de Migracion Automatica

**Tiempo estimado: 15 minutos**

```bash
#!/bin/bash
# scripts/ai-migrate.sh

echo "Iniciando migracion asistida por IA..."

# 1. Analizar cambios en modelos
claude -p "Analiza los cambios en src/models/ desde el ultimo release.
Genera las migraciones SQL necesarias para PostgreSQL.
Incluye:
- Alteraciones de tablas
- Nuevos indices
- Datos de seed si necesario" > migrations/$(date +%Y%m%d_%H%M%S).sql

# 2. Validar migracion
claude -p "Valida la migracion generada.
Es reversible?
Hay riesgo de perdida de datos?
Se necesita downtime?"

# 3. Ejecutar en staging
echo "Ejecutar en staging? (y/n)"
read confirm
if [ "$confirm" = "y" ]; then
    claude "@postgres Ejecuta la ultima migracion en la base de datos de staging"
fi
```

---

### Pre-commit Hook con IA

**Tiempo estimado: 20 minutos**

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Ejecutando AI pre-commit check..."

# Obtener archivos staged
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Quick AI review
REVIEW=$(claude -p "Review rapido de estos archivos (maximo 3 issues criticos):
$STAGED_FILES

Solo reporta issues de:
- Seguridad (inyecciones, secrets expuestos)
- Bugs obvios
- Errores de sintaxis

Responde 'OK' si no hay issues criticos." 2>/dev/null)

if [[ "$REVIEW" != *"OK"* ]]; then
    echo "AI encontro issues:"
    echo "$REVIEW"
    echo ""
    echo "Continuar de todos modos? (y/n)"
    read -r confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi

echo "Pre-commit check passed"
exit 0
```

**Instalacion**:
```bash
# Hacer el hook ejecutable
chmod +x .git/hooks/pre-commit
```

> **Checkpoint 6**: Has configurado al menos un hook o workflow automatizado en tu proyecto?

---

## 5. Mejores Practicas

**Tiempo estimado: 45 minutos**

### 1. Proporciona Contexto Rico

**Tiempo estimado: 15 minutos**

Un archivo CLAUDE.md bien estructurado es fundamental para obtener buenos resultados.

```markdown
# CLAUDE.md / GEMINI.md

## Proyecto: E-commerce Platform v2

### Stack Tecnologico
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Backend**: Node.js + Fastify + TypeORM
- **Base de datos**: PostgreSQL 15 + Redis 7
- **Infraestructura**: AWS (ECS, RDS, ElastiCache, S3)
- **CI/CD**: GitHub Actions + ArgoCD

### Arquitectura
```
+-------------+     +-------------+     +-------------+
|   Next.js   +---->+   Fastify   +---->+  PostgreSQL |
|  Frontend   |     |   Backend   |     |    + Redis  |
+-------------+     +-------------+     +-------------+
```

### Convenciones de Codigo
- **Naming**: camelCase para variables, PascalCase para clases/componentes
- **Commits**: Conventional Commits (feat:, fix:, docs:, etc.)
- **Branches**: feature/, bugfix/, hotfix/, release/
- **PRs**: Requieren 2 approvals + CI verde

### Estructura del Proyecto
```
/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Fastify backend
├── packages/
│   ├── ui/           # Componentes compartidos
│   ├── database/     # Schema y migraciones
│   └── types/        # TypeScript types compartidos
└── infra/            # IaC con Terraform
```

### Comandos Frecuentes
- `pnpm dev` - Desarrollo (todos los servicios)
- `pnpm test` - Tests unitarios
- `pnpm test:e2e` - Tests E2E con Playwright
- `pnpm db:migrate` - Ejecutar migraciones
- `pnpm lint` - ESLint + Prettier

### Variables de Entorno
Ver `.env.example` - nunca commitear `.env`

### Notas Importantes
- El rate limiter esta en Redis, no modificar sin revisar
- Los pagos usan Stripe, webhooks en /api/webhooks/stripe
- El search usa Algolia, sincronizacion cada 5 min
```

---

### 2. Divide Tareas Complejas

**Tiempo estimado: 10 minutos**

```bash
# MAL - Demasiado amplio
claude "Construye un sistema de autenticacion completo"

# BIEN - Pasos claros y manejables
claude "Paso 1: Disena el schema de DB para auth:
- Tabla users (id, email, password_hash, created_at, updated_at)
- Tabla sessions (id, user_id, token, expires_at, ip, user_agent)
- Tabla password_resets (id, user_id, token, expires_at, used_at)
Usa PostgreSQL MCP para crear las tablas."

claude "Paso 2: Implementa endpoint POST /auth/register:
- Validacion de email y password
- Hash de password con bcrypt (cost 12)
- Prevencion de email duplicado
- Respuesta con usuario (sin password)"

claude "Paso 3: Implementa endpoint POST /auth/login:
- Verificar credenciales
- Crear sesion en DB
- Generar JWT con expiracion 1h
- Refresh token con expiracion 7d"

# ... continua paso a paso
```

> **Error Comun**: Asumir que el agente recuerda el contexto de sesiones anteriores. Siempre proporciona el contexto necesario en cada prompt.

---

### 3. Usa TDD con IA

**Tiempo estimado: 10 minutos**

```bash
# Primero los tests
claude "Escribe tests para un servicio de carrito de compras.
El servicio debe:
- Anadir items (producto, cantidad)
- Remover items
- Actualizar cantidad
- Calcular subtotal por item
- Calcular total del carrito
- Aplicar descuentos (porcentaje o fijo)
- Manejar stock insuficiente

Usa Jest + TypeScript.
No implementes el servicio aun, solo los tests."

# Luego la implementacion
claude "Implementa CartService para que pasen todos los tests.
Los tests estan en src/services/__tests__/cart.test.ts"

# Verificar
claude "Ejecuta los tests y muestra el coverage.
Anade tests para cualquier caso edge que falte."
```

---

### 4. Verificacion Cruzada

**Tiempo estimado: 5 minutos**

Usa diferentes herramientas para verificar el codigo generado:

```bash
# Genera con una herramienta
claude "Implementa la funcion de validacion de tarjetas de credito"

# Revisa con otras
codex "Review this implementation for edge cases and security:
$(cat src/utils/cardValidation.ts)"

gemini "Check for performance issues and potential improvements:
$(cat src/utils/cardValidation.ts)"
```

---

### 5. Iteracion y Refinamiento

**Tiempo estimado: 5 minutos**

```bash
# Iteracion 1 - Version basica
claude "Genera un endpoint basico para busqueda de productos"

# Iteracion 2 - Agregar funcionalidad
claude "Ahora anade:
- Filtros por categoria, precio, rating
- Paginacion
- Ordenamiento"

# Iteracion 3 - Optimizacion
claude "Optimiza para performance:
- Anade indices necesarios
- Implementa cache con Redis
- Limita campos en respuesta"

# Iteracion 4 - Features avanzadas
claude "Anade busqueda full-text con PostgreSQL tsvector
o integracion con Elasticsearch si el volumen lo requiere"
```

---

## 6. Checklists de Implementacion

**Tiempo estimado: 30 minutos**

### Para Nuevos Proyectos

```markdown
## Setup Inicial

### Contexto para IA
- [ ] Crear CLAUDE.md/GEMINI.md con descripcion del proyecto
- [ ] Documentar stack tecnologico
- [ ] Definir convenciones de codigo
- [ ] Listar comandos frecuentes

### MCPs
- [ ] Identificar MCPs necesarios (DB, Cloud, Git, etc.)
- [ ] Configurar cada MCP con credenciales
- [ ] Probar conexion de cada MCP
- [ ] Documentar configuracion en README

### Automatizacion
- [ ] Configurar hooks de pre-commit
- [ ] Crear comandos personalizados en .claude/commands/
- [ ] Integrar AI review en CI/CD
- [ ] Configurar notificaciones (Slack, etc.)

### Seguridad
- [ ] Variables de entorno para secrets (nunca en codigo)
- [ ] Configurar permisos minimos en MCPs
- [ ] Activar modo confirmacion para comandos peligrosos
- [ ] Revisar codigo generado antes de deploy
```

---

### Para Proyectos Existentes

```markdown
## Adopcion de IA en Proyecto Existente

### Analisis Inicial
- [ ] Documentar arquitectura actual para contexto de IA
- [ ] Identificar deuda tecnica que IA puede ayudar a resolver
- [ ] Mapear workflows actuales
- [ ] Identificar tareas repetitivas automatizables

### Integracion Gradual
- [ ] Comenzar con code review asistido
- [ ] Anadir generacion de tests
- [ ] Automatizar documentacion
- [ ] Integrar en refactoring

### MCPs Especificos
- [ ] Configurar MCP para base de datos del proyecto
- [ ] Configurar MCP para cloud del proyecto
- [ ] Configurar integraciones especificas (Jira, Slack, etc.)

### Metricas
- [ ] Establecer baseline de productividad
- [ ] Definir metricas a trackear
- [ ] Configurar dashboard de seguimiento
```

---

### Para Cada Feature

```markdown
## Checklist de Feature

### Antes de Empezar
- [ ] Actualizar contexto en CLAUDE.md si cambio algo
- [ ] Verificar que MCPs necesarios esten funcionando
- [ ] Revisar dependencias y versiones

### Durante Desarrollo
- [ ] Dividir feature en pasos manejables
- [ ] Escribir tests antes o junto con codigo
- [ ] Ejecutar tests frecuentemente
- [ ] Hacer commits pequenos y frecuentes

### Antes de PR
- [ ] Ejecutar suite completa de tests
- [ ] Verificar cobertura minima (80%)
- [ ] Ejecutar linter y formatter
- [ ] Hacer self-review del codigo
- [ ] Actualizar documentacion

### Despues de Merge
- [ ] Verificar deploy exitoso
- [ ] Monitorear logs y metricas
- [ ] Documentar learnings
```

---

## 7. Metricas y Monitoreo

**Tiempo estimado: 45 minutos**

### Dashboard de Productividad

**Tiempo estimado: 25 minutos**

```python
# scripts/ai_metrics.py
"""
Sistema de metricas para desarrollo asistido por IA.
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AIInteraction:
    """Representa una interaccion con herramienta de IA."""
    timestamp: str
    tool: str  # claude, codex, gemini
    task_type: str  # code_gen, review, debug, docs, test
    duration_seconds: float
    tokens_used: int
    success: bool
    error_message: str = ""

class MetricsCollector:
    """Recolector de metricas de uso de IA."""

    def __init__(self, output_file: str = "ai_metrics.jsonl"):
        self.output_file = Path(output_file)

    def log_interaction(self, interaction: AIInteraction):
        """Registra una interaccion."""
        with open(self.output_file, "a") as f:
            f.write(json.dumps(asdict(interaction)) + "\n")

    def get_summary(self, days: int = 7) -> dict:
        """Genera resumen de metricas."""
        interactions = []
        cutoff = datetime.now().timestamp() - (days * 86400)

        if not self.output_file.exists():
            return {"message": "No hay datos suficientes"}

        with open(self.output_file) as f:
            for line in f:
                data = json.loads(line)
                if datetime.fromisoformat(data["timestamp"]).timestamp() > cutoff:
                    interactions.append(data)

        if not interactions:
            return {"message": "No hay datos suficientes"}

        return {
            "periodo_dias": days,
            "total_interacciones": len(interactions),
            "por_herramienta": self._group_by(interactions, "tool"),
            "por_tipo_tarea": self._group_by(interactions, "task_type"),
            "tasa_exito": sum(1 for i in interactions if i["success"]) / len(interactions),
            "tiempo_promedio_segundos": sum(i["duration_seconds"] for i in interactions) / len(interactions),
            "tokens_totales": sum(i["tokens_used"] for i in interactions),
        }

    def _group_by(self, items: list, key: str) -> dict:
        result = {}
        for item in items:
            k = item[key]
            result[k] = result.get(k, 0) + 1
        return result


# Ejemplo de uso
if __name__ == "__main__":
    collector = MetricsCollector()

    # Simular algunas interacciones
    collector.log_interaction(AIInteraction(
        timestamp=datetime.now().isoformat(),
        tool="claude",
        task_type="code_gen",
        duration_seconds=45.2,
        tokens_used=1500,
        success=True
    ))

    print(json.dumps(collector.get_summary(), indent=2))
```

---

### Integracion con Dashboard Web

**Tiempo estimado: 10 minutos**

```python
# scripts/metrics_dashboard.py
from flask import Flask, jsonify, render_template, request
from ai_metrics import MetricsCollector

app = Flask(__name__)
collector = MetricsCollector()

@app.route("/api/metrics")
def get_metrics():
    days = request.args.get("days", 7, type=int)
    return jsonify(collector.get_summary(days))

@app.route("/api/metrics/export")
def export_metrics():
    """Exporta metricas para analisis externo."""
    # Formato compatible con Grafana, Datadog, etc.
    pass

@app.route("/")
def dashboard():
    return render_template("dashboard.html", metrics=collector.get_summary())

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

---

### KPIs Sugeridos

**Tiempo estimado: 10 minutos**

| Metrica | Descripcion | Objetivo | Como Medir |
|---------|-------------|----------|------------|
| **Tiempo de desarrollo** | Tiempo promedio por feature | Reducir 30% | Comparar antes/despues de adoptar IA |
| **Bugs en produccion** | Bugs encontrados post-deploy | Reducir 50% | Trackear en sistema de issues |
| **Cobertura de tests** | % de codigo cubierto | Minimo 80% | Herramientas de coverage |
| **Tiempo de review** | Tiempo hasta approval de PR | Reducir 40% | Metricas de GitHub |
| **Satisfaccion del dev** | Encuesta mensual (1-10) | Minimo 8 | Encuestas anonimas |

---

## 8. Ejercicios Finales

### Ejercicio 1: Proyecto Completo (Principiante a Intermedio)

**Objetivo**: Implementar una API de gestion de tareas con desarrollo asistido por IA.

**Nivel de dificultad**: Intermedio

**Tiempo estimado**: 4-6 horas

**Requisitos**:
1. CRUD de tareas (crear, leer, actualizar, eliminar)
2. Autenticacion con JWT
3. Base de datos PostgreSQL
4. Tests con cobertura >80%
5. Documentacion OpenAPI
6. Deploy a cloud (AWS/GCP/Azure)

**Pasos**:
1. Configura CLAUDE.md con el contexto
2. Configura MCPs necesarios (PostgreSQL, GitHub, cloud)
3. Usa el patron de desarrollo iterativo
4. Implementa cada endpoint con tests
5. Haz code review con IA
6. Despliega con asistencia de IA

**Criterios de exito**:
- [ ] Todos los endpoints funcionan correctamente
- [ ] Autenticacion JWT implementada
- [ ] Tests pasan con >80% coverage
- [ ] Documentacion OpenAPI generada
- [ ] Aplicacion desplegada y accesible

---

### Ejercicio 2: Migracion de Proyecto Existente (Intermedio)

**Objetivo**: Migrar un proyecto legacy a arquitectura moderna con ayuda de IA.

**Nivel de dificultad**: Intermedio-Avanzado

**Tiempo estimado**: 6-8 horas

**Tareas**:
1. Analiza el codigo legacy con IA
2. Identifica patrones y anti-patrones
3. Disena nueva arquitectura
4. Migra modulo por modulo
5. Manten compatibilidad durante la migracion
6. Documenta el proceso

**Criterios de exito**:
- [ ] Arquitectura nueva documentada
- [ ] Al menos 3 modulos migrados
- [ ] Tests de regresion pasan
- [ ] Documentacion de migracion completa

---

### Ejercicio 3: Automatizacion de Workflow (Avanzado)

**Objetivo**: Crear un pipeline CI/CD completamente asistido por IA.

**Nivel de dificultad**: Avanzado

**Tiempo estimado**: 4-5 horas

**Componentes**:
1. Pre-commit hooks con AI review
2. GitHub Actions para testing
3. AI code review en PRs
4. Deploy automatizado
5. Monitoreo post-deploy
6. Alertas inteligentes

**Criterios de exito**:
- [ ] Pre-commit hook instalado y funcionando
- [ ] GitHub Action ejecuta AI review en cada PR
- [ ] Deploy automatico al aprobar PR
- [ ] Alertas configuradas para errores

---

### Ejercicio 4: Crear tu Propio MCP (Avanzado)

**Objetivo**: Desarrollar un MCP para una API o servicio que uses frecuentemente.

**Nivel de dificultad**: Avanzado

**Tiempo estimado**: 6-10 horas

**Ideas**:
- MCP para tu sistema de tickets (Jira, Linear, etc.)
- MCP para tu sistema de monitoreo
- MCP para tu base de datos especifica
- MCP para tu cloud provider

**Criterios de exito**:
- [ ] MCP implementado en Python o TypeScript
- [ ] Al menos 5 herramientas expuestas
- [ ] Documentacion de uso
- [ ] Tests unitarios

---

### Ejercicio 5: Documentar y Compartir (Todos los niveles)

**Objetivo**: Crear documentacion completa del setup de IA para tu equipo.

**Nivel de dificultad**: Variable

**Tiempo estimado**: 2-4 horas

**Incluir**:
1. Guia de instalacion paso a paso
2. Mejores practicas aprendidas
3. Errores comunes y soluciones
4. Templates de CLAUDE.md
5. Configuraciones de MCPs recomendadas
6. Workflows automatizados

**Criterios de exito**:
- [ ] Un companero puede seguir la guia sin ayuda
- [ ] Incluye al menos 3 ejemplos practicos
- [ ] Documenta errores comunes encontrados

---

## 9. Troubleshooting

### Problemas Comunes con MCPs

| Problema | Causa Probable | Solucion |
|----------|---------------|----------|
| MCP no responde | Credenciales incorrectas | Verificar API keys en configuracion |
| Timeout en consultas | Conexion lenta o servidor caido | Aumentar timeout, verificar conectividad |
| Error de permisos | Token sin permisos suficientes | Revisar scopes del token |
| MCP no encontrado | Paquete no instalado | Ejecutar `npx -y @nombre/del-mcp` |

### Problemas con GitHub Actions

| Problema | Causa Probable | Solucion |
|----------|---------------|----------|
| Secret no disponible | Nombre incorrecto | Verificar nombre exacto en Settings > Secrets |
| Workflow no ejecuta | Branch protegido | Revisar reglas de branch protection |
| AI review falla | API key invalida | Regenerar ANTHROPIC_API_KEY |

### Problemas de Performance

| Problema | Causa Probable | Solucion |
|----------|---------------|----------|
| Respuestas lentas | Contexto muy grande | Reducir tamano del CLAUDE.md |
| Tokens excedidos | Prompt muy largo | Dividir en prompts mas pequenos |
| Resultados inconsistentes | Falta de contexto | Agregar mas detalles al prompt |

### Cuando Contactar Soporte

- El MCP funciona localmente pero falla en CI/CD
- Errores de autenticacion persistentes despues de regenerar tokens
- Comportamiento inesperado del agente que no se resuelve con mejor contexto

---

## 10. Conclusion del Curso

### Resumen de lo Aprendido

Has completado el curso de **IA para Desarrollo de Software**. Ahora tienes:

| Modulo | Competencia Adquirida |
|--------|----------------------|
| **Modulo 1** | Conocimiento de APIs: Claude, OpenAI, Gemini, DeepSeek, Grok |
| **Modulo 2** | Dominio de CLIs: Claude Code, Gemini CLI, Codex CLI |
| **Modulo 3** | Fundamentos solidos: Contexto, MCP, subagentes, hooks |
| **Modulo 4** | MCPs del mercado: AWS, Cloudflare, Firebase, GitHub, bases de datos |
| **Modulo 5** | Capacidad de crear MCPs propios: Python y TypeScript |
| **Modulo 6** | Arquitecturas de desarrollo: Patrones, workflows, automatizacion |

### Competencias Clave Desarrolladas

- [ ] Disenar arquitecturas de desarrollo asistido por IA
- [ ] Seleccionar el patron apropiado segun el proyecto
- [ ] Configurar y usar multiples MCPs en workflows complejos
- [ ] Automatizar procesos de desarrollo con GitHub Actions
- [ ] Medir y mejorar la productividad con metricas
- [ ] Aplicar mejores practicas de seguridad

### Proximos Pasos Sugeridos

1. **Implementa los ejercicios en proyectos reales**
   - Comienza con el Ejercicio 1 si eres principiante
   - Avanza a ejercicios mas complejos progresivamente

2. **Contribuye a MCPs open source**
   - Revisa [MCP Servers](https://github.com/modelcontextprotocol/servers)
   - Propone mejoras o crea nuevos MCPs

3. **Comparte tu conocimiento con el equipo**
   - Organiza sesiones de capacitacion
   - Documenta casos de uso especificos de tu organizacion

4. **Mantente actualizado**
   - Sigue los changelogs de Claude Code y otros CLIs
   - Participa en comunidades de desarrolladores

### Recursos Adicionales

#### Documentacion Oficial
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Gemini CLI Docs](https://ai.google.dev/gemini-cli)
- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [MCP Specification](https://modelcontextprotocol.io)

#### Repositorios de Referencia
- [MCP Servers (Oficial)](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [FastMCP](https://github.com/jlowin/fastmcp)

#### Comunidades
- [Claude Developers Discord](https://discord.gg/anthropic)
- [Gemini CLI GitHub Discussions](https://github.com/google-gemini/gemini-cli/discussions)
- [MCP Community](https://github.com/modelcontextprotocol/discussions)

---

### Certificacion del Curso

Para obtener tu certificado de completitud:

- [ ] Completar al menos 3 de los 5 ejercicios finales
- [ ] Demostrar implementacion de un proyecto con IA
- [ ] Contribuir con al menos una mejora documentada

---

**Felicitaciones por completar el curso!**

El desarrollo asistido por IA es una habilidad que seguira evolucionando. Lo mas importante es mantener una mentalidad de aprendizaje continuo y experimentacion constante.

---

*Curso actualizado: Enero 2026*
*Version: 2.0*
