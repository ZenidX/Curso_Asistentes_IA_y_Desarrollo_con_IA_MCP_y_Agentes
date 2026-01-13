"""
Function Calling / Tool Use con APIs de IA
==========================================

Function calling permite que los modelos de IA:
1. Identifiquen cuándo necesitan usar una herramienta
2. Generen los parámetros correctos para la función
3. Integren el resultado en su respuesta

Casos de uso:
- Consultar bases de datos
- Llamar a APIs externas
- Realizar cálculos complejos
- Interactuar con sistemas
"""

import yaml
import json
from pathlib import Path
from openai import OpenAI
import anthropic


def cargar_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# =============================================================================
# FUNCIONES SIMULADAS (en producción, estas harían llamadas reales)
# =============================================================================

def obtener_clima(ciudad: str, unidad: str = "celsius") -> dict:
    """Simula obtener el clima de una ciudad."""
    # En producción, esto llamaría a una API de clima real
    climas_simulados = {
        "madrid": {"temp": 22, "condicion": "soleado", "humedad": 45},
        "barcelona": {"temp": 25, "condicion": "parcialmente nublado", "humedad": 60},
        "sevilla": {"temp": 30, "condicion": "soleado", "humedad": 35},
        "bilbao": {"temp": 18, "condicion": "lluvia ligera", "humedad": 80},
    }

    ciudad_lower = ciudad.lower()
    if ciudad_lower in climas_simulados:
        clima = climas_simulados[ciudad_lower]
        temp = clima["temp"]
        if unidad == "fahrenheit":
            temp = temp * 9/5 + 32
        return {
            "ciudad": ciudad,
            "temperatura": temp,
            "unidad": unidad,
            "condicion": clima["condicion"],
            "humedad": clima["humedad"]
        }
    return {"error": f"No hay datos para {ciudad}"}


def buscar_producto(nombre: str, categoria: str = None, precio_max: float = None) -> list:
    """Simula buscar productos en una tienda."""
    productos = [
        {"id": 1, "nombre": "Laptop Pro", "categoria": "electrónica", "precio": 999.99},
        {"id": 2, "nombre": "Laptop Basic", "categoria": "electrónica", "precio": 499.99},
        {"id": 3, "nombre": "Auriculares Bluetooth", "categoria": "electrónica", "precio": 79.99},
        {"id": 4, "nombre": "Silla Ergonómica", "categoria": "oficina", "precio": 299.99},
        {"id": 5, "nombre": "Monitor 27\"", "categoria": "electrónica", "precio": 349.99},
    ]

    resultados = []
    for p in productos:
        if nombre.lower() in p["nombre"].lower():
            if categoria and p["categoria"] != categoria:
                continue
            if precio_max and p["precio"] > precio_max:
                continue
            resultados.append(p)

    return resultados


def calcular(operacion: str, a: float, b: float) -> dict:
    """Realiza operaciones matemáticas."""
    operaciones = {
        "suma": a + b,
        "resta": a - b,
        "multiplicacion": a * b,
        "division": a / b if b != 0 else "Error: división por cero",
        "potencia": a ** b,
    }

    if operacion in operaciones:
        return {"operacion": operacion, "a": a, "b": b, "resultado": operaciones[operacion]}
    return {"error": f"Operación '{operacion}' no soportada"}


# =============================================================================
# DEFINICIÓN DE HERRAMIENTAS PARA LAS APIs
# =============================================================================

# Formato OpenAI
TOOLS_OPENAI = [
    {
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": "Obtiene el clima actual de una ciudad",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad (ej: Madrid, Barcelona)"
                    },
                    "unidad": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Unidad de temperatura"
                    }
                },
                "required": ["ciudad"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_producto",
            "description": "Busca productos en la tienda por nombre",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre o parte del nombre del producto"
                    },
                    "categoria": {
                        "type": "string",
                        "description": "Categoría del producto (electrónica, oficina, etc.)"
                    },
                    "precio_max": {
                        "type": "number",
                        "description": "Precio máximo en euros"
                    }
                },
                "required": ["nombre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular",
            "description": "Realiza operaciones matemáticas",
            "parameters": {
                "type": "object",
                "properties": {
                    "operacion": {
                        "type": "string",
                        "enum": ["suma", "resta", "multiplicacion", "division", "potencia"],
                        "description": "Tipo de operación"
                    },
                    "a": {"type": "number", "description": "Primer operando"},
                    "b": {"type": "number", "description": "Segundo operando"}
                },
                "required": ["operacion", "a", "b"]
            }
        }
    }
]

# Formato Anthropic
TOOLS_ANTHROPIC = [
    {
        "name": "obtener_clima",
        "description": "Obtiene el clima actual de una ciudad",
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {"type": "string", "description": "Nombre de la ciudad"},
                "unidad": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["ciudad"]
        }
    },
    {
        "name": "buscar_producto",
        "description": "Busca productos en la tienda por nombre",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string", "description": "Nombre del producto"},
                "categoria": {"type": "string"},
                "precio_max": {"type": "number"}
            },
            "required": ["nombre"]
        }
    },
    {
        "name": "calcular",
        "description": "Realiza operaciones matemáticas",
        "input_schema": {
            "type": "object",
            "properties": {
                "operacion": {"type": "string", "enum": ["suma", "resta", "multiplicacion", "division", "potencia"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operacion", "a", "b"]
        }
    }
]


def ejecutar_funcion(nombre: str, argumentos: dict) -> str:
    """Ejecuta una función por nombre y devuelve el resultado."""
    funciones = {
        "obtener_clima": obtener_clima,
        "buscar_producto": buscar_producto,
        "calcular": calcular
    }

    if nombre in funciones:
        resultado = funciones[nombre](**argumentos)
        return json.dumps(resultado, ensure_ascii=False)
    return json.dumps({"error": f"Función '{nombre}' no encontrada"})


def function_calling_openai(prompt: str, config: dict):
    """Demuestra function calling con OpenAI."""
    print("\n" + "=" * 60)
    print("🤖 OPENAI - Function Calling")
    print("=" * 60)

    client = OpenAI(api_key=config["apis"]["openai"]["api_key"])
    modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")

    print(f"Modelo: {modelo}")
    print(f"Prompt: {prompt}\n")

    messages = [
        {"role": "system", "content": "Eres un asistente útil. Usa las herramientas disponibles para responder."},
        {"role": "user", "content": prompt}
    ]

    # Primera llamada: el modelo decide si usar herramientas
    response = client.chat.completions.create(
        model=modelo,
        messages=messages,
        tools=TOOLS_OPENAI,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # Verificar si el modelo quiere usar herramientas
    if assistant_message.tool_calls:
        print("🔧 El modelo quiere usar herramientas:")

        # Agregar mensaje del asistente
        messages.append(assistant_message)

        # Procesar cada llamada a herramienta
        for tool_call in assistant_message.tool_calls:
            nombre_funcion = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments)

            print(f"   → {nombre_funcion}({argumentos})")

            # Ejecutar la función
            resultado = ejecutar_funcion(nombre_funcion, argumentos)
            print(f"   ← Resultado: {resultado}")

            # Agregar resultado al contexto
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": resultado
            })

        # Segunda llamada: el modelo genera respuesta final
        print("\n📝 Generando respuesta final...")
        response_final = client.chat.completions.create(
            model=modelo,
            messages=messages
        )

        respuesta = response_final.choices[0].message.content
    else:
        # El modelo respondió directamente sin usar herramientas
        respuesta = assistant_message.content

    print(f"\n💬 Respuesta:\n{respuesta}")


def function_calling_anthropic(prompt: str, config: dict):
    """Demuestra function calling (tool use) con Anthropic."""
    print("\n" + "=" * 60)
    print("🤖 ANTHROPIC - Tool Use")
    print("=" * 60)

    client = anthropic.Anthropic(api_key=config["apis"]["anthropic"]["api_key"])
    modelo = config["apis"]["anthropic"].get("default_model", "claude-3-haiku-20240307")

    print(f"Modelo: {modelo}")
    print(f"Prompt: {prompt}\n")

    messages = [{"role": "user", "content": prompt}]

    # Primera llamada
    response = client.messages.create(
        model=modelo,
        max_tokens=1024,
        system="Eres un asistente útil. Usa las herramientas disponibles para responder.",
        tools=TOOLS_ANTHROPIC,
        messages=messages
    )

    # Procesar la respuesta
    while response.stop_reason == "tool_use":
        # Encontrar el bloque de tool_use
        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use_block = block
                break

        if tool_use_block:
            nombre_funcion = tool_use_block.name
            argumentos = tool_use_block.input

            print(f"🔧 Herramienta: {nombre_funcion}({argumentos})")

            # Ejecutar función
            resultado = ejecutar_funcion(nombre_funcion, argumentos)
            print(f"   ← Resultado: {resultado}")

            # Agregar al contexto
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": resultado
                }]
            })

            # Siguiente llamada
            response = client.messages.create(
                model=modelo,
                max_tokens=1024,
                system="Eres un asistente útil. Usa las herramientas disponibles para responder.",
                tools=TOOLS_ANTHROPIC,
                messages=messages
            )

    # Extraer respuesta final
    respuesta = ""
    for block in response.content:
        if hasattr(block, "text"):
            respuesta += block.text

    print(f"\n💬 Respuesta:\n{respuesta}")


def main():
    print("=" * 60)
    print("FUNCTION CALLING / TOOL USE")
    print("=" * 60)
    print("Function calling permite a los modelos usar herramientas")
    print("como consultar APIs, bases de datos o hacer cálculos.")

    # Cargar configuración
    try:
        config = cargar_config()
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar APIs disponibles
    apis_disponibles = []

    api_key = config["apis"]["openai"]["api_key"]
    if api_key.startswith("sk-") and "tu-api-key" not in api_key:
        apis_disponibles.append(("OpenAI", function_calling_openai))

    api_key = config["apis"]["anthropic"]["api_key"]
    if api_key.startswith("sk-ant") and "tu-api-key" not in api_key:
        apis_disponibles.append(("Anthropic", function_calling_anthropic))

    if not apis_disponibles:
        print("✗ Se requiere OpenAI o Anthropic para este ejemplo.")
        return

    print(f"\n✓ APIs disponibles: {', '.join([a[0] for a in apis_disponibles])}")

    # Ejemplos de prompts
    print("\n📝 Ejemplos de prompts para probar:")
    print("   1. \"¿Qué tiempo hace en Madrid?\"")
    print("   2. \"Busca laptops con precio menor a 600 euros\"")
    print("   3. \"¿Cuánto es 15 elevado a la 3?\"")
    print("   4. \"¿Qué tiempo hace en Barcelona y cuánto cuesta un monitor?\"")

    prompt = input("\nIntroduce tu prompt: ").strip()
    if not prompt:
        prompt = "¿Qué tiempo hace en Madrid y cuánto es 25 * 4?"

    # Ejecutar con cada API disponible
    for nombre, func in apis_disponibles:
        try:
            func(prompt, config)
        except Exception as e:
            print(f"\n✗ Error con {nombre}: {e}")


if __name__ == "__main__":
    main()
