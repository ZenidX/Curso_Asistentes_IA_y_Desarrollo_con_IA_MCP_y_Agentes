"""
Comparar respuestas de diferentes modelos de IA
================================================

Este script envía el mismo prompt a múltiples APIs y compara:
- El contenido de las respuestas
- El tiempo de respuesta
- Los tokens utilizados (cuando está disponible)
"""

import yaml
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Importar clientes de cada API
from openai import OpenAI
import anthropic
import google.generativeai as genai
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


def llamar_openai(prompt: str, config: dict) -> dict:
    """Llama a OpenAI y devuelve resultado con métricas."""
    try:
        client = OpenAI(api_key=config["apis"]["openai"]["api_key"])
        modelo = config["apis"]["openai"].get("default_model", "gpt-4o-mini")

        inicio = time.time()
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Responde de forma concisa en español."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        tiempo = time.time() - inicio

        return {
            "proveedor": "OpenAI",
            "modelo": modelo,
            "respuesta": response.choices[0].message.content,
            "tiempo": tiempo,
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens,
            "error": None
        }
    except Exception as e:
        return {"proveedor": "OpenAI", "error": str(e)}


def llamar_anthropic(prompt: str, config: dict) -> dict:
    """Llama a Anthropic y devuelve resultado con métricas."""
    try:
        client = anthropic.Anthropic(api_key=config["apis"]["anthropic"]["api_key"])
        modelo = config["apis"]["anthropic"].get("default_model", "claude-3-haiku-20240307")

        inicio = time.time()
        response = client.messages.create(
            model=modelo,
            max_tokens=500,
            system="Responde de forma concisa en español.",
            messages=[{"role": "user", "content": prompt}]
        )
        tiempo = time.time() - inicio

        return {
            "proveedor": "Anthropic",
            "modelo": modelo,
            "respuesta": response.content[0].text,
            "tiempo": tiempo,
            "tokens_input": response.usage.input_tokens,
            "tokens_output": response.usage.output_tokens,
            "error": None
        }
    except Exception as e:
        return {"proveedor": "Anthropic", "error": str(e)}


def llamar_google(prompt: str, config: dict) -> dict:
    """Llama a Google Gemini y devuelve resultado con métricas."""
    try:
        genai.configure(api_key=config["apis"]["google"]["api_key"])
        modelo_nombre = config["apis"]["google"].get("default_model", "gemini-1.5-flash")

        modelo = genai.GenerativeModel(
            model_name=modelo_nombre,
            system_instruction="Responde de forma concisa en español."
        )

        inicio = time.time()
        response = modelo.generate_content(prompt)
        tiempo = time.time() - inicio

        return {
            "proveedor": "Google",
            "modelo": modelo_nombre,
            "respuesta": response.text,
            "tiempo": tiempo,
            "tokens_input": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else "N/A",
            "tokens_output": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else "N/A",
            "error": None
        }
    except Exception as e:
        return {"proveedor": "Google", "error": str(e)}


def llamar_ollama(prompt: str, config: dict) -> dict:
    """Llama a Ollama (local) y devuelve resultado con métricas."""
    try:
        modelo = config["apis"]["ollama"].get("default_model", "llama3.2")

        inicio = time.time()
        response = ollama.chat(
            model=modelo,
            messages=[
                {"role": "system", "content": "Responde de forma concisa en español."},
                {"role": "user", "content": prompt}
            ]
        )
        tiempo = time.time() - inicio

        return {
            "proveedor": "Ollama",
            "modelo": modelo,
            "respuesta": response["message"]["content"],
            "tiempo": tiempo,
            "tokens_input": response.get("prompt_eval_count", "N/A"),
            "tokens_output": response.get("eval_count", "N/A"),
            "error": None
        }
    except Exception as e:
        return {"proveedor": "Ollama", "error": str(e)}


def verificar_apis_disponibles(config: dict) -> list:
    """Verifica qué APIs están configuradas y disponibles."""
    disponibles = []

    # OpenAI
    api_key = config["apis"]["openai"]["api_key"]
    if api_key.startswith("sk-") and "tu-api-key" not in api_key:
        disponibles.append(("OpenAI", llamar_openai))

    # Anthropic
    api_key = config["apis"]["anthropic"]["api_key"]
    if api_key.startswith("sk-ant") and "tu-api-key" not in api_key:
        disponibles.append(("Anthropic", llamar_anthropic))

    # Google
    api_key = config["apis"]["google"]["api_key"]
    if len(api_key) > 10 and "tu-api-key" not in api_key:
        disponibles.append(("Google", llamar_google))

    # Ollama (verificar si está corriendo)
    try:
        ollama.list()
        disponibles.append(("Ollama", llamar_ollama))
    except Exception:
        pass

    return disponibles


def imprimir_resultado(resultado: dict):
    """Imprime el resultado de una API de forma formateada."""
    print(f"\n{'='*60}")
    print(f"🤖 {resultado['proveedor']}")
    print(f"{'='*60}")

    if resultado.get("error"):
        print(f"❌ Error: {resultado['error']}")
        return

    print(f"📦 Modelo: {resultado['modelo']}")
    print(f"⏱️  Tiempo: {resultado['tiempo']:.2f} segundos")
    print(f"📊 Tokens: {resultado['tokens_input']} input → {resultado['tokens_output']} output")
    print(f"\n💬 Respuesta:\n{resultado['respuesta']}")


def main():
    print("=" * 60)
    print("COMPARADOR DE MODELOS DE IA")
    print("=" * 60)

    # Cargar configuración
    try:
        config = cargar_config()
        print("✓ Configuración cargada")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return

    # Verificar APIs disponibles
    apis_disponibles = verificar_apis_disponibles(config)
    if not apis_disponibles:
        print("✗ No hay APIs configuradas. Edita config/config.yaml")
        return

    print(f"✓ APIs disponibles: {', '.join([a[0] for a in apis_disponibles])}")

    # Prompt para comparar
    prompt = input("\n📝 Introduce tu prompt (Enter para usar el default): ").strip()
    if not prompt:
        prompt = "Explica qué es machine learning en 2-3 frases simples."
    print(f"\n📝 Prompt: {prompt}")

    # Ejecutar llamadas en paralelo
    print("\n⏳ Consultando APIs en paralelo...")

    resultados = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futuros = {
            executor.submit(func, prompt, config): nombre
            for nombre, func in apis_disponibles
        }

        for futuro in as_completed(futuros):
            resultado = futuro.result()
            resultados.append(resultado)

    # Ordenar por tiempo de respuesta
    resultados_ok = [r for r in resultados if not r.get("error")]
    resultados_ok.sort(key=lambda x: x.get("tiempo", float("inf")))

    # Imprimir resultados
    for resultado in resultados_ok:
        imprimir_resultado(resultado)

    # Imprimir errores
    for resultado in resultados:
        if resultado.get("error"):
            imprimir_resultado(resultado)

    # Resumen comparativo
    if len(resultados_ok) > 1:
        print("\n" + "=" * 60)
        print("📊 RESUMEN COMPARATIVO")
        print("=" * 60)
        print(f"{'Proveedor':<15} {'Modelo':<30} {'Tiempo':<10} {'Tokens':<15}")
        print("-" * 70)
        for r in resultados_ok:
            tokens = f"{r.get('tokens_input', '?')}/{r.get('tokens_output', '?')}"
            print(f"{r['proveedor']:<15} {r['modelo']:<30} {r['tiempo']:.2f}s     {tokens:<15}")

        # Más rápido
        mas_rapido = resultados_ok[0]
        print(f"\n🏆 Más rápido: {mas_rapido['proveedor']} ({mas_rapido['tiempo']:.2f}s)")


if __name__ == "__main__":
    main()
