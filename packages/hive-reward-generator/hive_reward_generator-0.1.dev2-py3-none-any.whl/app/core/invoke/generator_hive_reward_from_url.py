from app.core.invoke.generator_hive_reward import generator_hive_reward_pydantic
from app.core.invoke.io.reader import reader


def generator_hive_reward_pydantic_from_url(url: str):
    """
    根据url生成hive_reward_pydantic
    :param url: 文件或目录的url，包括http和https
    :return:
    """
    body = reader(url=url)
    return generator_hive_reward_pydantic(original_article=body)
