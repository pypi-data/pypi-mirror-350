from abc import abstractmethod, ABC


class Runnable(ABC):
    """可被调度的任务执行"""

    thread_id: str = ''

    def __init__(self, **kwargs):
        print('Runnable.__init__ %s' % kwargs)
        self.thread_id = kwargs.get('thread_id', '')

    @abstractmethod
    def get_context(self):
        raise NotImplemented
