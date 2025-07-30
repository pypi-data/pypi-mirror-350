import loguru

from app.core.llm.data_structure.reward_data_json import hive_reward_pydantic, pydantic_2_json
from app.core.validator.article_generator.random_article_generator import RandomArticleGenerator
from app.core.validator.hive_reward_parser import parse_hive_reward
from app.core.validator.valid_hive_reward_json import validate_hive_reward_pydantic


def validator(original_article: str, hive_reward: hive_reward_pydantic) -> bool:
    """
    校验hive_reward是否符合数据集规范
    校验方法:
        1. 检查hive_reward是否符合数据集规范
        2. 使用hive_reward_pydantic对原文章进行解析，看是否可以获得满分
        3. 使用hive_reward_pydantic对随机生成的文章进行解析，看是否可以获得零分
    :param original_article:
    :param hive_reward:
    :return:
    """
    validate_hive_reward_pydantic(hive_reward)
    full_score_check_result = full_score_check(original_article, hive_reward)
    zero_score_check_result = zero_score_check(hive_reward)
    loguru.logger.debug(f"full_score_check_result: {full_score_check_result}")
    loguru.logger.debug(f"zero_score_check_result: {zero_score_check_result}")
    if full_score_check_result and zero_score_check_result:
        return True
    return False


def full_score_check(original_article: str, hive_reward: hive_reward_pydantic) -> bool:
    """
    校验hive_reward对原始文章的解析是否满分
    :param original_article:
    :param hive_reward:
    :return:
    """
    postive_article = original_article  # 正样本
    score = parse_hive_reward(pydantic_2_json(hive_reward), postive_article)
    loguru.logger.debug(f"full_score_check: {score}")
    if score == 0.0:
        return True
    return False


def zero_score_check(hive_reward: hive_reward_pydantic) -> bool:
    """
    校验hive_reward对随机生成的文章的解析是否零分
    :param hive_reward:
    :return:
    """
    RAG = RandomArticleGenerator()
    negative_article = RAG.random_article_generator()  # 负样本
    score = parse_hive_reward(pydantic_2_json(hive_reward), negative_article)
    loguru.logger.debug(f"zero_score_check: {score}")
    if score == -1.0:
        return True
    return False
