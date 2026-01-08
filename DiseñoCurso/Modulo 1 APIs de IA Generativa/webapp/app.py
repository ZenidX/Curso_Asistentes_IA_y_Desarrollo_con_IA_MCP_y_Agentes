"""
Aplicación Web ReactPy - Chat con múltiples IAs
===============================================

Esta aplicación permite:
- Seleccionar entre diferentes proveedores de IA
- Ajustar parámetros de generación
- Chatear y ver respuestas en tiempo real
- Comparar tokens y costes

Para ejecutar:
    cd webapp
    uvicorn app:app --reload

Luego abre http://localhost:8000 en tu navegador.
"""

from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from components import ModelSelector, ParameterPanel, ChatInterface
from services import AIClient


# CSS embebido para la aplicación
CSS_STYLES = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
    color: #e0e0e0;
}

.app-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 20px;
    min-height: 100vh;
}

.sidebar {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.main-content {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
}

h1 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: #fff;
    text-align: center;
}

h2 {
    font-size: 1.2rem;
    margin-bottom: 15px;
    color: #fff;
}

h3 {
    font-size: 1rem;
    margin-bottom: 15px;
    color: #ccc;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 10px;
}

/* Model Selector */
.model-selector {
    margin-bottom: 30px;
}

.selector-group {
    margin-bottom: 15px;
}

.selector-group label {
    display: block;
    margin-bottom: 5px;
    font-size: 0.9rem;
    color: #aaa;
}

.selector-group select {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    font-size: 0.9rem;
    cursor: pointer;
}

.selector-group select:focus {
    outline: none;
    border-color: #4a9eff;
}

/* Parameter Panel */
.parameter-panel {
    margin-top: 20px;
}

.parameter-item {
    margin-bottom: 20px;
}

.parameter-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.parameter-header label {
    font-size: 0.85rem;
    color: #ccc;
}

.parameter-value {
    font-size: 0.85rem;
    color: #4a9eff;
    font-weight: bold;
}

.parameter-slider {
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.1);
    appearance: none;
    cursor: pointer;
}

.parameter-slider::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #4a9eff;
    cursor: pointer;
}

.parameter-number {
    width: 100%;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    font-size: 0.9rem;
}

.parameter-description {
    font-size: 0.75rem;
    color: #888;
    margin-top: 5px;
}

/* Chat Interface */
.chat-interface {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    min-height: 400px;
    max-height: 60vh;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    margin-bottom: 15px;
}

.empty-chat {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #666;
    font-size: 1rem;
}

.chat-message {
    margin-bottom: 15px;
    padding: 15px;
    border-radius: 12px;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: linear-gradient(135deg, #4a9eff 0%, #3a7fcf 100%);
    margin-left: 20%;
}

.assistant-message {
    background: rgba(255, 255, 255, 0.1);
    margin-right: 20%;
}

.message-header {
    margin-bottom: 8px;
}

.message-role {
    font-size: 0.8rem;
    opacity: 0.8;
}

.message-content {
    font-size: 0.95rem;
    line-height: 1.5;
    white-space: pre-wrap;
}

.loading-indicator {
    text-align: center;
    padding: 20px;
    color: #4a9eff;
    display: none;
}

.loading-indicator.visible {
    display: block;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.token-info {
    display: flex;
    justify-content: space-between;
    padding: 10px 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 0.85rem;
    color: #aaa;
}

.cost-info {
    color: #4ade80;
}

.chat-input-form {
    display: flex;
    gap: 10px;
}

.chat-input {
    flex: 1;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    font-size: 0.95rem;
    resize: none;
    font-family: inherit;
}

.chat-input:focus {
    outline: none;
    border-color: #4a9eff;
}

.chat-input::placeholder {
    color: #666;
}

.send-button {
    padding: 15px 25px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #4a9eff 0%, #3a7fcf 100%);
    color: #fff;
    font-size: 0.95rem;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
}

.send-button:hover:not(:disabled) {
    transform: translateY(-2px);
}

.send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Clear button */
.clear-button {
    margin-top: 20px;
    padding: 10px;
    width: 100%;
    border-radius: 8px;
    border: 1px solid rgba(255, 100, 100, 0.3);
    background: rgba(255, 100, 100, 0.1);
    color: #ff6b6b;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s;
}

.clear-button:hover {
    background: rgba(255, 100, 100, 0.2);
}

/* Responsive */
@media (max-width: 900px) {
    .app-container {
        grid-template-columns: 1fr;
    }

    .sidebar {
        order: 2;
    }

    .main-content {
        order: 1;
    }
}
"""


@component
def App():
    """Componente principal de la aplicación."""

    # Cliente de IA
    ai_client = AIClient()

    # Estados
    messages, set_messages = hooks.use_state([])
    is_loading, set_is_loading = hooks.use_state(False)
    last_response_info, set_last_response_info = hooks.use_state({})

    # Proveedores y modelos
    available_providers = ai_client.get_available_providers()

    # Estado del proveedor seleccionado
    default_provider = available_providers[0] if available_providers else "openai"
    selected_provider, set_selected_provider = hooks.use_state(default_provider)

    # Estado del modelo seleccionado
    models = ai_client.get_models_for_provider(selected_provider)
    default_model = models[0][0] if models else ""
    selected_model, set_selected_model = hooks.use_state(default_model)

    # Parámetros de generación
    temperature, set_temperature = hooks.use_state(0.7)
    max_tokens, set_max_tokens = hooks.use_state(1024)
    top_p, set_top_p = hooks.use_state(1.0)
    frequency_penalty, set_frequency_penalty = hooks.use_state(0.0)
    presence_penalty, set_presence_penalty = hooks.use_state(0.0)

    # Obtener modelos por proveedor
    models_by_provider = {}
    for provider in available_providers:
        models_by_provider[provider] = ai_client.get_models_for_provider(provider)

    def handle_provider_change(new_provider):
        set_selected_provider(new_provider)
        new_models = ai_client.get_models_for_provider(new_provider)
        if new_models:
            set_selected_model(new_models[0][0])

    def handle_model_change(new_model):
        set_selected_model(new_model)

    def handle_parameter_change(param_name, value):
        if param_name == "temperature":
            set_temperature(value)
        elif param_name == "max_tokens":
            set_max_tokens(int(value))
        elif param_name == "top_p":
            set_top_p(value)
        elif param_name == "frequency_penalty":
            set_frequency_penalty(value)
        elif param_name == "presence_penalty":
            set_presence_penalty(value)

    async def handle_send_message(content):
        # Añadir mensaje del usuario
        new_messages = messages + [{"role": "user", "content": content}]
        set_messages(new_messages)
        set_is_loading(True)

        try:
            # Llamar a la API
            response = ai_client.chat(
                provider=selected_provider,
                model=selected_model,
                messages=new_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            if response.error:
                assistant_content = f"Error: {response.error}"
            else:
                assistant_content = response.content

            # Añadir respuesta del asistente
            set_messages(new_messages + [{"role": "assistant", "content": assistant_content}])

            # Actualizar info de tokens
            set_last_response_info({
                "tokens_input": response.tokens_input,
                "tokens_output": response.tokens_output,
                "provider": selected_provider
            })

        except Exception as e:
            set_messages(new_messages + [{"role": "assistant", "content": f"Error: {str(e)}"}])

        finally:
            set_is_loading(False)

    def handle_clear_chat(event):
        set_messages([])
        set_last_response_info({})

    return html.div(
        html.style(CSS_STYLES),
        html.div(
            {"class": "app-container"},
            # Sidebar
            html.aside(
                {"class": "sidebar"},
                html.h1("🤖 AI Chat Studio"),
                ModelSelector(
                    providers=available_providers,
                    models_by_provider=models_by_provider,
                    selected_provider=selected_provider,
                    selected_model=selected_model,
                    on_provider_change=handle_provider_change,
                    on_model_change=handle_model_change
                ),
                ParameterPanel(
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    on_change=handle_parameter_change
                ),
                html.button(
                    {"class": "clear-button", "onClick": handle_clear_chat},
                    "🗑️ Limpiar conversación"
                )
            ),
            # Main content
            html.main(
                {"class": "main-content"},
                html.h2(f"Chat con {selected_provider.capitalize()} - {selected_model}"),
                ChatInterface(
                    messages=messages,
                    on_send_message=handle_send_message,
                    is_loading=is_loading,
                    last_response_info=last_response_info
                )
            )
        )
    )


# Crear aplicación FastAPI
app = FastAPI(title="AI Chat Studio")

# Configurar ReactPy
configure(app, App)


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 AI Chat Studio")
    print("=" * 60)
    print("\nIniciando servidor en http://localhost:8000")
    print("Presiona Ctrl+C para detener\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
