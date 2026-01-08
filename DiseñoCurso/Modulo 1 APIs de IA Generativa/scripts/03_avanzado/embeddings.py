"""
Embeddings y Similitud Semántica
================================

Los embeddings son representaciones numéricas (vectores) del texto
que capturan su significado semántico.

Casos de uso:
- Búsqueda semántica (encontrar documentos similares)
- Clasificación de texto
- Detección de duplicados
- Sistemas de recomendación
- Clustering de documentos
"""

import yaml
import math
from pathlib import Path
from openai import OpenAI
import google.generativeai as genai


def cargar_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def similitud_coseno(v1: list, v2: list) -> float:
    """
    Calcula la similitud del coseno entre dos vectores.

    La similitud del coseno mide el ángulo entre dos vectores:
    - 1.0 = Idénticos (mismo significado)
    - 0.0 = Sin relación
    - -1.0 = Opuestos

    Args:
        v1: Primer vector de embedding
        v2: Segundo vector de embedding

    Returns:
        Similitud entre -1 y 1
    """
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))

    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0

    return dot_product / (norm_v1 * norm_v2)


def obtener_embedding_openai(texto: str, client: OpenAI, modelo: str = "text-embedding-3-small") -> list:
    """Obtiene el embedding de un texto usando OpenAI."""
    response = client.embeddings.create(
        input=texto,
        model=modelo
    )
    return response.data[0].embedding


def obtener_embedding_google(texto: str, modelo: str = "text-embedding-004") -> list:
    """Obtiene el embedding de un texto usando Google."""
    result = genai.embed_content(
        model=f"models/{modelo}",
        content=texto
    )
    return result["embedding"]


def demo_embeddings_openai(config: dict):
    """Demuestra embeddings con OpenAI."""
    print("\n" + "=" * 60)
    print("🤖 OPENAI - Embeddings")
    print("=" * 60)

    client = OpenAI(api_key=config["apis"]["openai"]["api_key"])
    modelo = "text-embedding-3-small"

    print(f"Modelo: {modelo}")
    print(f"Dimensiones del vector: 1536\n")

    # Textos de ejemplo
    textos = [
        "El gato duerme en el sofá",
        "El felino descansa sobre el sillón",
        "Python es un lenguaje de programación",
        "La programación en Python es popular",
        "Mañana lloverá en Madrid"
    ]

    print("📝 Textos de ejemplo:")
    for i, t in enumerate(textos):
        print(f"   {i+1}. {t}")

    # Obtener embeddings
    print("\n⏳ Generando embeddings...")
    embeddings = {}
    for texto in textos:
        embeddings[texto] = obtener_embedding_openai(texto, client, modelo)

    # Calcular matriz de similitud
    print("\n📊 Matriz de Similitud (coseno):\n")

    # Encabezado
    print("     ", end="")
    for i in range(len(textos)):
        print(f"  [{i+1}]  ", end="")
    print()

    for i, t1 in enumerate(textos):
        print(f"[{i+1}] ", end="")
        for j, t2 in enumerate(textos):
            sim = similitud_coseno(embeddings[t1], embeddings[t2])
            print(f" {sim:.3f} ", end="")
        print()

    # Encontrar los más similares
    print("\n🔍 Pares más similares (excluyendo mismo texto):")
    pares = []
    for i, t1 in enumerate(textos):
        for j, t2 in enumerate(textos):
            if i < j:
                sim = similitud_coseno(embeddings[t1], embeddings[t2])
                pares.append((sim, t1, t2))

    pares.sort(reverse=True)
    for sim, t1, t2 in pares[:3]:
        print(f"\n   Similitud: {sim:.4f}")
        print(f"   → \"{t1}\"")
        print(f"   → \"{t2}\"")


def demo_embeddings_google(config: dict):
    """Demuestra embeddings con Google."""
    print("\n" + "=" * 60)
    print("🤖 GOOGLE - Embeddings")
    print("=" * 60)

    genai.configure(api_key=config["apis"]["google"]["api_key"])
    modelo = "text-embedding-004"

    print(f"Modelo: {modelo}")
    print(f"Dimensiones del vector: 768\n")

    # Textos de ejemplo
    textos = [
        "El gato duerme en el sofá",
        "El felino descansa sobre el sillón",
        "Python es un lenguaje de programación",
        "La programación en Python es popular",
        "Mañana lloverá en Madrid"
    ]

    print("📝 Textos de ejemplo:")
    for i, t in enumerate(textos):
        print(f"   {i+1}. {t}")

    # Obtener embeddings
    print("\n⏳ Generando embeddings...")
    embeddings = {}
    for texto in textos:
        embeddings[texto] = obtener_embedding_google(texto, modelo)

    # Calcular matriz de similitud
    print("\n📊 Matriz de Similitud (coseno):\n")

    print("     ", end="")
    for i in range(len(textos)):
        print(f"  [{i+1}]  ", end="")
    print()

    for i, t1 in enumerate(textos):
        print(f"[{i+1}] ", end="")
        for j, t2 in enumerate(textos):
            sim = similitud_coseno(embeddings[t1], embeddings[t2])
            print(f" {sim:.3f} ", end="")
        print()

    # Encontrar los más similares
    print("\n🔍 Pares más similares (excluyendo mismo texto):")
    pares = []
    for i, t1 in enumerate(textos):
        for j, t2 in enumerate(textos):
            if i < j:
                sim = similitud_coseno(embeddings[t1], embeddings[t2])
                pares.append((sim, t1, t2))

    pares.sort(reverse=True)
    for sim, t1, t2 in pares[:3]:
        print(f"\n   Similitud: {sim:.4f}")
        print(f"   → \"{t1}\"")
        print(f"   → \"{t2}\"")


def demo_busqueda_semantica(config: dict):
    """Demuestra búsqueda semántica con embeddings."""
    print("\n" + "=" * 60)
    print("🔍 BÚSQUEDA SEMÁNTICA")
    print("=" * 60)

    # Verificar qué API usar
    api_key = config["apis"]["openai"]["api_key"]
    usar_openai = api_key.startswith("sk-") and "tu-api-key" not in api_key

    if usar_openai:
        client = OpenAI(api_key=api_key)
        obtener_embedding = lambda t: obtener_embedding_openai(t, client)
        print("Usando: OpenAI text-embedding-3-small\n")
    else:
        genai.configure(api_key=config["apis"]["google"]["api_key"])
        obtener_embedding = lambda t: obtener_embedding_google(t)
        print("Usando: Google text-embedding-004\n")

    # Base de conocimiento simulada
    documentos = [
        "Python es un lenguaje de programación interpretado de alto nivel.",
        "JavaScript se usa principalmente para desarrollo web frontend.",
        "Machine learning es una rama de la inteligencia artificial.",
        "Las redes neuronales imitan el funcionamiento del cerebro humano.",
        "SQL es un lenguaje para consultar bases de datos relacionales.",
        "Docker permite empaquetar aplicaciones en contenedores.",
        "Git es un sistema de control de versiones distribuido.",
        "REST es un estilo de arquitectura para APIs web.",
        "Los microservicios dividen una aplicación en servicios pequeños.",
        "Kubernetes orquesta contenedores en producción."
    ]

    print("📚 Base de conocimiento:")
    for i, doc in enumerate(documentos, 1):
        print(f"   {i}. {doc[:50]}...")

    # Pre-calcular embeddings de documentos
    print("\n⏳ Indexando documentos...")
    embeddings_docs = [obtener_embedding(doc) for doc in documentos]
    print("✓ Documentos indexados")

    # Búsqueda interactiva
    while True:
        query = input("\n🔍 Buscar (Enter para salir): ").strip()
        if not query:
            break

        # Obtener embedding de la consulta
        embedding_query = obtener_embedding(query)

        # Calcular similitud con todos los documentos
        resultados = []
        for i, (doc, emb) in enumerate(zip(documentos, embeddings_docs)):
            sim = similitud_coseno(embedding_query, emb)
            resultados.append((sim, doc))

        # Ordenar por similitud
        resultados.sort(reverse=True)

        # Mostrar top 3
        print("\n📄 Resultados más relevantes:")
        for i, (sim, doc) in enumerate(resultados[:3], 1):
            print(f"\n   {i}. (similitud: {sim:.4f})")
            print(f"      {doc}")


def main():
    print("=" * 60)
    print("EMBEDDINGS Y SIMILITUD SEMÁNTICA")
    print("=" * 60)
    print("Los embeddings convierten texto en vectores numéricos")
    print("que capturan el significado semántico del texto.")

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
        apis_disponibles.append(("OpenAI", demo_embeddings_openai))

    api_key = config["apis"]["google"]["api_key"]
    if len(api_key) > 10 and "tu-api-key" not in api_key:
        apis_disponibles.append(("Google", demo_embeddings_google))

    if not apis_disponibles:
        print("✗ Se requiere OpenAI o Google para este ejemplo.")
        return

    print(f"\n✓ APIs disponibles: {', '.join([a[0] for a in apis_disponibles])}")

    # Menú
    while True:
        print("\n" + "-" * 40)
        print("Selecciona una demo:")
        print("1. Comparar similitud de textos (OpenAI)" if ("OpenAI", demo_embeddings_openai) in apis_disponibles else "")
        print("2. Comparar similitud de textos (Google)" if ("Google", demo_embeddings_google) in apis_disponibles else "")
        print("3. Búsqueda semántica interactiva")
        print("0. Salir")

        opcion = input("\nOpción: ").strip()

        if opcion == "0":
            print("\n¡Hasta luego!")
            break
        elif opcion == "1" and ("OpenAI", demo_embeddings_openai) in apis_disponibles:
            demo_embeddings_openai(config)
        elif opcion == "2" and ("Google", demo_embeddings_google) in apis_disponibles:
            demo_embeddings_google(config)
        elif opcion == "3":
            demo_busqueda_semantica(config)
        else:
            print("Opción no válida o API no disponible.")


if __name__ == "__main__":
    main()
