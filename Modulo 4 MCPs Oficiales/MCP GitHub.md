# GitHub MCP

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Principiante |
| **Requisitos** | Cuenta GitHub, Personal Access Token |
| **Riesgo** | Medio (según permisos del token) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Generar un token de GitHub con permisos mínimos
- [ ] Configurar el GitHub MCP
- [ ] Gestionar issues y PRs desde Claude
- [ ] Crear branches y hacer push de archivos
- [ ] Automatizar workflows de desarrollo

---

Con el GitHub MCP puedes:
- Gestionar issues y PRs sin salir de Claude
- Automatizar revisiones de código
- Crear workflows de desarrollo integrados

---

## Configuración

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

## Obtener GitHub Token

1. Ve a [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. "Generate new token" → "Fine-grained tokens" (recomendado)
3. Nombre descriptivo: "MCP-Claude"
4. Selecciona repositorios: Solo los necesarios
5. Permisos recomendados:
   - Contents: Read and write
   - Issues: Read and write
   - Pull requests: Read and write
   - Metadata: Read
6. Generate y copia el token

> ⚠️ **No uses tokens con acceso a todos tus repositorios** si solo necesitas acceso a uno.

---

## Tools Disponibles

### Repositorios

| Tool | Función |
|------|---------|
| `search_repositories` | Buscar repositorios |
| `get_file_contents` | Leer archivo del repo |
| `create_or_update_file` | Crear/actualizar archivo |
| `push_files` | Push múltiples archivos |
| `list_commits` | Listar commits |
| `get_commit` | Detalle de commit |

### Issues

| Tool | Función |
|------|---------|
| `list_issues` | Listar issues |
| `get_issue` | Obtener issue |
| `create_issue` | Crear issue |
| `update_issue` | Actualizar issue |
| `add_issue_comment` | Añadir comentario |

### Pull Requests

| Tool | Función |
|------|---------|
| `list_pull_requests` | Listar PRs |
| `get_pull_request` | Obtener PR |
| `create_pull_request` | Crear PR |
| `create_pull_request_review` | Crear review |
| `merge_pull_request` | Mergear PR |
| `get_pull_request_files` | Archivos del PR |
| `get_pull_request_diff` | Diff del PR |

### Branches

| Tool | Función |
|------|---------|
| `create_branch` | Crear branch |
| `list_branches` | Listar branches |

---

## Ejemplo de Workflow

```
Usuario: "Crea un issue sobre el bug de login en taskflow-app"
Claude: create_issue(
  repo="mi-org/taskflow-app",
  title="Bug: Login no valida email correctamente",
  body="## Descripción\nEl formulario acepta emails inválidos...",
  labels=["bug", "priority-high"]
)

Usuario: "Lista los PRs abiertos"
Claude: list_pull_requests(repo="mi-org/taskflow-app", state="open")

Usuario: "Crea un PR desde fix/login-validation a main"
Claude: create_pull_request(
  repo="mi-org/taskflow-app",
  title="Fix: Validación de email en login",
  head="fix/login-validation",
  base="main",
  body="## Cambios\n- Validación de formato email\n\nCloses #42"
)
```

---

## Verificar token

```bash
curl -H "Authorization: token ghp_xxx" https://api.github.com/user
```

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Verificar tu token con `curl` hacia la API de GitHub
- [ ] Listar issues de un repositorio desde Claude
- [ ] Crear un issue de prueba
- [ ] Entender los permisos mínimos necesarios

---

## Resumen

| Aspecto | GitHub MCP |
|---------|------------|
| **Mejor para** | Automatizar gestión de issues, PRs y código |
| **Feature clave** | Integración completa con Git sin usar terminal |
| **Precaución** | Usar Fine-grained tokens con acceso limitado |
| **Caso de uso** | Crear issues desde análisis de código, revisar PRs |

---

## Recursos

- [GitHub Token Settings](https://github.com/settings/tokens)
- [GitHub API Documentation](https://docs.github.com/en/rest)
