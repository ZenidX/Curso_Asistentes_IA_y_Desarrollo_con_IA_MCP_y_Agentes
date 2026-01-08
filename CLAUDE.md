# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Spanish-language course repository: **"Curso de Asistentes IA y Desarrollo con IA, MCP y Agentes"** (AI Assistants and AI-Powered Development with MCP and Agents Course).

## Repository Structure

```
DiseñoCurso/
├── Modulo 1 APIs de IA Generativa/
│   ├── Teoria 1.md              # Course theory documentation
│   ├── requirements.txt         # Python dependencies
│   ├── config/
│   │   └── config.example.yaml  # API keys template
│   ├── scripts/
│   │   ├── 01_basico/          # Basic API usage examples
│   │   ├── 02_intermedio/      # Intermediate (streaming, comparison)
│   │   └── 03_avanzado/        # Advanced (function calling, embeddings)
│   └── webapp/
│       ├── app.py              # ReactPy main application
│       ├── components/         # UI components
│       └── services/           # AI client abstraction
├── Curso Completo IA para Desarrollo de Software.md
└── Ideas de Curso de IA.md
```

## Development Commands

### Setup
```bash
cd "DiseñoCurso/Modulo 1 APIs de IA Generativa"
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys
```

### Run Scripts
```bash
# Basic examples
python scripts/01_basico/openai_basico.py
python scripts/01_basico/anthropic_basico.py
python scripts/01_basico/google_basico.py
python scripts/01_basico/ollama_basico.py

# Intermediate
python scripts/02_intermedio/comparar_modelos.py
python scripts/02_intermedio/parametros_avanzados.py
python scripts/02_intermedio/streaming.py

# Advanced
python scripts/03_avanzado/function_calling.py
python scripts/03_avanzado/embeddings.py
```

### Run Webapp
```bash
cd webapp
uvicorn app:app --reload
# Open http://localhost:8000
```

## Architecture Notes

- **AI Client (`webapp/services/ai_client.py`)**: Unified interface for OpenAI, Anthropic, Google, and Ollama APIs
- **Config system**: YAML-based configuration with `config.example.yaml` as template
- **Scripts progression**: Basic → Intermediate → Advanced, each building on previous concepts
- **ReactPy webapp**: Single-page application with provider/model selection and parameter controls

## Content Guidelines

- All content is in Spanish
- Course modules follow `Modulo N <Topic>/` pattern
- Theory files use `Teoria N.md` pattern
- API keys must never be committed (config.yaml is in .gitignore)
