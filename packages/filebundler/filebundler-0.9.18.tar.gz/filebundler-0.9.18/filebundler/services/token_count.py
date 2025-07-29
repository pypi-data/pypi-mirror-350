# filebundler/services/token_count.py
import tiktoken


def compute_word_count(text: str):
    """Compute the word count in the given text"""
    # Simple word count implementation
    return len(text.split())


def count_tokens(text: str, model="o200k_base"):
    """
    Count the number of tokens in the text using tiktoken.

    Args:
        text (str): The text to count tokens for
        model (str): The tokenizer model to use (default: o200k_base for GPT-4)

    Returns:
        int: Number of tokens in the text
    """
    encoder = tiktoken.get_encoding(model)
    return len(encoder.encode(text))
