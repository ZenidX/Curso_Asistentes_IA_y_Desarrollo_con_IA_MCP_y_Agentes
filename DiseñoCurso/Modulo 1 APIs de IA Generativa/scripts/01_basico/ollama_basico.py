"""
Script básico para usar Ollama (Modelos Locales)
================================================

Este script demuestra cómo:
1. Cargar la configuración desde un archivo YAML
2. Conectarse a Ollama (local)
3. Enviar un prompt y recibir una respuesta
4. Manejar errores básicos

REQUISITOS:
- Tener Ollama instalado (https://ollama.ai/)
- Haber descargado un modelo: ollama pull llama3.2
"""

import yaml
from pathlib import Path
import ollama


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


def chat_con_ollama(prompt: str, config: dict) -> str:
    """
    Envía un prompt a Ollama (local) y devuelve la respuesta.

    Args:
        prompt: El mensaje del usuario
        config: Configuración con modelo y parámetros

    Returns:
        La respuesta del modelo
    """
    # Obtener configuración de Ollama
    ollama_config = config["apis"]["ollama"]
    modelo = ollama_config.get("default_model", "llama3.2")

    # Obtener parámetros por defecto
    defaults = config.get("defaults", {})

    # Realizar la petición
    response = ollama.chat(
        model=modelo,
        messages=[
            {"role": "system", "content": "Eres un asistente útil que responde en español."},
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": defaults.get("temperature", 0.7),
            "num_predict": defaults.get("max_tokens", 1024)
        }
    )

    # Extraer y devolver el contenido de la respuesta
    return response["message"]["content"]


def verificar_ollama_disponible() -> bool:
    """Verifica si Ollama está corriendo y disponible."""
    try:
        ollama.list()
        return True
    except Exception:
        return False


def listar_modelos_disponibles() -> list:
    """Lista los modelos instalados en Ollama."""
    try:
        response = ollama.list()
        return [model["name"] for model in response["models"]]
    except Exception:
        return []


def main():
    print("=" * 60)
    print("Ollama (Local) - Script Básico")
    print("=" * 60)

    # Verificar que Ollama está corriendo
    if not verificar_ollama_disponible():
        print("✗ Error: Ollama no está disponible.")
        print("  Asegúrate de que Ollama está instalado y corriendo.")
        print("  Instalación: https://ollama.ai/")
        return

    print("✓ Ollama está disponible")

    # Listar modelos disponibles
    modelos = listar_modelos_disponibles()
    if modelos:
        print(f"✓ Modelos instalados: {', '.join(modelos)}")
    else:
        print("✗ No hay modelos instalados. Ejecuta: ollama pull llama3.2")
        return

    # Cargar configuración
    try:
        config = cargar_config()
        print("✓ Configuración cargada correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar que el modelo configurado está disponible
    modelo_config = config["apis"]["ollama"].get("default_model", "llama3.2")
    if not any(modelo_config in m for m in modelos):
        print(f"⚠ Modelo '{modelo_config}' no encontrado. Usando el primero disponible.")
        config["apis"]["ollama"]["default_model"] = modelos[0].split(":")[0]

    # Prompt de ejemplo
    prompt = "¿Qué es la inteligencia artificial? Explícalo en 3 frases."
    print(f"\n📝 Prompt: {prompt}")
    print("-" * 60)

    # Obtener respuesta
    try:
        modelo = config["apis"]["ollama"].get("default_model", "llama3.2")
        print(f"🤖 Modelo: {modelo}")
        print("⏳ Esperando respuesta (local, puede tardar unos segundos)...\n")

        respuesta = chat_con_ollama(prompt, config)

        print("💬 Respuesta:")
        print(respuesta)

    except Exception as e:
        print(f"✗ Error al llamar a Ollama: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
