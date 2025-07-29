import python_environment_settings

__all__ = [
    "OPENAI_BASE_URL",
    "OPENAI_API_KEY",
    "OPENAI_CHAT_MODEL",
    "OLLAMA_BASE_URL",
    "OLLAMA_API_KEY",
    "OLLAMA_CHAT_MODEL",
    "OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE",
    "OPENAI_SIMPLE_CHAT_LOGGER_NAME",
]

# 兼容openai接口
OPENAI_BASE_URL = python_environment_settings.get(
    "OPENAI_BASE_URL",
    "http://localhost/v1",
    aliases=[
        "LLM_BASE_URL",
        "BASE_URL",
    ],
)
OPENAI_API_KEY = python_environment_settings.get(
    "OPENAI_API_KEY",
    None,
    aliases=[
        "LLM_API_KEY",
        "API_KEY",
    ],
)
OPENAI_CHAT_MODEL = python_environment_settings.get(
    "OPENAI_CHAT_MODEL",
    "qwen2.5-instruct",
    aliases=[
        "OPENAI_CHAT_MODEL_NAME",
        "OPENAI_MODEL",
        "OPENAI_MODEL_NAME",
        "CHAT_MODEL",
        "CHAT_MODEL_NAME",
    ],
)


# 兼容ollama接口
OLLAMA_BASE_URL = python_environment_settings.get(
    "OLLAMA_BASE_URL",
    "http://localhost/v1",
    aliases=[
        "LLM_BASE_URL",
        "BASE_URL",
    ],
)
OLLAMA_API_KEY = python_environment_settings.get(
    "OLLAMA_API_KEY",
    None,
    aliases=[
        "LLM_API_KEY",
        "API_KEY",
    ],
)
OLLAMA_CHAT_MODEL = python_environment_settings.get(
    "OLLAMA_CHAT_MODEL",
    "qwen2.5-instruct",
    aliases=[
        "OLLAMA_CHAT_MODEL_NAME",
        "CHAT_MODEL",
        "CHAT_MODEL_NAME",
    ],
)

# 其它设置项
OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE = python_environment_settings.get(
    "OPENAI_SIMPLE_CHAT_TEMPLATE_ENGINE",
    None,
)
OPENAI_SIMPLE_CHAT_LOGGER_NAME = python_environment_settings.get(
    "OPENAI_SIMPLE_CHAT_LOGGER_NAME",
    "openai_simple_chat",
)
