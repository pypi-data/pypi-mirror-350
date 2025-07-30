'''
Description:  
Author: Huang J
Date: 2025-05-06 09:35:22
'''
from typing import Optional, Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer
from webseer.utils.util import clean_html

def read_html(
    html: str,
    readerlm: Optional['PreTrainedModel'] = None,
    readertokenizer: Optional['PreTrainedTokenizer'] = None,
    instruction: Optional[str] = None,  
    schema: Optional[Dict[str, Any]] = None, 
    clean_svg: bool = True, 
    clean_base64: bool = True  
) -> str:
    """
    Cleans the provided HTML and uses ReaderLM to extract structured information based on a specified schema.

    Args:
        html (str): The raw HTML content to be processed.
        readerlm (Optional['PreTrainedModel']): The ReaderLM model used for extraction.
        readertokenizer (Optional['PreTrainedTokenizer']): The ReaderTokenizer used for tokenizing the input.
        instruction (Optional[str], optional): Custom instruction for extracting structured data (default is None).
        schema (Optional[Dict[str, Any]], optional): The schema for the expected output (default is None).
        clean_svg (bool, optional): Flag to clean SVG data from HTML (default is True).
        clean_base64 (bool, optional): Flag to clean base64 encoded data (default is True).

    Returns:
        str: The extracted and structured information as a JSON string.
    
    Raises:
        Exception: If either instruction or schema is None when one is provided.
    """
    html = clean_html(html=html,clean_svg=clean_svg,clean_base64=clean_base64)
    
    if instruction is None and schema is None:
        
        instruction = 'Extract the specified information from a list of news threads and present it in a structured JSON format.'
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "News thread title"},
                "content": {"type": "string", "description": "Article content,not summary"},
                "author": {"type": "string", "description": "Thread author"},
                "date":{"type":"string","description":"Article public date"}
            },
            "required": ["title", "content", "author", "date"]
        }
        
    elif instruction is None or schema is None:
        raise Exception("Check the parameters: 'instruction' and 'schema'")
    
    prompt = f"{instruction}\n```html\n{html}\n```\nThe JSON schema is as follows:```json{schema}```"
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    input_prompt = readertokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = readertokenizer.encode(input_prompt, return_tensors="pt").to(readerlm.device)
    outputs = readerlm.generate(
        inputs, max_new_tokens=102400, temperature=0, do_sample=False, repetition_penalty=1.08
    )
    
    return readertokenizer.decode(outputs[0])
    
    
    
    
        
    








