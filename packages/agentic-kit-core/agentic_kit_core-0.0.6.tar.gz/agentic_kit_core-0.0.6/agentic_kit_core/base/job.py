import base64
import datetime
import uuid
from enum import StrEnum
from typing import Optional, Any

from pydantic import BaseModel, Field


class JobStatusEnum(StrEnum):
    """
    READY -> RUNNING -> SUSPENDED -> RUNNING
                     -> COMPLETED
                     -> TERMINATED
    """
    READY = 'ready'
    RUNNING = 'running'
    SUSPENDED = 'suspended'  # waiting wakeup
    COMPLETED = 'completed'  # success
    TERMINATED = 'terminated'  # error


class Job(BaseModel):
    """可被调度的任务"""

    thread_id: str = Field(
        default_factory=uuid.uuid4,
        frozen=True,
        description="Unique identifier for the object, not set by user.",
    )

    # graph初始化状态，恢复时使用
    thread_config: Any
    is_stream: bool = True
    stream_mode: str = 'updates'
    init_state: Any

    parent_thread_id: Optional[str] = Field(
        default='', description="父任务id，可为空。比如在某个workflow中，可以溯源回去"
    )
    '''父任务id，可为空。比如在某个workflow中，可以溯源回去'''

    status: JobStatusEnum = JobStatusEnum.READY

    start_time: Optional[datetime.datetime] = Field(
        default=None, description="Start time of the task execution"
    )
    end_time: Optional[datetime.datetime] = Field(
        default=None, description="End time of the task execution"
    )

    runnable: Any = None
    '''运行主体，graph'''

    def dump(self, dump_only=True, dump_runnable=False):
        print('=====Job.dump=====')
        print(f'thread_id = {self.thread_id}')
        print(f'thread_config = {self.thread_config}')
        print(f'parent_thread_id = {self.parent_thread_id}')
        print(f'status = {self.status}')
        print(f'start_time = {self.start_time}')
        print(f'end_time = {self.end_time}')
        print(f'runnable = {self.runnable.__class__}')

        if not dump_only:
            return {
                'thread_id': self.thread_id,
                'thread_config': self.thread_config,
                'parent_thread_id': self.parent_thread_id,
                'status': self.status,
                'start_time': self.start_time.timestamp(),
                'end_time': self.end_time.timestamp(),
                'runnable': {
                    'repr': repr(self.runnable),
                    'png': 'data:image/png;base64,%s' % base64.b64encode(self.runnable.get_graph().draw_mermaid_png()).decode("utf-8")
                } if dump_runnable else {}
            }
