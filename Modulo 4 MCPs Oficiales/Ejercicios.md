# Ejercicios: Módulo 4 - MCPs Oficiales

## Información

| | |
|---|---|
| **Dificultad progresiva** | Básico → Intermedio → Avanzado |
| **Tiempo total estimado** | 4-5 horas |
| **Requisitos** | Claude Desktop/CLI, cuentas en servicios (opcional) |

---

## Ejercicio 1: Filesystem MCP - Gestión de archivos

**Nivel**: Básico
**Tiempo**: 25 minutos

### Objetivo
Dominar las operaciones básicas de archivos con el Filesystem MCP.

### Instrucciones

1. Configura Filesystem MCP con acceso a una carpeta de pruebas
2. Realiza las operaciones indicadas
3. Verifica los resultados

### Configuración

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/mcp-ejercicios"]
    }
  }
}
```

### Tareas

```bash
claude

# 1. Crear estructura de proyecto
> Crea esta estructura de carpetas:
> /tmp/mcp-ejercicios/
> ├── src/
> │   ├── components/
> │   └── utils/
> ├── tests/
> └── docs/

# 2. Crear archivo README
> Crea un README.md con información básica del proyecto

# 3. Crear múltiples archivos
> Crea archivos index.ts vacíos en src/, src/components/ y src/utils/

# 4. Buscar archivos
> Encuentra todos los archivos .ts en el proyecto

# 5. Leer y modificar
> Lee el README.md y añade una sección de instalación
```

### Criterios de éxito
- [ ] Estructura creada correctamente
- [ ] Archivos creados en las ubicaciones correctas
- [ ] Búsqueda retorna resultados esperados

---

## Ejercicio 2: Git MCP - Control de versiones

**Nivel**: Básico
**Tiempo**: 30 minutos

### Objetivo
Gestionar un repositorio Git usando el MCP.

### Instrucciones

1. Inicializa un repositorio de prueba
2. Realiza operaciones Git básicas
3. Practica el flujo de trabajo típico

### Preparación

```bash
# Crear repo de prueba
mkdir /tmp/git-ejercicio && cd /tmp/git-ejercicio
git init
echo "# Test" > README.md
git add . && git commit -m "Initial commit"
```

### Configuración

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/tmp/git-ejercicio"]
    }
  }
}
```

### Tareas

```bash
claude

# 1. Ver estado
> ¿Cuál es el estado actual del repositorio?

# 2. Ver historial
> Muestra los últimos 5 commits

# 3. Crear branch
> Crea una nueva rama llamada "feature/nueva-funcionalidad"

# 4. Modificar y commitear
> Añade una línea al README y crea un commit

# 5. Ver diferencias
> Muestra las diferencias entre main y la nueva rama
```

### Criterios de éxito
- [ ] Puedes ver estado y log
- [ ] Branches creados correctamente
- [ ] Commits realizados con mensajes apropiados

---

## Ejercicio 3: GitHub MCP - Gestión de Issues

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Gestionar issues y PRs de GitHub desde Claude.

### Preparación

1. Crea un repositorio de prueba en GitHub
2. Genera un token con permisos de issues y PRs
3. Configura el MCP

### Configuración

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxx"
      }
    }
  }
}
```

### Tareas

```bash
claude

# 1. Listar issues
> Lista los issues abiertos de mi repositorio [tu-usuario/tu-repo]

# 2. Crear issue
> Crea un issue con:
> Título: "Bug: Error en validación de formulario"
> Descripción: "El formulario no valida emails correctamente"
> Labels: bug, priority-high

# 3. Añadir comentario
> Añade un comentario al issue: "Investigando el problema..."

# 4. Cerrar issue
> Cierra el issue con el comentario "Resuelto en PR #X"

# 5. Crear PR
> Crea una PR desde feature-branch a main con descripción detallada
```

### Criterios de éxito
- [ ] Issues creados con labels correctos
- [ ] Comentarios añadidos
- [ ] PRs creadas correctamente

---

## Ejercicio 4: Base de datos con PostgreSQL MCP

**Nivel**: Intermedio
**Tiempo**: 45 minutos

### Objetivo
Interactuar con una base de datos PostgreSQL a través del MCP.

### Preparación

```bash
# Si usas Docker
docker run --name postgres-ejercicio \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15
```

### Configuración

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://postgres:password@localhost:5432/postgres"
      }
    }
  }
}
```

### Tareas

```bash
claude

# 1. Crear tabla
> Crea una tabla "usuarios" con: id, nombre, email, created_at

# 2. Insertar datos
> Inserta 5 usuarios de ejemplo

# 3. Consultar
> Lista todos los usuarios ordenados por nombre

# 4. Actualizar
> Actualiza el email del usuario con id=1

# 5. Crear tabla relacionada
> Crea una tabla "tareas" relacionada con usuarios

# 6. JOIN
> Muestra todas las tareas con el nombre del usuario asignado
```

### Criterios de éxito
- [ ] Tablas creadas correctamente
- [ ] CRUD funcionando
- [ ] JOINs ejecutados correctamente

---

## Ejercicio 5: Supabase MCP - Backend completo

**Nivel**: Intermedio
**Tiempo**: 50 minutos

### Objetivo
Usar Supabase como backend completo para una aplicación.

### Preparación

1. Crea un proyecto en [Supabase](https://supabase.com)
2. Obtén las credenciales del proyecto
3. Configura el MCP

### Configuración

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.supabase.com/mcp"]
    }
  }
}
```

### Tareas

```bash
claude

# 1. Crear schema
> Crea las tablas para un blog:
> - posts (id, title, content, author_id, created_at, published)
> - authors (id, name, bio, avatar_url)
> - comments (id, post_id, author_name, content, created_at)

# 2. Insertar datos
> Inserta 3 autores y 5 posts de ejemplo

# 3. Queries complejas
> Muestra los posts publicados con su autor, ordenados por fecha

# 4. Actualizar
> Publica todos los posts en borrador

# 5. Estadísticas
> ¿Cuántos posts tiene cada autor?
```

### Criterios de éxito
- [ ] Schema creado con relaciones
- [ ] Datos insertados correctamente
- [ ] Queries complejas funcionando

---

## Ejercicio 6: AWS MCP - Infraestructura cloud

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Explorar recursos AWS de forma segura.

### Configuración (Solo lectura)

```json
{
  "mcpServers": {
    "aws-api": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "eu-west-1",
        "READ_OPERATIONS_ONLY": "true",
        "ALLOWED_SERVICES": "s3,ec2,lambda"
      }
    }
  }
}
```

### Tareas

```bash
claude

# 1. Listar recursos
> Lista todos los buckets de S3
> Lista las instancias EC2 activas
> Lista las funciones Lambda

# 2. Describir
> Describe el bucket [nombre-bucket] con sus políticas
> Muestra los detalles de la instancia [id]

# 3. Análisis
> ¿Hay instancias EC2 que podrían reducirse de tamaño?
> ¿Qué buckets de S3 no tienen versionado activado?
```

### Criterios de éxito
- [ ] Recursos listados correctamente
- [ ] Modo solo lectura verificado
- [ ] Análisis útiles generados

---

## Ejercicio 7: Cloudflare D1 + R2

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Usar servicios serverless de Cloudflare.

### Configuración

```json
{
  "mcpServers": {
    "cloudflare-d1": {
      "command": "npx",
      "args": ["mcp-remote", "https://d1.mcp.cloudflare.com/mcp"]
    },
    "cloudflare-r2": {
      "command": "npx",
      "args": ["mcp-remote", "https://r2.mcp.cloudflare.com/mcp"]
    }
  }
}
```

### Tareas

```bash
claude

# D1 - Base de datos
# 1. Crear tabla
> Crea una tabla "productos" con id, nombre, precio, stock

# 2. Insertar datos
> Inserta 10 productos de ejemplo

# 3. Consultar
> Muestra productos con stock bajo (< 5 unidades)

# R2 - Storage
# 4. Listar buckets
> Lista los buckets disponibles

# 5. Subir archivo
> Sube un archivo JSON con el catálogo de productos
```

### Criterios de éxito
- [ ] D1 funcionando con SQL
- [ ] R2 gestionando archivos
- [ ] Operaciones completadas sin errores

---

## Ejercicio 8: Vercel MCP - Deployments

**Nivel**: Avanzado
**Tiempo**: 40 minutos

### Objetivo
Gestionar proyectos y deployments en Vercel.

### Configuración

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["-y", "@vercel/mcp"],
      "env": {
        "VERCEL_TOKEN": "tu-token"
      }
    }
  }
}
```

### Tareas

```bash
claude

# 1. Listar proyectos
> Lista todos mis proyectos de Vercel

# 2. Ver deployments
> Muestra los últimos 5 deployments del proyecto [nombre]

# 3. Estado del deployment
> ¿Cuál es el estado del último deployment?
> ¿Hubo algún error?

# 4. Variables de entorno
> Lista las variables de entorno del proyecto
> Añade una variable DATABASE_URL para producción

# 5. Dominios
> Lista los dominios configurados
> ¿El certificado SSL está activo?
```

### Criterios de éxito
- [ ] Proyectos listados
- [ ] Deployments monitoreados
- [ ] Variables de entorno gestionadas

---

## Ejercicio 9: Workflow multi-MCP

**Nivel**: Avanzado
**Tiempo**: 55 minutos

### Objetivo
Crear un workflow que combine múltiples MCPs.

### Escenario

Automatizar el proceso de:
1. Detectar cambios en el código
2. Crear un registro en la base de datos
3. Notificar en Slack (o crear issue en GitHub)

### Configuración

```json
{
  "mcpServers": {
    "git": { ... },
    "postgres": { ... },
    "github": { ... }
  }
}
```

### Workflow

```bash
claude

# Paso 1: Detectar cambios
> Muestra los archivos modificados en los últimos commits

# Paso 2: Analizar cambios
> Para cada archivo modificado, describe brevemente el cambio

# Paso 3: Registrar en BD
> Inserta un registro en la tabla "changelog" con:
> - fecha
> - archivos modificados
> - resumen de cambios
> - autor del commit

# Paso 4: Crear issue de seguimiento
> Crea un issue en GitHub resumiendo los cambios
> de esta semana para revisión del equipo
```

### Criterios de éxito
- [ ] Workflow completo ejecutado
- [ ] Datos registrados en BD
- [ ] Issue creado correctamente

---

## Ejercicio 10: Proyecto final - Sistema de monitoreo

**Nivel**: Avanzado
**Tiempo**: 75 minutos

### Objetivo
Construir un sistema de monitoreo que use múltiples MCPs.

### Arquitectura

```
┌────────────────────────────────────────────────────────┐
│                     MONITOR                             │
├────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│   │   Git   │  │ GitHub  │  │   AWS   │  │ Vercel  │  │
│   │   MCP   │  │   MCP   │  │   MCP   │  │   MCP   │  │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │
│        │            │            │            │        │
│        v            v            v            v        │
│   ┌────────────────────────────────────────────────┐   │
│   │              PostgreSQL / Supabase              │   │
│   │              (Registro de eventos)              │   │
│   └────────────────────────────────────────────────┘   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Tareas

```bash
claude

# 1. Setup de BD
> Crea las tablas para el sistema de monitoreo:
> - eventos (id, tipo, source, mensaje, timestamp)
> - alertas (id, evento_id, severidad, resuelto)
> - metricas (id, servicio, metrica, valor, timestamp)

# 2. Recopilar estado
> Obtén el estado actual de:
> - Último commit del repo
> - Issues abiertos en GitHub
> - Estado de instancias EC2
> - Último deployment en Vercel

# 3. Registrar eventos
> Guarda cada estado como un evento en la BD

# 4. Detectar anomalías
> ¿Hay algo inusual en los datos recopilados?
> Crea alertas si es necesario

# 5. Generar reporte
> Genera un reporte de estado en Markdown
```

### Criterios de éxito
- [ ] Sistema configurado con múltiples MCPs
- [ ] Datos recopilados de todos los servicios
- [ ] Eventos registrados en BD
- [ ] Reporte generado correctamente

---

## Recursos adicionales

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Supabase MCP Docs](https://supabase.com/docs/guides/getting-started/mcp)
- [Vercel MCP Docs](https://vercel.com/docs/mcp)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
