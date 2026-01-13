# Gemini CLI (Google)

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Principiante |
| **Requisitos** | Node.js 18+, cuenta Google |
| **Costo** | Gratis (1000 requests/día) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Instalar y configurar Gemini CLI
- [ ] Autenticarte con tu cuenta de Google
- [ ] Ejecutar prompts básicos e interactivos
- [ ] Aprovechar el contexto masivo de 1M tokens
- [ ] Crear un archivo GEMINI.md para tu proyecto

---

## ¿Por Qué Gemini CLI?

| Ventaja | Descripción |
|---------|-------------|
| **Gratis** | Tier gratuito muy generoso (1000 requests/día) |
| **Contexto masivo** | 1 millón de tokens (vs 200K de Claude) |
| **Open Source** | Código completamente abierto |

---

## 1. Instalación

```bash
# Via npm
npm install -g @google/gemini-cli

# Verificar
gemini --version
```

### Alternativas de instalación

```bash
# Via Homebrew (macOS)
brew install gemini-cli

# Via yarn
yarn global add @google/gemini-cli
```

### ⚠️ Error Común: "gemini no reconocido"

**Síntoma**: `'gemini' is not recognized as an internal or external command`

**Solución**:
```bash
# Ver dónde se instaló npm global
npm config get prefix

# Añadir esa ruta/bin al PATH del sistema
# Windows: Panel de Control → Sistema → Variables de entorno
# Linux/macOS: Añadir a ~/.bashrc o ~/.zshrc
export PATH="$PATH:$(npm config get prefix)/bin"
```

---

## 2. Límites del Tier Gratuito

| Recurso | Límite |
|---------|--------|
| Requests por minuto | 60 |
| Requests por día | 1,000 |
| Tokens de contexto | 1,000,000 |
| Modelo | Gemini 2.5 Pro |

**Cálculo práctico**: 1000 req/día ÷ 8 horas = **125 prompts/hora**. Más que suficiente para desarrollo normal.

> 💡 **Concepto clave**: El contexto de 1M tokens significa que Gemini puede "ver" proyectos completos de una vez. Un proyecto típico de 10,000 líneas ocupa ~15,000 tokens, dejando espacio para conversaciones extensas.

### 📍 Checkpoint 1

Antes de continuar, verifica:
- [ ] `gemini --version` funciona correctamente
- [ ] Entiendes los límites del tier gratuito

---

## 3. Autenticación

### Opción 1: Login interactivo

```bash
gemini
# Selecciona "Sign in with Google"
# Autoriza en el navegador
```

### Opción 2: API Key

```bash
# Obtener key en https://aistudio.google.com/
export GOOGLE_API_KEY="AIza..."

# O en el archivo de configuración
# ~/.gemini/settings.json
```

---

## 4. Comandos Básicos

### Sesión interactiva

```bash
gemini

# Dentro de la sesión:
> Analiza este proyecto
> Encuentra bugs potenciales en src/
> Genera tests para la función validateUser
```

### Prompt directo

```bash
# Ejecutar y salir
gemini "Analiza este proyecto"

# Con formato de salida
gemini -p "Lista las dependencias" --output-format json

# Modo no interactivo (para scripts)
gemini -p "Explica el error" < error.log
```

---

## 5. Comandos Slash

| Comando | Función |
|---------|---------|
| `/help` | Ayuda |
| `/chat` | Nueva conversación |
| `/settings` | Configuración |
| `/model` | Seleccionar modelo |
| `/memory list` | Ver archivos de memoria |
| `/extensions` | Gestionar extensiones |

---

## 6. Configuración

### Archivo settings.json

```json
// ~/.gemini/settings.json
{
  "theme": "dark",
  "model": "gemini-2.5-flash",
  "previewFeatures": true,
  "showStatusInTitle": true
}
```

### Archivo GEMINI.md

Similar a CLAUDE.md, proporciona contexto persistente:

```markdown
# Proyecto: E-commerce API

## Tecnologías
- Python 3.11 + FastAPI
- MongoDB
- Docker + Kubernetes

## Reglas de código
- Type hints obligatorios
- Docstrings en Google style
- Tests con pytest
```

---

## 7. Cuándo Elegir Gemini sobre otras CLIs

| Escenario | ¿Gemini? | Por qué |
|-----------|----------|---------|
| Proyecto con muchos archivos | ✅ Sí | Contexto de 1M tokens |
| Análisis de monorepos | ✅ Sí | Puede "ver" más código |
| Presupuesto limitado | ✅ Sí | Tier gratuito generoso |
| Razonamiento complejo | ❌ No | Claude es mejor |
| Código crítico/seguro | ❌ No | Claude más conservador |

---

## 8. Práctica Guiada

### Comparar con otras CLIs

Ejecuta el mismo prompt en Gemini y otra CLI:

```bash
# En un proyecto mediano
cd tu-proyecto

# Con Gemini
gemini "Identifica los 3 mayores problemas de arquitectura"

# Compara con Claude
claude "Identifica los 3 mayores problemas de arquitectura"
```

**Observa**:
- ¿Cuál da respuestas más detalladas?
- ¿Cuál es más rápido?
- ¿Las recomendaciones son similares?

---

## 9. Ventajas del Contexto Masivo

Con 1M tokens, Gemini puede:

```bash
# Analizar un monorepo completo
gemini "Analiza la arquitectura de todo el monorepo"

# Comparar múltiples archivos grandes
gemini "Compara la implementación de auth en los 5 microservicios"

# Revisar historial extenso
gemini "Analiza los últimos 100 commits y detecta patrones"
```

---

## 📍 Checkpoint Final

Verifica que puedes:
- [ ] Ejecutar `gemini --version`
- [ ] Autenticarte correctamente
- [ ] Ejecutar prompts básicos en modo interactivo
- [ ] Crear un archivo GEMINI.md para tu proyecto
- [ ] Entender cuándo elegir Gemini sobre otras CLIs

---

## Resumen

| Aspecto | Gemini CLI |
|---------|------------|
| **Mejor para** | Proyectos grandes, monorepos, presupuesto limitado |
| **Contexto** | 1,000,000 tokens (el mayor disponible) |
| **Costo** | Gratis hasta 1000 requests/día |
| **Limitación** | Razonamiento menos profundo que Claude |

---

## Recursos

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Google AI Studio](https://aistudio.google.com/) (para API keys)
- [Documentación Gemini API](https://ai.google.dev/docs)
