# Módulo 6: Arquitectura de Desarrollo Asistido por IA

## Índice
1. [Patrones de Arquitectura](#1-patrones-de-arquitectura)
2. [Caso Práctico: Feature Completa](#2-caso-práctico-feature-completa)
3. [Workflow Completo con MCPs](#3-workflow-completo-con-mcps)
4. [Automatización de Workflows](#4-automatización-de-workflows)
5. [Mejores Prácticas](#5-mejores-prácticas)
6. [Checklists de Implementación](#6-checklists-de-implementación)
7. [Métricas y Monitoreo](#7-métricas-y-monitoreo)
8. [Ejercicios Finales](#8-ejercicios-finales)

---

## 1. Patrones de Arquitectura

### Patrón 1: Agente Único con MCPs

El patrón más simple: un agente de IA conectado a múltiples MCPs.

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  GitHub  │ │ Firebase │ │   AWS    │ │ Postgres │  MCPs  │
│  │   MCP    │ │   MCP    │ │   MCP    │ │   MCP    │        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘        │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
    [GitHub]    [Firebase]     [AWS]     [PostgreSQL]
```

**Cuándo usar**:
- Proyectos pequeños/medianos
- Un solo desarrollador
- Tareas lineales

**Ejemplo de uso**:
```bash
claude "Crea un endpoint de usuarios:
1. Usa PostgreSQL MCP para crear la tabla
2. Implementa el código en src/api/users.ts
3. Crea un PR en GitHub
4. Despliega a AWS Lambda"
```

### Patrón 2: Multi-Agente Orquestado

Múltiples agentes especializados coordinados por un orquestador.

```
┌────────────────────────────────────────────────────────────────┐
│                    AGENTE ORQUESTADOR                           │
│                    (Claude Code)                                │
└────────────────────────────┬───────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Subagente     │ │   Subagente     │ │   Subagente     │
│   Frontend      │ │   Backend       │ │   Testing       │
│   (React/Vue)   │ │   (API/DB)      │ │   (Jest/Pytest) │
│   + GitHub MCP  │ │   + DB MCPs     │ │   + CI/CD MCP   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Cuándo usar**:
- Proyectos grandes
- Equipos múltiples
- Desarrollo paralelo

**Implementación**:
```bash
# Terminal 1: Agente Frontend
claude --profile frontend "Implementa el formulario de registro"

# Terminal 2: Agente Backend
claude --profile backend "Implementa la API de registro"

# Terminal 3: Agente Testing
claude --profile testing "Monitorea cambios y genera tests"

# Terminal 4: Orquestador
claude "Coordina la implementación de la feature de registro:
- Frontend está trabajando en el formulario
- Backend está trabajando en la API
- Testing generará tests cuando ambos terminen
Integra cuando todo esté listo."
```

### Patrón 3: Pipeline CI/CD Asistido

Agentes especializados en cada fase del pipeline.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Code     │───▶│    Test     │───▶│   Review    │───▶│   Deploy    │
│   Agent     │    │   Agent     │    │   Agent     │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼
   [Claude]           [Claude]          [Claude]           [Claude]
   Genera             Ejecuta           Revisa             Despliega
   código             tests             código             cambios
```

**Cuándo usar**:
- CI/CD automatizado
- Quality gates
- Deployment frecuente

### Patrón 4: Especialización por Dominio

Agentes expertos en áreas específicas.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ROUTER                                   │
│              (Analiza la tarea y la asigna)                      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
    ┌─────────────┬───────────┼───────────┬─────────────┐
    ▼             ▼           ▼           ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│Security│  │Database│  │  API   │  │  UI    │  │ DevOps │
│ Expert │  │ Expert │  │ Expert │  │ Expert │  │ Expert │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
```

**Implementación con profiles**:
```json
// ~/.claude/profiles/security-expert.json
{
  "name": "Security Expert",
  "systemPrompt": "Eres un experto en seguridad con 15 años de experiencia.
Tu enfoque principal es identificar vulnerabilidades OWASP Top 10,
revisar autenticación/autorización, y asegurar datos sensibles.",
  "model": "claude-opus-4-5-20251101"
}
```

---

## 2. Caso Práctico: Feature Completa

### Objetivo

Implementar un **Sistema de Notificaciones Push** usando desarrollo asistido por IA.

### Paso 1: Planificación

```bash
claude "Necesito implementar un sistema de notificaciones push para
nuestra app móvil.

Stack actual:
- Backend: Node.js + Express
- Base de datos: PostgreSQL
- Mobile: React Native
- Cloud: AWS

Analiza el codebase actual y propón una arquitectura que incluya:
1. Esquema de base de datos
2. Endpoints de API necesarios
3. Integración con Firebase Cloud Messaging
4. Componentes mobile

Genera un plan detallado antes de implementar."
```

### Paso 2: Configurar MCPs Necesarios

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

### Paso 3: Desarrollo Iterativo

#### 3.1 Crear estructura de base de datos

```bash
claude "Usando PostgreSQL MCP, crea las tablas necesarias:

1. notification_preferences
   - user_id (FK a users)
   - push_enabled (boolean)
   - email_enabled (boolean)
   - categories (jsonb) - qué tipos de notificaciones recibir

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

Incluye índices apropiados."
```

#### 3.2 Implementar endpoints API

```bash
claude "Implementa los endpoints REST en src/api/notifications/:

POST /api/notifications
- Crear y enviar notificación a usuario(s)
- Usar Firebase Cloud Messaging para push
- Guardar en base de datos

GET /api/notifications/:userId
- Listar notificaciones del usuario
- Paginación
- Filtros: read/unread, por fecha

PUT /api/notifications/:id/read
- Marcar como leída

POST /api/devices/register
- Registrar dispositivo para push
- Actualizar token si ya existe

DELETE /api/devices/:deviceId
- Eliminar dispositivo (logout)

Incluye:
- Validación con Joi/Zod
- Manejo de errores
- Logging
- Tests unitarios"
```

#### 3.3 Integrar Firebase Cloud Messaging

```bash
claude "Configura Firebase Cloud Messaging:

1. Usa el Firebase MCP para verificar la configuración
2. Crea src/services/pushService.ts con:
   - sendToDevice(token, payload)
   - sendToMultiple(tokens[], payload)
   - sendToTopic(topic, payload)
3. Implementa retry con exponential backoff
4. Maneja tokens inválidos (eliminar de DB)
5. Incluye métricas de envío"
```

#### 3.4 Ejecutar tests

```bash
claude "Ejecuta toda la suite de tests:
1. Tests unitarios de los nuevos endpoints
2. Tests de integración con la base de datos
3. Tests de integración con Firebase (mock)

Muestra el coverage y corrige cualquier fallo.
El coverage mínimo debe ser 80%."
```

#### 3.5 Code Review

```bash
claude "Revisa todo el código generado para notificaciones.

Verifica:
1. Seguridad
   - ¿Hay inyección SQL?
   - ¿Los endpoints están autenticados?
   - ¿Se validan los permisos?

2. Performance
   - ¿Queries eficientes?
   - ¿Hay N+1 queries?
   - ¿Se usa caché donde corresponde?

3. Mantenibilidad
   - ¿Código limpio y legible?
   - ¿Buena separación de responsabilidades?
   - ¿Documentación adecuada?

4. Edge cases
   - ¿Qué pasa si Firebase falla?
   - ¿Qué pasa con tokens expirados?
   - ¿Límites de rate?"
```

#### 3.6 Documentación

```bash
claude "Genera documentación:

1. Actualiza README.md con la nueva feature
2. Genera docs/api/notifications.md con:
   - Descripción de endpoints
   - Ejemplos de requests/responses
   - Códigos de error
3. Añade comentarios JSDoc a funciones públicas
4. Crea guía de configuración de Firebase"
```

#### 3.7 Pull Request

```bash
claude "Crea un Pull Request en GitHub:

1. Branch: feature/notifications-system
2. Título descriptivo
3. Descripción con:
   - Resumen de cambios
   - Screenshots si aplica
   - Testing realizado
   - Checklist de review
4. Asigna reviewers apropiados
5. Añade labels relevantes"
```

---

## 3. Workflow Completo con MCPs

### Escenario: Bug Fix Urgente en Producción

```bash
# 1. Identificar el bug (Sentry MCP)
claude "@sentry Muéstrame los errores críticos de las últimas 24 horas
en el servicio de pagos"

# Respuesta: Error AUTH_TOKEN_INVALID en checkout.js:234
# Stack trace: ...

# 2. Analizar código relacionado
claude "Analiza el stack trace del error AUTH_TOKEN_INVALID.
Lee el código en checkout.js y encuentra la causa raíz.
Revisa también los cambios recientes en Git que puedan estar relacionados."

# 3. Verificar en base de datos
claude "@postgres Revisa la tabla auth_tokens para ver si hay
tokens expirados o inválidos que coincidan con el timeframe del error"

# 4. Crear branch y fix
claude "Crea una branch 'hotfix/auth-token-validation'.
Implementa el fix basado en tu análisis.
Asegúrate de:
- Añadir validación de expiración
- Manejar el caso de token inválido gracefully
- Loggear el error correctamente"

# 5. Tests
claude "Escribe tests para cubrir el bug:
- Test cuando token está expirado
- Test cuando token es inválido
- Test cuando token es válido
Ejecuta los tests y verifica que pasen."

# 6. Code Review automático
claude "Revisa el fix implementado.
¿Hay efectos secundarios?
¿El fix es completo o solo parcial?"

# 7. Crear PR
claude "@github Crea un PR desde hotfix/auth-token-validation a main.
Usa el template de hotfix.
Marca como urgente."

# 8. Notificar al equipo
claude "@slack Envía un mensaje a #engineering:
'🚨 Hotfix para AUTH_TOKEN_INVALID en review.
PR #xxx - necesita review urgente.
Error afectaba checkout de pagos.'"

# 9. Deploy (después de approval)
claude "@aws Despliega el hotfix a producción usando CodeDeploy.
Monitorea los logs por 15 minutos después del deploy."
```

---

## 4. Automatización de Workflows

### GitHub Actions con Claude

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

          Enfócate en:
          1. Bugs potenciales
          2. Vulnerabilidades de seguridad
          3. Problemas de performance
          4. Mejores prácticas de código

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

            let body = '## 🤖 AI Code Review\n\n';
            body += `### Summary\n${review.summary}\n\n`;

            if (review.issues.length > 0) {
              body += '### Issues Found\n';
              for (const issue of review.issues) {
                body += `- **${issue.severity}** in \`${issue.file}:${issue.line}\`: ${issue.message}\n`;
                body += `  - Suggestion: ${issue.suggestion}\n`;
              }
            } else {
              body += '✅ No issues found!\n';
            }

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });
```

### Script de Migración Automática

```bash
#!/bin/bash
# scripts/ai-migrate.sh

echo "🚀 Iniciando migración asistida por IA..."

# 1. Analizar cambios en modelos
claude -p "Analiza los cambios en src/models/ desde el último release.
Genera las migraciones SQL necesarias para PostgreSQL.
Incluye:
- Alteraciones de tablas
- Nuevos índices
- Datos de seed si necesario" > migrations/$(date +%Y%m%d_%H%M%S).sql

# 2. Validar migración
claude -p "Valida la migración generada.
¿Es reversible?
¿Hay riesgo de pérdida de datos?
¿Se necesita downtime?"

# 3. Ejecutar en staging
echo "¿Ejecutar en staging? (y/n)"
read confirm
if [ "$confirm" = "y" ]; then
    claude "@postgres Ejecuta la última migración en la base de datos de staging"
fi
```

### Pre-commit Hook con IA

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🤖 Ejecutando AI pre-commit check..."

# Obtener archivos staged
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Quick AI review
REVIEW=$(claude -p "Review rápido de estos archivos (máximo 3 issues críticos):
$STAGED_FILES

Solo reporta issues de:
- Seguridad (inyecciones, secrets expuestos)
- Bugs obvios
- Errores de sintaxis

Responde 'OK' si no hay issues críticos." 2>/dev/null)

if [[ "$REVIEW" != *"OK"* ]]; then
    echo "⚠️ AI encontró issues:"
    echo "$REVIEW"
    echo ""
    echo "¿Continuar de todos modos? (y/n)"
    read -r confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi

echo "✅ Pre-commit check passed"
exit 0
```

---

## 5. Mejores Prácticas

### 1. Proporciona Contexto Rico

```markdown
# CLAUDE.md / GEMINI.md

## Proyecto: E-commerce Platform v2

### Stack Tecnológico
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Backend**: Node.js + Fastify + TypeORM
- **Base de datos**: PostgreSQL 15 + Redis 7
- **Infraestructura**: AWS (ECS, RDS, ElastiCache, S3)
- **CI/CD**: GitHub Actions + ArgoCD

### Arquitectura
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   Fastify   │────▶│  PostgreSQL │
│  Frontend   │     │   Backend   │     │    + Redis  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Convenciones de Código
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
- El rate limiter está en Redis, no modificar sin revisar
- Los pagos usan Stripe, webhooks en /api/webhooks/stripe
- El search usa Algolia, sincronización cada 5 min
```

### 2. Divide Tareas Complejas

```bash
# ❌ Malo - Demasiado amplio
claude "Construye un sistema de autenticación completo"

# ✅ Bueno - Pasos claros
claude "Paso 1: Diseña el schema de DB para auth:
- Tabla users (id, email, password_hash, created_at, updated_at)
- Tabla sessions (id, user_id, token, expires_at, ip, user_agent)
- Tabla password_resets (id, user_id, token, expires_at, used_at)
Usa PostgreSQL MCP para crear las tablas."

claude "Paso 2: Implementa endpoint POST /auth/register:
- Validación de email y password
- Hash de password con bcrypt (cost 12)
- Prevención de email duplicado
- Respuesta con usuario (sin password)"

claude "Paso 3: Implementa endpoint POST /auth/login:
- Verificar credenciales
- Crear sesión en DB
- Generar JWT con expiración 1h
- Refresh token con expiración 7d"

# ... continúa paso a paso
```

### 3. Usa TDD con IA

```bash
# Primero los tests
claude "Escribe tests para un servicio de carrito de compras.
El servicio debe:
- Añadir items (producto, cantidad)
- Remover items
- Actualizar cantidad
- Calcular subtotal por item
- Calcular total del carrito
- Aplicar descuentos (porcentaje o fijo)
- Manejar stock insuficiente

Usa Jest + TypeScript.
No implementes el servicio aún, solo los tests."

# Luego la implementación
claude "Implementa CartService para que pasen todos los tests.
Los tests están en src/services/__tests__/cart.test.ts"

# Verificar
claude "Ejecuta los tests y muestra el coverage.
Añade tests para cualquier caso edge que falte."
```

### 4. Verificación Cruzada

```bash
# Usa diferentes herramientas para verificar
claude "Implementa la función de validación de tarjetas de crédito"

codex "Review this implementation for edge cases and security:
$(cat src/utils/cardValidation.ts)"

gemini "Check for performance issues and potential improvements:
$(cat src/utils/cardValidation.ts)"
```

### 5. Iteración y Refinamiento

```bash
# Iteración 1
claude "Genera un endpoint básico para búsqueda de productos"

# Iteración 2
claude "Ahora añade:
- Filtros por categoría, precio, rating
- Paginación
- Ordenamiento"

# Iteración 3
claude "Optimiza para performance:
- Añade índices necesarios
- Implementa caché con Redis
- Limita campos en respuesta"

# Iteración 4
claude "Añade búsqueda full-text con PostgreSQL tsvector
o integración con Elasticsearch si el volumen lo requiere"
```

---

## 6. Checklists de Implementación

### Para Nuevos Proyectos

```markdown
## Setup Inicial

### Contexto para IA
- [ ] Crear CLAUDE.md/GEMINI.md con descripción del proyecto
- [ ] Documentar stack tecnológico
- [ ] Definir convenciones de código
- [ ] Listar comandos frecuentes

### MCPs
- [ ] Identificar MCPs necesarios (DB, Cloud, Git, etc.)
- [ ] Configurar cada MCP con credenciales
- [ ] Probar conexión de cada MCP
- [ ] Documentar configuración en README

### Automatización
- [ ] Configurar hooks de pre-commit
- [ ] Crear comandos personalizados en .claude/commands/
- [ ] Integrar AI review en CI/CD
- [ ] Configurar notificaciones (Slack, etc.)

### Seguridad
- [ ] Variables de entorno para secrets (nunca en código)
- [ ] Configurar permisos mínimos en MCPs
- [ ] Activar modo confirmación para comandos peligrosos
- [ ] Revisar código generado antes de deploy
```

### Para Proyectos Existentes

```markdown
## Adopción de IA en Proyecto Existente

### Análisis Inicial
- [ ] Documentar arquitectura actual para contexto de IA
- [ ] Identificar deuda técnica que IA puede ayudar
- [ ] Mapear workflows actuales
- [ ] Identificar tareas repetitivas

### Integración Gradual
- [ ] Comenzar con code review asistido
- [ ] Añadir generación de tests
- [ ] Automatizar documentación
- [ ] Integrar en refactoring

### MCPs Específicos
- [ ] Configurar MCP para base de datos del proyecto
- [ ] Configurar MCP para cloud del proyecto
- [ ] Configurar integraciones específicas (Jira, Slack, etc.)

### Métricas
- [ ] Establecer baseline de productividad
- [ ] Definir métricas a trackear
- [ ] Configurar dashboard de seguimiento
```

### Para Cada Feature

```markdown
## Checklist de Feature

### Antes de Empezar
- [ ] Actualizar contexto en CLAUDE.md si cambió algo
- [ ] Verificar que MCPs necesarios estén funcionando
- [ ] Revisar dependencias y versiones

### Durante Desarrollo
- [ ] Dividir feature en pasos manejables
- [ ] Escribir tests antes o junto con código
- [ ] Ejecutar tests frecuentemente
- [ ] Hacer commits pequeños y frecuentes

### Antes de PR
- [ ] Ejecutar suite completa de tests
- [ ] Verificar cobertura mínima
- [ ] Ejecutar linter y formatter
- [ ] Hacer self-review del código
- [ ] Actualizar documentación

### Después de Merge
- [ ] Verificar deploy exitoso
- [ ] Monitorear logs y métricas
- [ ] Documentar learnings
```

---

## 7. Métricas y Monitoreo

### Dashboard de Productividad

```python
# scripts/ai_metrics.py
"""
Sistema de métricas para desarrollo asistido por IA.
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AIInteraction:
    """Representa una interacción con herramienta de IA."""
    timestamp: str
    tool: str  # claude, codex, gemini
    task_type: str  # code_gen, review, debug, docs, test
    duration_seconds: float
    tokens_used: int
    success: bool
    error_message: str = ""

class MetricsCollector:
    """Recolector de métricas de uso de IA."""

    def __init__(self, output_file: str = "ai_metrics.jsonl"):
        self.output_file = Path(output_file)

    def log_interaction(self, interaction: AIInteraction):
        """Registra una interacción."""
        with open(self.output_file, "a") as f:
            f.write(json.dumps(asdict(interaction)) + "\n")

    def get_summary(self, days: int = 7) -> dict:
        """Genera resumen de métricas."""
        interactions = []
        cutoff = datetime.now().timestamp() - (days * 86400)

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

### Integración con Dashboard

```python
# scripts/metrics_dashboard.py
from flask import Flask, jsonify, render_template
from ai_metrics import MetricsCollector

app = Flask(__name__)
collector = MetricsCollector()

@app.route("/api/metrics")
def get_metrics():
    days = request.args.get("days", 7, type=int)
    return jsonify(collector.get_summary(days))

@app.route("/api/metrics/export")
def export_metrics():
    """Exporta métricas para análisis externo."""
    # Formato compatible con Grafana, Datadog, etc.
    pass

@app.route("/")
def dashboard():
    return render_template("dashboard.html", metrics=collector.get_summary())

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

### KPIs Sugeridos

| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| **Tiempo de desarrollo** | Tiempo promedio por feature | Reducir 30% |
| **Bugs en producción** | Bugs encontrados post-deploy | Reducir 50% |
| **Cobertura de tests** | % de código cubierto | Mínimo 80% |
| **Tiempo de review** | Tiempo hasta approval de PR | Reducir 40% |
| **Satisfacción del dev** | Encuesta mensual (1-10) | Mínimo 8 |

---

## 8. Ejercicios Finales

### Ejercicio 1: Proyecto Completo

**Objetivo**: Implementar una API de gestión de tareas con desarrollo asistido por IA.

**Requisitos**:
1. CRUD de tareas (crear, leer, actualizar, eliminar)
2. Autenticación con JWT
3. Base de datos PostgreSQL
4. Tests con cobertura >80%
5. Documentación OpenAPI
6. Deploy a cloud (AWS/GCP/Azure)

**Pasos**:
1. Configura CLAUDE.md con el contexto
2. Configura MCPs necesarios (PostgreSQL, GitHub, cloud)
3. Usa el patrón de desarrollo iterativo
4. Implementa cada endpoint con tests
5. Haz code review con IA
6. Despliega con asistencia de IA

### Ejercicio 2: Migración de Proyecto Existente

**Objetivo**: Migrar un proyecto legacy a arquitectura moderna con ayuda de IA.

**Tareas**:
1. Analiza el código legacy con IA
2. Identifica patrones y anti-patrones
3. Diseña nueva arquitectura
4. Migra módulo por módulo
5. Mantén compatibilidad durante la migración
6. Documenta el proceso

### Ejercicio 3: Automatización de Workflow

**Objetivo**: Crear un pipeline CI/CD completamente asistido por IA.

**Componentes**:
1. Pre-commit hooks con AI review
2. GitHub Actions para testing
3. AI code review en PRs
4. Deploy automatizado
5. Monitoreo post-deploy
6. Alertas inteligentes

### Ejercicio 4: Crear tu Propio MCP

**Objetivo**: Desarrollar un MCP para una API o servicio que uses frecuentemente.

**Ideas**:
- MCP para tu sistema de tickets (Jira, Linear, etc.)
- MCP para tu sistema de monitoreo
- MCP para tu base de datos específica
- MCP para tu cloud provider

### Ejercicio 5: Documentar y Compartir

**Objetivo**: Crear documentación completa del setup de IA para tu equipo.

**Incluir**:
1. Guía de instalación paso a paso
2. Mejores prácticas aprendidas
3. Errores comunes y soluciones
4. Templates de CLAUDE.md
5. Configuraciones de MCPs recomendadas
6. Workflows automatizados

---

## Recursos Adicionales

### Documentación Oficial
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Gemini CLI Docs](https://ai.google.dev/gemini-cli)
- [Codex CLI Docs](https://platform.openai.com/docs/codex)
- [MCP Specification](https://modelcontextprotocol.io)

### Repositorios de Referencia
- [MCP Servers (Oficial)](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [FastMCP](https://github.com/jlowin/fastmcp)

### Comunidades
- [Claude Developers Discord](https://discord.gg/anthropic)
- [Gemini CLI GitHub Discussions](https://github.com/google-gemini/gemini-cli/discussions)
- [MCP Community](https://github.com/modelcontextprotocol/discussions)

---

## Conclusión del Curso

Has completado el curso de **IA para Desarrollo de Software**. Ahora tienes:

1. **Conocimiento de APIs**: Claude, OpenAI, Gemini, DeepSeek, Grok
2. **Dominio de CLIs**: Claude Code, Gemini CLI, Codex CLI
3. **Fundamentos sólidos**: Contexto, MCP, subagentes, hooks
4. **MCPs del mercado**: AWS, Cloudflare, Firebase, GitHub, bases de datos
5. **Capacidad de crear MCPs propios**: Python y TypeScript
6. **Arquitecturas de desarrollo**: Patrones, workflows, automatización

**Próximos pasos sugeridos**:
1. Implementa los ejercicios en proyectos reales
2. Contribuye a MCPs open source
3. Comparte tu conocimiento con el equipo
4. Mantente actualizado con nuevas versiones

---

*Curso actualizado: Enero 2026*
*Versión: 1.0*
