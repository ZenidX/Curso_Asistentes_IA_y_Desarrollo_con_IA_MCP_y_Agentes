# Módulo 4: MCPs Oficiales del Mercado

## Índice
1. [MCPs de Referencia (Anthropic)](#1-mcps-de-referencia-anthropic)
2. [AWS MCP Servers](#2-aws-mcp-servers)
3. [Cloudflare MCP Servers](#3-cloudflare-mcp-servers)
4. [Firebase MCP](#4-firebase-mcp)
5. [GitHub MCP](#5-github-mcp)
6. [Bases de Datos](#6-bases-de-datos)
7. [Otros MCPs Populares](#7-otros-mcps-populares)
8. [Ejercicios Prácticos](#8-ejercicios-prácticos)

---

## 1. MCPs de Referencia (Anthropic)

Anthropic mantiene una colección de servidores MCP oficiales que demuestran las capacidades del protocolo y sirven como referencia.

### Servidores Disponibles

| MCP Server | Función | npm Package |
|------------|---------|-------------|
| **Everything** | Servidor demo con todas las capacidades | `@modelcontextprotocol/server-everything` |
| **Filesystem** | Operaciones de archivos seguras | `@modelcontextprotocol/server-filesystem` |
| **Git** | Operaciones con repositorios Git | `@modelcontextprotocol/server-git` |
| **Memory** | Memoria persistente (knowledge graph) | `@modelcontextprotocol/server-memory` |
| **Fetch** | Obtener contenido web | `@modelcontextprotocol/server-fetch` |
| **Sequential Thinking** | Razonamiento paso a paso | `@modelcontextprotocol/server-sequential-thinking` |
| **Postgres** | Consultas PostgreSQL | `@modelcontextprotocol/server-postgres` |
| **SQLite** | Base de datos SQLite | `@modelcontextprotocol/server-sqlite` |
| **Puppeteer** | Automatización de browser | `@modelcontextprotocol/server-puppeteer` |
| **Brave Search** | Búsqueda web | `@modelcontextprotocol/server-brave-search` |
| **Google Maps** | Datos de ubicación | `@modelcontextprotocol/server-google-maps` |
| **Slack** | Integración con Slack | `@modelcontextprotocol/server-slack` |

### Filesystem MCP

Control seguro de acceso a archivos.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu-usuario/proyectos",
        "/Users/tu-usuario/documentos"
      ]
    }
  }
}
```

**Tools disponibles**:
- `read_file`: Leer archivo
- `read_multiple_files`: Leer múltiples archivos
- `write_file`: Escribir archivo
- `create_directory`: Crear directorio
- `list_directory`: Listar contenido
- `move_file`: Mover/renombrar
- `search_files`: Buscar archivos
- `get_file_info`: Información del archivo

### Git MCP

Operaciones con repositorios Git.

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

**Tools disponibles**:
- `git_status`: Estado del repo
- `git_diff`: Ver cambios
- `git_log`: Historial de commits
- `git_commit`: Crear commit
- `git_branch`: Gestión de branches
- `git_checkout`: Cambiar de branch
- `git_add`: Añadir archivos al staging

### Memory MCP

Sistema de memoria persistente basado en knowledge graph.

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

**Tools disponibles**:
- `create_entities`: Crear entidades en el grafo
- `create_relations`: Crear relaciones
- `search_nodes`: Buscar en el grafo
- `read_graph`: Leer estado del grafo
- `delete_entities`: Eliminar entidades

### Fetch MCP

Obtener contenido web optimizado para LLMs.

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

**Tools disponibles**:
- `fetch`: Obtener URL y convertir a markdown
- `fetch_raw`: Obtener contenido raw

---

## 2. AWS MCP Servers

AWS proporciona una suite completa de servidores MCP para sus servicios.

### Servidores Principales

| Servidor | Función |
|----------|---------|
| **AWS API** | Ejecutar cualquier comando AWS CLI |
| **AWS Knowledge** | Documentación y best practices |
| **AWS CDK** | Guía de CDK y CloudFormation |
| **AWS Cost Analysis** | Análisis de costos |
| **AWS Nova Canvas** | Generación de imágenes con Nova |

### AWS API MCP

```json
{
  "mcpServers": {
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil",
        "AWS_REGION": "eu-west-1",
        "READ_OPERATIONS_ONLY": "true"
      }
    }
  }
}
```

**Variables de entorno**:
- `AWS_PROFILE`: Perfil de AWS a usar
- `AWS_REGION`: Región por defecto
- `READ_OPERATIONS_ONLY`: "true" para solo lecturas (seguro)
- `ALLOWED_SERVICES`: Lista de servicios permitidos (ej: "s3,ec2,lambda")

**Tools disponibles**:
- `execute_aws_command`: Ejecutar comandos AWS CLI
- `get_execution_plan`: Obtener plan paso a paso para tareas

**Ejemplo de uso**:
```
"Lista todos los buckets de S3"
→ Ejecuta: aws s3 ls

"Describe las instancias EC2 en eu-west-1"
→ Ejecuta: aws ec2 describe-instances --region eu-west-1
```

### AWS Knowledge MCP (Remoto)

Servidor remoto para documentación y mejores prácticas de AWS.

```json
{
  "mcpServers": {
    "aws-knowledge": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http"
    }
  }
}
```

**Resources disponibles**:
- Documentación oficial de AWS
- Best practices
- Guías de arquitectura
- Ejemplos de código

### AWS CDK MCP

```json
{
  "mcpServers": {
    "aws-cdk": {
      "command": "uvx",
      "args": ["awslabs.cdk-mcp-server@latest"]
    }
  }
}
```

**Tools disponibles**:
- `cdk_synth`: Sintetizar template CloudFormation
- `cdk_diff`: Ver diferencias
- `cdk_deploy`: Desplegar stack
- Guías de patrones CDK

### AWS Cost Analysis MCP

```json
{
  "mcpServers": {
    "aws-cost": {
      "command": "uvx",
      "args": ["awslabs.cost-analysis-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil"
      }
    }
  }
}
```

**Tools disponibles**:
- Análisis de costos por servicio
- Predicciones de gasto
- Recomendaciones de optimización
- Comparativas históricas

---

## 3. Cloudflare MCP Servers

Cloudflare ofrece MCPs remotos para toda su plataforma de desarrollo.

### Servidores Disponibles

| Servidor | URL | Función |
|----------|-----|---------|
| **Workers** | `workers.mcp.cloudflare.com` | Gestión de Cloudflare Workers |
| **KV** | `kv.mcp.cloudflare.com` | Key-Value storage |
| **R2** | `r2.mcp.cloudflare.com` | Object storage (S3-compatible) |
| **D1** | `d1.mcp.cloudflare.com` | Base de datos SQL serverless |
| **Observability** | `observability.mcp.cloudflare.com` | Analytics, logs, trazas |
| **Bindings** | `bindings.mcp.cloudflare.com` | Gestión de bindings |

### Configuración General

```json
{
  "mcpServers": {
    "cloudflare-workers": {
      "command": "npx",
      "args": ["mcp-remote", "https://workers.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-r2": {
      "command": "npx",
      "args": ["mcp-remote", "https://r2.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-d1": {
      "command": "npx",
      "args": ["mcp-remote", "https://d1.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-kv": {
      "command": "npx",
      "args": ["mcp-remote", "https://kv.mcp.cloudflare.com/mcp"]
    }
  }
}
```

### Workers MCP

**Tools disponibles**:
- `list_workers`: Listar Workers
- `get_worker`: Obtener código de un Worker
- `deploy_worker`: Desplegar Worker
- `delete_worker`: Eliminar Worker
- `get_worker_logs`: Ver logs

### R2 MCP (Object Storage)

**Tools disponibles**:
- `list_buckets`: Listar buckets
- `list_objects`: Listar objetos en bucket
- `get_object`: Obtener objeto
- `put_object`: Subir objeto
- `delete_object`: Eliminar objeto

### D1 MCP (SQL Database)

**Tools disponibles**:
- `list_databases`: Listar bases de datos
- `execute_sql`: Ejecutar consulta SQL
- `get_schema`: Obtener schema

**Ejemplo de uso**:
```
"Crea una tabla de usuarios en D1"
→ CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, created_at DATETIME)

"Lista todos los usuarios"
→ SELECT * FROM users
```

---

## 4. Firebase MCP

### Instalación

```json
{
  "mcpServers": {
    "firebase": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "/path/to/serviceAccountKey.json",
        "FIREBASE_STORAGE_BUCKET": "tu-proyecto.firebasestorage.app"
      }
    }
  }
}
```

### Obtener Service Account Key

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Proyecto → Settings → Service Accounts
3. "Generate New Private Key"
4. Guarda el archivo JSON de forma segura

### Tools Disponibles

#### Authentication
| Tool | Función |
|------|---------|
| `auth_get_user` | Obtener usuario por UID |
| `auth_get_user_by_email` | Obtener usuario por email |
| `auth_list_users` | Listar usuarios |
| `auth_create_user` | Crear usuario |
| `auth_update_user` | Actualizar usuario |
| `auth_delete_user` | Eliminar usuario |

#### Firestore
| Tool | Función |
|------|---------|
| `firestore_add_document` | Crear documento |
| `firestore_get_document` | Obtener documento |
| `firestore_update_document` | Actualizar documento |
| `firestore_delete_document` | Eliminar documento |
| `firestore_query` | Consultar colección |
| `firestore_list_collections` | Listar colecciones |

#### Storage
| Tool | Función |
|------|---------|
| `storage_list_files` | Listar archivos |
| `storage_upload` | Subir archivo |
| `storage_download` | Descargar archivo |
| `storage_delete` | Eliminar archivo |
| `storage_get_metadata` | Obtener metadata |

### Ejemplo de Uso

```
"Crea un usuario con email test@example.com"
→ auth_create_user(email="test@example.com", password="...")

"Guarda un documento en la colección 'productos'"
→ firestore_add_document(collection="productos", data={nombre: "...", precio: 99})

"Busca productos con precio mayor a 50"
→ firestore_query(collection="productos", where=[["precio", ">", 50]])
```

---

## 5. GitHub MCP

### Configuración

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

### Obtener GitHub Token

1. Ve a [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. "Generate new token (classic)" o "Fine-grained tokens"
3. Selecciona los scopes necesarios:
   - `repo` (acceso a repositorios)
   - `read:org` (leer organizaciones)
   - `read:user` (leer perfil)
   - `workflow` (si necesitas GitHub Actions)

### Tools Disponibles

#### Repositorios
| Tool | Función |
|------|---------|
| `search_repositories` | Buscar repositorios |
| `get_file_contents` | Leer archivo del repo |
| `create_or_update_file` | Crear/actualizar archivo |
| `push_files` | Push múltiples archivos |
| `list_commits` | Listar commits |
| `get_commit` | Obtener detalle de commit |

#### Issues
| Tool | Función |
|------|---------|
| `list_issues` | Listar issues |
| `get_issue` | Obtener issue |
| `create_issue` | Crear issue |
| `update_issue` | Actualizar issue |
| `add_issue_comment` | Añadir comentario |

#### Pull Requests
| Tool | Función |
|------|---------|
| `list_pull_requests` | Listar PRs |
| `get_pull_request` | Obtener PR |
| `create_pull_request` | Crear PR |
| `create_pull_request_review` | Crear review |
| `merge_pull_request` | Mergear PR |
| `get_pull_request_files` | Archivos del PR |
| `get_pull_request_diff` | Diff del PR |

#### Branches
| Tool | Función |
|------|---------|
| `create_branch` | Crear branch |
| `list_branches` | Listar branches |

### Ejemplo de Uso

```
"Crea un issue sobre el bug de login en el repo my-org/my-app"
→ create_issue(
    repo="my-org/my-app",
    title="Bug en login",
    body="El formulario de login no valida correctamente...",
    labels=["bug", "priority-high"]
  )

"Lista los PRs abiertos"
→ list_pull_requests(repo="my-org/my-app", state="open")

"Crea un PR desde feature/auth a main"
→ create_pull_request(
    repo="my-org/my-app",
    title="Feature: Sistema de autenticación",
    head="feature/auth",
    base="main",
    body="## Cambios\n- Login/logout\n- Registro..."
  )
```

---

## 6. Bases de Datos

### PostgreSQL MCP

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://usuario:password@localhost:5432/mi_base"
      }
    }
  }
}
```

**Tools**:
- `query`: Ejecutar consulta SQL (SELECT)
- `execute`: Ejecutar modificación (INSERT, UPDATE, DELETE)
- `describe_table`: Describir estructura de tabla
- `list_tables`: Listar tablas

**Resources**:
- `schema://tables`: Lista de tablas
- `schema://table/{name}`: Schema de una tabla

### MySQL MCP

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@benborber/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "mi_base"
      }
    }
  }
}
```

### MongoDB MCP

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mcp-mongo-server"],
      "env": {
        "MONGODB_URI": "mongodb://localhost:27017/mi_base"
      }
    }
  }
}
```

**Tools**:
- `find`: Buscar documentos
- `insertOne`: Insertar documento
- `updateOne`: Actualizar documento
- `deleteOne`: Eliminar documento
- `aggregate`: Pipeline de agregación

### SQLite MCP

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
    }
  }
}
```

### Redis MCP

```json
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-redis"],
      "env": {
        "REDIS_URL": "redis://localhost:6379"
      }
    }
  }
}
```

---

## 7. Otros MCPs Populares

### Comunicación y Productividad

#### Slack MCP
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T..."
      }
    }
  }
}
```

#### Linear MCP
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "lin_api_..."
      }
    }
  }
}
```

#### Notion MCP
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_..."
      }
    }
  }
}
```

### DevOps

#### Docker MCP
```json
{
  "mcpServers": {
    "docker": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-docker"]
    }
  }
}
```

**Tools**:
- `list_containers`: Listar contenedores
- `start_container`: Iniciar contenedor
- `stop_container`: Parar contenedor
- `container_logs`: Ver logs
- `build_image`: Construir imagen

#### Kubernetes MCP
```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-kubernetes"],
      "env": {
        "KUBECONFIG": "~/.kube/config"
      }
    }
  }
}
```

### Monitoring

#### Sentry MCP
```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-sentry"],
      "env": {
        "SENTRY_AUTH_TOKEN": "...",
        "SENTRY_ORG": "mi-org"
      }
    }
  }
}
```

**Tools**:
- `list_issues`: Listar errores
- `get_issue`: Detalles de error
- `resolve_issue`: Marcar como resuelto
- `get_event`: Obtener evento específico

### Browser Automation

#### Puppeteer MCP
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Tools**:
- `navigate`: Navegar a URL
- `screenshot`: Captura de pantalla
- `click`: Hacer click
- `type`: Escribir texto
- `evaluate`: Ejecutar JavaScript

### Tabla Resumen

| Categoría | MCPs |
|-----------|------|
| **Cloud** | AWS API, AWS CDK, Cloudflare Workers/R2/D1/KV |
| **Bases de datos** | PostgreSQL, MySQL, MongoDB, SQLite, Redis |
| **Desarrollo** | GitHub, Git, Filesystem |
| **Comunicación** | Slack, Linear, Notion, Jira |
| **DevOps** | Docker, Kubernetes, Sentry |
| **Web** | Fetch, Puppeteer, Brave Search |
| **AI** | Memory, Sequential Thinking |

---

## 8. Ejercicios Prácticos

### Ejercicio 1: Configurar MCPs Básicos

1. Configura el MCP de Filesystem
2. Configura el MCP de Git
3. Verifica que funcionan con `/mcp`

### Ejercicio 2: Trabajar con GitHub MCP

```bash
# Configurar
claude --configure-mcp github

# Usar
claude "Lista los issues abiertos de mi repositorio principal"
claude "Crea un PR con los cambios actuales"
```

### Ejercicio 3: Base de Datos

1. Configura PostgreSQL MCP con una base de datos local
2. Pide a Claude que describa el schema
3. Genera consultas SQL complejas

### Ejercicio 4: AWS MCP

1. Configura AWS API MCP en modo READ_ONLY
2. Lista tus recursos de S3, EC2
3. Pide recomendaciones de optimización de costos

### Ejercicio 5: Combinar MCPs

```bash
# Usa múltiples MCPs en una tarea
claude "Analiza los errores de Sentry de las últimas 24 horas,
busca el código relacionado en GitHub, y crea un issue
con la propuesta de fix"
```

### Ejercicio 6: Crear Workflow con MCPs

Diseña un workflow que use:
1. GitHub MCP para gestionar PRs
2. PostgreSQL MCP para verificar migraciones
3. Slack MCP para notificar al equipo

---

## Recursos Adicionales

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [Cloudflare MCP Docs](https://developers.cloudflare.com/workers/ai/mcp/)

---

## Próximo Módulo

En el **Módulo 5: Desarrollo de MCPs Propios** aprenderás:
- Arquitectura de un MCP Server
- Crear MCPs en Python y TypeScript
- FastMCP para desarrollo rápido
- Testing y debugging de MCPs
