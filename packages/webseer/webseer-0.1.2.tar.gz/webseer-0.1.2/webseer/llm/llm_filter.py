'''
Description:  
Author: Huang J
Date: 2025-04-28 15:09:24
'''
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer
import torch
import torch.nn.functional as F

from webseer.utils.prompts import build_prompt

def llm_margin_prob(
    text1: str,
    text2: str,
    model: 'PreTrainedModel',
    tokenizer: 'PreTrainedTokenizer',
    prompt: str,
    mar_threshold: float = 0.3 
) -> bool:
    """
    Calculate the margin probability between two texts by feeding them through a language model.

    This function computes the difference in token probabilities between two input texts 
    and returns True if the difference exceeds the given margin threshold.

    Args:
        text1 (str): The first input text.
        text2 (str): The second input text.
        model (PreTrainedModel): A pre-trained language model to generate token probabilities.
        tokenizer (PreTrainedTokenizer): The tokenizer to encode the prompt.
        prompt (str): A string template for the prompt, which will be formatted with text1 and text2.
        mar_threshold (float, optional): The margin threshold to determine if the difference in probabilities is significant. Defaults to 0.3.

    Returns:
        bool: True if the probability difference between the two texts exceeds the margin threshold, False otherwise.
    """

    prompt = build_prompt(prompt.format(text1,text2))
    prompt_ids = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
    output_ids = tokenizer(['1','2'], return_tensors='pt').input_ids.to(model.device)
    
    with torch.no_grad():
        outputs = model(prompt_ids)
        next_token_logits = outputs.logits[:, -1, :]
        token_probs = F.softmax(next_token_logits, dim=-1)
        
    next_token_id_0 = output_ids[0, :].unsqueeze(0)
    next_token_prob_0 = token_probs[:, next_token_id_0].item()  
        
    next_token_id_1 = output_ids[1, :].unsqueeze(0)
    next_token_prob_1 = token_probs[:, next_token_id_1].item()  
    prob_subtract=next_token_prob_0-next_token_prob_1
    
    if prob_subtract>mar_threshold:
        return True
    else:
        return False