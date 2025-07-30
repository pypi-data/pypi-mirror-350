import loguru
from transformers import pipeline


class RandomArticleGenerator:
    def __init__(self):
        self.generator = pipeline("text-generation", model="Qwen/Qwen3-0.6B")

    def random_article_generator(self) -> str:
        """
        Generate a random article using the random module.
        :return: A string representing the generated article.
        """
        try:
            loguru.logger.debug("Generating random article...")
            prompt = "好的，这个ctf题目应该这样解答:"
            generated_text = self.generator(prompt, max_length=256, num_return_sequences=1)
            loguru.logger.debug(f"Generated article: {generated_text[0]['generated_text'][:32]}...")
            return generated_text[0]['generated_text']
        except OSError as e:
            if 'huggingface.co' in str(e):
                raise OSError("HuggingFace源连接失败，建议使用国内源，如：\n"
                              "HF_ENDPOINT=https://hf-mirror.com script")
            else:
                raise e


if __name__ == "__main__":
    RAG = RandomArticleGenerator()
    article = RAG.random_article_generator()
    print(article)
