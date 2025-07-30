from django.test import TestCase
from openai_simple_chat import OpenAIChatService
from openai_simple_chat import get_template_prompt_by_django_template_engine
from openai_simple_chat import get_template_prompt_by_django_template_source_engine


class TestOpenAIChatService(TestCase):
    def test_1(self):
        llm = OpenAIChatService(
            template_engine=get_template_prompt_by_django_template_engine,
        )
        response, info = llm.jsonchat(
            prompt="1+1=?",
            template="examples/plus1.md",
        )
        assert response["result"] == 2

    def test_2(self):
        llm = OpenAIChatService(
            template_engine=get_template_prompt_by_django_template_source_engine,
        )
        template = """请以标准json返回以下计算结果，以result字段表示：{{prompt}}"""
        response, info = llm.jsonchat(
            prompt="1+1=?",
            template=template,
        )
        assert response["result"] == 2

    def test_3(self):
        llm = OpenAIChatService(
            template_engine=get_template_prompt_by_django_template_source_engine,
        )
        template = """请以标准json返回以下计算结果，以result字段表示：{{expression}}"""
        response, info = llm.jsonchat(
            expression="1+1=?",
            template=template,
        )
        assert response["result"] == 2
