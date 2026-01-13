# Ejercicios: Módulo 6 - Arquitectura IA

## Información

| | |
|---|---|
| **Dificultad progresiva** | Intermedio → Avanzado → Experto |
| **Tiempo total estimado** | 6-8 horas |
| **Requisitos** | Módulos 1-5 completados, experiencia con proyectos reales |

---

## Ejercicio 1: Diseño de arquitectura básica

**Nivel**: Intermedio
**Tiempo**: 45 minutos

### Objetivo
Diseñar la arquitectura de integración IA para un proyecto existente.

### Escenario

Tienes una aplicación web existente:
- Frontend: React
- Backend: Express/Node.js
- BD: PostgreSQL
- Deploy: Vercel + Railway

### Tareas

1. **Analiza**: Identifica puntos donde la IA puede añadir valor
2. **Diseña**: Dibuja el diagrama de arquitectura con MCPs
3. **Prioriza**: Ordena las integraciones por impacto/esfuerzo

### Template de diseño

```markdown
## Arquitectura IA para [Nombre del Proyecto]

### 1. Puntos de integración identificados
| Área | Uso de IA | MCP necesario | Prioridad |
|------|-----------|---------------|-----------|
| Code review | Revisar PRs automáticamente | GitHub MCP | Alta |
| ... | ... | ... | ... |

### 2. Diagrama de arquitectura
[Incluir diagrama ASCII o imagen]

### 3. Flujo de datos
1. Developer hace push → GitHub
2. Webhook trigger → ...
3. ...

### 4. Consideraciones de seguridad
- ...

### 5. Plan de implementación
- Fase 1: ...
- Fase 2: ...
```

### Criterios de éxito
- [ ] Identificados al menos 5 puntos de integración
- [ ] Diagrama claro y completo
- [ ] Plan de implementación realista

---

## Ejercicio 2: Patrón Agente Único

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Implementar el patrón de agente único con múltiples MCPs.

### Configuración

```json
{
  "mcpServers": {
    "filesystem": { ... },
    "git": { ... },
    "postgres": { ... },
    "github": { ... }
  }
}
```

### Escenario

Crea un workflow que:
1. Lea un archivo de especificación
2. Genere código según la especificación
3. Lo guarde en el filesystem
4. Cree un commit
5. Abra un PR en GitHub

### Ejemplo de ejecución

```bash
claude
> Lee la especificación en specs/new-feature.md y:
> 1. Implementa el código según lo especificado
> 2. Guárdalo en src/features/
> 3. Crea tests en tests/features/
> 4. Commitea con mensaje descriptivo
> 5. Crea un PR con la descripción de la feature
```

### Criterios de éxito
- [ ] Workflow completo ejecutado
- [ ] Todos los MCPs usados correctamente
- [ ] PR creado y listo para review

---

## Ejercicio 3: Patrón Multi-Agente

**Nivel**: Avanzado
**Tiempo**: 60 minutos

### Objetivo
Diseñar e implementar un sistema multi-agente.

### Arquitectura

```
                    ┌─────────────────┐
                    │   ORQUESTADOR   │
                    │    (Claude)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         v                   v                   v
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  AGENTE CÓDIGO │  │  AGENTE TESTS  │  │  AGENTE DOCS   │
│    - Escribe   │  │   - Genera     │  │  - Documenta   │
│    - Refactor  │  │   - Ejecuta    │  │  - README      │
│    - Review    │  │   - Reporta    │  │  - API Docs    │
└────────────────┘  └────────────────┘  └────────────────┘
```

### Implementación

```bash
# Crear comandos para cada agente
mkdir -p .claude/commands

# Agente de código
cat > .claude/commands/agent-code.md << 'EOF'
# Agente de Código

Eres un agente especializado en escribir código.

## Responsabilidades
- Implementar features según especificaciones
- Refactorizar código existente
- Seguir las convenciones del proyecto

## Restricciones
- NO ejecutes tests (eso lo hace otro agente)
- NO escribas documentación (eso lo hace otro agente)
- Solo código de producción

## Output
Cuando termines, indica qué archivos creaste/modificaste.
EOF

# Similar para agent-tests.md y agent-docs.md
```

### Workflow de orquestación

```bash
claude
> Actúa como orquestador:
> 1. Llama al agente de código para implementar la feature X
> 2. Con los archivos creados, llama al agente de tests
> 3. Si los tests pasan, llama al agente de docs
> 4. Consolida los resultados y reporta
```

### Criterios de éxito
- [ ] Agentes especializados creados
- [ ] Orquestación funcionando
- [ ] Comunicación entre agentes clara

---

## Ejercicio 4: CI/CD con IA

**Nivel**: Avanzado
**Tiempo**: 55 minutos

### Objetivo
Integrar IA en el pipeline de CI/CD.

### Pipeline propuesto

```yaml
# .github/workflows/ai-pipeline.yml
name: AI-Enhanced Pipeline

on:
  pull_request:
    branches: [main]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: AI Code Review
        run: |
          # Obtener diff del PR
          git diff origin/main...HEAD > diff.txt

          # Enviar a Claude para review
          claude -p "Revisa este diff y reporta problemas:
          $(cat diff.txt)

          Formato de salida:
          - CRÍTICO: problemas de seguridad
          - ALTO: bugs potenciales
          - MEDIO: mejoras de código
          - BAJO: sugerencias de estilo"

      - name: AI Test Generation
        if: success()
        run: |
          # Identificar archivos nuevos/modificados
          FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(ts|js)$')

          for file in $FILES; do
            claude -p "Genera tests para: $file"
          done

      - name: Post Review Comment
        uses: actions/github-script@v6
        with:
          script: |
            // Postear resultado como comentario en el PR
```

### Tareas

1. Adapta el workflow a tu proyecto
2. Implementa el script de review
3. Configura los secretos necesarios
4. Prueba con un PR real

### Criterios de éxito
- [ ] Workflow ejecuta en cada PR
- [ ] Reviews generados automáticamente
- [ ] Comentarios posteados en GitHub

---

## Ejercicio 5: Automatización de tareas repetitivas

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Crear scripts de automatización para tareas diarias.

### Scripts a crear

```bash
# 1. morning-standup.sh - Resumen diario
#!/bin/bash
claude "Genera un resumen para el standup basándote en:
1. Commits de ayer: $(git log --since='yesterday' --oneline)
2. PRs abiertos: $(gh pr list --state open)
3. Issues asignados: $(gh issue list --assignee @me)

Formato:
- Qué hice ayer
- Qué haré hoy
- Bloqueantes"

# 2. weekly-report.sh - Reporte semanal
#!/bin/bash
claude "Genera un reporte semanal basándote en:
1. Commits de la semana: $(git log --since='1 week ago' --oneline)
2. PRs mergeados: $(gh pr list --state merged --search 'merged:>=$(date -d '7 days ago' +%Y-%m-%d)')
3. Issues cerrados: $(gh issue list --state closed --search 'closed:>=$(date -d '7 days ago' +%Y-%m-%d)')

Incluye:
- Logros principales
- Métricas (PRs, issues, líneas de código)
- Próximos pasos"

# 3. tech-debt-audit.sh - Auditoría de deuda técnica
#!/bin/bash
claude "Analiza el proyecto y encuentra:
1. TODOs y FIXMEs en el código
2. Dependencias desactualizadas
3. Código duplicado
4. Archivos sin tests

Genera un informe priorizado por impacto."
```

### Criterios de éxito
- [ ] Scripts ejecutan correctamente
- [ ] Output útil y accionable
- [ ] Integrados en el flujo de trabajo

---

## Ejercicio 6: Métricas y monitoreo

**Nivel**: Avanzado
**Tiempo**: 60 minutos

### Objetivo
Implementar un sistema de métricas para desarrollo asistido por IA.

### Métricas a trackear

```python
# metrics_collector.py
import json
from datetime import datetime
from pathlib import Path

class AIMetrics:
    def __init__(self, metrics_file="ai_metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.load_metrics()

    def load_metrics(self):
        if self.metrics_file.exists():
            self.data = json.loads(self.metrics_file.read_text())
        else:
            self.data = {
                "sessions": [],
                "tools_usage": {},
                "tokens_used": 0,
                "time_saved_estimate": 0
            }

    def save_metrics(self):
        self.metrics_file.write_text(json.dumps(self.data, indent=2))

    def log_session(self, duration_minutes: int, tools_used: list, tokens: int):
        """Registra una sesión de trabajo con IA."""
        session = {
            "date": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
            "tools_used": tools_used,
            "tokens": tokens
        }
        self.data["sessions"].append(session)
        self.data["tokens_used"] += tokens

        for tool in tools_used:
            self.data["tools_usage"][tool] = self.data["tools_usage"].get(tool, 0) + 1

        # Estimar tiempo ahorrado (heurística simple)
        self.data["time_saved_estimate"] += duration_minutes * 0.5

        self.save_metrics()

    def generate_report(self) -> str:
        """Genera un reporte de métricas."""
        total_sessions = len(self.data["sessions"])
        total_time = sum(s["duration_minutes"] for s in self.data["sessions"])
        top_tools = sorted(
            self.data["tools_usage"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        report = f"""
# Reporte de Métricas IA

## Resumen
- **Sesiones totales**: {total_sessions}
- **Tiempo total con IA**: {total_time} minutos
- **Tokens consumidos**: {self.data['tokens_used']:,}
- **Tiempo ahorrado estimado**: {self.data['time_saved_estimate']:.0f} minutos

## Top 5 herramientas más usadas
{chr(10).join(f'- {tool}: {count} veces' for tool, count in top_tools)}
        """
        return report

# Uso
metrics = AIMetrics()
metrics.log_session(
    duration_minutes=30,
    tools_used=["git", "filesystem", "github"],
    tokens=5000
)
print(metrics.generate_report())
```

### Criterios de éxito
- [ ] Métricas se recopilan automáticamente
- [ ] Reportes generados semanalmente
- [ ] Datos útiles para optimización

---

## Ejercicio 7: Seguridad y permisos

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Implementar un sistema de permisos y auditoría para MCPs.

### Sistema de permisos

```python
# permissions.py
from enum import Enum
from typing import Set
import json

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"

class MCPPermissions:
    def __init__(self, config_file="mcp_permissions.json"):
        self.config = self._load_config(config_file)

    def _load_config(self, file):
        default = {
            "filesystem": [Permission.READ.value],
            "git": [Permission.READ.value, Permission.WRITE.value],
            "github": [Permission.READ.value],
            "postgres": [Permission.READ.value],
        }
        try:
            with open(file) as f:
                return json.load(f)
        except FileNotFoundError:
            return default

    def check_permission(self, mcp: str, action: Permission) -> bool:
        """Verifica si un MCP tiene permiso para una acción."""
        mcp_permissions = self.config.get(mcp, [])
        return action.value in mcp_permissions or Permission.ADMIN.value in mcp_permissions

    def audit_log(self, mcp: str, action: str, details: str):
        """Registra una acción para auditoría."""
        from datetime import datetime
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "mcp": mcp,
            "action": action,
            "details": details
        }
        with open("mcp_audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

# Wrapper para MCPs
class SecureMCPWrapper:
    def __init__(self, mcp_name: str, permissions: MCPPermissions):
        self.mcp_name = mcp_name
        self.permissions = permissions

    def execute(self, action: Permission, func, *args, **kwargs):
        if not self.permissions.check_permission(self.mcp_name, action):
            raise PermissionError(f"MCP {self.mcp_name} no tiene permiso para {action.value}")

        self.permissions.audit_log(self.mcp_name, action.value, str(args))
        return func(*args, **kwargs)
```

### Tareas

1. Implementa el sistema de permisos
2. Configura permisos por MCP
3. Habilita logging de auditoría
4. Prueba con operaciones reales

### Criterios de éxito
- [ ] Permisos enforced correctamente
- [ ] Audit log funcionando
- [ ] Operaciones no autorizadas bloqueadas

---

## Ejercicio 8: Testing de arquitectura

**Nivel**: Avanzado
**Tiempo**: 55 minutos

### Objetivo
Crear tests para validar la arquitectura de integración IA.

### Tests de integración

```python
# test_architecture.py
import pytest
from unittest.mock import Mock, patch
import asyncio

class TestMCPIntegration:
    """Tests de integración para MCPs."""

    @pytest.fixture
    def mock_filesystem_mcp(self):
        mcp = Mock()
        mcp.read_file.return_value = "file content"
        mcp.write_file.return_value = True
        return mcp

    @pytest.fixture
    def mock_git_mcp(self):
        mcp = Mock()
        mcp.status.return_value = {"modified": [], "staged": []}
        mcp.commit.return_value = {"sha": "abc123"}
        return mcp

    def test_workflow_read_modify_commit(self, mock_filesystem_mcp, mock_git_mcp):
        """Test: workflow de leer, modificar y commitear."""
        # Leer archivo
        content = mock_filesystem_mcp.read_file("test.py")
        assert content is not None

        # Modificar
        new_content = content + "\n# Modified by AI"
        mock_filesystem_mcp.write_file("test.py", new_content)

        # Commit
        mock_git_mcp.add(["test.py"])
        result = mock_git_mcp.commit("AI modification")

        assert result["sha"] is not None

    def test_mcp_failure_handling(self, mock_filesystem_mcp):
        """Test: manejo de errores de MCP."""
        mock_filesystem_mcp.read_file.side_effect = Exception("File not found")

        with pytest.raises(Exception) as exc_info:
            mock_filesystem_mcp.read_file("nonexistent.py")

        assert "File not found" in str(exc_info.value)

    def test_mcp_timeout(self, mock_filesystem_mcp):
        """Test: timeout de MCP."""
        async def slow_operation():
            await asyncio.sleep(10)
            return "result"

        mock_filesystem_mcp.slow_read = slow_operation

        with pytest.raises(asyncio.TimeoutError):
            asyncio.run(asyncio.wait_for(slow_operation(), timeout=1))

class TestSecurityPolicies:
    """Tests de políticas de seguridad."""

    def test_sensitive_data_not_logged(self):
        """Test: datos sensibles no se loguean."""
        from permissions import MCPPermissions
        perms = MCPPermissions()

        # Simular operación con datos sensibles
        perms.audit_log("postgres", "query", "SELECT * FROM users WHERE password = '***'")

        # Verificar que el password no aparece en el log
        with open("mcp_audit.log") as f:
            log_content = f.read()
            assert "actual_password" not in log_content

    def test_permission_escalation_blocked(self):
        """Test: escalación de permisos bloqueada."""
        from permissions import MCPPermissions, Permission

        perms = MCPPermissions()
        # filesystem solo tiene READ
        assert not perms.check_permission("filesystem", Permission.DELETE)
```

### Criterios de éxito
- [ ] Tests cubren flujos principales
- [ ] Tests de seguridad implementados
- [ ] CI ejecuta tests automáticamente

---

## Ejercicio 9: Documentación de arquitectura

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Crear documentación completa de la arquitectura IA.

### Template de documentación

```markdown
# Arquitectura de Desarrollo Asistido por IA

## 1. Visión General

### 1.1 Propósito
[Descripción del objetivo de la integración IA]

### 1.2 Alcance
[Qué incluye y qué no incluye]

## 2. Arquitectura

### 2.1 Diagrama de componentes
[Diagrama ASCII o imagen]

### 2.2 MCPs configurados
| MCP | Propósito | Permisos |
|-----|-----------|----------|
| filesystem | Gestión de archivos | read, write |
| git | Control de versiones | read, write |
| ... | ... | ... |

### 2.3 Flujos de trabajo
[Descripción de los flujos principales]

## 3. Seguridad

### 3.1 Modelo de permisos
[Descripción del sistema de permisos]

### 3.2 Auditoría
[Qué se loguea y dónde]

### 3.3 Datos sensibles
[Cómo se manejan]

## 4. Operación

### 4.1 Monitoreo
[Métricas y alertas]

### 4.2 Troubleshooting
[Problemas comunes y soluciones]

## 5. Mejores prácticas

### 5.1 Prompts efectivos
[Guía de prompts]

### 5.2 Code review con IA
[Proceso recomendado]

## 6. Roadmap
[Mejoras futuras planificadas]
```

### Criterios de éxito
- [ ] Documentación completa
- [ ] Diagramas claros
- [ ] Instrucciones actualizadas

---

## Ejercicio 10: Proyecto Final - TaskFlow Completo

**Nivel**: Experto
**Tiempo**: 3-4 horas

### Objetivo
Completar TaskFlow con arquitectura IA integral.

### Requisitos

1. **Backend funcional** con Express/Fastify
2. **Frontend** React básico
3. **Base de datos** PostgreSQL/Supabase
4. **MCP personalizado** para TaskFlow
5. **Integración CI/CD** con IA
6. **Documentación** completa
7. **Tests** >80% cobertura

### Estructura final

```
taskflow/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── services/
│   │   └── models/
│   ├── tests/
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── pages/
│   └── package.json
├── mcp-server/
│   ├── src/
│   ├── tests/
│   └── package.json
├── .claude/
│   ├── commands/
│   └── hooks.json
├── .github/
│   └── workflows/
│       └── ai-pipeline.yml
├── docs/
│   ├── architecture.md
│   └── api.md
├── CLAUDE.md
└── README.md
```

### Checklist de entrega

- [ ] Aplicación funcionando end-to-end
- [ ] MCP personalizado integrado
- [ ] CLAUDE.md con contexto completo
- [ ] Comandos personalizados creados
- [ ] CI/CD con review de IA
- [ ] Métricas de productividad
- [ ] Documentación de arquitectura
- [ ] Tests pasando
- [ ] Deploy en Vercel/Railway

### Demo final

Preparar una demo que muestre:
1. Uso del MCP desde Claude
2. Workflow completo de feature
3. CI/CD en acción
4. Métricas generadas

### Criterios de éxito
- [ ] Proyecto completo y funcional
- [ ] Arquitectura bien diseñada
- [ ] IA integrada en todo el ciclo
- [ ] Documentación profesional

---

## Recursos adicionales

- [MCP Documentation](https://modelcontextprotocol.io)
- [Claude Code Best Practices](https://docs.anthropic.com/claude-code)
- [Architecture Decision Records](https://adr.github.io/)
- [C4 Model for Architecture](https://c4model.com/)
