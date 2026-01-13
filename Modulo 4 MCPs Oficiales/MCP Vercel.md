# Vercel MCP

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Intermedio |
| **Requisitos** | Cuenta Vercel, Token de acceso |
| **Tipo** | Disponible remoto y local |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Configurar Vercel MCP (remoto o con token)
- [ ] Listar y gestionar proyectos y deployments
- [ ] Configurar variables de entorno
- [ ] Gestionar dominios personalizados
- [ ] Consultar logs de deployments

---

Vercel es la plataforma líder para deployment de aplicaciones frontend y serverless. Con el MCP puedes:
- Gestionar proyectos y deployments
- Configurar dominios
- Consultar logs y analytics
- Automatizar deploys desde Claude

---

## ¿Qué es Vercel?

- **Deployment**: Deploy automático desde Git
- **Serverless Functions**: API routes sin servidor
- **Edge Functions**: Código en el edge (baja latencia)
- **Hosting**: CDN global optimizado
- **Preview Deployments**: URL única por PR

---

## Configuración

### MCP Remoto (Recomendado)

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["mcp-remote", "https://vercel.com/api/mcp"]
    }
  }
}
```

La autenticación se realiza vía OAuth en el navegador.

### MCP con Token

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["-y", "@vercel/mcp"],
      "env": {
        "VERCEL_TOKEN": "tu-token-aqui"
      }
    }
  }
}
```

---

## Obtener Vercel Token

1. Ve a [Vercel Settings → Tokens](https://vercel.com/account/tokens)
2. Click "Create Token"
3. Nombre descriptivo: "MCP-Claude"
4. Selecciona scope (Full Account o proyecto específico)
5. Copia el token

> ⚠️ Los tokens tienen acceso completo a tu cuenta. Usa scopes limitados cuando sea posible.

---

## Tools Disponibles

### Proyectos

| Tool | Función |
|------|---------|
| `list_projects` | Listar proyectos |
| `get_project` | Obtener detalles de proyecto |
| `create_project` | Crear nuevo proyecto |
| `delete_project` | Eliminar proyecto |
| `update_project` | Actualizar configuración |

### Deployments

| Tool | Función |
|------|---------|
| `list_deployments` | Listar deployments |
| `get_deployment` | Obtener detalle de deployment |
| `create_deployment` | Crear nuevo deployment |
| `cancel_deployment` | Cancelar deployment en progreso |
| `redeploy` | Re-desplegar |

### Dominios

| Tool | Función |
|------|---------|
| `list_domains` | Listar dominios |
| `add_domain` | Añadir dominio |
| `remove_domain` | Eliminar dominio |
| `verify_domain` | Verificar DNS |

### Environment Variables

| Tool | Función |
|------|---------|
| `list_env_vars` | Listar variables de entorno |
| `create_env_var` | Crear variable |
| `update_env_var` | Actualizar variable |
| `delete_env_var` | Eliminar variable |

### Logs

| Tool | Función |
|------|---------|
| `get_deployment_logs` | Obtener logs de deployment |
| `get_function_logs` | Logs de serverless functions |

---

## Ejemplo de Workflow

```
Usuario: "Lista mis proyectos de Vercel"
Claude: list_projects()

Usuario: "Muestra los últimos deployments de taskflow-app"
Claude: list_deployments(project="taskflow-app", limit=5)

Usuario: "¿Por qué falló el último deployment?"
Claude: get_deployment_logs(deployment_id="dpl_xxx")

Usuario: "Redespliega la última versión exitosa"
Claude: redeploy(deployment_id="dpl_xxx_success")

Usuario: "Añade la variable de entorno DATABASE_URL"
Claude: create_env_var(
  project="taskflow-app",
  key="DATABASE_URL",
  value="postgresql://...",
  target=["production", "preview"]
)
```

---

## Integración con Git

Vercel se integra nativamente con GitHub/GitLab/Bitbucket:

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW TÍPICO                           │
│                                                              │
│  1. Push a GitHub                                           │
│        ↓                                                     │
│  2. Vercel detecta cambios automáticamente                  │
│        ↓                                                     │
│  3. Build y deploy automático                               │
│        ↓                                                     │
│  4. Preview URL para PRs / Production para main             │
└─────────────────────────────────────────────────────────────┘
```

Con el MCP puedes:
- Consultar estado de deployments
- Forzar redeploys
- Gestionar variables de entorno
- Configurar dominios

---

## Caso de uso: TaskFlow en Vercel

### 1. Deploy inicial

```
Usuario: "Conecta mi repo github.com/mi-usuario/taskflow a Vercel"
Claude: create_project(
  name="taskflow",
  git_repository={
    type: "github",
    repo: "mi-usuario/taskflow"
  },
  framework="nextjs"
)
```

### 2. Configurar dominio

```
Usuario: "Configura taskflow.midominio.com"
Claude: add_domain(
  project="taskflow",
  domain="taskflow.midominio.com"
)
```

### 3. Variables de entorno

```
Usuario: "Configura las variables para conectar con Supabase"
Claude:
- create_env_var(key="NEXT_PUBLIC_SUPABASE_URL", value="https://xxx.supabase.co")
- create_env_var(key="SUPABASE_SERVICE_KEY", value="eyJ...", target=["production"])
```

---

## Preview Deployments

Cada Pull Request genera una URL única de preview:

```
main branch     → taskflow.vercel.app
PR #42          → taskflow-git-feature-login-mi-usuario.vercel.app
PR #43          → taskflow-git-fix-bug-mi-usuario.vercel.app
```

Útil para:
- Revisar cambios antes de merge
- Compartir con stakeholders
- Testing de QA

---

## Edge Functions vs Serverless

| Tipo | Latencia | Cold Start | Uso |
|------|----------|------------|-----|
| **Edge Functions** | ~50ms | Sin cold start | Auth, redirects, A/B tests |
| **Serverless** | Variable | Posible | APIs, webhooks, procesamiento |

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Generar un token en Vercel Settings
- [ ] Listar tus proyectos desde Claude
- [ ] Ver los últimos deployments de un proyecto
- [ ] Entender el flujo Git → Vercel → Preview/Production

---

## Resumen

| Aspecto | Vercel MCP |
|---------|------------|
| **Mejor para** | Deployment de Next.js, React, frontend moderno |
| **Ventaja clave** | Preview URLs por PR, CDN global, Edge Functions |
| **Integración** | GitHub/GitLab/Bitbucket nativa |
| **Caso de uso** | Gestionar deploys y env vars desde Claude |

---

## Recursos

- [Vercel MCP Docs](https://vercel.com/docs/mcp)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Vercel Templates](https://vercel.com/templates)
