# Cloudflare MCP Servers

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Intermedio |
| **Requisitos** | Cuenta Cloudflare |
| **Tipo** | Servidores remotos (no requieren instalación local) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Configurar MCPs remotos de Cloudflare
- [ ] Gestionar Workers (funciones serverless)
- [ ] Usar D1 para base de datos SQL serverless
- [ ] Almacenar objetos en R2 (sin costos de egress)
- [ ] Usar KV para almacenamiento key-value

---

Cloudflare ofrece MCPs **remotos** para toda su plataforma:
- No necesitas instalar nada localmente
- La autenticación se maneja vía OAuth en el navegador
- Siempre tienes la versión más actualizada

---

## Catálogo de Servidores

| Servidor | URL | Función |
|----------|-----|---------|
| **Workers** | `workers.mcp.cloudflare.com` | Gestionar Cloudflare Workers |
| **KV** | `kv.mcp.cloudflare.com` | Key-Value storage |
| **R2** | `r2.mcp.cloudflare.com` | Object storage (S3-compatible) |
| **D1** | `d1.mcp.cloudflare.com` | Base de datos SQL serverless |
| **Observability** | `observability.mcp.cloudflare.com` | Analytics, logs, trazas |

---

## Configuración General

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

---

## 1. Workers MCP

Gestiona Cloudflare Workers (funciones serverless en el edge).

### Tools disponibles

| Tool | Función |
|------|---------|
| `list_workers` | Listar Workers |
| `get_worker` | Obtener código de un Worker |
| `deploy_worker` | Desplegar Worker |
| `delete_worker` | Eliminar Worker |
| `get_worker_logs` | Ver logs |

---

## 2. R2 MCP (Object Storage)

R2 es como S3 de AWS, pero **sin costos de egress** (transferencia de salida).

### Tools disponibles

| Tool | Función |
|------|---------|
| `list_buckets` | Listar buckets |
| `list_objects` | Listar objetos en bucket |
| `get_object` | Obtener objeto |
| `put_object` | Subir objeto |
| `delete_object` | Eliminar objeto |

### Caso de uso

Almacenar adjuntos de tareas (documentos, imágenes) en R2.

---

## 3. D1 MCP (SQL Database)

Base de datos SQL serverless basada en SQLite, distribuida globalmente.

### Tools disponibles

| Tool | Función |
|------|---------|
| `list_databases` | Listar bases de datos |
| `execute_sql` | Ejecutar consulta SQL |
| `get_schema` | Obtener schema |

### Ejemplo para TaskFlow

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
VALUES ('Revisar MCP', 'Completar módulo 4', 1);

-- Consultar tareas pendientes
SELECT * FROM tareas WHERE estado = 'pendiente' ORDER BY prioridad;
```

---

## 4. KV MCP (Key-Value)

Almacenamiento key-value distribuido globalmente.

### Tools disponibles

| Tool | Función |
|------|---------|
| `list_namespaces` | Listar namespaces |
| `get_value` | Obtener valor |
| `put_value` | Guardar valor |
| `delete_value` | Eliminar valor |
| `list_keys` | Listar keys |

### Casos de uso

- Caché de datos
- Configuración distribuida
- Sesiones de usuario
- Feature flags

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Configurar al menos un MCP de Cloudflare
- [ ] Autenticarte vía OAuth en el navegador
- [ ] Ejecutar una consulta SQL en D1
- [ ] Listar buckets en R2

---

## Resumen

| Aspecto | Cloudflare MCPs |
|---------|-----------------|
| **Mejor para** | Aplicaciones serverless en el edge |
| **Ventaja clave** | MCPs remotos, sin instalación, siempre actualizados |
| **Servicios** | Workers, D1, R2, KV |
| **Diferenciador** | R2 sin costos de egress (vs S3) |

---

## Recursos

- [Cloudflare MCP Docs](https://developers.cloudflare.com/workers/ai/mcp/)
- [Cloudflare Workers](https://workers.cloudflare.com/)
- [Cloudflare D1](https://developers.cloudflare.com/d1/)
