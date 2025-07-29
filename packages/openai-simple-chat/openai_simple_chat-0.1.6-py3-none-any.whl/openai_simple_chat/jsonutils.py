from typing import Dict
import re
import json
import logging

__all__ = [
    "parse_json_response",
]
_logger = logging.getLogger(__name__)


def parse_json_response(text) -> Dict:
    """
    解析JSON响应文本。

    该函数尝试从给定的文本中解析出JSON对象。它会处理原始文本和转义了双引号的文本，
    并使用正则表达式去除不需要的部分（如XML标签），或者提取出Markdown代码块中的JSON内容。

    参数:
    - text: 响应文本，可能包含JSON数据。

    返回:
    - 解析得到的JSON字典，如果无法解析则返回空字典。
    """
    # 创建一个包含原始文本和转义后文本的列表，以便后续处理
    texts = [
        text,  # 原文
        text.replace("&quot;", '"'),  # 双引号转义后的json
    ]
    # 遍历文本列表，尝试解析JSON
    for text in texts:
        # 忽略deepseek的think输出
        text = re.sub("<think>.*</think>", "", text, flags=re.MULTILINE | re.S)
        # 没有格式的json
        try:
            return json.loads(text)
        except Exception:
            pass
        # 带json标识的markdown代码类型
        # 使用.+?实现最小化匹配，处理响应有多个json区块的情况
        data = re.findall("""```json(.+?)```""", text, re.MULTILINE | re.S)
        for block in data:
            try:
                return json.loads(block)
            except Exception:
                pass
        # 不带json标识的markdown代码类型
        # 使用.+?实现最小化匹配，处理响应有多个json区块的情况
        data = re.findall("""```(.+?)```""", text, re.MULTILINE | re.S)
        for block in data:
            try:
                return json.loads(block)
            except Exception:
                pass
        # 带json标识的markdown代码类型（半开）
        # 半开json后面不能有其它内容
        data = re.findall("""```json(.+)$""", text, re.MULTILINE | re.S)
        for block in data:
            try:
                return json.loads(block)
            except Exception:
                pass
        # 不带json标识的markdown代码类型（半开）
        # 半开json后面不能有其它内容
        data = re.findall("""```(.+)$""", text, re.MULTILINE | re.S)
        for block in data:
            try:
                return json.loads(block)
            except Exception:
                pass
    # 如果所有尝试都失败，返回空字典
    _logger.error("parse_json_response failed: text=%s", text)
    return {}
