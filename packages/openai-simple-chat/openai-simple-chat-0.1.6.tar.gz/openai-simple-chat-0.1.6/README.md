# openai-simple-chat

大模型对话标准接口。支持模板对话、JSON对话等。

## 安装

```shell
pip install openai-simple-chat
```

## 环境变量配置项

- OPENAI_BASE_URL # 支持openai兼容服务
- OPENAI_API_KEY
- OPENAI_CHAT_MODEL
- OLLAMA_BASE_URL # 支持ollama兼容服务
- OLLAMA_API_KEY
- OLLAMA_CHAT_MODEL
- OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE # 其它设置
- OPENAI_SIMPLE_CHAT_LOGGER_NAME

## 使用方法

*test_templates/calc.txt*

```text
以标准json返回以下计算结果数值【输出格式为：{"result": xx}】：{{expression}}
```

*main1.py*

```python
import openai_simple_chat

llm = openai_simple_chat.OpenAIChatService(
    template_engine=openai_simple_chat.get_template_prompt_by_jinjia2,
    template_root="test_templates",
)
response, response_info = llm.jsonchat(
    template="calc.txt",
    expression="1+1",
)
assert response
assert response_info
assert isinstance(response, dict)
assert isinstance(response_info, dict)
assert "result" in response
assert response["result"] == 2

# 注意，如果是stream_chat的话，response可能为空字符串。
```

*main2.py*

```python
import openai_simple_chat

llm = openai_simple_chat.OllamaChatService(
    template_engine=openai_simple_chat.get_template_prompt_by_jinjia2,
    template_root="test_templates",
)
response, response_info = llm.jsonchat(template="calc.txt", expression="1+1")
assert response
assert response_info
assert isinstance(response, dict)
assert isinstance(response_info, dict)
assert "result" in response
assert response["result"] == 2
```

## 版本记录

### v0.1.0

- 版本首发。
- 支持模板对话。
- 支持json对话。
- 兼容openai和ollama服务。
- 兼容django和jinja2模板引擎。
- jsonchat已经对deekseek输出的`think`过程输出进行处理。

### v0.1.1

- OpenAIService服务支持max_tokens参数。

### v0.1.2

- 添加：get_template_prompt_by_django_template_source_engine提示词模板引擎。
- 改进：更灵活的服务初始化构造和调用。

### v0.1.3

- 修正：直接使用template生成提示词而无需prompt的情况下报错的问题。

### v0.1.4

- 添加：动态计算max_tokens的机制。
- 修改：移除max_input_tokens和max_output_tokens参数。
- 修正：openai的streaming_chat问题。
- 修正：ollama的对话问题。

### v0.1.5

- 优化：非标准json输出的处理，支持半开json块的解析。

### v0.1.6

- 优化：添加extra_messages参数。
