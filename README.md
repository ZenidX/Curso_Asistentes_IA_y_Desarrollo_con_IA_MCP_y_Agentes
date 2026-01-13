# Curso: IA para Desarrollo de Software

Curso completo sobre **Asistentes IA, MCPs y Agentes** para desarrolladores. Aprende a integrar IA generativa en tu flujo de trabajo de desarrollo.

## Contenido del Curso

| Módulo | Tema | Descripción |
|--------|------|-------------|
| 1 | **APIs de IA Generativa** | OpenAI, Anthropic, Google Gemini, Ollama. Incluye scripts y webapp práctica |
| 2 | **Herramientas CLI de IA** | Claude Code, Gemini CLI, Codex CLI |
| 3 | **Fundamentos de Software IA** | Ventanas de contexto, MCP, subagentes, hooks |
| 4 | **MCPs Oficiales** | AWS, Cloudflare, Firebase, GitHub, bases de datos |
| 5 | **Desarrollo de MCPs** | Crear servidores MCP en Python y TypeScript |
| 6 | **Arquitectura IA** | Patrones de desarrollo asistido por IA |

## Inicio Rápido

### Requisitos
- Python 3.10+
- Una o más API keys (OpenAI, Anthropic, Google) o Ollama instalado localmente

### Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd IA

# Configurar Módulo 1
cd "DiseñoCurso/Modulo 1 APIs de IA Generativa"
pip install -r requirements.txt

# Configurar API keys
cp config/config.example.yaml config/config.yaml
# Editar config.yaml con tus API keys
```

### Ejecutar Ejemplos

```bash
# Scripts básicos
python scripts/01_basico/openai_basico.py
python scripts/01_basico/anthropic_basico.py
python scripts/01_basico/google_basico.py
python scripts/01_basico/ollama_basico.py

# Webapp interactiva
cd webapp
uvicorn app:app --reload
# Abrir http://localhost:8000
```

## Estructura del Proyecto

```
DiseñoCurso/
├── Modulo 1 APIs de IA Generativa/
│   ├── Teoria 1.md
│   ├── config/config.example.yaml
│   ├── scripts/
│   │   ├── 01_basico/      # Llamadas básicas a APIs
│   │   ├── 02_intermedio/  # Streaming, comparación de modelos
│   │   └── 03_avanzado/    # Function calling, embeddings
│   └── webapp/             # App ReactPy con chat multi-proveedor
├── Modulo 2-6/             # Contenido teórico
└── Curso Completo IA para Desarrollo de Software.md
```

## APIs Soportadas

| Proveedor | Modelos | Tier Gratuito |
|-----------|---------|---------------|
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-3.5 | $5 crédito inicial |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus/Haiku | Créditos al registrarse |
| **Google** | Gemini 1.5 Pro/Flash | 60 req/min gratis |
| **Ollama** | Llama 3.2, Mistral, CodeLlama | 100% gratis (local) |

## Recursos

- [Documentación MCP](https://modelcontextprotocol.io)
- [Claude Code](https://claude.ai/code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Ollama](https://ollama.ai)

## Licencia

Contenido educativo. Uso personal y formativo.
