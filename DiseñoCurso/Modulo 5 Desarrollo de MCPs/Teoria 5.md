# Módulo 5: Desarrollo de MCPs Propios

## Índice
1. [Arquitectura de un MCP Server](#1-arquitectura-de-un-mcp-server)
2. [Crear MCP Server en Python](#2-crear-mcp-server-en-python)
3. [Crear MCP Server en TypeScript](#3-crear-mcp-server-en-typescript)
4. [FastMCP para Desarrollo Rápido](#4-fastmcp-para-desarrollo-rápido)
5. [Servidor MCP con HTTP Transport](#5-servidor-mcp-con-http-transport)
6. [Testing y Debugging](#6-testing-y-debugging)
7. [Buenas Prácticas](#7-buenas-prácticas)
8. [Ejercicios Prácticos](#8-ejercicios-prácticos)

---

## 1. Arquitectura de un MCP Server

### Componentes Principales

```
MCP Server
├── Transport Layer (stdio / HTTP)
│   └── Maneja la comunicación con el cliente
├── Protocol Handler (JSON-RPC 2.0)
│   └── Parsea mensajes y gestiona el protocolo
├── Resources
│   └── Datos de solo lectura
├── Tools
│   └── Funciones ejecutables
└── Prompts
    └── Plantillas reutilizables
```

### Flujo de Comunicación

```
┌───────────────┐                      ┌───────────────┐
│  Cliente MCP  │                      │  Servidor MCP │
│  (Claude)     │                      │  (Tu código)  │
└───────┬───────┘                      └───────┬───────┘
        │                                      │
        │  1. initialize                       │
        │─────────────────────────────────────▶│
        │                                      │
        │  2. initialized + capabilities       │
        │◀─────────────────────────────────────│
        │                                      │
        │  3. tools/list                       │
        │─────────────────────────────────────▶│
        │                                      │
        │  4. Lista de herramientas            │
        │◀─────────────────────────────────────│
        │                                      │
        │  5. tools/call {name, arguments}     │
        │─────────────────────────────────────▶│
        │                                      │
        │  6. Resultado de la herramienta      │
        │◀─────────────────────────────────────│
```

### Formato de Mensajes JSON-RPC

**Request (Cliente → Servidor)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "buscar_producto",
    "arguments": {
      "query": "laptop",
      "precio_max": 1000
    }
  }
}
```

**Response (Servidor → Cliente)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\": 1, \"nombre\": \"Laptop Pro\", \"precio\": 999}]"
      }
    ]
  }
}
```

---

## 2. Crear MCP Server en Python

### Paso 1: Configurar el Proyecto

```bash
# Crear directorio del proyecto
mkdir mi-mcp-server && cd mi-mcp-server

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install mcp pydantic

# Crear estructura
mkdir -p src tests
touch src/__init__.py src/server.py
```

### Paso 2: requirements.txt

```txt
mcp>=1.0.0
pydantic>=2.0.0
httpx>=0.25.0
```

### Paso 3: Implementar el Servidor

```python
# src/server.py
"""
Mi primer servidor MCP en Python.
Ejemplo: API de productos para e-commerce.
"""

import json
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    Prompt,
    PromptArgument,
    GetPromptResult,
    PromptMessage,
)

# ============================================================================
# DATOS DE EJEMPLO (en producción, esto sería una base de datos)
# ============================================================================

PRODUCTOS = [
    {"id": 1, "nombre": "Laptop Pro 15", "categoria": "electronica", "precio": 1299.99, "stock": 15},
    {"id": 2, "nombre": "Laptop Basic 14", "categoria": "electronica", "precio": 599.99, "stock": 30},
    {"id": 3, "nombre": "Mouse Wireless", "categoria": "electronica", "precio": 49.99, "stock": 100},
    {"id": 4, "nombre": "Teclado Mecánico", "categoria": "electronica", "precio": 129.99, "stock": 45},
    {"id": 5, "nombre": "Silla Ergonómica", "categoria": "oficina", "precio": 299.99, "stock": 20},
    {"id": 6, "nombre": "Escritorio Ajustable", "categoria": "oficina", "precio": 449.99, "stock": 10},
]

PEDIDOS = []

# ============================================================================
# CREAR SERVIDOR MCP
# ============================================================================

server = Server("productos-mcp")

# ============================================================================
# TOOLS (Herramientas)
# ============================================================================

@server.tool()
async def buscar_productos(
    query: str,
    categoria: str | None = None,
    precio_max: float | None = None
) -> str:
    """
    Busca productos en el catálogo.

    Args:
        query: Término de búsqueda (nombre del producto)
        categoria: Filtrar por categoría (electronica, oficina, etc.)
        precio_max: Precio máximo en euros
    """
    resultados = []

    for producto in PRODUCTOS:
        # Filtrar por query
        if query.lower() not in producto["nombre"].lower():
            continue

        # Filtrar por categoría
        if categoria and producto["categoria"] != categoria.lower():
            continue

        # Filtrar por precio máximo
        if precio_max and producto["precio"] > precio_max:
            continue

        resultados.append(producto)

    return json.dumps(resultados, indent=2, ensure_ascii=False)


@server.tool()
async def obtener_producto(producto_id: int) -> str:
    """
    Obtiene los detalles de un producto por su ID.

    Args:
        producto_id: ID único del producto
    """
    for producto in PRODUCTOS:
        if producto["id"] == producto_id:
            return json.dumps(producto, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"Producto con ID {producto_id} no encontrado"})


@server.tool()
async def crear_pedido(producto_id: int, cantidad: int, cliente: str) -> str:
    """
    Crea un nuevo pedido.

    Args:
        producto_id: ID del producto a pedir
        cantidad: Cantidad de unidades
        cliente: Nombre o email del cliente
    """
    # Buscar producto
    producto = None
    for p in PRODUCTOS:
        if p["id"] == producto_id:
            producto = p
            break

    if not producto:
        return json.dumps({"error": f"Producto {producto_id} no encontrado"})

    # Verificar stock
    if producto["stock"] < cantidad:
        return json.dumps({
            "error": f"Stock insuficiente. Disponible: {producto['stock']}, Solicitado: {cantidad}"
        })

    # Crear pedido
    pedido = {
        "id": len(PEDIDOS) + 1,
        "producto_id": producto_id,
        "producto_nombre": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "total": producto["precio"] * cantidad,
        "cliente": cliente,
        "estado": "pendiente"
    }

    # Actualizar stock
    producto["stock"] -= cantidad

    # Guardar pedido
    PEDIDOS.append(pedido)

    return json.dumps(pedido, indent=2, ensure_ascii=False)


@server.tool()
async def listar_pedidos(cliente: str | None = None) -> str:
    """
    Lista todos los pedidos, opcionalmente filtrados por cliente.

    Args:
        cliente: Filtrar por nombre de cliente (opcional)
    """
    if cliente:
        pedidos_filtrados = [p for p in PEDIDOS if cliente.lower() in p["cliente"].lower()]
        return json.dumps(pedidos_filtrados, indent=2, ensure_ascii=False)

    return json.dumps(PEDIDOS, indent=2, ensure_ascii=False)


@server.tool()
async def calcular_total(producto_ids: list[int]) -> str:
    """
    Calcula el precio total de una lista de productos.

    Args:
        producto_ids: Lista de IDs de productos
    """
    total = 0
    detalles = []

    for pid in producto_ids:
        for producto in PRODUCTOS:
            if producto["id"] == pid:
                total += producto["precio"]
                detalles.append({
                    "id": pid,
                    "nombre": producto["nombre"],
                    "precio": producto["precio"]
                })
                break

    return json.dumps({
        "productos": detalles,
        "total": round(total, 2),
        "iva": round(total * 0.21, 2),
        "total_con_iva": round(total * 1.21, 2)
    }, indent=2, ensure_ascii=False)


# ============================================================================
# RESOURCES (Recursos de solo lectura)
# ============================================================================

@server.resource("catalogo://productos")
async def get_catalogo() -> str:
    """Devuelve el catálogo completo de productos."""
    return json.dumps({
        "total_productos": len(PRODUCTOS),
        "categorias": list(set(p["categoria"] for p in PRODUCTOS)),
        "productos": PRODUCTOS
    }, indent=2, ensure_ascii=False)


@server.resource("catalogo://estadisticas")
async def get_estadisticas() -> str:
    """Devuelve estadísticas del catálogo."""
    total_valor = sum(p["precio"] * p["stock"] for p in PRODUCTOS)
    return json.dumps({
        "total_productos": len(PRODUCTOS),
        "total_pedidos": len(PEDIDOS),
        "valor_inventario": round(total_valor, 2),
        "producto_mas_caro": max(PRODUCTOS, key=lambda x: x["precio"]),
        "producto_mas_barato": min(PRODUCTOS, key=lambda x: x["precio"]),
    }, indent=2, ensure_ascii=False)


# ============================================================================
# PROMPTS (Plantillas)
# ============================================================================

@server.prompt("analizar-ventas")
async def prompt_analizar_ventas(periodo: str = "semanal") -> GetPromptResult:
    """Genera un prompt para analizar las ventas."""
    return GetPromptResult(
        description=f"Analiza las ventas del periodo {periodo}",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Analiza las ventas del periodo {periodo}.

Utiliza las herramientas disponibles para:
1. Obtener la lista de pedidos
2. Revisar el inventario actual
3. Identificar productos más vendidos
4. Calcular ingresos totales
5. Detectar productos con bajo stock

Genera un informe con:
- Resumen ejecutivo
- Productos estrella
- Alertas de stock
- Recomendaciones

Usa formato markdown para el informe."""
                )
            )
        ]
    )


@server.prompt("recomendar-productos")
async def prompt_recomendar(
    presupuesto: str = "500",
    uso: str = "trabajo remoto"
) -> GetPromptResult:
    """Genera recomendaciones de productos."""
    return GetPromptResult(
        description=f"Recomienda productos para {uso} con presupuesto {presupuesto}€",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Un cliente busca productos para {uso} con un presupuesto de {presupuesto}€.

Usa las herramientas disponibles para:
1. Buscar productos relevantes
2. Verificar disponibilidad
3. Calcular el total

Genera una recomendación que incluya:
- Lista de productos sugeridos
- Justificación de cada elección
- Total con y sin IVA
- Alternativas si el presupuesto no alcanza"""
                )
            )
        ]
    )


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Ejecuta el servidor MCP."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Paso 4: Configurar en Claude

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "productos": {
      "command": "python",
      "args": ["/ruta/completa/a/mi-mcp-server/src/server.py"],
      "env": {
        "PYTHONPATH": "/ruta/completa/a/mi-mcp-server"
      }
    }
  }
}
```

### Paso 5: Probar

```bash
# Verificar que funciona
claude
/mcp  # Debería mostrar "productos" en la lista

# Probar herramientas
"Busca laptops con precio menor a 1000€"
"Crea un pedido de 2 Laptop Basic 14 para cliente@example.com"
"Muestra las estadísticas del catálogo"
```

---

## 3. Crear MCP Server en TypeScript

### Paso 1: Inicializar Proyecto

```bash
mkdir mcp-typescript && cd mcp-typescript
npm init -y
npm install @modelcontextprotocol/sdk
npm install -D typescript @types/node tsx
```

### Paso 2: tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

### Paso 3: package.json

```json
{
  "name": "mi-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "bin": {
    "mi-mcp": "./build/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/index.ts",
    "start": "node build/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Paso 4: Implementar el Servidor

```typescript
// src/index.ts
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// ============================================================================
// TIPOS
// ============================================================================

interface Tarea {
  id: number;
  titulo: string;
  descripcion: string;
  estado: "pendiente" | "en_progreso" | "completada";
  prioridad: "baja" | "media" | "alta";
  fechaCreacion: string;
  fechaLimite?: string;
}

// ============================================================================
// DATOS
// ============================================================================

let tareas: Tarea[] = [
  {
    id: 1,
    titulo: "Configurar proyecto",
    descripcion: "Inicializar el proyecto con TypeScript y MCP",
    estado: "completada",
    prioridad: "alta",
    fechaCreacion: "2025-01-01",
  },
  {
    id: 2,
    titulo: "Implementar API",
    descripcion: "Crear endpoints REST para el backend",
    estado: "en_progreso",
    prioridad: "alta",
    fechaCreacion: "2025-01-02",
    fechaLimite: "2025-01-15",
  },
  {
    id: 3,
    titulo: "Escribir documentación",
    descripcion: "Documentar la API y el código",
    estado: "pendiente",
    prioridad: "media",
    fechaCreacion: "2025-01-03",
  },
];

let nextId = 4;

// ============================================================================
// SERVIDOR
// ============================================================================

const server = new Server(
  {
    name: "tareas-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// ============================================================================
// TOOLS
// ============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "listar_tareas",
      description: "Lista todas las tareas, opcionalmente filtradas por estado",
      inputSchema: {
        type: "object" as const,
        properties: {
          estado: {
            type: "string",
            enum: ["pendiente", "en_progreso", "completada"],
            description: "Filtrar por estado",
          },
          prioridad: {
            type: "string",
            enum: ["baja", "media", "alta"],
            description: "Filtrar por prioridad",
          },
        },
      },
    },
    {
      name: "crear_tarea",
      description: "Crea una nueva tarea",
      inputSchema: {
        type: "object" as const,
        properties: {
          titulo: {
            type: "string",
            description: "Título de la tarea",
          },
          descripcion: {
            type: "string",
            description: "Descripción detallada",
          },
          prioridad: {
            type: "string",
            enum: ["baja", "media", "alta"],
            description: "Nivel de prioridad",
          },
          fechaLimite: {
            type: "string",
            description: "Fecha límite (formato YYYY-MM-DD)",
          },
        },
        required: ["titulo", "descripcion"],
      },
    },
    {
      name: "actualizar_estado",
      description: "Actualiza el estado de una tarea",
      inputSchema: {
        type: "object" as const,
        properties: {
          id: {
            type: "number",
            description: "ID de la tarea",
          },
          estado: {
            type: "string",
            enum: ["pendiente", "en_progreso", "completada"],
            description: "Nuevo estado",
          },
        },
        required: ["id", "estado"],
      },
    },
    {
      name: "eliminar_tarea",
      description: "Elimina una tarea por ID",
      inputSchema: {
        type: "object" as const,
        properties: {
          id: {
            type: "number",
            description: "ID de la tarea a eliminar",
          },
        },
        required: ["id"],
      },
    },
    {
      name: "obtener_estadisticas",
      description: "Obtiene estadísticas de las tareas",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "listar_tareas": {
      const { estado, prioridad } = args as {
        estado?: string;
        prioridad?: string;
      };

      let resultado = [...tareas];

      if (estado) {
        resultado = resultado.filter((t) => t.estado === estado);
      }
      if (prioridad) {
        resultado = resultado.filter((t) => t.prioridad === prioridad);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(resultado, null, 2),
          },
        ],
      };
    }

    case "crear_tarea": {
      const { titulo, descripcion, prioridad, fechaLimite } = args as {
        titulo: string;
        descripcion: string;
        prioridad?: "baja" | "media" | "alta";
        fechaLimite?: string;
      };

      const nuevaTarea: Tarea = {
        id: nextId++,
        titulo,
        descripcion,
        estado: "pendiente",
        prioridad: prioridad || "media",
        fechaCreacion: new Date().toISOString().split("T")[0],
        fechaLimite,
      };

      tareas.push(nuevaTarea);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              { mensaje: "Tarea creada", tarea: nuevaTarea },
              null,
              2
            ),
          },
        ],
      };
    }

    case "actualizar_estado": {
      const { id, estado } = args as {
        id: number;
        estado: "pendiente" | "en_progreso" | "completada";
      };

      const tarea = tareas.find((t) => t.id === id);

      if (!tarea) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ error: `Tarea ${id} no encontrada` }),
            },
          ],
        };
      }

      const estadoAnterior = tarea.estado;
      tarea.estado = estado;

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                mensaje: `Estado actualizado de '${estadoAnterior}' a '${estado}'`,
                tarea,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "eliminar_tarea": {
      const { id } = args as { id: number };
      const index = tareas.findIndex((t) => t.id === id);

      if (index === -1) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ error: `Tarea ${id} no encontrada` }),
            },
          ],
        };
      }

      const tareaEliminada = tareas.splice(index, 1)[0];

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              { mensaje: "Tarea eliminada", tarea: tareaEliminada },
              null,
              2
            ),
          },
        ],
      };
    }

    case "obtener_estadisticas": {
      const stats = {
        total: tareas.length,
        por_estado: {
          pendiente: tareas.filter((t) => t.estado === "pendiente").length,
          en_progreso: tareas.filter((t) => t.estado === "en_progreso").length,
          completada: tareas.filter((t) => t.estado === "completada").length,
        },
        por_prioridad: {
          alta: tareas.filter((t) => t.prioridad === "alta").length,
          media: tareas.filter((t) => t.prioridad === "media").length,
          baja: tareas.filter((t) => t.prioridad === "baja").length,
        },
        tasa_completado:
          tareas.length > 0
            ? Math.round(
                (tareas.filter((t) => t.estado === "completada").length /
                  tareas.length) *
                  100
              )
            : 0,
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(stats, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Herramienta desconocida: ${name}`);
  }
});

// ============================================================================
// RESOURCES
// ============================================================================

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "tareas://todas",
      name: "Lista completa de tareas",
      mimeType: "application/json",
    },
    {
      uri: "tareas://resumen",
      name: "Resumen del proyecto",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "tareas://todas") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(tareas, null, 2),
        },
      ],
    };
  }

  if (uri === "tareas://resumen") {
    const resumen = {
      fecha: new Date().toISOString(),
      total_tareas: tareas.length,
      completadas: tareas.filter((t) => t.estado === "completada").length,
      pendientes: tareas.filter((t) => t.estado === "pendiente").length,
      en_progreso: tareas.filter((t) => t.estado === "en_progreso").length,
      prioridad_alta: tareas.filter((t) => t.prioridad === "alta").length,
    };

    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(resumen, null, 2),
        },
      ],
    };
  }

  throw new Error(`Recurso no encontrado: ${uri}`);
});

// ============================================================================
// PROMPTS
// ============================================================================

server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "planificar-sprint",
      description: "Ayuda a planificar un sprint con las tareas pendientes",
      arguments: [
        {
          name: "duracion",
          description: "Duración del sprint en días",
          required: false,
        },
      ],
    },
    {
      name: "informe-estado",
      description: "Genera un informe del estado actual del proyecto",
    },
  ],
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "planificar-sprint") {
    const duracion = args?.duracion || "14";
    return {
      description: `Planificación de sprint de ${duracion} días`,
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Ayúdame a planificar un sprint de ${duracion} días.

Usa las herramientas disponibles para:
1. Listar todas las tareas pendientes y en progreso
2. Obtener las estadísticas actuales
3. Priorizar según urgencia y dependencias

Genera un plan que incluya:
- Tareas a completar en este sprint
- Orden de ejecución sugerido
- Estimación de tiempo por tarea
- Riesgos potenciales`,
          },
        },
      ],
    };
  }

  if (name === "informe-estado") {
    return {
      description: "Informe de estado del proyecto",
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Genera un informe ejecutivo del estado del proyecto.

Usa las herramientas para obtener:
1. Lista completa de tareas
2. Estadísticas de progreso

El informe debe incluir:
- Resumen ejecutivo (2-3 líneas)
- Progreso general (% completado)
- Tareas destacadas (completadas recientemente)
- Bloqueadores o riesgos
- Próximos pasos recomendados

Formato: Markdown`,
          },
        },
      ],
    };
  }

  throw new Error(`Prompt no encontrado: ${name}`);
});

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Servidor MCP de Tareas iniciado");
}

main().catch(console.error);
```

### Paso 5: Compilar y Configurar

```bash
# Compilar
npm run build

# Configurar en Claude
```

```json
{
  "mcpServers": {
    "tareas": {
      "command": "node",
      "args": ["/ruta/a/mcp-typescript/build/index.js"]
    }
  }
}
```

---

## 4. FastMCP para Desarrollo Rápido

FastMCP es una librería Python que simplifica enormemente la creación de servidores MCP.

### Instalación

```bash
pip install fastmcp
```

### Ejemplo Completo

```python
# fast_server.py
from fastmcp import FastMCP

# Crear servidor
mcp = FastMCP("Mi Servidor Rápido")

# ============================================================================
# TOOLS con decoradores simples
# ============================================================================

@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


@mcp.tool()
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b


@mcp.tool()
def buscar_usuario(email: str) -> dict:
    """Busca un usuario por email."""
    # Simular base de datos
    usuarios = {
        "admin@example.com": {"id": 1, "nombre": "Admin", "rol": "admin"},
        "user@example.com": {"id": 2, "nombre": "Usuario", "rol": "user"},
    }
    return usuarios.get(email, {"error": "Usuario no encontrado"})


@mcp.tool()
def crear_usuario(email: str, nombre: str, rol: str = "user") -> dict:
    """Crea un nuevo usuario."""
    return {
        "success": True,
        "usuario": {
            "email": email,
            "nombre": nombre,
            "rol": rol,
            "creado": True
        }
    }


@mcp.tool()
def obtener_clima(ciudad: str) -> dict:
    """Obtiene el clima de una ciudad (simulado)."""
    import random
    return {
        "ciudad": ciudad,
        "temperatura": random.randint(10, 30),
        "condicion": random.choice(["soleado", "nublado", "lluvia"]),
        "humedad": random.randint(30, 90)
    }


# ============================================================================
# RESOURCES
# ============================================================================

@mcp.resource("stats://daily")
def estadisticas_diarias() -> str:
    """Estadísticas del día."""
    import json
    return json.dumps({
        "visitas": 1500,
        "conversiones": 45,
        "ingresos": 2340.50,
        "usuarios_nuevos": 23
    })


@mcp.resource("config://app")
def configuracion_app() -> str:
    """Configuración de la aplicación."""
    import json
    return json.dumps({
        "version": "1.0.0",
        "ambiente": "produccion",
        "features": {
            "dark_mode": True,
            "notifications": True
        }
    })


# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    mcp.run()
```

### Configurar FastMCP

```json
{
  "mcpServers": {
    "fast": {
      "command": "python",
      "args": ["/ruta/a/fast_server.py"]
    }
  }
}
```

### Ventajas de FastMCP

| Característica | MCP SDK | FastMCP |
|----------------|---------|---------|
| Líneas de código | ~200+ | ~50 |
| Boilerplate | Alto | Mínimo |
| Decoradores | Manual | Automático |
| Type hints | Opcionales | Obligatorios (schema automático) |
| Curva aprendizaje | Moderada | Baja |

---

## 5. Servidor MCP con HTTP Transport

Para servidores remotos, usa HTTP/SSE en lugar de stdio.

### TypeScript con Express

```typescript
// src/http-server.ts
import express from "express";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const app = express();
app.use(express.json());

// Almacenar transports activos
const transports = new Map<string, SSEServerTransport>();

// Crear servidor MCP
const server = new Server(
  { name: "http-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Configurar tools (igual que antes)...

// Endpoint SSE para conexiones
app.get("/sse", async (req, res) => {
  const sessionId = req.query.sessionId as string || crypto.randomUUID();

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  const transport = new SSEServerTransport("/messages", res);
  transports.set(sessionId, transport);

  await server.connect(transport);

  req.on("close", () => {
    transports.delete(sessionId);
  });
});

// Endpoint para mensajes
app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId as string;
  const transport = transports.get(sessionId);

  if (!transport) {
    return res.status(404).json({ error: "Session not found" });
  }

  // Procesar mensaje
  await transport.handlePostMessage(req, res);
});

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", sessions: transports.size });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`MCP HTTP Server en http://localhost:${PORT}`);
});
```

### Configurar Servidor Remoto

```json
{
  "mcpServers": {
    "mi-servidor-remoto": {
      "command": "npx",
      "args": ["mcp-remote", "https://mi-servidor.com/mcp"]
    }
  }
}
```

---

## 6. Testing y Debugging

### MCP Inspector

El Inspector es la herramienta oficial para probar servidores MCP.

```bash
# Instalar
npm install -g @modelcontextprotocol/inspector

# Ejecutar con tu servidor
npx @modelcontextprotocol/inspector python src/server.py
npx @modelcontextprotocol/inspector node build/index.js
```

El Inspector proporciona:
- UI web para probar tools
- Ver resources disponibles
- Ejecutar prompts
- Ver logs de comunicación

### Tests Unitarios (Python)

```python
# tests/test_server.py
import pytest
import json
from src.server import buscar_productos, crear_pedido, PRODUCTOS

@pytest.mark.asyncio
async def test_buscar_productos():
    """Test búsqueda de productos."""
    resultado = await buscar_productos("Laptop")
    productos = json.loads(resultado)

    assert len(productos) >= 1
    assert all("Laptop" in p["nombre"] for p in productos)


@pytest.mark.asyncio
async def test_buscar_con_precio_max():
    """Test filtro por precio máximo."""
    resultado = await buscar_productos("", precio_max=100)
    productos = json.loads(resultado)

    assert all(p["precio"] <= 100 for p in productos)


@pytest.mark.asyncio
async def test_buscar_por_categoria():
    """Test filtro por categoría."""
    resultado = await buscar_productos("", categoria="oficina")
    productos = json.loads(resultado)

    assert all(p["categoria"] == "oficina" for p in productos)


@pytest.mark.asyncio
async def test_crear_pedido():
    """Test creación de pedido."""
    # Guardar stock inicial
    producto = PRODUCTOS[0]
    stock_inicial = producto["stock"]

    resultado = await crear_pedido(
        producto_id=producto["id"],
        cantidad=2,
        cliente="test@example.com"
    )
    pedido = json.loads(resultado)

    assert "id" in pedido
    assert pedido["cantidad"] == 2
    assert producto["stock"] == stock_inicial - 2


@pytest.mark.asyncio
async def test_crear_pedido_sin_stock():
    """Test error cuando no hay stock suficiente."""
    resultado = await crear_pedido(
        producto_id=1,
        cantidad=9999,
        cliente="test@example.com"
    )
    respuesta = json.loads(resultado)

    assert "error" in respuesta
    assert "Stock insuficiente" in respuesta["error"]
```

### Tests en TypeScript

```typescript
// tests/server.test.ts
import { describe, it, expect, beforeEach } from "vitest";

// Simular las funciones del servidor
const tareas = [
  { id: 1, titulo: "Test", estado: "pendiente", prioridad: "alta" },
];

describe("MCP Server", () => {
  it("debe listar tareas", () => {
    const resultado = tareas.filter((t) => t.estado === "pendiente");
    expect(resultado.length).toBeGreaterThan(0);
  });

  it("debe filtrar por prioridad", () => {
    const resultado = tareas.filter((t) => t.prioridad === "alta");
    expect(resultado.every((t) => t.prioridad === "alta")).toBe(true);
  });
});
```

### Logging y Debugging

```python
# Añadir logging a tu servidor
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mcp-server.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("mcp-server")

@server.tool()
async def mi_tool(param: str) -> str:
    logger.info(f"Tool llamado con param={param}")
    try:
        resultado = procesar(param)
        logger.debug(f"Resultado: {resultado}")
        return resultado
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

---

## 7. Buenas Prácticas

### 1. Validación de Inputs

```python
from pydantic import BaseModel, validator

class ProductoInput(BaseModel):
    nombre: str
    precio: float
    categoria: str

    @validator("precio")
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser positivo")
        return v

    @validator("categoria")
    def categoria_valida(cls, v):
        categorias_validas = ["electronica", "oficina", "hogar"]
        if v.lower() not in categorias_validas:
            raise ValueError(f"Categoría debe ser una de: {categorias_validas}")
        return v.lower()
```

### 2. Manejo de Errores

```python
@server.tool()
async def mi_tool(param: str) -> str:
    try:
        # Lógica principal
        resultado = procesar(param)
        return json.dumps({"success": True, "data": resultado})

    except ValueError as e:
        return json.dumps({"success": False, "error": str(e), "tipo": "validacion"})

    except ConnectionError as e:
        return json.dumps({"success": False, "error": "Error de conexión", "tipo": "conexion"})

    except Exception as e:
        logger.exception("Error inesperado")
        return json.dumps({"success": False, "error": "Error interno", "tipo": "interno"})
```

### 3. Documentación Clara

```python
@server.tool()
async def transferir_fondos(
    origen: str,
    destino: str,
    cantidad: float,
    concepto: str = "Transferencia"
) -> str:
    """
    Realiza una transferencia de fondos entre cuentas.

    Esta herramienta simula una transferencia bancaria. En producción,
    se conectaría con la API del banco.

    Args:
        origen: Número de cuenta origen (formato: ES00-0000-0000-00-0000000000)
        destino: Número de cuenta destino (mismo formato)
        cantidad: Cantidad a transferir en euros (mínimo 1€, máximo 10000€)
        concepto: Concepto de la transferencia (máximo 140 caracteres)

    Returns:
        JSON con el resultado de la operación:
        - success: bool indicando si fue exitosa
        - referencia: Código de referencia de la transferencia
        - timestamp: Fecha y hora de la operación

    Raises:
        ValueError: Si los parámetros son inválidos
        InsufficientFundsError: Si no hay fondos suficientes
    """
    # Implementación...
```

### 4. Rate Limiting

```python
from functools import wraps
from collections import defaultdict
import time

call_counts = defaultdict(list)

def rate_limit(max_calls: int, period: int):
    """Limita llamadas a max_calls por periodo (segundos)."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            key = func.__name__

            # Limpiar llamadas antiguas
            call_counts[key] = [t for t in call_counts[key] if now - t < period]

            if len(call_counts[key]) >= max_calls:
                return json.dumps({
                    "error": "Rate limit excedido",
                    "retry_after": period - (now - call_counts[key][0])
                })

            call_counts[key].append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@server.tool()
@rate_limit(max_calls=10, period=60)
async def operacion_costosa(param: str) -> str:
    # Solo permite 10 llamadas por minuto
    ...
```

### 5. Seguridad

```python
import os
from typing import Optional

# Variables de entorno para secrets
DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY")

# Sanitización de inputs
import re

def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Limpia input del usuario."""
    # Truncar
    value = value[:max_length]
    # Eliminar caracteres peligrosos
    value = re.sub(r'[<>"\']', '', value)
    return value.strip()

# Validar permisos
ALLOWED_PATHS = ["/app/data", "/app/uploads"]

def validate_path(path: str) -> bool:
    """Verifica que el path esté permitido."""
    from pathlib import Path
    resolved = Path(path).resolve()
    return any(str(resolved).startswith(allowed) for allowed in ALLOWED_PATHS)
```

---

## 8. Ejercicios Prácticos

### Ejercicio 1: MCP de Notas

Crea un servidor MCP que gestione notas con:
- Tools: crear_nota, buscar_notas, editar_nota, eliminar_nota
- Resources: notas://todas, notas://recientes
- Prompt: organizar-notas

### Ejercicio 2: MCP de API Externa

Crea un servidor que se conecte a una API real:
- OpenWeatherMap para clima
- O cualquier API pública

### Ejercicio 3: MCP con Base de Datos

Crea un servidor que use SQLite para persistencia:
- CRUD completo
- Migraciones de schema
- Backup automático

### Ejercicio 4: Testing Completo

Para cualquiera de los ejercicios anteriores:
- Tests unitarios con pytest/vitest
- Tests de integración
- Cobertura mínima del 80%

### Ejercicio 5: Publicar MCP

1. Empaqueta tu MCP para npm o PyPI
2. Documenta instalación y uso
3. Añade al directorio de MCPs

---

## Recursos Adicionales

- [MCP SDK Python](https://github.com/modelcontextprotocol/python-sdk)
- [MCP SDK TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [MCP Specification](https://modelcontextprotocol.io/docs)

---

## Próximo Módulo

En el **Módulo 6: Arquitectura de Desarrollo Asistido por IA** aprenderás:
- Patrones de arquitectura para desarrollo con IA
- Casos prácticos completos
- Workflows de automatización
- Mejores prácticas y checklists
