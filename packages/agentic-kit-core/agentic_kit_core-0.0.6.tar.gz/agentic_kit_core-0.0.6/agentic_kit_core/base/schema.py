import datetime
from operator import add
from typing import Any, Annotated, TypedDict

from pydantic import BaseModel


class Breakpoint(BaseModel):
    id: str
    '''等于tool_call_id'''

    thread_id: str

    status: int = 0
    '''0: 未获得结果， 1: 已获得结果, 2:失败'''

    task: Any = None

    result: Any = None

    type: int = 1  # 断点类型：1：toolcall， 2:待扩展

    start_time: Any = 0

    end_time: Any = 0

    @classmethod
    def create(cls, id: str, thread_id: str, status: int = 0, task: Any = None, result: dict = None, type: int = 1):
        obj = cls(id=id, thread_id=thread_id, status=status, task=task, result=result, type=type, start_time=datetime.datetime.now().timestamp())
        return obj

    def resume(self, result: Any, status: int = 1):
        """断点完成时调用"""
        self.end_time = datetime.datetime.now().timestamp()
        self.status = status
        self.result = result


class BaseState(TypedDict):
    thread_id: str


class BaseStateInterrupt(BaseState):

    breakpoints: Annotated[list[Breakpoint], add]
    '''breakpoint_id: Breakpoint'''
