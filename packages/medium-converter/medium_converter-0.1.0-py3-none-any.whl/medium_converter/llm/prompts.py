"""Prompts for LLM enhancement."""


def get_enhancement_prompt(
    text: str,
    article_title: str,
    context: str = "article text",
) -> str:
    """Get a prompt for enhancing article text.

    Args:
        text: The text to enhance
        article_title: The title of the article
        context: What part of the article this text is from

    Returns:
        Prompt string for the LLM
    """
    return f"""You are a world-class editor. Your task is to enhance the following text 
from article "{article_title}" while preserving its meaning and intent. 
Part: {context}.

THE TEXT TO ENHANCE:
{text}

Please improve this text by:
1. Fixing any grammar or spelling errors
2. Improving clarity and flow
3. Making the language more engaging and precise
4. Ensuring technical accuracy
5. Keeping a consistent style and tone

YOUR ENHANCED VERSION (respond with only the enhanced text, nothing else):"""
