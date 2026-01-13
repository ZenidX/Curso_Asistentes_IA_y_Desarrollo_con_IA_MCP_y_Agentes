"""
Cliente unificado para múltiples APIs de IA
==========================================

Este módulo proporciona una interfaz unificada para interactuar
con diferentes proveedores de IA (OpenAI, Anthropic, Google, Ollama).
"""

import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Generator, Optional

from openai import OpenAI
import anthropic
import google.generativeai as genai
import ollama


@dataclass
class AIResponse:
    """Respuesta de una API de IA."""
    content: str
    model: str
    provider: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    error: Optional[str] = None


class AIClient:
    """Cliente unificado para múltiples APIs de IA."""

    # Modelos disponibles por proveedor
    MODELS = {
        "openai": [
            ("gpt-4o-mini", "GPT-4o Mini - Rápido y económico"),
            ("gpt-4o", "GPT-4o - Más potente"),
            ("gpt-4-turbo", "GPT-4 Turbo"),
            ("gpt-3.5-turbo", "GPT-3.5 Turbo - Más económico"),
        ],
        "anthropic": [
            ("claude-3-haiku-20240307", "Claude 3 Haiku - Rápido"),
            ("claude-3-sonnet-20240229", "Claude 3 Sonnet - Equilibrado"),
            ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet - Más reciente"),
            ("claude-3-opus-20240229", "Claude 3 Opus - Más potente"),
        ],
        "google": [
            ("gemini-1.5-flash", "Gemini 1.5 Flash - Rápido"),
            ("gemini-1.5-pro", "Gemini 1.5 Pro - Más capaz"),
        ],
        "ollama": [
            ("llama3.2", "Llama 3.2 - Ligero"),
            ("llama3.2:70b", "Llama 3.2 70B - Potente"),
            ("mistral", "Mistral 7B"),
            ("codellama", "CodeLlama - Para código"),
        ],
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Inicializa el cliente con la configuración."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

        self.config = self._load_config(config_path)
        self._init_clients()

    def _load_config(self, config_path: Path) -> dict:
        """Carga la configuración desde YAML."""
        if not config_path.exists():
            # Intentar con config.example.yaml
            example_path = config_path.parent / "config.example.yaml"
            if example_path.exists():
                config_path = example_path

        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _init_clients(self):
        """Inicializa los clientes de cada proveedor."""
        self.clients = {}

        # OpenAI
        api_key = self.config["apis"]["openai"]["api_key"]
        if api_key.startswith("sk-") and "tu-api-key" not in api_key:
            self.clients["openai"] = OpenAI(api_key=api_key)

        # Anthropic
        api_key = self.config["apis"]["anthropic"]["api_key"]
        if api_key.startswith("sk-ant") and "tu-api-key" not in api_key:
            self.clients["anthropic"] = anthropic.Anthropic(api_key=api_key)

        # Google
        api_key = self.config["apis"]["google"]["api_key"]
        if len(api_key) > 10 and "tu-api-key" not in api_key:
            genai.configure(api_key=api_key)
            self.clients["google"] = True  # Flag para indicar disponibilidad

        # Ollama
        try:
            ollama.list()
            self.clients["ollama"] = True
        except Exception:
            pass

    def get_available_providers(self) -> list:
        """Devuelve la lista de proveedores disponibles."""
        return list(self.clients.keys())

    def get_models_for_provider(self, provider: str) -> list:
        """Devuelve los modelos disponibles para un proveedor."""
        if provider == "ollama":
            # Obtener modelos instalados localmente
            try:
                response = ollama.list()
                return [(m["name"], m["name"]) for m in response["models"]]
            except Exception:
                return self.MODELS.get(provider, [])
        return self.MODELS.get(provider, [])

    def chat(
        self,
        provider: str,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: str = "Eres un asistente útil.",
    ) -> AIResponse:
        """
        Envía un mensaje y obtiene una respuesta.

        Args:
            provider: Proveedor de IA (openai, anthropic, google, ollama)
            model: ID del modelo a usar
            messages: Lista de mensajes [{role, content}]
            temperature: Creatividad (0.0-2.0)
            max_tokens: Máximo de tokens en respuesta
            system_prompt: Instrucciones del sistema

        Returns:
            AIResponse con el contenido y metadatos
        """
        if provider not in self.clients:
            return AIResponse(
                content="",
                model=model,
                provider=provider,
                error=f"Proveedor '{provider}' no configurado"
            )

        try:
            if provider == "openai":
                return self._chat_openai(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "anthropic":
                return self._chat_anthropic(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "google":
                return self._chat_google(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "ollama":
                return self._chat_ollama(model, messages, temperature, max_tokens, system_prompt)
        except Exception as e:
            return AIResponse(
                content="",
                model=model,
                provider=provider,
                error=str(e)
            )

    def _chat_openai(self, model, messages, temperature, max_tokens, system_prompt) -> AIResponse:
        """Chat con OpenAI."""
        client = self.clients["openai"]

        all_messages = [{"role": "system", "content": system_prompt}]
        all_messages.extend(messages)

        response = client.chat.completions.create(
            model=model,
            messages=all_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return AIResponse(
            content=response.choices[0].message.content,
            model=model,
            provider="openai",
            tokens_input=response.usage.prompt_tokens,
            tokens_output=response.usage.completion_tokens
        )

    def _chat_anthropic(self, model, messages, temperature, max_tokens, system_prompt) -> AIResponse:
        """Chat con Anthropic."""
        client = self.clients["anthropic"]

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        )

        return AIResponse(
            content=response.content[0].text,
            model=model,
            provider="anthropic",
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens
        )

    def _chat_google(self, model, messages, temperature, max_tokens, system_prompt) -> AIResponse:
        """Chat con Google Gemini."""
        genai_model = genai.GenerativeModel(
            model_name=model,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
            system_instruction=system_prompt
        )

        # Convertir mensajes al formato de Gemini
        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = genai_model.start_chat(history=history)
        response = chat.send_message(messages[-1]["content"])

        tokens_in = None
        tokens_out = None
        if hasattr(response, 'usage_metadata'):
            tokens_in = response.usage_metadata.prompt_token_count
            tokens_out = response.usage_metadata.candidates_token_count

        return AIResponse(
            content=response.text,
            model=model,
            provider="google",
            tokens_input=tokens_in,
            tokens_output=tokens_out
        )

    def _chat_ollama(self, model, messages, temperature, max_tokens, system_prompt) -> AIResponse:
        """Chat con Ollama."""
        all_messages = [{"role": "system", "content": system_prompt}]
        all_messages.extend(messages)

        response = ollama.chat(
            model=model,
            messages=all_messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        return AIResponse(
            content=response["message"]["content"],
            model=model,
            provider="ollama",
            tokens_input=response.get("prompt_eval_count"),
            tokens_output=response.get("eval_count")
        )

    def chat_stream(
        self,
        provider: str,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: str = "Eres un asistente útil.",
    ) -> Generator[str, None, None]:
        """
        Envía un mensaje y obtiene respuesta en streaming.

        Yields:
            Fragmentos de texto conforme se generan
        """
        if provider not in self.clients:
            yield f"Error: Proveedor '{provider}' no configurado"
            return

        try:
            if provider == "openai":
                yield from self._stream_openai(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "anthropic":
                yield from self._stream_anthropic(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "google":
                yield from self._stream_google(model, messages, temperature, max_tokens, system_prompt)
            elif provider == "ollama":
                yield from self._stream_ollama(model, messages, temperature, max_tokens, system_prompt)
        except Exception as e:
            yield f"Error: {str(e)}"

    def _stream_openai(self, model, messages, temperature, max_tokens, system_prompt):
        """Streaming con OpenAI."""
        client = self.clients["openai"]
        all_messages = [{"role": "system", "content": system_prompt}]
        all_messages.extend(messages)

        stream = client.chat.completions.create(
            model=model,
            messages=all_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def _stream_anthropic(self, model, messages, temperature, max_tokens, system_prompt):
        """Streaming con Anthropic."""
        client = self.clients["anthropic"]

        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text

    def _stream_google(self, model, messages, temperature, max_tokens, system_prompt):
        """Streaming con Google."""
        genai_model = genai.GenerativeModel(
            model_name=model,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
            system_instruction=system_prompt
        )

        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = genai_model.start_chat(history=history)
        response = chat.send_message(messages[-1]["content"], stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    def _stream_ollama(self, model, messages, temperature, max_tokens, system_prompt):
        """Streaming con Ollama."""
        all_messages = [{"role": "system", "content": system_prompt}]
        all_messages.extend(messages)

        stream = ollama.chat(
            model=model,
            messages=all_messages,
            options={"temperature": temperature, "num_predict": max_tokens},
            stream=True
        )

        for chunk in stream:
            yield chunk["message"]["content"]
