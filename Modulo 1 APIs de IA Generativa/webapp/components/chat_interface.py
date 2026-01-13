"""
Interfaz de chat
================

Componente principal de chat que muestra:
- Historial de mensajes
- Input para nuevo mensaje
- Información de tokens y costes
"""

from reactpy import component, html, hooks


@component
def ChatMessage(role: str, content: str):
    """Renderiza un mensaje individual del chat."""
    is_user = role == "user"

    return html.div(
        {
            "class": f"chat-message {'user-message' if is_user else 'assistant-message'}"
        },
        html.div(
            {"class": "message-header"},
            html.span(
                {"class": "message-role"},
                "👤 Tú" if is_user else "🤖 Asistente"
            )
        ),
        html.div(
            {"class": "message-content"},
            content
        )
    )


@component
def TokenInfo(tokens_input: int, tokens_output: int, provider: str):
    """Muestra información de tokens usados."""
    # Precios aproximados por 1M tokens (simplificado)
    prices = {
        "openai": {"input": 0.15, "output": 0.60},  # gpt-4o-mini
        "anthropic": {"input": 0.25, "output": 1.25},  # claude-3-haiku
        "google": {"input": 0, "output": 0},  # tier gratuito
        "ollama": {"input": 0, "output": 0},  # local
    }

    price = prices.get(provider, {"input": 0, "output": 0})
    cost_input = (tokens_input / 1_000_000) * price["input"]
    cost_output = (tokens_output / 1_000_000) * price["output"]
    total_cost = cost_input + cost_output

    return html.div(
        {"class": "token-info"},
        html.span(f"📊 Tokens: {tokens_input} entrada / {tokens_output} salida"),
        html.span(
            {"class": "cost-info"},
            f"💰 ~${total_cost:.6f}" if total_cost > 0 else "💰 Gratis"
        )
    )


@component
def ChatInterface(
    messages: list,
    on_send_message,
    is_loading: bool,
    last_response_info: dict
):
    """
    Interfaz principal de chat.

    Args:
        messages: Lista de mensajes [{role, content}]
        on_send_message: Callback cuando se envía un mensaje
        is_loading: Si está esperando respuesta
        last_response_info: Info del último response {tokens_input, tokens_output, provider}
    """
    input_value, set_input_value = hooks.use_state("")

    def handle_submit(event):
        event.preventDefault()
        if input_value.strip() and not is_loading:
            on_send_message(input_value.strip())
            set_input_value("")

    def handle_input_change(event):
        set_input_value(event["target"]["value"])

    def handle_key_press(event):
        if event.get("key") == "Enter" and not event.get("shiftKey"):
            handle_submit(event)

    return html.div(
        {"class": "chat-interface"},
        # Área de mensajes
        html.div(
            {"class": "messages-container"},
            [
                ChatMessage(msg["role"], msg["content"])
                for msg in messages
            ] if messages else [
                html.div(
                    {"class": "empty-chat"},
                    "💬 Empieza una conversación escribiendo un mensaje..."
                )
            ],
            # Indicador de carga
            html.div(
                {"class": f"loading-indicator {'visible' if is_loading else ''}"},
                "⏳ Pensando..."
            ) if is_loading else None
        ),

        # Info de tokens (si hay)
        TokenInfo(
            last_response_info.get("tokens_input", 0),
            last_response_info.get("tokens_output", 0),
            last_response_info.get("provider", "")
        ) if last_response_info.get("tokens_input") else None,

        # Formulario de entrada
        html.form(
            {"class": "chat-input-form", "onSubmit": handle_submit},
            html.textarea({
                "class": "chat-input",
                "value": input_value,
                "onChange": handle_input_change,
                "onKeyPress": handle_key_press,
                "placeholder": "Escribe tu mensaje... (Enter para enviar, Shift+Enter para nueva línea)",
                "disabled": is_loading,
                "rows": "3"
            }),
            html.button(
                {
                    "type": "submit",
                    "class": "send-button",
                    "disabled": is_loading or not input_value.strip()
                },
                "🚀 Enviar" if not is_loading else "⏳ Esperando..."
            )
        )
    )
