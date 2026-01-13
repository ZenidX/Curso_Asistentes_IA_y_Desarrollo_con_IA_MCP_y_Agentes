# Ejercicios: Módulo 1 - APIs de IA Generativa

## Información

| | |
|---|---|
| **Dificultad progresiva** | Básico → Intermedio → Avanzado |
| **Tiempo total estimado** | 3-4 horas |
| **Requisitos** | Python 3.10+, API keys configuradas |

---

## Ejercicio 1: Primera llamada a la API

**Nivel**: Básico
**Tiempo**: 20 minutos

### Objetivo
Realizar tu primera llamada a una API de IA y entender la estructura de request/response.

### Instrucciones

1. Elige un proveedor (OpenAI, Anthropic o Google)
2. Crea un script que envíe el prompt: "Explica qué es una API en una frase"
3. Imprime la respuesta

### Código de inicio

```python
# ejercicio_1.py
import os

# TODO: Importar la librería del proveedor elegido
# TODO: Configurar la API key
# TODO: Enviar el mensaje y mostrar respuesta

prompt = "Explica qué es una API en una frase"

# Tu código aquí
```

### Solución esperada

```python
# OpenAI
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explica qué es una API en una frase"}]
)
print(response.choices[0].message.content)
```

### Criterios de éxito
- [ ] El script ejecuta sin errores
- [ ] Recibes una respuesta coherente del modelo
- [ ] Entiendes la estructura del objeto response

---

## Ejercicio 2: Comparar modelos

**Nivel**: Básico
**Tiempo**: 30 minutos

### Objetivo
Enviar el mismo prompt a diferentes proveedores y comparar respuestas.

### Instrucciones

1. Configura al menos 2 proveedores diferentes
2. Envía el prompt: "¿Cuál es la capital de Francia y por qué es famosa?"
3. Compara: tiempo de respuesta, calidad, longitud

### Código de inicio

```python
# ejercicio_2.py
import time

prompt = "¿Cuál es la capital de Francia y por qué es famosa?"

def llamar_openai(prompt):
    start = time.time()
    # TODO: Implementar
    elapsed = time.time() - start
    return response, elapsed

def llamar_anthropic(prompt):
    start = time.time()
    # TODO: Implementar
    elapsed = time.time() - start
    return response, elapsed

# Comparar resultados
```

### Tabla de comparación esperada

| Proveedor | Tiempo (s) | Tokens | Observaciones |
|-----------|------------|--------|---------------|
| OpenAI    |            |        |               |
| Anthropic |            |        |               |
| Google    |            |        |               |

### Criterios de éxito
- [ ] Llamas a al menos 2 proveedores
- [ ] Mides el tiempo de respuesta
- [ ] Documentas las diferencias observadas

---

## Ejercicio 3: System prompts

**Nivel**: Básico
**Tiempo**: 25 minutos

### Objetivo
Entender cómo el system prompt afecta el comportamiento del modelo.

### Instrucciones

1. Envía el mensaje "Hola, ¿cómo estás?" con diferentes system prompts:
   - Sin system prompt
   - "Eres un pirata que habla en español antiguo"
   - "Eres un asistente formal y conciso. Responde en máximo 10 palabras"
   - "Eres un experto en Python. Solo hablas de programación"

2. Compara las respuestas

### Código de inicio

```python
# ejercicio_3.py

system_prompts = [
    None,
    "Eres un pirata que habla en español antiguo",
    "Eres un asistente formal y conciso. Responde en máximo 10 palabras",
    "Eres un experto en Python. Solo hablas de programación"
]

user_message = "Hola, ¿cómo estás?"

for system_prompt in system_prompts:
    print(f"\n--- System: {system_prompt} ---")
    # TODO: Enviar mensaje con cada system prompt
```

### Criterios de éxito
- [ ] Observas diferencias claras en las respuestas
- [ ] Entiendes el rol del system prompt
- [ ] Puedes explicar cuándo usarlo

---

## Ejercicio 4: Streaming

**Nivel**: Intermedio
**Tiempo**: 30 minutos

### Objetivo
Implementar respuestas en streaming para mejor UX.

### Instrucciones

1. Crea una función que solicite una respuesta larga (ej: "Escribe un cuento corto")
2. Implementa streaming para mostrar la respuesta token por token
3. Mide la diferencia de "tiempo hasta primer token" vs respuesta completa

### Código de inicio

```python
# ejercicio_4.py
import time

def respuesta_normal(prompt):
    start = time.time()
    # TODO: Llamada normal
    first_token_time = time.time() - start
    return response, first_token_time

def respuesta_streaming(prompt):
    start = time.time()
    first_token_time = None

    # TODO: Llamada con streaming
    # Al recibir primer chunk: first_token_time = time.time() - start

    for chunk in stream:
        # TODO: Imprimir cada chunk
        pass

    return first_token_time

# Comparar tiempos
```

### Criterios de éxito
- [ ] El texto aparece progresivamente
- [ ] Mides el tiempo hasta primer token
- [ ] Observas la diferencia en experiencia de usuario

---

## Ejercicio 5: Parámetros de generación

**Nivel**: Intermedio
**Tiempo**: 35 minutos

### Objetivo
Experimentar con temperature, max_tokens y top_p.

### Instrucciones

1. Usa el prompt: "Sugiere un nombre para una startup de IA"
2. Genera 5 respuestas con temperature=0 (determinista)
3. Genera 5 respuestas con temperature=1.5 (creativo)
4. Experimenta con max_tokens: 10, 50, 200
5. Documenta las diferencias

### Código de inicio

```python
# ejercicio_5.py

prompt = "Sugiere un nombre para una startup de IA"

def generar_con_parametros(prompt, temperature=1.0, max_tokens=100, n=1):
    # TODO: Implementar con los parámetros especificados
    pass

# Experimento 1: Temperature
print("=== Temperature 0 (5 veces) ===")
for i in range(5):
    resultado = generar_con_parametros(prompt, temperature=0)
    print(f"{i+1}: {resultado}")

print("\n=== Temperature 1.5 (5 veces) ===")
for i in range(5):
    resultado = generar_con_parametros(prompt, temperature=1.5)
    print(f"{i+1}: {resultado}")

# Experimento 2: Max tokens
print("\n=== Max tokens ===")
for max_t in [10, 50, 200]:
    resultado = generar_con_parametros(prompt, max_tokens=max_t)
    print(f"max_tokens={max_t}: {resultado}")
```

### Preguntas a responder

1. ¿Qué pasa con temperature=0? ¿Las respuestas son idénticas?
2. ¿Qué pasa con temperature muy alta?
3. ¿Cómo afecta max_tokens a la respuesta?

### Criterios de éxito
- [ ] Generas múltiples respuestas con diferentes parámetros
- [ ] Documentas el efecto de cada parámetro
- [ ] Puedes elegir parámetros según el caso de uso

---

## Ejercicio 6: Manejo de errores

**Nivel**: Intermedio
**Tiempo**: 30 minutos

### Objetivo
Implementar manejo robusto de errores y reintentos.

### Instrucciones

1. Crea una función que maneje los errores comunes:
   - Rate limit (429)
   - Timeout
   - API key inválida
   - Modelo no disponible
2. Implementa reintentos con backoff exponencial
3. Agrega logging para debugging

### Código de inicio

```python
# ejercicio_6.py
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def llamar_api_con_reintentos(prompt, max_reintentos=3, backoff_base=2):
    """
    Llama a la API con manejo de errores y reintentos.

    Args:
        prompt: El mensaje a enviar
        max_reintentos: Número máximo de reintentos
        backoff_base: Base para el backoff exponencial

    Returns:
        La respuesta del modelo o None si falla
    """
    for intento in range(max_reintentos):
        try:
            logger.info(f"Intento {intento + 1}/{max_reintentos}")
            # TODO: Llamar a la API

            return response

        except Exception as e:  # TODO: Especificar excepciones
            logger.warning(f"Error: {e}")

            if intento < max_reintentos - 1:
                wait_time = backoff_base ** intento
                logger.info(f"Esperando {wait_time}s antes de reintentar...")
                time.sleep(wait_time)
            else:
                logger.error("Máximo de reintentos alcanzado")
                return None

# Test
resultado = llamar_api_con_reintentos("Hola")
print(resultado)
```

### Criterios de éxito
- [ ] La función maneja errores sin crashear
- [ ] Implementa reintentos con backoff
- [ ] Los logs son útiles para debugging

---

## Ejercicio 7: Function Calling

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Implementar function calling para extender las capacidades del modelo.

### Instrucciones

1. Define una función `obtener_clima(ciudad: str) -> dict`
2. Configura el modelo para usar esta función
3. Envía: "¿Qué tiempo hace en Madrid?"
4. El modelo debe llamar a la función y usar el resultado

### Código de inicio

```python
# ejercicio_7.py
import json

# Simulamos una API de clima
def obtener_clima(ciudad: str) -> dict:
    """Obtiene el clima actual de una ciudad (simulado)."""
    climas = {
        "madrid": {"temp": 22, "condicion": "soleado", "humedad": 45},
        "barcelona": {"temp": 25, "condicion": "parcialmente nublado", "humedad": 60},
        "valencia": {"temp": 27, "condicion": "despejado", "humedad": 55},
    }
    return climas.get(ciudad.lower(), {"error": "Ciudad no encontrada"})

# Definición de la herramienta para el modelo
tools = [
    {
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": "Obtiene el clima actual de una ciudad española",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad"
                    }
                },
                "required": ["ciudad"]
            }
        }
    }
]

def chat_con_herramientas(mensaje):
    # TODO:
    # 1. Enviar mensaje con tools
    # 2. Si el modelo quiere usar una herramienta, ejecutarla
    # 3. Enviar el resultado de vuelta al modelo
    # 4. Retornar respuesta final
    pass

# Test
respuesta = chat_con_herramientas("¿Qué tiempo hace en Madrid?")
print(respuesta)
```

### Criterios de éxito
- [ ] El modelo detecta que debe usar la función
- [ ] Ejecutas la función con los argumentos correctos
- [ ] El modelo genera una respuesta natural con los datos

---

## Ejercicio 8: Embeddings y búsqueda semántica

**Nivel**: Avanzado
**Tiempo**: 50 minutos

### Objetivo
Implementar búsqueda semántica usando embeddings.

### Instrucciones

1. Crea una base de conocimiento con 5-10 documentos
2. Genera embeddings para cada documento
3. Implementa búsqueda por similitud
4. Encuentra los documentos más relevantes para una query

### Código de inicio

```python
# ejercicio_8.py
import numpy as np

# Base de conocimiento
documentos = [
    "Python es un lenguaje de programación interpretado y de alto nivel.",
    "JavaScript es el lenguaje de programación más usado en desarrollo web.",
    "SQL es un lenguaje para gestionar bases de datos relacionales.",
    "Docker permite empaquetar aplicaciones en contenedores.",
    "Git es un sistema de control de versiones distribuido.",
    "React es una biblioteca de JavaScript para construir interfaces de usuario.",
    "PostgreSQL es una base de datos relacional open source muy potente.",
    "Kubernetes orquesta contenedores Docker en producción.",
]

def obtener_embedding(texto):
    """Obtiene el embedding de un texto."""
    # TODO: Usar la API de embeddings
    pass

def similitud_coseno(a, b):
    """Calcula la similitud coseno entre dos vectores."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def buscar_documentos(query, documentos, top_k=3):
    """Busca los documentos más similares a la query."""
    query_embedding = obtener_embedding(query)

    similitudes = []
    for doc in documentos:
        doc_embedding = obtener_embedding(doc)
        sim = similitud_coseno(query_embedding, doc_embedding)
        similitudes.append((doc, sim))

    # Ordenar por similitud descendente
    similitudes.sort(key=lambda x: x[1], reverse=True)

    return similitudes[:top_k]

# Test
query = "¿Cómo puedo gestionar contenedores?"
resultados = buscar_documentos(query, documentos)

print(f"Query: {query}\n")
for doc, sim in resultados:
    print(f"[{sim:.3f}] {doc}")
```

### Criterios de éxito
- [ ] Generas embeddings para todos los documentos
- [ ] La búsqueda retorna resultados relevantes
- [ ] Entiendes cómo funciona la similitud coseno

---

## Ejercicio 9: Chatbot con memoria

**Nivel**: Avanzado
**Tiempo**: 45 minutos

### Objetivo
Crear un chatbot que mantiene contexto de la conversación.

### Instrucciones

1. Implementa una clase Chatbot con historial de mensajes
2. El chatbot debe recordar información mencionada
3. Limita el historial para no exceder el contexto
4. Añade un resumen automático cuando el historial es muy largo

### Código de inicio

```python
# ejercicio_9.py

class Chatbot:
    def __init__(self, system_prompt=None, max_mensajes=20):
        self.system_prompt = system_prompt or "Eres un asistente útil."
        self.historial = []
        self.max_mensajes = max_mensajes

    def _construir_mensajes(self):
        """Construye la lista de mensajes para la API."""
        mensajes = [{"role": "system", "content": self.system_prompt}]
        mensajes.extend(self.historial)
        return mensajes

    def _limpiar_historial(self):
        """Limpia el historial si es muy largo."""
        if len(self.historial) > self.max_mensajes:
            # TODO: Implementar resumen o truncado
            pass

    def enviar(self, mensaje):
        """Envía un mensaje y retorna la respuesta."""
        self.historial.append({"role": "user", "content": mensaje})

        # TODO: Llamar a la API con el historial completo

        respuesta = "..."  # TODO: Obtener respuesta
        self.historial.append({"role": "assistant", "content": respuesta})

        self._limpiar_historial()

        return respuesta

    def limpiar(self):
        """Limpia el historial de la conversación."""
        self.historial = []

# Test
bot = Chatbot(system_prompt="Eres un asistente que recuerda todo lo que te dicen.")

print(bot.enviar("Me llamo Carlos"))
print(bot.enviar("Trabajo como desarrollador"))
print(bot.enviar("¿Cómo me llamo y a qué me dedico?"))
```

### Criterios de éxito
- [ ] El chatbot recuerda información previa
- [ ] Maneja correctamente el historial
- [ ] La conversación fluye naturalmente

---

## Ejercicio 10: Proyecto integrador - Analizador de código

**Nivel**: Avanzado
**Tiempo**: 60 minutos

### Objetivo
Crear una herramienta que analiza código usando múltiples capacidades de la API.

### Instrucciones

1. Lee un archivo de código
2. Usa la API para:
   - Explicar qué hace el código
   - Detectar posibles bugs
   - Sugerir mejoras
   - Generar documentación
3. Genera un reporte en Markdown

### Código de inicio

```python
# ejercicio_10.py
import os

class AnalizadorCodigo:
    def __init__(self, modelo="gpt-4o-mini"):
        self.modelo = modelo

    def leer_archivo(self, ruta):
        """Lee el contenido de un archivo."""
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()

    def explicar(self, codigo, lenguaje="python"):
        """Explica qué hace el código."""
        prompt = f"""Analiza este código {lenguaje} y explica qué hace de forma clara:

```{lenguaje}
{codigo}
```

Proporciona:
1. Resumen general
2. Explicación de las funciones principales
3. Flujo de ejecución"""
        # TODO: Llamar a la API
        pass

    def detectar_bugs(self, codigo, lenguaje="python"):
        """Detecta posibles bugs."""
        # TODO: Implementar
        pass

    def sugerir_mejoras(self, codigo, lenguaje="python"):
        """Sugiere mejoras de código."""
        # TODO: Implementar
        pass

    def generar_documentacion(self, codigo, lenguaje="python"):
        """Genera documentación (docstrings, comentarios)."""
        # TODO: Implementar
        pass

    def analisis_completo(self, ruta):
        """Realiza un análisis completo y genera reporte."""
        codigo = self.leer_archivo(ruta)

        reporte = f"""# Análisis de Código: {ruta}

## Explicación
{self.explicar(codigo)}

## Posibles Bugs
{self.detectar_bugs(codigo)}

## Sugerencias de Mejora
{self.sugerir_mejoras(codigo)}

## Documentación Sugerida
{self.generar_documentacion(codigo)}
"""
        return reporte

# Test
analizador = AnalizadorCodigo()

# Crear archivo de prueba
codigo_prueba = '''
def calcular_promedio(numeros):
    total = 0
    for n in numeros:
        total = total + n
    return total / len(numeros)

def buscar_maximo(lista):
    max = lista[0]
    for i in range(len(lista)):
        if lista[i] > max:
            max = lista[i]
    return max
'''

with open('codigo_prueba.py', 'w') as f:
    f.write(codigo_prueba)

reporte = analizador.analisis_completo('codigo_prueba.py')
print(reporte)

# Guardar reporte
with open('reporte_analisis.md', 'w') as f:
    f.write(reporte)
```

### Criterios de éxito
- [ ] Lee archivos de código correctamente
- [ ] Genera explicaciones claras
- [ ] Detecta bugs potenciales
- [ ] El reporte es útil y bien formateado

---

## Recursos adicionales

- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Google AI Documentation](https://ai.google.dev/docs)
