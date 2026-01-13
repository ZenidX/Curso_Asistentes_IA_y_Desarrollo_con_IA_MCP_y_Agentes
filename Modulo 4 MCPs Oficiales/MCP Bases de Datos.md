# MCPs de Bases de Datos

**⏱️ Tiempo estimado: 45 minutos**

## Panorama de opciones

| Tipo | MCP | Caso de uso |
|------|-----|-------------|
| **SQL Relacional** | PostgreSQL, MySQL, SQLite | Datos estructurados, relaciones complejas |
| **NoSQL Documentos** | MongoDB | Datos flexibles, esquema dinámico |
| **Key-Value** | Redis | Caché, sesiones, datos rápidos |

---

## 1. PostgreSQL MCP

**Cuándo usar**: Datos estructurados, transacciones ACID, consultas complejas con JOINs.

### Configuración

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

### Tools disponibles

| Tool | Función |
|------|---------|
| `query` | Ejecutar SELECT |
| `execute` | INSERT, UPDATE, DELETE |
| `describe_table` | Estructura de tabla |
| `list_tables` | Listar tablas |

### Resources

- `schema://tables` - Lista de tablas
- `schema://table/{nombre}` - Schema detallado

> ⚠️ Usa variables de entorno del sistema para credenciales, no las escribas en el archivo de configuración.

---

## 2. MySQL MCP

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

---

## 3. MongoDB MCP

**Cuándo usar**: Datos con estructura variable, documentos anidados.

### Configuración

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

### Tools disponibles

| Tool | Función |
|------|---------|
| `find` | Buscar documentos |
| `insertOne` | Insertar documento |
| `updateOne` | Actualizar documento |
| `deleteOne` | Eliminar documento |
| `aggregate` | Pipeline de agregación |

---

## 4. SQLite MCP

**Cuándo usar**: Desarrollo local, aplicaciones embebidas, prototipado rápido.

### Configuración

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

**Ventaja**: No necesitas servidor. El archivo `.db` es toda tu base de datos.

---

## 5. Redis MCP

**Cuándo usar**: Caché, sesiones de usuario, colas de tareas.

### Configuración

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

## Schema de ejemplo para TaskFlow

```sql
-- PostgreSQL/MySQL schema

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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Etiquetas
CREATE TABLE etiquetas (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  color VARCHAR(7)
);

-- Relación tareas-etiquetas
CREATE TABLE tarea_etiquetas (
  tarea_id INTEGER REFERENCES tareas(id),
  etiqueta_id INTEGER REFERENCES etiquetas(id),
  PRIMARY KEY (tarea_id, etiqueta_id)
);
```

---

## Probar conexión

```bash
# PostgreSQL
psql "postgresql://usuario:password@localhost:5432/taskflow"

# MySQL
mysql -u usuario -p -h localhost taskflow

# MongoDB
mongosh "mongodb://localhost:27017/taskflow"

# Redis
redis-cli ping
```

---

## Recursos

- [PostgreSQL MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
- [MongoDB MCP](https://github.com/mongodb-labs/mcp-mongo-server)
