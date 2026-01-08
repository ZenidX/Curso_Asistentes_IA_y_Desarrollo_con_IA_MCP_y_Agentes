"""
Panel de parámetros de generación
=================================

Controles para ajustar:
- Temperature
- Max tokens
- Top P
- Frequency penalty
- Presence penalty
"""

from reactpy import component, html


@component
def ParameterPanel(
    temperature: float,
    max_tokens: int,
    top_p: float,
    frequency_penalty: float,
    presence_penalty: float,
    on_change
):
    """
    Panel de parámetros ajustables.

    Args:
        temperature: Valor actual de temperature
        max_tokens: Valor actual de max_tokens
        top_p: Valor actual de top_p
        frequency_penalty: Valor actual de frequency_penalty
        presence_penalty: Valor actual de presence_penalty
        on_change: Callback(param_name, new_value)
    """

    def create_slider(name, label, value, min_val, max_val, step, description):
        """Crea un slider con etiqueta y valor."""

        def handle_change(event):
            new_value = float(event["target"]["value"])
            on_change(name, new_value)

        return html.div(
            {"class": "parameter-item"},
            html.div(
                {"class": "parameter-header"},
                html.label({"for": f"param-{name}"}, label),
                html.span({"class": "parameter-value"}, f"{value:.2f}" if isinstance(value, float) else str(value))
            ),
            html.input({
                "type": "range",
                "id": f"param-{name}",
                "min": str(min_val),
                "max": str(max_val),
                "step": str(step),
                "value": str(value),
                "onChange": handle_change,
                "class": "parameter-slider"
            }),
            html.p({"class": "parameter-description"}, description)
        )

    def create_number_input(name, label, value, min_val, max_val, step, description):
        """Crea un input numérico."""

        def handle_change(event):
            try:
                new_value = int(event["target"]["value"])
                on_change(name, new_value)
            except ValueError:
                pass

        return html.div(
            {"class": "parameter-item"},
            html.div(
                {"class": "parameter-header"},
                html.label({"for": f"param-{name}"}, label),
            ),
            html.input({
                "type": "number",
                "id": f"param-{name}",
                "min": str(min_val),
                "max": str(max_val),
                "step": str(step),
                "value": str(value),
                "onChange": handle_change,
                "class": "parameter-number"
            }),
            html.p({"class": "parameter-description"}, description)
        )

    return html.div(
        {"class": "parameter-panel"},
        html.h3("Parámetros de Generación"),
        create_slider(
            "temperature",
            "Temperature",
            temperature,
            0.0, 2.0, 0.1,
            "Controla la creatividad. 0 = determinista, 2 = muy creativo."
        ),
        create_number_input(
            "max_tokens",
            "Max Tokens",
            max_tokens,
            1, 4096, 1,
            "Límite máximo de tokens en la respuesta."
        ),
        create_slider(
            "top_p",
            "Top P",
            top_p,
            0.0, 1.0, 0.05,
            "Nucleus sampling. Alternativa a temperature."
        ),
        create_slider(
            "frequency_penalty",
            "Frequency Penalty",
            frequency_penalty,
            -2.0, 2.0, 0.1,
            "Penaliza tokens según frecuencia de aparición."
        ),
        create_slider(
            "presence_penalty",
            "Presence Penalty",
            presence_penalty,
            -2.0, 2.0, 0.1,
            "Penaliza tokens que ya aparecieron."
        ),
    )
