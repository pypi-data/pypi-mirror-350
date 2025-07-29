import logging
import json

from typing import List
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Generator
from typing import Any

from ollama import chat as ollama_chat

from .base import ChatService
from .base import CHAT_RESPOSNE_CHUNK
from .template import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE
from .settings import OPENAI_SIMPLE_CHAT_LOGGER_NAME
from .settings import OLLAMA_API_KEY
from .settings import OLLAMA_BASE_URL
from .settings import OLLAMA_CHAT_MODEL

__all__ = [
    "OllamaChatService",
]
openai_simple_chat_logger = logging.getLogger(OPENAI_SIMPLE_CHAT_LOGGER_NAME)


class OllamaChatService(ChatService):
    default_base_url = OLLAMA_BASE_URL
    default_api_key = OLLAMA_API_KEY
    default_model = OLLAMA_CHAT_MODEL

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
            template_engine=template_engine,
            template_root=template_root,
            **kwargs,
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
        # 特殊处理ollama的options参数
        # @todo: num_ctx
        inner_options = {}
        if temperature:
            inner_options["temperature"] = temperature
        if max_tokens:
            inner_options["num_predict"] = max_tokens
        if "options" in options:
            inner_options.update(options["options"])
            del options["options"]
        completions_parameters = {
            "model": self.model,
            "messages": messages,
            "options": inner_options,
            "stream": False,
        }
        if options:
            completions_parameters.update(options)
        try:
            print("completions_parameters=", completions_parameters)
            result_info = ollama_chat(**completions_parameters)
            print("result_info=", result_info)
            openai_simple_chat_logger.warning(
                json.dumps(
                    {
                        "base_url": self.base_url,
                        "request": completions_parameters,
                        "response": result_info.model_dump(),
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
        response = result_info.message.content
        return response, result_info.model_dump()

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
        # 特殊处理ollama的options参数
        inner_options = {}
        if temperature:
            inner_options["temperature"] = temperature
        if max_tokens:
            inner_options["num_predict"] = max_tokens
        if "options" in options:
            inner_options.update(options["options"])
            del options["options"]
        completions_parameters = {
            "model": self.model,
            "messages": messages,
            "options": inner_options,
            "stream": True,
        }
        if options:
            completions_parameters.update(options)
        try:
            # 与OLLAMA对话
            outputs = []
            for chunk in ollama_chat(**completions_parameters):
                outputs.append(chunk.model_dump())
                delta = chunk.message.content
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
