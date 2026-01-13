# Modulo 4: MCPs Oficiales del Mercado

---

## Informacion del Modulo

| Campo | Detalle |
|-------|---------|
| **Duracion estimada** | 4-5 horas |
| **Nivel** | Intermedio |
| **Prerrequisitos** | Modulo 1 (APIs de IA), Modulo 2 (Introduccion a MCP), Modulo 3 (Configuracion de Claude) |
| **Herramientas necesarias** | Claude Desktop/CLI, Node.js 18+, Git, cuenta en servicios cloud (opcional) |
| **Proyecto asociado** | TaskFlow - Gestor de tareas inteligente |

---

## Objetivos de Aprendizaje

Al finalizar este modulo, seras capaz de:

- [ ] Identificar y seleccionar MCPs oficiales segun las necesidades de tu proyecto
- [ ] Configurar MCPs de referencia de Anthropic (filesystem, git, memory, fetch)
- [ ] Integrar servicios cloud mediante AWS y Cloudflare MCPs
- [ ] Conectar bases de datos relacionales y NoSQL a traves de MCPs
- [ ] Combinar multiples MCPs para crear flujos de trabajo potentes
- [ ] Expandir TaskFlow con capacidades de almacenamiento, versionado y comunicacion

---

## Conexion con el Proyecto TaskFlow

**Recordatorio**: TaskFlow es nuestro gestor de tareas inteligente que hemos ido construyendo a lo largo del curso.

En este modulo, expandiremos TaskFlow con MCPs oficiales para darle **superpoderes reales**:

```
TaskFlow Actual                    TaskFlow + MCPs Oficiales
-----------------                  -------------------------
[Tareas en memoria]      -->      [Tareas en Firebase/PostgreSQL]
[Sin control de version] -->      [Historial con Git MCP]
[Aislado]               -->       [Notificaciones via Slack]
[Archivos locales]      -->       [Almacenamiento en S3/R2]
[Sin busqueda web]      -->       [Investigacion con Fetch MCP]
```

**Por que esto importa**: Un gestor de tareas profesional necesita persistencia, colaboracion y conectividad. Los MCPs oficiales nos dan todo esto sin escribir integraciones desde cero.

---

## Indice

1. [MCPs de Referencia (Anthropic)](#1-mcps-de-referencia-anthropic)
2. [AWS MCP Servers](#2-aws-mcp-servers)
3. [Cloudflare MCP Servers](#3-cloudflare-mcp-servers)
4. [Firebase MCP](#4-firebase-mcp)
5. [GitHub MCP](#5-github-mcp)
6. [Bases de Datos](#6-bases-de-datos)
7. [Otros MCPs Populares](#7-otros-mcps-populares)
8. [Troubleshooting](#8-troubleshooting)
9. [Ejercicios Practicos](#9-ejercicios-practicos)
10. [Resumen y Proximos Pasos](#10-resumen-y-proximos-pasos)

---

## 1. MCPs de Referencia (Anthropic)

**Tiempo estimado: 60 minutos**

### Por que empezar aqui

Los MCPs de Anthropic son la **referencia oficial** del protocolo. Estan mantenidos por los creadores de MCP y representan las mejores practicas. Piensa en ellos como los "drivers oficiales" - funcionan garantizadamente y sirven de modelo para entender como deben comportarse otros MCPs.

**Analogia**: Si MCP fuera un sistema operativo, estos serian los drivers que vienen preinstalados. Funcionan out-of-the-box y estan optimizados.

### Catalogo de Servidores Oficiales

| MCP Server | Funcion | Package npm | Uso en TaskFlow |
|------------|---------|-------------|-----------------|
| **Everything** | Demo con todas las capacidades | `@modelcontextprotocol/server-everything` | Pruebas y aprendizaje |
| **Filesystem** | Operaciones de archivos seguras | `@modelcontextprotocol/server-filesystem` | Exportar/importar tareas |
| **Git** | Operaciones con repositorios | `@modelcontextprotocol/server-git` | Versionado de configuracion |
| **Memory** | Memoria persistente (knowledge graph) | `@modelcontextprotocol/server-memory` | Recordar preferencias del usuario |
| **Fetch** | Obtener contenido web | `@modelcontextprotocol/server-fetch` | Enriquecer tareas con info de URLs |
| **Sequential Thinking** | Razonamiento paso a paso | `@modelcontextprotocol/server-sequential-thinking` | Descomponer tareas complejas |
| **Postgres** | Consultas PostgreSQL | `@modelcontextprotocol/server-postgres` | Base de datos principal |
| **SQLite** | Base de datos SQLite | `@modelcontextprotocol/server-sqlite` | Almacenamiento local ligero |
| **Puppeteer** | Automatizacion de browser | `@modelcontextprotocol/server-puppeteer` | Capturar screenshots de URLs |
| **Brave Search** | Busqueda web | `@modelcontextprotocol/server-brave-search` | Buscar recursos para tareas |
| **Google Maps** | Datos de ubicacion | `@modelcontextprotocol/server-google-maps` | Tareas geolocalizadas |
| **Slack** | Integracion Slack | `@modelcontextprotocol/server-slack` | Notificaciones de equipo |

### 1.1 Filesystem MCP

**Que hace**: Permite a Claude leer, escribir y gestionar archivos de forma **segura y controlada**.

**Por que es importante**: Sin este MCP, Claude no puede interactuar con tu sistema de archivos. Con el, puedes exportar tareas a JSON, importar configuraciones, o generar reportes.

**Configuracion**:

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

**Concepto clave**: Los directorios que pasas como argumentos son los **unicos** a los que Claude tendra acceso. Esto es un **sandbox de seguridad**.

> **Por que multiples directorios?** Puedes dar acceso granular. Por ejemplo: acceso a `/proyectos` para codigo y a `/documentos/exportaciones` solo para outputs, sin exponer todo tu home.

**Tools disponibles**:

| Tool | Funcion | Ejemplo de uso |
|------|---------|----------------|
| `read_file` | Leer un archivo | Cargar configuracion de TaskFlow |
| `read_multiple_files` | Leer varios archivos | Importar multiples listas de tareas |
| `write_file` | Escribir archivo | Exportar tareas a JSON |
| `create_directory` | Crear directorio | Crear carpeta de backups |
| `list_directory` | Listar contenido | Ver archivos de un proyecto |
| `move_file` | Mover/renombrar | Organizar archivos exportados |
| `search_files` | Buscar archivos | Encontrar todos los .json de tareas |
| `get_file_info` | Info del archivo | Verificar fecha de ultima modificacion |

**Error Comun**:
> **Ruta no accesible**: Si Claude dice que no puede acceder a un archivo, verifica que el directorio padre este en la lista de argumentos del MCP. El MCP **no** tiene acceso a rutas no declaradas explicitamente.

### 1.2 Git MCP

**Que hace**: Ejecuta operaciones Git directamente desde Claude.

**Por que es importante para TaskFlow**: Puedes versionar la configuracion de tu gestor de tareas, crear commits automaticos cuando se modifican tareas importantes, o revisar el historial de cambios.

**Configuracion**:

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

| Tool | Funcion | Caso de uso en TaskFlow |
|------|---------|------------------------|
| `git_status` | Estado del repo | Ver si hay cambios sin commitear |
| `git_diff` | Ver cambios | Revisar modificaciones en tareas |
| `git_log` | Historial de commits | Auditar quien cambio que |
| `git_commit` | Crear commit | Guardar estado de tareas |
| `git_branch` | Gestion de branches | Crear rama para experimentos |
| `git_checkout` | Cambiar de branch | Volver a version anterior |
| `git_add` | Anadir al staging | Preparar archivos para commit |

**Practica Guiada: Versionando TaskFlow**

```bash
# 1. Crea un repositorio para la configuracion de TaskFlow
mkdir ~/taskflow-config && cd ~/taskflow-config
git init

# 2. Crea un archivo de tareas inicial
echo '{"tareas": []}' > tareas.json
git add tareas.json
git commit -m "Inicializar TaskFlow"

# 3. Configura el Git MCP apuntando a este repo
# Ahora Claude puede versionar tus tareas automaticamente
```

**Checkpoint**:
> Antes de continuar, verifica que entiendes:
> - Por que separamos el acceso por directorios en Filesystem MCP?
> - Que ventaja tiene versionar la configuracion de TaskFlow?

### 1.3 Memory MCP

**Que hace**: Proporciona memoria persistente usando un **knowledge graph** (grafo de conocimiento).

**Analogia**: Imagina un mapa mental donde puedes crear "nodos" (entidades) y "flechas" (relaciones) entre ellos. Claude puede guardar informacion aqui y recuperarla en futuras conversaciones.

**Por que es poderoso para TaskFlow**:
- Recordar las preferencias del usuario ("prefiero tareas cortas por la manana")
- Almacenar contexto de proyectos ("el proyecto X tiene deadline el viernes")
- Crear relaciones entre tareas y personas

**Configuracion**:

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

| Tool | Funcion | Ejemplo |
|------|---------|---------|
| `create_entities` | Crear entidades | Crear nodo "Usuario: Juan" |
| `create_relations` | Crear relaciones | "Juan -> prefiere -> tareas matutinas" |
| `search_nodes` | Buscar en el grafo | Encontrar todas las preferencias de Juan |
| `read_graph` | Leer estado completo | Ver todo el conocimiento almacenado |
| `delete_entities` | Eliminar entidades | Borrar informacion obsoleta |

**Ejemplo conceptual**:

```
Entidades:
  - Usuario: Juan
  - Proyecto: Rediseno Web
  - Preferencia: Tareas Cortas

Relaciones:
  - Juan --trabaja_en--> Rediseno Web
  - Juan --prefiere--> Tareas Cortas
  - Rediseno Web --deadline--> 2024-02-15
```

### 1.4 Fetch MCP

**Que hace**: Obtiene contenido de URLs y lo convierte a formato optimizado para LLMs (generalmente Markdown limpio).

**Por que no usar un simple HTTP request?** El Fetch MCP:
1. Limpia el HTML eliminando scripts, estilos y elementos no relevantes
2. Extrae el contenido principal
3. Convierte a Markdown legible
4. Maneja errores y timeouts graciosamente

**Configuracion**:

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

| Tool | Funcion | Cuando usar |
|------|---------|-------------|
| `fetch` | Obtener URL como Markdown | Articulos, documentacion, blogs |
| `fetch_raw` | Obtener contenido sin procesar | APIs, JSON, datos estructurados |

**Caso de uso en TaskFlow**: Cuando creas una tarea con una URL de referencia, Claude puede extraer automaticamente el contenido relevante y adjuntarlo como contexto.

**Error Comun**:
> **Contenido vacio o incompleto**: Algunos sitios bloquean requests automatizados o usan mucho JavaScript para renderizar. El Fetch MCP funciona mejor con sitios estaticos o con buen HTML semantico.

**Checkpoint**:
> Pausa y reflexiona:
> - Como combinarias Filesystem + Git para un backup automatico de tareas?
> - Que informacion guardarias en Memory MCP vs en un archivo JSON?

---

## 2. AWS MCP Servers

**Tiempo estimado: 45 minutos**

### Por que AWS tiene MCPs oficiales

AWS es la plataforma cloud mas usada. Tener MCPs oficiales significa que puedes **gestionar tu infraestructura cloud conversando con Claude**, sin memorizar cientos de comandos CLI.

**Analogia**: Es como tener un asistente que conoce todos los comandos de AWS CLI y puede ejecutarlos por ti, pero siempre preguntando antes de hacer cambios.

### Catalogo de AWS MCPs

| Servidor | Funcion | Nivel de riesgo |
|----------|---------|-----------------|
| **AWS API** | Ejecutar cualquier comando AWS CLI | Alto (configurable) |
| **AWS Knowledge** | Documentacion y best practices | Solo lectura |
| **AWS CDK** | Guia de CDK y CloudFormation | Medio |
| **AWS Cost Analysis** | Analisis de costos | Solo lectura |
| **AWS Nova Canvas** | Generacion de imagenes con Nova | Bajo |

### 2.1 AWS API MCP

**Configuracion segura**:

```json
{
  "mcpServers": {
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "mi-perfil",
        "AWS_REGION": "eu-west-1",
        "READ_OPERATIONS_ONLY": "true",
        "ALLOWED_SERVICES": "s3,ec2,lambda"
      }
    }
  }
}
```

**Variables de entorno criticas**:

| Variable | Funcion | Recomendacion |
|----------|---------|---------------|
| `AWS_PROFILE` | Perfil de credenciales | Usa un perfil con permisos limitados |
| `AWS_REGION` | Region por defecto | Tu region principal |
| `READ_OPERATIONS_ONLY` | Limitar a solo lectura | **"true" para empezar** |
| `ALLOWED_SERVICES` | Servicios permitidos | Lista explicita de servicios |

**Error Comun**:
> **Permisos excesivos**: Nunca uses tu perfil de administrador. Crea un perfil IAM especifico con los permisos minimos necesarios. Si `READ_OPERATIONS_ONLY` esta en "false", Claude podria crear o eliminar recursos.

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `execute_aws_command` | Ejecutar comandos AWS CLI |
| `get_execution_plan` | Obtener plan paso a paso para tareas complejas |

**Ejemplos de uso**:

```
Usuario: "Lista todos los buckets de S3"
Claude ejecuta: aws s3 ls

Usuario: "Describe las instancias EC2 en produccion"
Claude ejecuta: aws ec2 describe-instances --filters "Name=tag:Environment,Values=production"

Usuario: "Cuantas funciones Lambda tengo?"
Claude ejecuta: aws lambda list-functions --query 'length(Functions)'
```

### 2.2 AWS Knowledge MCP (Servidor Remoto)

**Que es diferente**: Este MCP es **remoto** - se conecta a servidores de AWS, no ejecuta nada local.

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

**Que proporciona**:
- Documentacion oficial de AWS
- Best practices de arquitectura
- Guias de seguridad
- Ejemplos de codigo

**Caso de uso**: "Como debo configurar un bucket S3 para hosting estatico de forma segura?"

### 2.3 AWS CDK MCP

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

| Tool | Funcion |
|------|---------|
| `cdk_synth` | Sintetizar template CloudFormation |
| `cdk_diff` | Ver diferencias entre local y deployed |
| `cdk_deploy` | Desplegar stack |

### 2.4 AWS Cost Analysis MCP

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

**Para que sirve**:
- Analisis de costos por servicio
- Predicciones de gasto
- Recomendaciones de optimizacion
- Comparativas historicas

**Practica Guiada: Auditoria de costos**

```
Paso 1: Configura el AWS Cost Analysis MCP
Paso 2: Pregunta "Cual ha sido mi gasto en S3 los ultimos 3 meses?"
Paso 3: Pregunta "Que servicio me esta costando mas?"
Paso 4: Pregunta "Hay recursos que podria optimizar?"
```

**Checkpoint**:
> Antes de pasar a Cloudflare, verifica:
> - Sabes por que `READ_OPERATIONS_ONLY` deberia ser "true" inicialmente?
> - Entiendes la diferencia entre un MCP local (AWS API) y uno remoto (AWS Knowledge)?

---

## 3. Cloudflare MCP Servers

**Tiempo estimado: 30 minutos**

### Filosofia de Cloudflare MCPs

Cloudflare ofrece MCPs **remotos** para toda su plataforma. Esto significa:
- No necesitas instalar nada localmente
- La autenticacion se maneja via OAuth en el navegador
- Siempre tienes la version mas actualizada

### Catalogo de Servidores

| Servidor | URL | Funcion |
|----------|-----|---------|
| **Workers** | `workers.mcp.cloudflare.com` | Gestionar Cloudflare Workers |
| **KV** | `kv.mcp.cloudflare.com` | Key-Value storage |
| **R2** | `r2.mcp.cloudflare.com` | Object storage (S3-compatible) |
| **D1** | `d1.mcp.cloudflare.com` | Base de datos SQL serverless |
| **Observability** | `observability.mcp.cloudflare.com` | Analytics, logs, trazas |
| **Bindings** | `bindings.mcp.cloudflare.com` | Gestion de bindings |

### Configuracion General

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

### 3.1 Workers MCP

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `list_workers` | Listar Workers |
| `get_worker` | Obtener codigo de un Worker |
| `deploy_worker` | Desplegar Worker |
| `delete_worker` | Eliminar Worker |
| `get_worker_logs` | Ver logs |

### 3.2 R2 MCP (Object Storage)

**Analogia**: R2 es como S3 de AWS, pero sin costos de egress (transferencia de salida). Perfecto para almacenar archivos de TaskFlow.

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `list_buckets` | Listar buckets |
| `list_objects` | Listar objetos en bucket |
| `get_object` | Obtener objeto |
| `put_object` | Subir objeto |
| `delete_object` | Eliminar objeto |

**Caso de uso en TaskFlow**: Almacenar adjuntos de tareas (documentos, imagenes) en R2.

### 3.3 D1 MCP (SQL Database)

**Que es D1**: Base de datos SQL serverless basada en SQLite, distribuida globalmente.

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `list_databases` | Listar bases de datos |
| `execute_sql` | Ejecutar consulta SQL |
| `get_schema` | Obtener schema |

**Ejemplo de uso para TaskFlow**:

```sql
-- Crear tabla de tareas en D1
CREATE TABLE tareas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT,
  estado TEXT DEFAULT 'pendiente',
  prioridad INTEGER DEFAULT 3,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_limite DATETIME
);

-- Insertar tarea
INSERT INTO tareas (titulo, descripcion, prioridad)
VALUES ('Revisar MCP', 'Completar modulo 4 del curso', 1);

-- Consultar tareas pendientes
SELECT * FROM tareas WHERE estado = 'pendiente' ORDER BY prioridad;
```

---

## 4. Firebase MCP

**Tiempo estimado: 30 minutos**

### Por que Firebase para TaskFlow

Firebase ofrece un **backend completo sin servidor**:
- Autenticacion de usuarios
- Base de datos en tiempo real (Firestore)
- Almacenamiento de archivos
- Hosting

**Caso ideal**: Quieres que TaskFlow sea multi-usuario y sincronice entre dispositivos.

### Configuracion

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

**Practica Guiada: Configuracion de Firebase**

```
Paso 1: Ve a https://console.firebase.google.com/
Paso 2: Selecciona tu proyecto (o crea uno nuevo)
Paso 3: Settings (engranaje) -> Service Accounts
Paso 4: Click en "Generate New Private Key"
Paso 5: Guarda el archivo JSON en ubicacion segura
Paso 6: Actualiza SERVICE_ACCOUNT_KEY_PATH en tu configuracion
```

**Error Comun**:
> **Service Account Key en repositorio**: NUNCA commits el archivo `serviceAccountKey.json`. Anadelo a `.gitignore` inmediatamente.

### Tools Disponibles

#### Authentication

| Tool | Funcion | Ejemplo |
|------|---------|---------|
| `auth_get_user` | Obtener usuario por UID | Verificar si existe usuario |
| `auth_get_user_by_email` | Obtener usuario por email | Buscar usuario especifico |
| `auth_list_users` | Listar usuarios | Ver todos los usuarios |
| `auth_create_user` | Crear usuario | Registrar nuevo usuario |
| `auth_update_user` | Actualizar usuario | Cambiar email o datos |
| `auth_delete_user` | Eliminar usuario | Dar de baja usuario |

#### Firestore

| Tool | Funcion | Ejemplo |
|------|---------|---------|
| `firestore_add_document` | Crear documento | Crear nueva tarea |
| `firestore_get_document` | Obtener documento | Leer tarea especifica |
| `firestore_update_document` | Actualizar documento | Marcar tarea completada |
| `firestore_delete_document` | Eliminar documento | Borrar tarea |
| `firestore_query` | Consultar coleccion | Buscar tareas por estado |
| `firestore_list_collections` | Listar colecciones | Ver estructura de datos |

#### Storage

| Tool | Funcion | Ejemplo |
|------|---------|---------|
| `storage_list_files` | Listar archivos | Ver adjuntos de tareas |
| `storage_upload` | Subir archivo | Adjuntar documento |
| `storage_download` | Descargar archivo | Obtener adjunto |
| `storage_delete` | Eliminar archivo | Borrar adjunto |
| `storage_get_metadata` | Obtener metadata | Ver tamano y tipo |

### Ejemplo Completo para TaskFlow

```
Usuario: "Crea un usuario para pruebas"
Claude: auth_create_user(email="test@taskflow.com", password="...")

Usuario: "Guarda una tarea en Firestore"
Claude: firestore_add_document(
  collection="tareas",
  data={
    titulo: "Completar modulo MCP",
    estado: "pendiente",
    prioridad: "alta",
    asignado_a: "test@taskflow.com"
  }
)

Usuario: "Busca tareas de alta prioridad"
Claude: firestore_query(
  collection="tareas",
  where=[["prioridad", "==", "alta"]]
)
```

---

## 5. GitHub MCP

**Tiempo estimado: 30 minutos**

### Por que GitHub MCP es esencial

Si desarrollas software, GitHub es probablemente donde vive tu codigo. Con el GitHub MCP puedes:
- Gestionar issues y PRs sin salir de Claude
- Automatizar revisiones de codigo
- Crear workflows de desarrollo integrados

### Configuracion

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

**Practica Guiada: Crear token de GitHub**

```
Paso 1: Ve a https://github.com/settings/tokens
Paso 2: "Generate new token" -> "Fine-grained tokens" (recomendado)
Paso 3: Nombre descriptivo: "MCP-Claude-TaskFlow"
Paso 4: Selecciona repositorios: Solo los necesarios
Paso 5: Permisos recomendados:
        - Contents: Read and write
        - Issues: Read and write
        - Pull requests: Read and write
        - Metadata: Read
Paso 6: Generate y copia el token
Paso 7: Guardalo en tu gestor de contrasenas
```

**Error Comun**:
> **Token con permisos excesivos**: No uses tokens con acceso a todos tus repositorios si solo necesitas acceso a uno. Los fine-grained tokens permiten control granular.

### Tools Disponibles

#### Repositorios

| Tool | Funcion |
|------|---------|
| `search_repositories` | Buscar repositorios |
| `get_file_contents` | Leer archivo del repo |
| `create_or_update_file` | Crear/actualizar archivo |
| `push_files` | Push multiples archivos |
| `list_commits` | Listar commits |
| `get_commit` | Detalle de commit |

#### Issues

| Tool | Funcion |
|------|---------|
| `list_issues` | Listar issues |
| `get_issue` | Obtener issue |
| `create_issue` | Crear issue |
| `update_issue` | Actualizar issue |
| `add_issue_comment` | Anadir comentario |

#### Pull Requests

| Tool | Funcion |
|------|---------|
| `list_pull_requests` | Listar PRs |
| `get_pull_request` | Obtener PR |
| `create_pull_request` | Crear PR |
| `create_pull_request_review` | Crear review |
| `merge_pull_request` | Mergear PR |
| `get_pull_request_files` | Archivos del PR |
| `get_pull_request_diff` | Diff del PR |

#### Branches

| Tool | Funcion |
|------|---------|
| `create_branch` | Crear branch |
| `list_branches` | Listar branches |

### Ejemplo de Workflow con TaskFlow

```
Usuario: "Crea un issue sobre el bug de login en taskflow-app"
Claude: create_issue(
  repo="mi-org/taskflow-app",
  title="Bug: Login no valida email correctamente",
  body="## Descripcion\nEl formulario acepta emails invalidos...\n\n## Pasos para reproducir\n1. ...",
  labels=["bug", "priority-high"]
)

Usuario: "Lista los PRs abiertos"
Claude: list_pull_requests(repo="mi-org/taskflow-app", state="open")

Usuario: "Crea un PR desde fix/login-validation a main"
Claude: create_pull_request(
  repo="mi-org/taskflow-app",
  title="Fix: Validacion de email en login",
  head="fix/login-validation",
  base="main",
  body="## Cambios\n- Agregada validacion de formato email\n- Tests unitarios\n\nCloses #42"
)
```

**Checkpoint**:
> Verifica que entiendes:
> - Por que usar fine-grained tokens en lugar de classic tokens?
> - Como conectarias un issue de GitHub con una tarea en TaskFlow?

---

## 6. Bases de Datos

**Tiempo estimado: 45 minutos**

### Panorama de opciones

| Tipo | MCP | Caso de uso |
|------|-----|-------------|
| **SQL Relacional** | PostgreSQL, MySQL, SQLite | Datos estructurados, relaciones complejas |
| **NoSQL Documentos** | MongoDB, Firebase | Datos flexibles, esquema dinamico |
| **Key-Value** | Redis, Cloudflare KV | Cache, sesiones, datos rapidos |

### 6.1 PostgreSQL MCP

**Cuando usar PostgreSQL**: Datos estructurados, necesitas transacciones ACID, consultas complejas con JOINs.

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://usuario:password@localhost:5432/taskflow"
      }
    }
  }
}
```

**Tools disponibles**:

| Tool | Funcion | Uso |
|------|---------|-----|
| `query` | Ejecutar SELECT | Consultas de lectura |
| `execute` | INSERT, UPDATE, DELETE | Modificaciones |
| `describe_table` | Estructura de tabla | Documentacion |
| `list_tables` | Listar tablas | Exploracion |

**Resources disponibles**:
- `schema://tables` - Lista de todas las tablas
- `schema://table/{nombre}` - Schema detallado de una tabla

**Error Comun**:
> **Credenciales en texto plano**: Usa variables de entorno del sistema operativo en lugar de escribir la password en el archivo de configuracion. Ejemplo: `DATABASE_URL` deberia venir de `$env:DATABASE_URL` o similar.

### 6.2 MySQL MCP

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@benborber/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "taskflow_user",
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "taskflow"
      }
    }
  }
}
```

### 6.3 MongoDB MCP

**Cuando usar MongoDB**: Datos con estructura variable, documentos anidados, escalabilidad horizontal.

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mcp-mongo-server"],
      "env": {
        "MONGODB_URI": "mongodb://localhost:27017/taskflow"
      }
    }
  }
}
```

**Tools disponibles**:

| Tool | Funcion | Ejemplo |
|------|---------|---------|
| `find` | Buscar documentos | Encontrar tareas por estado |
| `insertOne` | Insertar documento | Crear tarea |
| `updateOne` | Actualizar documento | Modificar tarea |
| `deleteOne` | Eliminar documento | Borrar tarea |
| `aggregate` | Pipeline de agregacion | Estadisticas de tareas |

### 6.4 SQLite MCP

**Cuando usar SQLite**: Desarrollo local, aplicaciones embebidas, prototipado rapido.

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/taskflow.db"]
    }
  }
}
```

**Ventaja**: No necesitas servidor de base de datos. El archivo `.db` es toda tu base de datos.

### 6.5 Redis MCP

**Cuando usar Redis**: Cache de datos frecuentes, sesiones de usuario, colas de tareas, datos temporales.

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

### Practica Guiada: Disenar schema para TaskFlow

```sql
-- PostgreSQL schema para TaskFlow

-- Usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  nombre VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Proyectos
CREATE TABLE proyectos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  descripcion TEXT,
  owner_id INTEGER REFERENCES usuarios(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tareas
CREATE TABLE tareas (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  descripcion TEXT,
  estado VARCHAR(20) DEFAULT 'pendiente',
  prioridad INTEGER DEFAULT 3 CHECK (prioridad BETWEEN 1 AND 5),
  proyecto_id INTEGER REFERENCES proyectos(id),
  asignado_a INTEGER REFERENCES usuarios(id),
  fecha_limite TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Etiquetas
CREATE TABLE etiquetas (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  color VARCHAR(7) -- hex color
);

-- Relacion tareas-etiquetas
CREATE TABLE tarea_etiquetas (
  tarea_id INTEGER REFERENCES tareas(id),
  etiqueta_id INTEGER REFERENCES etiquetas(id),
  PRIMARY KEY (tarea_id, etiqueta_id)
);
```

---

## 7. Otros MCPs Populares

**Tiempo estimado: 30 minutos**

### 7.1 Comunicacion y Productividad

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

**Caso de uso en TaskFlow**: Notificar al canal del equipo cuando una tarea de alta prioridad se completa o vence.

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

**Que es Linear**: Herramienta de gestion de proyectos para equipos de desarrollo. Alternativa moderna a Jira.

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

**Caso de uso**: Sincronizar tareas de TaskFlow con paginas de Notion para documentacion.

### 7.2 DevOps

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

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `list_containers` | Listar contenedores |
| `start_container` | Iniciar contenedor |
| `stop_container` | Parar contenedor |
| `container_logs` | Ver logs |
| `build_image` | Construir imagen |

**Caso de uso**: Gestionar contenedores de desarrollo de TaskFlow.

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

### 7.3 Monitoring

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

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `list_issues` | Listar errores |
| `get_issue` | Detalles de error |
| `resolve_issue` | Marcar como resuelto |
| `get_event` | Obtener evento especifico |

**Caso de uso**: Crear tareas en TaskFlow automaticamente a partir de errores en Sentry.

### 7.4 Browser Automation

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

**Tools disponibles**:

| Tool | Funcion |
|------|---------|
| `navigate` | Navegar a URL |
| `screenshot` | Captura de pantalla |
| `click` | Hacer click en elemento |
| `type` | Escribir texto |
| `evaluate` | Ejecutar JavaScript |

### Tabla Resumen de MCPs

| Categoria | MCPs disponibles | Uso principal |
|-----------|------------------|---------------|
| **Cloud** | AWS API, AWS CDK, Cloudflare Workers/R2/D1/KV | Infraestructura |
| **Bases de datos** | PostgreSQL, MySQL, MongoDB, SQLite, Redis | Persistencia |
| **Desarrollo** | GitHub, Git, Filesystem | Codigo y archivos |
| **Comunicacion** | Slack, Linear, Notion | Colaboracion |
| **DevOps** | Docker, Kubernetes, Sentry | Operaciones |
| **Web** | Fetch, Puppeteer, Brave Search | Navegacion |
| **AI** | Memory, Sequential Thinking | Capacidades IA |

---

## 8. Troubleshooting

**Tiempo estimado: 15 minutos**

### Problemas Comunes y Soluciones

#### Problema: "MCP no aparece en la lista"

**Sintomas**: Despues de configurar, el comando `/mcp` no muestra el servidor.

**Soluciones**:
1. Verificar sintaxis JSON (usa un validador online)
2. Reiniciar Claude Desktop completamente
3. Verificar que el package npm existe: `npx -y @package/name --help`
4. Revisar logs de Claude Desktop

```bash
# Verificar que el package existe
npx -y @modelcontextprotocol/server-filesystem --help
```

#### Problema: "Error de autenticacion"

**Sintomas**: El MCP se conecta pero las operaciones fallan con errores de permisos.

**Soluciones**:
1. Verificar que el token/key es correcto
2. Comprobar que el token tiene los permisos necesarios
3. Verificar que el token no ha expirado
4. Para AWS: verificar `aws sts get-caller-identity`

#### Problema: "Timeout al conectar"

**Sintomas**: El MCP tarda mucho o nunca responde.

**Soluciones**:
1. Verificar conectividad de red
2. Para MCPs remotos: comprobar que la URL es correcta
3. Verificar firewalls o proxies corporativos
4. Intentar con VPN desactivada (o activada si estas en red corporativa)

#### Problema: "El MCP no tiene permisos para acceder al archivo/directorio"

**Sintomas**: Filesystem MCP rechaza operaciones.

**Soluciones**:
1. Verificar que el path esta en la lista de argumentos
2. Usar paths absolutos, no relativos
3. Verificar permisos del sistema operativo
4. En Windows: verificar que no hay caracteres especiales en el path

#### Problema: "Base de datos: conexion rechazada"

**Sintomas**: PostgreSQL/MySQL MCP no conecta.

**Soluciones**:
1. Verificar que el servidor de BD esta corriendo
2. Comprobar host, puerto, usuario, password
3. Verificar que el usuario tiene permisos de conexion remota
4. Revisar firewall del servidor de BD

```bash
# Probar conexion manualmente
psql "postgresql://usuario:password@localhost:5432/taskflow"
# o
mysql -u usuario -p -h localhost taskflow
```

### Comandos de Diagnostico

```bash
# Verificar MCPs configurados
claude /mcp

# Ver logs detallados (ubicacion depende del OS)
# macOS: ~/Library/Logs/Claude/
# Windows: %APPDATA%\Claude\logs\
# Linux: ~/.config/Claude/logs/

# Probar MCP manualmente
npx -y @modelcontextprotocol/server-filesystem /tmp

# Verificar credenciales AWS
aws sts get-caller-identity

# Verificar token de GitHub
curl -H "Authorization: token ghp_xxx" https://api.github.com/user
```

---

## 9. Ejercicios Practicos

### Ejercicio 1: Configurar MCPs Basicos

**Nivel**: Principiante
**Tiempo**: 20 minutos

**Objetivo**: Configurar y verificar los MCPs fundamentales.

**Tareas**:
1. Configura el MCP de Filesystem con acceso a una carpeta de pruebas
2. Configura el MCP de Git apuntando a un repositorio local
3. Verifica que ambos funcionan con `/mcp`

**Criterios de exito**:
- [ ] Filesystem MCP puede listar archivos en el directorio configurado
- [ ] Git MCP puede mostrar el estado del repositorio
- [ ] No hay errores en los logs

---

### Ejercicio 2: Trabajar con GitHub MCP

**Nivel**: Principiante
**Tiempo**: 25 minutos

**Objetivo**: Gestionar issues y PRs desde Claude.

**Tareas**:
```bash
# 1. Configurar GitHub MCP
# (asegurate de tener un token con los permisos correctos)

# 2. Probar estas operaciones:
claude "Lista los issues abiertos de mi repositorio principal"
claude "Crea un issue de prueba con titulo 'Test desde MCP'"
claude "Cierra el issue de prueba que acabamos de crear"
```

**Criterios de exito**:
- [ ] Puedes listar issues existentes
- [ ] Puedes crear un nuevo issue
- [ ] Puedes cerrar/actualizar issues

---

### Ejercicio 3: Base de Datos + TaskFlow

**Nivel**: Intermedio
**Tiempo**: 40 minutos

**Objetivo**: Conectar TaskFlow a una base de datos real.

**Tareas**:
1. Configura PostgreSQL MCP (o SQLite si no tienes PostgreSQL)
2. Crea el schema de TaskFlow (tablas usuarios, proyectos, tareas)
3. Pide a Claude que describa el schema
4. Inserta datos de prueba
5. Ejecuta consultas para filtrar tareas

**Criterios de exito**:
- [ ] Schema creado correctamente
- [ ] Datos insertados sin errores
- [ ] Consultas devuelven resultados esperados

---

### Ejercicio 4: AWS MCP en Modo Seguro

**Nivel**: Intermedio
**Tiempo**: 30 minutos

**Objetivo**: Explorar recursos AWS de forma segura.

**Tareas**:
1. Configura AWS API MCP con `READ_OPERATIONS_ONLY=true`
2. Lista buckets de S3
3. Describe instancias EC2 (si tienes)
4. Consulta el costo del ultimo mes con AWS Cost Analysis MCP

**Criterios de exito**:
- [ ] MCP configurado en modo solo lectura
- [ ] Puedes listar recursos sin errores
- [ ] Ninguna operacion de escritura es posible

---

### Ejercicio 5: Combinar Multiples MCPs

**Nivel**: Avanzado
**Tiempo**: 45 minutos

**Objetivo**: Crear un flujo de trabajo que use varios MCPs.

**Escenario**: Automatizar la creacion de tareas a partir de errores.

**Tareas**:
```bash
claude "Analiza los errores de Sentry de las ultimas 24 horas,
busca el codigo relacionado en GitHub, y crea un issue
con la propuesta de fix. Guarda un resumen en un archivo local."
```

**MCPs necesarios**: Sentry, GitHub, Filesystem

**Criterios de exito**:
- [ ] Errores recuperados de Sentry
- [ ] Codigo localizado en GitHub
- [ ] Issue creado con informacion relevante
- [ ] Archivo de resumen guardado localmente

---

### Ejercicio 6: Workflow Completo de TaskFlow

**Nivel**: Avanzado
**Tiempo**: 60 minutos

**Objetivo**: Implementar un workflow completo de gestion de tareas.

**Escenario**: Un usuario quiere:
1. Crear una tarea con descripcion enriquecida desde una URL
2. Guardarla en la base de datos
3. Notificar al equipo en Slack
4. Versionar el cambio en Git

**MCPs necesarios**: Fetch, PostgreSQL/Firebase, Slack, Git

**Tareas**:
```bash
# Paso 1: Enriquecer tarea
claude "Crea una tarea sobre este articulo: [URL].
        Extrae los puntos principales y agregalos a la descripcion."

# Paso 2: Persistir
claude "Guarda esta tarea en la base de datos con prioridad alta"

# Paso 3: Notificar
claude "Envia un mensaje al canal #tareas con el resumen de la nueva tarea"

# Paso 4: Versionar
claude "Crea un commit con los cambios de configuracion"
```

**Criterios de exito**:
- [ ] Tarea creada con contenido extraido de la URL
- [ ] Tarea guardada en base de datos
- [ ] Mensaje enviado a Slack
- [ ] Commit creado en el repositorio

---

## 10. Resumen y Proximos Pasos

### Lo que aprendimos en este modulo

**MCPs de Referencia de Anthropic**:
- Filesystem: Acceso seguro a archivos con sandboxing por directorio
- Git: Operaciones de versionado integradas
- Memory: Persistencia de conocimiento entre sesiones
- Fetch: Extraccion inteligente de contenido web

**MCPs de Cloud**:
- AWS: Suite completa con modos de seguridad configurables
- Cloudflare: MCPs remotos para Workers, D1, R2, KV

**MCPs de Datos**:
- Firebase: Backend completo (auth + firestore + storage)
- GitHub: Gestion de codigo y colaboracion
- Bases de datos: PostgreSQL, MySQL, MongoDB, SQLite, Redis

**MCPs de Productividad**:
- Slack, Linear, Notion para comunicacion
- Docker, Kubernetes para DevOps
- Sentry para monitoring
- Puppeteer para automatizacion web

### Checklist de competencias

Antes de pasar al siguiente modulo, verifica que puedes:

- [ ] Configurar al menos 3 MCPs diferentes sin errores
- [ ] Combinar MCPs para flujos de trabajo multi-paso
- [ ] Diagnosticar problemas comunes de configuracion
- [ ] Aplicar principios de seguridad (tokens limitados, modo solo lectura)
- [ ] Disenar como expandir TaskFlow con MCPs oficiales

### Preparacion para el Modulo 5

En el **Modulo 5: Desarrollo de MCPs Propios** aprenderemos a:

- Entender la arquitectura interna de un MCP Server
- Crear MCPs personalizados en Python y TypeScript
- Usar FastMCP para desarrollo rapido
- Testear y debuggear MCPs
- Publicar MCPs para que otros los usen

**Tarea previa recomendada**:
1. Revisa la documentacion oficial de MCP: https://modelcontextprotocol.io
2. Ten preparado un entorno de desarrollo Python o Node.js
3. Piensa en una integracion que te gustaria crear para TaskFlow

---

## Recursos Adicionales

### Documentacion Oficial

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers) - Servidores oficiales de Anthropic
- [AWS MCP Servers](https://github.com/awslabs/mcp) - Suite de AWS
- [Cloudflare MCP Docs](https://developers.cloudflare.com/workers/ai/mcp/) - Documentacion de Cloudflare

### Comunidad

- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers) - Lista curada de MCPs
- [MCP Discord](https://discord.gg/mcp) - Comunidad de desarrolladores

### Seguridad

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub Token Security](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

**Fin del Modulo 4**

Continua con el [Modulo 5: Desarrollo de MCPs Propios](#) cuando estes listo para crear tus propias integraciones.
