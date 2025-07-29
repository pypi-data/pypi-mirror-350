from typing import Optional
from typing import List
from typing import Tuple
from typing import Dict
from typing import Generator
from typing import Union
from typing import Any

import json

from .template import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE
from .template import get_template_prompt_by_django_template_engine
from .template import get_template_prompt
from .jsonutils import parse_json_response

__all__ = [
    "CHAT_RESPOSNE_CHUNK",
    "ChatService",
]

CHAT_RESPOSNE_CHUNK = Tuple[str, Dict]


class ChatService(object):
    default_base_url = None
    default_api_key = None
    default_model = None
    default_temperature = None
    default_system_prompt = "You are helpful assistant."
    default_top_p = None
    default_max_token = None
    default_max_context_tokens = None

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_context_tokens: Optional[int] = None,
        template_engine: Optional[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE] = None,
        template_root: Optional[str] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ):
        # 基本参数
        self.base_url = base_url or self.default_base_url
        self.api_key = api_key or self.default_api_key
        self.system_prompt = system_prompt or self.default_system_prompt
        # 对话时可重载的参数
        self.model = model or self.default_model
        self.temperature = temperature or self.default_temperature
        self.top_p = top_p or self.default_top_p
        self.max_context_tokens = max_context_tokens or self.default_max_context_tokens
        self.max_tokens = max_tokens or self.default_max_token
        # 模板引擎相关参数
        self.template_engine = (
            template_engine or get_template_prompt_by_django_template_engine
        )
        self.template_root = template_root
        # 其它未定义参数
        self.kwargs = kwargs

    def get_final_prompt(
        self,
        prompt: Optional[str] = None,
        template: Optional[str] = None,
        **context,
    ):
        """利用模板引擎，生成最终的prompt提示词。"""
        if template:
            return get_template_prompt(
                template=template,
                prompt=prompt,
                template_engine=self.template_engine,
                template_root=self.template_root,
                **context,
            )
        else:
            return prompt

    def get_messages(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        histories: Optional[List[Tuple[str, str]]] = None,
        extra_messages: Optional[List[Any]] = None,
    ):
        """将文字版的prompt转化为messages数组。

        @parameter histories: 问答记录记录:
        ```
            histories = [
                ("question1", "answer1"),
                ("question2", "answer2"),
            ]
        ```
        """
        histories = histories or []
        history_messages = []
        for history in histories:
            history_messages.append({"role": "user", "content": history[0]})
            history_messages.append({"role": "assistant", "content": history[1]})

        if isinstance(prompt, str):
            result = [
                {"role": "system", "content": self.system_prompt},
            ]
            result += history_messages
            result += extra_messages
            result += [
                {"role": "user", "content": prompt},
            ]
        else:
            result = prompt[:1] + history_messages + extra_messages + prompt[1:]
        return result

    def get_input_tokens(self, messages, model):
        """近似计算用户输入的tokens。"""
        return json.dumps(messages) + 2

    def get_max_tokens(self, max_context_tokens, messages, model):
        """服务要求控制最大上下文长度（输入+输出）。

        由于无法快速计算出实际的输入长度，这里采用近似方法进行处理。
        """
        return max_context_tokens - self.get_input_tokens(messages, model)

    def chat(
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
        """对话功能。

        1、messages或prompt+histories二选一。
        2、max_context_tokens用于部分服务限制了输入+输出的总长度。
        """
        # 根据模板生成prompt最终版
        if prompt or template:
            prompt = self.get_final_prompt(
                prompt=prompt,
                template=template,
                **context,
            )
        # 生成最终的messages
        messages = messages or self.get_messages(
            prompt=prompt,
            histories=histories,
            extra_messages=extra_messages,
        )
        # 计算最终的可重载参数
        model = model or self.model
        temperature = temperature or self.temperature
        top_p = top_p or self.top_p
        max_context_tokens = max_context_tokens or self.max_context_tokens
        max_tokens = max_tokens or self.max_tokens
        if max_context_tokens and (not max_tokens):
            max_tokens = self.get_max_tokens(max_context_tokens, messages)
        # 调用服务
        return self.do_chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            max_context_tokens=max_context_tokens,
            options=options,
            **context,
        )

    def streaming_chat(
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
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        """messages或prompt+histories二选一"""
        # 根据模板生成prompt最终版
        if prompt or template:
            prompt = self.get_final_prompt(
                prompt=prompt,
                template=template,
                **context,
            )
        # 生成最终的messages
        messages = messages or self.get_messages(
            prompt=prompt,
            histories=histories,
        )
        # 计算最终的可重载参数
        model = model or self.model
        temperature = temperature or self.temperature
        top_p = top_p or self.top_p
        max_context_tokens = max_context_tokens or self.max_context_tokens
        max_tokens = max_tokens or self.max_tokens
        if max_context_tokens and (not max_tokens):
            max_tokens = self.get_max_tokens(max_context_tokens, messages)
        # 调用服务
        for chunk in self.do_streaming_chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            max_context_tokens=max_context_tokens,
            options=options,
            **context,
        ):
            yield chunk

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
        **context,
    ) -> CHAT_RESPOSNE_CHUNK:
        raise NotImplementedError()

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
        **context,
    ) -> Generator[CHAT_RESPOSNE_CHUNK, None, None]:
        raise NotImplementedError()

    def jsonchat(
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
        **context,
    ) -> Dict:
        response, response_info = self.chat(
            messages=messages,
            prompt=prompt,
            histories=histories,
            template=template,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            max_context_tokens=max_context_tokens,
            options=options,
            **context,
        )
        return parse_json_response(response), response_info
