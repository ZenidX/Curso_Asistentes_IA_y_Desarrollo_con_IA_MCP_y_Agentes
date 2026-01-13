# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spanish-language course: **"Curso de Asistentes IA y Desarrollo con IA, MCP y Agentes"** - A 6-module course covering AI APIs, CLI tools, MCP development, and AI-assisted architecture.

## Course Modules

| Module | Topic | Has Code |
|--------|-------|----------|
| 1 | APIs de IA Generativa | ✅ Python scripts + ReactPy webapp |
| 2 | Herramientas CLI de IA | Theory only (references TaskFlow project) |
| 3 | Fundamentos de Software IA | Theory only |
| 4 | MCPs Oficiales | Theory only |
| 5 | Desarrollo de MCPs | Theory only (MCP server examples) |
| 6 | Arquitectura IA | Theory only |

## Development Commands

```bash
# Module 1 setup
cd "Modulo 1 APIs de IA Generativa"
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml  # Add your API keys

# Run individual scripts
python scripts/01_basico/openai_basico.py
python scripts/02_intermedio/streaming.py
python scripts/03_avanzado/function_calling.py

# Run webapp (ReactPy)
cd webapp && uvicorn app:app --reload  # http://localhost:8000
```

## Architecture

### Module 1 Code Structure
```
Modulo 1 APIs de IA Generativa/
├── scripts/
│   ├── 01_basico/     → Basic API calls (OpenAI, Anthropic, Google, Ollama)
│   ├── 02_intermedio/ → Streaming, model comparison, advanced parameters
│   └── 03_avanzado/   → Function calling, embeddings
└── webapp/
    └── services/ai_client.py  → Unified AIClient class for all providers
```

### AIClient (`webapp/services/ai_client.py`)
Unified interface supporting:
- **Providers**: OpenAI, Anthropic, Google Gemini, Ollama (local)
- **Methods**: `chat()` for single response, `chat_stream()` for streaming
- **Config**: Reads from `config/config.yaml` (YAML format)

## Content Guidelines

- All content in Spanish
- Module naming: `Modulo N <Topic>/`
- Theory files: `Teoria N.md`
- Comprehensive course reference: `Curso Completo IA para Desarrollo de Software.md`
