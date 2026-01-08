"""
Componente selector de modelo y proveedor
=========================================

Permite seleccionar:
- Proveedor de IA (OpenAI, Anthropic, Google, Ollama)
- Modelo específico del proveedor
"""

from reactpy import component, html, hooks


@component
def ModelSelector(
    providers: list,
    models_by_provider: dict,
    selected_provider: str,
    selected_model: str,
    on_provider_change,
    on_model_change
):
    """
    Selector de proveedor y modelo.

    Args:
        providers: Lista de proveedores disponibles
        models_by_provider: Dict {provider: [(model_id, model_name), ...]}
        selected_provider: Proveedor actualmente seleccionado
        selected_model: Modelo actualmente seleccionado
        on_provider_change: Callback cuando cambia el proveedor
        on_model_change: Callback cuando cambia el modelo
    """
    # Iconos para cada proveedor
    provider_icons = {
        "openai": "🟢",
        "anthropic": "🟠",
        "google": "🔵",
        "ollama": "🦙",
    }

    provider_names = {
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "google": "Google",
        "ollama": "Ollama (Local)",
    }

    def handle_provider_change(event):
        new_provider = event["target"]["value"]
        on_provider_change(new_provider)
        # Seleccionar primer modelo del nuevo proveedor
        if new_provider in models_by_provider and models_by_provider[new_provider]:
            on_model_change(models_by_provider[new_provider][0][0])

    def handle_model_change(event):
        on_model_change(event["target"]["value"])

    # Obtener modelos del proveedor seleccionado
    available_models = models_by_provider.get(selected_provider, [])

    return html.div(
        {"class": "model-selector"},
        html.div(
            {"class": "selector-group"},
            html.label({"for": "provider-select"}, "Proveedor:"),
            html.select(
                {
                    "id": "provider-select",
                    "value": selected_provider,
                    "onChange": handle_provider_change
                },
                [
                    html.option(
                        {"value": p, "key": p},
                        f"{provider_icons.get(p, '🤖')} {provider_names.get(p, p)}"
                    )
                    for p in providers
                ]
            )
        ),
        html.div(
            {"class": "selector-group"},
            html.label({"for": "model-select"}, "Modelo:"),
            html.select(
                {
                    "id": "model-select",
                    "value": selected_model,
                    "onChange": handle_model_change
                },
                [
                    html.option({"value": model_id, "key": model_id}, model_name)
                    for model_id, model_name in available_models
                ] if available_models else [
                    html.option({"value": "", "disabled": True}, "No hay modelos disponibles")
                ]
            )
        )
    )
