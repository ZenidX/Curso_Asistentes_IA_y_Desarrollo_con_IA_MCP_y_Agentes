"""
Experimentar con parámetros de generación
=========================================

Este script permite experimentar con diferentes parámetros:
- Temperature: Controla la creatividad
- Max tokens: Limita la longitud de respuesta
- Top P: Alternativa a temperature (nucleus sampling)
- Frequency/Presence penalty: Controla repeticiones
"""

import yaml
from pathlib import Path
from openai import OpenAI


def cargar_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generar_con_parametros(
    prompt: str,
    client: OpenAI,
    modelo: str,
    temperature: float = 0.7,
    max_tokens: int = 200,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0
) -> str:
    """Genera una respuesta con los parámetros especificados."""
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content


def experimento_temperature(client: OpenAI, modelo: str):
    """Demuestra el efecto de temperature en las respuestas."""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 1: TEMPERATURE")
    print("=" * 60)
    print("Temperature controla la aleatoriedad/creatividad.")
    print("- 0.0 = Determinista (siempre igual)")
    print("- 1.0 = Equilibrado")
    print("- 2.0 = Muy creativo/aleatorio")

    prompt = "Escribe un título creativo para un artículo sobre inteligencia artificial."

    print(f"\n📝 Prompt: {prompt}\n")

    temperatures = [0.0, 0.5, 1.0, 1.5]

    for temp in temperatures:
        print(f"\n🌡️  Temperature = {temp}")
        print("-" * 40)
        # Generar 2 veces para ver variabilidad
        for i in range(2):
            respuesta = generar_con_parametros(
                prompt, client, modelo,
                temperature=temp, max_tokens=50
            )
            print(f"   {i+1}. {respuesta.strip()}")


def experimento_max_tokens(client: OpenAI, modelo: str):
    """Demuestra el efecto de max_tokens en las respuestas."""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 2: MAX_TOKENS")
    print("=" * 60)
    print("Max tokens limita la longitud de la respuesta.")
    print("Si se alcanza el límite, la respuesta se corta.")

    prompt = "Explica qué es la fotosíntesis."

    print(f"\n📝 Prompt: {prompt}\n")

    max_tokens_list = [20, 50, 150]

    for max_t in max_tokens_list:
        print(f"\n📏 Max tokens = {max_t}")
        print("-" * 40)
        respuesta = generar_con_parametros(
            prompt, client, modelo,
            temperature=0.7, max_tokens=max_t
        )
        print(f"   {respuesta}")
        print(f"   [Longitud: ~{len(respuesta.split())} palabras]")


def experimento_penalties(client: OpenAI, modelo: str):
    """Demuestra el efecto de frequency y presence penalty."""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 3: FREQUENCY & PRESENCE PENALTY")
    print("=" * 60)
    print("Estos parámetros controlan las repeticiones:")
    print("- Frequency penalty: Penaliza tokens según cuántas veces aparecen")
    print("- Presence penalty: Penaliza tokens que ya aparecieron (binario)")

    prompt = "Escribe un párrafo sobre el mar usando palabras variadas."

    print(f"\n📝 Prompt: {prompt}\n")

    configs = [
        {"frequency_penalty": 0.0, "presence_penalty": 0.0, "desc": "Sin penalización"},
        {"frequency_penalty": 1.0, "presence_penalty": 0.0, "desc": "Frequency penalty alto"},
        {"frequency_penalty": 0.0, "presence_penalty": 1.0, "desc": "Presence penalty alto"},
        {"frequency_penalty": 1.0, "presence_penalty": 1.0, "desc": "Ambos penalties altos"},
    ]

    for cfg in configs:
        print(f"\n⚖️  {cfg['desc']}")
        print(f"   (freq={cfg['frequency_penalty']}, pres={cfg['presence_penalty']})")
        print("-" * 40)
        respuesta = generar_con_parametros(
            prompt, client, modelo,
            temperature=0.7,
            max_tokens=100,
            frequency_penalty=cfg["frequency_penalty"],
            presence_penalty=cfg["presence_penalty"]
        )
        print(f"   {respuesta}")


def experimento_top_p(client: OpenAI, modelo: str):
    """Demuestra el efecto de top_p (nucleus sampling)."""
    print("\n" + "=" * 60)
    print("EXPERIMENTO 4: TOP_P (Nucleus Sampling)")
    print("=" * 60)
    print("Top P es una alternativa a temperature.")
    print("- top_p=0.1: Solo considera el 10% más probable")
    print("- top_p=0.9: Considera el 90% más probable")
    print("- top_p=1.0: Considera todos los tokens")
    print("\n⚠️  Se recomienda usar temperature O top_p, no ambos.")

    prompt = "Inventa un nombre para una startup de tecnología."

    print(f"\n📝 Prompt: {prompt}\n")

    top_p_values = [0.1, 0.5, 0.9]

    for top_p in top_p_values:
        print(f"\n🎯 Top P = {top_p}")
        print("-" * 40)
        for i in range(3):
            respuesta = generar_con_parametros(
                prompt, client, modelo,
                temperature=1.0,  # Fijo para aislar el efecto de top_p
                max_tokens=30,
                top_p=top_p
            )
            print(f"   {i+1}. {respuesta.strip()}")


def main():
    print("=" * 60)
    print("EXPERIMENTAR CON PARÁMETROS DE GENERACIÓN")
    print("=" * 60)

    # Cargar configuración
    try:
        config = cargar_config()
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar API key de OpenAI
    api_key = config["apis"]["openai"]["api_key"]
    if "tu-api-key" in api_key or not api_key.startswith("sk-"):
        print("✗ Este script requiere una API key de OpenAI válida.")
        return

    # Crear cliente
    client = OpenAI(api_key=api_key)
    modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")

    print(f"✓ Usando modelo: {modelo}")

    # Menú de experimentos
    while True:
        print("\n" + "-" * 40)
        print("Selecciona un experimento:")
        print("1. Temperature (creatividad)")
        print("2. Max tokens (longitud)")
        print("3. Frequency/Presence penalty (repeticiones)")
        print("4. Top P (nucleus sampling)")
        print("5. Ejecutar todos")
        print("0. Salir")

        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            experimento_temperature(client, modelo)
        elif opcion == "2":
            experimento_max_tokens(client, modelo)
        elif opcion == "3":
            experimento_penalties(client, modelo)
        elif opcion == "4":
            experimento_top_p(client, modelo)
        elif opcion == "5":
            experimento_temperature(client, modelo)
            experimento_max_tokens(client, modelo)
            experimento_penalties(client, modelo)
            experimento_top_p(client, modelo)
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
