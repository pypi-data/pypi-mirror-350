"""Content enhancement using LLMs."""

from ..core.models import Article, ContentBlock, Section
from .config import LLMConfig
from .prompts import get_enhancement_prompt
from .providers import get_llm_client


async def enhance_article(article: Article, config: LLMConfig | None = None) -> Article:
    """Enhance an article using LLM.

    Args:
        article: The article to enhance
        config: Optional LLM configuration

    Returns:
        Enhanced article
    """
    if config is None:
        config = LLMConfig.from_env()

    llm = get_llm_client(config)

    # Create a copy of the article to avoid modifying the original
    enhanced_article = article.model_copy(deep=True)

    # Process each content block through the LLM
    for item_index, item in enumerate(enhanced_article.content):
        if isinstance(item, Section):
            for block_index, block in enumerate(item.blocks):
                if block.type.value == "text":
                    # Enhance text blocks only
                    prompt = get_enhancement_prompt(
                        text=block.content,
                        article_title=article.title,
                        context="section text",
                    )

                    try:
                        enhanced_text = await llm.generate(prompt)
                        # Use a type check to satisfy mypy
                        content_item = enhanced_article.content[item_index]
                        if isinstance(content_item, Section):
                            content_item.blocks[block_index].content = enhanced_text
                    except Exception as e:
                        # Log error but continue with original content
                        print(f"Error enhancing content: {e}")

        elif isinstance(item, ContentBlock) and item.type.value == "text":
            prompt = get_enhancement_prompt(
                text=item.content, article_title=article.title, context="article text"
            )

            try:
                enhanced_text = await llm.generate(prompt)
                # Use a type check to satisfy mypy
                content_item = enhanced_article.content[item_index]
                if isinstance(content_item, ContentBlock):
                    content_item.content = enhanced_text
            except Exception as e:
                # Log error but continue with original content
                print(f"Error enhancing content: {e}")

    return enhanced_article
