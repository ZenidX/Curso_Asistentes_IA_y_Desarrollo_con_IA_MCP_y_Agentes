# Modulo 5: Desarrollo de MCPs Propios

## Informacion del Modulo

| | |
|---|---|
| **Duracion estimada** | 6-8 horas |
| **Nivel** | Intermedio-Avanzado |
| **Prerrequisitos** | Modulo 4 completado, Python 3.10+ o Node.js 18+, Claude Code funcionando |

---

## Objetivos de Aprendizaje

Al completar este modulo, seras capaz de:

- [ ] Comprender la arquitectura interna de un servidor MCP y el flujo de comunicacion JSON-RPC
- [ ] Crear un servidor MCP funcional en Python usando el SDK oficial
- [ ] Crear un servidor MCP funcional en TypeScript usando el SDK oficial
- [ ] Utilizar FastMCP para desarrollo rapido de servidores MCP
- [ ] Implementar transporte HTTP/SSE para servidores MCP remotos
- [ ] Aplicar testing y debugging efectivo a servidores MCP
- [ ] Integrar un MCP personalizado con el proyecto TaskFlow

---

## Continuacion del Proyecto: TaskFlow

En este modulo, crearemos un **MCP personalizado para TaskFlow** que permitira a Claude interactuar directamente con nuestro sistema de gestion de tareas.

```
TaskFlow/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
├── .claude/
│   ├── commands/
│   └── hooks.json
├── mcp-servers/              <-- NUEVO: Nuestros MCPs personalizados
│   ├── taskflow-mcp/         <-- MCP para TaskFlow
│   │   ├── src/
│   │   │   └── server.py
│   │   ├── tests/
│   │   └── requirements.txt
│   └── README.md
├── mcp-config.json
└── CLAUDE.md
```

**Objetivo del modulo**: Crear un MCP que permita a Claude crear, listar, actualizar y eliminar tareas en TaskFlow, asi como generar informes y estadisticas.

---

## Indice

1. [Arquitectura de un MCP Server](#1-arquitectura-de-un-mcp-server)
2. [Crear MCP Server en Python](#2-crear-mcp-server-en-python)
3. [Crear MCP Server en TypeScript](#3-crear-mcp-server-en-typescript)
4. [FastMCP para Desarrollo Rapido](#4-fastmcp-para-desarrollo-rapido)
5. [Servidor MCP con HTTP Transport](#5-servidor-mcp-con-http-transport)
6. [Testing y Debugging](#6-testing-y-debugging)
7. [Troubleshooting](#7-troubleshooting)
8. [Ejercicios Practicos](#8-ejercicios-practicos)
9. [Resumen y Preparacion para el Modulo 6](#9-resumen-y-preparacion-para-el-modulo-6)

---

## 1. Arquitectura de un MCP Server

**Tiempo estimado: 45 minutos**

### 1.1 Por que Necesitas Entender la Arquitectura

Antes de escribir codigo, es fundamental entender **como funciona internamente un MCP**. Esto te permitira:

1. **Debuggear problemas**: Saber donde buscar cuando algo falla
2. **Optimizar rendimiento**: Entender el flujo de datos para evitar cuellos de botella
3. **Disenar mejores herramientas**: Crear tools que aprovechen al maximo el protocolo
4. **Extender funcionalidad**: Implementar features avanzadas cuando las necesites

### 1.2 Componentes Principales

Un servidor MCP se compone de capas bien definidas. Cada capa tiene una responsabilidad especifica:

```
MCP Server
├── Transport Layer (stdio / HTTP)
│   └── Maneja la comunicacion con el cliente
│       Por que: Abstrae el medio de comunicacion
│
├── Protocol Handler (JSON-RPC 2.0)
│   └── Parsea mensajes y gestiona el protocolo
│       Por que: Estandar de la industria, bien documentado
│
├── Resources
│   └── Datos de solo lectura
│       Por que: Informacion que Claude puede consultar
│
├── Tools
│   └── Funciones ejecutables
│       Por que: Acciones que Claude puede realizar
│
└── Prompts
    └── Plantillas reutilizables
        Por que: Guias predefinidas para tareas comunes
```

### 1.3 Flujo de Comunicacion Detallado

Cuando Claude se conecta a tu MCP, ocurre esta secuencia:

```
┌───────────────┐                      ┌───────────────┐
│  Cliente MCP  │                      │  Servidor MCP │
│  (Claude)     │                      │  (Tu codigo)  │
└───────┬───────┘                      └───────┬───────┘
        │                                      │
        │  1. initialize                       │
        │─────────────────────────────────────>│
        │     "Hola, soy Claude v1.0"          │
        │                                      │
        │  2. initialized + capabilities       │
        │<─────────────────────────────────────│
        │     "Hola, tengo tools, resources"   │
        │                                      │
        │  3. tools/list                       │
        │─────────────────────────────────────>│
        │     "Que herramientas tienes?"       │
        │                                      │
        │  4. Lista de herramientas            │
        │<─────────────────────────────────────│
        │     "[buscar, crear, eliminar...]"   │
        │                                      │
        │  5. tools/call {name, arguments}     │
        │─────────────────────────────────────>│
        │     "Ejecuta 'buscar' con estos args"│
        │                                      │
        │  6. Resultado de la herramienta      │
        │<─────────────────────────────────────│
        │     "{resultado: [...]}"             │
```

### 1.4 Formato de Mensajes JSON-RPC

El protocolo MCP usa **JSON-RPC 2.0**, un estandar sencillo para llamadas remotas.

**Por que JSON-RPC?**
- Simple de implementar y debuggear
- Bien soportado en todos los lenguajes
- Formato legible por humanos
- Manejo de errores estandarizado

**Request (Cliente -> Servidor)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "buscar_tarea",
    "arguments": {
      "query": "implementar API",
      "estado": "pendiente"
    }
  }
}
```

**Por que cada campo?**
- `jsonrpc`: Version del protocolo (siempre "2.0")
- `id`: Identificador unico para correlacionar respuestas
- `method`: Accion a ejecutar
- `params`: Argumentos de la accion

**Response (Servidor -> Cliente)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\": 1, \"titulo\": \"Implementar API REST\", \"estado\": \"pendiente\"}]"
      }
    ]
  }
}
```

### Error Comun: Confundir Resources con Tools

**Resources** son datos de solo lectura que Claude puede consultar:
- Catalogo de productos
- Configuracion del sistema
- Estadisticas

**Tools** son funciones que realizan acciones:
- Crear una tarea
- Enviar un email
- Modificar un archivo

**Regla practica**: Si modifica estado o tiene efectos secundarios, es un **Tool**. Si solo devuelve informacion, puede ser un **Resource**.

---

### Checkpoint 1

Antes de continuar, asegurate de poder responder:

- [ ] Que protocolo usa MCP para comunicacion? (JSON-RPC 2.0)
- [ ] Cuales son los 3 tipos de capacidades que puede exponer un MCP? (Tools, Resources, Prompts)
- [ ] Cual es la diferencia principal entre un Resource y un Tool?

---

## 2. Crear MCP Server en Python

**Tiempo estimado: 90 minutos**

### 2.1 Por que Python para MCPs?

Python es ideal para MCPs por varias razones:

1. **Sintaxis clara**: Facil de leer y mantener
2. **Ecosistema rico**: Librerias para todo (bases de datos, APIs, ML)
3. **Tipado opcional**: Type hints mejoran la documentacion automatica
4. **FastMCP disponible**: Framework que simplifica aun mas el desarrollo

### 2.2 Configurar el Proyecto

**Practica Guiada: Crear estructura del proyecto TaskFlow MCP**

```bash
# Paso 1: Crear directorio del proyecto
cd TaskFlow
mkdir -p mcp-servers/taskflow-mcp/src
mkdir -p mcp-servers/taskflow-mcp/tests
cd mcp-servers/taskflow-mcp

# Paso 2: Crear entorno virtual
python -m venv venv

# Activar segun tu sistema operativo:
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Paso 3: Crear requirements.txt
```

### 2.3 requirements.txt

```txt
# Core MCP
mcp>=1.0.0

# Validacion de datos
pydantic>=2.0.0

# Cliente HTTP (para integraciones)
httpx>=0.25.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

**Por que cada dependencia?**
- `mcp`: SDK oficial de Anthropic para crear servidores MCP
- `pydantic`: Validacion robusta de datos con type hints
- `httpx`: Cliente HTTP async (si tu MCP conecta con APIs)
- `pytest*`: Framework de testing profesional

```bash
# Instalar dependencias
pip install -r requirements.txt
```

### 2.4 Implementar el Servidor MCP para TaskFlow

Ahora crearemos un servidor MCP que se integra con TaskFlow. Este servidor permitira a Claude:
- Listar tareas
- Crear nuevas tareas
- Actualizar estados
- Obtener estadisticas

```python
# src/server.py
"""
TaskFlow MCP Server
Permite a Claude interactuar con el sistema de gestion de tareas TaskFlow.

Este servidor expone:
- Tools: Operaciones CRUD sobre tareas
- Resources: Datos de solo lectura (estadisticas, configuracion)
- Prompts: Plantillas para tareas comunes
"""

import json
import asyncio
from datetime import datetime
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    GetPromptResult,
    PromptMessage,
)

# ============================================================================
# DATOS DE TASKFLOW
# En produccion, esto se conectaria a la base de datos real de TaskFlow
# ============================================================================

# Simulamos la base de datos de TaskFlow
TAREAS = [
    {
        "id": 1,
        "titulo": "Configurar proyecto TaskFlow",
        "descripcion": "Inicializar el proyecto con la estructura basica",
        "estado": "completada",
        "prioridad": "alta",
        "asignado": "dev@taskflow.com",
        "fecha_creacion": "2025-01-01",
        "fecha_limite": "2025-01-05"
    },
    {
        "id": 2,
        "titulo": "Implementar autenticacion",
        "descripcion": "Sistema de login con JWT",
        "estado": "en_progreso",
        "prioridad": "alta",
        "asignado": "dev@taskflow.com",
        "fecha_creacion": "2025-01-02",
        "fecha_limite": "2025-01-10"
    },
    {
        "id": 3,
        "titulo": "Crear dashboard de estadisticas",
        "descripcion": "Panel con graficas de progreso del proyecto",
        "estado": "pendiente",
        "prioridad": "media",
        "asignado": None,
        "fecha_creacion": "2025-01-03",
        "fecha_limite": "2025-01-20"
    },
]

# Contador para IDs
_next_id = 4

# ============================================================================
# CREAR SERVIDOR MCP
# ============================================================================

# El nombre del servidor aparecera en Claude cuando liste MCPs disponibles
server = Server("taskflow-mcp")

# ============================================================================
# TOOLS (Herramientas)
# Estas son las acciones que Claude puede ejecutar
# ============================================================================

@server.tool()
async def listar_tareas(
    estado: Optional[str] = None,
    prioridad: Optional[str] = None,
    asignado: Optional[str] = None
) -> str:
    """
    Lista las tareas de TaskFlow con filtros opcionales.

    Esta herramienta permite obtener una vista de las tareas del proyecto,
    pudiendo filtrar por diferentes criterios para encontrar exactamente
    lo que necesitas.

    Args:
        estado: Filtrar por estado (pendiente, en_progreso, completada)
        prioridad: Filtrar por prioridad (baja, media, alta)
        asignado: Filtrar por email del responsable

    Returns:
        JSON con la lista de tareas que coinciden con los filtros
    """
    # Comenzamos con todas las tareas
    resultado = TAREAS.copy()

    # Aplicamos filtros si se especifican
    # Por que filtrar asi? Permite combinaciones flexibles de filtros
    if estado:
        resultado = [t for t in resultado if t["estado"] == estado.lower()]

    if prioridad:
        resultado = [t for t in resultado if t["prioridad"] == prioridad.lower()]

    if asignado:
        resultado = [t for t in resultado if t.get("asignado") == asignado]

    # Devolvemos JSON formateado para legibilidad
    return json.dumps({
        "total": len(resultado),
        "tareas": resultado
    }, indent=2, ensure_ascii=False)


@server.tool()
async def crear_tarea(
    titulo: str,
    descripcion: str,
    prioridad: str = "media",
    asignado: Optional[str] = None,
    fecha_limite: Optional[str] = None
) -> str:
    """
    Crea una nueva tarea en TaskFlow.

    Use esta herramienta cuando el usuario quiera agregar una nueva tarea
    al proyecto. La tarea se creara con estado 'pendiente' por defecto.

    Args:
        titulo: Titulo descriptivo de la tarea (maximo 100 caracteres)
        descripcion: Descripcion detallada de lo que hay que hacer
        prioridad: Nivel de urgencia (baja, media, alta). Default: media
        asignado: Email del responsable. Default: sin asignar
        fecha_limite: Fecha limite en formato YYYY-MM-DD. Default: sin fecha

    Returns:
        JSON con los datos de la tarea creada, incluyendo su ID
    """
    global _next_id

    # Validacion basica
    # Por que validar? Previene datos corruptos en la base de datos
    if not titulo or len(titulo.strip()) == 0:
        return json.dumps({"error": "El titulo es obligatorio"})

    if prioridad.lower() not in ["baja", "media", "alta"]:
        return json.dumps({"error": "Prioridad debe ser: baja, media o alta"})

    # Crear la nueva tarea
    nueva_tarea = {
        "id": _next_id,
        "titulo": titulo.strip()[:100],  # Truncamos a 100 caracteres
        "descripcion": descripcion.strip(),
        "estado": "pendiente",
        "prioridad": prioridad.lower(),
        "asignado": asignado,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
        "fecha_limite": fecha_limite
    }

    # Guardar en nuestra "base de datos"
    TAREAS.append(nueva_tarea)
    _next_id += 1

    return json.dumps({
        "mensaje": "Tarea creada exitosamente",
        "tarea": nueva_tarea
    }, indent=2, ensure_ascii=False)


@server.tool()
async def actualizar_tarea(
    tarea_id: int,
    estado: Optional[str] = None,
    prioridad: Optional[str] = None,
    asignado: Optional[str] = None,
    fecha_limite: Optional[str] = None
) -> str:
    """
    Actualiza una tarea existente en TaskFlow.

    Permite modificar el estado, prioridad, asignacion o fecha limite
    de una tarea. Solo se actualizan los campos que se especifiquen.

    Args:
        tarea_id: ID de la tarea a actualizar (obligatorio)
        estado: Nuevo estado (pendiente, en_progreso, completada)
        prioridad: Nueva prioridad (baja, media, alta)
        asignado: Nuevo responsable (email)
        fecha_limite: Nueva fecha limite (YYYY-MM-DD)

    Returns:
        JSON con la tarea actualizada o error si no se encuentra
    """
    # Buscar la tarea
    tarea = None
    for t in TAREAS:
        if t["id"] == tarea_id:
            tarea = t
            break

    if not tarea:
        return json.dumps({"error": f"Tarea con ID {tarea_id} no encontrada"})

    # Guardar estado anterior para el mensaje
    cambios = []

    # Actualizar solo los campos especificados
    # Por que este patron? Permite actualizaciones parciales sin sobrescribir datos
    if estado:
        if estado.lower() not in ["pendiente", "en_progreso", "completada"]:
            return json.dumps({"error": "Estado invalido"})
        cambios.append(f"estado: {tarea['estado']} -> {estado.lower()}")
        tarea["estado"] = estado.lower()

    if prioridad:
        if prioridad.lower() not in ["baja", "media", "alta"]:
            return json.dumps({"error": "Prioridad invalida"})
        cambios.append(f"prioridad: {tarea['prioridad']} -> {prioridad.lower()}")
        tarea["prioridad"] = prioridad.lower()

    if asignado is not None:  # Permite asignar string vacio para desasignar
        cambios.append(f"asignado: {tarea['asignado']} -> {asignado or 'sin asignar'}")
        tarea["asignado"] = asignado if asignado else None

    if fecha_limite:
        cambios.append(f"fecha_limite: {tarea['fecha_limite']} -> {fecha_limite}")
        tarea["fecha_limite"] = fecha_limite

    if not cambios:
        return json.dumps({"mensaje": "No se especificaron cambios", "tarea": tarea})

    return json.dumps({
        "mensaje": "Tarea actualizada",
        "cambios": cambios,
        "tarea": tarea
    }, indent=2, ensure_ascii=False)


@server.tool()
async def eliminar_tarea(tarea_id: int) -> str:
    """
    Elimina una tarea de TaskFlow.

    ADVERTENCIA: Esta accion es irreversible. Use con precaucion.

    Args:
        tarea_id: ID de la tarea a eliminar

    Returns:
        JSON confirmando la eliminacion o error si no se encuentra
    """
    global TAREAS

    # Buscar y eliminar
    for i, tarea in enumerate(TAREAS):
        if tarea["id"] == tarea_id:
            tarea_eliminada = TAREAS.pop(i)
            return json.dumps({
                "mensaje": "Tarea eliminada",
                "tarea_eliminada": tarea_eliminada
            }, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"Tarea con ID {tarea_id} no encontrada"})


@server.tool()
async def buscar_tareas(query: str) -> str:
    """
    Busca tareas por texto en titulo o descripcion.

    Realiza una busqueda de texto simple (case-insensitive) en los
    campos titulo y descripcion de todas las tareas.

    Args:
        query: Texto a buscar

    Returns:
        JSON con las tareas que contienen el texto buscado
    """
    query_lower = query.lower()
    resultado = []

    for tarea in TAREAS:
        if (query_lower in tarea["titulo"].lower() or
            query_lower in tarea["descripcion"].lower()):
            resultado.append(tarea)

    return json.dumps({
        "query": query,
        "total_encontradas": len(resultado),
        "tareas": resultado
    }, indent=2, ensure_ascii=False)


# ============================================================================
# RESOURCES (Recursos de solo lectura)
# Estos proporcionan datos que Claude puede consultar sin modificar nada
# ============================================================================

@server.resource("taskflow://estadisticas")
async def get_estadisticas() -> str:
    """
    Devuelve estadisticas generales del proyecto TaskFlow.

    Incluye conteos por estado, prioridad, y metricas de progreso.
    """
    total = len(TAREAS)

    # Contar por estado
    por_estado = {
        "pendiente": len([t for t in TAREAS if t["estado"] == "pendiente"]),
        "en_progreso": len([t for t in TAREAS if t["estado"] == "en_progreso"]),
        "completada": len([t for t in TAREAS if t["estado"] == "completada"])
    }

    # Contar por prioridad
    por_prioridad = {
        "alta": len([t for t in TAREAS if t["prioridad"] == "alta"]),
        "media": len([t for t in TAREAS if t["prioridad"] == "media"]),
        "baja": len([t for t in TAREAS if t["prioridad"] == "baja"])
    }

    # Calcular porcentaje de completado
    porcentaje_completado = (por_estado["completada"] / total * 100) if total > 0 else 0

    # Tareas sin asignar
    sin_asignar = len([t for t in TAREAS if t.get("asignado") is None])

    return json.dumps({
        "total_tareas": total,
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "porcentaje_completado": round(porcentaje_completado, 1),
        "tareas_sin_asignar": sin_asignar,
        "fecha_consulta": datetime.now().isoformat()
    }, indent=2, ensure_ascii=False)


@server.resource("taskflow://tareas-urgentes")
async def get_tareas_urgentes() -> str:
    """
    Devuelve las tareas de alta prioridad que no estan completadas.

    Util para obtener rapidamente las tareas que requieren atencion inmediata.
    """
    urgentes = [
        t for t in TAREAS
        if t["prioridad"] == "alta" and t["estado"] != "completada"
    ]

    return json.dumps({
        "total_urgentes": len(urgentes),
        "tareas": urgentes
    }, indent=2, ensure_ascii=False)


# ============================================================================
# PROMPTS (Plantillas)
# Guias predefinidas para tareas comunes con TaskFlow
# ============================================================================

@server.prompt("planificar-sprint")
async def prompt_planificar_sprint(duracion: str = "2 semanas") -> GetPromptResult:
    """
    Genera un prompt para ayudar a planificar un sprint.
    """
    return GetPromptResult(
        description=f"Planificacion de sprint de {duracion}",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Ayudame a planificar un sprint de {duracion} para TaskFlow.

Usa las herramientas disponibles para:
1. Obtener las estadisticas actuales del proyecto
2. Listar las tareas pendientes y en progreso
3. Identificar las tareas urgentes

Con esa informacion, genera un plan de sprint que incluya:
- Tareas a completar en este sprint (priorizadas)
- Distribucion de trabajo sugerida
- Riesgos identificados
- Dependencias entre tareas

Formato: Markdown estructurado"""
                )
            )
        ]
    )


@server.prompt("informe-semanal")
async def prompt_informe_semanal() -> GetPromptResult:
    """
    Genera un prompt para crear un informe semanal de progreso.
    """
    return GetPromptResult(
        description="Informe semanal de progreso de TaskFlow",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text="""Genera un informe semanal de progreso para TaskFlow.

Usa las herramientas disponibles para:
1. Obtener estadisticas generales
2. Listar tareas completadas esta semana
3. Identificar bloqueos o tareas atrasadas

El informe debe incluir:
- Resumen ejecutivo (2-3 lineas)
- Logros de la semana
- Metricas clave (% completado, tareas nuevas vs cerradas)
- Problemas o riesgos identificados
- Prioridades para la proxima semana

Formato: Markdown profesional, listo para compartir con el equipo"""
                )
            )
        ]
    )


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Ejecuta el servidor MCP de TaskFlow."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### 2.5 Configurar en Claude

Ahora debemos decirle a Claude donde encontrar nuestro MCP:

```json
// Windows: %USERPROFILE%\.claude\settings.json
// Mac/Linux: ~/.claude/settings.json
{
  "mcpServers": {
    "taskflow": {
      "command": "python",
      "args": ["C:/ruta/a/TaskFlow/mcp-servers/taskflow-mcp/src/server.py"],
      "env": {
        "PYTHONPATH": "C:/ruta/a/TaskFlow/mcp-servers/taskflow-mcp"
      }
    }
  }
}
```

**Por que PYTHONPATH?** Asegura que Python pueda encontrar todos los modulos de tu proyecto.

### 2.6 Probar el MCP

```bash
# Reiniciar Claude Code para que cargue el nuevo MCP
claude

# Verificar que el MCP esta disponible
/mcp
# Deberia mostrar "taskflow" en la lista

# Probar las herramientas
> "Lista todas las tareas de TaskFlow"
> "Crea una nueva tarea: Implementar sistema de notificaciones, prioridad alta"
> "Muestra las estadisticas del proyecto"
> "Actualiza la tarea 2 a estado completada"
```

---

### Practica Guiada 1: Tu Primer Tool

Crea un nuevo tool llamado `asignar_tarea` que permita asignar una tarea a un usuario:

**Criterios de exito:**
- [ ] El tool recibe `tarea_id` y `email` como parametros
- [ ] Valida que la tarea exista
- [ ] Valida formato basico de email
- [ ] Actualiza el campo `asignado`
- [ ] Devuelve mensaje de confirmacion con los datos

**Pista**: Puedes basarte en `actualizar_tarea` pero simplificando la logica.

---

### Checkpoint 2

Antes de continuar, verifica:

- [ ] Tu servidor MCP se ejecuta sin errores
- [ ] Puedes ver "taskflow" en la lista de MCPs de Claude
- [ ] Al menos un tool funciona correctamente

---

## 3. Crear MCP Server en TypeScript

**Tiempo estimado: 90 minutos**

### 3.1 Por que TypeScript para MCPs?

TypeScript ofrece ventajas diferentes a Python:

1. **Tipado estricto**: Errores detectados en compilacion
2. **Ecosistema npm**: Millones de paquetes disponibles
3. **Performance**: V8 es muy rapido para I/O
4. **Integracion web**: Natural para servicios HTTP

### 3.2 Inicializar Proyecto

**Practica Guiada: Configurar proyecto TypeScript**

```bash
# Crear directorio
mkdir mcp-typescript && cd mcp-typescript

# Inicializar npm
npm init -y

# Instalar dependencias
npm install @modelcontextprotocol/sdk

# Instalar dependencias de desarrollo
npm install -D typescript @types/node tsx
```

### 3.3 tsconfig.json

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

**Por que estas opciones?**
- `target: ES2022`: Soporte para features modernas de JS
- `moduleResolution: NodeNext`: Resolucion correcta de imports con .js
- `strict: true`: Maximo nivel de comprobacion de tipos

### 3.4 package.json

```json
{
  "name": "tareas-mcp-ts",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "bin": {
    "tareas-mcp": "./build/index.js"
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

### 3.5 Implementar el Servidor

```typescript
// src/index.ts
#!/usr/bin/env node

/**
 * TaskFlow MCP Server en TypeScript
 *
 * Este servidor demuestra como crear un MCP en TypeScript
 * con tipado estricto y patrones modernos.
 */

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
// Definimos interfaces para tipado estricto
// ============================================================================

interface Tarea {
  id: number;
  titulo: string;
  descripcion: string;
  estado: "pendiente" | "en_progreso" | "completada";
  prioridad: "baja" | "media" | "alta";
  asignado: string | null;
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
    asignado: "dev@taskflow.com",
    fechaCreacion: "2025-01-01",
  },
  {
    id: 2,
    titulo: "Implementar API",
    descripcion: "Crear endpoints REST para el backend",
    estado: "en_progreso",
    prioridad: "alta",
    asignado: "dev@taskflow.com",
    fechaCreacion: "2025-01-02",
    fechaLimite: "2025-01-15",
  },
  {
    id: 3,
    titulo: "Escribir documentacion",
    descripcion: "Documentar la API y el codigo",
    estado: "pendiente",
    prioridad: "media",
    asignado: null,
    fechaCreacion: "2025-01-03",
  },
];

let nextId = 4;

// ============================================================================
// SERVIDOR
// ============================================================================

const server = new Server(
  {
    name: "taskflow-mcp-ts",
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
// En TypeScript usamos handlers con schemas explicitamente definidos
// ============================================================================

// Handler para listar herramientas disponibles
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "listar_tareas",
      description: "Lista todas las tareas, opcionalmente filtradas por estado o prioridad",
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
      description: "Crea una nueva tarea en TaskFlow",
      inputSchema: {
        type: "object" as const,
        properties: {
          titulo: {
            type: "string",
            description: "Titulo de la tarea",
          },
          descripcion: {
            type: "string",
            description: "Descripcion detallada",
          },
          prioridad: {
            type: "string",
            enum: ["baja", "media", "alta"],
            description: "Nivel de prioridad",
          },
          fechaLimite: {
            type: "string",
            description: "Fecha limite (formato YYYY-MM-DD)",
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
      description: "Elimina una tarea por ID (accion irreversible)",
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
      description: "Obtiene estadisticas generales del proyecto",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
  ],
}));

// Handler para ejecutar herramientas
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "listar_tareas": {
      const { estado, prioridad } = args as {
        estado?: "pendiente" | "en_progreso" | "completada";
        prioridad?: "baja" | "media" | "alta";
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
            text: JSON.stringify(
              { total: resultado.length, tareas: resultado },
              null,
              2
            ),
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
        asignado: null,
        fechaCreacion: new Date().toISOString().split("T")[0],
        fechaLimite,
      };

      tareas.push(nuevaTarea);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              { mensaje: "Tarea creada exitosamente", tarea: nuevaTarea },
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
                mensaje: `Estado actualizado: ${estadoAnterior} -> ${estado}`,
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
        porcentaje_completado:
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
      uri: "taskflow://todas-las-tareas",
      name: "Lista completa de tareas",
      mimeType: "application/json",
    },
    {
      uri: "taskflow://resumen",
      name: "Resumen del proyecto",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "taskflow://todas-las-tareas") {
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

  if (uri === "taskflow://resumen") {
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
          description: "Duracion del sprint en dias",
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
      description: `Planificacion de sprint de ${duracion} dias`,
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Ayudame a planificar un sprint de ${duracion} dias.

Usa las herramientas disponibles para:
1. Listar todas las tareas pendientes y en progreso
2. Obtener las estadisticas actuales
3. Priorizar segun urgencia

Genera un plan que incluya:
- Tareas a completar en este sprint
- Orden de ejecucion sugerido
- Estimacion de tiempo por tarea
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
2. Estadisticas de progreso

El informe debe incluir:
- Resumen ejecutivo (2-3 lineas)
- Progreso general (% completado)
- Tareas destacadas
- Bloqueadores o riesgos
- Proximos pasos

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
  // Nota: Usamos stderr para logs porque stdout se usa para comunicacion MCP
  console.error("Servidor MCP de TaskFlow (TypeScript) iniciado");
}

main().catch(console.error);
```

### 3.6 Compilar y Configurar

```bash
# Compilar TypeScript a JavaScript
npm run build

# Configurar en Claude
```

```json
// settings.json
{
  "mcpServers": {
    "taskflow-ts": {
      "command": "node",
      "args": ["C:/ruta/a/mcp-typescript/build/index.js"]
    }
  }
}
```

---

### Error Comun: console.log rompe la comunicacion MCP

Cuando usas `console.log()` en un servidor MCP con transporte stdio, **rompes la comunicacion** porque stdout esta reservado para JSON-RPC.

**Solucion**: Usa `console.error()` para logs de debugging.

```typescript
// MAL - Rompe el MCP
console.log("Procesando tarea...");

// BIEN - No interfiere con MCP
console.error("Procesando tarea...");
```

---

### Checkpoint 3

Antes de continuar:

- [ ] El proyecto TypeScript compila sin errores (`npm run build`)
- [ ] Puedes ejecutar el servidor (`npm start`)
- [ ] Entiendes la diferencia entre Python SDK y TypeScript SDK

---

## 4. FastMCP para Desarrollo Rapido

**Tiempo estimado: 45 minutos**

### 4.1 Que es FastMCP?

FastMCP es una libreria Python que **reduce drasticamente** el codigo necesario para crear MCPs. Es como Flask para servidores web: minimo boilerplate, maximo resultado.

**Comparativa de codigo**:

| Caracteristica | MCP SDK | FastMCP |
|----------------|---------|---------|
| Lineas para "Hello World" | ~50 | ~10 |
| Definicion de tools | Handlers manuales | Decoradores |
| Schema de parametros | JSON Schema manual | Automatico de type hints |
| Curva de aprendizaje | Moderada | Baja |

### 4.2 Instalacion

```bash
pip install fastmcp
```

### 4.3 Ejemplo: TaskFlow con FastMCP

Veamos como se simplifica nuestro servidor TaskFlow:

```python
# fast_taskflow.py
"""
TaskFlow MCP con FastMCP
Mismo funcionalidad, 70% menos codigo.
"""

from fastmcp import FastMCP
from datetime import datetime
import json

# Crear servidor - Una sola linea!
mcp = FastMCP("TaskFlow Rapido")

# ============================================================================
# DATOS
# ============================================================================

TAREAS = [
    {"id": 1, "titulo": "Tarea inicial", "estado": "pendiente", "prioridad": "alta"},
    {"id": 2, "titulo": "Segunda tarea", "estado": "en_progreso", "prioridad": "media"},
]
_next_id = 3

# ============================================================================
# TOOLS - Nota lo simple que es!
# ============================================================================

@mcp.tool()
def listar_tareas(estado: str = None, prioridad: str = None) -> dict:
    """
    Lista tareas de TaskFlow con filtros opcionales.

    Args:
        estado: Filtrar por estado (pendiente, en_progreso, completada)
        prioridad: Filtrar por prioridad (baja, media, alta)
    """
    resultado = TAREAS.copy()

    if estado:
        resultado = [t for t in resultado if t["estado"] == estado]
    if prioridad:
        resultado = [t for t in resultado if t["prioridad"] == prioridad]

    return {"total": len(resultado), "tareas": resultado}


@mcp.tool()
def crear_tarea(titulo: str, descripcion: str = "", prioridad: str = "media") -> dict:
    """
    Crea una nueva tarea.

    Args:
        titulo: Titulo de la tarea
        descripcion: Descripcion detallada
        prioridad: baja, media o alta
    """
    global _next_id

    nueva = {
        "id": _next_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": "pendiente",
        "prioridad": prioridad,
        "fecha_creacion": datetime.now().isoformat()
    }

    TAREAS.append(nueva)
    _next_id += 1

    return {"mensaje": "Tarea creada", "tarea": nueva}


@mcp.tool()
def actualizar_estado(tarea_id: int, nuevo_estado: str) -> dict:
    """
    Cambia el estado de una tarea.

    Args:
        tarea_id: ID de la tarea
        nuevo_estado: pendiente, en_progreso o completada
    """
    for tarea in TAREAS:
        if tarea["id"] == tarea_id:
            estado_anterior = tarea["estado"]
            tarea["estado"] = nuevo_estado
            return {
                "mensaje": f"Estado cambiado: {estado_anterior} -> {nuevo_estado}",
                "tarea": tarea
            }

    return {"error": f"Tarea {tarea_id} no encontrada"}


@mcp.tool()
def obtener_estadisticas() -> dict:
    """Obtiene estadisticas del proyecto."""
    total = len(TAREAS)
    completadas = len([t for t in TAREAS if t["estado"] == "completada"])

    return {
        "total": total,
        "completadas": completadas,
        "porcentaje": round(completadas / total * 100, 1) if total > 0 else 0,
        "por_estado": {
            "pendiente": len([t for t in TAREAS if t["estado"] == "pendiente"]),
            "en_progreso": len([t for t in TAREAS if t["estado"] == "en_progreso"]),
            "completada": completadas
        }
    }


# ============================================================================
# RESOURCES - Igual de simple
# ============================================================================

@mcp.resource("taskflow://tareas")
def todas_las_tareas() -> str:
    """Todas las tareas en formato JSON."""
    return json.dumps(TAREAS, indent=2)


@mcp.resource("taskflow://resumen")
def resumen_proyecto() -> str:
    """Resumen ejecutivo del proyecto."""
    stats = obtener_estadisticas()
    return json.dumps({
        "fecha": datetime.now().isoformat(),
        "estadisticas": stats
    }, indent=2)


# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    mcp.run()
```

### 4.4 Por que FastMCP Funciona Asi

**Magia de los decoradores**: FastMCP inspecciona tus funciones y:

1. **Extrae el schema** de los type hints (`titulo: str`, `prioridad: str = "media"`)
2. **Genera documentacion** del docstring
3. **Maneja serializacion** automaticamente (puedes devolver `dict` directamente)
4. **Configura el servidor** con valores sensatos por defecto

### 4.5 Configurar FastMCP

```json
{
  "mcpServers": {
    "taskflow-fast": {
      "command": "python",
      "args": ["C:/ruta/a/fast_taskflow.py"]
    }
  }
}
```

---

### Error Comun: Type hints incorrectos

FastMCP genera schemas automaticamente de los type hints. Si no son correctos, Claude recibira informacion erronea.

```python
# MAL - Sin type hints, schema vacio
@mcp.tool()
def buscar(query):
    ...

# BIEN - Type hints claros
@mcp.tool()
def buscar(query: str, limite: int = 10) -> list:
    ...
```

---

### Practica Guiada 2: Migrar a FastMCP

Toma el servidor Python completo de la seccion 2 y migrar a FastMCP:

**Criterios de exito:**
- [ ] Todas las tools funcionan igual que antes
- [ ] Al menos un resource funciona
- [ ] El codigo tiene menos de 100 lineas

---

## 5. Servidor MCP con HTTP Transport

**Tiempo estimado: 60 minutos**

### 5.1 Cuando Usar HTTP en Lugar de stdio

**stdio** (estandar input/output):
- El MCP corre como proceso local
- Claude lo inicia y para directamente
- Ideal para: desarrollo local, herramientas personales

**HTTP/SSE** (Server-Sent Events):
- El MCP corre como servicio web
- Puede estar en otro servidor
- Ideal para: produccion, equipos, MCPs compartidos

### 5.2 Arquitectura HTTP

```
┌─────────────────┐         HTTP/SSE          ┌─────────────────┐
│  Claude Code    │ <-----------------------> │  MCP Server     │
│  (Cliente)      │                           │  (Remoto)       │
└─────────────────┘                           └─────────────────┘
                                                     │
                                              ┌──────┴──────┐
                                              │  Tu logica  │
                                              │  de negocio │
                                              └─────────────┘
```

### 5.3 Implementacion con Express (TypeScript)

```typescript
// src/http-server.ts
import express from "express";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const app = express();
app.use(express.json());

// Almacenar sesiones activas
// Por que Map? Permite multiples clientes conectados simultaneamente
const sessions = new Map<string, SSEServerTransport>();

// Crear servidor MCP
const mcpServer = new Server(
  { name: "taskflow-http", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Configurar tools (igual que antes)
mcpServer.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "ping",
      description: "Verifica que el servidor esta funcionando",
      inputSchema: { type: "object" as const, properties: {} },
    },
    // ... mas tools
  ],
}));

mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "ping") {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            status: "ok",
            timestamp: new Date().toISOString(),
            sessions_activas: sessions.size,
          }),
        },
      ],
    };
  }
  throw new Error(`Tool no encontrado: ${request.params.name}`);
});

// ============================================================================
// ENDPOINTS HTTP
// ============================================================================

// Endpoint SSE para conexiones
// Por que SSE? Permite comunicacion bidireccional sobre HTTP
app.get("/sse", async (req, res) => {
  // Generar ID de sesion
  const sessionId = (req.query.sessionId as string) || crypto.randomUUID();

  // Configurar headers para SSE
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("Access-Control-Allow-Origin", "*");

  // Crear transport SSE
  const transport = new SSEServerTransport("/messages", res);
  sessions.set(sessionId, transport);

  // Conectar servidor MCP
  await mcpServer.connect(transport);

  console.error(`Nueva sesion: ${sessionId} (Total: ${sessions.size})`);

  // Limpiar al desconectar
  req.on("close", () => {
    sessions.delete(sessionId);
    console.error(`Sesion cerrada: ${sessionId} (Total: ${sessions.size})`);
  });
});

// Endpoint para mensajes JSON-RPC
app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId as string;
  const transport = sessions.get(sessionId);

  if (!transport) {
    return res.status(404).json({
      error: "Sesion no encontrada",
      hint: "Conecta primero a /sse?sessionId=tu-id",
    });
  }

  await transport.handlePostMessage(req, res);
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    uptime: process.uptime(),
    sessions: sessions.size,
  });
});

// ============================================================================
// INICIAR SERVIDOR
// ============================================================================

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.error(`
╔══════════════════════════════════════════════════════════╗
║  TaskFlow MCP HTTP Server                                ║
╠══════════════════════════════════════════════════════════╣
║  URL:      http://localhost:${PORT}                        ║
║  SSE:      http://localhost:${PORT}/sse                    ║
║  Messages: http://localhost:${PORT}/messages               ║
║  Health:   http://localhost:${PORT}/health                 ║
╚══════════════════════════════════════════════════════════╝
  `);
});
```

### 5.4 Configurar Cliente para Servidor Remoto

```json
{
  "mcpServers": {
    "taskflow-remoto": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:3000/sse"]
    }
  }
}
```

**Nota**: `mcp-remote` es un cliente que hace de puente entre Claude (que espera stdio) y tu servidor HTTP.

### 5.5 Consideraciones de Produccion

Para desplegar un MCP HTTP en produccion:

```typescript
// Agregar autenticacion
app.use((req, res, next) => {
  const apiKey = req.headers["x-api-key"];
  if (apiKey !== process.env.MCP_API_KEY) {
    return res.status(401).json({ error: "API key invalida" });
  }
  next();
});

// Rate limiting
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 100, // 100 requests por minuto
});

app.use(limiter);

// HTTPS obligatorio
if (process.env.NODE_ENV === "production") {
  app.use((req, res, next) => {
    if (!req.secure) {
      return res.redirect(`https://${req.headers.host}${req.url}`);
    }
    next();
  });
}
```

---

## 6. Testing y Debugging

**Tiempo estimado: 45 minutos**

### 6.1 MCP Inspector: Tu Mejor Amigo

El Inspector es la herramienta oficial para probar MCPs sin necesidad de Claude.

```bash
# Instalar globalmente
npm install -g @modelcontextprotocol/inspector

# Probar servidor Python
npx @modelcontextprotocol/inspector python src/server.py

# Probar servidor TypeScript
npx @modelcontextprotocol/inspector node build/index.js
```

**Que puedes hacer con el Inspector?**
- Ver todas las tools disponibles
- Ejecutar tools con argumentos personalizados
- Ver resources y su contenido
- Ejecutar prompts
- Ver logs de comunicacion JSON-RPC

### 6.2 Tests Unitarios en Python

```python
# tests/test_server.py
"""
Tests para el servidor MCP de TaskFlow.

Ejecutar con: pytest tests/ -v
"""

import pytest
import json
from src.server import (
    listar_tareas,
    crear_tarea,
    actualizar_tarea,
    eliminar_tarea,
    TAREAS
)

# Fixture para resetear datos entre tests
@pytest.fixture(autouse=True)
def reset_tareas():
    """Restaura las tareas al estado inicial antes de cada test."""
    global TAREAS
    TAREAS.clear()
    TAREAS.extend([
        {"id": 1, "titulo": "Test", "estado": "pendiente", "prioridad": "alta"},
        {"id": 2, "titulo": "Test 2", "estado": "completada", "prioridad": "baja"},
    ])
    yield


class TestListarTareas:
    """Tests para la herramienta listar_tareas."""

    @pytest.mark.asyncio
    async def test_lista_todas(self):
        """Debe listar todas las tareas sin filtros."""
        resultado = await listar_tareas()
        datos = json.loads(resultado)

        assert datos["total"] == 2
        assert len(datos["tareas"]) == 2

    @pytest.mark.asyncio
    async def test_filtrar_por_estado(self):
        """Debe filtrar correctamente por estado."""
        resultado = await listar_tareas(estado="pendiente")
        datos = json.loads(resultado)

        assert datos["total"] == 1
        assert datos["tareas"][0]["estado"] == "pendiente"

    @pytest.mark.asyncio
    async def test_filtrar_por_prioridad(self):
        """Debe filtrar correctamente por prioridad."""
        resultado = await listar_tareas(prioridad="alta")
        datos = json.loads(resultado)

        assert all(t["prioridad"] == "alta" for t in datos["tareas"])


class TestCrearTarea:
    """Tests para la herramienta crear_tarea."""

    @pytest.mark.asyncio
    async def test_crear_tarea_basica(self):
        """Debe crear una tarea con datos minimos."""
        resultado = await crear_tarea(
            titulo="Nueva tarea",
            descripcion="Descripcion de prueba"
        )
        datos = json.loads(resultado)

        assert "tarea" in datos
        assert datos["tarea"]["titulo"] == "Nueva tarea"
        assert datos["tarea"]["estado"] == "pendiente"

    @pytest.mark.asyncio
    async def test_crear_tarea_con_prioridad(self):
        """Debe respetar la prioridad especificada."""
        resultado = await crear_tarea(
            titulo="Urgente",
            descripcion="Muy importante",
            prioridad="alta"
        )
        datos = json.loads(resultado)

        assert datos["tarea"]["prioridad"] == "alta"

    @pytest.mark.asyncio
    async def test_crear_tarea_titulo_vacio(self):
        """Debe rechazar titulo vacio."""
        resultado = await crear_tarea(titulo="", descripcion="algo")
        datos = json.loads(resultado)

        assert "error" in datos


class TestActualizarTarea:
    """Tests para la herramienta actualizar_tarea."""

    @pytest.mark.asyncio
    async def test_actualizar_estado(self):
        """Debe actualizar el estado correctamente."""
        resultado = await actualizar_tarea(tarea_id=1, estado="completada")
        datos = json.loads(resultado)

        assert "cambios" in datos
        assert datos["tarea"]["estado"] == "completada"

    @pytest.mark.asyncio
    async def test_tarea_no_existe(self):
        """Debe retornar error si la tarea no existe."""
        resultado = await actualizar_tarea(tarea_id=999, estado="completada")
        datos = json.loads(resultado)

        assert "error" in datos


class TestEliminarTarea:
    """Tests para la herramienta eliminar_tarea."""

    @pytest.mark.asyncio
    async def test_eliminar_existente(self):
        """Debe eliminar tarea existente."""
        resultado = await eliminar_tarea(tarea_id=1)
        datos = json.loads(resultado)

        assert "tarea_eliminada" in datos
        assert len(TAREAS) == 1

    @pytest.mark.asyncio
    async def test_eliminar_no_existente(self):
        """Debe retornar error si no existe."""
        resultado = await eliminar_tarea(tarea_id=999)
        datos = json.loads(resultado)

        assert "error" in datos
```

### 6.3 Tests en TypeScript

```typescript
// tests/server.test.ts
import { describe, it, expect, beforeEach } from "vitest";

// Importar funciones a testear
// Nota: En un proyecto real, exportarias las funciones de logica
// separadas de los handlers MCP

interface Tarea {
  id: number;
  titulo: string;
  estado: "pendiente" | "en_progreso" | "completada";
  prioridad: "baja" | "media" | "alta";
}

let tareas: Tarea[] = [];

beforeEach(() => {
  tareas = [
    { id: 1, titulo: "Test 1", estado: "pendiente", prioridad: "alta" },
    { id: 2, titulo: "Test 2", estado: "completada", prioridad: "baja" },
  ];
});

describe("Filtrado de tareas", () => {
  it("debe filtrar por estado", () => {
    const resultado = tareas.filter((t) => t.estado === "pendiente");

    expect(resultado).toHaveLength(1);
    expect(resultado[0].id).toBe(1);
  });

  it("debe filtrar por prioridad", () => {
    const resultado = tareas.filter((t) => t.prioridad === "alta");

    expect(resultado).toHaveLength(1);
    expect(resultado.every((t) => t.prioridad === "alta")).toBe(true);
  });

  it("debe permitir multiples filtros", () => {
    const resultado = tareas.filter(
      (t) => t.estado === "pendiente" && t.prioridad === "alta"
    );

    expect(resultado).toHaveLength(1);
  });
});

describe("Creacion de tareas", () => {
  it("debe asignar ID incrementales", () => {
    const maxId = Math.max(...tareas.map((t) => t.id));
    const nuevaTarea: Tarea = {
      id: maxId + 1,
      titulo: "Nueva",
      estado: "pendiente",
      prioridad: "media",
    };

    tareas.push(nuevaTarea);

    expect(tareas).toHaveLength(3);
    expect(nuevaTarea.id).toBe(3);
  });
});

describe("Estadisticas", () => {
  it("debe calcular porcentaje completado", () => {
    const completadas = tareas.filter((t) => t.estado === "completada").length;
    const porcentaje = Math.round((completadas / tareas.length) * 100);

    expect(porcentaje).toBe(50);
  });
});
```

```bash
# Ejecutar tests con vitest
npm install -D vitest
npx vitest
```

### 6.4 Logging Efectivo

```python
# Agregar logging a tu servidor
import logging
import sys

# Configurar logging a stderr (stdout esta reservado para MCP)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr),  # Importante: stderr, no stdout!
        logging.FileHandler("mcp-server.log")
    ]
)

logger = logging.getLogger("taskflow-mcp")

@server.tool()
async def mi_tool(param: str) -> str:
    logger.info(f"Tool invocado con param={param}")

    try:
        resultado = procesar(param)
        logger.debug(f"Resultado: {resultado}")
        return resultado

    except Exception as e:
        logger.error(f"Error procesando: {e}", exc_info=True)
        return json.dumps({"error": str(e)})
```

---

### Error Comun: Tests que modifican estado global

Si tus tests modifican datos globales sin restaurarlos, los tests se afectan entre si.

```python
# MAL - Los tests dependen del orden de ejecucion
def test_crear():
    crear_tarea("Nueva")

def test_contar():
    # Puede fallar si test_crear se ejecuto antes
    assert len(TAREAS) == 2


# BIEN - Cada test tiene su propio estado
@pytest.fixture(autouse=True)
def reset_estado():
    TAREAS.clear()
    TAREAS.extend([...datos iniciales...])
    yield  # Test se ejecuta aqui
    # Cleanup automatico
```

---

## 7. Troubleshooting

**Tiempo estimado: 30 minutos de lectura, referencia continua**

### 7.1 Problemas de Conexion

**Problema**: Claude no encuentra el MCP

```
Error: MCP server "taskflow" failed to start
```

**Soluciones**:
1. Verifica la ruta en `settings.json` (usar rutas absolutas)
2. Comprueba que el comando existe (`python --version`, `node --version`)
3. Verifica permisos de ejecucion del script
4. Revisa logs de Claude: `~/.claude/logs/`

**Problema**: El MCP se inicia pero no responde

**Diagnoistico**:
```bash
# Probar manualmente
python src/server.py
# Debe quedarse esperando (no terminar)

# Si termina inmediatamente, hay un error de sintaxis
python -c "import src.server"
```

### 7.2 Problemas de Comunicacion

**Problema**: Tools no aparecen en Claude

**Causa comun**: Error en el handler de `tools/list`

```python
# Verificar que el handler esta registrado
@server.tool()  # Este decorador es necesario!
async def mi_tool():
    ...
```

**Problema**: Tool falla silenciosamente

**Causa comun**: Excepcion no manejada

```python
# ANTES: Excepcion se pierde
@server.tool()
async def mi_tool(x: int) -> str:
    resultado = 10 / x  # Division by zero si x=0
    return str(resultado)

# DESPUES: Excepcion se reporta
@server.tool()
async def mi_tool(x: int) -> str:
    try:
        resultado = 10 / x
        return str(resultado)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

### 7.3 Problemas de Datos

**Problema**: JSON malformado en respuesta

```python
# MAL - Puede fallar con caracteres especiales
return str(datos)

# BIEN - JSON siempre valido
return json.dumps(datos, ensure_ascii=False)
```

**Problema**: Tipos de datos incorrectos

```python
# MAL - Devuelve int, MCP espera string
@server.tool()
async def contar() -> int:
    return len(TAREAS)

# BIEN - Devuelve string (JSON)
@server.tool()
async def contar() -> str:
    return json.dumps({"total": len(TAREAS)})
```

### 7.4 Tabla de Diagnostico Rapido

| Sintoma | Causa Probable | Solucion |
|---------|---------------|----------|
| MCP no aparece en `/mcp` | Ruta incorrecta en config | Verificar settings.json |
| Error al iniciar | Dependencias faltantes | `pip install -r requirements.txt` |
| Tools no aparecen | Decorador faltante | Agregar `@server.tool()` |
| Tool devuelve null | Excepcion no manejada | Agregar try/except |
| JSON invalido | Serializacion incorrecta | Usar `json.dumps()` |
| Timeout | Operacion muy lenta | Agregar async/await correctos |

---

## 8. Ejercicios Practicos

### Ejercicio 1: MCP de Notas (Nivel: Basico)

**Objetivo**: Crear un servidor MCP para gestion de notas personales.

**Requisitos**:
- Tools: `crear_nota`, `buscar_notas`, `editar_nota`, `eliminar_nota`
- Resources: `notas://todas`, `notas://recientes`
- Prompt: `organizar-notas`

**Criterios de exito**:
- [ ] El MCP se conecta correctamente a Claude
- [ ] Se pueden crear notas con titulo y contenido
- [ ] La busqueda funciona por titulo y contenido
- [ ] Los resources devuelven datos validos

**Dificultad**: 2/5
**Tiempo estimado**: 60-90 minutos

---

### Ejercicio 2: MCP de API Externa (Nivel: Intermedio)

**Objetivo**: Crear un MCP que se conecte a una API REST externa.

**Opciones**:
- OpenWeatherMap (clima)
- NewsAPI (noticias)
- JSONPlaceholder (pruebas)

**Requisitos**:
- Manejo de errores de red
- Caching basico de respuestas
- Rate limiting

**Criterios de exito**:
- [ ] Conexion exitosa a la API externa
- [ ] Manejo correcto de errores de red
- [ ] Respuestas cacheadas cuando es apropiado
- [ ] Tests unitarios con mocks

**Dificultad**: 3/5
**Tiempo estimado**: 2-3 horas

---

### Ejercicio 3: MCP con Base de Datos (Nivel: Intermedio-Avanzado)

**Objetivo**: Crear un MCP con persistencia en SQLite.

**Requisitos**:
- CRUD completo para tareas
- Migraciones de schema
- Backup automatico

**Criterios de exito**:
- [ ] Datos persisten entre reinicios del servidor
- [ ] Schema actualizable con migraciones
- [ ] Backup automatico funcional
- [ ] Tests de integracion

**Dificultad**: 4/5
**Tiempo estimado**: 3-4 horas

---

### Ejercicio 4: MCP TaskFlow Completo (Nivel: Avanzado)

**Objetivo**: Integrar el MCP con el proyecto TaskFlow real.

**Requisitos**:
- Conexion a la base de datos de TaskFlow
- Sincronizacion con la API existente
- Notificaciones de cambios

**Criterios de exito**:
- [ ] Lee datos reales de TaskFlow
- [ ] Los cambios via MCP se reflejan en TaskFlow
- [ ] Manejo de conflictos de concurrencia
- [ ] Documentacion completa

**Dificultad**: 5/5
**Tiempo estimado**: 4-6 horas

---

### Ejercicio 5: Publicar MCP (Nivel: Avanzado)

**Objetivo**: Empaquetar y publicar tu MCP.

**Para Python (PyPI)**:
```bash
# Estructura
mi-mcp/
├── pyproject.toml
├── src/
│   └── mi_mcp/
│       ├── __init__.py
│       └── server.py
└── README.md
```

**Para TypeScript (npm)**:
```bash
# Estructura
mi-mcp/
├── package.json
├── src/
│   └── index.ts
├── build/
└── README.md
```

**Criterios de exito**:
- [ ] Paquete publicado en PyPI o npm
- [ ] README con instrucciones claras
- [ ] CI/CD configurado
- [ ] Version semantica

**Dificultad**: 4/5
**Tiempo estimado**: 2-3 horas

---

## 9. Resumen y Preparacion para el Modulo 6

### Lo que Aprendiste en Este Modulo

1. **Arquitectura MCP**: Entiendes los componentes (Transport, Protocol, Tools, Resources, Prompts) y el flujo JSON-RPC

2. **Desarrollo en Python**: Puedes crear MCPs completos con el SDK oficial, incluyendo tools, resources y prompts

3. **Desarrollo en TypeScript**: Conoces las diferencias con Python y puedes elegir el lenguaje apropiado

4. **FastMCP**: Sabes cuando usar FastMCP para desarrollo rapido vs SDK completo

5. **HTTP Transport**: Puedes crear MCPs remotos para produccion

6. **Testing**: Conoces las estrategias de testing y debugging

### Checklist de Competencias

Antes de pasar al Modulo 6, verifica:

- [ ] Puedo explicar la diferencia entre Tool, Resource y Prompt
- [ ] He creado al menos un MCP funcional (Python o TypeScript)
- [ ] Se como configurar un MCP en Claude (`settings.json`)
- [ ] Puedo usar MCP Inspector para debugging
- [ ] Entiendo cuando usar stdio vs HTTP transport
- [ ] He escrito al menos un test para mi MCP

### Preparacion para el Modulo 6

El **Modulo 6: Arquitectura de Desarrollo Asistido por IA** construira sobre lo aprendido:

**Temas que vendra**:
- Patrones de arquitectura con MCPs
- Orquestacion de multiples agentes
- Pipelines CI/CD asistidos por IA
- Casos practicos completos

**Antes del Modulo 6**:
1. Asegurate de tener tu MCP TaskFlow funcionando
2. Practica usando los MCPs que creaste
3. Revisa los patrones de arquitectura basicos (en la documentacion oficial)

---

## Recursos Adicionales

- [MCP SDK Python](https://github.com/modelcontextprotocol/python-sdk)
- [MCP SDK TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [MCP Specification](https://modelcontextprotocol.io/docs)
- [Ejemplos Oficiales](https://github.com/modelcontextprotocol/servers)

---

**Siguiente Modulo**: [Modulo 6: Arquitectura de Desarrollo Asistido por IA](../Modulo%206%20Arquitectura%20IA/Teoria%206.md)
