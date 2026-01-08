"""
Script básico para usar la API de OpenAI (GPT-4, GPT-3.5)
=========================================================

Este script demuestra cómo:
1. Cargar la configuración desde un archivo YAML
2. Conectarse a la API de OpenAI
3. Enviar un prompt y recibir una respuesta
4. Manejar errores básicos
"""

import yaml
from pathlib import Path
from openai import OpenAI


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


def chat_con_openai(prompt: str, config: dict) -> str:
    """
    Envía un prompt a OpenAI y devuelve la respuesta.

    Args:
        prompt: El mensaje del usuario
        config: Configuración con API key y parámetros

    Returns:
        La respuesta del modelo
    """
    # Crear cliente de OpenAI
    client = OpenAI(api_key=config["apis"]["openai"]["api_key"])

    # Obtener parámetros por defecto
    defaults = config.get("defaults", {})
    modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")

    # Realizar la petición
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Eres un asistente útil que responde en español."},
            {"role": "user", "content": prompt}
        ],
        temperature=defaults.get("temperature", 0.7),
        max_tokens=defaults.get("max_tokens", 1024)
    )

    # Extraer y devolver el contenido de la respuesta
    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("OpenAI - Script Básico")
    print("=" * 60)

    # Cargar configuración
    try:
        config = cargar_config()
        print("✓ Configuración cargada correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar que hay API key
    api_key = config["apis"]["openai"]["api_key"]
    if "tu-api-key" in api_key or not api_key.startswith("sk-"):
        print("✗ Error: Configura tu API key de OpenAI en config.yaml")
        return

    # Prompt de ejemplo
    prompt = "¿Qué es la inteligencia artificial? Explícalo en 3 frases."
    print(f"\n📝 Prompt: {prompt}")
    print("-" * 60)

    # Obtener respuesta
    try:
        modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")
        print(f"🤖 Modelo: {modelo}")
        print("⏳ Esperando respuesta...\n")

        respuesta = chat_con_openai(prompt, config)

        print("💬 Respuesta:")
        print(respuesta)

    except Exception as e:
        print(f"✗ Error al llamar a la API: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
