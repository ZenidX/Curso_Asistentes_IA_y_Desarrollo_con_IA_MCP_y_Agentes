"""
Script básico para usar la API de Anthropic (Claude)
====================================================

Este script demuestra cómo:
1. Cargar la configuración desde un archivo YAML
2. Conectarse a la API de Anthropic
3. Enviar un prompt y recibir una respuesta
4. Manejar errores básicos
"""

import yaml
from pathlib import Path
import anthropic


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


def chat_con_anthropic(prompt: str, config: dict) -> str:
    """
    Envía un prompt a Anthropic Claude y devuelve la respuesta.

    Args:
        prompt: El mensaje del usuario
        config: Configuración con API key y parámetros

    Returns:
        La respuesta del modelo
    """
    # Crear cliente de Anthropic
    client = anthropic.Anthropic(api_key=config["apis"]["anthropic"]["api_key"])

    # Obtener parámetros por defecto
    defaults = config.get("defaults", {})
    modelo = config["apis"]["anthropic"].get("default_model", "claude-3-haiku-20240307")

    # Realizar la petición
    response = client.messages.create(
        model=modelo,
        max_tokens=defaults.get("max_tokens", 1024),
        system="Eres un asistente útil que responde en español.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extraer y devolver el contenido de la respuesta
    return response.content[0].text


def main():
    print("=" * 60)
    print("Anthropic Claude - Script Básico")
    print("=" * 60)

    # Cargar configuración
    try:
        config = cargar_config()
        print("✓ Configuración cargada correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar que hay API key
    api_key = config["apis"]["anthropic"]["api_key"]
    if "tu-api-key" in api_key or not api_key.startswith("sk-ant"):
        print("✗ Error: Configura tu API key de Anthropic en config.yaml")
        return

    # Prompt de ejemplo
    prompt = "¿Qué es la inteligencia artificial? Explícalo en 3 frases."
    print(f"\n📝 Prompt: {prompt}")
    print("-" * 60)

    # Obtener respuesta
    try:
        modelo = config["apis"]["anthropic"].get("default_model", "claude-3-haiku-20240307")
        print(f"🤖 Modelo: {modelo}")
        print("⏳ Esperando respuesta...\n")

        respuesta = chat_con_anthropic(prompt, config)

        print("💬 Respuesta:")
        print(respuesta)

    except Exception as e:
        print(f"✗ Error al llamar a la API: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
