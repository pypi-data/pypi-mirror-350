from typing import Optional
from typing import Callable
from typing import Union

from zenutils import importutils
from jinja2 import Environment
from jinja2 import FileSystemLoader
from django.template.loader import render_to_string
from django.template import Template
from django.template import Context

from .settings import OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE

__all__ = [
    "OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE",
    "OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE",
    "get_template_prompt_by_django_template_source_engine",
    "get_template_prompt_by_django_template_engine",
    "get_template_prompt_by_jinjia2",
    "get_template_prompt",
]

OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE = Callable[
    [
        Optional[str],  # template
        Optional[str],  # template_root
        Optional[str],  # promot
    ],
    str,  # final prompt
]
OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE_TYPE = Union[OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE, str]


def get_template_prompt_by_django_template_source_engine(
    template: Optional[str] = None,
    template_root: Optional[str] = None,
    prompt: Optional[str] = None,
    **context,
):
    """使用django源代码模板引擎生成最终提示词。

    template: 模板源代码。
    """
    tmpl = Template(template)
    return tmpl.render(
        Context(
            {
                "prompt": prompt,
                **context,
            }
        )
    )


def get_template_prompt_by_django_template_engine(
    template: Optional[str] = None,
    template_root: Optional[str] = None,
    prompt: Optional[str] = None,
    **context,
):
    """使用django模板引擎生成最终提示词。

    template: 模板文件所在路径。
    """
    return render_to_string(
        template,
        context={
            "prompt": prompt,
            **context,
        },
    )


def get_template_prompt_by_jinjia2(
    template: Optional[str] = None,
    template_root: str = None,
    prompt: str = None,
    **context,
):
    """使用jinja2模板引擎生成最终提示词。

    template: 模板文件所在路径。
    """

    template_root = template_root or "templates/"
    environment = Environment(loader=FileSystemLoader(template_root))
    tempalte = environment.get_template(template)
    return tempalte.render(prompt=prompt, **context)


def get_template_prompt(
    template: Optional[str] = None,
    prompt: str = None,
    template_root: Optional[str] = None,
    template_engine=None,
    **context,
):
    """根据提示词模板、用户问题和其它参数，生成最终的提示词。"""
    if template_engine:
        if callable(template_engine):
            return template_engine(
                template=template,
                template_root=template_root,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(template_engine)
            return template_engine(
                template=template,
                template_root=template_root,
                prompt=prompt,
                **context,
            )
    else:
        if not OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE:
            return get_template_prompt_by_django_template_engine(
                template=template,
                template_root=template_root,
                prompt=prompt,
                **context,
            )
        elif callable(OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE):
            return template_engine(
                template=template,
                template_root=template_root,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(
                OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE
            )
            return template_engine(
                template=template,
                template_root=template_root,
                prompt=prompt,
                **context,
            )
