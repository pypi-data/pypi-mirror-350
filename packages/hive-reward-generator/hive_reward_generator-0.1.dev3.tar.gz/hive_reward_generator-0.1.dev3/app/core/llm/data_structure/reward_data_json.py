from enum import Enum
from typing import Any

from pydantic import BaseModel, validator, field_validator
from pydantic_core import core_schema


class matching_method_enum(Enum):
    """
    匹配方法枚举类
    """
    normal = "normal"
    regex = "regex"


class hive_reward_pydantic(BaseModel):
    topic: str
    checkpoint: list[dict[str, float]]
    matchingmethod: list[matching_method_enum]

    @field_validator("matchingmethod", mode="before")
    def validate_lengths(cls, matchingmethod, info):
        checkpoint = info.data.get("checkpoint")
        if checkpoint and len(checkpoint) != len(matchingmethod):
            raise ValueError("`checkpoint` and `matchingmethod` must have the same length")
        return matchingmethod


def pydantic_2_json(obj: Any) -> Any:
    """
    将 pydantic 对象转换为 JSON 可序列化的结构
    """
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, BaseModel):
        return pydantic_2_json(obj.model_dump())
    elif isinstance(obj, list):
        return [pydantic_2_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: pydantic_2_json(value) for key, value in obj.items()}
    else:
        return obj


if __name__ == '__main__':
    data = {
        "topic": "Example Topic",
        "checkpoint": [{"keyword1": 0.5}, {"keyword2": 0.5}],
        "matchingmethod": ["normal", "regex"]
    }
    hive_reward = hive_reward_pydantic(**data)
    print(hive_reward)
    print(pydantic_2_json(hive_reward))
