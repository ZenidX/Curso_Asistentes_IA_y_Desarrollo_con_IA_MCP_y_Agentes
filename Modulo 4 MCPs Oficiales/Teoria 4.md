# Módulo 4: MCPs Oficiales del Mercado

## Información del Módulo

| Campo | Detalle |
|-------|---------|
| **Duración estimada** | 4-5 horas |
| **Nivel** | Intermedio |
| **Prerrequisitos** | Módulo 1-3 completados |
| **Herramientas necesarias** | Claude Desktop/CLI, Node.js 18+ |

---

## Contenido del Módulo

| Archivo | Categoría | MCPs incluidos |
|---------|-----------|----------------|
| [MCP Referencia Anthropic.md](MCP%20Referencia%20Anthropic.md) | Oficiales Anthropic | Filesystem, Git, Memory, Fetch |
| [MCP AWS.md](MCP%20AWS.md) | Cloud AWS | API, Knowledge, CDK, Cost Analysis |
| [MCP Cloudflare.md](MCP%20Cloudflare.md) | Cloud Cloudflare | Workers, R2, D1, KV |
| [MCP Firebase.md](MCP%20Firebase.md) | Backend-as-a-Service | Auth, Firestore, Storage |
| [MCP GitHub.md](MCP%20GitHub.md) | Desarrollo | Repos, Issues, PRs |
| [MCP Bases de Datos.md](MCP%20Bases%20de%20Datos.md) | Persistencia | PostgreSQL, MySQL, MongoDB, SQLite, Redis |
| [MCP Supabase.md](MCP%20Supabase.md) | Backend-as-a-Service | Database, Auth, Storage, Edge Functions |
| [MCP Vercel.md](MCP%20Vercel.md) | Deployment | Projects, Deployments, Domains |

---

## Objetivos de Aprendizaje

Al finalizar este módulo, serás capaz de:

- [ ] Seleccionar MCPs oficiales según las necesidades del proyecto
- [ ] Configurar MCPs de referencia de Anthropic
- [ ] Integrar servicios cloud (AWS, Cloudflare, Vercel, Supabase)
- [ ] Conectar bases de datos relacionales y NoSQL
- [ ] Combinar múltiples MCPs para flujos de trabajo potentes

---

## Conexión con el Proyecto TaskFlow

En este módulo, expandiremos TaskFlow con MCPs oficiales:

```
TaskFlow Actual                    TaskFlow + MCPs Oficiales
-----------------                  -------------------------
[Tareas en memoria]      -->      [Tareas en Supabase/Firebase]
[Sin control de versión] -->      [Historial con Git MCP]
[Aislado]               -->       [Notificaciones via Slack]
[Archivos locales]      -->       [Almacenamiento en R2/S3]
[Deploy manual]         -->       [Deploy automático en Vercel]
```

---

## Tabla Resumen de MCPs

| Categoría | MCPs disponibles | Uso principal |
|-----------|------------------|---------------|
| **Referencia** | Filesystem, Git, Memory, Fetch | Operaciones básicas |
| **Cloud AWS** | API, CDK, Cost Analysis | Infraestructura AWS |
| **Cloud Cloudflare** | Workers, R2, D1, KV | Edge computing |
| **Backend** | Firebase, Supabase | BaaS completo |
| **Deployment** | Vercel | Deploy y hosting |
| **Bases de datos** | PostgreSQL, MySQL, MongoDB, SQLite, Redis | Persistencia |
| **Desarrollo** | GitHub, Git | Código y colaboración |
| **Comunicación** | Slack, Linear, Notion | Productividad |
| **DevOps** | Docker, Kubernetes, Sentry | Operaciones |

---

## Troubleshooting Común

### "MCP no aparece en la lista"

**Soluciones**:
1. Verificar sintaxis JSON
2. Reiniciar Claude Desktop
3. Verificar que el package npm existe: `npx -y @package/name --help`

### "Error de autenticación"

**Soluciones**:
1. Verificar que el token/key es correcto
2. Comprobar permisos del token
3. Verificar que el token no ha expirado

### "Timeout al conectar"

**Soluciones**:
1. Verificar conectividad de red
2. Comprobar URL para MCPs remotos
3. Revisar firewalls o proxies

---

## Ejercicios Prácticos

### Ejercicio 1: MCPs Básicos (20 min)
Configurar Filesystem y Git MCP, verificar funcionamiento.

### Ejercicio 2: Base de Datos (40 min)
Conectar TaskFlow a PostgreSQL o Supabase.

### Ejercicio 3: Workflow Completo (60 min)
Combinar múltiples MCPs: Fetch + DB + GitHub.

---

## Recursos Adicionales

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Supabase MCP Docs](https://supabase.com/docs/guides/getting-started/mcp)
- [Vercel MCP Docs](https://vercel.com/docs/mcp)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
