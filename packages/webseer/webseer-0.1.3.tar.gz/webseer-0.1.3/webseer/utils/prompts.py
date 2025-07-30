'''
Description:  
Author: Huang J
Date: 2025-04-28 15:04:37
'''

RELATED_URL_PROMPT = """这是文本相关性分析任务。你是一个文本分析专家，请您根据文本语义判断给定的文本和目标文本是否相关，如果相关请输出1，不然输出2。

目标文本：{}

给定文本：{}
"""

RELATED_CHUNK_PROMPT = """这是文本相关性分析任务。你是一个文本分析专家，请您根据文本语义判断给定的文本和目标文本是否相关，如果相关请输出1，不然输出2。

目标文本：{}

给定文本：{}
"""


def build_prompt(query: str) -> str:
    """
    Build a conversation prompt string including system role and user input.

    Args:
        query (str): The user's input query or instruction.

    Returns:
        str: The formatted conversation prompt string.
    """
    
    return "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n{}<|im_end|>\n<|im_start|>assistant\n".format(query)
