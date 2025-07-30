import logging
import json

from typing import List
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Generator
from typing import Any

from openai import OpenAI

from .base import ChatService
from .base import CHAT_RESPOSNE_CHUNK
from .template import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE
from .settings import OPENAI_SIMPLE_CHAT_LOGGER_NAME
from .settings import OPENAI_API_KEY
from .settings import OPENAI_BASE_URL
from .settings import OPENAI_CHAT_MODEL

__all__ = [
    "OpenAIChatService",
]
openai_simple_chat_logger = logging.getLogger(OPENAI_SIMPLE_CHAT_LOGGER_NAME)


class OpenAIChatService(ChatService):
    default_base_url = OPENAI_BASE_URL
    default_api_key = OPENAI_API_KEY
    default_model = OPENAI_CHAT_MODEL

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_context_tokens: Optional[int] = None,
        template_engine: Optional[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE] = None,
        template_root: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            max_context_tokens=max_context_tokens,
            template_engine=template_engine,
            template_root=template_root,
            **kwargs,
        )
        self.llm = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def do_chat(
        self,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_context_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        extra_messages: Optional[List[Any]] = None,
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        options = options or {}
        completions_parameters = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if temperature:
            completions_parameters["temperature"] = temperature
        if max_tokens:
            completions_parameters["max_tokens"] = max_tokens
        if options:
            completions_parameters.update(**options)
        try:
            response_info = self.llm.chat.completions.create(**completions_parameters)
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": response_info.model_dump(),
                        "error": None,
                    },
                    ensure_ascii=False,
                )
            )
        except Exception as error:
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": None,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                )
            )
            raise error
        if (not response_info) or (not response_info.choices):
            raise RuntimeError(422, f"LLM service response failed: {response_info}")
        response = response_info.choices[0].message.content
        return response, response_info.model_dump()

    def do_streaming_chat(
        self,
        prompt: Optional[str] = None,
        histories: Optional[List[Tuple[str, str]]] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_context_tokens: Optional[int] = None,
        options: Optional[Dict] = None,
        extra_messages: Optional[List[Any]] = None,
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        options = options or {}
        completions_parameters = {
            "model": model,
            "messages": messages,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if temperature:
            completions_parameters["temperature"] = temperature
        if max_tokens:
            completions_parameters["max_tokens"] = max_tokens
        if options:
            completions_parameters.update(**options)
        outputs = []
        try:
            for chunk in self.llm.chat.completions.create(**completions_parameters):
                outputs.append(chunk.model_dump())
                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):
                    delta = chunk.choices[0].delta.content
                else:
                    delta = ""
                yield delta, chunk.model_dump()
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": outputs,
                        "error": None,
                    },
                    ensure_ascii=False,
                )
            )
        except Exception as error:
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": None,
                        "error": str(error),
                    },
                    ensure_ascii=False,
                )
            )
            raise error
