# Supabase MCP

## Información

| | |
|---|---|
| **Duración** | 35 minutos |
| **Nivel** | Intermedio |
| **Requisitos** | Proyecto en Supabase, credenciales API |
| **Costo** | Tier gratuito disponible |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Configurar Supabase MCP (remoto o local)
- [ ] Ejecutar consultas SQL desde Claude
- [ ] Gestionar usuarios y autenticación
- [ ] Usar Row Level Security para proteger datos
- [ ] Subir y gestionar archivos en Storage

---

Supabase es una alternativa open source a Firebase que ofrece:
- Base de datos PostgreSQL
- Autenticación
- Storage
- Edge Functions
- Realtime subscriptions

---

## ¿Por qué Supabase?

| Característica | Supabase | Firebase |
|----------------|----------|----------|
| Base de datos | PostgreSQL (SQL) | Firestore (NoSQL) |
| Open Source | ✅ Completo | ❌ No |
| Self-hosting | ✅ Posible | ❌ No |
| Pricing | Más predecible | Por operaciones |
| SQL | ✅ Completo | ❌ No |

---

## Configuración

### Opción 1: MCP Remoto (Recomendado)

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

La autenticación se realiza vía OAuth en el navegador.

### Opción 2: MCP Local con API Keys

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "supabase-mcp"],
      "env": {
        "SUPABASE_URL": "https://xxxxx.supabase.co",
        "SUPABASE_SERVICE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
    }
  }
}
```

---

## Obtener credenciales

1. Ve a [Supabase Dashboard](https://app.supabase.com/)
2. Selecciona tu proyecto
3. Settings → API
4. Copia:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **Service Role Key**: Para acceso completo (solo desarrollo)
   - **Anon Key**: Para acceso público limitado

> ⚠️ **Nunca expongas el Service Role Key** en código cliente o repositorios públicos.

---

## Capacidades del MCP

### Database

| Tool | Función |
|------|---------|
| `query` | Ejecutar consultas SQL |
| `insert` | Insertar filas |
| `update` | Actualizar filas |
| `delete` | Eliminar filas |
| `describe_table` | Ver estructura de tabla |
| `list_tables` | Listar tablas |

### Auth

| Tool | Función |
|------|---------|
| `list_users` | Listar usuarios |
| `create_user` | Crear usuario |
| `update_user` | Actualizar usuario |
| `delete_user` | Eliminar usuario |

### Storage

| Tool | Función |
|------|---------|
| `list_buckets` | Listar buckets |
| `list_files` | Listar archivos |
| `upload_file` | Subir archivo |
| `download_file` | Descargar archivo |
| `delete_file` | Eliminar archivo |

### Edge Functions

| Tool | Función |
|------|---------|
| `list_functions` | Listar functions |
| `invoke_function` | Invocar function |

---

## Ejemplo para TaskFlow

### Crear tabla de tareas

```sql
-- Ejecutar en Supabase SQL Editor o via MCP
CREATE TABLE tareas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  titulo TEXT NOT NULL,
  descripcion TEXT,
  estado TEXT DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'en_progreso', 'completada')),
  prioridad INT DEFAULT 3 CHECK (prioridad BETWEEN 1 AND 5),
  user_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE tareas ENABLE ROW LEVEL SECURITY;

-- Política: usuarios solo ven sus tareas
CREATE POLICY "Users can view own tasks"
  ON tareas FOR SELECT
  USING (auth.uid() = user_id);

-- Política: usuarios pueden crear sus tareas
CREATE POLICY "Users can create own tasks"
  ON tareas FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

### Operaciones con MCP

```
Usuario: "Muestra todas las tareas pendientes"
Claude: query("SELECT * FROM tareas WHERE estado = 'pendiente' ORDER BY prioridad")

Usuario: "Crea una tarea de alta prioridad"
Claude: insert(
  table="tareas",
  data={
    titulo: "Revisar MCPs",
    descripcion: "Completar módulo 4",
    prioridad: 1,
    user_id: "uuid-del-usuario"
  }
)

Usuario: "Marca la tarea como completada"
Claude: update(
  table="tareas",
  match={id: "uuid-tarea"},
  data={estado: "completada", updated_at: "now()"}
)
```

---

## Modo seguro (Solo lectura)

Para entornos de producción o cuando quieres limitar el acceso:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.supabase.com/mcp"],
      "env": {
        "READ_ONLY": "true"
      }
    }
  }
}
```

---

## Realtime (Tiempo real)

Supabase permite suscripciones en tiempo real a cambios en la base de datos:

```javascript
// Ejemplo en código (no MCP)
const channel = supabase
  .channel('tareas-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'tareas' },
    (payload) => console.log('Cambio:', payload)
  )
  .subscribe()
```

---

## Ventajas sobre Firebase

1. **SQL completo**: JOINs, vistas, funciones PostgreSQL
2. **Row Level Security**: Políticas de seguridad a nivel de fila
3. **Self-hosting**: Puedes hostear tu propia instancia
4. **Extensiones**: PostGIS, pg_vector, etc.
5. **Open Source**: Código completamente abierto

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Obtener credenciales desde el Dashboard de Supabase
- [ ] Configurar el MCP (remoto u local)
- [ ] Ejecutar una consulta SQL desde Claude
- [ ] Entender la diferencia entre Service Role Key y Anon Key

---

## Resumen

| Aspecto | Supabase MCP |
|---------|--------------|
| **Mejor para** | Proyectos que necesitan PostgreSQL + Auth + Storage |
| **Ventaja clave** | Open source, SQL completo, Row Level Security |
| **Precaución** | Nunca exponer Service Role Key en cliente |
| **Alternativa a** | Firebase (pero con SQL en lugar de NoSQL) |

---

## Recursos

- [Supabase MCP Docs](https://supabase.com/docs/guides/getting-started/mcp)
- [Supabase Dashboard](https://app.supabase.com/)
- [Supabase GitHub](https://github.com/supabase/supabase)
- [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp)
