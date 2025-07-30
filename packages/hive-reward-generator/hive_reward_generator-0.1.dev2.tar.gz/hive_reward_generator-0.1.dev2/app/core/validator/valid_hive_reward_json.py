import math

from app.core.llm.data_structure.reward_data_json import hive_reward_pydantic, pydantic_2_json
from app.core.validator.hive_reward_parser import check_hive_reward_json_valid


def validate_hive_reward_pydantic(hive_reward: hive_reward_pydantic):
    """
    校验 .hive-reward.json 文件是否符合 HIVE-REWARD-DATASET 规范
    :param hive_reward:
    :return: None
    """
    check_hive_reward_json_valid(pydantic_2_json(hive_reward))
