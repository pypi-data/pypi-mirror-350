from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class NeedRAGModel(BaseModel):
    isNeed: int = Field(description="是否需要查询资料库，1为需要，0为不需要")
    keywords: str = Field(description="空格隔开的关键词")


class TaskStatus(Enum):
    PEN = "pending"
    WOK = "working"
    ERR = "error"
    SUC = "success"

    def __str__(self):
        """
        Let the class can be JSON serialized.
        :return:
        """
        return self.value


class TaskModel(BaseModel):
    abstract: str = Field(description="任务简述")
    description: str = Field(description="任务描述")
    verification: str = Field(description="任务验证的标准（例如：是否提供了包含漏洞的返回包）")


class TaskModelOut(BaseModel):
    result_abstract: str = Field(description="任务执行结果的摘要")
    result: str = Field(description="任务执行结果的详细信息")


class TaskChainModel(BaseModel):
    tasks: List[TaskModel] = Field(description="任务列表")


class NeedBranchModel(BaseModel):
    isNeed: int = Field(description="是否需要分支，1为需要，0为不需要")
    task_chain: TaskChainModel = Field(description="子任务链")


class TaskExecuteStatusModel(BaseModel):
    is_task_successful: int = Field(description="此任务是否成功完成，1为成功，0为不成功")
    is_task_impossible: int = Field(description="如果没有成功完成，此任务以你的能力是否不可能完成，1为不可能，0为可能")
    explain: str = Field(
        description="如果不可能完成，解释不可能完成的原因。如果可能完成，说明任务应该的执行方式问题在哪，如何修正")
