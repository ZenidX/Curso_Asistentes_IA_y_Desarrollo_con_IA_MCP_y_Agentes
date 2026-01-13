# Ejercicios: Módulo 5 - Desarrollo de MCPs

## Información

| | |
|---|---|
| **Dificultad progresiva** | Básico → Intermedio → Avanzado |
| **Tiempo total estimado** | 5-6 horas |
| **Requisitos** | Python 3.10+ o Node.js 18+, conocimientos de APIs |

---

## Ejercicio 1: MCP mínimo en Python

**Nivel**: Básico
**Tiempo**: 30 minutos

### Objetivo
Crear el servidor MCP más simple posible.

### Instrucciones

1. Crea un MCP con una única herramienta
2. Pruébalo manualmente
3. Conéctalo a Claude

### Código inicial

```python
# server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("mi-primer-mcp")

@app.tool()
async def saludar(nombre: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"¡Hola, {nombre}! Bienvenido al mundo de MCPs."

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read, write):
            await app.run(read, write)

    asyncio.run(main())
```

### Tareas

1. Ejecuta el servidor manualmente
2. Configúralo en Claude
3. Prueba la herramienta

### Configuración

```json
{
  "mcpServers": {
    "mi-primer-mcp": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

### Criterios de éxito
- [ ] El servidor inicia sin errores
- [ ] Aparece en `/mcp`
- [ ] La herramienta funciona

---

## Ejercicio 2: MCP con múltiples herramientas

**Nivel**: Básico
**Tiempo**: 35 minutos

### Objetivo
Añadir varias herramientas relacionadas a un MCP.

### Instrucciones

Crea un MCP "calculadora" con operaciones básicas.

### Código

```python
# calculadora_mcp.py
from mcp.server import Server

app = Server("calculadora")

@app.tool()
async def sumar(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b

@app.tool()
async def restar(a: float, b: float) -> float:
    """Resta dos números."""
    return a - b

@app.tool()
async def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b

@app.tool()
async def dividir(a: float, b: float) -> float:
    """Divide dos números."""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

@app.tool()
async def potencia(base: float, exponente: float) -> float:
    """Calcula la potencia de un número."""
    return base ** exponente

# TODO: Añade más operaciones
# - raiz_cuadrada
# - porcentaje
# - promedio (lista de números)
```

### Tareas

1. Completa las operaciones faltantes
2. Prueba todas las herramientas
3. Verifica el manejo de errores

### Criterios de éxito
- [ ] Todas las operaciones funcionan
- [ ] División por cero manejada
- [ ] Errores reportados claramente

---

## Ejercicio 3: MCP con recursos

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Implementar recursos (datos de solo lectura) en un MCP.

### Instrucciones

Crea un MCP que exponga configuración y estado como recursos.

### Código

```python
# config_mcp.py
from mcp.server import Server
from mcp.types import Resource
import json
import os

app = Server("config-manager")

# Datos de configuración
CONFIG = {
    "app_name": "TaskFlow",
    "version": "1.0.0",
    "environment": "development",
    "features": {
        "dark_mode": True,
        "notifications": True,
        "analytics": False
    }
}

@app.resource("config://settings")
async def get_settings() -> Resource:
    """Configuración actual de la aplicación."""
    return Resource(
        uri="config://settings",
        name="Application Settings",
        mimeType="application/json",
        text=json.dumps(CONFIG, indent=2)
    )

@app.resource("config://environment")
async def get_environment() -> Resource:
    """Variables de entorno relevantes."""
    env_vars = {
        "HOME": os.environ.get("HOME", "N/A"),
        "PATH": os.environ.get("PATH", "N/A")[:100] + "...",
        "SHELL": os.environ.get("SHELL", "N/A")
    }
    return Resource(
        uri="config://environment",
        name="Environment Variables",
        mimeType="application/json",
        text=json.dumps(env_vars, indent=2)
    )

# TODO: Añade recursos para:
# - config://features - Lista de features activas
# - config://status - Estado del sistema (uptime, memoria, etc.)
```

### Criterios de éxito
- [ ] Recursos accesibles desde Claude
- [ ] Datos formateados correctamente
- [ ] Múltiples recursos funcionando

---

## Ejercicio 4: MCP con validación

**Nivel**: Intermedio
**Tiempo**: 45 minutos

### Objetivo
Implementar validación robusta de inputs.

### Instrucciones

Crea un MCP para gestión de usuarios con validación completa.

### Código

```python
# users_mcp.py
from mcp.server import Server
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

app = Server("users-manager")

class UserCreate(BaseModel):
    username: str
    email: str
    age: int

    @validator('username')
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Username debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username solo puede contener letras, números y _')
        return v

    @validator('email')
    def email_valid(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Email inválido')
        return v

    @validator('age')
    def age_valid(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Edad debe estar entre 0 y 150')
        return v

# Base de datos simulada
users_db = []

@app.tool()
async def crear_usuario(username: str, email: str, age: int) -> dict:
    """Crea un nuevo usuario con validación."""
    try:
        user = UserCreate(username=username, email=email, age=age)
        user_dict = user.dict()
        user_dict['id'] = len(users_db) + 1
        users_db.append(user_dict)
        return {"success": True, "user": user_dict}
    except ValueError as e:
        return {"success": False, "error": str(e)}

@app.tool()
async def listar_usuarios() -> list:
    """Lista todos los usuarios."""
    return users_db

# TODO: Añade:
# - actualizar_usuario (con validación)
# - eliminar_usuario
# - buscar_por_email
```

### Criterios de éxito
- [ ] Validación funciona correctamente
- [ ] Errores devueltos de forma clara
- [ ] CRUD completo implementado

---

## Ejercicio 5: MCP con FastMCP

**Nivel**: Intermedio
**Tiempo**: 40 minutos

### Objetivo
Usar FastMCP para desarrollo rápido.

### Instrucciones

Recrea el MCP de calculadora usando FastMCP.

### Código

```python
# fast_calc.py
from fastmcp import FastMCP

mcp = FastMCP("Calculadora Avanzada")

@mcp.tool()
def sumar(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b

@mcp.tool()
def restar(a: float, b: float) -> float:
    """Resta dos números."""
    return a - b

@mcp.tool()
def historial() -> list:
    """Muestra el historial de operaciones."""
    # FastMCP maneja el estado automáticamente
    return mcp.state.get("historial", [])

@mcp.resource("calc://stats")
def estadisticas():
    """Estadísticas de uso."""
    return {
        "operaciones_totales": len(mcp.state.get("historial", [])),
        "ultima_operacion": mcp.state.get("historial", [])[-1] if mcp.state.get("historial") else None
    }
```

### Comparación

| Aspecto | SDK Oficial | FastMCP |
|---------|-------------|---------|
| Líneas de código | ~50 | ~20 |
| Configuración | Manual | Automática |
| Estado | Manual | Gestionado |
| Testing | Manual | Incluido |

### Criterios de éxito
- [ ] MCP funciona con FastMCP
- [ ] Menos código que versión manual
- [ ] Estado gestionado automáticamente

---

## Ejercicio 6: MCP con base de datos

**Nivel**: Avanzado
**Tiempo**: 55 minutos

### Objetivo
Crear un MCP que interactúe con una base de datos real.

### Instrucciones

Crea un MCP para gestionar tareas de TaskFlow.

### Código

```python
# taskflow_mcp.py
from mcp.server import Server
import sqlite3
from datetime import datetime
from pathlib import Path

app = Server("taskflow")

# Inicializar BD
DB_PATH = Path("taskflow.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.tool()
async def crear_tarea(title: str, description: str = "", priority: int = 3) -> dict:
    """Crea una nueva tarea."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
        (title, description, priority)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": task_id, "title": title, "status": "pending"}

@app.tool()
async def listar_tareas(status: str = None) -> list:
    """Lista tareas, opcionalmente filtradas por estado."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if status:
        rows = conn.execute("SELECT * FROM tasks WHERE status = ?", (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()
    return [dict(row) for row in rows]

@app.tool()
async def completar_tarea(task_id: int) -> dict:
    """Marca una tarea como completada."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE tasks SET status = 'completed', completed_at = ? WHERE id = ?",
        (datetime.now().isoformat(), task_id)
    )
    conn.commit()
    conn.close()
    return {"success": True, "task_id": task_id}

# TODO: Añade:
# - eliminar_tarea
# - actualizar_tarea
# - buscar_tareas (por texto)
# - estadisticas_tareas
```

### Criterios de éxito
- [ ] BD SQLite creada e inicializada
- [ ] CRUD completo de tareas
- [ ] Datos persisten entre sesiones

---

## Ejercicio 7: MCP con API externa

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Crear un MCP que consuma una API externa.

### Instrucciones

Crea un MCP para obtener información del clima.

### Código

```python
# weather_mcp.py
from mcp.server import Server
import httpx
import os

app = Server("weather")

API_KEY = os.environ.get("WEATHER_API_KEY", "demo")
BASE_URL = "https://api.weatherapi.com/v1"

@app.tool()
async def clima_actual(ciudad: str) -> dict:
    """Obtiene el clima actual de una ciudad."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/current.json",
            params={"key": API_KEY, "q": ciudad, "lang": "es"}
        )

        if response.status_code != 200:
            return {"error": f"No se pudo obtener el clima: {response.text}"}

        data = response.json()
        return {
            "ciudad": data["location"]["name"],
            "pais": data["location"]["country"],
            "temperatura_c": data["current"]["temp_c"],
            "condicion": data["current"]["condition"]["text"],
            "humedad": data["current"]["humidity"],
            "viento_kph": data["current"]["wind_kph"]
        }

@app.tool()
async def pronostico(ciudad: str, dias: int = 3) -> dict:
    """Obtiene el pronóstico para los próximos días."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/forecast.json",
            params={"key": API_KEY, "q": ciudad, "days": dias, "lang": "es"}
        )

        if response.status_code != 200:
            return {"error": "No se pudo obtener el pronóstico"}

        data = response.json()
        forecast = []
        for day in data["forecast"]["forecastday"]:
            forecast.append({
                "fecha": day["date"],
                "max_c": day["day"]["maxtemp_c"],
                "min_c": day["day"]["mintemp_c"],
                "condicion": day["day"]["condition"]["text"]
            })

        return {"ciudad": ciudad, "pronostico": forecast}

# TODO: Añade:
# - alertas_meteorologicas
# - comparar_ciudades
```

### Criterios de éxito
- [ ] API externa llamada correctamente
- [ ] Errores manejados apropiadamente
- [ ] Datos formateados para el usuario

---

## Ejercicio 8: MCP con TypeScript

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Crear un MCP usando TypeScript y el SDK oficial.

### Instrucciones

Porta el MCP de tareas a TypeScript.

### Código

```typescript
// taskflow-mcp/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";

const db = new Database("taskflow.db");

// Inicializar BD
db.exec(`
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

const server = new Server(
  { name: "taskflow-ts", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Listar herramientas
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "crear_tarea",
      description: "Crea una nueva tarea",
      inputSchema: {
        type: "object",
        properties: {
          title: { type: "string", description: "Título de la tarea" }
        },
        required: ["title"]
      }
    },
    {
      name: "listar_tareas",
      description: "Lista todas las tareas",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

// Ejecutar herramientas
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "crear_tarea": {
      const stmt = db.prepare("INSERT INTO tasks (title) VALUES (?)");
      const result = stmt.run(args.title);
      return {
        content: [{ type: "text", text: `Tarea creada con ID: ${result.lastInsertRowid}` }]
      };
    }
    case "listar_tareas": {
      const tasks = db.prepare("SELECT * FROM tasks").all();
      return {
        content: [{ type: "text", text: JSON.stringify(tasks, null, 2) }]
      };
    }
    default:
      throw new Error(`Tool desconocida: ${name}`);
  }
});

// Iniciar servidor
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

### Criterios de éxito
- [ ] Compila sin errores
- [ ] Funciona igual que versión Python
- [ ] Tipos correctamente definidos

---

## Ejercicio 9: Testing de MCPs

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Implementar tests para un servidor MCP.

### Código de tests

```python
# test_taskflow_mcp.py
import pytest
import asyncio
from mcp.client import Client
from mcp.client.stdio import stdio_client

@pytest.fixture
async def client():
    """Crea un cliente MCP conectado al servidor."""
    async with stdio_client(["python", "taskflow_mcp.py"]) as (read, write):
        client = Client()
        await client.connect(read, write)
        yield client

@pytest.mark.asyncio
async def test_crear_tarea(client):
    """Test: crear una tarea."""
    result = await client.call_tool("crear_tarea", {
        "title": "Test Task",
        "description": "Una tarea de prueba"
    })
    assert result["id"] is not None
    assert result["title"] == "Test Task"

@pytest.mark.asyncio
async def test_listar_tareas(client):
    """Test: listar tareas."""
    # Crear una tarea primero
    await client.call_tool("crear_tarea", {"title": "Task for List"})

    # Listar
    tasks = await client.call_tool("listar_tareas", {})
    assert len(tasks) > 0

@pytest.mark.asyncio
async def test_completar_tarea(client):
    """Test: completar una tarea."""
    # Crear tarea
    created = await client.call_tool("crear_tarea", {"title": "To Complete"})
    task_id = created["id"]

    # Completar
    result = await client.call_tool("completar_tarea", {"task_id": task_id})
    assert result["success"] == True

@pytest.mark.asyncio
async def test_validacion_titulo_vacio(client):
    """Test: validación de título vacío."""
    with pytest.raises(Exception):
        await client.call_tool("crear_tarea", {"title": ""})
```

### Criterios de éxito
- [ ] Tests ejecutan correctamente
- [ ] Cubren casos principales
- [ ] Incluyen tests de error

---

## Ejercicio 10: Proyecto final - MCP completo para TaskFlow

**Nivel**: Avanzado
**Tiempo**: 90 minutos

### Objetivo
Crear un MCP production-ready para TaskFlow.

### Requisitos

1. **CRUD completo** de tareas
2. **Proyectos** para agrupar tareas
3. **Etiquetas** para categorizar
4. **Estadísticas** y reportes
5. **Validación** robusta
6. **Tests** completos
7. **Documentación**

### Estructura

```
taskflow-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py        # Servidor principal
│   ├── database.py      # Gestión de BD
│   ├── models.py        # Modelos de datos
│   ├── tools/           # Herramientas
│   │   ├── tasks.py
│   │   ├── projects.py
│   │   └── stats.py
│   └── resources/       # Recursos
│       └── config.py
├── tests/
│   ├── test_tasks.py
│   ├── test_projects.py
│   └── test_integration.py
├── requirements.txt
├── README.md
└── setup.py
```

### Entregables

1. Código completo del MCP
2. Tests con >80% cobertura
3. README con instrucciones
4. Configuración de ejemplo para Claude

### Criterios de éxito
- [ ] Todas las funcionalidades implementadas
- [ ] Tests pasando
- [ ] Documentación completa
- [ ] Funciona con Claude Desktop/CLI

---

## Recursos adicionales

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Examples](https://github.com/modelcontextprotocol/servers)
