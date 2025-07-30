import loguru

from app.core.llm.agent_hive_reward_generator import agent_hive_reward_generator
from app.core.llm.data_structure.reward_data_json import hive_reward_pydantic
from app.core.scheduler.core.init import global_llm
from app.core.validator.hive_reward_validator import validator


def generator_hive_reward_pydantic(original_article: str) -> hive_reward_pydantic:
    """
    通过LLM生成经过校验的hive_reward_pydantic
    :param original_article:
    :return:
    """
    with global_llm():
        hive_reward = agent_hive_reward_generator(original_article=original_article)
        validate_result = validator(original_article=original_article, hive_reward=hive_reward)
        if validate_result:
            return hive_reward
        else:
            loguru.logger.warning(f"生成的hive_reward不符合规范: {hive_reward}")
            return generator_hive_reward_pydantic(original_article=original_article)
