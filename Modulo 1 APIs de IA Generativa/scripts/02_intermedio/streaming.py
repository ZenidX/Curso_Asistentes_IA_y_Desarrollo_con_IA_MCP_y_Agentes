"""
Streaming de respuestas con diferentes APIs
============================================

Este script demuestra cómo recibir respuestas en streaming,
es decir, token por token en tiempo real, en lugar de esperar
a que se genere toda la respuesta.

Ventajas del streaming:
- Mejor experiencia de usuario (respuesta inmediata)
- Útil para respuestas largas
- Permite cancelar si la respuesta no es útil
"""

import yaml
import sys
from pathlib import Path

from openai import OpenAI
import anthropic
import google.generativeai as genai
import ollama


def cargar_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def streaming_openai(prompt: str, config: dict):
    """Streaming con OpenAI."""
    print("\n" + "=" * 60)
    print("🤖 OPENAI - Streaming")
    print("=" * 60)

    client = OpenAI(api_key=config["apis"]["openai"]["api_key"])
    modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")

    print(f"Modelo: {modelo}")
    print(f"Prompt: {prompt}\n")
    print("Respuesta: ", end="", flush=True)

    # Crear stream
    stream = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Responde en español."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        stream=True  # Activar streaming
    )

    # Procesar tokens conforme llegan
    respuesta_completa = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            contenido = chunk.choices[0].delta.content
            print(contenido, end="", flush=True)
            respuesta_completa += contenido

    print("\n")
    return respuesta_completa


def streaming_anthropic(prompt: str, config: dict):
    """Streaming con Anthropic Claude."""
    print("\n" + "=" * 60)
    print("🤖 ANTHROPIC CLAUDE - Streaming")
    print("=" * 60)

    client = anthropic.Anthropic(api_key=config["apis"]["anthropic"]["api_key"])
    modelo = config["apis"]["anthropic"].get("default_model", "claude-3-haiku-20240307")

    print(f"Modelo: {modelo}")
    print(f"Prompt: {prompt}\n")
    print("Respuesta: ", end="", flush=True)

    # Crear stream
    respuesta_completa = ""
    with client.messages.stream(
        model=modelo,
        max_tokens=500,
        system="Responde en español.",
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            respuesta_completa += text

    print("\n")
    return respuesta_completa


def streaming_google(prompt: str, config: dict):
    """Streaming con Google Gemini."""
    print("\n" + "=" * 60)
    print("🤖 GOOGLE GEMINI - Streaming")
    print("=" * 60)

    genai.configure(api_key=config["apis"]["google"]["api_key"])
    modelo_nombre = config["apis"]["google"].get("default_model", "gemini-1.5-flash")

    modelo = genai.GenerativeModel(
        model_name=modelo_nombre,
        system_instruction="Responde en español."
    )

    print(f"Modelo: {modelo_nombre}")
    print(f"Prompt: {prompt}\n")
    print("Respuesta: ", end="", flush=True)

    # Crear stream
    respuesta_completa = ""
    response = modelo.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            respuesta_completa += chunk.text

    print("\n")
    return respuesta_completa


def streaming_ollama(prompt: str, config: dict):
    """Streaming con Ollama (local)."""
    print("\n" + "=" * 60)
    print("🤖 OLLAMA (LOCAL) - Streaming")
    print("=" * 60)

    modelo = config["apis"]["ollama"].get("default_model", "llama3.2")

    print(f"Modelo: {modelo}")
    print(f"Prompt: {prompt}\n")
    print("Respuesta: ", end="", flush=True)

    # Crear stream
    respuesta_completa = ""
    stream = ollama.chat(
        model=modelo,
        messages=[
            {"role": "system", "content": "Responde en español."},
            {"role": "user", "content": prompt}
        ],
        stream=True  # Activar streaming
    )

    for chunk in stream:
        contenido = chunk["message"]["content"]
        print(contenido, end="", flush=True)
        respuesta_completa += contenido

    print("\n")
    return respuesta_completa


def verificar_apis_disponibles(config: dict) -> dict:
    """Verifica qué APIs están configuradas."""
    disponibles = {}

    api_key = config["apis"]["openai"]["api_key"]
    if api_key.startswith("sk-") and "tu-api-key" not in api_key:
        disponibles["openai"] = streaming_openai

    api_key = config["apis"]["anthropic"]["api_key"]
    if api_key.startswith("sk-ant") and "tu-api-key" not in api_key:
        disponibles["anthropic"] = streaming_anthropic

    api_key = config["apis"]["google"]["api_key"]
    if len(api_key) > 10 and "tu-api-key" not in api_key:
        disponibles["google"] = streaming_google

    try:
        ollama.list()
        disponibles["ollama"] = streaming_ollama
    except Exception:
        pass

    return disponibles


def main():
    print("=" * 60)
    print("STREAMING DE RESPUESTAS")
    print("=" * 60)
    print("El streaming muestra la respuesta token por token,")
    print("en tiempo real, en lugar de esperar a que termine.")

    # Cargar configuración
    try:
        config = cargar_config()
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar APIs disponibles
    apis = verificar_apis_disponibles(config)

    if not apis:
        print("✗ No hay APIs configuradas.")
        return

    print(f"\n✓ APIs disponibles: {', '.join(apis.keys())}")

    # Prompt
    prompt = input("\n📝 Introduce tu prompt (Enter para default): ").strip()
    if not prompt:
        prompt = "Escribe una breve historia de 3 párrafos sobre un robot que aprende a pintar."

    print(f"\n📝 Usando prompt: {prompt}")

    # Menú
    while True:
        print("\n" + "-" * 40)
        print("Selecciona una API para probar streaming:")

        opciones = list(apis.keys())
        for i, api in enumerate(opciones, 1):
            print(f"{i}. {api.capitalize()}")
        print(f"{len(opciones) + 1}. Probar todas")
        print("0. Salir")

        opcion = input("\nOpción: ").strip()

        try:
            opcion_num = int(opcion)
            if opcion_num == 0:
                print("\n¡Hasta luego!")
                break
            elif 1 <= opcion_num <= len(opciones):
                api_seleccionada = opciones[opcion_num - 1]
                try:
                    apis[api_seleccionada](prompt, config)
                except Exception as e:
                    print(f"\n✗ Error con {api_seleccionada}: {e}")
            elif opcion_num == len(opciones) + 1:
                for nombre, func in apis.items():
                    try:
                        func(prompt, config)
                    except Exception as e:
                        print(f"\n✗ Error con {nombre}: {e}")
            else:
                print("Opción no válida.")
        except ValueError:
            print("Introduce un número válido.")


if __name__ == "__main__":
    main()
