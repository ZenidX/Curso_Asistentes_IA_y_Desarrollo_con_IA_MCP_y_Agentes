"""
Script básico para usar la API de Google AI (Gemini)
====================================================

Este script demuestra cómo:
1. Cargar la configuración desde un archivo YAML
2. Conectarse a la API de Google Gemini
3. Enviar un prompt y recibir una respuesta
4. Manejar errores básicos
"""

import yaml
from pathlib import Path
import google.generativeai as genai


def cargar_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"No se encontró {config_path}\n"
            "Copia config.example.yaml a config.yaml y añade tus API keys."
        )

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def chat_con_google(prompt: str, config: dict) -> str:
    """
    Envía un prompt a Google Gemini y devuelve la respuesta.

    Args:
        prompt: El mensaje del usuario
        config: Configuración con API key y parámetros

    Returns:
        La respuesta del modelo
    """
    # Configurar la API key
    genai.configure(api_key=config["apis"]["google"]["api_key"])

    # Obtener parámetros por defecto
    defaults = config.get("defaults", {})
    modelo_nombre = config["apis"]["google"].get("default_model", "gemini-1.5-flash")

    # Crear el modelo con configuración
    generation_config = genai.GenerationConfig(
        temperature=defaults.get("temperature", 0.7),
        max_output_tokens=defaults.get("max_tokens", 1024),
    )

    modelo = genai.GenerativeModel(
        model_name=modelo_nombre,
        generation_config=generation_config,
        system_instruction="Eres un asistente útil que responde en español."
    )

    # Realizar la petición
    response = modelo.generate_content(prompt)

    # Extraer y devolver el contenido de la respuesta
    return response.text


def main():
    print("=" * 60)
    print("Google Gemini - Script Básico")
    print("=" * 60)

    # Cargar configuración
    try:
        config = cargar_config()
        print("✓ Configuración cargada correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar que hay API key
    api_key = config["apis"]["google"]["api_key"]
    if "tu-api-key" in api_key or len(api_key) < 10:
        print("✗ Error: Configura tu API key de Google en config.yaml")
        return

    # Prompt de ejemplo
    prompt = "¿Qué es la inteligencia artificial? Explícalo en 3 frases."
    print(f"\n📝 Prompt: {prompt}")
    print("-" * 60)

    # Obtener respuesta
    try:
        modelo = config["apis"]["google"].get("default_model", "gemini-1.5-flash")
        print(f"🤖 Modelo: {modelo}")
        print("⏳ Esperando respuesta...\n")

        respuesta = chat_con_google(prompt, config)

        print("💬 Respuesta:")
        print(respuesta)

    except Exception as e:
        print(f"✗ Error al llamar a la API: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
