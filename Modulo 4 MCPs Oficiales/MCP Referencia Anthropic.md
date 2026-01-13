# MCPs de Referencia (Anthropic)

**⏱️ Tiempo estimado: 60 minutos**

Los MCPs de Anthropic son la **referencia oficial** del protocolo. Están mantenidos por los creadores de MCP y representan las mejores prácticas.

---

## Catálogo de Servidores Oficiales

| MCP Server | Función | Package npm |
|------------|---------|-------------|
| **Filesystem** | Operaciones de archivos seguras | `@modelcontextprotocol/server-filesystem` |
| **Git** | Operaciones con repositorios | `@modelcontextprotocol/server-git` |
| **Memory** | Memoria persistente (knowledge graph) | `@modelcontextprotocol/server-memory` |
| **Fetch** | Obtener contenido web | `@modelcontextprotocol/server-fetch` |
| **Sequential Thinking** | Razonamiento paso a paso | `@modelcontextprotocol/server-sequential-thinking` |
| **Puppeteer** | Automatización de browser | `@modelcontextprotocol/server-puppeteer` |
| **Brave Search** | Búsqueda web | `@modelcontextprotocol/server-brave-search` |
| **Slack** | Integración Slack | `@modelcontextprotocol/server-slack` |

---

## 1. Filesystem MCP

Permite a Claude leer, escribir y gestionar archivos de forma **segura y controlada**.

### Configuración

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

> **Seguridad**: Los directorios en los argumentos son los **únicos** a los que Claude tendrá acceso.

### Tools disponibles

| Tool | Función | Ejemplo |
|------|---------|---------|
| `read_file` | Leer un archivo | Cargar configuración |
| `read_multiple_files` | Leer varios archivos | Importar listas |
| `write_file` | Escribir archivo | Exportar datos |
| `create_directory` | Crear directorio | Crear carpeta backups |
| `list_directory` | Listar contenido | Ver archivos |
| `move_file` | Mover/renombrar | Organizar archivos |
| `search_files` | Buscar archivos | Encontrar .json |
| `get_file_info` | Info del archivo | Ver metadata |

---

## 2. Git MCP

Ejecuta operaciones Git directamente desde Claude.

### Configuración

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

### Tools disponibles

| Tool | Función |
|------|---------|
| `git_status` | Estado del repo |
| `git_diff` | Ver cambios |
| `git_log` | Historial de commits |
| `git_commit` | Crear commit |
| `git_branch` | Gestión de branches |
| `git_checkout` | Cambiar de branch |
| `git_add` | Añadir al staging |

### Ejemplo de uso

```bash
# Crea un repositorio para configuración
mkdir ~/taskflow-config && cd ~/taskflow-config
git init
echo '{"tareas": []}' > tareas.json
git add . && git commit -m "Inicializar"
```

---

## 3. Memory MCP

Proporciona memoria persistente usando un **knowledge graph** (grafo de conocimiento).

### Configuración

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

### Tools disponibles

| Tool | Función | Ejemplo |
|------|---------|---------|
| `create_entities` | Crear entidades | Crear nodo "Usuario: Juan" |
| `create_relations` | Crear relaciones | "Juan -> prefiere -> tareas matutinas" |
| `search_nodes` | Buscar en el grafo | Encontrar preferencias |
| `read_graph` | Leer estado completo | Ver todo el conocimiento |
| `delete_entities` | Eliminar entidades | Borrar info obsoleta |

### Ejemplo conceptual

```
Entidades:
  - Usuario: Juan
  - Proyecto: Rediseño Web
  - Preferencia: Tareas Cortas

Relaciones:
  - Juan --trabaja_en--> Rediseño Web
  - Juan --prefiere--> Tareas Cortas
```

---

## 4. Fetch MCP

Obtiene contenido de URLs y lo convierte a formato optimizado para LLMs.

### Configuración

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

### Tools disponibles

| Tool | Función | Cuándo usar |
|------|---------|-------------|
| `fetch` | Obtener URL como Markdown | Artículos, documentación |
| `fetch_raw` | Obtener contenido sin procesar | APIs, JSON |

### Ventajas sobre HTTP directo

1. Limpia el HTML eliminando scripts y estilos
2. Extrae el contenido principal
3. Convierte a Markdown legible
4. Maneja errores y timeouts

---

## 5. Puppeteer MCP

Automatización de navegador para screenshots y scraping.

### Configuración

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

### Tools disponibles

| Tool | Función |
|------|---------|
| `navigate` | Navegar a URL |
| `screenshot` | Captura de pantalla |
| `click` | Hacer click en elemento |
| `type` | Escribir texto |
| `evaluate` | Ejecutar JavaScript |

---

## 6. Brave Search MCP

Búsqueda web integrada.

### Configuración

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "tu-api-key"
      }
    }
  }
}
```

### Obtener API Key

1. Ve a [Brave Search API](https://brave.com/search/api/)
2. Crea una cuenta
3. Genera una API key

---

## Recursos

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Documentación MCP](https://modelcontextprotocol.io)
